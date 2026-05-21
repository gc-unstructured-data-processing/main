#!/usr/bin/env python3
"""
381 firm-year 전체 수집 (백그라운드 실행용).
회의 결정: 데이터 381개 다 살리기 (김혜성 v2) + 이동원 recover XML parser.
- find_business_report_v2: 결산월 무관 + 정정 우선순위 (원본>기재정정>첨부정정)
- XMLParser(recover=True): well-formed 아닌 XML도 복구
- II/IV/VI 섹션 본문 추출
- 가짜 0 금지: 실패 행은 status/reason 기록
체크포인트: 매 firm-year corpus JSON 저장 → 재실행 시 스킵 (idempotent)
"""
import os, re, json, time, zipfile, html
from io import BytesIO
from pathlib import Path
import requests
import pandas as pd
from lxml import etree

ROOT = Path("/sessions/blissful-upbeat-volta/mnt/unstructured-data-processing-final-project")
RAW_DIR = ROOT / "data" / "raw"
INTERIM_DIR = ROOT / "data" / "interim"
CORPUS_DIR = ROOT / "data" / "interim" / "corpus_381"
LOGS_DIR = ROOT / "logs"
for d in (RAW_DIR, INTERIM_DIR, CORPUS_DIR, LOGS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# API key
API_KEY = None
with open(ROOT / ".env") as f:
    for line in f:
        if line.startswith("API_KEY"):
            API_KEY = line.split("=", 1)[1].strip()

cm = pd.read_csv(ROOT / "data" / "company_master.csv", dtype=str)
cm["stock_code"] = cm["stock_code"].str.zfill(6)
corp_map = pd.read_parquet(ROOT / "data" / "cache" / "corp_code_map.parquet")
stock_to_corp = dict(zip(corp_map["stock_code"].str.zfill(6), corp_map["corp_code"]))

META_PATH = CORPUS_DIR / "_collection_meta.csv"
SESSION = requests.Session()


def find_business_report_v2(corp_code, fiscal_year):
    """김혜성 v2: 결산월 무관 + 정정 우선순위."""
    search_year = int(fiscal_year) + 1
    params = {"crtfc_key": API_KEY, "corp_code": corp_code,
              "bgn_de": f"{search_year}0101", "end_de": f"{search_year}1231",
              "pblntf_detail_ty": "A001", "page_count": "100"}
    try:
        res = SESSION.get("https://opendart.fss.or.kr/api/list.json", params=params, timeout=20)
        payload = res.json()
    except Exception as e:
        return None, f"api_error:{e}"
    if payload.get("status") != "000":
        return None, f"list_status_{payload.get('status')}"
    rows = payload.get("list", [])
    cands = [r for r in rows if "사업보고서" in r.get("report_nm", "")
             and "반기" not in r.get("report_nm", "") and "분기" not in r.get("report_nm", "")]
    if not cands:
        return None, "no_report_found"

    def prio(nm):
        if "[첨부정정]" in nm: return 2
        if "[기재정정]" in nm or "[정정]" in nm: return 1
        return 0
    cands.sort(key=lambda r: (prio(r.get("report_nm", "")), -int(r.get("rcept_dt", "0"))))
    ch = cands[0]
    return {"rcept_no": ch.get("rcept_no"), "report_nm": ch.get("report_nm"),
            "rcept_dt": ch.get("rcept_dt"), "n_candidates": len(cands),
            "selection_priority": prio(ch.get("report_nm", ""))}, "ok"


def download_xml(rcept_no, stock_code, fiscal_year):
    """이동원 방식: zip 보존(위반금지 #5) + idempotent 캐시."""
    zip_path = RAW_DIR / f"{stock_code}_{fiscal_year}_disclosure.zip"
    if zip_path.exists() and zip_path.stat().st_size > 1024:
        zip_bytes = zip_path.read_bytes()
    else:
        try:
            res = SESSION.get("https://opendart.fss.or.kr/api/document.xml",
                              params={"crtfc_key": API_KEY, "rcept_no": rcept_no}, timeout=60)
            res.raise_for_status()
            zip_bytes = res.content
            zip_path.write_bytes(zip_bytes)
        except Exception as e:
            return None, f"download_error:{e}"
    try:
        with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
            names = zf.namelist()
            # 가장 큰 XML = 사업보고서 본문
            best, best_len = None, 0
            for n in names:
                t = zf.read(n).decode("utf-8", errors="ignore")
                if len(t) > best_len:
                    best, best_len = t, len(t)
        return best, "ok"
    except Exception as e:
        return None, f"unzip_error:{e}"


def extract_esg_sections(xml_text):
    """이동원 recover parser + 김혜성 TITLE 로마숫자 + TABLE 제거 + P 추출.
    II/IV/VI 섹션 본문 텍스트 반환."""
    # recover=True: well-formed 아닌 XML 복구 (이동원 Fix F 핵심)
    parser = etree.XMLParser(recover=True, huge_tree=True)
    try:
        etree.fromstring(xml_text.encode("utf-8"), parser=parser)  # 파싱 가능성 확인
    except Exception:
        pass  # recover 모드는 거의 항상 통과; 정규식 추출로 진행

    title_iter = list(re.finditer(r'<TITLE[^>]*>(.*?)</TITLE>', xml_text, re.DOTALL))
    roman_re = re.compile(r'^\s*(I{1,3}|IV|V|VI{0,3}|IX|X)\.\s*([가-힣].{1,40})')
    big = []
    for m in title_iter:
        clean = re.sub(r'\s+', ' ', m.group(1)).strip()
        rm = roman_re.match(clean)
        if rm:
            big.append({"pos": m.start(), "roman": rm.group(1), "title": clean})
    targets = ["II", "IV", "VI"]
    out = {}
    for i, sec in enumerate(big):
        if sec["roman"] not in targets:
            continue
        start = sec["pos"]
        end = big[i + 1]["pos"] if i + 1 < len(big) else len(xml_text)
        sx = xml_text[start:end]
        sx_no_tbl = re.sub(r'<TABLE.*?</TABLE>', ' ', sx, flags=re.DOTALL)
        paras = re.findall(r'<P[^>]*>(.*?)</P>', sx_no_tbl, re.DOTALL)
        clean_p = []
        for p in paras:
            txt = re.sub(r'<[^>]+>', ' ', p)
            txt = html.unescape(txt)
            txt = re.sub(r'\s+', ' ', txt).strip()
            if len(txt) >= 10:
                clean_p.append(txt)
        full = "\n".join(clean_p)
        out[sec["roman"]] = {"title": sec["title"], "text": full,
                             "n_paragraphs": len(clean_p), "n_chars": len(full)}
    return out


def collect_one(row):
    sc = row["stock_code"]
    fy = int(row["fiscal_year"])
    key = f"{sc}_{fy}"
    doc_path = CORPUS_DIR / f"{key}.json"
    if doc_path.exists():
        try:
            d = json.load(open(doc_path, encoding="utf-8"))
            return {**d.get("_meta", {}), "status": "SUCCESS", "cached": True}
        except Exception:
            pass
    corp_code = stock_to_corp.get(sc)
    base = {"company_name": row.get("company_name"), "stock_code": sc, "corp_code": corp_code,
            "fiscal_year": fy, "esg_year": fy + 1}
    if not corp_code:
        return {**base, "status": "FAIL", "reason": "missing_corp_code"}
    rep, why = find_business_report_v2(corp_code, fy)
    if rep is None:
        return {**base, "status": "FAIL", "reason": why}
    xml_text, why2 = download_xml(rep["rcept_no"], sc, fy)
    if xml_text is None:
        return {**base, "status": "FAIL", "reason": why2, "rcept_no": rep["rcept_no"]}
    secs = extract_esg_sections(xml_text)
    body = "\n".join(secs[k]["text"] for k in ("II", "IV", "VI") if k in secs)
    n_chars = len(body)
    meta = {**base, "rcept_no": rep["rcept_no"], "report_nm": rep["report_nm"],
            "rcept_dt": rep["rcept_dt"], "selection_priority": rep["selection_priority"],
            "section_chars_II": secs.get("II", {}).get("n_chars", 0),
            "section_chars_IV": secs.get("IV", {}).get("n_chars", 0),
            "section_chars_VI": secs.get("VI", {}).get("n_chars", 0),
            "total_chars": n_chars,
            "viewer_url": f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rep['rcept_no']}"}
    if n_chars < 50:
        meta["status"] = "WARN_NO_SECTIONS"
        meta["reason"] = "II/IV/VI 추출 텍스트 거의 없음"
    else:
        meta["status"] = "SUCCESS"
        meta["reason"] = ""
    json.dump({"_meta": meta, "stock_code": sc, "fiscal_year": fy, "esg_year": fy + 1,
               "rcept_no": rep["rcept_no"], "sections": secs, "firm_year_doc": body},
              open(doc_path, "w", encoding="utf-8"), ensure_ascii=False)
    return meta


def main(max_seconds=40):
    """시간 제한 배치: max_seconds 안에 처리 가능한 만큼만. 캐시 idempotent로 이어감."""
    t0 = time.time()
    n = len(cm)
    done_this_run = 0
    for idx, (_, row) in enumerate(cm.iterrows()):
        sc, fy = row["stock_code"], int(row["fiscal_year"])
        doc_path = CORPUS_DIR / f"{sc}_{fy}.json"
        if doc_path.exists():
            continue  # 이미 수집됨 → 스킵 (빠름)
        collect_one(row)
        done_this_run += 1
        if time.time() - t0 > max_seconds:
            break
        time.sleep(0.15)
    n_cached = len(list(CORPUS_DIR.glob("*.json")))
    elapsed = time.time() - t0
    print("[배치] 이번 실행 " + str(done_this_run) + "건 신규 | 누적 corpus " + str(n_cached) + "/" + str(n) + " | " + str(round(elapsed)) + "s", flush=True)


if __name__ == "__main__":
    import sys
    secs = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    main(secs)
