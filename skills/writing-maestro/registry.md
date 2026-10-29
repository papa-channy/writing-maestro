# writing-maestro 스킬 레지스트리

writing-maestro가 매 호출 새로 읽는 스킬 목록이다. 앞부분은 범위·측면·단계·묶음·조합 규칙, 뒷부분은 스킬별 항목이다. 이 파일이 진실 원천이다. 스킬 원문(서드파티)은 고치지 않고, 충돌은 여기 적은 측면과 시안 지시의 우선순위로만 다룬다.

## 고치는 법

- **스킬 추가**: `~/.claude/skills/<이름>/`에 설치하고 설치 매니페스트(`research/install/2026-10-29-install-manifest.json`)의 `skills` 목록에 항목을 더한 뒤(`installed_dir`는 설치 폴더 절대 경로로 마지막 이름이 `<이름>`과 같아야 하고, `status`는 `READY`처럼 `BLOCKED`가 아닌 값이어야 설치된 것으로 친다. 나머지 필드는 기존 항목을 따른다. 출처가 `plugin`인 스킬은 설치 확인을 건너뛴다), `## 스킬` 아래에 `### <이름>` 항목을 다른 항목과 같은 필드 순서로 쓴다. 주 측면은 그 스킬의 본업으로 결과물에서 정하는 측면, 부 측면은 원문에 규칙이 있지만 본업이 아닌 측면이다. 주·부 측면, 필수 동반, 금지 짝마다 `근거`에 `<키> "<원문 인용>"` 쌍을 하나씩 ` / `로 이어 붙인다(인용 안에 ` / 단어 "` 형태는 쓰지 않는다). 사용자 정보 없이는 결과가 안 나올 때만 단계에 `clarify`를 넣는다. 측면 표의 '주 측면 스킬' 칸도 함께 고친다.
- **스킬 제거**: 항목을 지우고, 측면 표와 묶음 표에서 이름을 지운다. 다른 스킬의 `필수 동반`에 남아 있으면 검증이 실패한다.
- **새 측면**: 두 스킬이 동시에 다르게 지시하면 결과가 흔들리는 결과물 속성일 때만 만든다. id는 소문자 ascii 슬러그.
- **재생성 주의**: `research/registry-build/build_registry.py`를 다시 돌리면 이 파일의 손 편집이 덮어써진다. 고칠 때는 `research/registry-build/assignments.py`를 고친 뒤 다시 만들거나, 이 파일만 직접 고치고 스크립트는 돌리지 않는다.
- **검증**: 고친 뒤 다음을 돌려 `OK <n> skills`를 확인한다(매니페스트는 레지스트리 경로에서 찾는다. 다른 파일은 `--manifest`로 넘긴다). 구조 오류는 exit 1, 설치 불일치는 `WARN` 줄과 `OK <n> skills (<k> warnings)`로 나온다. 조합 하나를 따져 보려면 `combo_check.py`를 쓴다.

```
python3 skills/writing-maestro/scripts/registry_check.py --registry skills/writing-maestro/registry.md
python3 skills/writing-maestro/scripts/combo_check.py --registry skills/writing-maestro/registry.md copywriting humanizer
```

## 범위

다룬다: 글쓰기 과제 네 종류.
- `new` 새 글 쓰기: 요청과 자료로 새 글을 쓴다.
- `edit` 기존 글 고치기: 원문을 고친 판본(교정, 번역, 문체 변환, AI식 표현 제거 등). 원문 파일은 고치지 않는다.
- `review` 검토만 하기: 발견 사항·심각도·수정 제안이 담긴 검토 보고서. 대상 원문은 고치지 않는다.
- `docs` 코드베이스 문서 작업: README, CLAUDE.md/AGENTS.md, 설계 문서, 런북 같은 레포 문서. 시안은 대상 파일을 자기 폴더로 복사해 작업한다.

다루지 않는다: 게시·발송·업로드(메일 발송, 소셜 게시, 투고 제출은 사용자가 직접 한다), 글이 아닌 과제(코드 구현, 이미지·영상 생성, 데이터 분석 자체).

## 측면

측면 = 두 스킬이 한 시안에서 동시에 다르게 지시하면 결과가 흔들리는 결과물 속성. 같은 측면을 **주 측면**으로 가진 스킬들이 한 클러스터이고, 조합은 클러스터당 하나만 뽑는다(묶음 예외는 아래 조합 규칙). 한 스킬은 주 측면을 여러 개 가질 수 있다.

장르 규칙은 장르별로 나눴다. 학술(`academic`), 기술 문서(`tech-docs`), 프롬프트(`prompt`)는 장르 측면을 하나씩 두고, 서사는 전제·플롯·인물·장면·원고·장르 팩·운문·연속성으로 쪼갰다(같은 묶음 안에서 순서대로 함께 쓰는 스킬들이 서로 막히지 않게). 마케팅·소셜은 장르 측면을 따로 두지 않았다. 그 스킬들의 규칙은 이미 설득(`persuasion`)·훅(`hook`)·포맷(`format`)·구조(`structure`)로 갈리기 때문이다.

| id | 이름 | 설명 | 주 측면 스킬(클러스터) |
|---|---|---|---|
| intent | 요구·의도 정의 | 글의 목적·독자·성공 기준·범위. 대부분 사용자 답이 있어야 정해지므로 명확화 단계 스킬이 소유한다. | doc-coauthoring, idea-refine, interview-me, requirements-clarity, story-init |
| topic-plan | 주제·기획 선정 | 무엇을 쓸지(콘텐츠 필러, 연구 방향)를 고르고 순위를 매기는 일. 한 편의 골격(structure)과는 다른 층이다. | content-strategy, research-ideation |
| evidence | 근거·출처 | 주장마다 어떤 근거를 대는지, 근거 없는 주장을 어떻게 표시하는지, 주장 강도를 근거에 맞추는 규칙. 조사·근거 지도 스킬이 주 소유자이고, 초안 스킬의 '지어내지 말라' 규칙은 부 측면이다. | build-evidence-map, docs-sync-audit, evidence-synthesis, investigating-sources, literature-review, scientific-writing |
| citation-check | 서지 검증 | 참고문헌이 실재하고 메타데이터가 맞는지 확인하는 일. 근거 조직(evidence)과 나눈 이유: 검증 방식이 달라도 결과가 흔들리지 않으므로, 근거를 조직하는 초안 스킬과 검증 스킬을 한 조합에 넣을 수 있게 한다. | citation-verification |
| structure | 전체 구조·논증 흐름 | 문서 골격(섹션 구성·순서·템플릿)과 논증 순서. 초안 스킬은 저마다 자기 산출물의 골격을 정하므로, 두 초안 스킬은 대개 여기서 갈린다. | abstract-writing, agent-md-refactor, awesome-content-repurpose, blog-post-writing, chatbot-conversation-design, copywriting, crafting-effective-readmes, create-implementation-plan, create-specification, data-storytelling, doc-coauthoring, documenting-contracts, literature-review, paper-writing, rebuttal-and-response-to-reviewers, recording-decisions, short-form-video-script, writing-design-docs, writing-runbooks |
| flow | 문단 흐름·제목 척추 | 제목·소제목·문단 첫 문장·문단 끝·문단 사이 전환. 골격(structure)은 그대로 두고 다듬는 층이다. | non-autoregressive-writing-pass |
| prose-edit | 문장 문체·교정 | 문장 단위의 명료성·간결성·어휘 호응·리듬·문법. 리듬(문장 길이)도 여기에 넣는다: 리듬만 따로 지시하는 스킬은 writing-cadence 하나뿐이고 그마저 humanizer가 부른다. | academic-voice, better-usage, general-writing, line-editing, reviewing-technical-prose, technical-writing, writing-cadence |
| ai-tells | AI식 표현 제거 | 대조 반전(not X but Y), 3항 나열, 엠대시, AI 어휘, 상투 도입·결말처럼 기계 티가 나는 패턴의 금지·제거 목록. 목록이 스킬마다 다르므로 한 시안에서는 한 목록만 따른다. | general-writing, humanizer, prose-naturalizer, reviewing-technical-prose, technical-writing |
| voice | 저자·브랜드 목소리 | 누구의 목소리로 쓰는가: 보이스 프로필(voice.md, brand-profile.md), 학술 레지스터, 작가·인물 목소리 보존, 문서 어조. | awesome-content-voice, brand-profile, line-editing, voice-builder, voice-style |
| hook | 도입·훅 | 첫 줄, 영상 첫 3초, 제목줄, 메일 첫 문장처럼 독자를 붙잡는 오프닝. | hook-writer |
| persuasion | 독자 설득·전환 | 가치 제안, 혜택, CTA, 요청 하나, 피치처럼 독자를 행동으로 옮기는 설계. | cold-email, copywriting, research-grants, submission |
| format | 포맷·채널 규격 | 길이·글자 수 한도, 고정 템플릿과 front matter, 파일 위치·이름, 플랫폼·검색(SEO) 규격, 출력 포장 형식. | awesome-content-repurpose, blog-post-writing, create-implementation-plan, create-specification, short-form-video-script, submission |
| translation | 번역·현지화 | 원문 의미 충실성, 용어 일관성, 로케일 적응. | translation |
| review-report | 검토 보고서 형식 | 검토 결과의 판정·심각도·점수 체계와 보고서 구조. 검토 스킬끼리 조합할 수 있도록 대부분 부 측면으로 두었다. | submission-reviewer |
| academic | 학술 장르 관례 | 연구 원고·초록·리뷰·연구비 제안서·심사 답변의 분야 관례: 주장 경계, 근거 동사 등급, 보고 지침, 기관 요건. | abstract-writing, evidence-synthesis, paper-writing, rebuttal-and-response-to-reviewers, research-grants, scientific-writing |
| tech-docs | 기술 문서 하우스 스타일 | 저장소 기술 문서의 공통 규칙: 문서 종류별 편집 규칙, 규칙 우선순위, 한 사실 한 곳, 불변 기록. | technical-writing |
| prompt | 프롬프트·에이전트 지시문 설계 | 모델이 읽는 지시문의 설계: 목표 배치, 정책 계층, 긍정형 지시, 예시, 압축. | context-engineering, prompt-improving, prompt-optimizer-copilot, prompt-optimizer-sentry, write-agent-prompts, writing-for-agents |
| premise | 전제·주제 (서사) | 통제 아이디어(가치+원인), 로그라인, 주제 아크, 모티프. | premise-workshop, story-init, theme-craft |
| plot | 플롯·페이싱 (서사) | 아크, 비트 시트, 타임라인, 복선·회수 기록, 장면 결과로 본 페이싱. | plot-structure |
| character | 인물 설계 (서사) | 인물 프로필, 관계, 이야기 중 변화(progressions), 아크 기록. | character-management |
| scene | 장면 기법 (서사) | 장면 단위 기법: scene/sequel, 서브텍스트, 딥 POV, 플래시백, 보여주기. | scene-craft |
| narrative | 서사 원고 집필 | 챕터 본문을 쓰는 절차: 아웃라인 승인, 맥락 수집 규율, POV·시제·언어. | chapter-writing |
| fiction-genre | 소설 장르 관례 | 미스터리·로맨스·스릴러·호러·SF 등 장르 팩의 독자 계약과 원장. | genre-craft |
| verse | 운문 형식 | 운율·압운·정형시 규칙과 스캔 증명. | verse-craft |
| continuity | 연속성·프로젝트 기록 | story 프로젝트의 연속성 상태, 레지스트리, 메타데이터 정합성. | revision-continuity, story-maintenance |

## 단계

조합 안 적용 순서는 research → draft → genre → prose이다.

| id | 이름 | 설명 |
|---|---|---|
| clarify | 명확화 | 사용자만 줄 수 있는 정보(인터뷰, 실제 글 샘플, 브랜드 사실, 사용자가 하는 스크리닝)가 있어야 결과가 나오는 단계. 조합에 넣지 않고 ② 단계로 보낸다. |
| research | 조사·근거 | 출처 조사, 근거 지도, 주제·연구 방향 선정. |
| draft | 구조·초안 | 골격을 정하고 본문 초안을 쓴다. |
| genre | 장르·포맷 | 장르 관례나 채널 규격을 초안 위에 얹는다. |
| prose | 문장·문체 | 완성 초안의 문장·목소리·AI식 표현을 다듬는다. |
| check | 검수 | 결과물을 고치지 않고 점검해 보고한다. 조합 본체가 아니라 검수 단계로 붙는다. |

## 묶음

같은 저장소 안에서 서로 부르는 순서가 정해진 스킬 집합. 묶음 흐름 중간에 다른 스킬을 같은 측면으로 끼워 넣지 않는다.

| id | 구성 | 설명 |
|---|---|---|
| story-skills | story-init, premise-workshop, character-management, plot-structure, scene-craft, chapter-writing, line-editing, verse-craft, story-maintenance, voice-style, theme-craft, genre-craft, submission, revision-continuity | danjdewhurst/story-skills. story-init(또는 premise-workshop→story-init)이 프로젝트를 만들고, 설계(인물·플롯·주제·장르) → scene-craft → chapter-writing → line-editing(voice-style 선행) 순. 모두 `story` CLI와 story.md 프로젝트를 공유한다. |
| social-media-skills | brand-profile, voice-builder, hook-writer, short-form-video-script | social-media-skills/skills. brand-profile → voice-builder(샘플이 있을 때) → hook-writer / short-form-video-script. 앞의 둘이 만든 brand-profile.md·voice.md를 뒤의 둘이 읽는다. |
| msimchowitz | paper-writing, abstract-writing, academic-voice, general-writing, literature-review, non-autoregressive-writing-pass, prompt-improving, humanizer, better-usage, writing-cadence | msimchowitz/writing-skills. paper-writing·literature-review·abstract-writing이 마지막에 general-writing을 부르고, general-writing은 humanizer를 임베디드 모드로 부르며, humanizer가 better-usage → academic-voice → writing-cadence → non-autoregressive-writing-pass를 차례로 적용한다. |
| technical-writer | technical-writing, writing-design-docs, writing-runbooks, recording-decisions, documenting-contracts, reviewing-technical-prose | riekelt/technical-writer. technical-writing이 하우스 스타일 기반이고 나머지 다섯은 문서 유형 스킬로 모두 technical-writing을 필수 배경으로 읽는다. |
| research-skills | investigating-sources, evidence-synthesis | anayy09/claude-research-skills 중 호출 관계가 있는 둘. evidence-synthesis가 인용 검증을 investigating-sources의 check_citations.py에 맡긴다. 같은 저장소의 prose-naturalizer·research-ideation·submission-reviewer는 서로 부르지 않아 묶음에 넣지 않았다. |

## 조합 규칙

`combo_check.py`가 다음을 결정적으로 판정한다.

1. **금지 짝**: 어느 쪽이 적었든 두 구성원을 함께 넣지 않는다. 구성원 A가 금지한 스킬 S가 다른 구성원 B의 닫힘에 있어도 충돌이다(`forbidden pair A+S(via B)`). 단 S가 A 자신의 닫힘에 있으면(예: paper-writing은 humanizer를 금지하지만 general-writing을 거쳐 스스로 부른다) 이 경유 충돌은 면제한다.
2. **주 측면 배제(동반 포함)**: 각 구성원의 `필수 동반`을 끝까지 따라간 닫힘(조건부 동반 포함, 자기 자신 제외)까지 함께 본다. 구성원이 직접 넣지 않아도 그 동반 스킬의 규칙이 시안에 들어가기 때문이다(예: writing-design-docs → technical-writing의 문장 규칙, paper-writing → general-writing → humanizer의 AI식 표현 목록). 측면마다 그것을 주 측면으로 가진 서로 다른 출처 스킬을 모으고, 출처가 둘 이상이며 그 출처끼리 조율되어 있지 않으면 `primary overlap <측면>: <그 출처를 들여온 구성원들>` 충돌이다. 두 구성원이 같은 출처 하나를 들여오는 것(예: writing-design-docs와 reviewing-technical-prose가 둘 다 technical-writing을 부름)은 충돌이 아니다. 같은 측면의 두 출처를 한 구성원(자신과 그 닫힘)만 들여오면 묶음이 달라도 조율로 보고 충돌이 아니다. 그 구성원이 자기 동반들의 순서를 짜기 때문이다(현재 레지스트리에서는 이런 출처끼리가 모두 같은 묶음이라 아래 조율로도 걸러진다). 조율 = 같은 묶음이고, (구성원 ∪ 닫힘) 안의 어떤 스킬이 `필수 동반`을 따라 두 출처 모두에 닿는다(한 출처가 다른 출처를 부르는 경우 포함, 여러 단계 허용). 부르는 쪽이 순서를 짜기 때문이다. 공통 동반을 함께 부를 뿐인 형제(writing-design-docs와 writing-runbooks가 둘 다 technical-writing을 부름)는 서로 조율되지 않으므로 둘의 골격(structure)은 충돌이다.
3. **생성 스킬 최대 3개**: 단계가 `clarify`·`check`만이 아닌 구성원이 생성 스킬이다. 조합 안 다른 구성원의 `필수 동반`인 구성원은 세지 않는다. 닫힘에만 있는 동반 스킬은 구성원이 아니므로 세지 않는다.
4. **명확화 전용 스킬은 조합에 넣지 않는다**: 단계가 `clarify`뿐인 스킬은 ② 명확화 단계로 보낸다.
5. **우선순위**: 부 측면도 주 측면처럼 (구성원 ∪ 닫힘)으로 보고 구성원에게 돌린다. 구성원 자신이나 그 닫힘의 스킬이 부 측면으로 가진 측면은 그 구성원이 가진 것으로 친다. 그 측면은 주 측면으로 가진 구성원(자기 자신 또는 닫힘이 소유)을 따른다(앞선 구성원 우선). 그런 구성원이 없으면 그 측면을 부 측면으로 가진 구성원 중 조합 순서상 뒤 스킬을 따른다. 따르는 구성원이 아닌 나머지 부 측면 보유 구성원은 `ignored`에 오른다. 단 그 측면을 주 측면으로 가진 구성원은 오르지 않는다. 부 측면 보유 구성원이 하나뿐이고 주 측면 소유자가 없으면 `precedence`에만 있고 `ignored`에는 없다. 시안 지시에 "측면별 따를 스킬"로 적는다.

`필수 동반`은 자동 포함이 아니다. 조합에는 오케스트레이터가 직접 순서를 짜는 스킬만 넣고, 구성원이 스스로 부르는 동반 스킬(예: general-writing → humanizer)은 넣지 않는다. 동반 관계는 충돌·우선순위를 닫힘까지 따지는 데(규칙 1·2·5)와 생성 스킬 수 계산에 쓴다. 산출 파일 규약이 다른 두 보이스 프로필(`voice.md` vs `voice/<name>.md`)은 한 시안에서 하나만 쓴다.

## 스킬

### abstract-writing
- id: WM-X0279
- 출처: msimchowitz/writing-skills `for-agents/abstract-writing/SKILL.md` @ 214981f, MIT
- 역할: 연구 논문 초록을 섹션별 요약이 아니라 독자를 위한 압축된 논증으로 쓰거나 고치거나 진단한다.
- 맞는 상황: 초록만 요청받았을 때, 학회·저널·arXiv 초록, 기여 목록이나 목차 압축처럼 읽히는 초록을 다시 쓸 때.
- 맞지 않는 상황: 초록 외 논문 본문 작성, 일반 산문 편집(general-writing 담당), 근거 원고나 노트가 전혀 없는 상태에서의 결과 창작.
- 고유 접근: 문제-한계-답-증거-범위-함의의 단일 추론 흐름을 먼저 세우고, 근거 동사 수준과 주장 경계를 원고와 대조해 검증한 뒤 본문 확정 후 초록으로 되돌아가 재점검한다.
- 주 측면: structure, academic
- 부 측면: evidence, ai-tells, prose-edit, flow
- 단계: draft
- 과제 종류: new, edit, review
- 묶음: msimchowitz
- 필수 동반: general-writing
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: 원고 본문·도입·결론·한계 (근거로 읽음); references/example-abstract-patterns.md (Simchowitz 그룹 음성 맞춤 시)
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트 이슈 없음(READY). 노트만 있을 때는 계획과 완료 작업을 구분하고 누락된 결과는 사용자에게 묻는다. academic-voice 읽기는 '더 강한 음성 샘플이 없을 때' 조건부이므로 requires에 넣지 않았다. 판단: general-writing 동반은 주장 감사 뒤 마지막 음성 패스로 부른다는 뜻이다.
- 근거: structure "Do not give every section or contribution equal space." / academic "Use "shows" or "demonstrates" for direct evidence" / evidence "Never infer a result, comparison, number, or limitation from a generic abstract pattern." / ai-tells "Avoid wrappers such as "This paper presents,"" / prose-edit "Let sentence length follow the argument." / flow "Do not end by announcing code, future work, or another contribution" / general-writing "After the claim audit, run the complete sibling [general-writing workflow](../general-writing/SKILL.md) once."

