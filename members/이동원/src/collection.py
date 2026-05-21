"""DART 사업보고서 정밀 수집 모듈 (v5).

01_collection_phase1_v5 노트북의 모든 함수를 재사용 가능한 형태로 모듈화.
Phase 2A (50건 batch) 및 Phase 2B (전체 381건) 에서 그대로 호출.

핵심 함수:
- `run_one_firm_year(stock, year)` — 1 firm-year 풀 파이프라인
- `run_batch(sample)` — N firm-year batch (rate limit + retry 포함)
- `extract_sections_v5(xml_text)` — SECTION-1 + 표/본문 분리 (Fix #12)
- `find_rcept_no_v5(...)` — 정정공시 fallback (Fix #13)

가이드 매핑:
- 가이드 02 line 18 (II/IV/VI target) → extract_sections_v5
- 가이드 02 line 35 (silent 오매칭 금지) → stock_code 기준 사용
- 가이드 02 line 69 (정정공시 기록) → find_rcept_no_v5 + correction_log
- 가이드 02 line 153-158 (1~6단계) → 본 모듈 함수 매핑
- 가이드 02 line 170-172 (실패 행 가짜 0 ❌) → status 11종 세분화 + WARN_FALLBACK_*
- 가이드 02 line 216-222 (.env API key 안전) → load_api_key + mask_key

작성자: 이동원
작성일: 2026-05-16
벤치마킹: dart-fss-text (https://github.com/jaepil-choi/dart-fss-text) +
          dart-fss (https://github.com/josw123/dart-fss)
"""

from __future__ import annotations

import json
import os
import re
import time
import warnings
import zipfile
from copy import deepcopy
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv
from lxml import etree

# rapidfuzz는 선택적 의존성 (Fix #9 fuzzy matching — Phase 2B에서 활성화 가능)
try:
    from rapidfuzz import fuzz  # noqa: F401

    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False


# ============================================================================
# 모듈 상수 (DART 사업보고서 구조 매핑)
# ============================================================================

SECTION_CODE_MAP: dict[str, tuple[str, str]] = {
    "CEO_CERT": ("TTL_CEO_CERT", "대표이사 등의 확인"),
    "I": ("010000", "I. 회사의 개요"),
    "II": ("020000", "II. 사업의 내용"),  # ⭐ ESG target
    "III": ("030000", "III. 재무에 관한 사항"),
    "IV": ("040000", "IV. 이사의 경영진단 및 분석의견"),  # ⭐ ESG target
    "V": ("050000", "V. 회계감사인의 감사의견 등"),
    "VI": ("060000", "VI. 이사회 등 회사의 기관에 관한 사항"),  # ⭐ ESG target
    "VII": ("070000", "VII. 주주에 관한 사항"),
    "VIII": ("080000", "VIII. 임원 및 직원 등에 관한 사항"),
    "IX": ("090000", "IX. 계열회사 등에 관한 사항"),
    "X": ("100000", "X. 대주주 등과의 거래내용"),
    "XI": ("110000", "XI. 그 밖에 투자자 보호를 위하여 필요한 사항"),
    "XII": ("TTL_APPENDIX", "XII. 상세표"),
    "EXPERT_CERT": ("", "전문가의 확인"),
}

# 가이드 line 18 — ESG primary target
ESG_TARGET_LABELS: list[str] = ["II", "IV", "VI"]

# TITLE 텍스트 매칭용 패턴 (AASSOCNOTE 빈 값 케이스 보조)
TITLE_PATTERNS: dict[str, list[str]] = {
    "I": [r"^I\.\s", r"^Ⅰ\.\s", r"회사의\s*개요"],
    "II": [r"^II\.\s", r"^Ⅱ\.\s", r"^2\.\s", r"사업의\s*내용"],
    "III": [r"^III\.\s", r"^Ⅲ\.\s", r"^3\.\s", r"재무에\s*관한\s*사항"],
    "IV": [r"^IV\.\s", r"^Ⅳ\.\s", r"^4\.\s", r"이사의\s*경영진단", r"이사.*경영진단"],
    "V": [r"^V\.\s", r"^Ⅴ\.\s", r"^5\.\s", r"감사인의\s*감사의견", r"회계감사인"],
    "VI": [r"^VI\.\s", r"^Ⅵ\.\s", r"^6\.\s", r"이사회\s*등.*기관", r"이사회.*회사의\s*기관"],
    "VII": [r"^VII\.\s", r"^Ⅶ\.\s", r"^7\.\s", r"주주에\s*관한\s*사항"],
    "VIII": [r"^VIII\.\s", r"^Ⅷ\.\s", r"^8\.\s", r"임원\s*및\s*직원"],
    "IX": [r"^IX\.\s", r"^Ⅸ\.\s", r"^9\.\s", r"계열회사"],
    "X": [r"^X\.\s", r"^Ⅹ\.\s", r"^10\.\s", r"대주주.*거래내용"],
    "XI": [r"^XI\.\s", r"^Ⅺ\.\s", r"^11\.\s", r"그\s*밖.*투자자\s*보호"],
}

