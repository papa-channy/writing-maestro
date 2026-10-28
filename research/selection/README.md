# Writing Maestro — 405개 기능 군집 기반 50개 1차 압축

> **잠정 연구 결과.** 레지스트리 승인, 외부 스킬 설치, 실증 평가, 외부 후기 검증이 아니다. 2026-10-28의 원본 스냅샷을 기준으로 한다.

## 결과

- 전체: **405개** / 레지스트리 후보 **50개** / 미선정 **355개**
- 잠정 기능 인접군: **57개** (복수 후보군 49개, 비교 근거 부족·독립 역할 단독 후보 8개)
- 후보를 남긴 인접군 33개; 미선정 인접군 24개. 각 군집에 슬롯을 의무 할당하지 않는다.
- 선정 후보 정규화 근거: 분석자 해석 35개, 자동 원문 추출 15개.

## 선별 원리

1. 먼저 405개 출처의 목적·입력·절차·출력·경계를 보고 **기능 대체성 중심의 잠정 비교 인접군**으로 배치한다. 기존 24개 분류·28개 예비 명단은 군집 기준이나 보장된 선발권이 아니다.
2. 같은 목적·출력에 경쟁자가 많은 군집일수록 중복을 강하게 줄인다. 반면 장면 설계와 실제 집필, 문헌 합성과 서술 리뷰처럼 **작동 계약이 달라 보완적인 후보**는 같은 인접군에서도 복수로 선별한다.
3. 단독 군집은 자동 채택이 아니고, 대형 군집은 자동 증원도 아니다. 제한된 50개 슬롯에서 실제 활용성·기능 폭·원문에 명시된 절차 구체성·환경 의존을 고려한 **정성적 포트폴리오 판단**이다.
4. 이번 판은 외부 후기나 실사용 벤치마크를 직접 확인하지 않았다. 소스 기반 선별일 뿐 **개별 스킬의 품질 우위나 안전성이 실증됐다는 뜻은 아니다.**
5. 인접군은 고정 분류 체계가 아니다. 후속 검토에서 **병합·분리·독립 유지가 가능**하다. 원문 추출 수준의 305개는 특히 주의해야 한다.

## 후보 50개 — 소속 잠정 군집 및 선정 이유