### academic-voice
- id: WM-X0280
- 출처: msimchowitz/writing-skills `for-agents/academic-voice/SKILL.md` @ 214981f, MIT
- 역할: 사려 깊고 정확하며 독자 이해를 중시하는 학자의 목소리로 산문을 쓰거나 고친다.
- 맞는 상황: 연구 설명문, 학술 논문, 교재식 설명, 학술 요약, 기업·LinkedIn·Reddit·GitHub 어조를 피해야 하는 초안.
- 맞지 않는 상황: 매뉴얼·절차서 같은 지시문(직접 지시는 그런 장르에서만), 캐주얼·법률·개인 글을 저널 문체로 바꾸는 일, 다른 스킬 파이프라인 호출(호출 경계에서 금지).
- 고유 접근: 추상 명사 압축을 학술적 엄밀함으로 착각하지 않도록 행위자와 관계를 이름 붙이고, 차용된 레지스터 네 가지(기업, LinkedIn, Reddit, GitHub)를 명시적으로 제거한다.
- 주 측면: prose-edit
- 부 측면: voice, evidence, ai-tells, flow
- 단계: prose
- 과제 종류: new, edit
- 묶음: msimchowitz
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트 이슈 없음(READY). forbids는 다른 스킬이 호출했을 때의 호출 경계 규칙이다(단독 사용 시 해당 없음). 판단: 원문의 'Do not invoke Humanizer …' 줄은 humanizer가 이 스킬을 부를 때 파이프라인을 다시 부르지 말라는 재귀 방지 규칙이라 금지 짝으로 적지 않았다. humanizer(general-writing 경유 포함)가 이미 이 스킬을 적용하므로 그런 조합에 따로 넣으면 중복이다. 예외: paper-writing이 학술 산문 초안에서 academic-voice를 직접 부르는 경우. 학술 레지스터(voice)는 부 측면으로 둔다: humanizer가 이 스킬을 학술·설명문일 때만 레지스터로 적용하고(캐주얼·기술·개인 글은 바꾸지 않음) 사용자 샘플이 규칙보다 우선하므로, 주 측면으로 두면 humanizer·general-writing을 거쳐 브랜드·작가 목소리 스킬(hook-writer, line-editing 등)과의 조합이 모두 막힌다.
- 근거: prose-edit "Do not mistake abstraction for rigor." / voice "Write like an academic who is thoughtful, careful, and precise" / evidence "Distinguish evidence, interpretation, and conjecture." / ai-tells "Remove LinkedIn cadence: manufactured hooks, one-line lessons, motivational closure" / flow "Prefer connected exposition to a stack of directives, slogans, headings, or equally weighted bullets."