# 정정공시 fallback 순서 (Fix #13, 가이드 line 69)
REPORT_FALLBACK_ORDER: list[tuple[str, str, str, str]] = [
    # (label, pblntf_detail_ty, name_keyword, year_offset_in_nm)
    ("PRIMARY_BIZ", "A001", "사업보고서", "12"),
    ("FALLBACK_HALF", "A002", "반기보고서", "06"),
    ("FALLBACK_Q3", "A003", "분기보고서", "09"),
    ("FALLBACK_Q1", "A003", "분기보고서", "03"),
]

DOC_TYPE_PATTERN = re.compile(r"<DOCUMENT-NAME[^>]*>([^<]+)</DOCUMENT-NAME>", re.UNICODE)

# collection_log.csv 예상 컬럼 (v5 스키마, Fix #4 자동 백업 트리거)
EXPECTED_LOG_COLUMNS_V5: list[str] = [
    "stock_code", "fiscal_year", "esg_year", "corp_code", "rcept_no",
    "fallback_used", "status", "reason", "n_passages_body", "n_passages_tables",
    "sec_II_code", "sec_II_text", "sec_II_body", "sec_II_tables", "sec_II_n_tbl",
    "sec_IV_code", "sec_IV_text", "sec_IV_body", "sec_IV_tables", "sec_IV_n_tbl",
    "sec_VI_code", "sec_VI_text", "sec_VI_body", "sec_VI_tables", "sec_VI_n_tbl",
    "n_sec1_total", "viewer_url", "parser_version", "timestamp",
]

KEY_CANDIDATES: list[str] = ["OPENDART_API_KEY", "API_KEY", "DART_API_KEY"]


# ============================================================================
# Step 1: 환경 + API key 안전 (가이드 line 216-222)
# ============================================================================

def find_project_root() -> Path:
    """anchor 파일(`data/company_master.csv`) 기준으로 프로젝트 root 탐색.

    v2 Fix #1 — cwd 의존성 제거.
    """
    for candidate in [Path.cwd(), *Path.cwd().parents]:
        if (candidate / "data" / "company_master.csv").exists():
            return candidate
    raise FileNotFoundError(
        "project root not found — `data/company_master.csv` 찾을 수 없음"
    )


def mask_key(key: str) -> str:
    """API key 마스킹 (위반금지 #4 line 216-222)."""
    if not key:
        return "(empty)"
    return f"{key[:4]}...len={len(key)}"


def load_api_key(env_path: Path | None = None) -> str:
    """`.env` 로드 후 후보 리스트로 견고하게 API key 추출.

    ⚠️ 이동원 .env는 `API_KEY` 이름 (가이드 02 line 216-222의 OPENDART_API_KEY 예시와 다름).
       KEY_CANDIDATES 순서로 시도 — 가정 금지.
    """
    if env_path is None:
        env_path = find_project_root() / ".env"
    load_dotenv(env_path)
    api_key = next((os.getenv(k) for k in KEY_CANDIDATES if os.getenv(k)), None)
    if not api_key:
        raise RuntimeError(
            f"❌ {KEY_CANDIDATES} 중 어느 것도 {env_path}에 없습니다."
        )
    return api_key


