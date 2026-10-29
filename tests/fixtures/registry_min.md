# 레지스트리 (테스트용 최소본)

## 측면
| id | 이름 | 설명 |
|---|---|---|
| prose-edit | 문장 다듬기 | 문장 단위 편집 |
| ai-tells | AI식 표현 제거 | AI 티 나는 표현 제거 |
| persuasion | 설득 | 설득력 있는 카피 |
| voice | 목소리 | 글쓴이 목소리 보존 |

## 단계
| id | 이름 |
|---|---|
| clarify | 명확화 |
| research | 조사·근거 |
| draft | 구조·초안 |
| genre | 장르·포맷 |
| prose | 문장·문체 |
| check | 검수 |

## 묶음
| id | 구성 |
|---|---|
| msimchowitz | general-writing, humanizer |

## 스킬

### general-writing
- id: WM-X0282
- 출처: msimchowitz/writing-skills `for-agents/general-writing/SKILL.md` @ 214981f, MIT
- 역할: 초안을 더 명료하고 사람다운 문장으로 고친다
- 맞는 상황: 기존 초안의 문장 편집
- 맞지 않는 상황: 새 글의 구조 설계
- 고유 접근: 글쓴이의 목소리를 보존하며 줄 단위로 편집
- 주 측면: prose-edit
- 부 측면: voice
- 단계: prose
- 과제 종류: new, edit, docs
- 묶음: msimchowitz
- 필수 동반: humanizer
- 금지 짝: 없음
- 실행 요건: 필수 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 없음
- 근거: prose-edit "Edit drafts into clearer, sharper, more human prose" / voice "preserving the writer's meaning and personal voice" / humanizer "Remove signs of AI-generated writing"

### humanizer
- id: companion
- 출처: msimchowitz/writing-skills `for-agents/humanizer/SKILL.md` @ 214981f, MIT
- 역할: AI 글쓰기 징후를 제거한다
- 맞는 상황: AI 티가 나는 초안
- 맞지 않는 상황: 사실 검증
- 고유 접근: 위키피디아 AI 글쓰기 징후 목록 기반
- 주 측면: ai-tells
- 부 측면: 없음
- 단계: prose
- 과제 종류: edit
- 묶음: msimchowitz
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 없음
- 근거: ai-tells "Remove signs of AI-generated writing from text"

### prose-naturalizer
- id: WM-X0100
- 출처: example/skills `prose-naturalizer/SKILL.md` @ abc1234, MIT
- 역할: 문장을 자연스럽게 만든다
- 맞는 상황: 어색한 번역투 문장
- 맞지 않는 상황: 원고 전체 집필
- 고유 접근: 문장 리듬 교정
- 주 측면: ai-tells, prose-edit
- 부 측면: 없음
- 단계: prose
- 과제 종류: edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: manuscript-writing
- 실행 요건: 필수 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 없음
- 근거: ai-tells "removes machine-sounding phrasing" / prose-edit "rewrites sentences for natural rhythm" / manuscript-writing "overlaps with full manuscript drafting"

### copywriting
- id: WM-X0200
- 출처: example/skills `copywriting/SKILL.md` @ def5678, MIT
- 역할: 마케팅 카피를 쓴다
- 맞는 상황: 랜딩 페이지 카피
- 맞지 않는 상황: 학술 글
- 고유 접근: 가치 제안 중심
- 주 측면: persuasion
- 부 측면: ai-tells
- 단계: draft
- 과제 종류: new, edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 없음
- 근거: persuasion "Write, rewrite, or improve marketing copy" / ai-tells "Drafts never use AI tells"
