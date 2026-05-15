# 협업 가이드 — ESG DART 기말 프로젝트

팀 4명이 한 레포에서 충돌 없이 작업하기 위한 규칙입니다.

## 브랜치 명명 규칙

```
feature/<이슈>-<짧은-설명>      # 새 기능/분석
fix/<이슈>-<짧은-설명>           # 버그 수정
chore/<설명>                    # 환경·문서·메타 (이번 셋업 같은 것)
experiment/<이니셜>-<주제>       # 개인 실험 (예: experiment/A-theta-sweep-test)
```

예시:
- `feature/collection-pilot-samsung-2024`
- `feature/preprocessing-okt-tokenize`
- `fix/rate-limit-backoff-retry`
- `chore/folder-structure-setup`
- `experiment/C-fasttext-theta-0.85`

## 커밋 메시지 규칙

```
<type>: <짧은 한국어 제목 50자 이내>

<본문 (선택) — 무엇·왜 위주, 어떻게는 코드가 말함>
```

**type 종류**:
- `feat` — 새 기능/분석 추가
- `fix` — 버그 수정
- `docs` — 문서만 변경
- `chore` — 환경·메타·폴더 정리
- `refactor` — 기능 변화 없이 코드 정리
- `data` — 데이터 추가/갱신 (raw 제외)
- `experiment` — 실험적 작업 (병합 안 할 수도)

예시:
```
feat: 삼성전자 2024 pilot 수집 end-to-end 통과

stock_code 005930 → corp_code → rcept_no까지 흐름 작동.
rate limit 분당 600회 페이스로 안전 마진 확보.
```

## PR 흐름

1. `main`에서 브랜치 따기: `git checkout -b feature/...`
2. 작업 + 커밋 (자주 커밋)
3. push: `git push -u origin feature/...`
4. GitHub에서 PR 생성 — base: `main`, compare: `feature/...`
5. 팀원 1명 이상 리뷰
6. 머지 (squash merge 권장)
7. 브랜치 삭제

## PR 템플릿

```markdown
## 무엇을 했나
- (한 줄)

## 왜 이 변경이 필요한가
- (가이드 인용 또는 팀 토론 결과)

## 검토 포인트
- [ ] (리뷰어가 확인할 것 1)
- [ ] (리뷰어가 확인할 것 2)

## 위반금지 체크 (해당 시)
- [ ] 실패 행을 가짜 0으로 채우지 않았다
- [ ] 회사명 join 없이 stock_code 기준
- [ ] API key가 코드/노트북 출력에 노출되지 않았다
- [ ] esg_year = fiscal_year + 1 고정

## 스크린샷 / 결과 (선택)
```

## 노트북 충돌 방지

노트북 셀 출력이 git diff를 망가뜨립니다. **반드시 셋업**:

```bash
pip install nbstripout
nbstripout --install
```

이 설정 후에는 커밋할 때 셀 출력이 자동 제거됩니다. 최종 제출 직전에만 셀 출력을 살린 ipynb를 별도로 만드세요.

## 데이터 파일 다루기

- `data/company_master.csv`, `seed_dictionary.csv`, `stopwords_ko_esg.txt`는 **공유** (교수님 제공, 모두 동일)
- `data/raw/`, `data/interim/`, `data/feature/`는 **각자 수집** (gitignore, 대용량)
- 새로운 데이터 추가 시 `data/README.md`에 출처 명시

## API key 다루기

- 반드시 `.env`에만 저장
- 코드에 `os.getenv("OPENDART_API_KEY")`로 읽기
- 노트북에 출력하지 말 것 (`print(api_key)` 금지)
- 제출 직전 grep으로 확인: `grep -r "crtfc_key" notebooks/`

## 팀 헌법 3개 (재게시)

1. **식별자**: `stock_code` 기준 (회사명 X)
2. **타이밍**: `esg_year = fiscal_year + 1`
3. **실패 행**: drop + 이유 기록 (가짜 0 X)

이 셋을 어기는 PR은 머지하지 않습니다.

## 충돌 해결 우선순위

1. 교수님 가이드 (`docs/professor_md/01-04`) — 최우선
2. README.md / CONTRIBUTING.md — 팀 합의 사항
3. 심층분석가이드 / 보강 자료 (`docs/`) — 보충
4. 외부 자료 (학술 논문, 블로그) — 참고

충돌 시 위 순서대로.