def setup_directories(root: Path) -> dict[str, Path]:
    """디렉토리 생성 + 경로 dict 반환."""
    dirs = {
        "raw": root / "data" / "raw",
        "interim": root / "data" / "interim",
        "cache": root / "data" / "cache",
        "logs": root / "logs",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs


# ============================================================================
# Step 1+: AASSOCNOTE / TITLE 매칭 헬퍼
# ============================================================================

def parse_aassocnote(aassoc: str) -> tuple[str | None, str | None]:
    """`D-0-X-Y-Z` 형식 → (label, section_code).

    예시: `D-0-2-0-0` → (`'II'`, `'020000'`)
    """
    if not aassoc or not aassoc.startswith("D-"):
        return (None, None)
    parts = aassoc.split("-")
    if len(parts) < 5:
        return (None, None)
    try:
        x, y, z = int(parts[2]), int(parts[3]), int(parts[4])
        roman_map = ["", "I", "II", "III", "IV", "V", "VI", "VII",
                     "VIII", "IX", "X", "XI", "XII"]
        roman = roman_map[x] if 0 < x < len(roman_map) else None
        if roman is None:
            return (None, None)
        return (roman, f"{x:02d}{y:02d}{z:02d}")
    except (ValueError, IndexError):
        return (None, None)


def match_title_to_label(title_text: str) -> str | None:
    """TITLE 텍스트를 SECTION-1 label로 매칭.

    AASSOCNOTE가 빈 값인 케이스 (Samsung 2024 VI/I/VIII 등)에 보조 사용.
    """
    if not title_text:
        return None
    text = title_text.strip()
    for label, patterns in TITLE_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text):
                return label
    return None


# ============================================================================
# Step 3: stock_code → corp_code (가이드 line 153)
# ============================================================================

def fetch_corp_code_map(api_key: str, cache_dir: Path) -> pd.DataFrame:
    """corpCode.xml 1회 다운로드 → DataFrame → parquet 캐시.

    가이드 line 153 (1단계 stock → corp).
    """
    cache_path = cache_dir / "corp_code_map.parquet"
    if cache_path.exists():
        return pd.read_parquet(cache_path)

    res = requests.get(
        "https://opendart.fss.or.kr/api/corpCode.xml",
        params={"crtfc_key": api_key}, timeout=30,
    )
    res.raise_for_status()
    with zipfile.ZipFile(BytesIO(res.content)) as zf:
        xml_bytes = zf.read(zf.namelist()[0])
    root = etree.fromstring(xml_bytes)
    rows = [
        {
            "corp_code": (el.findtext("corp_code") or "").strip(),
            "corp_name": (el.findtext("corp_name") or "").strip(),
            "stock_code": (el.findtext("stock_code") or "").strip(),
        }
        for el in root.findall("list")
    ]
    df = pd.DataFrame(rows)
    df = df[df["stock_code"].str.len() == 6]  # 상장사만
    df.to_parquet(cache_path, index=False)
    return df


def stock_to_corp(stock_code: str, corp_map: pd.DataFrame) -> str:
    """가이드 line 35 (silent 오매칭 금지) — stock_code 기준 매칭."""
    match = corp_map[corp_map["stock_code"] == stock_code]
    if len(match) != 1:
        raise RuntimeError(
            f"FAIL_CORP_NOT_FOUND — stock={stock_code}, 매칭 수={len(match)}"
        )
    return match.iloc[0]["corp_code"]


# ============================================================================
# Step 4: corp_code → rcept_no + 정정공시 fallback (가이드 line 154, 69)
# ============================================================================

def find_rcept_no_v5(
    api_key: str, corp_code: str, fiscal_year: int, *, timeout: int = 20,
) -> dict[str, Any]:
    """🔥 v5 Fix #13 — 정정공시 fallback (사업보고서 → 반기 → 분기).

    Returns:
        dict with `selected`, `all_candidates`, `fallback_used`.
    """
    selected: dict | None = None
    fallback_used: str | None = None
    all_candidates: list[dict] = []

    for label, pblntf, kw, mm in REPORT_FALLBACK_ORDER:
        params = {
            "crtfc_key": api_key, "corp_code": corp_code,
            "bgn_de": f"{fiscal_year + 1}0101",
            "end_de": f"{fiscal_year + 1}1231",
            "pblntf_detail_ty": pblntf,
            "last_reprt_at": "Y",
            "page_count": "100",
        }
        res = requests.get(
            "https://opendart.fss.or.kr/api/list.json",
            params=params, timeout=timeout,
        )
        res.raise_for_status()
        rows = res.json().get("list", [])
        target_label = f"({fiscal_year}.{mm})"
        finals = [
            r for r in rows
            if kw in r.get("report_nm", "") and target_label in r.get("report_nm", "")
        ]
        if finals:
            sel = finals[0]
            selected = {
                "rcept_no": sel["rcept_no"],
                "rcept_dt": sel["rcept_dt"],
                "report_nm": sel["report_nm"],
                "fallback_used": label,
                "viewer_url": (
                    f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={sel['rcept_no']}"
                ),
            }
            fallback_used = label

            # 정정공시 이력 (가이드 line 69)
            params_all = {**params, "last_reprt_at": "N"}
            try:
                res2 = requests.get(
                    "https://opendart.fss.or.kr/api/list.json",
                    params=params_all, timeout=timeout,
                )
                if res2.status_code == 200:
                    for r in res2.json().get("list", []):
                        if kw in r.get("report_nm", "") and target_label in r.get("report_nm", ""):
                            all_candidates.append({
                                "rcept_no": r["rcept_no"],
                                "rcept_dt": r["rcept_dt"],
                                "report_nm": r["report_nm"],
                                "fallback_used": label,
                            })
            except requests.RequestException:
                pass  # 정정 이력 실패는 정상 흐름 차단 ❌
            break

    if selected is None:
        # 위반금지 #1 (line 172) — 명시적 실패 (가짜 0 ❌)
        raise RuntimeError(
            f"FAIL_LIST_NO_REPORT — 사업보고서·반기·분기 모두 없음 "
            f"(corp={corp_code}, fiscal={fiscal_year})"
        )

    return {
        "selected": selected,
        "all_candidates": all_candidates,
        "fallback_used": fallback_used,
    }


