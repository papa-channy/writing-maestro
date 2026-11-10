# 09 llm-hub-api-spec 평가

폴더: `/Users/chan/Developer/workflow/AI-Studio/writing-drafts/20261107-1650-llm-hub-api-spec`
평가 단위: 시안 3개(combo2 d1, combo3 d1, combo4 d1). compare.html의 id 접두사는 c20 / c30 / c40 / c41이고, c41은 combo4의 보조 파일 `API_SPEC-research.md`(리서치 DTO)다. 즉 `.md` 외의 별도 시안은 없다. combo4는 `API_SPEC.md`(68KB)와 `API_SPEC-research.md`(15KB) 둘을 한 시안으로 평가했다. `final/` 폴더는 없다.

## 점수표

| 시안 | C1 적합성 | C2 판단·행동 | C3 정확성 | C4 구조 | C5 문장 | C6 구체성 | C7 준비도 | 합 |
|---|---|---|---|---|---|---|---|---|
| combo2 documenting-contracts → reviewing-technical-prose | 4 | 4 | 4 | 4 | 4 | 3 | 4 | 27 |
| combo3 create-specification → general-writing | 3 | 3 | 4 | 3 | 3 | 5 | 3 | 24 |
| combo4 documenting-contracts → writing-for-agents | 4 | 5 | 4 | 5 | 4 | 4 | 4 | 30 |

## 사실 대조 범위

대조 대상 코드: `~/Developer/module-server/llm-hub`. 시안이 고정한 `92b5a36`과 현재 HEAD `56b48ae` 사이에 `src/`는 `docs-writer.ts` 하나만 바뀌어(문서 생성기) 계약 대조에 영향이 없다.
직접 대조한 주장(모두 코드와 일치):
- 포트·호스트 기본값 18734/127.0.0.1, `AUTH_MODE` 기본 permissive (`src/config.ts:56-58`)
- 본문 상한 32 MiB(passthrough)/10 MiB, 413 처리 (`src/server/middleware.ts:12-27`)
- `HUB_RPM` 기본 1000 (`src/config.ts:33`), `x-project-id` 앞 64자 (`src/auth/middleware.ts:36`)
- `key_conflict`, `project_reserved`(대소문자 무관) (`src/auth/middleware.ts:168-173`)
- 동기 배치 50, 비동기 200, 결과 TTL 24시간, 동시성 상한 20 (`src/config.ts:130-135`)
- 번역 경로 role 3종 (`src/proxy/validation.ts:24`), 재시도 상수 `RETRY_PRE_SEND_MAX` 2, `RETRY_AFTER_CAP_S` 60, `ATTEMPT_MAX` 5 (`src/config.ts:109-113`)
- 리서치 상한 `RESEARCH_MAX_TARGETS` 10, `RESEARCH_PROMPT_MAX_CHARS` 100000, 출력 지시 문장 (`src/research/validate.ts:110`)
- 예약 본문 바이트/3 (`RESERVE_BYTES_PER_TOKEN` 기본 3), 레지스트리 갱신 14일, Windows/WSL 포트 18735(`docs/STATUS.md:9`)
- 엔드포인트 수: 라우트를 직접 세면 26개(`openapi.json` 18경로 + 스펙에 없는 8)
- 스펙 재생성·인용 줄 전수 대조는 하지 않았다(NOTES.md의 주장이라 대조 대상으로만 봤다).
- 내부 앵커(`#...`) 링크는 세 시안 모두 스크립트로 확인: 깨진 링크 0.

미확인(코드를 읽지 못했거나 실행이 필요): combo3의 "`/multi`에 `temperature: null`이면 HTTP 200에 항목별 오류" (`validateMultiRequest`가 이 값을 걸러내는지 확인하지 못함), "Anthropic 모델에 `tools`를 보내면 어댑터가 싣지 않는다"(`anthropic-adapter.ts`에서 `tools` 문자열이 없음을 확인했을 뿐 요청 경로 전체는 못 봄), 전체 오류 코드 표의 줄 번호 인용, Hono `%2F` 처리(combo4가 스스로 "실행 확인 안 함"으로 표시).

---

## combo2 (documenting-contracts → reviewing-technical-prose)

파일: `combo2-documenting-contracts+reviewing-technical-prose/d1/API_SPEC.md` (568줄, 63KB)

**한 줄 요약**: 규약 → 엔드포인트 색인+의미 → DTO → 오류의 가장 표준적인 계약 문서이고, 모든 서술에 `src/...:줄` 출처를 단 뒤 이름 붙은 결함만 최소 수정한 시안.

**가장 큰 강점**: 근거 밀도와 문장 절제. 예: "리서치 오류는 모두 500·503만 true"를 입장 거부(429 `rate_limited`는 true)와 모순된다고 잡아 `API_SPEC.md:186`에서 "리서치 고유 코드의 `x-should-retry`는 500과 503이 `true`, 나머지가 `false`이고, 입장 거부는 입장 표의 재시도 값을 따른다"로 고친 흔적이 있다. 항목 요청 ID, 결과 24시간 삭제(`:180`)처럼 호출 코드가 분기에 쓰는 값이 출처와 함께 있다.

