# 평가: 20261031-1805-writing-maestro-guide (docs, combo1 technical-writing, d1/d2)

평가 대상 본문: `combo1-technical-writing/d1/GUIDE.md`(370줄, 46KB), `d2/GUIDE.md`(367줄, 42KB). compare/ html은 가공본이라 보지 않았다. final/ 폴더는 없다.

## 점수표

| 시안 | C1 과제 적합성 | C2 독자 판단·행동 | C3 정확성·근거 | C4 구조·탐색성 | C5 문장 품질 | C6 구체성 | C7 사용 준비도 |
|---|---|---|---|---|---|---|---|
| combo1 d1 | 4 | 3 | 5 | 4 | 3 | 4 | 4 |
| combo1 d2 | 5 | 4 | 5 | 4 | 4 | 5 | 4 |

## 대조한 사실 주장 (직접 실행·열람)

현재 HEAD는 `fe1a813`이고 작업 트리는 feedback.md 수정과 `docs/pipeline.html`, `docs/viz/` 미추적 상태다. 시안이 적은 "작업 트리 clean"은 작성 시점 기준이라 지금 재현되지 않지만 오류로 보지 않는다.

| 주장 | 대조 방법 | 결과 | d1 | d2 |
|---|---|---|---|---|
| `OK 67 skills` | `registry_check.py` 실행 | 일치 | O | O |
| 측면 25 / 단계 6 / 묶음 5, 필수 필드 18 | `parse_registry` 실행, `registry_lib.py:11-15` | 일치 | O | O |
| 테스트 66개 통과, 함수 63개 | `pytest -q` → `66 passed`, `grep def test_` 63 | 일치 | O | O(66만) |
| `copywriting humanizer` precedence/ignored 3줄 | `combo_check.py` 실행 | 일치(ignored: prose-edit, ai-tells, evidence) | O | O |
| `general-writing`+`prose-naturalizer` → `primary overlap ai-tells` | 실행 | 일치 | O | O |
| `translation`+`writing-design-docs` format 우선순위 | 실행 | 일치(ignored: translation의 format, voice) | - | O |
| `interview-me`+`copywriting` → `clarify-stage skill in combo` | 실행 | 일치 | - | O |
| `paper-writing academic-voice general-writing` generation_count 1 | 실행 | 일치 | - | O |
| humanizer가 prose-edit을 가져가는 이유(better-usage, academic-voice, writing-cadence 닫힘) | `registry_lookup.py --skill` | 일치 | - | O |
| `registry_check.py --registry /nonexistent.md`가 `IndexError` 트레이스백 | 실행(`registry_check.py:29`의 `parents[2]`) | 일치 | - | O |
| `combo_check.py` 파일 없음 → 트레이스백 | 실행 | 일치 | O | O |
| `build_registry.py --out` 결과가 registry.md와 동일 | 스크래치로 생성해 diff | 일치(SAME) | O | O |
| 출력 폴더·범위 밖/검증 실패 시 brief.md 규칙 | SKILL.md:141, 198-200 | 일치 | O | O |
| 설계 문서 측면 목록이 10개 초안 | design.md:102 | 일치 | - | O |
| 설계 문서와 SKILL.md의 출력 폴더·넘기는 형식 차이 | design.md:129-165 대 SKILL.md | 일치(설계에는 source/, clarify/, gitignore, 범위 밖 줄 없음) | O | - |
| 시험 사례 A: 후보 3개, 조합 2·3 선택, 서브에이전트 4개 | research/trials/.../A-blog-new.md:13-15 | 일치 | O | O |
| 사용자 기준 6개가 커밋 `0593eef`에서 들어감 | `git log`, feedback.md | 일치 | O | - |
| `doc-coauthoring` 출처가 `plugin`으로 시작 | registry.md:523 | 일치 | O | O |
| `~/.local/bin/story` 셸 심 | 매니페스트 support_files | 일치 | O | - |
| 필수 명령 분포(story+node 13, node 1, python3 8) | registry 필드 집계 | "대부분" 서술과 부합 | O | - |
| `readlink ~/.claude/skills/writing-maestro` → 레포 | 실행 | 일치 | - | O |
| `/usr/bin/python3` 3.9.6 | 실행 | 일치 | O | O(3.9) |
| 상대 링크 전부 해석(`docs/` 기준) | 링크 추출 후 존재 확인 | 깨진 링크 0 (pipeline.html은 지금은 있음, 미추적) | O | O |

미확인: `/writing-maestro <과제>` 슬래시 호출 표기(레포 문서에 없고 두 시안 모두 일반 관례에 기댐, d1 NOTES가 인정), GitHub 렌더링(표 안 이스케이프, 한글 앵커), `test_py39.py`가 실제로 skip 없이 돌았는지(66 passed로 간접 확인).

