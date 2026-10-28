# Writing Maestro — 광역 발굴 및 데이터 기반 클러스터링 2차 조사

- 기준일: 2026-10-28
- **서로 다른 GitHub 스킬 경로 405개**, **저장소 31개** (이전 159개 포함)
- 유사도 기반 초기 소규모 집합 **48개** (의미적 완성 클러스터가 아님)
- `SKILL.md` 내부 확인을 거쳐 사후적으로 명명한 **24개 잠정 기능 묶음 / 대표 후보 28개**
- `riekelt/technical-writer`의 `technical-writing`은 의존 기반 스킬로 별도 고려

## 1. 중요한 범위 변경

이전처럼 문서 유형 또는 사용 분야를 사전에 정한 다음 스킬을 끼워 넣지 않았다. 글쓰기, 프롬프팅, 픽션, 학술 논증, 설득 카피, 저자 문체, 검수 등을 확장 탐색했다. GitHub 저장소 트리에서 개별 `SKILL.md` 경로를 확인하고 키 `(repo,path)`로 중복 제거했다.

## 2. 클러스터링 절차와 한계

1. **원본 수집:** 기존 분류/추천 등급은 벡터에서 제외. 개별 스킬명, 경로와 일부 직접 읽은 설명을 사용했다.
2. **비지도 초기 탐색:** TF-IDF(단어 1~2그램) → SVD 75차원 → KMeans 여러 k 값으로 후보 집합 48개를 얻었다. 이 과정은 분류표를 사용하지 않았다.
3. **실패 확인:** 초기 스킬명 유사도만으로는 이질적인 스킬이 섞이고 이름이 다른 같은 기능을 놓친다. 실루엣 값 0.275는 높지 않다. k 탐색 상한에서 최고값이 나왔으므로 48이 최적 군집수라는 주장은 **불가**하다.
4. **대표 텍스트 점검:** 관련 `SKILL.md` 본문을 읽어 실제 입력/출력/금지조건/방법/의존성을 비교했다. 거기서 확인된 유사 기능만 사후적으로 24개 잠정 묶음으로 정리했다.
5. **채택 범위:** 전체 405개가 24개 의미 클러스터로 검증되어 분류된 것이 **아니다**. 현재 기능 묶음 소속은 본문 검토한 28개 우선 후보에만 부여했다. 나머지는 원본 미시 군집을 남기고 클러스터 미확정으로 표기했다.

## 3. 사후 도출된 24개 기능 묶음과 28개 대표 후보