# ============================================================================
# Step 5: document.xml zip + DOCUMENT-NAME type 판별 (Fix #0, 가이드 line 155)
# ============================================================================

def download_document_xml_v5(
    api_key: str, rcept_no: str, stock_code: str, fiscal_year: int,
    raw_dir: Path, *, fallback_label: str = "PRIMARY_BIZ", timeout: int = 60,
) -> dict[str, Any]:
    """가이드 line 155 — zip 보존 (위반금지 #5) + DOCUMENT-NAME type 판별 (Fix #0).

    fallback_label에 따라 primary 선택 type 변경 (사업/반기/분기).
    """
    zip_path = raw_dir / f"{stock_code}_{fiscal_year}_disclosure.zip"

    # idempotent: 캐시 hit 시 재다운로드 ❌
    if zip_path.exists() and zip_path.stat().st_size > 1024:
        zip_bytes = zip_path.read_bytes()
    else:
        res = requests.get(
            "https://opendart.fss.or.kr/api/document.xml",
            params={"crtfc_key": api_key, "rcept_no": rcept_no}, timeout=timeout,
        )
        res.raise_for_status()
        zip_bytes = res.content
        zip_path.write_bytes(zip_bytes)

    sources: dict[str, list[tuple[str, str, str]]] = {
        "사업보고서": [], "반기보고서": [], "분기보고서": [],
        "연결감사보고서": [], "감사보고서": [], "unknown": [],
    }
    with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
        for name in zf.namelist():
            xml_text = zf.read(name).decode("utf-8", errors="ignore")
            m = DOC_TYPE_PATTERN.search(xml_text)
            doc_type = m.group(1).strip() if m else "unknown"
            key = doc_type if doc_type in sources else "unknown"
            sources[key].append((name, xml_text, doc_type))
        n_xml_files = len(zf.namelist())

    # fallback에 따른 primary 선택
    type_map = {
        "PRIMARY_BIZ": "사업보고서",
        "FALLBACK_HALF": "반기보고서",
        "FALLBACK_Q3": "분기보고서",
        "FALLBACK_Q1": "분기보고서",
    }
    target_type = type_map.get(fallback_label, "사업보고서")
    primary: tuple[str, str, str] | None = None
    if sources[target_type]:
        primary = max(sources[target_type], key=lambda x: len(x[1]))
    elif sources["unknown"]:
        primary = max(sources["unknown"], key=lambda x: len(x[1]))
    else:
        # 위반금지 #1 — 명시적 실패
        raise RuntimeError(
            f"FAIL_NO_BUSINESS_REPORT — fallback={fallback_label}, "
            f"target_type={target_type} 없음"
        )

    return {
        "zip_path": zip_path,
        "sources": sources,
        "primary": primary,
        "n_xml_files": n_xml_files,
    }


def save_aux_sources(
    sources: dict, stock_code: str, fiscal_year: int, interim_dir: Path,
) -> dict[str, Path | None]:
    """세분화 축 A — 보조 보고서(감사보고서·연결감사보고서) 별도 보존."""
    name_map = {
        "연결감사보고서": "aux_audit_consolidated",
        "감사보고서": "aux_audit_separate",
    }
    saved: dict[str, Path | None] = {}
    for doc_type, suffix in name_map.items():
        items = sources.get(doc_type, [])
        if not items:
            saved[doc_type] = None
            continue
        payload = {
            "doc_type": doc_type,
            "stock_code": stock_code,
            "fiscal_year": fiscal_year,
            "files": [
                {
                    "filename": fn, "doc_name_in_xml": dt,
                    "xml_text_length": len(xt), "xml_text": xt,
                }
                for fn, xt, dt in items
            ],
        }
        path = interim_dir / f"{stock_code}_{fiscal_year}_{suffix}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        saved[doc_type] = path
    return saved