## 시안별

### combo1 d1
- 한 줄 요약: 원본 파일별 역할 표와 "하는 일/설치/호출"로 시작해 SKILL.md 절 번호를 따라 절별 해설을 붙인 서술형 가이드. 용어 부록과 시안 지시 템플릿(측면별 따를 스킬) 설명이 있다.
- 가장 큰 결함: 도입부가 본문 가치보다 길다. 3~17줄이 "독자가 네 파일에 나뉘어 있다"는 소개, 파일 역할 표, 커밋 확인 문구로 채워져 있고 실제 사용 정보는 19줄 이후에 나온다. 예: 3행 "…하는 일과 하지 않는 일, 호출 방법, 작동 파이프라인, 출력 폴더, 레지스트리 구조, … 테스트"처럼 목차를 문장으로 되풀이하고, 9~15행 표의 "그 파일을 읽는 쪽" 열은 호출·수정하려는 독자의 판단에 쓰이지 않는다. 또 호출 예시가 실제 명령줄이 아니라 요청 문장 표(49~54행)여서 복사해 쓸 수 있는 예가 적다.
- 가장 큰 강점: 규칙을 "왜"와 함께 풀어 적었다. 188행 "닫힘"의 정의와 `writing-design-docs`+`general-writing` 충돌 설명, 190~194행 다섯 규칙 번호 목록, 221행 `근거`의 ` / 단어 "` 제약 설명, 349행 `test_registry_real.py`가 머신 설치 상태에 의존한다는 경고가 유지보수자에게 직접 쓸모 있다.
- 사실 오류: 확인된 것 없음. 대조 범위 밖 주장 일부는 미확인(위 목록).

### combo1 d2
- 한 줄 요약: 맨 앞에 "현재 상태" 값·측정 명령 표를 두고 목적→기능→파이프라인→사용법→레지스트리→추가/제거→build_registry→스크립트→feedback→테스트 순으로 brief 항목 순서를 그대로 따른 참조형 가이드. 실제 호출 명령 3줄, 규칙별 실제 판정 사례 표, build_registry 별도 절, 오류 줄·exit 코드 전수 목록이 있다.
- 가장 큰 결함: 같은 내용이 파이프라인 안에서 여러 번 나뉘어 반복되고 밀도가 높다. 57~105행 "작동 파이프라인"에 표, "단계 사이의 판단"(75~85행), "측면별 따를 스킬"(87~105행)이 이어져 사용법(107행~)이 문서 중간 아래로 밀린다. 16행 "현재 상태" 표의 `python3 -B -c "import sys; ..."` 한 줄 명령은 길고 독자가 직접 칠 일이 드물다. 용어 부록이 없어 닫힘, 클러스터, 생성 스킬 같은 용어는 본문 곳곳에서 풀이를 찾아야 한다.
- 가장 큰 강점: 독자가 따라 칠 수 있는 구체성. 113~117행 실제 `/writing-maestro ...` 호출 3줄, 180~187행 규칙별 "판정 사례" 표(모두 실행 결과와 일치), 280~291행 구조 오류 8종과 WARN 2종 전수, 293행 `IndexError` 특이 동작(실행으로 재현됨), 244~251행 build_registry 덮어쓰기 위험과 `--out` 비교 절차.
- 사실 오류: 확인된 것 없음.

## 프로젝트별

### 시안 간 순위
1. d2: C1 5, C2 4, C3 5, C4 4, C5 4, C6 5, C7 4 (합 31).
2. d1: C1 4, C2 3, C3 5, C4 4, C5 3, C6 4, C7 4 (합 27).

근거. C1: brief가 "호출 예시"와 "기능"을 요구했는데 d2만 실제 호출 명령줄과 `기능` 절을 갖췄고 build_registry 절은 brief 밖이지만 "스킬 추가/제거"의 덮어쓰기 위험과 직결된다(d1도 227행에서 같은 위험을 다룸). C2: d1은 도입 3~17행이 본문 진입을 늦추고 설치·요구사항(37~43행)은 유용하나 독자 행동 순서와 거리가 있다. d2는 상태 표 → 목적 → 한도 순으로 판단 정보가 앞에 온다. C5: d1은 3행 콜론 나열, 5행 긴 단문 연쇄처럼 한 문장에 정보를 과적재한다. d2도 83행 같은 긴 문장이 있으나 길이를 점검해 나눴다고 NOTES에 있고 본문도 대체로 한 문장 한 사실이다. 두 시안 모두 한다체로 일관되고 용어("닫힘", "구성원", "생성 스킬")는 일관된다. C6: d2의 실제 명령·실제 판정 결과·exit 목록이 d1보다 많다. d1은 부록 용어 표와 JSON 필드 표가 강점이라 4. 순위 차이는 크지 않으며(사실 정확도는 동률) 사용자가 읽는 방식에 따라 d1의 부록이 선호될 수 있다.

