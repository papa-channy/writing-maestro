# Writing Maestro: external skill discovery — 2026-10-28

**Status:** 조사 후보 목록. 레포에 미등록. 다운로드·설치·정량 효과 검증 없음.

## 조사 기준

- 후보는 GitHub 저장소에서 실제 `SKILL.md` 경로를 확인한 스킬이며, 단순 리포지토리 수나 가상의 기능명이 아니다.
- `body_excerpt_reviewed`는 해당 스킬의 frontmatter·핵심 규칙 일부·목차를 직접 확인한 사례이다. 전체 심사나 테스트 완료를 뜻하지 않는다. `path_verified_only`는 구현 품질을 평가하지 않았다.
- `CORE`, `DEPENDENCY`, `CONDITIONAL`은 레지스트리 등록 **제안**이며, 실증된 품질 등급이 아니다.
- `DEPENDENCY`는 다른 스킬이 요구하는 상위 규칙 스킬이므로 명시적으로 함께 다뤄야 한다.
- 임의의 글쓰기 요청마다 레지스트리 전부 로딩하지 않는다. 문서 정책 정본 > 외부 스킬 규칙.

## 조사 규모

- SKILL.md 경로 확인: **159개**
- 서로 다른 소유 저장소: **14개**
- 1차 등록안: **28개** (핵심 15 / 의존 1 / 조건부 12)

## 카테고리

| 구획 | 수 |
|---|---:|
| document_authoring | 49 |
| evidence_review | 24 |
| prompt_engineering | 21 |
| communication | 21 |
| research_evidence | 15 |
| agent_context | 10 |
| task_planning | 7 |
| skill_authoring | 5 |
| writing_quality | 4 |
| decision_records | 3 |

## 우선 등록안 (미적용)