**가장 큰 결함**: 독자를 어디로 보낼지의 안내가 없다. 규약 → 색인 순서의 고정 진행이고(`:7-86`), "하려는 일 → 읽을 곳" 같은 진입점이 없다. 또 예시가 UsageRecord JSON 하나(`:320-322`)뿐이라 호출 코드 작성자가 실제 요청 한 건을 그대로 가져다 쓸 수 없다(C6 3).

**사실 오류**: 대조한 범위에서는 발견하지 못함. (엔드포인트 색인 26행은 실제와 일치.)

**감점 메모**: 점검 모드·허브 RPM 등 일부 운영 상태를 별도 절 없이 흩어 둔 점(C4), 영어 식별자 중심이라 문장은 한다체로 일관(C5 4).

## combo3 (create-specification → general-writing)

파일: `combo3-create-specification+general-writing/d1/API_SPEC.md` (771줄, 66KB)

**한 줄 요약**: create-specification의 11절 템플릿(Purpose, Definitions, REQ-/SEC-/CON- 번호, Acceptance Criteria, Test Automation Strategy, Dependencies 등)에 llm-hub 계약을 채운 형식 규격서형 시안.

**가장 큰 강점**: 구체성. 실행 가능한 curl 4개, OpenAI SDK 설정, 오류 코드 추출 함수(TypeScript `hubErrorCode`, `:700-712`), 실패 사례 8개(`:715-722`, 예: 오타 난 `provider` 필터는 400이 아니라 전체 목록), Given/When/Then 12개(`:610-621`). 호출 코드를 쓰는 사람과 Claude Code 세션에 바로 복사해 쓸 재료가 셋 중 가장 많다.

**가장 큰 결함**: 템플릿이 과제 밖의 절을 채우게 만들었다. 브리프(`brief.md` 1절)는 "호출자용 명세, admin·내부 범위 밖"인데 6절 Test Automation Strategy가 Vitest 파일명 18개를 나열하고(`:623-630`), 8절이 "Compliance Dependencies"와 "Third-Party Services"에 항목 하나씩을 채운다(`:646-675`). 독자에게 필요 없는 내용이다. 머리의 YAML(`version`, `last_updated`, `owner`, `tags`, `:1-8`)도 사실 확인이 안 되는 자리표시다. 절 제목은 영어와 한국어가 섞여 있다(`Introduction`, `Requirements, Constraints & Guidelines`).

**사실 오류**: 확인된 것 없음. 미확인 두 곳은 위 "미확인" 참조.

**감점 메모**: 절 번호가 `4.1.2`, `4.1.5`처럼 깊고, 오류 분기는 본문 4.1.5와 3절 GUD, 9절 함수에 나뉘어 있다(C4 3). 용어가 "장치 키(device key)"와 본문의 "기기"로 갈린다(C5). 허브가 `x-llm-hub-*`로 호출을 기록한다는 설명 등 일부 문장은 영어 명세 직역투("전제는 다음과 같다")(C5 3).

## combo4 (documenting-contracts → writing-for-agents)

파일: `combo4-documenting-contracts+writing-for-agents/d1/API_SPEC.md` (724줄, 68KB) + `API_SPEC-research.md` (15KB)

**한 줄 요약**: documenting-contracts 골격 위에 "읽는 순서와 완료 기준" 절을 앞에 얹어, 사람보다 호출 코드를 쓰는 에이전트가 읽고 체크리스트로 자기 작업이 끝났는지 판단하게 만든 시안. 리서치 DTO는 별도 파일로 분리.

**가장 큰 강점**: 진입점과 종료 조건. `:9-28`의 "하려는 일별 한 갈래만 읽는다" 5갈래와 8개 완료 기준(예: "`x-llm-hub-warning`이 오면 테스트를 실패로 본다", "비동기 배치는 `status: "completed"`를 성공으로 읽지 않고 `summary.failed`를 확인") 덕분에 에이전트 세션이 문서 전체를 읽지 않고 필요한 절로 간다. 번역 경로 검사 순서 9단계(`:243-253`)처럼 "첫 실패가 응답을 정한다"로 오류의 원인을 역추적하게 해 준다.

**가장 큰 결함**: 엔드포인트 수 오기. 본문 `:206`은 "엔드포인트는 27개"라고 쓰지만 같은 문서의 표는 26행이고, 괄호 안 합산(7+1+1+1+4+5+1+2+2+2)도 26이다. 코드도 26(`src/server/app.ts:106-116` 마운트 기준). 숫자 하나지만 완료 기준을 에이전트가 기계적으로 대조할 때 어긋남을 만든다. 보조로, 코드 예시가 JSON 하나와 짧은 SSE 조각뿐이라 curl·SDK 호출 한 줄도 없다(C6 4).