### 조합 적합성
technical-writing 단독 조합은 저장소 기술 문서라는 과제에 맞았다. 두 시안 모두 NOTES에서 truth.md·style.md를 읽고 금지 구문 목록을 한국어 상투 표현으로 준용했으며(영어 전용 목록이라 한국어에는 직접 적용 불가), 제목의 "종합"을 "사용·유지보수"로 바꾼 것도 스킬 규칙을 따른 결과다. 어긋남: brief 해석은 "종합 가이드"인데 두 시안 모두 제목에서 "종합"을 뺐다. 사용자 의도보다 스킬 규칙을 앞세운 사례다(경미). 동반 스킬 처리가 달랐다. d2는 writing-runbooks, documenting-contracts, reviewing-technical-prose를 라우팅 표에 따라 실제로 읽었다고 적었고, d1은 writing-runbooks를 "structure 주 측면 소유자가 하나 더 생긴다"며 읽지 않았다. brief 제외 목록은 writing-runbooks를 별도 조합 후보로 두었으나 technical-writing의 동반 호출은 조합 규칙 밖(닫힘)이므로 판정상 문제는 아니다. 다만 측면 우선순위 지시는 "없음"인데 d2가 runbooks 규칙을 적용했다면 지시와 결과의 경계가 흐려진다(NOTES 자기 설명 기준이며 본문에서 단정할 수 없음).

### 시안 간 차별성
쌍둥이는 아니다. 문서 순서(d1: 근거 파일 표와 하는 일 → 설치 → 호출, d2: 현재 상태 표 → 목적 → 기능), 포함 범위(d1: 설치·요구사항, 시안 지시 설명, 용어 부록 / d2: build_registry 절, 오류 줄 전수, IndexError, 규칙 사례 표), 서술 방식(d1 해설형 / d2 참조형)이 다르다. 다만 지시는 같고(SKILL 규칙 "같은 조합의 시안끼리 다르게 쓰라는 지시를 넣지 않는다"), 사실 코어(숫자, 절차, 표)는 거의 같은 원자료에서 나와 항목 목록은 겹친다. 독립 실행만으로 구조가 달라진다는 SKILL 가정은 이번에도 맞았다.

### writing-maestro 개선 후보
1. (추정, 1회 관찰) 두 시안 NOTES가 같은 레포 결함을 독립적으로 발견했다: registry.md "고치는 법"의 스킬 제거 항목에 매니페스트 정리 누락(`registry.md:8`)과 `registry_check.py` 얕은 경로 IndexError. 둘 다 레포 수정은 하지 않아(읽기 전용) 메인 대화가 후속 처리해야 하는데, SKILL.md는 docs 시안의 "레포 쪽 발견"을 어디에 모아 넘길지 정하지 않는다. 8절 결과 표나 brief에 "시안이 발견한 레포 쪽 문제" 줄을 두는 것을 검토할 만하다.
2. (추정) 과제가 "writing-maestro 자체를 설명"인 자기참조형인데 brief에 "사실 대조 원본 목록"(SKILL.md, registry.md, scripts, tests, 매니페스트)이 입력 자료로 정리돼 있어 두 시안의 사실 정확도가 높았다. 이 방식(입력 자료에 원본과 검증 명령을 명시)을 docs 과제 brief의 기본 항목으로 올릴 가치가 있다.
3. (추정) brief의 요구 "종합 가이드"와 technical-writing의 inflated adjective 규칙이 충돌해 시안이 제목을 바꿨다. 시안 지시에 "사용자가 지정한 제목·명칭은 스킬의 금지어 규칙보다 우선하지 않는지 NOTES에 밝힌다" 정도의 한 줄을 두면 의도 이탈이 NOTES에서 보이게 된다(지금은 가정란에 적혀 있어 추적은 가능).
4. (추정) 두 시안이 모두 "커밋 `fe1a813`, 2026-10-31, 작업 트리 clean"이라는 시점 고정 문구를 본문에 넣었다. 유지보수 문서에서는 레포가 바뀌면 낡는다. 시안 지시의 "주의"에 "시점 고정 값은 한 곳에 모으고 재측정 명령을 함께 둔다"를 두면 d2 방식(현재 상태 표)으로 수렴한다. 현재는 두 시안의 선택에 맡겨져 있다.
5. 이 과제에서 조합 선택 과정(combo 2 writing-runbooks, combo 3 writing-design-docs 후보 제외 없이 사용자가 combo 1 선택)은 순위·추천 금지 규칙과 충돌 없이 작동했다. 개선 필요 없음.