### agent-md-refactor
- id: WM-X0371
- 출처: softaworks/agent-toolkit `skills/agent-md-refactor/SKILL.md` @ 3027f20, MIT
- 역할: 비대해진 AGENTS.md, CLAUDE.md 같은 에이전트 지침 파일을 점진적 공개 원칙에 따라 최소 루트 파일과 연결된 주제별 파일로 나눈다.
- 맞는 상황: 'AGENTS.md가 너무 길다', 'CLAUDE.md 정리/분리' 같은 요청.
- 맞지 않는 상황: 일반 문서나 README 작성, 새 지침의 내용을 만드는 작업. 지침 파일 구조 개편 전용이다.
- 고유 접근: 모순 찾기, 필수 추출, 분류, 구조 생성, 삭제 표시의 5단계로 진행하고 루트 파일을 50줄 미만으로 유지한다.
- 주 측면: structure
- 부 측면: prompt, intent
- 단계: draft
- 과제 종류: edit, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: CLAUDE.md 또는 AGENTS.md(루트); 링크 대상 .claude/*.md 또는 docs/agent-instructions/*.md
- 주의: 매니페스트: sha_match true, 제한 없음. Phase 1에서 모순이 발견되면 사용자 답을 받아야 진행하므로 부분적으로 대화가 필요하지만 핵심 작업은 비대화형으로 판단했다. 판단: 단계: facts의 stage_hint는 prose지만 산출물이 파일 재구성이라 draft로 둔다.
- 근거: structure "Aim for 3-8 files (not too granular, not too broad)" / prompt "Include only actionable instructions" / intent "Ask the user to resolve before proceeding."

### awesome-content-repurpose
- id: WM-X0242
- 출처: khasky/awesome-agent-skills `skills/awesome-content-repurpose/SKILL.md` @ 58ea4e8, MIT
- 역할: 하나의 원문(글, 가이드, 노트)을 긴 글, 일반 포스트, 짧은 포스트 3종으로 변환하며 사실·수치·판단을 보존한다.
- 맞는 상황: 한 글을 소셜 포스트로 각색해 달라는 요청. 사용자가 고른 언어로 플랫폼 그룹별 3개 형식(1-short/2-regular/3-long)을 생성.
- 맞지 않는 상황: 게시 시각·일정·큐 관리(awesome-content-campaign/publisher 몫), 원문에 없는 사실 추가, 원문과 다른 글로 바꾸는 각색.
- 고유 접근: 긴 글을 먼저 완결본으로 쓰고 나머지 둘을 그 사실에서 새 문장으로 다시 쓴다. 6문항 인터뷰, 증거 노트와 모듈 맵, 사실 검증, 앵커, 형식별 한도(짧은 280자, 일반 2000자)와 감사 단계를 거친다.
- 주 측면: structure, format
- 부 측면: evidence, ai-tells, prose-edit, flow
- 단계: draft
- 과제 종류: new
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: ffmpeg for video stills (Phase 10); web access for Phase 3 verification; voice/<name>.md from awesome-content-voice (user-supplied path); awesome-style-mimic, awesome-humanize-en, awesome-content-campaign, awesome-content-publisher, awesome-content-image-adapter (not installed)
- 필수 명령: 없음
- 상태 파일: repurpose/<slug>-<YYYYmmdd-HHMMSS>/ (run folder under the agent's scratch area; holds source/, run-settings.md, source-notes.md, editorial-brief.md, anchors.md, claims.md); repurpose/<slug>-<stamp>/<slug>_social_posts/1-short.md, 2-regular.md, 3-long.md (+ optional media/); voice/<name>.md from awesome-content-voice (optional input, user-supplied path)
- 주의: 매니페스트: 보이스 의존은 선택적(기본 1인칭). 언어·아이디어·보이스·이모지·크리에이티비티·푸터 6문항 인터뷰가 모두 답변되기 전에는 초안 작성 금지(플래그/발화로 답한 항목은 생략). 끝에 미디어 질문 필수. 형제 스킬 다수 미설치. 레포 출력은 호출 디렉터리가 아닌 scratch 영역 repurpose/ 아래. 판단: 단계: 원문은 6문항 인터뷰(언어·아이디어·보이스·이모지·크리에이티비티·푸터)를 먼저 하지만 모두 초안 서브에이전트가 가정할 수 있는 값이라 clarify로 두지 않았다. 가정은 brief.md에 적는다.
- 근거: structure "The long form is written first, and the other two come out of it." / format "2000 characters, the whole body counted" / evidence "nothing is added that the source or a primary-source verification does not carry." / ai-tells "no em or en dash and no Unicode arrow" / prose-edit "Sentence length is a spread, never a pattern." / flow "Every form closes in its own words, on a verdict."

### awesome-content-voice
- id: WM-X0243
- 출처: khasky/awesome-agent-skills `skills/awesome-content-voice/SKILL.md` @ 58ea4e8, MIT
- 역할: 사용자의 글(게시글, 파일, 샘플, 인터뷰)에서 보이스 프로필 voice/<name>.md를 만들어 다른 스킬이 읽게 한다.
- 맞는 상황: '내 보이스 학습' 요청. 게시글 URL, 파일/폴더, 붙여넣기 텍스트, 사이트 또는 증거가 없는 콜드스타트(인터뷰+아키타입)에서 시작.
- 맞지 않는 상황: 다른 사람 보이스를 사용자 것으로 제시하는 용도. 실제 글 작성 자체는 하지 않고 프로필만 만든다.
- 고유 접근: 증거를 디스크에 덤프해 존재/부재(분모 포함) 신호를 분석하고, 플랫폼별 레지스터를 분리하며 '지우지 말 개인 습관'을 보호한다. 출처·신뢰도를 기록하고 재생(playback)과 보정(calibration) 단계로 검증한다.
- 주 측면: voice
- 부 측면: evidence, ai-tells
- 단계: clarify
- 과제 종류: new
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: browser/Playwright MCP bridge for scraping social profiles (level c); awesome-style-mimic (only when a website is a source; not installed); awesome-content-publisher/references/browser-interaction.md (target gate; not installed)
- 필수 명령: 없음
- 상태 파일: voice/<name>.md (created in the invocation directory; <name> defaults to handle or 'me'; never overwritten without asking); voice/.work/<name>/ (sources/, analysis/, history/<date>.md; working state, deletable); voice/ may need .gitignore (asks user inside a git repo)
- 주의: 매니페스트: 결과물은 호출 디렉터리의 voice/<name>.md이며 awesome-content-repurpose가 선택적으로 읽음. git 저장소 안에서는 커밋 여부 동의를 먼저 구해야 함. 로그인 필요 플랫폼(level c)은 브라우저 브릿지/토큰 확인 후에만 수집. awesome-style-mimic 미설치. 판단: 산출 파일은 voice/<name>.md로, social-media-skills의 voice.md와 경로 규약이 다르다. 두 프로필을 한 시안에 섞지 않는다.
- 근거: voice "One file that other skills read instead of guessing a voice per task." / evidence "Never write an absence claim you did not count" / ai-tells "Personal tics — never clean these"

### better-usage
- id: companion
- 출처: msimchowitz/writing-skills `for-agents/better-usage/SKILL.md` @ 214981f, MIT
- 역할: 문법적으로는 맞지만 주어가 동사를 수행할 수 없거나 목적어가 안 맞는 단어 조합을 의도한 주장을 보존하며 진단하고 고친다. humanizer 3단계 동반 스킬.
- 맞는 상황: 동사가 주어나 목적어에 문자 그대로 맞지 않을 때, 주장이나 섹션이 할 수 없는 행동을 하는 문장, 모호한 의인화로 가려진 추상 관계, 행위자를 숨기거나 검토를 암시하는 추상 과정 명사, 동사 교체만으로 부족해 중간 명사가 필요한 경우.
- 맞지 않는 상황: 확립된 학술 약어(정리가 함의한다, 증거가 지지한다, 그림이 보여준다)와 의도적 은유의 제거, 절차 세부나 강조를 덧붙이는 수리.
- 고유 접근: 주어, 동사, 목적어를 분해해 의도한 관계를 다른 말로 풀어쓴 뒤, 필요한 경우 주장의 범위 같은 누락된 중간 명사를 명명하며 인식적 강도를 유지한다.
- 주 측면: prose-edit
- 부 측면: evidence
- 단계: prose
- 과제 종류: edit, review
- 묶음: msimchowitz
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: references/compatibility-examples.md (전체 의미 사용 패스 시)
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트: 동반 스킬, SHA가 선택 목록에 없어 현재 HEAD 설치. humanizer 3단계가 호출하므로 단독 라우팅 대상이 아니다. forbids는 호출 경계 규칙(다른 스킬이 호출했을 때 파이프라인 재호출 금지). 판단: 원문의 'Do not invoke Humanizer …' 줄은 humanizer가 이 스킬을 부를 때 파이프라인을 다시 부르지 말라는 재귀 방지 규칙이라 금지 짝으로 적지 않았다. humanizer(general-writing 경유 포함)가 이미 이 스킬을 적용하므로 그런 조합에 따로 넣으면 중복이다.
- 근거: prose-edit "Choose words that express the relation the sentence actually asserts." / evidence "Recheck epistemic force."

### blog-post-writing
- id: WM-X0335
- 출처: seb1n/awesome-ai-agent-skills `writing-and-content/blog-post-writing/SKILL.md` @ 75865a5, MIT
- 역할: 하우투, 리스티클, 오피니언, 케이스 스터디 등 SEO 최적화 블로그 글을 키워드 조사부터 개요, 초안, SEO, 교정까지 쓴다.
- 맞는 상황: 블로그 글 작성 요청(주제, 키워드, 포맷, 오디언스, 톤, 분량, CTA 제공 시).
- 맞지 않는 상황: 검색량 없는 오피니언/틈새 글은 SEO가 부차적. 마케팅 랜딩 카피나 학술 글에는 맞지 않는다.
- 고유 접근: 검색 의도에 따라 포맷을 고르고 주요 키워드를 제목·첫 문단·H2·메타 설명에 배치하며, 훅-논지-본문-요약+CTA 구조와 피처드 스니펫 섹션을 설계한다.
- 주 측면: structure, format
- 부 측면: hook, flow, persuasion, evidence, voice
- 단계: draft
- 과제 종류: new
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: web access for keyword/top-ranking research
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트: 특이사항 없음. 예시의 통계(Datadog 설문 등)는 예시용이며 실제 작성 시 출처 검증 필요.
- 근거: structure "Create a detailed outline with the title (including the primary keyword)" / format "Write a meta description (150-160 characters)" / hook "Start with the hook, not the backstory." / flow "No paragraph should exceed 4-5 sentences in a blog post." / persuasion "End with a clear CTA." / evidence "Verify all statistics and claims have credible sources." / voice "review 2-3 recent published posts to match the existing tone"

### brand-profile
- id: companion
- 출처: social-media-skills/skills `skills/brand-profile/SKILL.md` @ f28cef2, MIT
- 역할: 다른 소셜 스킬이 모두 읽는 브랜드 컨텍스트(정체성, 포지셔닝, 오디언스, 보이스, 증거, 가드레일, 운영 기본값)를 인터뷰·자료 추출로 brand-profile.md에 기록한다.
- 맞는 상황: 새 비즈니스/클라이언트 작업 시작, '브랜드 설정', '브랜드 보이스 정의', 다른 소셜 스킬이 브랜드 컨텍스트를 요구할 때. 모든 업종에 사용 가능.
- 맞지 않는 상황: 실제 게시글 작성(콘텐츠 스킬), 기존 글 코퍼스에서 보이스 도출(voice-builder). 완전하고 최신인 프로필이 이미 있으면 재인터뷰하지 않는다.
- 고유 접근: 웹사이트/기존 글에서 먼저 초안을 뽑고 2~4문항씩 소규모 인터뷰로 확인·교정하며, 모호한 답을 구체적으로 밀어붙인다. 보이스는 형용사 대신 차원과 어휘로 기록한다.
- 주 측면: voice
- 부 측면: evidence
- 단계: clarify
- 과제 종류: new
- 묶음: social-media-skills
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: user's website, social handles, existing posts, deck (used to draft provisional profile)
- 필수 명령: 없음
- 상태 파일: brand-profile.md (created/read; stored with the user's project files in the user's workspace; per-client profile named by client for agencies; not stored in WoopSocial)
- 주의: 컴패니언 스킬(SELECTED_V3 58 ID 목록 외). hook-writer/voice-builder/short-form-video-script가 먼저 읽는 파일 brand-profile.md를 생성. 프로필이 분기보다 오래되면 stale. 이미 최신 프로필이 있으면 재인터뷰 금지.
- 근거: voice "The voice section has **specific lexicon and banned words**, not adjectives." / evidence "claims it can't legally make"

### build-evidence-map
- id: WM-X0196
- 출처: github/awesome-copilot `skills/build-evidence-map/SKILL.md` @ b6483db, MIT
- 역할: 논쟁적인 기술 선택이나 중대한 결정을 위해, 지지·반박·한정·부재 증거를 정확한 출처 구간과 함께 보존하는 감사 가능한 증거 지도(.doubt.json)를 만든다.
- 맞는 상황: 증거, 중간 주장, 상충 관계, 빠진 사실 사이의 관계가 중요한 쟁점 하나를 지도화할 때.
- 맞지 않는 상황: 단순 사실 주장이나 일반 팩트체크(doublecheck 같은 검증 워크플로 사용)와 출처 없는 답변을 그래프로 꾸미는 일.
- 고유 접근: 노드 4종(position/claim/evidence/unknown)과 간선 4종(supports/contradicts/qualifies/missing)으로 추론을 구조화하고, 번들 Node 검증기가 exit 0과 64자 영수증을 낼 때만 유효하다고 말한다.
- 주 측면: evidence
- 부 측면: review-report
- 단계: research
- 과제 종류: new, review
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: node>=18 (built-ins only, no npm deps); UTF-8 JSON .doubt.json output | 선택: doubt-ai@0.8.0 CLI for HTML render ('doubt map') and source verify ('doubt verify'), only if user already installed it and explicitly allows network
- 필수 명령: node
- 상태 파일: <decision>.doubt.json (canonical map, user-chosen path); <decision>.html (optional render); scripts/validate.mjs and scripts/contract.mjs in skill dir (validator); references/map-schema.md, references/evidence-ladder.md
- 주의: 매니페스트: READY_WITH_LIMITS. 렌더러/검증기(doubt-ai@0.8.0)는 설치하지 않아 HTML 렌더와 네트워크 출처 검증은 불가, 검증기 자체는 정상. 검증기가 edge의 추가 'confidence' 키를 거부하지 않음(스키마 문서는 무효라 함). 원문은 doubt verify를 명시적 네트워크 허락 없이 실행하지 말라고 함. 산문 글쓰기 스킬이 아니라 JSON 산출물 스킬이다. 판단: facts의 requires에 있던 node는 스킬이 아니라 실행 파일이라 필수 명령으로 옮겼다.
- 근거: evidence "Topical similarity is not support." / review-report "the current position in one sentence;"

### chapter-writing
- id: WM-X0151
- 출처: danjdewhurst/story-skills `skills/chapter-writing/SKILL.md` @ e44c97c, MIT
- 역할: 스토리 챕터를 outline-first로 쓰는 스킬: `story context`로 맥락을 모으고 비트별 아웃라인 승인을 받은 뒤 전체 산문을 쓰고, 장면·연속성·복선 레코드를 갱신한다.
- 맞는 상황: 챕터 작성, 다음 챕터, 챕터 아웃라인, 이야기 이어쓰기, 장면 집필 등 스토리 프로젝트의 산문 집필.
- 맞지 않는 상황: 장면의 구조·서브텍스트·outcome 계획은 scene-craft, 아웃라인 없는 발견형 집필은 discovery-drafting, 기존 챕터 개정은 revision-continuity(라인 편집은 line-editing).
- 고유 접근: `story context`가 출력한 예산 내 패킹된 맥락(후속 챕터는 제외)만으로 집필하고, 사용자 아웃라인 승인 후 산문을 쓰며, 이후 scene 레코드·continuity/state.md·복선 레코드를 갱신하고 CLI 점검 블록을 돌린다.
- 주 측면: narrative
- 부 측면: scene, voice, hook, continuity, format
- 단계: draft
- 과제 종류: new
- 묶음: story-skills
- 필수 동반: story-init
- 금지 짝: 없음
- 실행 요건: 필수: story.md; characters/ 에 최소 한 명의 캐릭터; story CLI(story context 사용) | 선택: plot/_index.md 플롯 구조; better-writing 스킬(외부, 산문 품질 보완); line-editing 스킬(산문 패스)
- 필수 명령: story, node
- 상태 파일: chapters/chapter-NN.md; scenes/chapter-NN-scene-NN.md; continuity/state.md (current-chapter, character-state, object-state, knowledge-state); continuity/promises|clues|questions/; plot/timeline.md; plot/arcs/*.md Foreshadowing
- 주의: Story Skills 번들 공통: `story` CLI(node>=18, npm 의존성 없음; bun 불필요)에 의존하며 manifest 상 상태 READY, 제한 없음. 상대 파일 참조는 모두 해결됨. 스토리 프로젝트(story.md 기준) 마크다운 폴더 구조와 YAML frontmatter 규칙을 따라야 하며, 소설 프로젝트 파일에 쓰는 스킬이므로 일반 산문/문서 작업에는 맞지 않음. 번들의 line-editing 스킬이 산문 패스를 담당하며 `revised` 표시 전에 실행. 외부 better-writing은 선택 사항이며 설치는 명시적 승인 없이는 실행하지 않음. 분기 책은 interactive-fiction 필요. `story next` 종료 코드는 연속성 결과가 아님. 판단: 단계: 원문은 아웃라인 승인을 받지만 승인만 필요한 것이라 clarify로 두지 않았다. 시안에서는 아웃라인을 brief.md 가정으로 확정하고 쓴다.
- 근거: narrative "Present the outline to the user for approval." / scene "Convey emotion through action, dialogue, and sensory detail rather than stating feelings" / voice "Give each speaker their recorded voice" / hook "Avoid opening with weather or waking up" / continuity "Do not add or edit registry rows by hand." / format "separate scenes with `---` on a line of its own" / story-init "A story project must already exist with at least:"

### character-management
- id: WM-X0152
- 출처: danjdewhurst/story-skills `skills/character-management/SKILL.md` @ e44c97c, MIT
- 역할: 스토리 프로젝트의 characters/ 아래에 캐릭터 프로필(frontmatter+본문)을 만들고 관계·가계도·진행(progressions)·사망/개명·voice 필드를 관리하는 스킬.
- 맞는 상황: 캐릭터 생성·수정·이름 짓기, 관계 그래프·가계도, 캐릭터 타임라인·아크, 개명 또는 사망 처리 같은 캐릭터 관리.
- 맞지 않는 상황: 캐릭터 목소리 기록·점검은 voice-style, 목소리가 구분되도록 대사 고쳐쓰기는 line-editing, 주제 아크의 거짓/진실/아크 유형은 theme-craft.
- 고유 접근: `story names`로 이름 충돌을 먼저 검사하고 대화로 프로필을 쌓아 템플릿에 기록하며, 이후 변화는 progressions로, 관계는 양방향으로, 그래프는 `story diagram relationships`로 생성한다.
- 주 측면: character
- 부 측면: continuity, voice
- 단계: draft
- 과제 종류: new, edit, docs
- 묶음: story-skills
- 필수 동반: story-init
- 금지 짝: 없음
- 실행 요건: 필수: 기존 스토리 프로젝트(story.md 존재) | 선택: story CLI
- 필수 명령: story, node
- 상태 파일: characters/{name-kebab}.md; characters/_index.md (CLI가 재생성; Relationship Map/Family Trees 섹션은 수작업); worldbuilding/factions|artifacts|locations 백링크; continuity/state.md
- 주의: Story Skills 번들 공통: `story` CLI(node>=18, npm 의존성 없음; bun 불필요)에 의존하며 manifest 상 상태 READY, 제한 없음. 상대 파일 참조는 모두 해결됨. 스토리 프로젝트(story.md 기준) 마크다운 폴더 구조와 YAML frontmatter 규칙을 따라야 하며, 소설 프로젝트 파일에 쓰는 스킬이므로 일반 산문/문서 작업에는 맞지 않음. 캐릭터 파일은 이야기 시작 시점의 상태를 기술. 한국어 등 비ASCII 이름은 --id로 ASCII id 지정 필요. 판단: 단계: 원문은 대화로 프로필을 만들지만 인물은 초안 서브에이전트가 제안할 수 있어 draft로 둔다(facts stage_hint는 clarify).
- 근거: character "Build the profile through conversation, exploring:" / continuity "A character file describes the character as the story opens." / voice "Keep these lists short (three to eight entries)" / story-init "A story project must already exist (created via the story-init skill). Verify by checking for `story.md` in"

### chatbot-conversation-design
- id: WM-X0317
- 출처: seb1n/awesome-ai-agent-skills `communication/chatbot-conversation-design/SKILL.md` @ 75865a5, MIT
- 역할: 챗봇 대화 설계: 페르소나, 인텐트·슬롯, 슬롯 채우기, 모호성 해소, 오류 복구/폴백, 컨텍스트 관리를 설계한다.
- 맞는 상황: 새 챗봇의 대화 아키텍처 설계 또는 기존 챗봇 대화 흐름 감사(막다른 길, 오류 처리 개선). 대상: 개발자, UX 라이터, PM.
- 맞지 않는 상황: 일반 산문/마케팅 글쓰기에는 맞지 않는다. 대화형 인터페이스(웹 위젯, Slack, WhatsApp, 음성) 설계 전용.
- 고유 접근: 불행한 경로를 먼저 설계하고 3단계 폴백(재질문, 선택지 제한, 사람 에스컬레이션)과 대화 상태 스택으로 모든 경로가 해결 또는 핸드오프로 끝나게 한다.
- 주 측면: structure
- 부 측면: voice, format
- 단계: draft
- 과제 종류: new, review
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: Botmock, Voiceflow, or Dialogflow CX for prototyping
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트: 특이사항 없음, 스크립트 없음. 입력으로 봇 목적, 대상 사용자, 지원 작업, 플랫폼 필요(없으면 요청 필요할 수 있음).
- 근거: structure "Design three tiers of fallback" / voice "Define the bot persona and scope." / format "Keep bot utterances under 3 sentences."

### citation-verification
- id: WM-X0030
- 출처: KalarisLabs/research-agent-skills `skills/citation-verification/SKILL.md` @ b0ee35a, MIT
- 역할: 참고문헌이 실제로 존재하고 메타데이터가 일치하는지 Crossref, OpenAlex, arXiv로 확인해 환각·손상·불일치 인용을 투고 전에 잡아내는 스킬.
- 맞는 상황: .bib 파일이나 참고문헌 목록 점검, AI가 인용을 작성한 뒤 검증, DOI가 엉뚱한 논문을 가리키는 경우, 누락 DOI 추가, camera-ready 직전.
- 맞지 않는 상황: 일부 항목은 자동 수정하지 않는다: mismatch, uncertain, not-found는 사용자 확인이 필요. 서지 형식·중복 정리는 bibtex-hygiene, 문헌 검색은 literature-review 등 다른 스킬.
- 고유 접근: 식별자가 해석되고 제목·제1저자·연도가 모두 일치해야 verified로 보고 verify_citations.py로 항목별 상태(verified, found-add-doi, mismatch, doi-not-found, uncertain, not-found)를 표로 보고한다.
- 주 측면: citation-check
- 부 측면: evidence, review-report
- 단계: check
- 과제 종류: new, edit, review
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: python3 >=3.9 (stdlib); network access to api.crossref.org, api.openalex.org, export.arxiv.org | 선택: CROSSREF_MAILTO env var (polite pool)
- 필수 명령: python3
- 상태 파일: references.bib; citation-report.json (--json)
- 주의: READY_WITH_LIMITS: 핵심 기능은 Crossref/OpenAlex/arXiv 외부 네트워크가 필요(스모크 테스트에서 미실행). API 키 불필요. 관련 스킬(bibtex-hygiene 등)은 참고용.
- 근거: citation-check "Never write a reference from memory." / evidence "Verify the claim too: open the abstract or the cited section" / review-report "Apply only mechanical fixes automatically"

### cold-email
- id: WM-X0125
- 출처: coreyhaines31/marketingskills `skills/cold-email/SKILL.md` @ 0cd9b3a, MIT
- 역할: B2B 콜드 아웃바운드의 이메일, 후속 시퀀스, 발송 설정, 링크드인, 멀티채널 케이던스, 답장 처리를 다룬다.
- 맞는 상황: 콜드 이메일, 아웃리치, 팔로업 시퀀스, 답장이 없을 때의 점검, 발송 도메인과 전달률 설정, 링크드인 메시지.
- 맞지 않는 상황: 리드 목록 구축과 계정 조사(prospecting), 라이프사이클 이메일(emails), 콜 스크립트와 세일즈 자료(sales-enablement), 랜딩 페이지 카피(copywriting).
- 고유 접근: 동료가 보낸 듯한 짧은 메일, 문제와 연결된 개인화, 질문 한 가지의 낮은 마찰 CTA를 원칙으로 하고, 보조 도메인, 목록 검증, 오픈 추적 끄기, 답장 시 전 채널 중단을 함께 요구한다.
- 주 측면: persuasion
- 부 측면: voice, prose-edit, hook, ai-tells, format, structure
- 단계: draft
- 과제 종류: new, edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: .agents/product-marketing.md 또는 .claude/product-marketing.md(있으면 읽음); 발송 도구(Instantly, lemlist 등은 외부 링크)
- 필수 명령: 없음
- 상태 파일: .agents/product-marketing.md 또는 .claude/product-marketing.md (읽기 전용, 있을 때만)
- 주의: 매니페스트: 선택적 product-marketing 파일은 조건부 사용자 데이터이지 스킬이 아님. 관련 스킬(prospecting, copywriting, emails 등)은 참고 언급일 뿐 미설치. 'Don't block on missing inputs' 이므로 비대화형. 영어 B2B 영업 메일 특화이며 한국어 일반 글에는 맞지 않는다. 엠대시 금지는 자체 규칙.
- 근거: persuasion "One CTA per email." / voice "Use contractions. Read it aloud." / prose-edit "If a sentence doesn't move the reader toward replying, cut it." / hook "Opening with "I hope this email finds you well"" / ai-tells "Contrast reveals ("It's not about X, it's about Y")" / format "2-4 words, lowercase, no punctuation tricks" / structure "Each follow-up should add something new"

### content-strategy
- id: WM-X0129
- 출처: coreyhaines31/marketingskills `skills/content-strategy/SKILL.md` @ 0cd9b3a, MIT
- 역할: 어떤 콘텐츠를 만들지 정하는 전략 스킬로 필러, 토픽 클러스터, 우선순위 점수, 캘린더 비율, 배포 계획을 만든다.
- 맞는 상황: 콘텐츠 전략, 무엇을 쓸지 모를 때, 블로그 주제, 에디토리얼 캘린더, 토픽 클러스터 계획.
- 맞지 않는 상황: 개별 글 작성(copywriting), SEO 기술 감사(seo-audit), 소셜 콘텐츠(social).
- 고유 접근: 모든 콘텐츠를 검색형 또는 공유형으로 나누고, 고객 인터뷰와 검색 데이터로 점수화(고객 영향 40%, 적합 30%, 검색 20%, 자원 10%)하며, 60/30/10 캘린더와 한 번 만들어 두 번 배포하는 원칙을 쓴다.
- 주 측면: topic-plan
- 부 측면: hook, evidence, format
- 단계: research
- 과제 종류: new, review
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: .agents/product-marketing.md 또는 .claude/product-marketing.md(있으면 읽음); 키워드 내보내기, 통화 녹취, 설문(사용자 제공 시); 웹 검색(포럼, 경쟁사 조사)
- 필수 명령: 없음
- 상태 파일: .agents/product-marketing.md 또는 .claude/product-marketing.md (읽기 전용, 있을 때만)
- 주의: 매니페스트: 조건부 product-marketing 파일, 관련 스킬(copywriting, seo-audit 등) 참고 언급만이며 requires 아님. 'ask if not provided' 방식이라 비대화형으로 판단. 출력은 글이 아니라 전략 문서다.
- 근거: topic-plan "Content pillars are the 3-5 core topics your brand will own." / hook "write **10 title options** before drafting" / evidence "Output content ideas with supporting quotes." / format "Every piece of content must be searchable, shareable, or both."

### context-engineering
- id: WM-X0059
- 출처: addyosmani/agent-skills `skills/context-engineering/SKILL.md` @ eb07f19, MIT
- 역할: 에이전트 세션의 컨텍스트(규칙 파일, 스펙, 소스, 오류 출력, 대화 이력)를 의도적으로 큐레이션해 출력 품질을 높이는 코딩 에이전트용 스킬이다.
- 맞는 상황: 새 세션 시작, 출력 품질 저하, 작업 전환, 프로젝트 규칙 파일(CLAUDE.md 등) 구성이 필요할 때.
- 맞지 않는 상황: 글 본문을 쓰거나 고치는 작업에는 맞지 않는다. 코딩 프로젝트의 에이전트 설정과 컨텍스트 관리용이다.
- 고유 접근: 컨텍스트를 규칙 파일부터 대화 이력까지 5단 계층으로 나누고, 75% 지점부터 압축하며, 모호함은 임의로 고르지 않고 선택지와 함께 사용자에게 드러내도록 한다.
- 주 측면: prompt
- 부 측면: intent
- 단계: draft
- 과제 종류: review, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: CLAUDE.md / AGENTS.md / .cursorrules 등 프로젝트 규칙 파일(프로젝트 루트)
- 주의: 매니페스트: sha_match false(원본 커밋과 파일 해시 불일치), 특이 제한 없음. 코딩 에이전트 컨텍스트 중심이라 글쓰기 오케스트레이션 적합도는 낮다. 판단: 단계: facts stage_hint는 clarify지만 규칙 파일은 저장소를 읽고 쓸 수 있어 draft로 둔다. 충돌하는 요구는 고르지 말고 사용자에게 올린다.
- 근거: prompt "Include only what is relevant to the current task." / intent "Don't invent requirements — that's the human's job"

### copywriting
- id: WM-X0131
- 출처: coreyhaines31/marketingskills `skills/copywriting/SKILL.md` @ 0cd9b3a, MIT
- 역할: 홈페이지, 랜딩, 가격, 기능, 소개 페이지의 마케팅 카피를 쓰거나 고친다. 입력 상황(공백, 실제 목소리, 부분 수정)을 먼저 진단해 변경 범위를 정한다.
- 맞는 상황: '카피 써줘', '이 카피 개선', 헤드라인, CTA, 가치 제안, 'AI 같다/사람처럼' 요청.
- 맞지 않는 상황: 이메일 카피(emails), 팝업(popups), 기존 카피 편집(copy-editing), 보너스와 보증 같은 오퍼 설계(offers).
- 고유 접근: 상황 진단(A 공백, B 목소리 보존, C 부분 수정) 후 단위별로 후보를 만들어 고정하고, 세 질문 게이트와 AI 티 금지 목록으로 검증하며, 근거 없는 주장은 거절하고 해제 조건을 명시한다.
- 주 측면: persuasion, structure
- 부 측면: prose-edit, ai-tells, evidence, format
- 단계: draft
- 과제 종류: new, edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: .agents/product-marketing.md 또는 .claude/product-marketing.md(있으면 읽음); references/ai-tells.md, copy-frameworks.md, natural-transitions.md(스킬 폴더 내)
- 필수 명령: 없음
- 상태 파일: .agents/product-marketing.md 또는 .claude/product-marketing.md (읽기 전용, 있을 때만)
- 주의: 매니페스트: 조건부 product-marketing 파일, 관련 스킬(copy-editing, cro, emails, popups, ab-testing)은 참고 언급만이며 미설치. 영어 마케팅 페이지 중심. 자체 AI 티 금지 규칙은 부 측면(ai-tells)으로 두어, humanizer·prose-naturalizer 같은 ai-tells 주 소유자와 조합되면 그쪽 규칙을 따른다.
- 근거: persuasion "[Action Verb] + [What They Get] + [Qualifier if needed]" / structure "Each section should advance one argument. Build a logical flow down the page." / prose-edit "If you have to choose between clear and creative, choose clear." / ai-tells ""It's not X, it's Y." "Not because X. Because Y." "Not just X, but Y." State Y directly, with the reason." / evidence "flag missing proof as `[NEED: ...]` rather than inventing it." / format "For headlines and CTAs, provide 2-3 options:"

### crafting-effective-readmes
- id: WM-X0374
- 출처: softaworks/agent-toolkit `skills/crafting-effective-readmes/SKILL.md` @ 3027f20, MIT
- 역할: 독자와 프로젝트 유형(OSS, 개인, 사내, 설정 폴더)에 맞춰 README를 새로 쓰거나 고치거나 점검하도록 템플릿과 지침을 제공한다.
- 맞는 상황: README 작성, 개선, 갱신, 정확성 검토.
- 맞지 않는 상황: README 이외의 일반 산문 품질 조정(그쪽은 writing-clearly-and-concisely를 참조하라고 함).
- 고유 접근: 먼저 독자가 누구이고 무엇을 알아야 하는지 묻고, 작업 종류별 질문과 유형별 템플릿(templates/)으로 섹션을 맞춘다.
- 주 측면: structure
- 부 측면: intent, evidence
- 단계: draft
- 과제 종류: new, edit, review, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: templates/oss.md, personal.md, internal.md, xdg-config.md; section-checklist.md, style-guide.md, using-references.md
- 필수 명령: 없음
- 상태 파일: README.md (프로젝트 루트)
- 주의: 매니페스트: sha_match true, 상대 참조(templates/*.md 등) 전부 해석됨. writing-clearly-and-concisely는 산문용 참조 안내일 뿐 requires가 아니며 미설치. 프로젝트 유형이 불분명하면 사용자에게 묻도록 되어 있으나 필수 인터뷰는 아니라고 판단.
- 근거: structure "Every README needs at minimum:" / intent "Who will read this, and what do they need to know?" / evidence "Check against actual project state (package.json, main files, etc.)"

### create-implementation-plan
- id: WM-X0203
- 출처: github/awesome-copilot `skills/create-implementation-plan/SKILL.md` @ b6483db, MIT
- 역할: 신규 기능, 리팩터링, 패키지 업그레이드, 설계·인프라 작업을 위한 기계 판독 가능한 구현 계획 파일(/plan/*.md)을 만든다.
- 맞는 상황: AI 에이전트나 사람이 해석 없이 실행할 수 있는 결정적 구현 계획 문서가 필요할 때.
- 맞지 않는 상황: 원문에 명시된 제외 대상은 없음. 설명형 산문이나 요구사항 명세(create-specification 영역)에는 맞지 않는다.
- 고유 접근: REQ-/TASK-/GOAL- 같은 고유 접두 식별자, 고정 템플릿, 단계별 측정 가능한 완료 기준, grep 기반 식별자 중복 검사로 자동 실행 가능성을 강제한다.
- 주 측면: structure, format
- 부 측면: prose-edit
- 단계: draft
- 과제 종류: new, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: plan purpose (${input:PlanPurpose} placeholder in SKILL.md) | 선택: POSIX shell with grep, sed, sort, uniq for identifier uniqueness check
- 필수 명령: 없음
- 상태 파일: /plan/[purpose]-[component]-[version].md (output)
- 주의: SKILL.md에 ${input:PlanPurpose} 같은 VS Code Copilot식 플레이스홀더가 있다. 출력은 AI-to-AI 소비용 기계 판독 문서로 사람 대상 산문 글쓰기와 결이 다르다. 매니페스트상 이슈 없음(READY). 판단: grep·sed·sort·uniq는 식별자 중복 검사용 선택 도구라 필수 명령에서 뺐다.
- 근거: structure "Plans must consist of discrete, atomic phases containing executable tasks." / format "All implementation plans must strictly adhere to the following template." / prose-edit "Use explicit, unambiguous language with zero interpretation required"

### create-specification
- id: WM-X0205
- 출처: github/awesome-copilot `skills/create-specification/SKILL.md` @ b6483db, MIT
- 역할: 솔루션 구성요소의 요구사항, 제약, 인터페이스를 생성형 AI가 쓰기 좋게 정의하는 명세 파일(/spec/spec-*.md)을 만든다.
- 맞는 상황: 명확하고 모호하지 않으며 자기완결적인 AI 소비용 명세 문서가 필요할 때.
- 맞지 않는 상황: 원문에 명시된 제외 대상은 없음. 구현 단계 계획(create-implementation-plan)이나 일반 설명 산문에는 맞지 않는다.
- 고유 접근: 11개 섹션 고정 템플릿과 REQ/SEC/CON/GUD/PAT/AC 식별자, Given-When-Then 수용 기준, 'what not how' 의존성 서술을 요구한다.
- 주 측면: structure, format
- 부 측면: prose-edit, prompt
- 단계: draft
- 과제 종류: new, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: specification purpose (${input:SpecPurpose} placeholder) | 선택: 없음
- 필수 명령: 없음
- 상태 파일: /spec/spec-[a-z0-9-]+.md (output)
- 주의: SKILL.md에 ${input:SpecPurpose} 플레이스홀더가 그대로 남아 있다(VS Code Copilot 문법). 템플릿 테스트 섹션 예시가 .NET(MSTest 등)에 치우쳐 있다. 산출물은 AI 소비용 기계 판독 명세이므로 사람용 산문 규칙과 충돌할 수 있다.
- 근거: structure "Clearly distinguish between requirements, constraints, and recommendations." / format "The specification should be saved in the `/spec/` directory" / prose-edit "Avoid idioms, metaphors, or context-dependent references." / prompt "Use precise, explicit, and unambiguous language."

### data-storytelling
- id: WM-X0394
- 출처: wshobson/agents `plugins/business-analytics/skills/data-storytelling/SKILL.md` @ 0874a27, MIT
- 역할: 분석 데이터를 시각화, 맥락, 설득 구조로 풀어 이해관계자용 내러티브(보고서, 발표)로 바꾸는 스킬.
- 맞는 상황: 경영진 분석 발표, 분기 사업 리뷰, 투자자 발표, 데이터 기반 보고서, 비전문가 대상 인사이트 전달, 데이터 기반 제안.
- 맞지 않는 상황: 원문에 명시된 제외 대상 없음. 평이한 기술 문서(technical-writing)와는 설득 중심 구조에서 상충할 수 있다.
- 고유 접근: Setup-Conflict-Resolution 내러티브 아크, 데이터/내러티브/시각화 세 기둥, '[구체 숫자]+[사업 영향]+[실행 맥락]' 헤드라인 공식, 인사이트 선두 배치.
- 주 측면: structure
- 부 측면: hook, persuasion, evidence, prose-edit, ai-tells
- 단계: draft
- 과제 종류: new, edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: references/details.md (worked examples, templates)
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트 notes: 해당 플러그인 경로만 sparse checkout. 설명 문구가 'compelling', 'persuasive'를 지향하므로 평이한 기술 문체(technical-writing)와 어조 충돌 가능. references/details.md의 헤드라인 예시는 극적 어조(예: 'We're Losing $2.4M...'). 판단: 'rule of three' 권장은 humanizer·technical-writing 등이 금지하는 패턴이다. ai-tells 주 소유자와 조합되면 그쪽을 따른다.
- 근거: structure "Setup → Conflict → Resolution" / hook "Hook: Grab attention with surprising insight" / persuasion "**End with action** - Clear next steps" / evidence "Acknowledge limitations:" / prose-edit "**Don't use jargon** - Match audience vocabulary" / ai-tells "**Use the rule of three** - Three points, three comparisons"

### doc-coauthoring
- id: WM-X0111
- 출처: plugin anthropic-skills (anthropics/skills skills/doc-coauthoring/SKILL.md) @ca45fc4, license: see anthropics/skills repo (not checked)
- 역할: 문서(스펙, 제안서, 결정 문서 등)를 컨텍스트 수집, 섹션별 구조화/정제, 독자 테스트의 3단계로 사용자와 함께 공동 집필하는 워크플로 스킬.
- 맞는 상황: 문서 작성, 제안서, 기술 스펙, 결정 문서, PRD, RFC 등 구조화된 문서를 사용자와 협업해 쓰는 실질적 집필 과제.
- 맞지 않는 상황: 사용자가 거절하면 자유 형식으로 진행(워크플로 강요 안 함). 짧은 단발 글쓰기에는 과함.
- 고유 접근: 사용자 컨텍스트 덤프 후 5-10개 질문, 섹션마다 5-20개 선택지를 브레인스토밍하고 사용자가 유지/삭제/병합을 고르는 방식, 맥락 없는 새 Claude(서브에이전트)로 독자 테스트.
- 주 측면: intent, structure
- 부 측면: ai-tells, prose-edit
- 단계: clarify
- 과제 종류: new, edit, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: Slack/Drive 등 연동(있으면 컨텍스트 수집에 사용); sub-agent tool (Reader Testing in Claude Code); artifact create_file or markdown file in working directory
- 필수 명령: 없음
- 상태 파일: markdown scaffold file in working directory (e.g. decision-doc.md, technical-spec.md) or artifact
- 주의: 매니페스트 notes: anthropic-skills:doc-coauthoring로 이미 사용 가능, 플러그인 사본과 동일(중복 설치 안 함). 라이선스 미확인. 사용자와의 다회 상호작용이 전제이며 서브에이전트 없으면 사용자가 수동으로 독자 테스트를 해야 한다. 판단: 단계: 사용자와 여러 번 주고받는 공동 집필 워크플로(질문 5-10개, 큐레이션)라 사용자 없이 핵심 산출물이 나오지 않는다. clarify만 두어 조합에는 넣지 않는다.
- 근거: intent "What type of document is this?" / structure "Summary sections are best left for last." / ai-tells "Anything that feels like "slop" or generic filler" / prose-edit "Whether every sentence carries weight"

### docs-sync-audit
- id: WM-X0207
- 출처: github/awesome-copilot `skills/docs-sync-audit/SKILL.md` @ b6483db, MIT
- 역할: 문서가 코드, 설정, API, 명령, 예제와 어긋나는지 읽기 전용으로 감사하고 P0-P3 심각도와 path:line 근거가 달린 보고서를 낸다.
- 맞는 상황: 기능, PR, 브랜치, API, 설정, CLI 변경 뒤 README나 가이드나 changelog가 낡았는지 확인할 때.
- 맞지 않는 상황: 일반 코드 리뷰는 아니다. 원문: 'This is not a general code review'. 사용자가 요청하기 전에는 문서를 고치지 않는다.
- 고유 접근: docs가 주장하는 바와 코드가 하는 일을 대조하고, 양쪽 근거를 모두 인용하며, 확인된 drift와 추정 gap을 구분하고, 번들 docs_drift.py로 확정 가능한 불일치를 먼저 찾는다.
- 주 측면: evidence
- 부 측면: review-report
- 단계: check
- 과제 종류: review, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: python3 (stdlib only) for bundled scripts/docs_drift.py (python if python3 absent) | 선택: git (git status, diff base)
- 필수 명령: python3
- 상태 파일: scripts/docs_drift.py in skill dir (read-only checker)
- 주의: 매니페스트: READY, docs_drift.py는 실리포에 읽기 전용 실행 후 8개 발견 보고로 확인. 스크립트는 npm run/make 대상, 상대 링크, 환경변수명만 검사하고 산문은 판단하지 않는다. 문서 작성용이 아니라 점검용(stage check). 사용자 요청 시에만 'Post-Audit Update Workflow'로 문서를 고친다. docs 작업에서도 'Avoid creating docs during the audit phase'. 판단: git은 diff 기준을 잡을 때만 쓰는 선택 도구라 필수 명령에서 뺐다.
- 근거: evidence "Ground every finding in both sides of the mismatch" / review-report "Use this structure unless the user asks otherwise:"

### documenting-contracts
- id: WM-X0304
- 출처: riekelt/technical-writer `plugins/technical-writer/skills/documenting-contracts/SKILL.md` @ 85e5372, MIT
- 역할: HTTP API, 메시지 페이로드, 큐 계약, DTO, 파일 포맷, 웹훅 같은 기계 인터페이스를 호출자용 계약 문서로 쓰는 스킬. 네 가지 상세 수준과 DTO 카탈로그 구조를 강제한다.
- 맞는 상황: 호출자가 필드 의미나 에러를 반복해서 묻는 API, 메시지, 웹훅, CLI 명령, 파일 포맷 문서화, 레거시 캠페인의 api-reference.
- 맞지 않는 상황: 내부 코드 인터페이스, 설정 레퍼런스(config-reference), 계약 설계의 좋고 나쁨 평가.
- 고유 접근: 인덱스/시맨틱스/형태/예시 네 수준에 각각 한 곳만 두고, DTO를 와이어 타입과 Source 줄로 한 번만 정의하며, 생성된 OpenAPI 스펙이 있으면 필드 표를 스펙에 맡기고 생략 대 null 의미를 명시한다.
- 주 측면: structure
- 부 측면: evidence, tech-docs
- 단계: draft
- 과제 종류: new, edit, docs
- 묶음: technical-writer
- 필수 동반: technical-writing
- 금지 짝: 없음
- 실행 요건: 필수: technical-writing skill (hard rules, truth rules, style) | 선택: OpenAPI/AsyncAPI spec when one exists; documenting-legacy-codebases (not installed, informational)
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트 notes: documenting-legacy-codebases 교차 참조는 미설치(정보성). 소스 코드의 직렬화 설정과 DTO를 읽어야 정확한 문서가 나온다.
- 근거: structure "Each level has its own home" / evidence "**Verify against the serializer, not the class.**" / tech-docs "never hand-maintain field tables beside a generated one; a second home drifts." / technical-writing "**REQUIRED BACKGROUND:** the `technical-writing` skill"

### evidence-synthesis
- id: WM-X0101
- 출처: anayy09/claude-research-skills `evidence-synthesis/SKILL.md` @ f0d3359, MIT
- 역할: 체계적/스코핑/신속/엄브렐라 등 공식 근거 종합(evidence synthesis)을 프로토콜, 검색, 스크리닝 로그, 편향 위험 평가, GRADE, PRISMA 보고까지 연구 설계로 수행하는 스킬.
- 맞는 상황: 프로토콜·스크리닝 로그·평가 도구·보고 지침이 필요한 리뷰 논문(systematic review, scoping review, meta-analysis, PRISMA flow, risk of bias, GRADE)과 리뷰 방법론에 대한 심사자 지적 대응.
- 맞지 않는 상황: 관련 연구(related-work) 섹션, 문헌 훑기, 참고문헌 감사, reference diet는 investigating-sources 담당이다.
- 고유 접근: 리뷰를 읽기 연습이 아닌 연구 설계로 보고, 검색식을 한 번 정의해 여러 DB 문법으로 렌더링하며 스크리닝 결정을 로그로 남겨 PRISMA 흐름도 숫자를 로그에서 도출해 정합성을 검사한다.
- 주 측면: evidence, academic
- 부 측면: citation-check
- 단계: clarify, research
- 과제 종류: new, review
- 묶음: research-skills
- 필수 동반: investigating-sources
- 금지 짝: 없음
- 실행 요건: 필수: python3; investigating-sources/scripts/check_citations.py (verify_citations.py shim delegates to it) | 선택: web search / scholarly MCP connectors for SEARCH; requests (live DOI checks); network
- 필수 명령: python3
- 상태 파일: search.yaml; screening log (screening_log.py); sources.json (--write-log)
- 주의: READY_WITH_LIMITS: 검색 단계는 web search/scholarly MCP가 유리하고 실시간 DOI 확인은 네트워크 필요. 두 번째 사람이 하는 스크리닝은 사용자가 직접 수행해야 하므로 단일 대화로 리뷰를 완성하지 않는다. 형제 스킬(manuscript-writing 등) 인계는 제안일 뿐 필수 아님. requires는 판단: 원문이 인용 검증을 investigating-sources의 check_citations.py에 위임한다고 명시(zip에 사본 포함, 설치본은 형제 경로로 탐색). interactive는 판단: 사용자가 스크리닝을 해야 한다고 명시. 판단: 단계: 두 번째 스크리닝은 사용자가 직접 해야 하므로 clarify를 함께 둔다. 프로토콜·검색 설계는 research로 조합에 들어갈 수 있다.
- 근거: evidence "Report certainty per outcome, not for the review as a whole." / academic "The type determines the protocol, the reporting guideline, the appraisal tool," / citation-check "A citation you cannot confirm does not go in the document." / investigating-sources "Citation verification is delegated to the collection's one checker, `check_citations.py` in"

### general-writing
- id: WM-X0282
- 출처: msimchowitz/writing-skills `for-agents/general-writing/SKILL.md` @ 214981f, MIT
- 역할: 작가의 의미와 목소리를 보존하면서 초안을 더 명확하고 사람다운 산문으로 편집하거나, 편집 없이 AI 슬롭 패턴만 감사한다.
- 맞는 상황: 일반 글쓰기, 라인 편집, 명료성·목소리 수정, 간결화, AI 같은 문장 점검, AI 작성 여부 탐지 요청.
- 맞지 않는 상황: 초안 없이 새로 쓰기(초안을 먼저 요청), 사실·주장·통계 창작, 독자용 human-writing-guide 디렉터리 로드(에이전트 컨텍스트에 넣지 말라고 명시).
- 고유 접근: Humanizer를 임베디드 모드로 먼저 돌린 뒤 이 스킬을 최종 하우스 스타일 패스로 적용하고, eval.md 체크리스트로 직접 검증한다. 탐지 요청에는 패턴명과 인용만 반환한다.
- 주 측면: prose-edit, ai-tells
- 부 측면: flow, evidence, voice, format
- 단계: prose
- 과제 종류: new, edit, review, docs
- 묶음: msimchowitz
- 필수 동반: humanizer
- 금지 짝: 없음
- 실행 요건: 필수: 편집할 초안 (없으면 요청) | 선택: 작가의 글쓰기 샘플(Humanizer 보정용); 대상 독자와 게재 매체
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트 노트: ../../for-humans/human-writing-guide/ 를 참조하나 이는 사람용 가이드라 미설치이며 로드하지 말라고 명시됨. 형제 스킬(abstract-writing, academic-voice, humanizer 등)은 ~/.claude/skills에서 해석된다. 초안이 없으면 먼저 요청해야 하므로 단독 호출 시 입력 확인 필요. Humanizer 안에서 better-usage, academic-voice, writing-cadence, non-autoregressive-writing-pass가 이미 적용되므로 중복 실행 금지.
- 근거: prose-edit "Make the minimum effective edit." / ai-tells "Ban these unless quoted or technically necessary: delve, foster, leverage" / flow "Do not treat display text as metadata." / evidence "Do not invent claims, examples, statistics, quotations, or opinions." / voice "**Preserve the writer's real voice.**" / format "return the full edited draft plus a short **What changed** section." / humanizer "For editing requests, read the sibling [Humanizer skill](../humanizer/SKILL.md) and invoke it in embedded"

### genre-craft
- id: companion
- 출처: danjdewhurst/story-skills `skills/genre-craft/SKILL.md` @ e44c97c, MIT
- 역할: 장르별 구조 팩(미스터리 페어플레이·단서 원장, 로맨스 비트·HEA, 스릴러 시한, 호러, MG/YA, SF, 판타지, 역사, 코미디, 연재)을 점검 가능한 규칙·원장·감사로 적용한다.
- 맞는 상황: 지원 장르로 이야기를 시작하거나 재분류할 때, 단서·시계·시즌 목표 같은 장르의 하중 요소를 계획할 때, 초고를 장르 계약에 맞춰 감사할 때.
- 맞지 않는 상황: 퇴고 패스로서의 단서 점검은 revision-continuity, 줄 단위 장르 목소리는 better-writing 스킬의 장르 작업(구조 팩이 아님), 순문학은 팩으로 제공하지 않는다.
- 고유 접근: 장르 계약을 clue ledger(continuity/clues/), 약속 원장, season-goal·episode-question 같은 프런트매터 필드로 인코딩해 story clues·story pacing·story timeline으로 검증하고, 팩마다 끝에 감사 체크리스트를 둔다.
- 주 측면: fiction-genre
- 부 측면: continuity
- 단계: genre
- 과제 종류: new, review, docs
- 묶음: story-skills
- 필수 동반: story-init
- 금지 짝: 없음
- 실행 요건: 필수: story-init으로 만든 story 프로젝트와 story.md에 기록된 장르; 해당 팩 references/*.md | 선택: plot-structure 플롯 구조; story CLI 또는 번들 폴백 (add clue, clues, pacing, timeline, next, list); scene-craft, chapter-writing, worldbuilding, research, editorial-review, series-continuity(상황별 연계)
- 필수 명령: story, node
- 상태 파일: story.md (genre, sub-genre, season-goal, release-every, release-start, target-words, setting-era); continuity/clues/; continuity/promises/; worldbuilding/systems/; research/; chapters/*.md (episode-question, release-date, hook); style-sheet.md
- 주의: 매니페스트: 동반(companion) 스킬, READY_WITH_LIMITS. references/serial-episodic.md가 상대 경로 ../../../examples/the-left-luggage-office/ 를 링크하는데 ~/.claude/skills 기준으로는 해석되지 않는다(예시는 ~/.local/share/writing-maestro/vendor/danjdewhurst__story-skills/examples/ 에 있으며 포인터일 뿐). 원문에 언급된 better-writing 스킬은 별도 설치 대상이 아님. 순문학 팩 없음.
- 근거: fiction-genre "Multi-genre stories: load each applicable pack; where packs conflict" / continuity "Genre audits live in the revision plan or `continuity/` audit files" / story-init "A story project must already exist (created via the story-init skill) with"

### hook-writer
- id: WM-X0354
- 출처: social-media-skills/skills `skills/hook-writer/SKILL.md` @ f28cef2, MIT
- 역할: 소셜 콘텐츠(캡션 첫 줄, 영상 첫 3초, 캐러셀 커버, 스레드 첫 글, 유튜브 제목, 이메일 제목)의 훅(오프닝)을 쓰는 스킬.
- 맞는 상황: 캡션 첫 줄, 영상 첫 1~3초, 캐러셀 커버, 스레드 오프너, 유튜브 제목, 이메일 제목 등 주의를 끄는 오프닝 한 줄이 필요할 때.
- 맞지 않는 상황: 전체 캡션(caption-writer)이나 전체 영상 스크립트(영상 스킬)에는 쓰지 않는다. 오프닝 자체만 쓴다.
- 고유 접근: 콘텐츠에서 가장 놀랍거나 구체적인 요소를 뽑아 서로 다른 메커니즘으로 5~10개 후보를 만들고, 루브릭(Gap/Specificity/Truth/Fit/Voice/Pull)으로 채점해 1~2개만 남긴다. Truth와 Pull은 통과/탈락 게이트.
- 주 측면: hook
- 부 측면: evidence, format, voice
- 단계: genre
- 과제 종류: new, edit
- 묶음: social-media-skills
- 필수 동반: brand-profile, voice-builder
- 금지 짝: 없음
- 실행 요건: 필수: brand-profile.md and voice.md user files (produced by companions brand-profile / voice-builder) | 선택: caption-writer (not installed)
- 필수 명령: 없음
- 상태 파일: brand-profile.md (read; user project files, produced by brand-profile); voice.md (read; produced by voice-builder)
- 주의: 매니페스트 주석: Step 0에서 brand-profile.md/voice.md가 없으면 brand-profile(샘플이 있으면 voice-builder)을 먼저 실행하라고 함. 관련 스킬 caption-writer 등은 미설치. 판단: 필수 동반 brand-profile·voice-builder는 명확화 단계에서 만드는 파일(brand-profile.md, voice.md)을 읽는다는 뜻이다. 조합 구성원으로 넣지 않는다.
- 근거: hook "Write **5–10 candidate hooks**, deliberately using *different mechanisms*" / evidence "Hooks must be TRUE to the content that follows" / format "**Caption** — one line before the "…more" cutoff (~125 chars on Instagram)." / voice "A hook in the wrong voice still fails; the fingerprint" / brand-profile "Load `brand-profile.md` and `voice.md`." / voice-builder "`brand-profile` (and `voice-builder` if samples exist) first."

### humanizer
- id: companion
- 출처: msimchowitz/writing-skills `for-agents/humanizer/SKILL.md` @ 214981f, MIT
- 역할: AI가 쓴 듯한 문장 패턴(Wikipedia 'Signs of AI writing' 기반)을 감지해 제거하고 더 자연스러운 글로 다듬는다. general-writing이 임베디드 모드로 호출하는 동반 스킬.
- 맞는 상황: 텍스트를 더 자연스럽고 사람다운 글로 편집하거나 검토할 때, 파일 모드·임베디드 모드·붙여넣기 모드의 문서 워크플로 단계로.
- 맞지 않는 상황: 사실·이름·수치·날짜·인용 창작, 소스 코드·데이터·링크 대상 수정, 기술·법률·참고 문서에 의견이나 1인칭 주입, 인용문·제목·고유명사 속 패턴어 재작성.
- 고유 접근: 39개 패턴 카탈로그로 초안-감사-최종 루프를 돌리고, better-usage, academic-voice, writing-cadence, non-autoregressive-writing-pass 네 형제 스킬을 순서대로 적용하며 사실 창작을 결함으로 취급한다.
- 주 측면: ai-tells
- 부 측면: evidence, flow, voice
- 단계: prose
- 과제 종류: new, edit, review
- 묶음: msimchowitz
- 필수 동반: better-usage, academic-voice, writing-cadence, non-autoregressive-writing-pass
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: 사용자 글쓰기 샘플(보이스 보정)
- 필수 명령: 없음
- 상태 파일: scripts/validate-package.py (패키지 검증용, 출력에 무관)
- 주의: 매니페스트: 동반 스킬(companion), SHA가 선택 목록에 없어 현재 HEAD(214981f)를 설치, 자체 LICENSE 파일 있음. 요청된 필수 항목에 better-usage와 writing-cadence만 언급됐지만 원문 프로세스 3~6단계가 academic-voice와 non-autoregressive-writing-pass도 읽고 적용하라고 명시해 네 개 모두 requires에 기록. academic-voice는 학술·설명문일 때만 학술 레지스터를 쓰고, 캐주얼·법률·기술·개인 글은 저널 문체로 바꾸지 않는다. 임베디드 모드에서는 최종 텍스트만 출력. 판단: 동반 네 스킬은 humanizer가 스스로 순서대로 적용한다. 오케스트레이터가 따로 조합에 넣지 않는다.
- 근거: ai-tells "**Identify AI patterns** - Scan the complete artifact for the patterns listed below." / evidence "The rewrite must not contain any fact, name, number, date, quote, or citation that isn't in the source text." / flow "End where the reasoning arrives: on a supported consequence, boundary, unresolved tension, or concrete fact." / voice "A sample outranks this skill's style rules" / better-usage "Read and apply the sibling [better-usage skill](../better-usage/SKILL.md) to the draft." / academic-voice "Read and apply the sibling [academic-voice skill](../academic-voice/SKILL.md)." / writing-cadence "Read and apply the sibling [writing-cadence skill](../writing-cadence/SKILL.md) last." / non-autoregressive-writing-pass "Read and apply the sibling [non-autoregressive writing pass](../non-autoregressive-writing-pass/SKILL.md)"

### idea-refine
- id: WM-X0062
- 출처: addyosmani/agent-skills `skills/idea-refine/SKILL.md` @ eb07f19, MIT
- 역할: 막연한 아이디어를 발산-수렴 3단계 대화로 다듬어 문제 정의, 추천 방향, 가정, MVP 범위, Not Doing 목록이 든 마크다운 한 장짜리로 만든다.
- 맞는 상황: 아이디어가 아직 흐릿할 때, 계획 전에 가정을 검증하고 싶을 때, 하나로 좁히기 전에 선택지를 넓히고 싶을 때.
- 맞지 않는 상황: 원하는 바 자체를 모르는 사용자(interview-me로), 이미 방향이 정해져 스펙이 필요한 경우(spec-driven-development로).
- 고유 접근: How Might We 재진술, 3-5개 질문, 5-8개 변형을 렌즈별로 낸 뒤 가정을 명시적으로 드러내고, 정직하게 반박하며, Not Doing 목록으로 마무리한다.
- 주 측면: intent
- 부 측면: topic-plan, format
- 단계: clarify
- 과제 종류: new
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: AskUserQuestion 도구(사용자 질문 수집) | 선택: bash(scripts/idea-refine.sh로 docs/ideas 생성); frameworks.md, refinement-criteria.md, examples.md(스킬 폴더 내)
- 필수 명령: 없음
- 상태 파일: docs/ideas/[idea-name].md (사용자 확인 후 저장)
- 주의: 매니페스트: sha_match false. 스크립트는 cwd에 docs/ideas만 mkdir한다. 사용자 반응(Phase 1 이후)을 받아야 Phase 2로 넘어가는 대화형 스킬이다. 근거: 'Use the `AskUserQuestion` tool to gather this input. Do NOT proceed until you understand who this is for and what success looks like.' 이므로 interactive=true. 판단: bash는 docs/ideas 폴더를 만드는 선택 스크립트용이라 필수 명령에서 뺐다.
- 근거: intent "Ask 3-5 sharpening questions" / topic-plan "**Don't generate 20+ ideas.** Quality over quantity." / format "The final output is a markdown one-pager saved to `docs/ideas/[idea-name].md`"

### interview-me
- id: WM-X0063
- 출처: addyosmani/agent-skills `skills/interview-me/SKILL.md` @ eb07f19, MIT
- 역할: 가설과 신뢰도를 밝히고 한 번에 한 질문(추측 첨부)씩 던져 사용자가 실제로 원하는 바를 약 95% 확신까지 끌어내 확정된 의도 진술문을 만든다.
- 맞는 상황: 요청이 모호할 때(누구를 위해, 왜, 성공 기준, 제약이 빠짐), 사용자가 '인터뷰해줘'라고 할 때, 계획이나 코드 이전에 가정을 채우고 싶을 때.
- 맞지 않는 상황: 명확한 단일 요청(변수명 변경), 속도 우선 요청, 단순 정보 질문, 기계적 작업. 비대화형 환경(CI, 스케줄, /loop)에서는 쓰지 않는다.
- 고유 접근: 질문마다 에이전트의 추측을 붙이고, 다음 질문 3개에 대한 반응을 예측할 수 있을 때까지 진행하며, 'Out of scope'가 든 재진술에 명시적 yes를 받으면 즉시 턴을 멈춘다.
- 주 측면: intent
- 부 측면: format
- 단계: clarify
- 과제 종류: new, edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 실시간으로 응답하는 사용자(대화형 세션) | 선택: docs/intent/[topic].md 저장(사용자 확인 시)
- 필수 명령: 없음
- 상태 파일: docs/intent/[topic].md (사용자가 원할 때만)
- 주의: 매니페스트: sha_match true. 'This skill needs a live, responsive user. **Do not invoke in non-interactive contexts** like CI pipelines, scheduled runs, `/loop`, or autonomous-loop.' spec-driven-development, idea-refine 등은 선택적 후속 연계일 뿐 requires가 아니다(미설치). 확정 후 같은 턴에서 후속 작업을 시작하면 안 된다.
- 근거: intent "Ask one question at a time, each with a guess attached" / format "Including "Out of scope" is non-negotiable."

### investigating-sources
- id: WM-X0102
- 출처: anayy09/claude-research-skills `investigating-sources/SKILL.md` @ f0d3359, MIT
- 역할: 모든 사실 주장을 검증된 실제 출처로 추적하는 인용 정직형 리서치 보조: brief, report, lit-review, fact-check, verify, scope, related-work-table, reference-diet 모드.
- 맞는 상황: 주제 조사, 문헌 검토, 근거 종합, 팩트체크, DOI/출처 실존 확인, 주석 참고문헌, '출처 포함' 보고서, 모호한 질문을 답할 수 있는 질문으로 좁히기, 관련 연구 비교표, 참고문헌 수 줄이기.
- 맞지 않는 상황: 소설, 의견 칼럼, 출처가 핵심이 아닌 마케팅 카피. 프로토콜·스크리닝 로그·위험 평가가 필요한 공식 체계적 리뷰는 evidence-synthesis.
- 고유 접근: 7단계 척추(SCOPE-SEARCH-VERIFY-SYNTHESIZE-CHALLENGE-COMPOSE-AUDIT)와 check_citations.py/audit_report.py로 인용 실존을 Crossref/DataCite로 확인하고, 동료심사 문헌을 먼저 검색해 출판본을 인용한다.
- 주 측면: evidence
- 부 측면: citation-check, ai-tells, academic, prose-edit
- 단계: research
- 과제 종류: new, edit, review
- 묶음: research-skills
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: python3 | 선택: web_search / scholarly MCP connectors; requests (live DOI checks); network
- 필수 명령: python3
- 상태 파일: sources.json (source log)
- 주의: READY_WITH_LIMITS: 검색에 web_search/MCP, 실시간 인용 검증에 네트워크 필요(스크립트는 오프라인 폴백). interactive는 판단: 모드를 사용자에게 묻거나 추론하며 scope 모드만 반복 대화, 핵심 작업은 대화 없이 가능하여 false. related-work 서술 자체는 manuscript-writing(미설치)을 언급하지만 필수 아님.
- 근거: evidence "No unsupported factual assertions in a deliverable." / citation-check "if you cannot confirm a source exists, it is a FAIL" / ai-tells "Avoid the AI-tell patterns listed in" / academic "Include a short note that AI-assisted research tools were used" / prose-edit "Quotation is minimal; paraphrase in your own words and cite."

### line-editing
- id: WM-X0158
- 출처: danjdewhurst/story-skills `skills/line-editing/SKILL.md` @ e44c97c, MIT
- 역할: 구조가 확정된 뒤 초고 챕터에 문장 수준 품질 패스(라인 에디트, 인물 목소리 구분, 카피에디트, 소리 내어 읽기, 교정)를 적용한다. 모든 수정은 before/after와 한 줄 근거로 제안하고 작가의 목소리를 기준으로 삼는다.
- 맞는 상황: 챕터 구조가 확정되어 문장을 다듬어야 할 때, 모든 인물의 대사가 비슷하게 들릴 때, 베타 리더·편집자·투고용 원고를 준비할 때, story passes의 line/copyedit/proof 패스 차례일 때.
- 맞지 않는 상황: 구조·플롯·연속성 수정은 revision-continuity, 스타일시트·목소리 기록 작성은 voice-style, 딥 POV·서브텍스트 같은 장면 기법은 scene-craft, 외부 독자 노트 처리는 feedback-triage, 운문 작성·스캔은 verse-craft를 쓴다.
- 고유 접근: 수정마다 위치·범주·before/after·효과를 명시한 한 줄 근거를 달고 배치당 약 20개로 끊어 작가가 번호로 수락/거절하게 하며, story prose/voices/build 결과로 패스를 뒷받침한다.
- 주 측면: prose-edit, voice
- 부 측면: continuity, ai-tells
- 단계: prose
- 과제 종류: new, edit, review
- 묶음: story-skills
- 필수 동반: voice-style
- 금지 짝: 없음
- 실행 요건: 필수: story.md와 draft 이상 상태의 챕터가 있는 story 프로젝트; style-sheet.md(없거나 빈약하면 voice-style로 먼저 작성); story CLI 또는 번들 폴백 node ../story-maintenance/scripts/story.js (story CLI 부재 시 번들 폴백; story-maintenance 미설치면 CLI 없이 수동 점검) | 선택: TTS: macOS say, Linux espeak-ng/spd-say (설치 전 사용자 확인); PDF 엔진: Prince/WeasyPrint/pagedjs-cli/Chrome (story build --pdf); better-writing 스킬(반-상투 점검 보완); story-maintenance(conventions.md, 폴백 CLI)
- 필수 명령: story, node
- 상태 파일: story.md (language, pov, tense, revision-passes); style-sheet.md; chapters/*.md (## Chapter Text 아래 직접 편집); characters/*.md (voice-words, voice-avoid); dist/ (story build 산출물)
- 주의: 매니페스트: READY, 모든 상대 참조 해석됨. story CLI는 ~/.local/bin/story 셸 심 또는 번들 폴백으로 동작(v0.24.1 스모크 테스트 통과, bun 없어 테스트는 미실행). 원문 자체의 안내: 카피에디트는 인쇄 출판용 전문 교정자를 대체하지 못한다. 수정 위치 표기는 story build의 문단 앵커(ch03-p12)만 권위 있음. Bun/패키지 스크립트가 아니라 Node로 실행. 필터 워드 등 단어 목록 점검은 영어 전용. 판단: 필수 동반 voice-style은 style-sheet.md가 없거나 빈약할 때 먼저 만들라는 조건부 요구다. 단계: 수정마다 허락을 받지만 초안 서브에이전트가 제안 형식으로 낼 수 있어 prose로 둔다.
- 근거: prose-edit "Own the prose-quality passes that come after structure is settled" / voice "The author's voice wins." / continuity "A line edit does not change events, facts, or who knows what." / ai-tells "**Genericness.** Stock phrases (*a beat of silence*" / voice-style "it first with the `voice-style` skill, because the copyedit checks against"

### literature-review
- id: WM-X0287
- 출처: msimchowitz/writing-skills `for-agents/literature-review/SKILL.md` @ 214981f, MIT
- 역할: 추적 가능한 근거 기반으로 문헌 검토, 서베이, 관련 연구 종합을 조사·구조화·작성·검증한다.
- 맞는 상황: 연구 분야 지도 작성, 모델·방법 계보 비교, 학습 레시피 재구성, 근거 표 작성, 공개/미공개 세부 사항 식별, living review 유지, 인용된 문헌 검토 섹션이나 독립 LaTeX 보고서 작성.
- 맞지 않는 상황: 논문(IMRaD 본문) 작성 자체, 출처 없는 논문·수치·저자 창작, 순위표 점수를 학습 메커니즘의 근거로 쓰는 일.
- 고유 접근: review-plan 계약과 source ledger, claim-evidence matrix를 먼저 만들고 모든 근거를 reported/derived/inferred/conflicting/not-disclosed로 표시하며, 감사 스크립트와 LaTeX 빌드로 마무리한다.
- 주 측면: evidence, structure
- 부 측면: citation-check, academic, format, ai-tells
- 단계: research, draft
- 과제 종류: new, edit, review
- 묶음: msimchowitz
- 필수 동반: general-writing, paper-writing
- 금지 짝: 없음
- 실행 요건: 필수: python3 (stdlib only); LaTeX 리뷰 산출 시 latexmk | 선택: assets/review-plan.md, source-ledger.csv, claim-evidence-matrix.csv 복사본
- 필수 명령: python3
- 상태 파일: research/source-ledger.csv; research/claim-evidence-matrix.csv; review-plan.md (프로젝트 내); <review-name>-main.tex / <review-name>-main.pdf (프로젝트 루트); scripts/audit_review.py (스킬 번들, 프로젝트 루트에서 실행)
- 주의: 매니페스트: python3 stdlib만 사용, audit_review.py --help 스모크 통과. paper-writing 읽기는 논문/LaTeX 산출물일 때만 조건부, general-writing 실행은 주장·인용·구조 안정 후 마지막 단계. latexmk가 필요한 것은 LaTeX 빌드 시에만. 기준일과 검색 경계를 명시해야 한다. 판단: 필수 동반 paper-writing은 논문·LaTeX 산출물일 때만, general-writing은 주장·인용·구조가 안정된 뒤 마지막에 부른다. latexmk는 LaTeX 빌드 때만 필요해 선택 요건으로 옮겼다.
- 근거: evidence "label evidence as `reported`, `derived`, `inferred`, `conflicting`, or `not-disclosed`" / structure "state one synthesis claim;" / citation-check "Never invent papers, authors, dates, identifiers" / academic "Include a limitations section that names search boundaries" / format "Do not create a generic `main.tex`." / ai-tells "Avoid promotional release language." / general-writing "After claims, citations, and structure are stable, run the complete sibling" / paper-writing "For a research-paper or LaTeX deliverable, read the sibling [`paper-writing`](../paper-writing/SKILL.md) skill"

### non-autoregressive-writing-pass
- id: WM-X0288
- 출처: msimchowitz/writing-skills `for-agents/non-autoregressive-writing-pass/SKILL.md` @ 214981f, MIT
- 역할: 완성된 초안 전체를 아는 상태에서 제목, 부제, 소제목, 문단 머리, 문단 간 전환을 다시 쓰는 편집 패스.
- 맞는 상황: 표시 텍스트가 완성된 작업과 안 맞을 때, 도입이 평범하거나 갑작스러울 때, 문단들이 개별적으로는 명확하나 서로 쌓이지 않을 때, 완성된 초록의 첫 문장 보강, 문단 끝이 자연스럽게 닫히지 않을 때.
- 맞지 않는 상황: 주장·근거·문단 순서·전반 리듬이 아직 안정되지 않은 초안, 구조 개편 대체, 드래프팅 개요 용도.
- 고유 접근: 제목-머리 문장 척추를 따로 읽고 문단 끝과 다음 문단 첫 두 문장을 짝지어 관계(연속, 원인, 대조 등)를 명명한 뒤 고친다. 긍정 주장은 부정 프레임보다 먼저 제시한다.
- 주 측면: flow
- 부 측면: evidence, prose-edit
- 단계: prose
- 과제 종류: edit
- 묶음: msimchowitz
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 안정된 완성 초안 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트 이슈 없음(READY). 상태: 완성 초안 이후에 실행. forbids는 다른 스킬이 호출했을 때의 호출 경계 규칙. Humanizer 프로세스 6단계에서 이미 포함되어 호출되므로 humanizer와 중복 실행 금지. 판단: 원문의 'Do not invoke Humanizer …' 줄은 humanizer가 이 스킬을 부를 때 파이프라인을 다시 부르지 말라는 재귀 방지 규칙이라 금지 짝으로 적지 않았다. humanizer(general-writing 경유 포함)가 이미 이 스킬을 적용하므로 그런 조합에 따로 넣으면 중복이다.
- 근거: flow "Name their relation: continuation, cause, consequence, contrast" / evidence "Preserve facts, citations, qualifications, notation, examples, and deliberate voice." / prose-edit "Prefer lexical continuity and a clear logical relation to formulaic connectors"

### paper-writing
- id: WM-X0289
- 출처: msimchowitz/writing-skills `for-agents/paper-writing/SKILL.md` @ 214981f, MIT
- 역할: 기술 연구 논문을 주장, 표기, 근거, 인용, 저자 목소리를 보존하며 계획·작성·수정·구조화한다.
- 맞는 상황: 초록, 도입, 관련 연구, 방법, 이론, 실험, 결과, 논의, 결론, 그림, 부록, LaTeX 프로젝트 구성, 전체 원고 설계.
- 맞지 않는 상황: 인용·실험·정량 결과·정리 조건·신규성 주장의 창작, 사람용 human-writing-guide를 스킬처럼 라우팅하는 일, 문헌 조사 자체(literature-review 영역).
- 고유 접근: 주장-근거 지도와 paper-plan을 먼저 세우고 가장 강한 근거부터 바깥으로 쓰며, 마지막에 general-writing을 산문 집행자로 돌리고 본문 확정 후 초록을 재점검한다.
- 주 측면: structure, academic
- 부 측면: evidence, flow, prose-edit, voice, format
- 단계: draft
- 과제 종류: new, edit, docs
- 묶음: msimchowitz
- 필수 동반: academic-voice, general-writing, abstract-writing
- 금지 짝: humanizer
- 실행 요건: 필수: 없음 | 선택: 예시 논문 폴더(사용자에게 위치를 묻고 'none' 허용); LaTeX 툴체인(새 LaTeX 프로젝트일 때)
- 필수 명령: 없음
- 상태 파일: paper-plan.md (프로젝트에 복사); <project-name>-main.tex, body/, appendix/, preamble/, references.bib (LaTeX 스켈레톤); assets/ 아웃라인·figure-storyboard 템플릿
- 주의: 매니페스트: ../../for-humans/human-writing-guide/ 는 사람용이라 미설치이며 스킬처럼 라우팅하지 말라고 명시됨(없으면 번들 참조 사용). 형제 스킬 링크는 ~/.claude/skills에서 해석됨. 선택적 예시 논문 폴더는 런타임에 사용자에게 요청하며 저장소 상위나 홈에서 추측 탐색 금지. requires 중 abstract-writing은 초록만 요청일 때, academic-voice는 초록 외 드래프팅일 때, general-writing은 최종 음성 패스 때 조건부로 필요하다. Humanizer는 general-writing이 호출하므로 별도 실행 금지. 판단: 필수 동반 셋은 위 조건부 요구 그대로 근거에 원문 조건을 남겼다. humanizer 금지 짝은 원문이 직접 밝힌 실제 금지다.
- 근거: structure "Build a claim-evidence map." / academic "Use "shows" or "demonstrates" only for direct evidence" / evidence "Never invent citations, experiments, quantitative results" / flow "Prefer informative section titles that state the result or question." / prose-edit "Default to a declarative sentence with the main subject and verb near the front:" / voice "Use active first-person verbs: "we show,"" / format "Rename its `paper-main.tex` entry point" / academic-voice "For other drafting or revision of scholarly prose, read the sibling [academic-voice" / general-writing "Read the sibling [general-writing skill](../general-writing/SKILL.md) and its [evaluation" / abstract-writing "For an abstract-only request, read and follow the sibling [abstract-writing" / humanizer "It invokes Humanizer in embedded mode before applying the house-style check, so do not run Humanizer"

### plot-structure
- id: WM-X0159
- 출처: danjdewhurst/story-skills `skills/plot-structure/SKILL.md` @ e44c97c, MIT
- 역할: 스토리 아크, 플롯 포인트, 타임라인, 복선/회수(promise·clue·question) 기록, 책 단위 페이싱을 계획·관리하는 스킬.
- 맞는 상황: 플롯 아크 생성, 구조 모델 선택(3막·영웅의 여정 등), 스노플레이크, 타임라인, 복선 추적, 처지는 중반부와 페이싱, 챕터 beat/hook 계획.
- 맞지 않는 상황: 장면 결과와 챕터 훅의 장인 기법은 계획 단계까지만 다루고 scene-craft로, 퇴고 단계의 페이싱 점검은 revision-continuity로 보낸다.
- 고유 접근: 구조 모델을 장르에 맞춰 추천하고 아크 파일·beat·hook·outcome을 frontmatter로 기록하며, 각 복선은 하나의 소유 레코드(clue/promise/question)에만 기록하고 `story pacing`/`grid`로 점검한다.
- 주 측면: plot
- 부 측면: continuity
- 단계: draft
- 과제 종류: new, docs
- 묶음: story-skills
- 필수 동반: story-init
- 금지 짝: 없음
- 실행 요건: 필수: 기존 스토리 프로젝트(story.md 존재) | 선택: story CLI; characters/ 캐릭터 등록부
- 필수 명령: story, node
- 상태 파일: plot/_index.md (structure); plot/arcs/{arc}.md; plot/timeline.md; continuity/promises|clues|questions/{id}.md; chapters/ frontmatter (beat, hook); scenes/ frontmatter (outcome)
- 주의: Story Skills 번들 공통: `story` CLI(node>=18, npm 의존성 없음; bun 불필요)에 의존하며 manifest 상 상태 READY, 제한 없음. 상대 파일 참조는 모두 해결됨. 스토리 프로젝트(story.md 기준) 마크다운 폴더 구조와 YAML frontmatter 규칙을 따라야 하며, 소설 프로젝트 파일에 쓰는 스킬이므로 일반 산문/문서 작업에는 맞지 않음. 구조 재배치는 승인 필요. 분할/병합 절차는 revision-continuity의 Structural Edits를 따름. 판단: 단계: 원문은 대화로 아크를 만들고 재배치에 승인을 받지만, 아크 초안은 전제에서 제안할 수 있어 draft로 둔다(facts stage_hint는 clarify).
- 근거: plot "Recommend a structure based on genre (default to three-act if unclear)." / continuity "Each setup has exactly one record." / story-init "A story project must already exist (created via the story-init skill). Verify by checking for `story.md` in"

### premise-workshop
- id: WM-X0160
- 출처: danjdewhurst/story-skills `skills/premise-workshop/SKILL.md` @ e44c97c, MIT
- 역할: 프로젝트 생성 전에 불씨(이미지·what-if·인물·배경)를 what-if, 로그라인, premise/counter-premise, 이해관계, 형식, 제목, 비교 도서 점검으로 시험된 전제로 다듬고 story-init에 브리프로 넘기는 스킬.
- 맞는 상황: 이야기 아이디어 브레인스토밍, 전제 개발과 강도 점검, 로그라인 워크숍, 단편/중편/장편 형식 선택, 제목 아이디어 등 project 이전 단계.
- 맞지 않는 상황: 이미 쓴 책의 통제 아이디어·주제는 theme-craft, 프로젝트 폴더 생성은 story-init, 전제 확정 후 아웃라인은 plot-structure(또는 discovery-drafting), 투고용 비교 도서·피치·블러브는 submission.
- 고유 접근: 작가가 아이디어의 주인임을 전제로 옵션과 테스트만 제시(결정하지 않음)하며, 8-12개 what-if, 로그라인 스트레스 테스트(pass/weak/fail), 3단계 이해관계, 형식 추천, 제목 5개 숏리스트를 거쳐 한 화면 브리프로 story-init에 인계한다.
- 주 측면: premise
- 부 측면: intent, evidence
- 단계: clarify
- 과제 종류: new
- 묶음: story-skills
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: story CLI (프로젝트 생성 후 names/check 및 init 인계); 웹 검색(비교 도서 존재 검증; 없으면 unverified 표시); theme-craft/references/controlling-idea.md 와 story-init/references/title-logline.md 참조
- 필수 명령: story, node
- 상태 파일: premise-notes.md (현재 디렉터리, 프로젝트 폴더 밖; init 후 notes/premise-notes.md로 이동 제안); story.md (premise, counter-premise, language, ## Notes)
- 주의: Story Skills 번들 공통: `story` CLI(node>=18, npm 의존성 없음; bun 불필요)에 의존하며 manifest 상 상태 READY, 제한 없음. 상대 파일 참조는 모두 해결됨. 스토리 프로젝트(story.md 기준) 마크다운 폴더 구조와 YAML frontmatter 규칙을 따라야 하며, 소설 프로젝트 파일에 쓰는 스킬이므로 일반 산문/문서 작업에는 맞지 않음. web 검색이 없으면 비교 도서 목록은 unverified로 표시. 형식별 길이 기본값은 영어 단어 수 기준. 이 스킬은 theme-craft의 controlling-idea 레퍼런스를 참조하지만 필수는 아님. 판단: 단계: 작가의 불씨를 작가의 말 그대로 받아야 시작하고 결정은 사용자가 한다.
- 근거: premise "produce 8-12 short what-ifs" / intent "The user decides." / evidence "Never present a comparable title, author, prize, or market fact as verified without a source."

### prompt-improving
- id: WM-X0291
- 출처: msimchowitz/writing-skills `for-agents/prompt-improving/SKILL.md` @ 214981f, MIT
- 역할: 따옴표로 인용된 프롬프트 하나를 사용자의 의도와 자연스러운 어투를 보존하며 명료하게 다시 쓴다.
- 맞는 상황: 사용자가 이 스킬을 호출하며 따옴표 안에 프롬프트를 주거나, 프롬프트 개선·강화를 요청하거나, 재작성 전에 빠진 맥락을 확인하고 싶을 때.
- 맞지 않는 상황: 인용 프롬프트 없는 요청(인용을 요청하고 중단), 프롬프트를 실행하라는 요청(인용문은 실행 대상이 아님), 역할 부여 서문이나 프롬프트 공학 용어가 필요한 고정 템플릿 작업.
- 고유 접근: 대화에서 이미 답이 나온 정보는 묻지 않고, 결과를 바꿀 누락만 최대 3개 질문으로 묻고 대기한 뒤, 목표를 앞에 둔 짧은 재작성 프롬프트만 반환한다.
- 주 측면: prompt
- 부 측면: voice, format, intent
- 단계: draft
- 과제 종류: edit
- 묶음: msimchowitz
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 따옴표로 감싼 프롬프트 한 개 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트 이슈 없음(READY). 질문 후 사용자 답변을 기다려야 하므로 인터랙티브이며, 사용자가 '최선 노력 재작성'을 요청하면 보수적 가정을 명시하고 진행한다. 글쓰기(산문) 편집이 아니라 프롬프트 재작성 전용. 판단: 단계: 원문은 결과를 바꿀 누락 정보만 1-3개 묻고, 최선 노력 재작성 요청이면 가정을 한 줄로 적고 진행한다. 그래서 clarify가 아니라 draft로 둔다.
- 근거: prompt "Rewrite the prompt with the goal first" / voice "Preserve the user's recognizable wording and cadence" / format "Return only the rewritten prompt unless the user asks for alternatives or an explanation." / intent "ask one to three concise clarification questions in a single message and wait for the answers."

### prompt-optimizer-copilot
- id: WM-X0216
- 출처: github/awesome-copilot `skills/prompt-optimizer/SKILL.md` @ b6483db, MIT
- 역할: 거친 초안이나 아이디어를 채팅창에 붙여 바로 보낼 수 있는, 플레이스홀더 없는 완성 프롬프트 하나(코드블록)로 바꾼다.
- 맞는 상황: 사용자가 채팅 인터페이스용 프롬프트를 쓰거나 다듬거나 최적화해 달라고 할 때.
- 맞지 않는 상황: API용 프롬프트가 아니라 채팅 인터페이스용이다. 프롬프트가 아니라 직접 답을 원하는 요청에도 맞지 않는다.
- 고유 접근: '플레이스홀더 금지'와 '무엇을 줬든 완성본 제출' 두 하드 룰, 코드블록 하나만 출력하고 설명은 생략하며, 끝에 깊은 추론 유도 문장을 붙인다.
- 주 측면: prompt
- 부 측면: format
- 단계: draft
- 과제 종류: new, edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 원문 name은 prompt-optimizer이며 설치 시 prompt-optimizer-copilot으로 개명(사전 지정). 같은 계열의 prompt-optimizer-sentry와 대상이 겹친다(채팅용 일회성 프롬프트 vs 에이전트/시스템 프롬프트 eval 루프). 출력 형식이 '코드블록만'이라 다른 글쓰기 스킬의 설명·보고 규칙과 충돌 가능.
- 근거: prompt "State the task explicitly." / format "No text before the code block. No text after."

### prompt-optimizer-sentry
- id: WM-X0181
- 출처: getsentry/skills `skills/prompt-optimizer/SKILL.md` @ d12f250, Apache-2.0
- 역할: 에이전트 프롬프트, 시스템·개발자 프롬프트, 재사용 템플릿을 평가(eval) 기반으로 작성·개선·모델군 간 이식한다.
- 맞는 상황: 프롬프트 개선, 시스템 프롬프트 최적화, 문구 튜닝, 신뢰도 향상, OpenAI/Claude/Gemini 간 이식, 프롬프트 eval 설계를 요청받을 때.
- 맞지 않는 상황: SPEC의 제외 범위: 모델 구조 선택이나 파인튜닝, 프롬프트가 참조하는 문서 재작성, 재사용 에이전트 스킬 제작, 프롬프트와 무관한 코드 디버깅, 숨은 추론(chain-of-thought) 요청.
- 고유 접근: 계약 먼저 기록하고 eval 세트로 기준선을 잡아 실패를 원인별로 묶고 후보 2-4개를 같은 케이스로 비교해 홀드아웃으로 검증하며, 반복·절단·인과 없는 지시를 제거한다.
- 주 측면: prompt
- 부 측면: prose-edit
- 단계: draft
- 과제 종류: new, edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: references/core-patterns.md, model-family-notes.md, meta-optimization-loop.md, transformed-examples.md (task-dependent reads) | 선택: SOURCES.md provenance
- 필수 명령: 없음
- 상태 파일: references/*.md, SPEC.md, SOURCES.md (read-only)
- 주의: 원문 name은 prompt-optimizer이며 설치 시 prompt-optimizer-sentry로 개명(사전 지정). prompt-optimizer-copilot과 대상이 겹침(에이전트/시스템 프롬프트와 eval 루프 vs 일회성 채팅 프롬프트). eval 세트가 없으면 작은 세트부터 만들라고 하므로 데이터 확보가 필요할 수 있다. 출력은 8항목 패키지이다.
- 근거: prompt "Keep one owner per behavior rule." / prose-edit "Use the shortest wording that preserves the constraint."

### prose-naturalizer
- id: WM-X0105
- 출처: anayy09/claude-research-skills `prose-naturalizer/SKILL.md` @ f0d3359, MIT
- 역할: AI가 쓴 듯한 비학술 영문 산문을 내용은 유지한 채 작성자 목소리로 다듬는 스킬(Wikipedia 'Signs of AI writing' 기반).
- 맞는 상황: 블로그, 에세이, 문서, README, 이메일 등 비학술 글에서 not-X-but-Y 대비, 한 줄 마무리, 삼단 나열, 대시 남발, 과장, 영업 문구, 굵은 라벨 같은 AI 징후 제거.
- 맞지 않는 상황: 연구 원고, 학위논문, 응답서(response letter)에는 로드하지 않는다. manuscript-writing이 해당 패턴 부분집합과 자체 린트를 가지며 둘을 함께 로드하면 지시가 충돌한다.
- 고유 접근: AI 문체 패턴 25개를 강한 순서(§1-§25)로 번호 매겨 표시한 뒤 재작성하고, 재작성이 사실·수치·인용을 더하거나 잃지 않았는지 검사하며 글쓴이 샘플이 있으면 그 목소리를 우선한다.
- 주 측면: ai-tells
- 부 측면: voice, prose-edit, evidence, format
- 단계: prose
- 과제 종류: new, edit, review, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: manuscript-writing
- 실행 요건: 필수: 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: READY. 연구 원고/학위논문/응답서에는 쓰지 말 것. forbids는 설명문 그대로 manuscript-writing으로 기록(해당 스킬은 설치되어 있지 않을 수 있음). 영문 비학술 산문 대상이며 본문 규칙은 영어 표현 기준. 판단: 금지 짝 manuscript-writing은 설치되어 있지 않다. 연구 원고·학위논문·응답서에는 이 스킬을 쓰지 않는다.
- 근거: ai-tells "Ideas arrive in threes to sound complete" / voice "If the user gives a writing sample, read it first and match its sentence length" / prose-edit "Vary sentence length; real writing alternates short and long." / evidence "Do not add a fact, name, number, date, quote, or citation unless it comes from the source or the user." / format "Keep code blocks, inline code, commands, paths, YAML metadata, data, and link targets unchanged." / manuscript-writing "Do not load it for a research manuscript, thesis, or response letter"

### rebuttal-and-response-to-reviewers
- id: WM-X0044
- 출처: KalarisLabs/research-agent-skills `skills/rebuttal-and-response-to-reviewers/SKILL.md` @ b0ee35a, MIT
- 역할: 동료심사 리뷰에 대한 응답을 계획하고 작성하는 스킬: 저널 response letter, 학회 rebuttal(길이 제한), 메타리뷰 응답, 이의 제기.
- 맞는 상황: 리뷰를 받은 뒤 코멘트 분류(triage), 항목별 답변 초안, 추가 실험 결정, 정중한 반박, 수정 변경 로그 관리.
- 맞지 않는 상황: 남의 논문을 심사하는 경우(peer-review를 쓴다). 자기 원고에 대한 리뷰 응답에만 해당한다.
- 고유 접근: 리뷰를 원자적 코멘트로 쪼개 유형·노력·계획 표로 분류하고 점수를 좌우하는 2-3개 쟁점을 먼저 다루며, 실험과 원고 수정을 끝낸 뒤 변경 위치를 가리키는 답변을 쓴다.
- 주 측면: structure, academic
- 부 측면: voice, evidence
- 단계: draft
- 과제 종류: new
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: 없음
- 필수 명령: 없음
- 상태 파일: triage table / change log (manuscript section, page, line numbers)
- 주의: READY. 의존성 없음. Related skills(peer-review, scientific-writing 등)는 참고용. 실제 리뷰 텍스트와 수정본이 입력으로 필요하나 대화 인터뷰는 요구하지 않음.
- 근거: structure "Split every review into atomic comments and classify each in a table:" / academic "Lead with a short **general response** covering shared concerns and new results." / voice "Never be sarcastic, never say the reviewer "failed to understand"." / evidence "Never promise experiments you will not run."

### recording-decisions
- id: WM-X0306
- 출처: riekelt/technical-writer `plugins/technical-writer/skills/recording-decisions/SKILL.md` @ 85e5372, MIT
- 역할: 이미 내려진 결정을 ADR(Nygard 형식) 또는 경량 결정 로그 항목으로 기록하는 스킬. 추가 전용, 수락된 결정은 불변.
- 맞는 상황: 선택이 이미 이루어져 기록해야 할 때, '왜 이렇게 했는지 적어달라'는 요청, 기존 결정을 대체할 때, 채팅에만 남은 결정.
- 맞지 않는 상황: 아직 논쟁 중인 결정(writing-design-docs 영역).
- 고유 접근: Negative 결과 필드 필수, 대안마다 가장 강한 반대 논거 기록, append-only 규칙, 채팅은 영속 근거가 아니므로 커밋 후 인용.
- 주 측면: structure
- 부 측면: prose-edit, evidence, tech-docs
- 단계: draft
- 과제 종류: new, docs
- 묶음: technical-writer
- 필수 동반: technical-writing
- 금지 짝: 없음
- 실행 요건: 필수: technical-writing skill | 선택: 없음
- 필수 명령: 없음
- 상태 파일: ADR files / decision log (repository, append-only)
- 주의: 매니페스트 notes: technical-writing 필수 배경(설치됨). 결정자 이름을 모르면 fill-before-filing으로 표시해야 한다.
- 근거: structure "Nygard format. One decision per ADR." / prose-edit "Active voice: "We release on tags", not "it was decided that"." / evidence "A chat session is not a durable source." / tech-docs "Append-only. A wrong entry gets a new dated entry" / technical-writing "**REQUIRED BACKGROUND:** the `technical-writing` skill"

### requirements-clarity
- id: WM-X0384
- 출처: softaworks/agent-toolkit `skills/requirements-clarity/SKILL.md` @ 3027f20, MIT
- 역할: 모호한 요구사항을 100점 명확도 채점과 라운드별 질문으로 90점 이상까지 끌어올린 뒤 PRD 문서를 생성한다.
- 맞는 상황: 요구사항이 불명확하거나 기능이 크거나(2일 초과) 팀 간 조율이 필요한 구현 전 단계.
- 맞지 않는 상황: 파일 경로, 코드 조각, 기존 함수 언급이 있거나 재현 절차가 명확한 버그 수정.
- 고유 접근: 기능, 기술, 완성도, 비즈니스의 4개 항목으로 명확도를 점수화하고 라운드당 2-3개 질문으로 90점이 될 때까지 반복하며 PRD를 ./docs/prds/에 저장한다.
- 주 측면: intent
- 부 측면: format
- 단계: clarify
- 과제 종류: new, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 사용자 응답(라운드별 질의응답) | 선택: 없음
- 필수 명령: 없음
- 상태 파일: ./docs/prds/{feature_name}-v{version}-prd.md (없으면 ./docs/prds/ 생성)
- 주의: 매니페스트: sha_match true. 프로젝트에 PRD를 ./docs/prds/로 쓴다. 'Do NOT activate when' 조건(파일 경로, 코드 조각 등)이 있다. 코딩 기능 PRD 중심이라 글쓰기 과제에는 요구 정리 용도로만 맞다.
- 근거: intent "One category at a time (2-3 questions per round)" / format "**Final PRD**: `./docs/prds/{feature_name}-v{version}-prd.md`"

### research-grants
- id: WM-X0017
- 출처: K-Dense-AI/scientific-agent-skills `skills/research-grants/SKILL.md` @ 5f2bc03, MIT
- 역할: NSF, NIH, DOE, DARPA, 대만 NSTC의 연구비 제안서 작성·검토를 기관별 요건, 목표(aims), 심사 기준, 예산, broader impacts, 재제출까지 지원하는 스킬.
- 맞는 상황: 연구자가 직접 작성하는 제안서 개발, 준수 매트릭스(compliance matrix), 제안서 비평, specific aims와 project description 작성, 예산 정당화, 재제출 대응.
- 맞지 않는 상황: NIH는 AI가 실질적으로 작성한 신청서·섹션을 정책상 제외하므로 요건 확인, 비평, 일관성 점검, 연구자 작성 자료의 제한적 편집에만 쓴다. 허구의 데이터·인용·승인·파트너 확약 생성 금지.
- 고유 접근: 먼저 해당 공고(opportunity)의 식별자·마감·양식·평가 기준을 기록하고 요구사항-원문 섹션-초안 위치-격차 매트릭스를 만든 뒤에 준수 여부를 판단하며, 최종 내보낸 파일로 쪽수를 확인한다.
- 주 측면: academic, persuasion
- 부 측면: format, evidence, prose-edit, structure
- 단계: draft
- 과제 종류: new, edit, review
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: network access to verify agency instructions (or supplied dated official documents) | 선택: scientific-schematics skill + OPENROUTER_API_KEY (figures)
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: READY. 선택적 도식 생성은 scientific-schematics(미설치)와 OPENROUTER_API_KEY 필요하며 프롬프트가 제3자 API(OpenRouter)로 전송됨. 'Integration with Other Skills'는 참고용. 공식 패키지가 없으면 제한된 초안 검토만 하고 미해결 규칙을 나열.
- 근거: academic "For each task, record agency, opportunity identifier and amendment" / persuasion "Grants are persuasive documents" / format "Inspect the final exported files; Markdown text does not establish page compliance." / evidence "Never invent data, citations, investigator records" / prose-edit "**Excessive Jargon**: Inaccessible to broader review panel" / structure "Build a requirement -> source section -> draft location -> gap matrix"

### research-ideation
- id: WM-X0106
- 출처: anayy09/claude-research-skills `research-ideation/SKILL.md` @ f0d3359, MIT
- 역할: 사용자의 기존 연구 자산(논문, 코드, 데이터, 예비·부정 결과)에서 검증된 신규성 델타와 반증 가능한 주장, 제출까지의 실험 계획을 갖춘 순위화된 연구 방향을 만드는 연구 전략가 스킬.
- 맞는 상황: 다음에 무엇을 할지, 논문이 무엇을 주장해야 하는지, 기존 결과·실패 실험을 논문으로 바꾸는 법, 신규성 충분 여부, 학위/다논문 계획, 마감 대비 계획.
- 맞지 않는 상황: 문헌 검토 자체(evidence-synthesis, investigating-sources), 학술지 선택(journal-advisor), 완성된 원고 채점(submission-reviewer), 통계 계산, 논문 집필(manuscript-writing)은 범위 밖이다.
- 고유 접근: 자산 목록부터 만들고 20여 개 연산자로 후보를 생성해 실제 선행연구로 신규성을 확인한 뒤, 6차원 루브릭과 rank_ideas.py로 결정적으로 점수화하고 plan_timeline.py로 마감 역산 일정을 만든다.
- 주 측면: topic-plan
- 부 측면: evidence, format, ai-tells
- 단계: research
- 과제 종류: new, review
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: python3 (rank_ideas.py, plan_timeline.py) | 선택: web search / scholarly tools (novelty check)
- 필수 명령: python3
- 상태 파일: ideas.json
- 주의: READY_WITH_LIMITS: 신규성 검사에 web search/학술 도구 필요. 형제 스킬(manuscript-writing, journal-advisor 등) 인계는 제안일 뿐 필수 아님. interactive는 판단: 부족한 정보는 순위에 영향을 줄 때만 묻고 기본값을 가정해 진행하라고 하므로 false.
- 근거: topic-plan "Ideas are only as good as the assets they can stand on" / evidence "Search rather than recalling:" / format "Use the exact structure in `references/report-format.md`." / ai-tells "**No motivational framing.**"

### reviewing-technical-prose
- id: WM-X0307
- 출처: riekelt/technical-writer `plugins/technical-writer/skills/reviewing-technical-prose/SKILL.md` @ 85e5372, MIT
- 역할: 타인의 기술 문서를 검토/재작성하거나 문서 발송 전 최종 점검을 하는 스킬. 심각도 매핑, 발견 사항 형식, 플래그하지 말 목록, 납품 체크리스트를 제공한다.
- 맞는 상황: 타인의 기술 텍스트 리뷰나 재작성, 문서에 대한 리뷰 보고서 작성, 어떤 문서든 납품 직전 최종 확인.
- 맞지 않는 상황: 코드 리뷰(코드 안의 산문만 해당), 확정된 결정의 재논의, 범위 확장, 자기 취향으로의 재스타일링.
- 고유 접근: 이름 붙은 결함이 있을 때만 최소 수정한다. 재작성 시 사실을 더하거나 빼지 않고(통제 질문 3개), 주장 없는 문장은 삭제 후 [input wanted]로 표시한다.
- 주 측면: ai-tells, prose-edit
- 부 측면: review-report, evidence, tech-docs
- 단계: check, prose
- 과제 종류: edit, review, docs
- 묶음: technical-writer
- 필수 동반: technical-writing
- 금지 짝: 없음
- 실행 요건: 필수: technical-writing skill incl. references/style.md and references/truth.md | 선택: 없음
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트 notes: technical-writing의 references/style.md, truth.md를 형제 스킬 디렉터리에서 읽어야 한다(설치됨). 영어 금지 어휘 목록은 영어 전용. 판단: 단계: 검토 보고(check)와 내용 불변 재작성(prose)을 둘 다 한다.
- 근거: ai-tells "Which sentence still sounds like a language model?" / prose-edit "Rewriting natural or approved language without a named defect is itself a defect." / review-report "Verdict in the first line, findings ordered most severe first." / evidence "traces to a source named in the document" / tech-docs "**BLOCKER**: hard-rule violations (banned dashes, changelog sections, delivery history in prose)" / technical-writing "**REQUIRED BACKGROUND:** the `technical-writing` skill, including `references/style.md` (banned"

### revision-continuity
- id: companion
- 출처: danjdewhurst/story-skills `skills/revision-continuity/SKILL.md` @ e44c97c, MIT
- 역할: 기존 story 프로젝트를 연속성을 잃지 않고 개정한다. 이름 붙은 개정 패스 사다리(structure, character, theme, continuity, pacing, line, copyedit, proof), 연속성 감사, 발달 편집, 역개요, 분량 패스, 스냅샷, 챕터 이동·분할·병합을 다룬다.
- 맞는 상황: 챕터 수정, 연속성·타임라인·캐릭터 상태 감사, 발달 편집, 구조 개정, 서브플롯 삭제, 분량 맞춰 줄이기, 다음 개정 패스 결정.
- 맞지 않는 상황: 책 구조 계획은 plot-structure, 장면 수준 기법은 scene-craft, 목소리 일관성은 voice-style, 발견형으로 쓴 챕터의 정리는 discovery-drafting을 쓴다.
- 고유 접근: story passes 사다리와 pass-checklists.md로 큰 구조 변경을 문장 다듬기보다 먼저 하게 하고, 다챕터 패스 전에 스냅샷을 찍고, 컷·이동은 사용자 승인 후에만 하며, story continuity 결정적 검사 결과를 먼저 모은다.
- 주 측면: continuity
- 부 측면: review-report
- 단계: check, draft
- 과제 종류: edit, review, docs
- 묶음: story-skills
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: story.md가 있는 기존 story 프로젝트; story CLI 또는 번들 폴백 (reindex, wordcount, check, doctor, continuity, passes, compare, snapshot, move, split, merge) | 선택: git(스냅샷 태그); line-editing(line/copyedit/proof 패스 위임); plot-structure, scene-craft, series-continuity(story.md follows/precedes일 때), interactive-fiction(choices가 있는 분기 책); research 스킬(fact check 패스); story-maintenance(conventions.md, 폴백 CLI)
- 필수 명령: story, node
- 상태 파일: story.md (status, revision-passes, language, follows, precedes); chapters/_index.md; chapters/*.md; scenes/; continuity/state.md; continuity/exemptions.md; plot/timeline.md; arc 파일; references/pass-checklists.md; git 태그 또는 .snapshots/<name>/
- 주의: 매니페스트: 동반(companion) 스킬(submission이 pass-checklists.md를 링크), READY, 서포트 파일 없음. story snapshot --restore는 스냅샷에 없는 마크다운을 삭제하므로 --dry-run 후 승인 필요. git 커밋·태그는 사용자 승인 없이 하지 않는다. interactive는 계획 승인 대기와 패스 유형 확인 때문에 true로 판단함. 판단: 단계: 연속성 감사(check)와 개정 패스(draft)를 둘 다 한다. 계획 승인은 받지만 사용자 정보가 필요한 것은 아니라 clarify로 두지 않았다. git은 스냅샷 태그용 선택 도구.
- 근거: continuity "Run `story continuity .` first to collect the deterministic findings" / review-report "return findings ordered by severity with file references and concrete fixes."

### scene-craft
- id: WM-X0165
- 출처: danjdewhurst/story-skills `skills/scene-craft/SKILL.md` @ e44c97c, MIT
- 역할: 플롯 비트와 챕터 산문 사이의 장면 단위 기법을 다루는 스킬: scene/sequel, try/fail, 장면 카드, 대사 서브텍스트, 딥 POV·심리적 거리, 설명, 플래시백·시간 도약, 오프닝.
- 맞는 상황: 장면 구조 계획, 시퀄 장면, 대화 서브텍스트, 딥 POV, try/fail, 장면 카드, 설명·인포덤프, 플래시백·타임스킵, 소설/챕터 오프닝, 장면 outcome과 챕터 훅.
- 맞지 않는 상황: 책 단위 페이싱·막 구조는 plot-structure, 장면·챕터의 산문 집필은 chapter-writing.
- 고유 접근: 문제를 장면 단위 기법 레이어(8개 reference)로 진단해 해당 reference의 체크리스트와 계획 필드를 적용하고, outcome·sequel·date/time·hook을 장면 frontmatter에 기계가독 상태로 기록한다.
- 주 측면: scene
- 부 측면: plot, continuity
- 단계: draft
- 과제 종류: new, edit
- 묶음: story-skills
- 필수 동반: story-init, character-management, plot-structure
- 금지 짝: 없음
- 실행 요건: 필수: 기존 스토리 프로젝트(story.md); 정의된 캐릭터와 플롯 구조 | 선택: story CLI (pacing, prose, timeline)
- 필수 명령: story, node
- 상태 파일: scenes/chapter-NN-scene-NN.md (outcome, sequel, dilemma, flashback-to, date, time, travel-hours, state-changes); chapters/chapter-NN.md (hook); continuity/state.md; continuity/exemptions.md
- 주의: Story Skills 번들 공통: `story` CLI(node>=18, npm 의존성 없음; bun 불필요)에 의존하며 manifest 상 상태 READY, 제한 없음. 상대 파일 참조는 모두 해결됨. 스토리 프로젝트(story.md 기준) 마크다운 폴더 구조와 YAML frontmatter 규칙을 따라야 하며, 소설 프로젝트 파일에 쓰는 스킬이므로 일반 산문/문서 작업에는 맞지 않음. chapter-writing의 outline-first 워크플로를 대체하지 않고 확장. 딥 POV·대사 reference의 단어 목록은 영어 기준. 일부 날짜 있는 플래시백은 `timestamp runs backward` 경고가 나므로 exemptions.md에 기록. 판단: 원문은 필수 입력을 모르면 추측하지 말고 물으라고 한다(정본을 바꾸기 때문). 시안에서는 그 가정을 brief.md에 적고 사용자 확인 대상으로 남긴다.
- 근거: scene "Identify which scene-grain problem this is" / plot "Prefer the complicating `yes-but` and `no-and`" / continuity "All planning metadata (dilemma, decision, subtext wants, psychic-distance" / story-init "A story project must already exist (created via the story-init skill), with" / character-management "characters defined (character-management)" / plot-structure "a plot structure in place"

### scientific-writing
- id: WM-X0022
- 출처: K-Dense-AI/scientific-agent-skills `skills/scientific-writing/SKILL.md` @ 5f2bc03, MIT
- 역할: 과학 원고·보고서를 증거 출처 추적, 보고 지침 커버리지, 저자 책임, 기밀 통제, 로컬 일관성 검사와 함께 초안·수정·감사하는 스킬.
- 맞는 상황: 원고 섹션, 참고문헌, 선언문, 표·그림, 투고 준비에서 과학적 정확성과 추적 가능성이 중요한 경우.
- 맞지 않는 상황: 미공개 원고·심사 자료를 승인 없이 외부 서비스로 보내는 작업, 증거 없는 내용 채우기. 기존 LaTeX 템플릿은 제거되었고 서식은 Markdown 스캐폴드와 대상 학술지 템플릿으로 한다.
- 고유 접근: 초안 작성, 증거 검증, 투고 승인을 분리하고 모든 주장에 E/C ID를 붙여 사람 검증자가 원문을 열어 확인하게 하며 8개 로컬 CLI(scaffold, lint, audit_claims, check_consistency 등)로 fail-closed 점검한다.
- 주 측면: academic, evidence
- 부 측면: citation-check, format
- 단계: draft
- 과제 종류: new, edit, review
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: python3 >=3.11 (stdlib only, offline, no API keys) | 선택: 없음
- 필수 명령: python3
- 상태 파일: manuscript_manifest.json; source_manifest.json; claims.csv; consistency_manifest.json; authorship.json; reporting_coverage.json; draft-workspace/ (scaffold output)
- 주의: READY. 스크립트는 스킬 디렉터리 기준 상대 경로(python3 scripts/...)로 실행하고 python -I로 돌리면 형제 _common import가 깨진다. interactive는 판단: intake에서 정보를 얻거나 미해결로 표시하라고 하므로 false이나 사람 검증·승인 단계가 필요. 산출물은 submission_ready=false 상태로 시작하며 사람만 승인 가능.
- 근거: academic "Choose by actual design and article type, then open the current official statement," / evidence "Every factual or numeric manuscript claim must map to verified evidence IDs." / citation-check "Follow NLM *Citing Medicine* or the current official style" / format "provide alt text and redundant non-color cues;"

### short-form-video-script
- id: WM-X0362
- 출처: social-media-skills/skills `skills/short-form-video-script/SKILL.md` @ f28cef2, MIT
- 역할: 릴스/틱톡/쇼츠 등 세로형 숏폼 영상 스크립트(대사, 화면 텍스트, 비트/샷 지시, 훅 변형, CTA)를 시청 지속률 중심으로 쓰는 스킬.
- 맞는 상황: 숏폼 영상 스크립트, 훅·리텐션·페이싱·엔딩 루프, 음소거 자막, 초반 이탈 개선이 필요할 때.
- 맞지 않는 상황: 영상 생성(ai-video/veo-3/heygen), 기존 긴 영상 클리핑(captions-and-clipping), 긴 영상 스크립트/스토리보드(scripting-and-storyboarding)에는 쓰지 않는다. 사람이 촬영·편집하고 이 스킬은 스크립트만 쓴다.
- 고유 접근: WATCH 프레임워크(첫 3초, 오픈루프 아크, 음소거/유음 두 트랙, 약속 이행, 루프 엔딩+CTA)로 15~35초 3트랙 비트 스크립트를 쓴다. 음소거 버전을 먼저 쓰고 훅 5개 변형을 제시한다.
- 주 측면: structure, format
- 부 측면: hook, persuasion, evidence, voice
- 단계: draft
- 과제 종류: new
- 묶음: social-media-skills
- 필수 동반: brand-profile, voice-builder, hook-writer
- 금지 짝: 없음
- 실행 요건: 필수: brand-profile.md and voice.md user files | 선택: content-angle skill (storytelling/educational/data/listicle/contrarian) - pick-one category, not installed; reels-script, tiktok-script, youtube-shorts (not installed)
- 필수 명령: 없음
- 상태 파일: brand-profile.md (read); voice.md (read)
- 주의: 'Read these first' 항목의 content-angle 스킬은 미설치(카테고리 선택형). 플랫폼 스킬/게시(WoopSocial)는 범위 밖. 통계는 attribute+verify-quarterly. 네이티브 트렌딩 오디오·영상 생성은 하지 않음. 판단: 필수 동반 brand-profile·voice-builder는 명확화 단계 산출 파일을 읽는다는 뜻이고, hook-writer는 같은 묶음에서 훅 줄을 맡는다.
- 근거: structure "## The framework: WATCH" / format "~15–35s is the sweet spot (~75 words ≈ 30s)" / hook "Most striking frame first, no intro/logo/"hey" / persuasion "fitting ≈2s CTA tied to value" / evidence "**Never** fabricate a metric or guarantee virality" / voice "the voice the script speaks in." / brand-profile "1. **brand-profile** + **voice-builder** — the voice the script speaks in." / voice-builder "1. **brand-profile** + **voice-builder** — the voice the script speaks in." / hook-writer "and **hook-writer** for the hook line."

### story-init
- id: WM-X0167
- 출처: danjdewhurst/story-skills `skills/story-init/SKILL.md` @ e44c97c, MIT
- 역할: 새 소설 프로젝트의 마크다운 폴더 구조(story bible, 레지스트리, 장면 추적, 연속성 상태, 용어집, 플롯, 챕터 트래커)를 `story init`으로 초기화하는 스킬.
- 맞는 상황: 새 이야기·책·소설 프로젝트를 처음부터 시작하거나, 이미 있는 아이디어를 위한 폴더 구조를 세팅할 때.
- 맞지 않는 상황: 후속편·전편은 series-continuity, 아이디어 자체를 찾는 단계(막연한 구상, 전제 없음)는 premise-workshop을 먼저, 기존 원고 변환은 `story import`, 기존 스토리 프로젝트에 추가하는 작업은 각 도메인 스킬로 보낸다.
- 고유 접근: 제목·형식·장르·POV·시제·언어(BCP 47)를 묻고 `story init`을 홑따옴표 인자로 실행한 뒤 premise/counter-premise 가설을 story.md에 수작업 기입하고 reindex/wordcount/check 유지보수 블록으로 마무리한다.
- 주 측면: intent, premise
- 부 측면: format
- 단계: clarify
- 과제 종류: new, docs
- 묶음: story-skills
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: story CLI (없으면 bundled fallback story-maintenance/scripts/story.js, 둘 다 불가 시 references/manual-setup.md로 수작업); premise-workshop 산출물(있으면 재사용)
- 필수 명령: story, node
- 상태 파일: <project>/story.md (title, form, genre, premise, counter-premise, pov, tense, language, target-words); <project>/style-sheet.md; characters/, worldbuilding/, plot/, scenes/, continuity/, glossary/, chapters/ 의 _index.md 레지스트리 및 plot/timeline.md, continuity/state.md; .gitignore
- 주의: Story Skills 번들 공통: `story` CLI(node>=18, npm 의존성 없음; bun 불필요)에 의존하며 manifest 상 상태 READY, 제한 없음. 상대 파일 참조는 모두 해결됨. 스토리 프로젝트(story.md 기준) 마크다운 폴더 구조와 YAML frontmatter 규칙을 따라야 하며, 소설 프로젝트 파일에 쓰는 스킬이므로 일반 산문/문서 작업에는 맞지 않음. init은 기존 디렉터리를 --force 없이 거부하며 --force도 기존 파일은 덮어쓰지 않음. 비ASCII 제목은 --dir 필요할 수 있음. 제목 변경 시 `story reindex .` 필요. Form을 안 정하면 --form novel 사용. 판단: 단계: 제목·형식·장르·POV·시제·언어를 사용자에게 받아 프로젝트를 만든다. 다른 story 스킬의 전제 조건이지만 조합 구성원은 아니다.
- 근거: intent "Ask for basic story information" / premise "The premise is a one-sentence controlling idea" / format "kebab-case ids and filenames, YAML frontmatter on every story-project file"

### story-maintenance
- id: WM-X0168
- 출처: danjdewhurst/story-skills `skills/story-maintenance/SKILL.md` @ e44c97c, MIT
- 역할: Story Skills 프로젝트의 결정적(기계적) 유지보수를 Story CLI로 수행하는 스킬: validate, reindex, wordcount, links, continuity, pacing, clues, voices, 빌드·내보내기 등.
- 맞는 상황: validate/reindex/레지스트리 복구/링크·연속성·페이싱·단서·목소리·이름 검사, 단어 수 집계, 프로젝트 요약, 기존 원고 import, 원고 export/build, 다이어그램 생성이 필요할 때.
- 맞지 않는 상황: 발견된 문제의 판단·스토리 수정은 하지 않는다: 연속성 오류와 퇴고 패스는 revision-continuity, 페이싱은 plot-structure, 목소리·산문은 voice-style, 단서·공정한 플레이는 genre-craft, 독자와 리뷰 사본 공유는 feedback-triage.
- 고유 접근: CLI 검사 결과를 읽고 보고하며, 오래된 레지스트리·깨진 참조 같은 기계적 문제만 고치고 창작 산문은 건드리지 않는다. 모든 편집 뒤 reindex -> wordcount --write -> check 블록을 표준화한다.
- 주 측면: continuity
- 부 측면: evidence, format, review-report
- 단계: check
- 과제 종류: review, docs
- 묶음: story-skills
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: story CLI 또는 번들 node scripts/story.js (없으면 conventions.md 기준 수작업) | 선택: PDF 렌더 엔진(build --pdf); git (compare --ref)
- 필수 명령: story, node
- 상태 파일: story.md (cli-defaults, severity, revision-passes); progress.md; continuity/exemptions.md; continuity/state.md; dist/ (build 산출물); snapshots
- 주의: Story Skills 번들 공통: `story` CLI(node>=18, npm 의존성 없음; bun 불필요)에 의존하며 manifest 상 상태 READY, 제한 없음. 상대 파일 참조는 모두 해결됨. 스토리 프로젝트(story.md 기준) 마크다운 폴더 구조와 YAML frontmatter 규칙을 따라야 하며, 소설 프로젝트 파일에 쓰는 스킬이므로 일반 산문/문서 작업에는 맞지 않음. `import --force`는 chapters/ 의 chapter-NN.md를 삭제하고 `snapshot --restore`는 파일을 삭제하므로 사용자 승인 필요. 이 스킬은 판단/수정이 아니라 실행·보고용. Node로 실행하며 Bun은 쓰지 않는다.
- 근거: continuity "After any change to story files, run the maintenance block, in this order:" / evidence "Never invent acknowledgments, biographical facts, or copyright details" / format "`build` when the user asks to build the book artifact" / review-report "it is advisory, so report what it found, never a verdict."

### submission
- id: companion
- 출처: danjdewhurst/story-skills `skills/submission/SKILL.md` @ e44c97c, MIT
- 역할: 완성 원고의 투고 준비를 맡는다. 투고 준비도 점검, 한 줄 피치, 비교작, 쿼리 레터, 시놉시스, 블러브/소매점 설명, Shunn 형식 원고 빌드, 투고 추적기, 단편 시장과 선집 구성까지 다룬다.
- 맞는 상황: 원고가 투고 가능한지 점검할 때, 쿼리 레터·피치·시놉시스·블러브·비교작 목록을 쓸 때, Shunn 형식 원고를 만들 때, 자가출판 설명문을 쓸 때, 투고·응답을 기록할 때, 단편을 잡지·선집·공모전에 낼 때.
- 맞지 않는 상황: 여러 권 시리즈 피칭은 series-continuity, 자가출판 제작·메타데이터·판권 계약은 publishing, 원고 자체 수정은 revision-continuity, 독자 피드백 라운드는 feedback-triage를 쓴다. 블러브·소매점 설명·단편 시장이 사는 권리(재수록권 등)는 이 스킬에 남는다.
- 고유 접근: story check/prose/report 결정적 점검으로 준비도 판정(ready/ready-with-caveats/not-ready)을 먼저 내고, 모든 초안에 [TODO: author to supply] 플레이스홀더를 쓰며 작가 정보·시장·응답을 절대 지어내지 않고 작가 본인이 발송하게 한다.
- 주 측면: persuasion, format
- 부 측면: evidence
- 단계: draft
- 과제 종류: new, review
- 묶음: story-skills
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 완성 또는 거의 완성된 초고가 있는 story 프로젝트(story.md에 status, genre, premise, author, contact, language); story CLI 또는 번들 폴백 (reindex, wordcount, check, prose, report, synopsis, build) | 선택: voice-style(style-sheet.md가 스캐폴드일 때 먼저); revision-continuity(not-ready 블로커 인계, 분량 length pass); story-init의 title-logline.md 로그라인 레시피; publishing, series-continuity, editorial-review, plot-structure(연계); PDF 엔진(shunn --pdf)
- 필수 명령: story, node
- 상태 파일: submission/query.md; submission/comps.md; submission/synopsis-1-page.md; submission/synopsis-3-page.md; submission/blurb.md; submission/tracker.md; dist/<story-id>.shunn.docx|.md|.pdf; continuity/exemptions.md (후속권으로 넘기는 열린 약속 기록); story.md
- 주의: 매니페스트: 동반(companion) 스킬, READY. 상대 참조 ../revision-continuity/references/pass-checklists.md 가 submission 폴더 기준으로는 해석되지 않는다(스킬 폴더 형제 위치로는 존재). word-count-norms 등 레퍼런스는 영어권 시장 기준의 대략적 관례이므로 사용자에게 확인시킨다. story.md status가 complete/revising이 아니면 준비도 점검이 실패한다. 투고 패키지는 submission/ 아래에 있고 CLI가 검증하지 않으며 빌드에도 포함되지 않는다. 판단: 발송·업로드는 하지 않는다(범위 밖). 작가가 직접 제출한다.
- 근거: persuasion "Draft a one-sentence pitch: protagonist + goal + obstacle + stakes" / format "Keep the letter between 250 and 350 words." / evidence "Never invent the author's bio, credentials, awards, publication history,"

### submission-reviewer
- id: WM-X0107
- 출처: anayy09/claude-research-skills `submission-reviewer/SKILL.md` @ f0d3359, MIT
- 역할: 논문 또는 특허 제출물을 공정하고 건설적인 동료 심사자로서 가중 루브릭에 따라 100점 만점으로 채점하고 순위가 매겨진 수정 목록과 예상 점수를 내는 스킬.
- 맞는 상황: 원고, 프리프린트, 학위 챕터, 초록, 발명 신고서, 특허 초안에 대한 리뷰, 점수, 제출 전 점검, 신규성·출판 가능성 판단, '심사자가 뭐라 할까' 질문.
- 맞지 않는 상황: 저널/학회 추천(journal-advisor), 산문 재작성(manuscript-writing, prose-naturalizer), 실제 수정 작업(manuscript-editor), 서식 맞춤, 그림 재제작, 통계 계산, 법률 자문은 하지 않는다.
- 고유 접근: claim map을 먼저 만들고 실제 선행기술을 검색해 신규성을 확인한 뒤 score.py로 결정적 점수를 계산하며, authenticity 검사 결과를 비난 없이 사실 문구로 보고하고 수정 목록 표(id, 심각도, 위치, 노력)로 끝낸다.
- 주 측면: review-report
- 부 측면: evidence, voice
- 단계: check
- 과제 종류: review
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: python3 (scripts/score.py) | 선택: web search / patent databases (prior art)
- 필수 명령: python3
- 상태 파일: review report per references/report-format.md
- 주의: READY. 검색 도구가 없으면 신규성 신뢰도를 낮게 표기. 특허 리뷰는 법률 자문이 아님을 한 번 명시. 형제 스킬 인계는 제안일 뿐 필수 아님.
- 근거: review-report "Use the exact structure in `references/report-format.md`." / evidence "Do not score novelty from memory." / voice "Criticize the artifact, never the author."

### technical-writing
- id: WM-X0308
- 출처: riekelt/technical-writer `plugins/technical-writer/skills/technical-writing/SKILL.md` @ 85e5372, MIT
- 역할: 스펙, 설계 문서, README, 레퍼런스, 계획, 보고서 등 저장소에 들어가는 기술 문서 전반의 하우스 스타일, 진실/출처 규칙, 금지 구문 목록을 정의하는 기반 스킬.
- 맞는 상황: 한 문단을 넘는 저장소 대상 기술 문서 작성, 구조 변경, 개정. 형제 문서 유형 스킬의 기반.
- 맞지 않는 상황: 마케팅 카피, 소셜 포스트, UI 마이크로카피(진실 규칙만 적용). '펀치 있게', '설득력 있게' 요구에는 응하지 않는다.
- 고유 접근: 결론 우선, 모든 주장에 출처, 한 사실은 한 곳에만, 문서 종류(규범/기술/역사/런북/레퍼런스)별 편집 규칙, 금지 구문 표와 em dash 금지.
- 주 측면: tech-docs, prose-edit, ai-tells
- 부 측면: evidence, structure, flow, format, voice
- 단계: draft
- 과제 종류: new, edit, docs
- 묶음: technical-writer
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: references/style.md; references/truth.md (same skill folder) | 선택: sibling skills in routing table: writing-design-docs, recording-decisions, writing-changelogs, writing-runbooks, writing-issues, writing-postmortems, documenting-legacy-codebases, diagramming-processes, documenting-contracts, reviewing-technical-prose
- 필수 명령: 없음
- 상태 파일: project CLAUDE.md line recording the skill invocation (suggested)
- 주의: 매니페스트 notes: 라우팅 표의 형제 스킬 7개(writing-changelogs, writing-issues, writing-postmortems, documenting-legacy-codebases, diagramming-processes 등)는 'also load' 힌트이며 미설치. 규칙은 영어, 어휘 목록은 영어 전용. 마케팅 카피/UI 마이크로카피는 대상 아님. 사실상 '문체를 평이하게 고정'하므로 설득형/보이스형 스킬과 충돌 가능. 판단: 문장 규칙과 금지 구문 목록이 본업이라 prose-edit·ai-tells를 주 측면으로 둔다. 그래서 general-writing·humanizer와는 한 시안에 넣지 않는다(문체 규칙이 둘이 된다).
- 근거: tech-docs "When instructions conflict, apply them in this order:" / prose-edit "One claim per sentence. Average around 20 words, hard maximum 35." / ai-tells "No em dashes, no en dashes, no ` -- ` dashes." / evidence "Never state as fact what you cannot trace" / structure "**Draft conclusion-first** at every level" / flow "Banned: the heading that names the question instead of the content" / format "**Headings in sentence case**, never Title Case." / voice "Does not yield to a request to make a document "punchy", "compelling", or "persuasive""

### theme-craft
- id: companion
- 출처: danjdewhurst/story-skills `skills/theme-craft/SKILL.md` @ e44c97c, MIT
- 역할: 주제를 장식이 아닌 작동 메커니즘으로 설계하고 감사한다. 통제 아이디어(가치+원인), 거짓/진실/상처와 세 가지 아크 유형, 반대 논거로서의 적대자, 모티프 추적, 퇴고 시 주제 감사를 다룬다.
- 맞는 상황: 스토리 시작 시 작업 전제 수립, 캐릭터 설계 시 lie/truth/arc-type, 완성 초고 후 주제 감사, 모티프 계획·추적.
- 맞지 않는 상황: 전제 발굴·검증은 premise-workshop, 캐릭터 프로필·관계·'캐릭터 아크' 기록은 character-management를 쓴다.
- 고유 접근: 주제를 story.md의 premise/counter-premise와 캐릭터 lie/truth/ghost-wound/arc-type 필드로 기계적으로 기록하고, 감사 결과를 continuity/theme-audit.md에 theme-holds/theme-broken 판정으로 남긴다.
- 주 측면: premise
- 부 측면: character, continuity
- 단계: draft
- 과제 종류: new, review, docs
- 묶음: story-skills
- 필수 동반: story-init
- 금지 짝: 없음
- 실행 요건: 필수: story-init으로 만든 story 프로젝트(story.md) | 선택: character-management 캐릭터 파일, plot-structure 플롯 구조(있거나 진행 중이면 좋음); story CLI 또는 번들 폴백 (reindex, wordcount, check); continuity/motifs.md, continuity/theme-audit.md
- 필수 명령: story, node
- 상태 파일: story.md 프런트매터(premise, counter-premise); characters/*.md (arc-type, lie, truth, ghost-wound); continuity/motifs.md; continuity/theme-audit.md
- 주의: 매니페스트: 동반(companion) 스킬(premise-workshop이 controlling-idea.md를 참조), READY. 모티프 원장과 theme-audit.md는 산문 노트라 CLI가 검증하지 않아 모티프 회수·판정은 수동 감사해야 한다. premise를 'tbd-discovery'로 두고 발견형으로 갈 수 있다.
- 근거: premise "Theme is dramatized through choices and consequences." / character "give the antagonist an edge, a" / continuity "Motif ids are kebab-case and tracked in the motif ledger with" / story-init "A story project must already exist (created via the story-init skill)."

### translation
- id: WM-X0339
- 출처: seb1n/awesome-ai-agent-skills `writing-and-content/translation/SKILL.md` @ 75865a5, MIT
- 역할: 언어 간 번역: 문화 적응, 용어 일관성, 포맷 보존으로 기술 문서, 마케팅, UI 문자열, 법률 텍스트 등을 번역한다.
- 맞는 상황: 번역 요청(대상 언어, 격식 수준, 도메인, 용어집, 출력 포맷 지정 가능). JSON 로케일 파일과 마크다운 문서도 포함.
- 맞지 않는 상황: 원문 작성이나 문체 편집에는 맞지 않는다. 번역 외 윤문은 다른 스킬 영역.
- 고유 접근: 원문 문맥·레지스터 분석, 용어집 구축, 서식·플레이스홀더 보존 번역, 로케일 현지화(단위·날짜·관용구), 모호한 선택에 번역자 주석을 붙여 납품한다.
- 주 측면: translation
- 부 측면: format, voice
- 단계: draft
- 과제 종류: new, edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: user glossary / translation memory
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트: 'translation'은 일반적인 이름이나 설치 시 ~/.claude/skills에서 충돌 없었음. 격식·성별 선택은 사용자 확인이 필요할 수 있으나 핵심 작업은 비대화형으로 처리 가능.
- 근거: translation "Use the same translated term for a given source term throughout the entire document." / format "Never strip Markdown, HTML tags, or JSON keys during translation." / voice "Always confirm the desired register before translating."

### verse-craft
- id: WM-X0171
- 출처: danjdewhurst/story-skills `skills/verse-craft/SKILL.md` @ e44c97c, MIT
- 역할: 리머릭·소네트·하이쿠·빌라넬·발라드·노래 가사·운율 그림책 텍스트 등 운문을 쓰고, 스캔하고, 고친다. 모든 '스캔된다'는 주장은 강세 표기·음절 수·압운 표로 증명한다.
- 맞는 상황: 새 시·노래·라임을 정해진 형식으로 쓸 때, 기존 시가 운율·압운 구조를 지키는지 점검할 때, 억지 압운이나 군더더기 행을 고칠 때, 이야기 속 인물의 노래·예언·수수께끼를 쓸 때.
- 맞지 않는 상황: 산문에 우연히 생긴 라임은 line-editing, 타인의 시·가사 인용 허락은 editorial-review를 쓴다. 시집을 story 프로젝트로 만들지 않으며(story init 금지) 시 모음은 일반 파일로 관리한다.
- 고유 접근: 행마다 강세·음절·압운 문자를 보여 주는 스캔 표를 필수로 내고, 의도된 변이(deliberate)와 결함(fault)을 구분하며, 수정은 line-editing의 edit-note 형식으로 제안한다.
- 주 측면: verse
- 부 측면: prose-edit, voice, continuity, format
- 단계: draft
- 과제 종류: new, edit, review
- 묶음: story-skills
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: 이야기 속 운문이면 story.md(era, tone, language)와 화자 캐릭터 파일; story CLI 또는 번들 폴백 (story add matter, reindex, check); TTS: say / espeak-ng / spd-say (설치 전 확인)
- 필수 명령: 없음
- 상태 파일: 단독 시: 사용자가 지정한 위치의 .md 파일; 이야기 속 운문: 챕터 본문 또는 matter/ 파일(story add matter 'Epigraph' --heading=false); story.md; characters/*.md (voice-words, voice-avoid)
- 주의: 매니페스트: READY, 모든 상대 참조 해석됨. 단독 시에는 프로젝트가 필요 없다. references의 형식·예시·강제 압운 신호는 영어 기준이라 타 언어에서는 조정하고 신뢰 불가능하면 그렇다고 밝혀야 한다. story 명령은 번들 폴백 가능. 판단: 단독 운문에는 story 프로젝트가 필요 없어 story·node를 필수 명령에서 뺐다(이야기 속 운문일 때만 쓴다).
- 근거: verse "Never say a line scans without showing its stresses" / prose-edit "Never invert natural word order to land a rhyme" / voice "Verse a character writes sounds like that character" / continuity "Verse must not state canon the project" / format "Keep line breaks through every build"

### voice-builder
- id: WM-X0369
- 출처: social-media-skills/skills `skills/voice-builder/SKILL.md` @ f28cef2, MIT
- 역할: 사용자/브랜드의 실제 글 샘플을 6개 층위로 분석해 재현 가능한 voice.md(보이스 가이드)를 만든다.
- 맞는 상황: '내 보이스 만들어줘', '내 어조 캡처', 글이 제너릭/'내 글 같지 않음'일 때, 고스트라이팅 보이스 확립, 실제 글 샘플이 3개 이상 있을 때.
- 맞지 않는 상황: 샘플이 없으면 쓰지 않고 brand-profile의 보이스 인터뷰로 보낸다(보이스를 지어내지 않음). 건별 보이스 적용·AI티 제거는 writing-style-and-tone 몫.
- 고유 접근: 형용사 대신 증거(샘플 인용)로 어휘·구문·수사·구조·태도·부정 공간 6층 분석 → 5~7개 시그니처 지문 → voice.md 작성 → 새 주제로 보이스 테스트(생성·비교·채점·수정)까지 수행.
- 주 측면: voice
- 부 측면: 없음
- 단계: clarify
- 과제 종류: new
- 묶음: social-media-skills
- 필수 동반: brand-profile
- 금지 짝: 없음
- 실행 요건: 필수: user writing samples (3 minimum, 5-10 recommended); brand-profile.md | 선택: writing-style-and-tone (not installed)
- 필수 명령: 없음
- 상태 파일: voice.md (created; alongside brand-profile.md in user project files; one named voice.md per voice when multiple); brand-profile.md (read)
- 주의: 실제 글 샘플이 필요하며 없으면 brand-profile 보이스 인터뷰로 대체해야 한다. 저장 위치는 원문에 명시되지 않음(brand-profile과 같은 프로젝트 파일 옆). 샘플이 얇으면 low-confidence 표기.
- 근거: voice "**voice is extracted from evidence, not described in adjectives.**" / brand-profile "Load `brand-profile.md` for identity, audience, and guardrails."

### voice-style
- id: companion
- 출처: danjdewhurst/story-skills `skills/voice-style/SKILL.md` @ e44c97c, MIT
- 역할: 책의 목소리와 표면 관습을 style-sheet.md에 기록하고, story prose(필터 워드·-ly 부사·말버릇 태그·반복어·비슷한 이름)와 story voices(인물별 대사 지문)로 일관성을 점검한다.
- 맞는 상황: 프로젝트 시작 시 첫 챕터나 샘플이 생겼을 때, 챕터·세션 사이 목소리가 흐려졌을 때, 카피에디트에 스타일 결정을 기록해야 할 때, 공유 전에 기계적 산문 점검이 필요할 때, 인물별 목소리를 기록하고 검사할 때.
- 맞지 않는 상황: 대사 목소리가 다 비슷할 때 대사를 고쳐 쓰는 일은 line-editing, 인물 성격·아크는 character-management, 딥 POV·서브텍스트는 scene-craft, 라인 바이 라인 문장 패스(라인 에디트·카피에디트·소리 내어 읽기·교정)는 line-editing을 쓴다.
- 고유 접근: 스타일시트 프런트매터(dialect, preferred, watch-words, allow-words, samples)를 기계가 읽게 만들고, 작가가 승인한 샘플을 기준선으로 삼아 챕터가 그 기준에서 벗어났는지 경고한다. 수치는 재독의 신호이지 명령이 아니다.
- 주 측면: voice
- 부 측면: prose-edit
- 단계: prose, check
- 과제 종류: edit, review, docs
- 묶음: story-skills
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: story.md가 있는 story 프로젝트(story init이 style-sheet.md 생성) | 선택: story CLI 또는 번들 폴백 (story prose, story voices, story names, story rename); 프로즈가 없으면 사용자가 주는 문단이나 비슷한 목소리의 책 3권; scene-craft의 dialogue-subtext.md(태그 교체 테스트); line-editing의 language-conventions.md(타 언어 대사 구두점)
- 필수 명령: story, node
- 상태 파일: style-sheet.md (프런트매터 dialect/preferred/watch-words/allow-words/samples, add-words/replace-words); story.md (language, cli-defaults, severity); characters/*.md (voice-words, voice-avoid, Voice & Speech Patterns); chapters/*.md
- 주의: 매니페스트: 동반(companion) 스킬, READY, 상대 참조 해석됨. line-editing이 style-sheet 구축을 위해 의존해 설치됨. 필터 워드·부사·말버릇 목록은 영어, 스페인어, 프랑스어, 독일어 팩만 있고 그 외 언어는 점검이 건너뛰어져 직접 읽어야 한다. 경고는 자문용이며 story.md severity로 오류로 승격 가능. interactive는 샘플 수집·불일치 결정이 필요해 true로 판단함(원문은 조건부 질문). 판단: 단계: 원고가 이미 내린 결정을 기록하고 story prose·voices로 점검한다. 불일치 결정만 사용자에게 물으므로 clarify로 두지 않았다.
- 근거: voice "Recording each character's voice" / prose-edit "revise sentence length by intent"

### write-agent-prompts
- id: WM-X0227
- 출처: inanna-malick/agent-skills `skills/write-agent-prompts/SKILL.md` @ fa2ce23, MIT
- 역할: 유능한 동료 에이전트를 위한 프롬프트와 스킬을, 고현저성 기술 용어와 개념 폭, 의미 압축으로 쓰는 방법을 제시한다.
- 맞는 상황: 에이전트가 과제 구조를 인식하고 지식을 끌어오며 방법을 고르고 접근을 바꾸는 방식을 형성하는 프롬프트나 스킬을 쓸 때.
- 맞지 않는 상황: 원문에 명시된 제외 대상은 없음. 완성형 단일 채팅 프롬프트 생성이나 평가 루프 중심 작업과는 결이 다르다.
- 고유 접근: 인지과학·AI 개념(공통 기반, 인지 과제 분석, 구조 정렬, 메타추론 등)을 렌즈로 삼아 설명을 압축하고 개념 레퍼토리를 구조적으로 조직한다. 스킬 자체가 그 기법의 시연이다.
- 주 측면: prompt
- 부 측면: 없음
- 단계: draft
- 과제 종류: new, edit
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: references/concepts.md for grounding of referents
- 필수 명령: 없음
- 상태 파일: references/concepts.md (read-only)
- 주의: 매니페스트: READY, agents/openai.yaml은 메타데이터일 뿐이며 references/concepts.md 링크는 해석됨. 어휘가 추상적이고 압축적이라 사람 독자용 산문에는 부적합하며 에이전트 대상 프롬프트 작성에 한정. prompt-optimizer 계열과 대상이 겹친다.
- 근거: prompt "Use the recipient's shared technical vocabulary."

### writing-cadence
- id: companion
- 출처: msimchowitz/writing-skills `for-agents/writing-cadence/SKILL.md` @ 214981f, MIT
- 역할: 단조로운 짧은 문장 연속, 균일한 길이, 반복 시작, 반복 대조 공식, 행위자를 숨기는 추상 과정 틀을 진단하고 리듬을 의미와 강조에 맞게 고친다. humanizer 5단계 동반 스킬.
- 맞는 상황: 리듬, 박자, 문장 다양성, 끊기거나 단조로운 산문 요청, 'not X but Y', 'treats X as Y, not Z' 같은 반복 패턴.
- 맞지 않는 상황: 길이를 기계적으로 번갈아 맞추기, 질감용 파편 추가, 분류나 증명처럼 반복 구문이 필요한 고정 형식 문단 억지 수정, 주장·한계를 바꾸는 편집.
- 고유 접근: 진단 목록(짧은 문장 연속, 반복 시작, 반복 대조 프레임, 추상 과정 명사)을 규칙이 아닌 진단으로만 쓰고, 문단 끝은 추론이 도달하는 곳에서 끝내며, 소리 내어 읽는 속도로 점검한다.
- 주 측면: prose-edit
- 부 측면: ai-tells, flow
- 단계: prose
- 과제 종류: edit, review
- 묶음: msimchowitz
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: references/cadence-principles.md (전체 리듬 편집 시)
- 필수 명령: 없음
- 상태 파일: 없음
- 주의: 매니페스트: 동반 스킬, SHA가 선택 목록에 없어 현재 HEAD 설치. humanizer 5단계가 마지막 순서로 호출한다. forbids는 호출 경계 규칙으로, 이 스킬이 다른 파이프라인 스킬을 호출하지 말라는 의미다. 판단: 원문의 'Do not invoke Humanizer …' 줄은 humanizer가 이 스킬을 부를 때 파이프라인을 다시 부르지 말라는 재귀 방지 규칙이라 금지 짝으로 적지 않았다. humanizer(general-writing 경유 포함)가 이미 이 스킬을 적용하므로 그런 조합에 따로 넣으면 중복이다.
- 근거: prose-edit "Shape rhythm around meaning and emphasis." / ai-tells "Mark every contrast built from a reusable difference template" / flow "Do not append a summary, slogan, generic implication, or sentence about the document"

### writing-design-docs
- id: WM-X0310
- 출처: riekelt/technical-writer `plugins/technical-writer/skills/writing-design-docs/SKILL.md` @ 85e5372, MIT
- 역할: 제안서, RFC, 설계 문서, 스펙, 마이그레이션 계획처럼 변경을 주장하거나 설계를 기록하는 문서를 쓰는 스킬. Why & What 박스와 완결성 점검을 제공한다.
- 맞는 상황: 변경을 논증하거나 범위를 정해야 하는 문서, 'should we' 문서, '접근 방식을 정리해줘' 요청.
- 맞지 않는 상황: 이미 내려진 결정 기록(recording-decisions), 절차(writing-runbooks), 상태 보고서.
- 고유 접근: 결론 먼저의 요약, 비자명한 선택마다 Why & What 박스(가장 강한 반대 논거, 해결하지 못하는 것, 폴백), 이익과 함께 비용 명시, 사실과 제안 분리.
- 주 측면: structure
- 부 측면: evidence, voice, tech-docs
- 단계: draft
- 과제 종류: new, edit, docs
- 묶음: technical-writer
- 필수 동반: technical-writing
- 금지 짝: 없음
- 실행 요건: 필수: technical-writing skill | 선택: recording-decisions (after acceptance)
- 필수 명령: 없음
- 상태 파일: design doc markdown in repository
- 주의: 매니페스트 notes: technical-writing 필수 배경(설치됨). 기반 스킬의 대시 금지, 금지 구문 규칙이 함께 적용된다.
- 근거: structure "Every non-trivial choice gets one; readers react to the box, not to the conclusion." / evidence "mark them `**[source wanted: ...]**`" / voice "No superlatives, no promise language." / tech-docs "the register rules hold whatever the deadline" / technical-writing "**REQUIRED BACKGROUND:** the `technical-writing` skill"

### writing-for-agents
- id: WM-X0272
- 출처: mattpocock/skills `skills/productivity/writing-for-agents/SKILL.md` @ 59db609, MIT
- 역할: 스킬, AGENTS.md/CLAUDE.md, 포인터로 닿는 문서 등 에이전트가 읽는 모든 문서를 쓰는 참조 지침이다.
- 맞는 상황: 스킬을 만들거나 고치거나 AGENTS.md나 CLAUDE.md를 수정할 때.
- 맞지 않는 상황: 사람 독자용 글쓰기는 대상이 아니다. 스킬 프런트매터와 호출 방식 등 스킬 고유 사항은 SKILL-MECHANICS.md가 따로 다룬다.
- 고유 접근: 컨텍스트 포인터, 컨텍스트/인지 부하, 정보 위계와 점진적 공개, 완료 기준, 리딩 워드, 가지치기라는 레버로 에이전트 실행 경로의 변동성을 줄인다.
- 주 측면: prompt
- 부 측면: structure
- 단계: draft
- 과제 종류: new, edit, docs
- 묶음: 없음
- 필수 동반: 없음
- 금지 짝: 없음
- 실행 요건: 필수: 없음 | 선택: SKILL-MECHANICS.md when the document being written is a skill
- 필수 명령: 없음
- 상태 파일: SKILL-MECHANICS.md (sibling, read-only); agents/openai.yaml (ignored by Claude Code)
- 주의: 매니페스트: READY, SKILL-MECHANICS.md 링크 해석됨, agents/openai.yaml은 Claude Code에서 무시됨. 대상은 에이전트가 읽는 문서이며 사람용 산문 글쓰기에는 적용하지 않는다. 스킬 작성이면 SKILL-MECHANICS.md를 읽으라고 안내함(조건부).
- 근거: prompt "Prompt the **positive**:" / structure "Progressive disclosure"

### writing-runbooks
- id: WM-X0313
- 출처: riekelt/technical-writer `plugins/technical-writer/skills/writing-runbooks/SKILL.md` @ 85e5372, MIT
- 역할: 런북, 설정 가이드, 릴리스 절차, 마이그레이션/폐기 가이드, 트러블슈팅 항목처럼 누군가 시간에 쫓겨 실행할 순서형 운영 문서를 쓰는 스킬.
- 맞는 상황: 실행되는 모든 절차 문서, 설정 노트, 마이그레이션 가이드, 증상 우선 트러블슈팅, 시스템 내부 에러 메시지와 로그 문구.
- 맞지 않는 상황: 설계 근거(writing-design-docs), 아무도 실행하지 않는 레퍼런스 자료. 한 번도 실행하지 않은 절차는 런북이 아니라 초안으로 표시해야 한다.
- 고유 접근: 실제로 실행해 본 단계만 기록, 위험 범례, TL;DR 해피 패스, 복붙 가능한 명령, 단계별 롤백, 증상 우선 트러블슈팅, 만료일 있는 마이그레이션 가이드.
- 주 측면: structure
- 부 측면: evidence, format, prose-edit
- 단계: draft
- 과제 종류: new, edit, docs
- 묶음: technical-writer
- 필수 동반: technical-writing
- 금지 짝: 없음
- 실행 요건: 필수: technical-writing skill | 선택: writing-design-docs, recording-decisions, writing-changelogs (migration guide siblings)
- 필수 명령: 없음
- 상태 파일: runbook markdown in repository
- 주의: 매니페스트 notes: technical-writing 필수 배경(설치됨). 실제 실행 경험이 없으면 초안으로만 표시 가능. 마이그레이션 가이드는 기반 스킬의 이력 금지 규칙의 명시적 예외.
- 근거: structure "**TL;DR happy path first**" / evidence "Write from a real run" / format "keep the placeholder visibly bracketed, never invented" / prose-edit "one action each, present tense or imperative, with a visible actor." / technical-writing "**REQUIRED BACKGROUND:** the `technical-writing` skill"