**사실 오류**:
| 위치 | 글의 주장 | 실제 |
|---|---|---|
| `API_SPEC.md:206` | 엔드포인트는 27개 | 26개(표 26행, 같은 줄 합산 26, `app.ts` 마운트 기준 26) |

**감점 메모**: DTO를 두 파일로 나눈 결정은 브리프("진입 문서 `API_SPEC.md`, 여러 파일이면 폴더 안에 둠")와 맞지만, 호출 한 건의 맥락이 파일을 넘나든다(예: 리서치 오류는 본문, 필드는 보조 파일). 링크는 모두 유효(C4 5 유지). 코드 값 기록이 가장 촘촘(정책 헤더 표, 응답 헤더 표, 입장 거부 표의 `retry-after` 열)해 C2·C3는 높음.

---

## 프로젝트별 항목

### 시안 간 순위
1. combo4 (30): C2 5, C4 5. 에이전트가 읽는 문서라는 브리프 독자(Claude Code 세션)에 직접 맞춘 읽는 순서와 완료 기준이 결정적이다.
2. combo2 (27): C3·C5는 combo4와 같으나 진입점이 없어 C2·C4가 낮고 예시가 부족해 C6이 낮다.
3. combo3 (24): C6 5로 가장 구체적이지만 템플릿 잔재(C1·C2·C7)와 영어·한국어 혼용(C5)이 깎는다. 호출자 예시 부분만 따로 가져다 쓰기에는 가장 좋다.

### 조합 적합성
- 브리프는 "호출자용 계약 문서"인데 documenting-contracts(조합 2, 4)가 이 장르에 직접 맞다. 조합 3의 create-specification은 구현 명세 템플릿이라 호출자 독자와 어긋나 있고, 그 어긋남이 6·8절에 그대로 드러난다.
- reviewing-technical-prose(조합 2)는 후속 검토로서 근거 정확도에 실제로 기여했다(NOTES에 BLOCKER 2건 수정, 본문 `:186`에서 확인). 반면 writing-for-agents(조합 4)는 구조 지시가 무시되고(`wfa.structure` ignored) 진입 절과 완료 기준만 더했는데 이것이 독자(에이전트)에 가장 크게 효과를 냈다.
- 시안 지시와 결과 사이: NOTES.md의 "엔드포인트 26개 행을 awk로 확인"(combo2)은 본문과 일치한다. combo4 NOTES는 개수를 말하지 않으며 본문 숫자와 합산이 어긋난다(위 오류). combo3 본문의 "공개 경로 26개(4.3 표)"는 맞다.

### 시안 간 차별성
셋은 서로 다른 선택지였다. combo2와 combo4는 같은 기반(documenting-contracts)에서 나와 규약 → 엔드포인트 → DTO → 오류의 뼈대와 사실이 거의 같고, 차이는 combo4의 진입·완료 기준 절, 오류의 하위 분류(인증·정책·입장·번역·passthrough·리서치 7묶음), 파일 분할이다. 문장만 다른 쌍둥이는 아니지만 "같은 내용의 다른 포장"에 가깝다. combo3는 형식·예시·절 구성이 뚜렷이 다르다. 사용자가 비교로 얻는 새 정보는 (a) 진입 안내 유무, (b) 예시 유무, (c) 형식 규격 유무 세 축이다.

### writing-maestro 개선 후보
1. (추정, 한 번의 관찰) 브리프 "분량" 항목에 문서 내 예시·호출 샘플의 필요 여부를 적게 하면, 예시가 거의 없는 시안(combo2, combo4)과 예시 위주 시안(combo3)이 갈리는 일이 줄 수 있다. 이 과제에서 호출자가 가장 먼저 찾는 것은 curl 한 줄인데 두 시안에 없다.
2. (추정) 조합 후보 풀에서 create-specification 같은 템플릿 고정 스킬은, 템플릿 절이 과제 범위를 넘을 때(테스트 전략, 컴플라이언스) "채우지 않는 절"을 시안 지시에 명시하게 하면 군더더기가 줄 수 있다. 현재 시안 지시가 이를 막지 못해 6·8절이 채워졌다.
3. (추정) 숫자 요약 주장(엔드포인트 개수, 상한 개수)은 시안 지시에 "표를 센 값으로 쓴다"를 넣어 둘 수 있다. combo4의 27개는 표를 세지 않고 합산한 흔적이다.
4. 한 번의 관찰이라 일반화는 어렵지만, 독자가 "에이전트"로 명시된 브리프에서는 writing-for-agents 같은 진입·종료 기준 스킬을 항상 동반 후보로 올리는 규칙이 효과가 있었다. 레지스트리의 독자 태그에 이 연결이 있는지 확인해 볼 만하다.