| 군집 | 후보 | 왜 남겼나 |
|---|---|---|
| 연구비 제안·그랜트 서술 | `WM-X0017` `research-grants` | 연구비 제안서의 타당성·지원 논증 |
| 논문·학술 원고 집필 | `WM-X0022` `scientific-writing` | 학술 주장·출처·저자 책임의 경계 보존 |
| 서지 관리·인용 검증 | `WM-X0030` `citation-verification` | DOI·저자·서지 메타데이터 검증 |
| 심사 의견 답변·학술 제출 편지 | `WM-X0044` `rebuttal-and-response-to-reviewers` | 심사자 지적에 구조적으로 응답 |
| 에이전트 지시문·컨텍스트 작성 | `WM-X0059` `context-engineering` | 컨텍스트 정보의 계층화·적재 설계 |
| 의도 탐색·요구사항 명확화 | `WM-X0062` `idea-refine` | 아이디어 대안 발산·가정 압박·수렴 |
| 의도 탐색·요구사항 명확화 | `WM-X0063` `interview-me` | 잠재적 요구와 사용자 의도 인터뷰 |
| 문헌 검토·근거 합성 | `WM-X0101` `evidence-synthesis` | 프로토콜·편향·근거 확실성을 포함한 합성 |
| AI식 표현 제거·자연스러움 개선 | `WM-X0105` `prose-naturalizer` | AI식 관용 표현의 구체적 진단과 재작성 |
| 문서 공동집필·범용 기술문서 | `WM-X0111` `doc-coauthoring` | 맥락 수집에서 독자 테스트까지 공동 집필 |
| 콜드 아웃바운드·뉴스레터·메일 시퀀스 | `WM-X0125` `cold-email` | 회신 유도를 위한 B2B 콜드 메일 작성 |
| 콘텐츠 전략·캠페인·채널 운영 계획 | `WM-X0129` `content-strategy` | 콘텐츠 주제·독자·채널 전략 수립 |
| 판매 전환 카피·카피 교정 | `WM-X0130` `copy-editing` | 이미 작성한 마케팅 카피 진단·개정 |
| 판매 전환 카피·카피 교정 | `WM-X0131` `copywriting` | 랜딩/세일즈 페이지 전환 중심 카피 |
| 소설·시 창작 및 장면 집필 | `WM-X0151` `chapter-writing` | 장/장면의 실제 소설 산문 집필 |
| 소설 전제·주제·세계관·플롯 | `WM-X0159` `plot-structure` | 서사 전체의 플롯·전개 구조 설계 |
| 소설 전제·주제·세계관·플롯 | `WM-X0160` `premise-workshop` | 이야기 착상→전제·로그라인 검증 |
| 서사 피드백·편집·연속성 관리 | `WM-X0162` `reader-panel` | 독자 관점의 서사 이해·몰입 피드백 |
| 소설·시 창작 및 장면 집필 | `WM-X0165` `scene-craft` | 목적·갈등·시점별 장면 설계 |
| 소설·시 창작 및 장면 집필 | `WM-X0171` `verse-craft` | 시 창작의 독립 운율·이미지 작업 |
| 소설 전제·주제·세계관·플롯 | `WM-X0173` `worldbuilding` | 서사 세계의 설정·인과 일관성 구축 |
| 프롬프트 생성·최적화 | `WM-X0181` `prompt-optimizer` | 시스템·에이전트 프롬프트의 평가·반복 최적화 |
| PRD·명세·사용자 스토리 | `WM-X0205` `create-specification` | 요구를 구조적 명세 문서로 변환 |
| 문서 정합성·주장 검수 | `WM-X0207` `docs-sync-audit` | 코드·설정 대비 문서 변경 누락의 읽기 감사 |
| 프롬프트 생성·최적화 | `WM-X0216` `prompt-optimizer` | 플레이스홀더 없는 즉시 사용 채팅 프롬프트 |
| 프롬프트 생성·최적화 | `WM-X0227` `write-agent-prompts` | 에이전트가 수행할 판단·행동 구조를 고밀도 지시문으로 설계 |
| 콘텐츠 재활용·리퍼포징 | `WM-X0242` `awesome-content-repurpose` | 원본 콘텐츠에서 플랫폼별 파생 게시물 제작 |
| 저자 문체·브랜드 보이스 | `WM-X0243` `awesome-content-voice` | 저자 자신의 샘플 기반 재사용 문체 프로필 |
| 저자 문체·브랜드 보이스 | `WM-X0252` `awesome-style-mimic` | 외부 브랜드 글의 문체 특성 추출·적용 |
| 에이전트 지시문·컨텍스트 작성 | `WM-X0272` `writing-for-agents` | 에이전트가 소비하는 문서의 포인터·분기·완료 조건 |
| 범용 문장 교정·가독성 향상 | `WM-X0282` `general-writing` | 기본 산문의 자연스러운 가독성·의미 보존 |
| 문헌 검토·근거 합성 | `WM-X0287` `literature-review` | 문헌 동향·지식 계보 중심 서술적 리뷰 |
| 원고 전역 구성·문장 리듬 | `WM-X0288` `non-autoregressive-writing-pass` | 완성 원고 전체의 논증·전환 재검토 |
| 논문·학술 원고 집필 | `WM-X0289` `paper-writing` | 실제 연구 논문의 주장·섹션 집필 |
| 프롬프트 생성·최적화 | `WM-X0291` `prompt-improving` | 기존 프롬프트 의도 유지형 최소 개정 |
| 원고 전역 구성·문장 리듬 | `WM-X0293` `writing-cadence` | 문장 길이·반복 패턴·호흡 개선 |
| API·계약·핸드오프 문서 | `WM-X0304` `documenting-contracts` | HTTP API·메시지의 인터페이스 계약 문서화 |
| 확정된 아키텍처·의사결정 기록 | `WM-X0306` `recording-decisions` | 확정된 결정과 근거를 불변 기록으로 관리 |
| 문서 정합성·주장 검수 | `WM-X0307` `reviewing-technical-prose` | 기술 문장의 오류·근거·심각도 진단 |
| 설계 제안·기술적 논증 | `WM-X0310` `writing-design-docs` | 미확정 설계의 근거·비용·대안 논증 |
| 사고·작업 회고 | `WM-X0312` `writing-postmortems` | 사고 원인·영향·후속조치 중심 포스트모템 |
| 운영·사고 대응 실행 절차 | `WM-X0313` `writing-runbooks` | 검증상태·실행 단계·롤백을 갖춘 운영 절차 |
| 업무 메일·회의·조직 커뮤니케이션 | `WM-X0318` `email-drafting` | 업무 목적·수신자에 맞는 전문 이메일 초안 |
| 번역·현지화 | `WM-X0339` `translation` | 원문 의미와 용어를 보존하는 번역·현지화 |
| 소셜 플랫폼별 텍스트 포맷 | `WM-X0345` `carousel-writer` | 슬라이드형 소셜 캐러셀 원고 제작 |
| 숏폼 동영상 대본·스토리보드 | `WM-X0362` `short-form-video-script` | Reels/TikTok 공통 숏폼 대본 설계 |
| 에이전트 지시문·컨텍스트 작성 | `WM-X0371` `agent-md-refactor` | 과밀한 에이전트 안내 문서의 분리·재구획 |
| README·코드 설명·개발자 문서 | `WM-X0374` `crafting-effective-readmes` | README 구조와 독자 적합성에 특화 |
| 의도 탐색·요구사항 명확화 | `WM-X0384` `requirements-clarity` | 명세 전 요구사항 결손과 수용 기준 확정 |
| 사업 분석·리포트·데이터 기반 이야기 | `WM-X0394` `data-storytelling` | 데이터를 해석 가능한 이야기·시각적 논증으로 변환 |

