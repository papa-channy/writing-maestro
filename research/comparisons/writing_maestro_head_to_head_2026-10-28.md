# Writing Maestro — 유사 스킬 실제 작동 비교 v1

**일자:** 2026-10-28 · **상태:** HEAD-TO-HEAD DOCUMENT INSPECTION / NOT BENCHMARKED · **대상:** 24개 과거 잠정 클러스터, 33개 비교쌍

## 판정 방법

선행 군집 이름·문서 파일명은 판정 기준으로 쓰지 않았다. 각각의 `SKILL.md` 본문에서 **(1) 호출 전제와 입력, (2) 수행 단계, (3) 실제 산출물·부작용, (4) 명시된 NOT 조건, (5) 의존성·도구 요구**를 읽어 차이를 기록했다. 이 파일은 배포 레지스트리가 아닌 **변경 가설**이다. 전체 405개를 모두 본문 검토한 결과가 아니며, 1차 선정 스킬도 검증 완료로 표현하지 않는다.

정확한 경계가 알려지지 않은 것은 실험 과제로 둔다. 서로 다른 경계가 관찰되면 **SPLIT**, 실제 내용 중복이면 **DEDUPLICATE**, 독립 도메인과 무관하면 **REASSIGN_NEIGHBOR**, 메커니즘은 비슷하지만 두 축이 유효하면 **KEEP_TWO_POSSIBLE**, 도구/권한이 과하면 **DOWNRANK_DEPENDENCY**로 기록한다. 새 군집 수를 목표로 맞추지 않는다.

## 강한 증거 8건

1. **동일 명칭의 서로 다른 계약:** GitHub `prompt-optimizer`는 사용자 채팅에 붙이는 완성 요청문(플레이스홀더 금지), Sentry `prompt-optimizer`는 시스템/개발자/에이전트 프롬프트의 모델 이전·평가 루프다. 명칭만 같고 기능은 다르다.
2. **의존성 차이:** `boost-prompt`는 Joyride 도구/클립보드를 요구한다. `prompt-improving`은 원문의 의도를 보존하는 교정 규칙을 요구하고, 따옴표 입력이 없는 경우 질문 후 종료한다.
3. **추가 정보 수집 ≠ 요구사항 명세:** `interview-me`는 사용자의 잠재 의도 탐색과 명시 확인, `requirements-clarity`는 이미 확인된 기능의 수용 기준·PRD 완성을 중시한다.
4. **에이전트용 글 ≠ 컨텍스트 배치:** `writing-for-agents`는 조건부 참조/분기/완료 판단의 문장 메커니즘, `context-engineering`은 언제 어떤 정보를 컨텍스트에 올리는지 계층 구성을 다룬다.
5. **문서 유형은 상태를 보존해야 한다:** `writing-design-docs`는 논의 중인 변경 제안, `recording-decisions`는 확정된 선택의 불변 기록이다. 같은 ADR 계열로 병합해서는 안 된다.
6. **중복 제거 실증:** Anthropic과 Sentry의 `doc-coauthoring` SKILL.md는 장문행 집합 유사도 약 0.996, 앞쪽 376행이 동일한 실질적 복제/파생 판본이다(파일 해시는 다름). 독립 후보로 두지 않는다.
7. **검수의 변경 권한 차이:** `docs-sync-audit`는 읽기 전용 감사를 기본으로 하고, `awesome-claims-audit`는 공개 주장 확인 후 고치기까지 흐름에 포함한다. 검수 요청만 받은 상황에서 후자를 그대로 호출하면 권한을 넘길 수 있다.
8. **학술 리뷰의 깊이 차이:** `evidence-synthesis`는 프로토콜·선별·비뚤림·근거 확실성까지 연구 설계로 다루고, `literature-review`는 문헌 동향과 기술 계보 중심의 서술적 근거 합성을 한다.

## 비교 결과 전수표

