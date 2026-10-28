# Writing Maestro — 2차 경쟁 후보 비교·선정 수정 v2

> **잠정 결정.** 런타임 실행이나 405개 전문 교차 실험이 아니라, 405개 기능 프로필을 재검토한 뒤 실제 경쟁 후보의 원본 SKILL.md를 읽은 선택 수정이다. 원본 클러스터 57개는 고정 분류가 아니라 수정 가능한 기능 인접군이다.

## 결론

**50개 유지. 8개 교체, 42개 유지.** 405개 전체의 선정 여부는 `pruning_405_v2.csv`와 JSON에 남긴다. 1차 파일은 보존한다.

- 총군집 57개(기존 57개 임시 인접군 보존). 후보 있는 군집 35개. 신규 실증/커뮤니티 평판 확인 없음.
- 선정자 중 분석자 정규화 32개, 원문 기반 자동 정규화 18개. **새로 들어온 8개는 실제 SKILL.md 전문을 별도 열람**했다.
- 8개 교체는 기능 완성도의 우월함을 실증한 것이 아니라 **전체 50개의 기능 범위·전제 일관성을 개선하는 포트폴리오 판단**이다.

## 실제 교체 8건

| 신규 채택 | 기존 후보 제외 | 관찰된 유용성·교체 이유 | 명시적 손실/반론 |
|---|---|---|---|
| [`WM-X0308` technical-writing](https://github.com/riekelt/technical-writer/blob/main/plugins/technical-writer/skills/technical-writing/SKILL.md) | `WM-X0318` email-drafting | technical-writing이 riekelt 문서 유형 스킬의 필수 공통 베이스임을 원문에서 확인. 한국어 문서도 구조/근거 규칙 적용 명시. | 업무 이메일 전용 템플릿과 수신자별 톤 안내의 깊이는 줄어든다. |
| [`WM-X0102` investigating-sources](https://github.com/anayy09/claude-research-skills/blob/main/investigating-sources/SKILL.md) | `WM-X0252` awesome-style-mimic | 조사→출처 실재 확인→근거 종합→인용 감사가 일관된 워크플로. evidence-synthesis의 체계적 근거 검토와 달리 단일 조사 보고서·fact-check·출처 감사 등을 지원. | 외부 사이트의 보이스 크롤링과 일괄 스타일 모사 기능을 잃는다. |
| [`WM-X0106` research-ideation](https://github.com/anayy09/claude-research-skills/blob/main/research-ideation/SKILL.md) | `WM-X0293` writing-cadence | 기존 논문·데이터·코드를 인벤토리로 삼아 신규 연구 질문을 가설·신규성·출판 경로와 연결. 범용 idea-refine과 목표/제약이 다르다. | 문장 호흡/대조 문형을 정밀하게 분석하는 전문 패스가 빠진다. |
| [`WM-X0107` submission-reviewer](https://github.com/anayy09/claude-research-skills/blob/main/submission-reviewer/SKILL.md) | `WM-X0130` copy-editing | 논문/특허 초고에 대해 주장-근거, 독창성·재현성·준비도 관점의 심사와 우선 수정 과제를 제공. 본문 작성/리뷰어 답변과 분리된다. | Seven Sweeps 방식의 마케팅 카피 전문 편집 깊이가 줄어든다. |
| [`WM-X0335` blog-post-writing](https://github.com/seb1n/awesome-ai-agent-skills/blob/main/writing-and-content/blog-post-writing/SKILL.md) | `WM-X0345` carousel-writer | 자료 조사→형식 선택→아웃라인→장문 작성→SEO 편집의 독립적인 블로그 본문 산출 기능. content-strategy는 기획이고 copywriting은 전환 글 중심. | 슬라이드별 카피·캐러셀 구성 전용 워크플로를 잃는다. |
| [`WM-X0203` create-implementation-plan](https://github.com/github/awesome-copilot/blob/main/skills/create-implementation-plan/SKILL.md) | `WM-X0312` writing-postmortems | 상세 명세를 실행 가능한 단계/의존성/검증 기준이 있는 계획서로 변환. 기술 설계 제안서와 작업 명세의 다음 산출물을 명시한다. 고정 /plan/ 경로는 통합 위험. | 사고 시각표·기여 요인·불변 후속기록의 전용 서식/관리가 줄어든다. |
| [`WM-X0317` chatbot-conversation-design](https://github.com/seb1n/awesome-ai-agent-skills/blob/main/communication/chatbot-conversation-design/SKILL.md) | `WM-X0162` reader-panel | 의도·슬롯·대화 분기·다단계 오류 복구·컨텍스트 이월 등 대화형 시스템의 서술·대화 설계 전담. 에이전트 프롬프트 최적화와 다르다. | 소설 베타리더 관점의 가상 다중 피드백 워크플로를 잃는다. |
| [`WM-X0167` story-init](https://github.com/danjdewhurst/story-skills/blob/main/skills/story-init/SKILL.md) | `WM-X0173` worldbuilding | 선정된 plot-structure/scene-craft/chapter-writing의 story.md 프로젝트 생성 전제. 이야기 설정을 스키마·인덱스가 있는 프로젝트로 초기화한다. | 세부 세계관·지명·문화·설정 데이터베이스 전용 작업을 잃는다. |

## 추가 경쟁 후보: 유용하지만 이번 50개에서는 미선정

| 후보 | 직접 비교 결과 | 상태 |
|---|---|---|
| [`WM-X0330` fact-checking](https://github.com/seb1n/awesome-ai-agent-skills/blob/main/research-and-knowledge/fact-checking/SKILL.md) | 주장 원자화·교차검증·판정표 전문. 그러나 새로 채택한 investigating-sources가 `fact-check` 모드와 출처 실재 확인·인용 감사를 이미 제공하므로 추가 1석의 한계 가치가 작음 | RESERVE |
| [`WM-X0015` peer-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/peer-review/SKILL.md) | 기밀 원고 사전 승인과 로컬 검수 게이트를 갖춘 철저한 심사 초안. submission-reviewer는 제출 전 논문·특허의 독창성·준비도와 수정 우선순위에 더 직접적. 정식 익명 심사 환경에서는 0015가 더 적합할 수 있음 | RESERVE |
| [`WM-X0301` writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) | 작은 테스트/커밋 단위로 분해하는 코드 에이전트 계획. 0203은 정해진 문서 스키마·식별자·검증 조건 등 자동 처리형 계획에 집중. Superpowers 실행체계와 결합되면 0301 교체가 유리할 수 있음 | RESERVE |
| [`WM-X0196` build-evidence-map](https://github.com/github/awesome-copilot/blob/main/skills/build-evidence-map/SKILL.md) | 근거의 지지/반박/한정/미확인을 그래프형 `.doubt.json`으로 분리해 차별화. Node 검증기와 특수 스키마가 필수이고 현재 조사/근거 합성 계열이 일부 근접 | RESERVE |
| [`WM-X0395` social-evidence-research](https://github.com/wshobson/agents/blob/main/plugins/research/skills/social-evidence-research/SKILL.md) | 소셜 증언 수집 근거의 반복/범위 관리가 전문적이지만 이번에는 일반 조사·사실검증을 먼저 보완 | RESERVE |
| [`WM-X0345` carousel-writer](https://github.com/social-media-skills/skills/blob/main/skills/carousel-writer/SKILL.md) | 고유한 멀티슬라이드 산출을 가짐. 다만 브랜드 프로필·훅 등의 동반 스킬 의존 및 좁은 출력 매체로 후순위 | RESERVE |

## 특히 확인된 의존 관계

1. `technical-writing`은 riekelt 문서형 스킬의 공통 기반으로 원문에 명시된다. 이번에 레지스트리 후보로 추가했으나 해당 스킬들의 실행이 보장되는 것은 아니다.
2. `story-init`은 `plot-structure`, `scene-craft`, `chapter-writing`이 요구하는 `story.md` 프로젝트를 만드는 진입점이다. 다만 추가로 `character-management`, Story CLI, `line-editing` 등의 런타임 의존성이 남아 있다. 설치·의존성을 별도 게이트에서 확인해야 한다.
3. `investigating-sources`, `research-ideation`, `submission-reviewer`의 v1 원본 경로에는 `skills/` 접두사가 있었지만, 실제 저장소 파일은 각 이름의 **루트 디렉터리/SKILL.md**다. v2의 `resolved_source_path`와 URL에 수정된 경로를 별도로 남겼고 원본 기록은 보존했다.
4. `create-implementation-plan`은 `/plan/` 폴더와 고정 식별자·구조를 강하게 요구한다. 소비 프로젝트의 스펙·경로 규약과 충돌하면 대체 또는 제외를 재검토한다.

## 평가 범위와 결정 경계

- **군집 숫자는 결과를 증명하지 않는다.** v1 57개는 기능적 설명을 사람이 인접군에 배치한 결과이고, 자동으로 최적 군집을 학습한 결론이 아니다.
- 405개 정규화·선별 기록을 다시 전수 대조했으나, 미선정 355개 각자의 실행·외부 평판·허가·한국어 품질을 일일이 검사하지는 않았다. 원본 직접 열람은 경쟁 우선 후보에 집중했다.
- 한 기능에서 대체성이 낮으면 복수 후보를 남긴다. 단독 기능이라는 이유만으로 자동 등록하지 않으며, 복수 후보를 남기는 데 군집 정원도 사용하지 않는다.
- 등록 확정 이전에는 원본 라이선스, 설치·환경 호환, 권한, 의존성, 한국어 작문 적합성을 핵심 후보에 한해 확인한다.

## 현행 50개 명단

| ID | 스킬 | 기능 인접군 |
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
| `WM-X0159` | `plot-structure` | 소설 전제·주제·세계관·플롯 |
| `WM-X0160` | `premise-workshop` | 소설 전제·주제·세계관·플롯 |
| `WM-X0165` | `scene-craft` | 소설·시 창작 및 장면 집필 |
| `WM-X0167` | `story-init` | 소설·시 창작 및 장면 집필 |
| `WM-X0171` | `verse-craft` | 소설·시 창작 및 장면 집필 |
| `WM-X0181` | `prompt-optimizer` | 프롬프트 생성·최적화 |
| `WM-X0203` | `create-implementation-plan` | 계획·작업 분해·이슈 전환 |
| `WM-X0205` | `create-specification` | PRD·명세·사용자 스토리 |
| `WM-X0207` | `docs-sync-audit` | 문서 정합성·주장 검수 |
| `WM-X0216` | `prompt-optimizer` | 프롬프트 생성·최적화 |
| `WM-X0227` | `write-agent-prompts` | 프롬프트 생성·최적화 |
| `WM-X0242` | `awesome-content-repurpose` | 콘텐츠 재활용·리퍼포징 |
| `WM-X0243` | `awesome-content-voice` | 저자 문체·브랜드 보이스 |
| `WM-X0272` | `writing-for-agents` | 에이전트 지시문·컨텍스트 작성 |
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
| `WM-X0362` | `short-form-video-script` | 숏폼 동영상 대본·스토리보드 |
| `WM-X0371` | `agent-md-refactor` | 에이전트 지시문·컨텍스트 작성 |
| `WM-X0374` | `crafting-effective-readmes` | README·코드 설명·개발자 문서 |
| `WM-X0384` | `requirements-clarity` | 의도 탐색·요구사항 명확화 |
| `WM-X0394` | `data-storytelling` | 사업 분석·리포트·데이터 기반 이야기 |

## 데이터

- `pruning_405_v2.json`: 전수 405 후보, 최신 50, 8개 비교 결과, 참조 경로 보정
- `pruning_405_v2.csv`: Excel 호환 전수 기록
- 1차 `pruning_405_v1.*` 변경 없음