| 구분 | 스킬 | 적용 가치 | 핵심 제약 |
|---|---|---|---|
| CORE | [agent-md-refactor](https://github.com/softaworks/agent-toolkit/blob/main/skills/agent-md-refactor/SKILL.md) | 길어진 CLAUDE.md·AGENTS.md 구조 분리 | 파일 변경 전 승인/기존 링크 보호 |
| CORE | [context-engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/context-engineering/SKILL.md) | 문서의 적정 컨텍스트·라우팅·정보 계층 | 코딩 에이전트 중심 구조를 범용 규칙으로 오해 금지 |
| CORE | [writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md) | 에이전트가 읽는 정책·지시문의 검색·실행 구조 | 적용 전 사용자 프로젝트 문서 정본 확인 |
| CORE | [recording-decisions](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/recording-decisions/SKILL.md) | 확정된 결정과 논의 중 제안 구분 | technical-writing 의존 |
| CORE | [doc-coauthoring](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md) | 대형 문서 협업: 컨텍스트 수집→초안→독자 테스트 | 첫 단계 인터뷰가 과도해질 수 있음 |
| CORE | [documentation-and-adrs](https://github.com/addyosmani/agent-skills/blob/main/skills/documentation-and-adrs/SKILL.md) | ADR 및 설계 근거·대안·결과 기록 | 기존 ADR 관례 우선 |
| CORE | [documentation-writer](https://github.com/github/awesome-copilot/blob/main/skills/documentation-writer/SKILL.md) | 독자 목적별 Diátaxis 문서 유형 분리 | 정책·ADR을 무조건 Diátaxis에 끼워 넣지 않기 |
| CORE | [requirements-clarity](https://github.com/softaworks/agent-toolkit/blob/main/skills/requirements-clarity/SKILL.md) | 모호한 요구를 구체적인 질문과 수용조건으로 변환 | 질문 반복/점수화의 타당성 추가 검토 |
| CORE | [writing-design-docs](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-design-docs/SKILL.md) | 제안·RFC·설계 논증 문서 구성 | technical-writing 의존 |
| CORE | [build-evidence-map](https://github.com/github/awesome-copilot/blob/main/skills/build-evidence-map/SKILL.md) | 찬반·한정·미확인 근거를 분해한 논거 지도 | 출처 없는 claim을 근거로 승격하지 않기 |
| CORE | [reviewing-technical-prose](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/reviewing-technical-prose/SKILL.md) | 문서 결함 중심의 근거있는 리뷰 | technical-writing 의존; 하우스 스타일 과적용 금지 |
| CORE | [scientific-critical-thinking](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-critical-thinking/SKILL.md) | 주장·근거·연구 설계의 비판적 타당성 검토 | 범용 정책문서에 통계 규범 무분별 적용 금지 |
| CORE | [brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) | 구조화된 논의와 선택지 탐색 | 사용자가 이미 결정한 부분 재개방 금지 |
| CORE | [prompt-optimizer](https://github.com/github/awesome-copilot/blob/main/skills/prompt-optimizer/SKILL.md) | 검수·논의·리서치 요청용 프롬프트 개선 | 일회성 채팅용; 템플릿 변수 금지 강제는 충돌 |
| CORE | [writing-clearly-and-concisely](https://github.com/softaworks/agent-toolkit/blob/main/skills/writing-clearly-and-concisely/SKILL.md) | 문장의 명료성·중복 개선 | 영문 중심 규범을 한국어에 직수입 금지 |
| DEPENDENCY | [technical-writing](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/technical-writing/SKILL.md) | 기술문서 묶음의 상위 진실성·문체 규칙 | 규칙 강제력 및 사용자 하우스 스타일 충돌 검토 |
| CONDITIONAL | [claude-md-improver](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/skills/claude-md-improver/SKILL.md) | CLAUDE.md 결함 진단과 국소 개선 | Claude 전용, 수정 전 승인 게이트 |
| CONDITIONAL | [crafting-effective-readmes](https://github.com/softaworks/agent-toolkit/blob/main/skills/crafting-effective-readmes/SKILL.md) | 프로젝트 상황에 맞춘 README 구성 | 프로젝트 정책 정본과 중복 금지 |
| CONDITIONAL | [create-specification](https://github.com/github/awesome-copilot/blob/main/skills/create-specification/SKILL.md) | 기계 소비용 요구사항·인터페이스·수용조건 작성 | 고정 경로/템플릿을 프로젝트 설정으로 오버라이드 |
| CONDITIONAL | [writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) | 명세에서 실행 가능한 작업계획 작성 | 소프트웨어 구현 계획 특화; 일반 글쓰기에 남용 금지 |
| CONDITIONAL | [writing-runbooks](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-runbooks/SKILL.md) | 절차·중단·롤백·확인조건 명시 | technical-writing 의존; 운영 절차에만 |
| CONDITIONAL | [docs-sync-audit](https://github.com/github/awesome-copilot/blob/main/skills/docs-sync-audit/SKILL.md) | 문서-코드 변경 불일치 점검 | 아직 본문 정밀 검토 전 |
| CONDITIONAL | [doubt-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/doubt-driven-development/SKILL.md) | 고위험 결정의 반증 중심 검수 | 독립 모델 호출 비용과 과도한 리뷰 가능성 |
| CONDITIONAL | [peer-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/peer-review/SKILL.md) | 학술 원고·제안서의 정교한 심사 | 기밀·AI 심사 승인 필요, 일반 검수와 분리 |
| CONDITIONAL | [prompt-engineering-patterns](https://github.com/wshobson/agents/blob/main/plugins/llm-application-dev/skills/prompt-engineering-patterns/SKILL.md) | 재사용 프롬프트 템플릿·구조화 출력·few-shot 설계 | 운영 LLM API용 패턴 중심; 장황한 추론 강요 주의 |
| CONDITIONAL | [citation-management](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/citation-management/SKILL.md) | 인용 서지 검증·참고문헌 처리 | 네트워크/API 의존, 비학술 문서에는 보류 |
| CONDITIONAL | [literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md) | 재현 가능한 학술 문헌 조사·합성 | 학술 영역 특화, 추가 도구·네트워크 요구 |
| CONDITIONAL | [research-lookup](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/research-lookup/SKILL.md) | 다수 근거 수집과 claim-source 대응 | Parallel API 의존, 연구 수행용이지 요청문 작성용 아님 |

## 후보 전체 목록

| ID | 스킬 | 범주 | 초기 적합도 | 확인 수준 |
|---|---|---|---|---|
| WM-C001 | [doc-coauthoring](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C002 | [internal-comms](https://github.com/anthropics/skills/blob/main/skills/internal-comms/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C003 | [docx](https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C004 | [pdf](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C005 | [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | skill_authoring | medium | path_verified_only |
| WM-C006 | [claude-md-improver](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/skills/claude-md-improver/SKILL.md) | agent_context | high | body_excerpt_reviewed |
| WM-C007 | [writing-rules](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/hookify/skills/writing-rules/SKILL.md) | agent_context | medium | path_verified_only |
| WM-C008 | [skill-development](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md) | skill_authoring | medium | path_verified_only |
| WM-C009 | [boost-prompt](https://github.com/github/awesome-copilot/blob/main/skills/boost-prompt/SKILL.md) | prompt_engineering | high | body_excerpt_reviewed |
| WM-C010 | [prompt-optimizer](https://github.com/github/awesome-copilot/blob/main/skills/prompt-optimizer/SKILL.md) | prompt_engineering | high | body_excerpt_reviewed |
| WM-C011 | [finalize-agent-prompt](https://github.com/github/awesome-copilot/blob/main/skills/finalize-agent-prompt/SKILL.md) | prompt_engineering | high | path_verified_only |
| WM-C012 | [tldr-prompt](https://github.com/github/awesome-copilot/blob/main/skills/tldr-prompt/SKILL.md) | prompt_engineering | high | path_verified_only |
| WM-C013 | [ai-prompt-engineering-safety-review](https://github.com/github/awesome-copilot/blob/main/skills/ai-prompt-engineering-safety-review/SKILL.md) | prompt_engineering | high | path_verified_only |
| WM-C014 | [build-evidence-map](https://github.com/github/awesome-copilot/blob/main/skills/build-evidence-map/SKILL.md) | evidence_review | high | body_excerpt_reviewed |
| WM-C015 | [audit-integrity](https://github.com/github/awesome-copilot/blob/main/skills/audit-integrity/SKILL.md) | evidence_review | high | path_verified_only |
| WM-C016 | [docs-sync-audit](https://github.com/github/awesome-copilot/blob/main/skills/docs-sync-audit/SKILL.md) | evidence_review | high | body_excerpt_reviewed |
| WM-C017 | [code-review](https://github.com/github/awesome-copilot/blob/main/skills/code-review/SKILL.md) | evidence_review | high | path_verified_only |
| WM-C018 | [security-review](https://github.com/github/awesome-copilot/blob/main/skills/security-review/SKILL.md) | evidence_review | high | path_verified_only |
| WM-C019 | [test-gap-audit](https://github.com/github/awesome-copilot/blob/main/skills/test-gap-audit/SKILL.md) | evidence_review | high | path_verified_only |
| WM-C020 | [documentation-writer](https://github.com/github/awesome-copilot/blob/main/skills/documentation-writer/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C021 | [create-readme](https://github.com/github/awesome-copilot/blob/main/skills/create-readme/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C022 | [readme-blueprint-generator](https://github.com/github/awesome-copilot/blob/main/skills/readme-blueprint-generator/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C023 | [create-specification](https://github.com/github/awesome-copilot/blob/main/skills/create-specification/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C024 | [update-specification](https://github.com/github/awesome-copilot/blob/main/skills/update-specification/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C025 | [create-architectural-decision-record](https://github.com/github/awesome-copilot/blob/main/skills/create-architectural-decision-record/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C026 | [create-implementation-plan](https://github.com/github/awesome-copilot/blob/main/skills/create-implementation-plan/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C027 | [update-implementation-plan](https://github.com/github/awesome-copilot/blob/main/skills/update-implementation-plan/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C028 | [meeting-minutes](https://github.com/github/awesome-copilot/blob/main/skills/meeting-minutes/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C029 | [create-technical-spike](https://github.com/github/awesome-copilot/blob/main/skills/create-technical-spike/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C030 | [copilot-instructions-blueprint-generator](https://github.com/github/awesome-copilot/blob/main/skills/copilot-instructions-blueprint-generator/SKILL.md) | agent_context | high | path_verified_only |
| WM-C031 | [generate-custom-instructions-from-codebase](https://github.com/github/awesome-copilot/blob/main/skills/generate-custom-instructions-from-codebase/SKILL.md) | agent_context | high | path_verified_only |
| WM-C032 | [acquire-codebase-knowledge](https://github.com/github/awesome-copilot/blob/main/skills/acquire-codebase-knowledge/SKILL.md) | agent_context | high | path_verified_only |
| WM-C033 | [agent-governance](https://github.com/github/awesome-copilot/blob/main/skills/agent-governance/SKILL.md) | agent_context | high | path_verified_only |
| WM-C034 | [breakdown-feature-prd](https://github.com/github/awesome-copilot/blob/main/skills/breakdown-feature-prd/SKILL.md) | task_planning | medium | path_verified_only |
| WM-C035 | [breakdown-plan](https://github.com/github/awesome-copilot/blob/main/skills/breakdown-plan/SKILL.md) | task_planning | medium | path_verified_only |
| WM-C036 | [breakdown-epic-pm](https://github.com/github/awesome-copilot/blob/main/skills/breakdown-epic-pm/SKILL.md) | task_planning | medium | path_verified_only |
| WM-C037 | [project-workflow-analysis-blueprint-generator](https://github.com/github/awesome-copilot/blob/main/skills/project-workflow-analysis-blueprint-generator/SKILL.md) | task_planning | medium | path_verified_only |
| WM-C038 | [structured-autonomy-plan](https://github.com/github/awesome-copilot/blob/main/skills/structured-autonomy-plan/SKILL.md) | task_planning | medium | path_verified_only |
| WM-C039 | [prd](https://github.com/github/awesome-copilot/blob/main/skills/prd/SKILL.md) | task_planning | medium | path_verified_only |
| WM-C040 | [autoresearch](https://github.com/github/awesome-copilot/blob/main/skills/autoresearch/SKILL.md) | research_evidence | medium | path_verified_only |
| WM-C041 | [signal-write](https://github.com/github/awesome-copilot/blob/main/skills/signal-write/SKILL.md) | communication | medium | path_verified_only |
| WM-C042 | [technical-writing](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/technical-writing/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C043 | [writing-design-docs](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-design-docs/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C044 | [writing-runbooks](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-runbooks/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C045 | [documenting-contracts](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/documenting-contracts/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C046 | [documenting-legacy-codebases](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/documenting-legacy-codebases/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C047 | [writing-issues](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-issues/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C048 | [writing-changelogs](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-changelogs/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C049 | [writing-postmortems](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/writing-postmortems/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C050 | [reviewing-technical-prose](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/reviewing-technical-prose/SKILL.md) | evidence_review | high | body_excerpt_reviewed |
| WM-C051 | [recording-decisions](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/recording-decisions/SKILL.md) | decision_records | high | body_excerpt_reviewed |
| WM-C052 | [diagramming-processes](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/diagramming-processes/SKILL.md) | communication | medium | path_verified_only |
| WM-C053 | [writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md) | agent_context | high | body_excerpt_reviewed |
| WM-C054 | [grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) | prompt_engineering | high | path_verified_only |
| WM-C055 | [grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) | prompt_engineering | high | path_verified_only |
| WM-C056 | [to-questionnaire](https://github.com/mattpocock/skills/blob/main/skills/productivity/to-questionnaire/SKILL.md) | prompt_engineering | high | path_verified_only |
| WM-C057 | [wait-what](https://github.com/mattpocock/skills/blob/main/skills/productivity/wait-what/SKILL.md) | prompt_engineering | high | path_verified_only |
| WM-C058 | [handoff](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md) | communication | medium | path_verified_only |
| WM-C059 | [teach](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md) | communication | medium | path_verified_only |
| WM-C060 | [to-spec](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C061 | [to-tickets](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C062 | [grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) | prompt_engineering | high | body_excerpt_reviewed |
| WM-C063 | [research](https://github.com/mattpocock/skills/blob/main/skills/engineering/research/SKILL.md) | research_evidence | high | body_excerpt_reviewed |
| WM-C064 | [code-review](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C065 | [retro](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C066 | [writing-beats](https://github.com/mattpocock/skills/blob/main/skills/in-progress/writing-beats/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C067 | [writing-fragments](https://github.com/mattpocock/skills/blob/main/skills/in-progress/writing-fragments/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C068 | [writing-shape](https://github.com/mattpocock/skills/blob/main/skills/in-progress/writing-shape/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C069 | [claude-handoff](https://github.com/mattpocock/skills/blob/main/skills/in-progress/claude-handoff/SKILL.md) | communication | medium | path_verified_only |
| WM-C070 | [agent-md-refactor](https://github.com/softaworks/agent-toolkit/blob/main/skills/agent-md-refactor/SKILL.md) | agent_context | high | body_excerpt_reviewed |
| WM-C071 | [session-handoff](https://github.com/softaworks/agent-toolkit/blob/main/skills/session-handoff/SKILL.md) | agent_context | high | path_verified_only |
| WM-C072 | [crafting-effective-readmes](https://github.com/softaworks/agent-toolkit/blob/main/skills/crafting-effective-readmes/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C073 | [requirements-clarity](https://github.com/softaworks/agent-toolkit/blob/main/skills/requirements-clarity/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C074 | [backend-to-frontend-handoff-docs](https://github.com/softaworks/agent-toolkit/blob/main/skills/backend-to-frontend-handoff-docs/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C075 | [frontend-to-backend-requirements](https://github.com/softaworks/agent-toolkit/blob/main/skills/frontend-to-backend-requirements/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C076 | [writing-clearly-and-concisely](https://github.com/softaworks/agent-toolkit/blob/main/skills/writing-clearly-and-concisely/SKILL.md) | writing_quality | high | body_excerpt_reviewed |
| WM-C077 | [humanizer](https://github.com/softaworks/agent-toolkit/blob/main/skills/humanizer/SKILL.md) | writing_quality | high | path_verified_only |
| WM-C078 | [skill-judge](https://github.com/softaworks/agent-toolkit/blob/main/skills/skill-judge/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C079 | [qa-test-planner](https://github.com/softaworks/agent-toolkit/blob/main/skills/qa-test-planner/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C080 | [reducing-entropy](https://github.com/softaworks/agent-toolkit/blob/main/skills/reducing-entropy/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C081 | [professional-communication](https://github.com/softaworks/agent-toolkit/blob/main/skills/professional-communication/SKILL.md) | communication | medium | path_verified_only |
| WM-C082 | [feedback-mastery](https://github.com/softaworks/agent-toolkit/blob/main/skills/feedback-mastery/SKILL.md) | communication | medium | path_verified_only |
| WM-C083 | [lesson-learned](https://github.com/softaworks/agent-toolkit/blob/main/skills/lesson-learned/SKILL.md) | communication | medium | path_verified_only |
| WM-C084 | [daily-meeting-update](https://github.com/softaworks/agent-toolkit/blob/main/skills/daily-meeting-update/SKILL.md) | communication | medium | path_verified_only |
| WM-C085 | [web-to-markdown](https://github.com/softaworks/agent-toolkit/blob/main/skills/web-to-markdown/SKILL.md) | research_evidence | medium | path_verified_only |
| WM-C086 | [c4-architecture](https://github.com/softaworks/agent-toolkit/blob/main/skills/c4-architecture/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C087 | [mermaid-diagrams](https://github.com/softaworks/agent-toolkit/blob/main/skills/mermaid-diagrams/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C088 | [context-engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/context-engineering/SKILL.md) | agent_context | high | body_excerpt_reviewed |
| WM-C089 | [documentation-and-adrs](https://github.com/addyosmani/agent-skills/blob/main/skills/documentation-and-adrs/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C090 | [spec-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/spec-driven-development/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C091 | [planning-and-task-breakdown](https://github.com/addyosmani/agent-skills/blob/main/skills/planning-and-task-breakdown/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C092 | [doubt-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/doubt-driven-development/SKILL.md) | evidence_review | high | body_excerpt_reviewed |
| WM-C093 | [source-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/source-driven-development/SKILL.md) | evidence_review | high | body_excerpt_reviewed |
| WM-C094 | [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) | evidence_review | high | path_verified_only |
| WM-C095 | [idea-refine](https://github.com/addyosmani/agent-skills/blob/main/skills/idea-refine/SKILL.md) | prompt_engineering | medium | path_verified_only |
| WM-C096 | [interview-me](https://github.com/addyosmani/agent-skills/blob/main/skills/interview-me/SKILL.md) | prompt_engineering | medium | path_verified_only |
| WM-C097 | [using-agent-skills](https://github.com/addyosmani/agent-skills/blob/main/skills/using-agent-skills/SKILL.md) | skill_authoring | medium | path_verified_only |
| WM-C098 | [constraint-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/constraint-driven-development/SKILL.md) | task_planning | medium | path_verified_only |
| WM-C099 | [brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) | prompt_engineering | high | body_excerpt_reviewed |
| WM-C100 | [writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) | document_authoring | high | body_excerpt_reviewed |
| WM-C101 | [verification-before-completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C102 | [requesting-code-review](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C103 | [receiving-code-review](https://github.com/obra/superpowers/blob/main/skills/receiving-code-review/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C104 | [writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) | skill_authoring | medium | path_verified_only |
| WM-C105 | [using-superpowers](https://github.com/obra/superpowers/blob/main/skills/using-superpowers/SKILL.md) | skill_authoring | medium | path_verified_only |
| WM-C106 | [research-lookup](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/research-lookup/SKILL.md) | research_evidence | high | body_excerpt_reviewed |
| WM-C107 | [literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md) | research_evidence | high | body_excerpt_reviewed |
| WM-C108 | [paper-lookup](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/paper-lookup/SKILL.md) | research_evidence | high | path_verified_only |
| WM-C109 | [paperclip](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/paperclip/SKILL.md) | research_evidence | high | path_verified_only |
| WM-C110 | [bgpt-paper-search](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/bgpt-paper-search/SKILL.md) | research_evidence | high | path_verified_only |
| WM-C111 | [exa-search](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/exa-search/SKILL.md) | research_evidence | high | path_verified_only |
| WM-C112 | [parallel-web](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/parallel-web/SKILL.md) | research_evidence | high | path_verified_only |
| WM-C113 | [citation-management](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/citation-management/SKILL.md) | research_evidence | high | body_excerpt_reviewed |
| WM-C114 | [pyzotero](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/pyzotero/SKILL.md) | research_evidence | high | path_verified_only |
| WM-C115 | [scientific-critical-thinking](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-critical-thinking/SKILL.md) | evidence_review | high | body_excerpt_reviewed |
| WM-C116 | [peer-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/peer-review/SKILL.md) | evidence_review | high | body_excerpt_reviewed |
| WM-C117 | [scholar-evaluation](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scholar-evaluation/SKILL.md) | evidence_review | high | path_verified_only |
| WM-C118 | [scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C119 | [research-grants](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/research-grants/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C120 | [market-research-reports](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/market-research-reports/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C121 | [markdown-mermaid-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/markdown-mermaid-writing/SKILL.md) | document_authoring | high | path_verified_only |
| WM-C122 | [scientific-brainstorming](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-brainstorming/SKILL.md) | prompt_engineering | medium | path_verified_only |
| WM-C123 | [hypothesis-generation](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/hypothesis-generation/SKILL.md) | prompt_engineering | medium | path_verified_only |
| WM-C124 | [experimental-design](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/experimental-design/SKILL.md) | prompt_engineering | medium | path_verified_only |
| WM-C125 | [what-if-oracle](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/what-if-oracle/SKILL.md) | prompt_engineering | medium | path_verified_only |
| WM-C126 | [consciousness-council](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/consciousness-council/SKILL.md) | prompt_engineering | medium | path_verified_only |
| WM-C127 | [markitdown](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/markitdown/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C128 | [copywriting](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copywriting/SKILL.md) | communication | medium | path_verified_only |
| WM-C129 | [copy-editing](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copy-editing/SKILL.md) | communication | medium | path_verified_only |
| WM-C130 | [content-strategy](https://github.com/coreyhaines31/marketingskills/blob/main/skills/content-strategy/SKILL.md) | communication | medium | path_verified_only |
| WM-C131 | [customer-research](https://github.com/coreyhaines31/marketingskills/blob/main/skills/customer-research/SKILL.md) | communication | medium | path_verified_only |
| WM-C132 | [product-marketing](https://github.com/coreyhaines31/marketingskills/blob/main/skills/product-marketing/SKILL.md) | communication | medium | path_verified_only |
| WM-C133 | [marketing-plan](https://github.com/coreyhaines31/marketingskills/blob/main/skills/marketing-plan/SKILL.md) | communication | medium | path_verified_only |
| WM-C134 | [public-relations](https://github.com/coreyhaines31/marketingskills/blob/main/skills/public-relations/SKILL.md) | communication | medium | path_verified_only |
| WM-C135 | [cold-email](https://github.com/coreyhaines31/marketingskills/blob/main/skills/cold-email/SKILL.md) | communication | medium | path_verified_only |
| WM-C136 | [avoid-ai-writing](https://github.com/wshobson/agents/blob/main/plugins/avoid-ai-writing/skills/avoid-ai-writing/SKILL.md) | writing_quality | high | path_verified_only |
| WM-C137 | [architecture-decision-records](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/skills/architecture-decision-records/SKILL.md) | decision_records | medium | path_verified_only |
| WM-C138 | [openapi-spec-generation](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/skills/openapi-spec-generation/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C139 | [grounded-vault](https://github.com/wshobson/agents/blob/main/plugins/documentation-standards/skills/grounded-vault/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C140 | [hads](https://github.com/wshobson/agents/blob/main/plugins/documentation-standards/skills/hads/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C141 | [multi-reviewer-patterns](https://github.com/wshobson/agents/blob/main/plugins/agent-teams/skills/multi-reviewer-patterns/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C142 | [prompt-engineering-patterns](https://github.com/wshobson/agents/blob/main/plugins/llm-application-dev/skills/prompt-engineering-patterns/SKILL.md) | prompt_engineering | high | body_excerpt_reviewed |
| WM-C143 | [data-storytelling](https://github.com/wshobson/agents/blob/main/plugins/business-analytics/skills/data-storytelling/SKILL.md) | communication | medium | path_verified_only |
| WM-C144 | [evaluation-methodology](https://github.com/wshobson/agents/blob/main/plugins/plugin-eval/skills/evaluation-methodology/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C145 | [incident-runbook-templates](https://github.com/wshobson/agents/blob/main/plugins/incident-response/skills/incident-runbook-templates/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C146 | [on-call-handoff-patterns](https://github.com/wshobson/agents/blob/main/plugins/incident-response/skills/on-call-handoff-patterns/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C147 | [postmortem-writing](https://github.com/wshobson/agents/blob/main/plugins/incident-response/skills/postmortem-writing/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C148 | [social-evidence-research](https://github.com/wshobson/agents/blob/main/plugins/content-marketing/skills/social-evidence-research/SKILL.md) | research_evidence | medium | path_verified_only |
| WM-C149 | [writing-guidelines](https://github.com/vercel-labs/agent-skills/blob/main/skills/writing-guidelines/SKILL.md) | writing_quality | high | path_verified_only |
| WM-C150 | [obsidian-markdown](https://github.com/kepano/obsidian-skills/blob/main/skills/obsidian-markdown/SKILL.md) | document_authoring | medium | path_verified_only |
| WM-C151 | [defuddle](https://github.com/kepano/obsidian-skills/blob/main/skills/defuddle/SKILL.md) | research_evidence | medium | path_verified_only |
| WM-C152 | [decision-logger](https://github.com/alirezarezvani/claude-skills/blob/main/c-level-advisor/skills/decision-logger/SKILL.md) | decision_records | medium | path_verified_only |
| WM-C153 | [internal-narrative](https://github.com/alirezarezvani/claude-skills/blob/main/c-level-advisor/skills/internal-narrative/SKILL.md) | communication | medium | path_verified_only |
| WM-C154 | [strategic-alignment](https://github.com/alirezarezvani/claude-skills/blob/main/c-level-advisor/skills/strategic-alignment/SKILL.md) | communication | medium | path_verified_only |
| WM-C155 | [competitive-intel](https://github.com/alirezarezvani/claude-skills/blob/main/c-level-advisor/skills/competitive-intel/SKILL.md) | communication | medium | path_verified_only |
| WM-C156 | [prd](https://github.com/alirezarezvani/claude-skills/blob/main/.gemini/skills/prd/SKILL.md) | prompt_engineering | medium | path_verified_only |
| WM-C157 | [persona](https://github.com/alirezarezvani/claude-skills/blob/main/.gemini/skills/persona/SKILL.md) | prompt_engineering | medium | path_verified_only |
| WM-C158 | [cs-engineer-grill](https://github.com/alirezarezvani/claude-skills/blob/main/.gemini/skills/cs-engineer-grill/SKILL.md) | evidence_review | medium | path_verified_only |
| WM-C159 | [cs-ux-researcher](https://github.com/alirezarezvani/claude-skills/blob/main/.gemini/skills/cs-ux-researcher/SKILL.md) | research_evidence | medium | path_verified_only |

## 증거 해석과 미해결 게이트

1. Reddit 추천은 사용자 보고이며 비교 실험이나 사용성 검증이 아니다. 설치 수·스타 수는 품질에 대한 직접 측정치가 아니다.
2. GitHub tree에 SKILL.md 경로가 있는 사실은 작성 품질·종속 도구·라이선스·실제 실행 가능성을 보장하지 않는다.
3. registry 1차 선정은 논리적 작업 적합성에 기초한 가설이다. 아직 baseline 대비 효과, 토큰 비용, 충돌률, 한국어 규칙 준수 측정을 하지 않았다.
4. 복수 스킬 간 충돌, Claude 전용 메타데이터/툴 지정, 상위 스킬 의존, 라이선스 및 업데이트 안정성을 다음에 검증해야 한다.
5. 문서 생성 프롬프트와 문서 생성 작업, 리서치 요청문 작성과 실제 리서치 실행은 별도 task intent로 분류한다.

## 조사 참고 출처

- 공식 스킬 샘플: https://github.com/anthropics/skills
- 공식 플러그인: https://github.com/anthropics/claude-plugins-official
- Copilot 커뮤니티: https://github.com/github/awesome-copilot
- 연구 스킬: https://github.com/K-Dense-AI/scientific-agent-skills
- 작업별 큐레이션: https://lazyskills.sh/skills/writing-docs
- 폭넓은 발견 색인: https://github.com/VoltAgent/awesome-agent-skills
- 학술 큐레이션: https://github.com/neverbiasu/awesome-research-skills
- Reddit community review: https://www.reddit.com/r/ClaudeAI/comments/1ok9v3d/i_tested_30_community_claude_skills_for_a_week/
- Reddit concern: https://www.reddit.com/r/ClaudeCode/comments/1x53emo/are_skills_really_that_useful_if_you_know_what/
- Reddit method comparison: https://www.reddit.com/r/ClaudeAI/comments/1xckkpr/are_superpowers_skills_and_sdd_still_worth_it_on/

**저장소 수정은 수행하지 않았다.**