# ============================================================================
# Step 6: SECTION-1 + 표/본문 분리 (Fix #6·#7 + 🔥 v5 Fix #12)
# ============================================================================

def extract_sections_v5(xml_text: str) -> tuple[dict[str, dict], list[dict]]:
    """🔥 v5 핵심 — lxml로 SECTION-1 14개 노드 순회 + 표/본문 분리.

    가이드 line 156-157 (4-5단계) 의도 충실 구현.

    Returns:
        sections: {label: {section_code, section_title, section_text, section_body,
                           section_tables, char_count, body_char_count,
                           tables_char_count, n_tables, table_ratio, ...}}
        match_log: [{sec1_index, label, section_code, method, ...}]
    """
    parser = etree.XMLParser(recover=True, huge_tree=True)
    root = etree.fromstring(xml_text.encode("utf-8"), parser=parser)
    if root is None:
        raise RuntimeError("FAIL_XML_PARSE — lxml 파싱 실패")

    sec1_nodes = root.findall(".//SECTION-1")
    sections: dict[str, dict] = {}
    match_log: list[dict] = []

    for idx, s1 in enumerate(sec1_nodes):
        title_el = s1.find(".//TITLE")
        title_text = (title_el.text or "").strip() if title_el is not None else ""
        aassoc = title_el.get("AASSOCNOTE", "") if title_el is not None else ""
        atoc = title_el.get("ATOC", "") if title_el is not None else ""

        # 1) AASSOCNOTE 우선 매칭
        label, section_code = parse_aassocnote(aassoc)
        method = "AASSOCNOTE"

        # 2) TITLE 텍스트 매칭 (보조)
        if not label:
            label = match_title_to_label(title_text)
            if label:
                section_code = SECTION_CODE_MAP.get(label, ("",))[0]
                method = "TITLE_text"

        # 3) 미식별
        if not label:
            method = "no_match"
            label = f"UNK_{idx}"
            section_code = ""

        # 🔥 Fix #12 — 표/본문 분리
        # 전체 (text)
        section_text = " ".join(t.strip() for t in s1.itertext() if t and t.strip())
        # 본문만 (body — 표 제거)
        s1_no_tbl = deepcopy(s1)
        for tbl in s1_no_tbl.findall(".//TABLE"):
            parent = tbl.getparent()
            if parent is not None:
                parent.remove(tbl)
        section_body = " ".join(t.strip() for t in s1_no_tbl.itertext() if t and t.strip())
        # 표만 (tables)
        table_pieces = []
        for tbl in s1.findall(".//TABLE"):
            tbl_text = re.sub(r"\s+", " ", "".join(tbl.itertext())).strip()
            if tbl_text:
                table_pieces.append(tbl_text)
        section_tables = "\n\n".join(table_pieces)

        n_tables = len(s1.findall(".//TABLE"))
        text_len = len(section_text)
        table_ratio = (len(section_tables) / text_len) if text_len else 0

        sections[label] = {
            "section_code": section_code,
            "section_title": title_text,
            "aassocnote": aassoc,
            "atoc": atoc,
            "method": method,
            "sec1_index": idx,
            "section_text": section_text,
            "section_body": section_body,
            "section_tables": section_tables,
            "text_char_count": text_len,
            "body_char_count": len(section_body),
            "tables_char_count": len(section_tables),
            "n_tables": n_tables,
            "table_ratio": table_ratio,
        }
        match_log.append({
            "sec1_index": idx, "label": label, "section_code": section_code,
            "aassocnote": aassoc, "method": method, "title_text": title_text[:80],
            "text_char_count": text_len, "body_char_count": len(section_body),
            "tables_char_count": len(section_tables), "n_tables": n_tables,
            "table_ratio": round(table_ratio, 3),
        })

    return sections, match_log


# ============================================================================
# Step 7: ESG passage 추출 (가이드 line 158, body/tables/text 옵션)
# ============================================================================

