# Writing Maestro — 30~60개 유동 범위 기반 보완 검토 v3

> **잠정 연구 선정안.** 실행·품질 벤치마크·설치 또는 최종 레지스트리 승인이 아니다. 2026-10-29 검토.

## 결론

- 범위: **30~60개** (상한·하한을 채우기 위한 목표 배정은 하지 않음). 현재 **58개**는 근거 있는 추가로 도달한 수량일 뿐이다.
- v2의 50개는 기능·전제 점검 결과 즉시 제거해야 한다고 확인된 후보가 없어 유지했다. **8개 추가**: 서사 3, 논문 2, 소셜 대본 보조 2, 논거 구조화 1.
- 후보 **405개** 전수 배치·상태 기록 유지. 군집은 **58개 잠정 기능 인접군**. 기존 57개에서 독립적으로 기능하는 스토리 프로젝트 구축·관리군을 1개 분리했다.
- 각 스킬에 정원을 배분하지 않았다. 동일 이름은 무조건 합치지 않고, 다르게 수행하는 기능은 유지했다. 품질·커뮤니티 평판에 대해 검증되지 않은 수치를 만들지 않았다.

## 8개 추가 근거

| ID | 스킬 | 보완하는 역할 | 분류 |
|---|---|---|---|
| `WM-X0152` | [character-management](https://github.com/danjdewhurst/story-skills/blob/main/skills/character-management/SKILL.md) | 캐릭터 정보·관계·상태를 구조화하여 장면/챕터 작성에 제공 | 기존 후보의 전제/독립 기능 |
| `WM-X0158` | [line-editing](https://github.com/danjdewhurst/story-skills/blob/main/skills/line-editing/SKILL.md) | 초고 이후 소설의 문장·대화·목소리·교정 패스 | 기존 후보의 전제/독립 기능 |
| `WM-X0168` | [story-maintenance](https://github.com/danjdewhurst/story-skills/blob/main/skills/story-maintenance/SKILL.md) | 스토리 프로젝트의 인덱스·링크·연속성 및 검증 CLI | 기존 후보의 전제/독립 기능 |
| `WM-X0279` | [abstract-writing](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/abstract-writing/SKILL.md) | 학술 초록을 핵심 문제·근거·조건으로 압축·검수 | 기존 후보의 전제/독립 기능 |
| `WM-X0280` | [academic-voice](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/academic-voice/SKILL.md) | 학술 분야의 정확성과 저자 목소리를 유지하는 문체 | 기존 후보의 전제/독립 기능 |
| `WM-X0196` | [build-evidence-map](https://github.com/github/awesome-copilot/blob/main/skills/build-evidence-map/SKILL.md) | 주장·반론·한정·미확인의 관계를 출처와 함께 모델링 | 독립 기능 |
| `WM-X0354` | [hook-writer](https://github.com/social-media-skills/skills/blob/main/skills/hook-writer/SKILL.md) | 플랫폼·매체별 첫 문장·첫 3초 훅의 진실성/효과 검토 | 기존 후보의 전제/독립 기능 |
| `WM-X0369` | [voice-builder](https://github.com/social-media-skills/skills/blob/main/skills/voice-builder/SKILL.md) | 소셜 콘텐츠용 voice.md를 실제 글 샘플로 구축 | 기존 후보의 전제/독립 기능 |

## 1. 서사 프로젝트 의존 관계 검토

Story Skills의 `plot-structure`, `scene-craft`, `chapter-writing`은 프로젝트 `story.md`와 연동한다. 장면 작업은 캐릭터가 정의되어야 하고, 장/문장 집필 단계에서는 `line-editing`이 명시적 보조 패스다. 기계적 검증은 `story-maintenance`가 담당한다. 이들은 모두 서로 대체 가능한 글쓰기 스킬이 아니라 **상태·창작·검수**를 나누어 맡는다.

- `story-init`과 `character-management`: 프로젝트 및 인물 정보를 생성·관리
- `plot-structure`와 `scene-craft`: 구조·장면을 설계
- `chapter-writing`과 `line-editing`: 초안 작성·언어적 보정
- `story-maintenance`: 구조/링크/CLI 기반 검사 — 문학적 우열 판단과 다름

스토리 CLI는 실행해 보지 않았다. Node와 sibling `references/`·`scripts/` 파일을 함께 배포할 수 있는지 검증이 필요하다.

## 2. 학술 글쓰기 세부 계약

`paper-writing` 원문은 초록 전용 요청을 `abstract-writing`으로 보내고 본문 집필 전에 `academic-voice`를 읽으며 최종 원고 편집에 `general-writing`을 사용한다. 기존의 `scientific-writing`과는 증거 보존/보고규정 중심 역할이 다르다. 두 보조 스킬은 품질 우열 때문이 아니라 실제 지시된 워크플로와 명확히 분리된 산출 가치 때문에 추가했다.

## 3. 소셜 미디어 서브스킬 — 등록 후보와 준비 상태 구분

`short-form-video-script`는 `hook-writer`와 `voice-builder`를 먼저 활용하도록 지시한다. `hook-writer`는 여러 포맷의 첫 문장/첫 3초라는 독립 작업을 담당한다. `voice-builder`는 소셜 스킬이 기대하는 `voice.md`를 만들며, 기존 `awesome-content-voice`의 `voice/<name>.md`를 스키마 동일하다고 가정해서 대체하지 않는다.

**중요:** 세 스킬 모두 `brand-profile` 맥락을 전제하며, 현재 405개 목록 내에서 이를 확정적으로 제공하는 스킬이 식별되지 않았다. 따라서 이들은 **연동 조건부 후보**로만 볼 수 있고 독립 실행 가능하다고 표현해서는 안 된다. 콘텐츠 앵글 스킬과 공개되지 않은 서브스킬 요구도 추가 검증한다.

## 4. 고유 논거 보존

`build-evidence-map`은 단순 참/거짓 점검이나 문헌 합성과 달리 근거·반증·한정·미확인을 연결하는 `.doubt.json` 산출물을 만들고 Node 기반 검증기로 구조를 확인한다. 기존 `investigating-sources`, `evidence-synthesis`와 작업 단위가 달라 유지할 가치가 있다. 실행 검증이나 명시된 선택적 렌더러 설치는 진행하지 않았다.

## 5. 50개 기존 후보의 중복 검토

| 인접군 | 유사해 보이는 후보 | 당장 제거하지 않은 이유 |
|---|---|---|
| 프롬프트 | `write-agent-prompts` / 두 `prompt-optimizer` / `prompt-improving` | 에이전트용 방법 표현, 시스템 프롬프트 평가 반복, 채팅용 완성 프롬프트, 기존 인용 프롬프트 최소 수정이라는 계약 차이. 과거 33쌍 비교와 이번 원문 대조로 구별 가능 |
| 학술 연구 | `scientific-writing` / `paper-writing` | 보고기준·근거·저자 책임 중심 vs 본문 논증 구조·실제 문장 집필 중심 |
| 글쓰기 교정 | `general-writing` / `prose-naturalizer` / `academic-voice` | 범용 글 정제, AI식 표현 제거, 학술 장르의 논증적 문체로 역할이 다름 |
| 문헌 조사 | `investigating-sources` / `literature-review` / `evidence-synthesis` | 조사·인용 감사, 관련 연구 서술, PRISMA 등의 정형 합성 절차로 각각 다른 결과물 |
| 저자 문체 | `awesome-content-voice` / `voice-builder` | 파일 규약·후속 소비자 차이가 존재. 다만 기능 중복이 있어 통합이 실제로 가능한지 재검토 가능 |

## 명시적 미해결 게이트

1. **실행 준비됨 ≠ 레지스트리 후보.** 외부 스킬 자체는 설치하지 않았다. 특히 Story CLI, 브랜드 프로필, Node 검증기 등은 아직 통합 검증되지 않았다.
2. **후보 수는 목표가 아님.** 동등한 기능이 실증적으로 확인되면 58보다 적게, 누락된 필수 동반 스킬이 확인되면 60 범위 내에서 늘릴 수 있다.
3. **군집 58개도 정답이 아님.** 현재 인접군은 분석적으로 배치한 잠정 구조다. 추가 비교에서 병합·분리된다.
4. **외부 후기·안전성·한국어 작문 품질은 아직 별도 검증되지 않았다.** 최종 스킬 후보 중심의 얕고 실용적인 점검을 권한다.

## 전수 데이터

- `pruning_405_v3.json`: 405개 중 58개 후보, 가변 수량 정책, 군집 경계 조정, 의존 관계, 남은 장애
- `pruning_405_v3.csv`: 전체 405개 현재 결정 및 근거를 보는 표
- 이전 `pruning_405_v1.*` 및 `pruning_405_v2.*`는 수정 없이 보존

## 현재 58개 후보

| ID | 이름 | 기능 인접군 |
|---|---|---|
| `WM-X0017` | `research-grants` | 연구비 제안·그랜트 서술 |
| `WM-X0022` | `scientific-writing` | 논문·학술 원고 집필 |
| `WM-X0030` | `citation-verification` | 서지 관리·인용 검증 |
| `WM-X0044` | `rebuttal-and-response-to-reviewers` | 심사 의견 답변·학술 제출 편지 |
| `WM-X0059` | `context-engineering` | 에이전트 지시문·컨텍스트 작성 |
| `WM-X0062` | `idea-refine` | 의도 탐색·요구사항 명확화 |
| `WM-X0063` | `interview-me` | 의도 탐색·요구사항 명확화 |
| `WM-X0101` | `evidence-synthesis` | 문헌 검토·근거 합성 |
| `WM-X0102` | `investigating-sources` | 외부 학술·웹 근거 탐색 |
| `WM-X0105` | `prose-naturalizer` | AI식 표현 제거·자연스러움 개선 |
| `WM-X0106` | `research-ideation` | 연구·아이디어 발산과 실험 설계 |
| `WM-X0107` | `submission-reviewer` | 학술 비평·동료심사 |
| `WM-X0111` | `doc-coauthoring` | 문서 공동집필·범용 기술문서 |
| `WM-X0125` | `cold-email` | 콜드 아웃바운드·뉴스레터·메일 시퀀스 |
| `WM-X0129` | `content-strategy` | 콘텐츠 전략·캠페인·채널 운영 계획 |
| `WM-X0131` | `copywriting` | 판매 전환 카피·카피 교정 |
| `WM-X0151` | `chapter-writing` | 소설·시 창작 및 장면 집필 |
| `WM-X0152` | `character-management` | 서사 프로젝트 구축·인물·무결성 관리 |
| `WM-X0158` | `line-editing` | 서사 피드백·편집·연속성 관리 |
| `WM-X0159` | `plot-structure` | 소설 전제·주제·세계관·플롯 |
| `WM-X0160` | `premise-workshop` | 소설 전제·주제·세계관·플롯 |
| `WM-X0165` | `scene-craft` | 소설·시 창작 및 장면 집필 |
| `WM-X0167` | `story-init` | 서사 프로젝트 구축·인물·무결성 관리 |
| `WM-X0168` | `story-maintenance` | 서사 프로젝트 구축·인물·무결성 관리 |
| `WM-X0171` | `verse-craft` | 소설·시 창작 및 장면 집필 |
| `WM-X0181` | `prompt-optimizer` | 프롬프트 생성·최적화 |
| `WM-X0196` | `build-evidence-map` | 사실확인·근거 추적 |
| `WM-X0203` | `create-implementation-plan` | 계획·작업 분해·이슈 전환 |
| `WM-X0205` | `create-specification` | PRD·명세·사용자 스토리 |
| `WM-X0207` | `docs-sync-audit` | 문서 정합성·주장 검수 |
| `WM-X0216` | `prompt-optimizer` | 프롬프트 생성·최적화 |
| `WM-X0227` | `write-agent-prompts` | 프롬프트 생성·최적화 |
| `WM-X0242` | `awesome-content-repurpose` | 콘텐츠 재활용·리퍼포징 |
| `WM-X0243` | `awesome-content-voice` | 저자 문체·브랜드 보이스 |
| `WM-X0272` | `writing-for-agents` | 에이전트 지시문·컨텍스트 작성 |
| `WM-X0279` | `abstract-writing` | 논문·학술 원고 집필 |
| `WM-X0280` | `academic-voice` | 저자 문체·브랜드 보이스 |
| `WM-X0282` | `general-writing` | 범용 문장 교정·가독성 향상 |
| `WM-X0287` | `literature-review` | 문헌 검토·근거 합성 |
| `WM-X0288` | `non-autoregressive-writing-pass` | 원고 전역 구성·문장 리듬 |
| `WM-X0289` | `paper-writing` | 논문·학술 원고 집필 |
| `WM-X0291` | `prompt-improving` | 프롬프트 생성·최적화 |
| `WM-X0304` | `documenting-contracts` | API·계약·핸드오프 문서 |
| `WM-X0306` | `recording-decisions` | 확정된 아키텍처·의사결정 기록 |
| `WM-X0307` | `reviewing-technical-prose` | 문서 정합성·주장 검수 |
| `WM-X0308` | `technical-writing` | 문서 공동집필·범용 기술문서 |
| `WM-X0310` | `writing-design-docs` | 설계 제안·기술적 논증 |
| `WM-X0313` | `writing-runbooks` | 운영·사고 대응 실행 절차 |
| `WM-X0317` | `chatbot-conversation-design` | 독립 후보(인접 비교 미확정): chatbot-conversation-design |
| `WM-X0335` | `blog-post-writing` | 독립 후보(인접 비교 미확정): blog-post-writing |
| `WM-X0339` | `translation` | 번역·현지화 |
| `WM-X0354` | `hook-writer` | 소셜 플랫폼별 텍스트 포맷 |
| `WM-X0362` | `short-form-video-script` | 숏폼 동영상 대본·스토리보드 |
| `WM-X0369` | `voice-builder` | 저자 문체·브랜드 보이스 |
| `WM-X0371` | `agent-md-refactor` | 에이전트 지시문·컨텍스트 작성 |
| `WM-X0374` | `crafting-effective-readmes` | README·코드 설명·개발자 문서 |
| `WM-X0384` | `requirements-clarity` | 의도 탐색·요구사항 명확화 |
| `WM-X0394` | `data-storytelling` | 사업 분석·리포트·데이터 기반 이야기 |