| 잠정 클러스터 | 확인된 유사 기능 | 우선 후보 (원본 저장소) |
|---|---|---|
| C01 에이전트 지시문 설계 | 기존 맥락을 압축해 에이전트가 선택할 행동·판단 경계를 전달 | [write-agent-prompts](https://github.com/inanna-malick/agent-skills/blob/main/skills/write-agent-prompts/SKILL.md) · [prompt-optimizer](https://github.com/getsentry/skills/blob/main/skills/prompt-optimizer/SKILL.md) |
| C02 프롬프트 개정·명확화 | 사용자 요청의 의도를 보존하면서 입력·출력·제약의 모호함을 줄임 | [prompt-improving](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/prompt-improving/SKILL.md) |
| C03 요구사항 질문·범위 확정 | 작성 전에 미정의 요구·제약·승인 기준을 좁혀 명세 가능 상태로 만듦 | [requirements-clarity](https://github.com/softaworks/agent-toolkit/blob/main/skills/requirements-clarity/SKILL.md) |
| C04 에이전트 운영 컨텍스트 문서 | CLAUDE.md/AGENTS.md 내용과 포인터, 로드 조건, 권한 경계 설계 | [writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md) |
| C05 지시문 문서 재구획 | 비대한 에이전트 안내서를 정본·참조로 분리하고 모순·중복을 제거 | [agent-md-refactor](https://github.com/softaworks/agent-toolkit/blob/main/skills/agent-md-refactor/SKILL.md) |
| C06 협업적 문서 초안·독자 테스트 | 컨텍스트 수집, 아웃라인, 초안, 독자 이해도 테스트 | [doc-coauthoring](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md) |
| C07 요구·계약 명세 | 요구조건·인터페이스·검증 조건이 분명한 명세 산출 | [create-specification](https://github.com/github/awesome-copilot/blob/main/skills/create-specification/SKILL.md) |
| C08 설계 제안·대안 논증 | 제안과 사실, 비용과 이익, 대안과 잔여 리스크를 분리 | [writing-design-docs](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-design-docs/SKILL.md) |
| C09 확정된 결정 보존 | 이미 결정된 내용과 그 근거·대안·후속 변경을 불변 기록 | [recording-decisions](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/recording-decisions/SKILL.md) |
| C10 실행 절차·운영 가이드 | 실행 단계, 실패 대응, 롤백 및 실제 검증 상태를 명시 | [writing-runbooks](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-runbooks/SKILL.md) |
| C11 문서-근거 드리프트 감사 | 문서의 주장과 실제 코드·설정을 대조해 불일치를 식별 | [docs-sync-audit](https://github.com/github/awesome-copilot/blob/main/skills/docs-sync-audit/SKILL.md) · [awesome-claims-audit](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-claims-audit/SKILL.md) |
| C12 논거-근거 관계 모델링 | 주장·반박·조건·미확인을 추적 가능한 근거 구조로 분해 | [build-evidence-map](https://github.com/github/awesome-copilot/blob/main/skills/build-evidence-map/SKILL.md) |
| C13 기술 문장 검수·최소 수정 | 문서 결함을 위치·심각도·근거와 함께 판정하고 필요한 만큼만 수정 | [reviewing-technical-prose](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/reviewing-technical-prose/SKILL.md) |
| C14 독립적 반증·설계 압박 | 현재 가설의 숨은 가정과 반례를 fresh-context로 공격적으로 검증 | [doubt-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/doubt-driven-development/SKILL.md) |
| C15 연구 근거 통합·문헌 합성 | 연구 질문에 대해 비교·평가·근거 합성을 실시 | [evidence-synthesis](https://github.com/anayy09/claude-research-skills/blob/main/skills/evidence-synthesis/SKILL.md) · [literature-review](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/literature-review/SKILL.md) |
| C16 서지 사실 검증 | 참고문헌 DOI·저자·제목·연도 실재 여부를 외부 DB에 대조 | [citation-verification](https://github.com/KalarisLabs/research-agent-skills/blob/main/skills/citation-verification/SKILL.md) |
| C17 명료한 일반 글 편집 | 문장 명료성·중복·과장 표현을 저자 의미 보존 아래 개선 | [general-writing](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/general-writing/SKILL.md) · [awesome-document-style](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-document-style/SKILL.md) |
| C18 저자 목소리 프로파일링 | 저자 글을 분석해 재사용 가능한 문체 증거와 제한점을 기록 | [awesome-content-voice](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-content-voice/SKILL.md) |
| C19 완성 원고의 거시적 문장 연결 | 완성된 전체 논증을 참조해 제목·문단 첫문장·전환을 재검토 | [non-autoregressive-writing-pass](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/non-autoregressive-writing-pass/SKILL.md) |
| C20 장면 단위 서사 구성 | 픽션의 장면 목적·시점·갈등·정보 배치를 설계 | [scene-craft](https://github.com/danjdewhurst/story-skills/blob/main/skills/scene-craft/SKILL.md) |
| C21 서사 아이디어 검증 | 착상을 로그라인·갈등·반논제로 구체화해 이야기 가능성 검토 | [premise-workshop](https://github.com/danjdewhurst/story-skills/blob/main/skills/premise-workshop/SKILL.md) |
| C22 인문 논증·해석 글쓰기 | 정교한 개념 구분과 저자 해석을 보존하는 비판적 작문 | [humanities-writing-companion](https://github.com/tizzy916/humanities-writing-companion/blob/main/SKILL.md) |
| C23 설득형 제품 카피 | 독자의 의사결정과 전환 행동을 목표로 카피 구성 | [copywriting](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copywriting/SKILL.md) |
| C24 과학적 글쓰기·주장 검증 | 연구 주장·실증 근거·인용의 경계를 유지하며 논문 작성 | [scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) |


## 4. 결과 해석

- **레포 인기도≠스킬 품질.** 리포지토리 별점은 해당 개별 스킬의 실사용 평점이 아님.
- **원본 경로≠원본 내용.** 유사/복제 가능성이 있는 K-Dense-AI와 KalarisLabs 같은 묶음은 `SKILL.md` 내용 해시 비교 전까지 서로 다른 역량으로 간주하지 않음.
- **런타임 의존성.** `technical-writing` 사전 로드, story CLI/프로젝트, 브라우저, 네트워크, API 인증 등은 배포 검증의 핵심.
- **프롬프트 생성과 프롬프트 실행을 분리.** Writing Maestro가 리서치 요청문을 만들 때 외부 리서치 스킬의 실제 검색을 자동 개시해서는 안 됨.
- **언어 적합성.** 영어 중심 문장 규칙은 한국어 정책문서에 적용 가능하지 않을 수 있음.
- **미해결.** 405개 전문을 읽고 비교하지 않았으므로 선정안은 검증 완료가 아님. 본문 비교가 남은 후보는 28개 선정안에 도전할 수 있음.

## 5. 다음 검증

같은 클러스터 경쟁 후보를 최소 두 개씩 본문 비교(인풋/아웃풋/금지/토큰/의존/라이선스/실행 가능성), 한국어 사례로 적합성 검증, 동일 과업 단일/복수/무스킬 비교. 이후 각 클러스터 0~2개 채택하고 중복 제거.

## 6. 추가 탐색에 도움 된 커뮤니티·디렉터리

- [Writing skills 116개 분류 인덱스](https://skilltrove.dev/categories/writing) — 발견용, 독립 품질 인증 아님
- [2026 Reddit humanizer 비교 토론](https://www.reddit.com/r/claudeskills/comments/1vhuq5t/i_dug_through_8_opensource_ai_humanizers_heres/) — 주장과 실증 근거 분리 필요
- [2026 Reddit 글쓰기 스킬 토론](https://www.reddit.com/r/claudeskills/comments/1wpbkmy/a_free_claude_skill_to_deai_your_written_content/) — 인기도 신호만 취급
- [neverbiasu 연구 스킬 큐레이션](https://github.com/neverbiasu/awesome-research-skills) — 경로·라이선스·환경 의존 비교 신호
- [story-skills 상세 라우팅 문서](https://github.com/danjdewhurst/story-skills/blob/main/docs/skills.md) — 명확한 not-for 경계
- [writing-skills 라우터](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/writing/SKILL.md) — 단일 primary 선택과 점진 로드

전체 후보/마이크로 군집/잠정 대표 28개: CSV·JSON·XLSX 참조.

## 7. 직접 비교가 남은 인접 경쟁 후보

이 후보들은 동일 클러스터의 차순위가 아니라 **유사도 신호에 의해 확인이 필요한 후보**이며, 아직 우열을 실험으로 판정하지 않았다.

| 기능 묶음 | 검토할 인접 후보 | 원본 |
|---|---|---|
| C01 | prompt-optimizer | [SKILL.md](https://github.com/github/awesome-copilot/blob/main/skills/prompt-optimizer/SKILL.md) |
| C01 | prompt-engineering-patterns | [SKILL.md](https://github.com/wshobson/agents/blob/main/plugins/llm-application-dev/skills/prompt-engineering-patterns/SKILL.md) |
| C02 | boost-prompt | [SKILL.md](https://github.com/github/awesome-copilot/blob/main/skills/boost-prompt/SKILL.md) |
| C02 | prompt-optimizer | [SKILL.md](https://github.com/github/awesome-copilot/blob/main/skills/prompt-optimizer/SKILL.md) |
| C03 | interview-me | [SKILL.md](https://github.com/addyosmani/agent-skills/blob/main/skills/interview-me/SKILL.md) |
| C03 | grill-me | [SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) |
| C04 | writing-project-constitution | [SKILL.md](https://github.com/mazrean/agent-skills/blob/main/skills/writing-project-constitution/SKILL.md) |
| C04 | context-engineering | [SKILL.md](https://github.com/addyosmani/agent-skills/blob/main/skills/context-engineering/SKILL.md) |
| C05 | claude-md-improver | [SKILL.md](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/skills/claude-md-improver/SKILL.md) |
| C06 | doc-coauthoring | [SKILL.md](https://github.com/getsentry/skills/blob/main/skills/doc-coauthoring/SKILL.md) |
| C06 | writing-and-editing | [SKILL.md](https://github.com/matt-riley/agent-skills/blob/main/skills/writing-and-editing/SKILL.md) |
| C07 | writing-feature-spec | [SKILL.md](https://github.com/mazrean/agent-skills/blob/main/skills/writing-feature-spec/SKILL.md) |
| C07 | to-spec | [SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md) |
| C08 | documentation-and-adrs | [SKILL.md](https://github.com/addyosmani/agent-skills/blob/main/skills/documentation-and-adrs/SKILL.md) |
| C09 | architecture-decision-records | [SKILL.md](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/skills/architecture-decision-records/SKILL.md) |
| C09 | create-architectural-decision-record | [SKILL.md](https://github.com/github/awesome-copilot/blob/main/skills/create-architectural-decision-record/SKILL.md) |
| C10 | incident-runbook-templates | [SKILL.md](https://github.com/wshobson/agents/blob/main/plugins/incident-response/skills/incident-runbook-templates/SKILL.md) |
| C11 | awesome-code-docs | [SKILL.md](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-code-docs/SKILL.md) |
| C12 | source-driven-development | [SKILL.md](https://github.com/addyosmani/agent-skills/blob/main/skills/source-driven-development/SKILL.md) |
| C13 | awesome-grammar-check | [SKILL.md](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-grammar-check/SKILL.md) |
| C14 | requesting-code-review | [SKILL.md](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md) |
| C15 | systematic-review-prisma | [SKILL.md](https://github.com/KalarisLabs/research-agent-skills/blob/main/skills/systematic-review-prisma/SKILL.md) |
| C15 | literature-review | [SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md) |
| C16 | citation-management | [SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/citation-management/SKILL.md) |
| C17 | writing-clearly-and-concisely | [SKILL.md](https://github.com/softaworks/agent-toolkit/blob/main/skills/writing-clearly-and-concisely/SKILL.md) |
| C17 | prose-naturalizer | [SKILL.md](https://github.com/anayy09/claude-research-skills/blob/main/skills/prose-naturalizer/SKILL.md) |
| C18 | awesome-style-mimic | [SKILL.md](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-style-mimic/SKILL.md) |
| C19 | writing-cadence | [SKILL.md](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/writing-cadence/SKILL.md) |
| C20 | chapter-writing | [SKILL.md](https://github.com/danjdewhurst/story-skills/blob/main/skills/chapter-writing/SKILL.md) |
| C21 | theme-craft | [SKILL.md](https://github.com/danjdewhurst/story-skills/blob/main/skills/theme-craft/SKILL.md) |
| C22 | Academic-Writing | [SKILL.md](https://github.com/YuanZHAO321/Academic-Writing/blob/main/SKILL.md) |
| C22 | academic_writer | [SKILL.md](https://github.com/nqmn/academic_writer/blob/main/SKILL.md) |
| C23 | awesome-copywriting | [SKILL.md](https://github.com/khasky/awesome-agent-skills/blob/main/skills/awesome-copywriting/SKILL.md) |
| C24 | scientific-writing | [SKILL.md](https://github.com/KalarisLabs/research-agent-skills/blob/main/skills/scientific-writing/SKILL.md) |
| C24 | paper-writing | [SKILL.md](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/paper-writing/SKILL.md) |