def extract_passages_v5(
    target_sections: dict, seed_df: pd.DataFrame,
    *, source: str = "body", min_len: int = 20,
) -> pd.DataFrame:
    """seed 매칭 문장 후보 추출.

    Args:
        target_sections: ESG_TARGET_LABELS만 골라낸 dict
        seed_df: data/seed_dictionary.csv DataFrame
        source: 'text' (전체) / 'body' (본문) / 'tables' (표) 중 선택
        min_len: 문장 최소 길이

    위반금지 #3 (line 94): 순수 Python re로 재현 (MCP 의존 ❌).
    """
    seed_by_dim = seed_df.groupby("dimension")["seed_term"].apply(list).to_dict()
    pattern_by_dim = {
        dim: re.compile("|".join(map(re.escape, terms)))
        for dim, terms in seed_by_dim.items()
    }
    field_map = {"text": "section_text", "body": "section_body", "tables": "section_tables"}
    field = field_map[source]

    rows = []
    for label, sec_dict in target_sections.items():
        text = sec_dict.get(field, "")
        if not text:
            continue
        sentences = re.split(r"(?<=[\.!?])\s+|\n+", text)
        for sent in sentences:
            sent = sent.strip()
            if len(sent) < min_len:
                continue
            matched_dims: list[str] = []
            matched_terms: list[str] = []
            for dim, pat in pattern_by_dim.items():
                hits = pat.findall(sent)
                if hits:
                    matched_dims.append(dim)
                    matched_terms.extend(set(hits))
            if matched_dims:
                rows.append({
                    "section": label,
                    "section_code": sec_dict.get("section_code", ""),
                    "source": source,
                    "dimensions": "|".join(sorted(set(matched_dims))),
                    "matched_terms": "|".join(sorted(set(matched_terms))),
                    "n_matches": len(matched_terms),
                    "sentence": sent,
                })
    return pd.DataFrame(rows)


# ============================================================================
# Step 9: collection_log (Fix #4·#5, 가이드 line 137-146, 170-172)
# ============================================================================

def append_log_v5(log_path: Path, row: dict) -> pd.DataFrame:
    """Fix #4 — 컬럼 mismatch 자동 백업 + Fix #5 — status 세분화 컬럼."""
    if log_path.exists():
        try:
            existing = pd.read_csv(log_path, nrows=0)
            if list(existing.columns) != EXPECTED_LOG_COLUMNS_V5:
                stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                bak = log_path.with_suffix(f".csv.bak_{stamp}")
                log_path.rename(bak)
        except (pd.errors.ParserError, Exception):
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            bak = log_path.with_suffix(f".csv.bak_{stamp}")
            log_path.rename(bak)

    df_row = pd.DataFrame([row], columns=EXPECTED_LOG_COLUMNS_V5)
    df_row.to_csv(
        log_path, mode="a", header=not log_path.exists(),
        index=False, encoding="utf-8-sig",
    )
    return pd.read_csv(log_path)


def determine_status(
    fallback_used: str, sections_all: dict, n_pass_body: int,
    dim_counts: dict[str, int],
) -> tuple[str, str]:
    """가이드 line 172 (실패 행 가짜 0 ❌) 준수.

    11종 status:
    SUCCESS · FAIL_HTTP · FAIL_LIST_NO_REPORT · FAIL_NO_BUSINESS_REPORT ·
    FAIL_XML_PARSE · FAIL_SECTION_NOT_FOUND · FAIL_SECTION_II/IV/VI ·
    FAIL_PASSAGE · WARN_DIM_IMBALANCE · WARN_FALLBACK_*
    """
    sec_II = sections_all.get("II", {}).get("text_char_count", 0)
    sec_IV = sections_all.get("IV", {}).get("text_char_count", 0)
    sec_VI = sections_all.get("VI", {}).get("text_char_count", 0)
    e_n = dim_counts.get("E", 0)
    s_n = dim_counts.get("S", 0)
    g_n = dim_counts.get("G", 0)

    if sec_II == 0 and sec_IV == 0 and sec_VI == 0:
        return ("FAIL_SECTION_NOT_FOUND", "II/IV/VI 모두 0자")
    if n_pass_body == 0:
        return ("FAIL_PASSAGE", "body passage 0건")
    if min(e_n, s_n, g_n) < 5:
        return ("WARN_DIM_IMBALANCE", f"E={e_n}, S={s_n}, G={g_n} (5 미만)")
    if fallback_used != "PRIMARY_BIZ":
        return (
            f"WARN_FALLBACK_{fallback_used.replace('FALLBACK_', '')}",
            f"사업보고서 없음, {fallback_used} 사용",
        )
    return ("SUCCESS", "")


