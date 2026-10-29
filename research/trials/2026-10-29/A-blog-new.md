# 시험 사례 A — 새 글: 한국어 블로그

- 요청: "'AI 글쓰기 도구 고르는 법'을 주제로 한국어 블로그 글 써줘. 독자는 글쓰기에 AI를 써 보려는 직장인이고 분량은 2000자 내외."
- 실행: 2026-10-29 23:55 (KST), 메인 세션에서 대화형 호출. 출력 폴더 `writing-drafts/20261029-2355-blog-choosing-ai-writing-tools/` (git 제외).

## 절차 확인
| 항목 | 결과 |
|---|---|
| registry_check | `OK 67 skills` |
| 과제 해석 | new / 하우투 블로그 / 직장인 / 2000자 / 한국어 |
| 명확화 | 생략(목적·독자·분량이 요청에 있음) — 맞음 |
| 후보 거르기 | prose-naturalizer가 "맞지 않는 상황"(영문 산문 대상)으로 빠짐, content-strategy·copywriting·hook-writer 역할 불일치로 빠짐 |
| 조합 후보 | 3개, 모두 `combo_check --check-runtime` ok |
| 질문 | `AskUserQuestion` 1회(조합 multiSelect + 조합당 개수). 사용자: 조합 2·3, 2개씩 |
| 시안 수 | 4개(2 × 2), opus 서브에이전트 4개 한 메시지 동시 실행, 실패 0 |
| 같은 조합 시안 차이 | 차이 강제 지시 없이 구성·관점이 서로 달랐음 |
| 측면별 따를 스킬 | 지시대로 적용됨(NOTES.md 확인) |
| 원본 불변 | 원문 없음(new). 레포 파일 변경 없음 |

## combo_check 결과
| 후보 | ok | generation | precedence(요약) |
|---|---|---|---|
| blog-post-writing | ✅ | 1 | 모두 blog-post-writing |
| blog-post-writing → general-writing | ✅ | 2 | flow·evidence·voice → general-writing, format·hook·persuasion → blog-post-writing |
| investigating-sources → blog-post-writing → general-writing | ✅ | 3 | evidence·citation-check → investigating-sources, ai-tells·prose-edit·flow·voice → general-writing |

## 결과와 평가
| 시안 | 본문 | 외부 출처 | 사용자 평가 |
|---|---|---|---|
| 조합 2 시안 1 | 1,807자 | 0 | 4위 |
| 조합 2 시안 2 | 1,947자 | 1 | 1위 |
| 조합 3 시안 1 | 2,099자 | 7 | 2위 |
| 조합 3 시안 2 | 2,044자 | 10 | 3위 |

평가 상세와 사용자 기준은 `skills/writing-maestro/feedback.md` 2026-10-30 사이클.

## 발견 사항
1. **(수정 대상, 스킬 사이)** "측면별 따를 스킬"이 조합 안에서 한 스킬만 지시하는 측면까지 줄로 낸다(예: 블로그 시안에 `academic: investigating-sources를 따른다`). 두 스킬 이상이 지시하는 측면만 적어야 한다.
2. **(관찰, 스킬 사이)** investigating-sources를 앞에 둔 조합은 조사한 근거를 많이 싣는 쪽으로 기울어 응집력이 떨어졌다. 레지스트리 주의나 시안 지시에 선별 규칙을 둘지는 추가 사례로 판단.
3. **(범위 밖, 기록만)** 조합 3 시안 2 서브에이전트가 Crossref 첫 요청에 사용자 이메일을 `mailto`로 1회 보냈다. 사용자 결정: 개인정보 등 프로젝트 정책은 writing-maestro가 다루지 않는다(스킬 사이 조율만 담당).
