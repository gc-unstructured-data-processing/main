#!/usr/bin/env python3
"""분석기 비교 캐시 생성 (노트북 섹션 2와 동일 표본 로직).
Kiwi(user dict score=50) vs Okt — seed별 빈도 + 비교 지표 → analyzer_cache.json
"""
import json, glob, time
from pathlib import Path
from collections import Counter
import pandas as pd
from kiwipiepy import Kiwi
from konlpy.tag import Okt

ROOT = Path("/sessions/blissful-upbeat-volta/mnt/unstructured-data-processing-final-project")
DATA = ROOT / "data"
CORPUS_DIR = DATA / "interim" / "corpus_381"
OUT_DIR = ROOT / "members" / "이동원" / "notebooks" / "integrated" / "v1" / "outputs"
ANA_CACHE = OUT_DIR / "analyzer_cache.json"

seed_df = pd.read_csv(DATA / "seed_dictionary.csv")
ALL_SEED = seed_df["seed_term"].tolist()

# 노트북 섹션1·2-2와 동일: SUCCESS firm-year doc 길이순 30개 표본
recs = []
for f in sorted(glob.glob(str(CORPUS_DIR / "*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    m = d.get("_meta", {})
    if m.get("status") == "SUCCESS":
        doc = d.get("firm_year_doc", "")
        recs.append({"key": f"{m['stock_code']}_{m['fiscal_year']}", "doc": doc, "dlen": len(doc)})
sk = pd.DataFrame(recs).sort_values("dlen")
sample = sk.iloc[::max(1, len(sk) // 15)].head(15).reset_index(drop=True)
# Okt 속도 위해 각 문서 앞 25000자만 (Kiwi·Okt 동일 절단 → 공정 비교)
docs = [d[:25000] for d in sample["doc"].tolist()]
print(f"표본 {len(docs)}개 (분량 {sample['dlen'].min():,}~{sample['dlen'].max():,})", flush=True)

def kiwi_nouns(kiwi, text, ml=2):
    return [t.form for t in kiwi.tokenize(text)
            if (t.tag.startswith("NN") or t.tag == "SL") and len(t.form) >= ml]

def okt_nouns(okt, text, ml=2):
    return [w for w in okt.nouns(text) if len(w) >= ml]

results, kiwi_seed_freq, okt_seed_freq = {}, {}, {}

kiwi = Kiwi()
for term in ALL_SEED:
    kiwi.add_user_word(str(term).strip(), "NNP", score=50.0)
t0 = time.time(); tl = [kiwi_nouns(kiwi, d) for d in docs]; el = time.time() - t0
fr = Counter(t for l in tl for t in l)
kiwi_seed_freq = {s: fr.get(s, 0) for s in ALL_SEED}
results["Kiwi"] = {"seed_보존": sum(1 for s in ALL_SEED if fr.get(s, 0) > 0),
                   "토큰합": sum(len(l) for l in tl), "vocab": len(fr),
                   "시간_s": round(el, 1), "user_dict": "seed30 NNP score=50"}
print(f"Kiwi 완료 {el:.1f}s | seed 보존 {results['Kiwi']['seed_보존']}/30", flush=True)

okt = Okt()
t0 = time.time(); tl = [okt_nouns(okt, d) for d in docs]; el = time.time() - t0
fr = Counter(t for l in tl for t in l)
okt_seed_freq = {s: fr.get(s, 0) for s in ALL_SEED}
results["Okt"] = {"seed_보존": sum(1 for s in ALL_SEED if fr.get(s, 0) > 0),
                  "토큰합": sum(len(l) for l in tl), "vocab": len(fr),
                  "시간_s": round(el, 1), "user_dict": "미지원 (강제 불가)"}
print(f"Okt 완료 {el:.1f}s | seed 보존 {results['Okt']['seed_보존']}/30", flush=True)

payload = json.dumps({"results": results, "kiwi_seed_freq": kiwi_seed_freq, "okt_seed_freq": okt_seed_freq}, ensure_ascii=False)
with open(ANA_CACHE, "w", encoding="utf-8") as fp:
    fp.write(payload)
print("analyzer_cache.json 저장 완료", flush=True)