## 군집 압축 결과(복수 후보 인접군)

| 인접군 | 전체 후보 | 선정 |
|---|---:|---|
| 사업 분석·리포트·데이터 기반 이야기 (`business-insights`) | 23 | WM-X0394 |
| 코드 검토·보안·시험 품질 (`code-review-operations`) | 20 | 0 |
| 마케팅 전환·고객 획득 전략 (`marketing-conversion`) | 18 | 0 |
| 계획·작업 분해·이슈 전환 (`planning-documents`) | 18 | 0 |
| 에이전트 지시문·컨텍스트 작성 (`agent-instructions`) | 15 | WM-X0059, WM-X0272, WM-X0371 |
| 지식 저장소·논문 코퍼스 활용 (`knowledge-work`) | 15 | 0 |
| 콘텐츠 전략·캠페인·채널 운영 계획 (`marketing-strategy`) | 15 | WM-X0129 |
| README·코드 설명·개발자 문서 (`repo-guides`) | 14 | WM-X0374 |
| 연구·아이디어 발산과 실험 설계 (`research-ideation`) | 14 | 0 |
| 논문·학술 원고 집필 (`research-writing`) | 13 | WM-X0022, WM-X0289 |
| 외부 학술·웹 근거 탐색 (`research-lookup`) | 12 | 0 |
| 소셜 플랫폼별 텍스트 포맷 (`social-text`) | 12 | WM-X0345 |
| PRD·명세·사용자 스토리 (`specification`) | 10 | WM-X0205 |
| 설계 제안·기술적 논증 (`design-rationale`) | 9 | WM-X0310 |
| 프롬프트 생성·최적화 (`prompt-production`) | 9 | WM-X0181, WM-X0216, WM-X0227, WM-X0291 |
| 업무 메일·회의·조직 커뮤니케이션 (`workplace-comms`) | 9 | WM-X0318 |
| 문서 공동집필·범용 기술문서 (`coauthoring`) | 8 | WM-X0111 |
| 문헌 검토·근거 합성 (`evidence-synthesis`) | 8 | WM-X0101, WM-X0287 |
| 서사 피드백·편집·연속성 관리 (`fiction-revision`) | 8 | WM-X0162 |
| 의도 탐색·요구사항 명확화 (`intent-elicitation`) | 8 | WM-X0062, WM-X0063, WM-X0384 |
| 검색 최적화·시장 경쟁·오디언스 연구 (`marketing-seo`) | 8 | 0 |
| 스킬 작성·평가·라우팅 (`skill-authoring`) | 8 | 0 |
| 소설·시 창작 및 장면 집필 (`fiction-drafting`) | 7 | WM-X0151, WM-X0165, WM-X0171 |
| 범용 문장 교정·가독성 향상 (`plain-writing`) | 7 | WM-X0282 |
| AI식 표현 제거·자연스러움 개선 (`ai-prose`) | 6 | WM-X0105 |
| 원본 자료를 Markdown 등으로 변환 (`document-conversion`) | 6 | 0 |
| 원고 전역 구성·문장 리듬 (`macro-revision`) | 6 | WM-X0288, WM-X0293 |
| 저자 문체·브랜드 보이스 (`voice-and-style`) | 6 | WM-X0243, WM-X0252 |
| 확정된 아키텍처·의사결정 기록 (`decision-records`) | 5 | WM-X0306 |
| Mermaid·프로세스 시각화 (`diagram-writing`) | 5 | 0 |
| 문서 정합성·주장 검수 (`document-audit`) | 5 | WM-X0207, WM-X0307 |
| 사실확인·근거 추적 (`fact-grounding`) | 5 | 0 |
| 소설 전제·주제·세계관·플롯 (`fiction-concept`) | 5 | WM-X0159, WM-X0160, WM-X0173 |
| 전문 도메인 문서·제안서 (`niche-document-domain`) | 5 | 0 |
| 사고·작업 회고 (`postmortem`) | 5 | WM-X0312 |
| 학술 비평·동료심사 (`research-peer-review`) | 5 | 0 |
| 판매 전환 카피·카피 교정 (`sales-copy`) | 5 | WM-X0130, WM-X0131 |
| 숏폼 동영상 대본·스토리보드 (`short-video-script`) | 5 | WM-X0362 |
| 요약·노트·세션 전달 (`summarization`) | 5 | 0 |
| API·계약·핸드오프 문서 (`api-contract-docs`) | 4 | WM-X0304 |
| 서지 관리·인용 검증 (`citation-workflow`) | 4 | WM-X0030 |
| 연구비 제안·그랜트 서술 (`research-grants`) | 4 | WM-X0017 |
| 변경 요약·릴리스 노트 (`changelog`) | 3 | 0 |
| 콜드 아웃바운드·뉴스레터·메일 시퀀스 (`marketing-email`) | 3 | WM-X0125 |
| 심사 의견 답변·학술 제출 편지 (`research-rebuttal`) | 3 | WM-X0044 |
| 운영·사고 대응 실행 절차 (`runbook`) | 3 | WM-X0313 |
| 콘텐츠 재활용·리퍼포징 (`content-repurposing`) | 2 | WM-X0242 |
| 창작물 출판·제출 (`fiction-publishing`) | 2 | 0 |
| 번역·현지화 (`translation`) | 2 | WM-X0339 |

## 재검토 가이드

- 선택되지 않은 355개도 `pruning_405_v1.csv`와 JSON에 전부 **출처 SHA, 소속 인접군, 판정**이 보존된다. `NOT_SELECTED`는 기능 부재나 성능 열등 증명이 아니다.
- 대체성이 약한 거대 인접군은 다음 비교 때 기능 계약에 따라 분할할 수 있다. 동시에 단독 후보를 무리하게 다른 군집에 끼워넣지 않는다.
- **원문/자동 추출의 미확인 필드**가 있는 후보들은 선별을 바꿀 만한 명확한 반례가 나올 때만 재검토한다. 모든 후보를 길고 정밀한 1:1 평가에 넣지는 않는다.
- 등록 직전에는 소수 후보에 한하여 실행 조건, 라이선스, 외부 쓰기·도구 권한, 한국어 적합성, 품질을 확인한다.

## 아티팩트

- `pruning_405_v1.json` — 405 전수 할당·잠정 군집·선정/미선정 근거
- `pruning_405_v1.csv` — Excel 호환 전체 405개 추적표
- 종전 조사·비교 결과는 `research/normalization/` 및 `research/snapshots/2026-10-28/`에 불변 보존

