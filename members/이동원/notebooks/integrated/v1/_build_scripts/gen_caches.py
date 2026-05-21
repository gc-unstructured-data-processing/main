#!/usr/bin/env python3
"""노트북 무거운 단계 캐시 선생성 (시간제한 배치).
- tokens_primary.json: Kiwi(user dict score=50) + 불용어 토큰화 (노트북 섹션3과 동일 로직)
노트북은 이 캐시를 우선 로드 → nbconvert가 빠르게 완주.
"""
import os, re, json, glob, time, sys
from pathlib import Path
from collections import Counter
import pandas as pd
from kiwipiepy import Kiwi

ROOT = Path("/sessions/blissful-upbeat-volta/mnt/unstructured-data-processing-final-project")
DATA = ROOT / "data"
CORPUS_DIR = DATA / "interim" / "corpus_381"
OUT_DIR = ROOT / "members" / "이동원" / "notebooks" / "integrated" / "v1" / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TOK_CACHE = OUT_DIR / "tokens_primary.json"

cm = pd.read_csv(DATA / "company_master.csv", dtype=str)
cm["stock_code"] = cm["stock_code"].str.zfill(6)
seed_df = pd.read_csv(DATA / "seed_dictionary.csv")
ALL_SEED = seed_df["seed_term"].tolist()

# 불용어 (노트북 섹션 3-1과 동일)
stop = set()
sw = DATA / "stopwords_ko_esg.txt"
if sw.exists():
    stop |= {w.strip() for w in sw.read_text(encoding="utf-8").split() if w.strip()}
stop |= set("및 관련 통해 대한 당사 회사 사업 보고서 내용 경우 기타 주요 해당 제출 공시 정정 첨부 "
            "재무제표 부채 자산 매출 손익 영업 자본 주석 단위 백만원 천원 기준 현재 연결 별도".split())
for nm in cm["company_name"].dropna().astype(str).unique():
    stop.add(nm)
    if len(nm) >= 4:
        stop.add(nm[:2]); stop.add(nm[2:])
stop -= set(ALL_SEED)

kiwi = Kiwi()
for term in ALL_SEED:
    kiwi.add_user_word(str(term).strip(), "NNP", score=50.0)

def to_nouns(text, min_len=2):
    return [t.form for t in kiwi.tokenize(text)
            if (t.tag.startswith("NN") or t.tag == "SL") and len(t.form) >= min_len]

def load_doc(p):
    return json.load(open(p, encoding="utf-8")).get("firm_year_doc", "")

# 기존 캐시 로드 (손상 시 무시하고 재생성)
token_data = {}
if TOK_CACHE.exists():
    try:
        token_data = json.load(open(TOK_CACHE, encoding="utf-8"))
    except Exception as e:
        print(f"[캐시 손상 — 재생성] {e}", flush=True)
        token_data = {}

files = sorted(glob.glob(str(CORPUS_DIR / "*.json")))
max_seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 40
t0 = time.time()
done = 0
for f in files:
    d = json.load(open(f, encoding="utf-8"))
    sc = str(d.get("stock_code")).zfill(6); fy = int(d.get("fiscal_year"))
    key = f"{sc}_{fy}"
    if key in token_data:
        continue
    doc = d.get("firm_year_doc", "")
    if not doc:
        continue
    nouns = to_nouns(doc)
    token_data[key] = [w for w in nouns if w not in stop]
    done += 1
    if time.time() - t0 > max_seconds:
        break

payload = json.dumps(token_data, ensure_ascii=False)
with open(TOK_CACHE, "w", encoding="utf-8") as fp:
    fp.write(payload)
print("[토큰화 캐시] 이번 " + str(done) + "건 신규 | 누적 " + str(len(token_data)) + "/" + str(len(files)) + " | " + str(round(time.time()-t0)) + "s", flush=True)