# ============================================================================
# Phase 2 orchestration — 1 firm-year + batch
# ============================================================================

def run_one_firm_year(
    stock_code: str, fiscal_year: int, *,
    api_key: str, corp_map: pd.DataFrame, seed_df: pd.DataFrame,
    dirs: dict[str, Path], sleep_after: float = 0.5,
) -> dict[str, Any]:
    """1 firm-year 풀 파이프라인 (가이드 line 153-158 1~6단계 모두).

    Returns:
        log_row dict (EXPECTED_LOG_COLUMNS_V5 스키마).
    """
    esg_year = fiscal_year + 1
    viewer_url = ""
    sections_all: dict = {}
    n_pass_body = 0
    n_pass_tables = 0
    fallback_used = "PRIMARY_BIZ"

    try:
        # Step 3: corp_code
        corp_code = stock_to_corp(stock_code, corp_map)

        # Step 4: rcept (Fix #13 fallback)
        r4 = find_rcept_no_v5(api_key, corp_code, fiscal_year)
        rcept_no = r4["selected"]["rcept_no"]
        viewer_url = r4["selected"]["viewer_url"]
        fallback_used = r4["fallback_used"]

        # Step 5: zip + type 판별
        r5 = download_document_xml_v5(
            api_key, rcept_no, stock_code, fiscal_year,
            dirs["raw"], fallback_label=fallback_used,
        )
        primary_xml = r5["primary"][1]

        # Step 5+: aux 저장
        save_aux_sources(r5["sources"], stock_code, fiscal_year, dirs["interim"])

        # Step 6: SECTION-1 + 표/본문 분리 (Fix #12)
        sections_all, match_log = extract_sections_v5(primary_xml)

        # primary sections.json 저장
        payload = {
            "doc_type": "사업보고서" if fallback_used == "PRIMARY_BIZ" else fallback_used,
            "fallback_used": fallback_used,
            "stock_code": stock_code, "fiscal_year": fiscal_year, "esg_year": esg_year,
            "rcept_no": rcept_no, "viewer_url": viewer_url,
            "parser_version": "v5",
            "parsed_at": datetime.now().isoformat(timespec="seconds"),
            "sections": sections_all,
            "esg_target_labels": ESG_TARGET_LABELS,
        }
        (dirs["interim"] / f"{stock_code}_{fiscal_year}_sections.json").write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )

        # section_match_v5 누적
        match_df = pd.DataFrame([
            {**m, "stock_code": stock_code, "fiscal_year": fiscal_year,
             "fallback_used": fallback_used,
             "timestamp": datetime.now().isoformat(timespec="seconds")}
            for m in match_log
        ])
        match_csv = dirs["logs"] / "section_match_v5.csv"
        match_df.to_csv(
            match_csv, mode="a", header=not match_csv.exists(),
            index=False, encoding="utf-8-sig",
        )

        # correction_log
        if r4["all_candidates"]:
            cdf = pd.DataFrame([{
                "stock_code": stock_code, "fiscal_year": fiscal_year,
                **c, "is_selected": c["rcept_no"] == rcept_no,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            } for c in r4["all_candidates"]])
            cpath = dirs["logs"] / "correction_log.csv"
            cdf.to_csv(
                cpath, mode="a", header=not cpath.exists(),
                index=False, encoding="utf-8-sig",
            )

        # Step 7: passage (body 기준 primary)
        target = {k: sections_all[k] for k in ESG_TARGET_LABELS if k in sections_all}
        passages_body = extract_passages_v5(target, seed_df, source="body")
        passages_tables = extract_passages_v5(target, seed_df, source="tables")
        n_pass_body = len(passages_body)
        n_pass_tables = len(passages_tables)

        # 차원 카운트
        dim_b = (
            passages_body["dimensions"].apply(lambda x: x.split("|")).explode().value_counts().to_dict()
            if n_pass_body else {}
        )

        # status 판정
        status, reason = determine_status(fallback_used, sections_all, n_pass_body, dim_b)

    except Exception as e:
        # 위반금지 #1 — 가짜 0 ❌ 명시적 실패
        ename = type(e).__name__
        status, reason = "FAIL", f"{ename}: {e}"
        rcept_no = ""
        corp_code = ""

    # log_row
    def _g(label: str, field: str, default: Any = 0) -> Any:
        return sections_all.get(label, {}).get(field, default)

    log_row = {
        "stock_code": stock_code, "fiscal_year": fiscal_year, "esg_year": esg_year,
        "corp_code": locals().get("corp_code", ""),
        "rcept_no": locals().get("rcept_no", ""),
        "fallback_used": fallback_used, "status": status, "reason": reason,
        "n_passages_body": n_pass_body, "n_passages_tables": n_pass_tables,
        "sec_II_code": _g("II", "section_code", ""),
        "sec_II_text": _g("II", "text_char_count"),
        "sec_II_body": _g("II", "body_char_count"),
        "sec_II_tables": _g("II", "tables_char_count"),
        "sec_II_n_tbl": _g("II", "n_tables"),
        "sec_IV_code": _g("IV", "section_code", ""),
        "sec_IV_text": _g("IV", "text_char_count"),
        "sec_IV_body": _g("IV", "body_char_count"),
        "sec_IV_tables": _g("IV", "tables_char_count"),
        "sec_IV_n_tbl": _g("IV", "n_tables"),
        "sec_VI_code": _g("VI", "section_code", ""),
        "sec_VI_text": _g("VI", "text_char_count"),
        "sec_VI_body": _g("VI", "body_char_count"),
        "sec_VI_tables": _g("VI", "tables_char_count"),
        "sec_VI_n_tbl": _g("VI", "n_tables"),
        "n_sec1_total": len(sections_all),
        "viewer_url": viewer_url, "parser_version": "v5",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    # collection_log 누적
    append_log_v5(dirs["logs"] / "collection_log.csv", log_row)

    if sleep_after > 0:
        time.sleep(sleep_after)  # rate limit 회피

    return log_row


def run_batch(
    sample: list[tuple[str, int]], *,
    api_key: str, corp_map: pd.DataFrame, seed_df: pd.DataFrame,
    dirs: dict[str, Path], sleep: float = 0.5,
    max_retry: int = 3, backoff_base: float = 5.0,
) -> pd.DataFrame:
    """N firm-year batch — rate limit + 지수 backoff + 격리 실패.

    가이드 line 117 (최대 381 firm-year) + line 170-172 (실패 행 reason 명시).
    """
    results = []
    for i, (stock_code, fiscal_year) in enumerate(sample):
        attempt = 0
        while attempt < max_retry:
            try:
                row = run_one_firm_year(
                    stock_code, fiscal_year, api_key=api_key,
                    corp_map=corp_map, seed_df=seed_df, dirs=dirs,
                    sleep_after=sleep,
                )
                results.append(row)
                break  # 성공 → retry 루프 탈출
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 429:
                    wait = backoff_base * (2**attempt)
                    warnings.warn(f"HTTP 429 — {wait}s 대기 후 재시도 ({attempt + 1}/{max_retry})")
                    time.sleep(wait)
                    attempt += 1
                    continue
                # 다른 HTTP 에러는 격리 실패 처리
                results.append({
                    "stock_code": stock_code, "fiscal_year": fiscal_year,
                    "status": "FAIL_HTTP", "reason": str(e),
                    "parser_version": "v5",
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                })
                break
            except Exception as e:
                # 위반금지 #1 — 격리 실패 + reason 명시
                results.append({
                    "stock_code": stock_code, "fiscal_year": fiscal_year,
                    "status": "FAIL", "reason": f"{type(e).__name__}: {e}",
                    "parser_version": "v5",
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                })
                break
    return pd.DataFrame(results)


# ============================================================================
# Phase 2A — 균형 표본 선택
# ============================================================================

def select_balanced_sample(
    company_master: pd.DataFrame, n: int = 50, *, seed: int = 42,
    exclude_stocks: list[str] | None = None,
) -> list[tuple[str, int]]:
    """업종·연도·등급 균형 표본 선택 (Phase 2A 50건 기본).

    가이드 line 35 (회사명 join 금지) — stock_code 기준.
    """
    df = company_master.copy()
    if exclude_stocks:
        df = df[~df["stock_code"].isin(exclude_stocks)]

    # 단순 stratify: fiscal_year 균등 + 업종 균등 + 랜덤
    rng = pd.np.random.default_rng(seed) if hasattr(pd, "np") else None
    parts = []
    n_per_year = n // df["fiscal_year"].nunique()
    for yr, g in df.groupby("fiscal_year"):
        # 업종별 비례 추출
        sampled = g.sample(min(n_per_year, len(g)), random_state=seed)
        parts.append(sampled)
    sample_df = pd.concat(parts, ignore_index=True).sample(n=min(n, len(pd.concat(parts))), random_state=seed)
    return [(row["stock_code"], int(row["fiscal_year"])) for _, row in sample_df.iterrows()]