| 쌍 | 이전 군집 | A → B | 실제 차이(요약) | 잠정 조치 |
|---|---|---|---|---|
| P01 | C01 | [write-agent-prompts](https://github.com/inanna-malick/agent-skills/blob/main/skills/write-agent-prompts/SKILL.md) ↔ [prompt-optimizer](https://github.com/getsentry/skills/blob/main/skills/prompt-optimizer/SKILL.md) | 개념·방법론을 고밀도로 압축해 에이전트에 전달 vs 계약 수집→모델 전략→프롬프트 작성→평가/반복 및 모델 이식 | `SPLIT` |
| P02 | C01 | [prompt-optimizer](https://github.com/getsentry/skills/blob/main/skills/prompt-optimizer/SKILL.md) ↔ [prompt-optimizer](https://github.com/github/awesome-copilot/blob/main/skills/prompt-optimizer/SKILL.md) | 시스템/개발자/에이전트 프롬프트와 반복 평가 vs 채팅 UI에 붙여 넣을 완성형 단일 프롬프트, 플레이스홀더 금지 | `SPLIT` |
| P03 | C02 | [prompt-improving](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/prompt-improving/SKILL.md) ↔ [prompt-optimizer](https://github.com/github/awesome-copilot/blob/main/skills/prompt-optimizer/SKILL.md) | 인용된 기존 프롬프트의 의도·문체 유지와 최소 보강 vs 미완성 생각도 완성된 단일 채팅 프롬프트로 변환 | `KEEP_ADJACENT` |
| P04 | C02 | [boost-prompt](https://github.com/github/awesome-copilot/blob/main/skills/boost-prompt/SKILL.md) ↔ [prompt-improving](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/prompt-improving/SKILL.md) | Joyride를 통한 대화형 질의·클립보드 복사 vs 원문 재작성과 맥락 기반 부족정보 점검 | `DOWNRANK_DEPENDENCY` |
| P05 | C03 | [requirements-clarity](https://github.com/softaworks/agent-toolkit/blob/main/skills/requirements-clarity/SKILL.md) ↔ [interview-me](https://github.com/addyosmani/agent-skills/blob/main/skills/interview-me/SKILL.md) | 모호한 구현 요구를 PRD/수용 기준으로 구체화 vs 사용자가 실제 원하는 목적을 일문일답으로 파악·명시적 확인 | `SPLIT` |
| P06 | C03 | [idea-refine](https://github.com/addyosmani/agent-skills/blob/main/skills/idea-refine/SKILL.md) ↔ [requirements-clarity](https://github.com/softaworks/agent-toolkit/blob/main/skills/requirements-clarity/SKILL.md) | 대안 발산·가정 압박·아이디어 수렴 vs 요구사항 갭 탐지와 PRD 완성 | `SPLIT` |
| P07 | C04 | [writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md) ↔ [context-engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/context-engineering/SKILL.md) | 에이전트가 읽는 문서의 포인터/분기/완료조건 표현 vs 규칙·스펙·코드·로그를 언제 로드할지 컨텍스트 계층 구성 | `SPLIT` |
| P08 | C04 | [writing-project-constitution](https://github.com/mazrean/agent-skills/blob/main/skills/writing-project-constitution/SKILL.md) ↔ [writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md) | always-loaded CLAUDE.md/AGENTS.md의 포함·배제·템플릿 vs 모든 에이전트용 문서에서 정보를 발견하게 하는 표현 규칙 | `SPLIT` |
| P09 | C05 | [agent-md-refactor](https://github.com/softaworks/agent-toolkit/blob/main/skills/agent-md-refactor/SKILL.md) ↔ [claude-md-improver](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/skills/claude-md-improver/SKILL.md) | 큰 지시문 파일을 분리해 링크·중복·충돌 정리 vs CLAUDE.md 목록화·점수 기반 감사 후 표적 수정 | `SPLIT` |
| P10 | C06 | [doc-coauthoring](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md) ↔ [doc-coauthoring](https://github.com/getsentry/skills/blob/main/skills/doc-coauthoring/SKILL.md) | 맥락 수집→구조 정제→독자 테스트 과정이 사실상 동일; Sentry는 말미 출처 표기가 추가된 판본 | `DEDUPLICATE` |
| P11 | C06 | [doc-coauthoring](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md) ↔ [writing-and-editing](https://github.com/matt-riley/agent-skills/blob/main/skills/writing-and-editing/SKILL.md) | 독자 테스트까지 포함한 단계별 공동집필 vs 문서 작성·가독성·짧은 메타데이터 교정을 묶은 넓은 도구 | `KEEP_ADJACENT` |
| P12 | C07 | [create-specification](https://github.com/github/awesome-copilot/blob/main/skills/create-specification/SKILL.md) ↔ [writing-feature-spec](https://github.com/mazrean/agent-skills/blob/main/skills/writing-feature-spec/SKILL.md) | 명세 문서 파일을 구조화하여 작성 vs PRD를 참조 파일이 있는 Agent Skill 디렉터리로 출력 | `SPLIT` |
| P13 | C07 | [create-specification](https://github.com/github/awesome-copilot/blob/main/skills/create-specification/SKILL.md) ↔ [to-spec](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md) | 신규 명세 템플릿 작성 vs 기존 대화 내용을 합성해 이슈 트래커에 스펙을 발행 | `SPLIT` |
| P14 | C08 | [writing-design-docs](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-design-docs/SKILL.md) ↔ [documentation-and-adrs](https://github.com/addyosmani/agent-skills/blob/main/skills/documentation-and-adrs/SKILL.md) | 미결정 제안의 Why/What·비용·미해결 쟁점 구조 vs 확정/주요 아키텍처 선택의 근거 문서화까지 포괄 | `KEEP_DISTINCT_FROM_C09` |
| P15 | C09 | [recording-decisions](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/recording-decisions/SKILL.md) ↔ [architecture-decision-records](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/skills/architecture-decision-records/SKILL.md) | ADR와 가벼운 결정 로그를 구분하고 확정 기록을 불변 취급 vs ADR 수명주기·관리·인덱스 중심 | `KEEP_TWO_POSSIBLE` |
| P16 | C10 | [writing-runbooks](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-runbooks/SKILL.md) ↔ [incident-runbook-templates](https://github.com/wshobson/agents/blob/main/plugins/incident-response/skills/incident-runbook-templates/SKILL.md) | 실행 검증 여부·롤백·시나리오별 사실성을 요구하는 범용 운영 절차 vs 사고 등급·에스컬레이션·복구 중심 장애 대응 템플릿 | `KEEP_TWO_POSSIBLE` |
| P17 | C11 | [docs-sync-audit](https://github.com/github/awesome-copilot/blob/main/skills/docs-sync-audit/SKILL.md) ↔ [awesome-claims-audit](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-claims-audit/SKILL.md) | 코드/설정 대비 전체 문서 변경 누락을 읽기 전용으로 탐지 vs 외부 공개 주장 문장을 출처 코드까지 추적 후 수정·재검증 | `SPLIT` |
| P18 | C12 | [build-evidence-map](https://github.com/github/awesome-copilot/blob/main/skills/build-evidence-map/SKILL.md) ↔ [source-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/source-driven-development/SKILL.md) | 찬성·반박·한정·미확인 근거 사이의 논리 관계를 도식화 vs 공식 API 문서에 코드 구현 판단을 결박 | `REASSIGN_NEIGHBOR` |
| P19 | C13 | [reviewing-technical-prose](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/reviewing-technical-prose/SKILL.md) ↔ [awesome-grammar-check](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-grammar-check/SKILL.md) | 기술 주장/정본/구조 문제를 심각도별 진단하고 결함에만 최소수정 vs 문법·논리·흐름의 제안 목록을 작성하되 본문은 수정하지 않음 | `SPLIT` |
| P20 | C14 | [doubt-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/doubt-driven-development/SKILL.md) ↔ [requesting-code-review](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md) | 작성 진행 중 결정·가정에 대해 새 맥락 반증자 호출 vs 기능/코드 구현 후 리뷰 요청 절차 | `REASSIGN_NEIGHBOR` |
| P21 | C15 | [evidence-synthesis](https://github.com/anayy09/claude-research-skills/blob/main/evidence-synthesis/SKILL.md) ↔ [literature-review](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/literature-review/SKILL.md) | 프로토콜·포함 기준·선별 로그·비뚤림 위험·GRADE까지 갖춘 근거 합성 연구 vs 문헌 지형과 기술 계보를 추적해 비교 서술 | `SPLIT` |
| P22 | C15 | [evidence-synthesis](https://github.com/anayy09/claude-research-skills/blob/main/evidence-synthesis/SKILL.md) ↔ [systematic-review-prisma](https://github.com/KalarisLabs/research-agent-skills/blob/main/skills/systematic-review-prisma/SKILL.md) | 다양한 공식 근거 합성 유형과 적합 도구 선택 vs PRISMA 2020 프로토콜·검색·중복 제거·플로우 다이어그램 구체 실행 | `KEEP_TWO_POSSIBLE` |
| P23 | C16 | [citation-verification](https://github.com/KalarisLabs/research-agent-skills/blob/main/skills/citation-verification/SKILL.md) ↔ [citation-management](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/citation-management/SKILL.md) | 기존 참고문헌/DOI의 실재 여부·메타데이터를 검증 vs 논문 탐색·메타데이터 수집·BibTeX 생성·관리 | `SPLIT` |
| P24 | C17 | [general-writing](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/general-writing/SKILL.md) ↔ [awesome-document-style](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-document-style/SKILL.md) | 문장의 자연스러운 저자 목소리·AI식 표현을 다루는 일반 편집 vs Markdown 문서의 군더더기·구조·특정성·수치/출처 관리 | `SPLIT` |
| P25 | C17 | [prose-naturalizer](https://github.com/anayy09/claude-research-skills/blob/main/prose-naturalizer/SKILL.md) ↔ [awesome-document-style](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-document-style/SKILL.md) | AI식 문체 패턴을 세부 진단·개정 vs 문서 구조와 검증 가능한 주장에 중점을 둔 일반 편집 | `SPLIT` |
| P26 | C18 | [awesome-content-voice](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-content-voice/SKILL.md) ↔ [awesome-style-mimic](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-style-mimic/SKILL.md) | 사용자 자신의 샘플·인터뷰에서 음성 프로필 구축 vs 타 웹사이트를 크롤링해 외부 브랜드 스타일 가이드를 생성·적용 | `SPLIT` |
| P27 | C19 | [non-autoregressive-writing-pass](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/non-autoregressive-writing-pass/SKILL.md) ↔ [writing-cadence](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/writing-cadence/SKILL.md) | 완성 원고 전체 논증을 보고 제목/문단 첫 문장/전환을 재설계 vs 문장 길이·반복 도식·호흡을 의미 단위로 보정 | `SPLIT` |
| P28 | C20 | [scene-craft](https://github.com/danjdewhurst/story-skills/blob/main/skills/scene-craft/SKILL.md) ↔ [chapter-writing](https://github.com/danjdewhurst/story-skills/blob/main/skills/chapter-writing/SKILL.md) | 장면의 목표·갈등·시점·하위텍스트 등 설계 vs 장면/장 전체의 실제 산문 초안 작성 | `SPLIT` |
| P29 | C21 | [premise-workshop](https://github.com/danjdewhurst/story-skills/blob/main/skills/premise-workshop/SKILL.md) ↔ [theme-craft](https://github.com/danjdewhurst/story-skills/blob/main/skills/theme-craft/SKILL.md) | 착상에서 전제·로그라인·형식 선택까지 검증 vs 이미 존재하는 이야기의 테마·주장·모티프·인물 변화 추적 | `SPLIT` |
| P30 | C22 | [SKILL](https://github.com/tizzy916/humanities-writing-companion/blob/main/SKILL.md) ↔ [SKILL](https://github.com/nqmn/academic_writer/blob/main/SKILL.md) | 해석학·개념 구별·저자의 논증 주체성 보존에 초점 vs 연구 논문 전 과정·체계적 문헌고찰·서지 분석까지 광범위한 작업 라우팅 | `SPLIT` |
| P31 | C23 | [copywriting](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copywriting/SKILL.md) ↔ [awesome-copywriting](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-copywriting/SKILL.md) | 페이지 단위 포지셔닝·고객 맥락·전환 카피 작성 vs 버튼/에러/제목/스토어 설명 등 짧은 제품 텍스트의 상태별 압축 | `SPLIT` |
| P32 | C24 | [scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) ↔ [scientific-writing](https://github.com/KalarisLabs/research-agent-skills/blob/main/skills/scientific-writing/SKILL.md) | 인용·기밀·저자 승인과 검증을 공통 기반으로 하는 고유사도 변형본(서로 다른 검증/버전 메타데이터) | `NEAR_DUPLICATE` |
| P33 | C24 | [scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) ↔ [paper-writing](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/paper-writing/SKILL.md) | 기밀/저자 책임/근거의 진실성·서지 검증 통제 vs 연구 주장 구조·표기·서론/방법/실험 등 실제 기술 논문 집필 | `SPLIT` |

## 현 시점의 클러스터 재편 권고 (확정 레지스트리가 아님)

- **즉시 사실상 병합:** `doc-coauthoring` 계열 2개는 하나의 계보로 묶는다. `scientific-writing` 동명 2개는 동일 기능 계보 후보로 묶되 차이 및 라이선스를 검토한다. 서로 다른 저장소 수가 기술 다양성을 뜻하지 않도록 중복 플래그를 유지한다.
- **분리 우선:** ① 단일 채팅 요청문 vs 재사용 가능한 시스템/에이전트 프롬프트의 평가 최적화, ② 사용자의 의도 탐색 vs 명세화, ③ 에이전트 문서의 작성 규칙 vs 컨텍스트 적재 구조, ④ 논의 중인 설계 vs 확정 결정, ⑤ 문서 드리프트 읽기 감사 vs 공개 주장 수정, ⑥ 체계적 근거 합성 vs 서술적 문헌 합성, ⑦ 미시적인 문장 리듬 vs 완성 원고 전체 논증 연결.
- **단순 인접성을 해제:** `source-driven-development`는 근거 지도 작성의 직접 경쟁자가 아니고 구현 과정의 공식 문서 검증에 가깝다. `requesting-code-review`도 글쓰기 과정의 반증 검토와 다르다.
- **의존성·권한 검토:** `technical-writing`은 riekelt 하위 스킬들의 필수 전제, `boost-prompt`는 Joyride 전제, `grill-me`는 외부 `grilling` 호출만 수행, `to-spec`은 이슈 트래커 쓰기 부작용이 있다. 이는 성능이 아닌 **실행 가능성 게이트**로 관리한다.
- **원래 유사도 결과는 불변 보존:** 과거 24개 그룹/48개 자동 클러스터/405개 후보는 `research/snapshots/2026-10-28/`에서 수정하지 않는다. 이번 문서의 분리·병합 가설을 그 위에 덧씌우는 방식으로 추적한다.

## 실제 우열 평가에 필요한 대조 실험

**아직 실행하지 않았다.** 동일 입력·동일 기준 모델·도구 권한 통제·최소 3회 반복을 적용해야 구조적 설계의 우수성이 결과 품질로 이어지는지 확인 가능하다. 네 가지 대표 대조 입력을 권한다.

- `Goal.md`를 기존 결정과 함께 작성: 정보 누락·정본 충돌·근거 없는 목표 생성 여부.
- `CLAUDE.md`를 기존 정책들과 정합적으로 재구획: 토큰/링크/중복·기존 문서 훼손 여부.
- 설계 변경안에 대한 검수 프롬프트 작성: 검수 수행과 지시문 작성의 구분, 재현 가능한 근거 요구 여부.
- 외부 논문 조사 지시문 생성: 프로토콜 강요 여부, 검증 범위·근거 기준·검토 게이트의 명확성.

결과를 비교할 때는 문서 산출 품질뿐 아니라 **호출 비용, 외부 도구 요구, 편집 부작용, 사용자 의도 이탈, 작업 단계와의 부적합**도 기록해야 한다. 우승자 수는 평가 이전에 고정하지 않는다.

## 데이터와 출처

동일 디렉터리의 `2026-10-28-head-to-head.csv`는 각 비교쌍의 원본 GitHub `SKILL.md` URL, 차이, 조치, 활성화 경계, 미검증 항목을 보존한다. 일부 후보는 리포지토리 내부 자매 스킬/참조 파일을 필요로 한다. 이번 단계의 확인은 **실제 스킬 본문을 읽은 비교**이며, 스킬을 설치하거나 사용자 프로젝트에 실행하지 않았다.
