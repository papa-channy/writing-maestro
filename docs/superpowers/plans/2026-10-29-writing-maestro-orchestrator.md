# writing-maestro 오케스트레이터 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 설치된 글쓰기 스킬 67개를 주·부 측면 기반 레지스트리로 등록하고, 이를 읽어 충돌 없는 스킬 조합을 제안·실행해 시안 N개를 만드는 `writing-maestro` 오케스트레이터 스킬을 만든다.

**Architecture:** 오케스트레이터는 LLM이 따르는 `SKILL.md`와 사람이 고치는 `registry.md`로 이루어진다. 충돌 판정은 LLM 판단에 맡기지 않고, `registry.md`를 파싱하는 stdlib 파이썬 스크립트(`combo_check.py`)가 결정적으로 계산해 SKILL.md가 호출한다. 레지스트리 내용은 병렬 에이전트가 스킬 원문에서 사실을 뽑고(Task 3) 단일 패스가 측면 분류·조립(Task 4)한다.

**Tech Stack:** Markdown (SKILL.md, registry.md), Python 3.11 stdlib (스크립트), pytest (테스트), Claude Code skills (`~/.claude/skills`).

**Spec:** `docs/superpowers/specs/2026-10-29-writing-maestro-orchestrator-design.md`

## Global Constraints

- 서드파티 스킬 원문(`~/.claude/skills/<name>/` 아래)은 수정하지 않는다. 우선순위 지정은 시안 지시 안에서만.
- 오케스트레이터 문서(SKILL.md, registry.md, feedback.md)는 한국어. 측면·단계 id는 파싱용 영문 slug, 표시는 한국어 라벨.
- 조합 후보 최대 4개. 조합당 생성 스킬 최대 3개(묶음 안 필수 동반은 세지 않음). 억지로 개수를 채우지 않는다.
- 조합·개수 질문은 `AskUserQuestion` 1회. 조합이 하나면 개수만. 검토 과제는 개수 질문 없이 조합당 1개.
- 같은 조합 시안끼리 차이를 강제하는 지시를 넣지 않는다.
- 시안 서브에이전트: model opus, 한 메시지에서 동시 실행. 실패 시 재시도하지 않고 사유 기록.
- 출력 폴더: `<프로젝트 루트>/writing-drafts/<YYYYMMDD-HHMM>-<과제-slug>/` (프로젝트 없으면 현재 작업 폴더). `brief.md` + `combo<k>-<id>+<id>/d<n>/`(본문 + NOTES.md).
- 원문·레포 파일은 시안 폴더로 복사해서 작업, 원본 불변.
- 질문 불가 시: 명확화 생략, 모든 후보 × 1개, 사용자 입력이 필수인 조합은 "실행 불가: 사용자 입력 필요".
- 순위·추천을 넣지 않는다. 넘기고 멈춘다.
- 스크립트는 Python stdlib만 (레포 `tools/` 관례). 테스트만 pytest.

## Review Focus

1. **등록되지 않은 스킬을 사용자가 지명** → 쓰지 않고 결과의 "제외"에 "미등록"으로 적는다. (Task 5 SKILL.md 규칙 + Task 6 시험 사례 F)
2. **레지스트리 범위 밖 과제**(예: "엑셀 수식 짜줘") → 조합·질문 없이 "범위 밖" 한 줄 보고. (Task 5 + Task 6 사례 G)
3. **필수 실행 요건 미충족**(예: `story` CLI가 PATH에 없음) → 그 조합은 질문 전에 "실행 불가"로 빠지고 다른 스킬로 임의 대체하지 않는다. (`combo_check.py --check-runtime`, Task 2 테스트 `test_runtime_missing_command`)
4. **레지스트리와 설치 상태 불일치**(디렉터리 삭제, 미등록 설치 스킬) → `registry_check.py`가 오류로 잡는다. (Task 1 테스트 `test_missing_install_dir`, `test_unregistered_installed_skill`)
5. **사용자가 개수를 총합으로 답함**("총 5개") → 조합 수로 나눠 앞 조합부터 1개씩 더 배분(5개/2조합 → 3,2). (Task 5 SKILL.md 규칙 + 사례 A에서 확인)

---

## File Structure

```
skills/writing-maestro/
  SKILL.md                  # 오케스트레이터 절차 (Task 5)
  registry.md               # 레지스트리 (Task 4)
  feedback.md               # 사용자 기준·사이클 기록 (Task 5, 빈 골격)
  scripts/
    registry_lib.py         # registry.md 파서 + 데이터 타입 (Task 1)
    registry_check.py       # 레지스트리 검증 CLI (Task 1)
    combo_check.py          # 조합 충돌·우선순위 계산 CLI (Task 2)
tests/
  fixtures/registry_min.md  # 테스트용 최소 레지스트리 (Task 1)
  test_registry_lib.py      # (Task 1)
  test_combo_check.py       # (Task 2)
  test_registry_real.py     # 실제 registry.md 수용 테스트 (Task 4)
research/install/2026-10-29-install-manifest.json   # 설치 매니페스트 (Task 1)
research/registry-build/facts/<skill>.json          # 스킬별 원문 사실 (Task 3)
research/trials/2026-10-29/<case>.md                # 시험 기록 (Task 6)
```

## registry.md 형식 (Task 1이 파싱, Task 4가 채움)

```markdown
## 측면
| id | 이름 | 설명 |
|---|---|---|
| ai-tells | AI식 표현 제거 | ... |

## 단계
| id | 이름 |
|---|---|
| clarify | 명확화 |  research | 조사·근거 |  draft | 구조·초안 |  genre | 장르·포맷 |  prose | 문장·문체 |  check | 검수 |
(실제 파일은 한 행에 하나)

## 묶음
| id | 구성 |
|---|---|
| story-skills | story-init, character-management, ... |

## 스킬

### general-writing
- id: WM-X0282
- 출처: msimchowitz/writing-skills `for-agents/general-writing/SKILL.md` @ 214981f, MIT
- 역할: ...
- 맞는 상황: ...
- 맞지 않는 상황: ...
- 고유 접근: ...
- 주 측면: prose-edit, ai-tells
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
- 근거: prose-edit "..." / ai-tells "..." / voice "..." / humanizer "..."
```

- `id`: `WM-X####` 또는 `companion`. `doc-coauthoring`은 `출처`에 `plugin anthropic-skills` 표기.
- `과제 종류` 값: `new`(새 글), `edit`(고치기), `review`(검토), `docs`(코드베이스 문서).
- `필수 명령`: 실행 전 `command -v`로 확인할 실행 파일 목록(예: `story, node`) 또는 `없음`.
- 목록 필드는 쉼표 구분, 빈 값은 `없음`.
- `근거`: `/`로 구분된 `<측면 id 또는 스킬명> "<원문 인용>"` 쌍. 모든 주·부 측면, 필수 동반, 금지 짝마다 하나씩.

---

### Task 1: 레지스트리 파서와 검증기

**Files:**
- Create: `skills/writing-maestro/scripts/registry_lib.py`, `skills/writing-maestro/scripts/registry_check.py`
- Create: `tests/fixtures/registry_min.md`, `tests/test_registry_lib.py`
- Create: `research/install/2026-10-29-install-manifest.json` (복사: `/private/tmp/claude-501/-Users-chan-Developer-Skills-writing-maestro/2175444f-7ba7-47c4-be01-511c422a8fef/scratchpad/install-manifest.json`)

**Interfaces:**
- Produces:
  - `@dataclass Skill(name: str, wm_id: str, primary: list[str], secondary: list[str], stages: list[str], task_types: list[str], bundle: str | None, requires: list[str], forbids: list[str], commands: list[str], evidence: dict[str, str], fields: dict[str, str])`
  - `@dataclass Registry(aspects: dict[str, str], stages: dict[str, str], bundles: dict[str, list[str]], skills: dict[str, Skill])`
  - `parse_registry(text: str) -> Registry`
  - `validate(reg: Registry, installed: set[str], skills_dir: Path) -> list[str]` (오류 문자열 목록, 빈 목록이면 통과)
  - CLI: `python3 registry_check.py --registry PATH --manifest PATH [--skills-dir ~/.claude/skills]` → 오류를 한 줄씩 출력, 있으면 exit 1, 없으면 `OK <n> skills` exit 0.
  - `installed` = 매니페스트 `skills[].installed_dir`의 basename (status ≠ BLOCKED) ∪ `{"doc-coauthoring"}`.

- [ ] **Step 1: 매니페스트를 레포로 복사하고 픽스처 작성**

`tests/fixtures/registry_min.md`: 위 형식으로 측면 4개(`prose-edit`, `ai-tells`, `persuasion`, `voice`), 단계 6개, 묶음 1개(`msimchowitz: general-writing, humanizer`), 스킬 4개: `general-writing`(주 prose-edit; 부 voice; 필수 동반 humanizer; 단계 prose), `humanizer`(companion; 주 ai-tells; 단계 prose; 묶음 msimchowitz), `prose-naturalizer`(주 ai-tells, prose-edit; 금지 짝 manuscript-writing; 단계 prose), `copywriting`(주 persuasion; 부 ai-tells; 단계 draft; 필수 명령 없음). 각 근거 포함.

- [ ] **Step 2: 실패하는 테스트 작성** — `tests/test_registry_lib.py`

```python
def test_parse_fixture():
    reg = parse_registry(FIXTURE.read_text())
    assert set(reg.aspects) == {"prose-edit", "ai-tells", "persuasion", "voice"}
    assert reg.skills["general-writing"].primary == ["prose-edit"]
    assert reg.skills["general-writing"].requires == ["humanizer"]
    assert reg.skills["prose-naturalizer"].forbids == ["manuscript-writing"]
    assert reg.skills["humanizer"].wm_id == "companion"
    assert reg.bundles["msimchowitz"] == ["general-writing", "humanizer"]

def test_fixture_valid(tmp_path):  # 네 스킬 디렉터리를 tmp_path에 만들고
    assert validate(reg, {"general-writing","humanizer","prose-naturalizer","copywriting"}, tmp_path) == []

def test_unknown_aspect():           # 주 측면에 "nope" → "general-writing: unknown aspect nope"
def test_missing_evidence():         # 근거에서 voice 제거 → "general-writing: no evidence for voice"
def test_missing_field():            # "- 단계:" 줄 삭제 → "...: missing field 단계"
def test_missing_install_dir():      # copywriting 디렉터리 없음 → "copywriting: not installed"
def test_unregistered_installed_skill():  # installed에 "extra" 추가 → "extra: installed but not in registry"
def test_requires_unknown_skill():   # 필수 동반 "ghost" → "general-writing: requires unknown skill ghost"
```
`doc-coauthoring`은 `출처`에 `plugin`이 있으면 디렉터리 검사를 건너뛴다(별도 테스트 `test_plugin_skill_skips_dir_check`). 금지 짝은 미등록 이름을 허용한다.

- [ ] **Step 3: 실패 확인** — Run: `python3 -m pytest tests/test_registry_lib.py -q` / Expected: ImportError로 FAIL

- [ ] **Step 4: `registry_lib.py`, `registry_check.py` 구현** — `## 측면`/`## 단계`/`## 묶음` 표는 첫 열 id, `### <name>` 아래 `- 키: 값` 줄을 dict로 모은 뒤 필드 매핑. 필수 필드는 형식 예시의 키 전부.

- [ ] **Step 5: 통과 확인** — Run: `python3 -m pytest tests/test_registry_lib.py -q` / Expected: all passed

- [ ] **Step 6: Commit**
```bash
git add skills/writing-maestro/scripts tests research/install
git commit -m "feat: add writing-maestro registry parser and validator"
```

### Task 2: 조합 충돌·우선순위 계산기

**Files:**
- Create: `skills/writing-maestro/scripts/combo_check.py`, `tests/test_combo_check.py`

**Interfaces:**
- Consumes: `parse_registry`, `Registry`, `Skill` (Task 1)
- Produces:
  - `@dataclass ComboResult(ok: bool, conflicts: list[str], precedence: dict[str, str], ignored: list[tuple[str, str]], generation_count: int, missing_commands: list[str])`
    - `precedence`: 부 측면 id → 따를 스킬. `ignored`: (스킬, 측면) — 그 스킬의 해당 규칙은 적용하지 않음.
  - `check_combo(reg: Registry, skills: list[str], check_runtime: bool = False) -> ComboResult` (`skills`는 적용 순서)
  - CLI: `python3 combo_check.py --registry PATH [--check-runtime] SKILL [SKILL ...]` → `ComboResult`를 JSON으로 stdout, ok면 exit 0 아니면 1.

규칙 (스펙 §4.3–4.5):
1. 미등록 스킬 → conflict `unknown skill X`.
2. 금지 짝(어느 쪽이 선언했든) → conflict `forbidden pair A+B`.
3. 같은 주 측면을 가진 두 스킬 → conflict `primary overlap <aspect>: A, B`. **예외:** 둘이 같은 묶음이고 조합 안에서 `필수 동반` 간선(방향 무시)으로 연결돼 있으면 허용.
4. 생성 스킬 수 = 단계가 `clarify`/`check`만이 아닌 스킬 중, 조합 안 다른 스킬의 `필수 동반`이 아닌 것. 3 초과 → conflict `too many generation skills: n`.
5. 단계가 `clarify`만인 스킬이 들어오면 → conflict `clarify-stage skill in combo: X`.
6. 우선순위: 조합 안 스킬의 부 측면마다, 그 측면을 주 측면으로 가진 스킬이 있으면 그 스킬, 없으면 그 측면을 부 측면으로 가진 스킬 중 순서상 마지막. 따를 스킬이 아닌 나머지는 `ignored`에 넣는다.
7. `check_runtime=True`면 각 스킬 `commands`를 `shutil.which`로 확인, 없으면 `missing_commands`에 `skill:cmd`를 넣고 ok=False.

- [ ] **Step 1: 실패하는 테스트 작성** — `tests/test_combo_check.py` (Task 1 픽스처 사용)

```python
def test_primary_overlap_conflicts():
    r = check_combo(reg, ["general-writing", "prose-naturalizer"])
    assert not r.ok and "primary overlap prose-edit: general-writing, prose-naturalizer" in r.conflicts

def test_bundle_companion_allowed():   # 픽스처에서 humanizer 주 측면에 prose-edit도 넣은 변형 레지스트리로
    r = check_combo(reg2, ["general-writing", "humanizer"]); assert r.ok

def test_precedence_primary_owner():
    r = check_combo(reg, ["copywriting", "humanizer"])
    assert r.ok and r.precedence == {"ai-tells": "humanizer"} and ("copywriting", "ai-tells") in r.ignored

def test_precedence_last_secondary(): # 주 소유자 없이 부 측면 voice만 두 스킬이 가진 변형 → 순서상 마지막
def test_forbidden_pair():            # 금지 짝을 등록 스킬로 바꾼 변형 → "forbidden pair ..."
def test_too_many_generation():       # 생성 스킬 4개 변형 → "too many generation skills: 4"
def test_companion_not_counted():     # general-writing+humanizer → generation_count == 1
def test_clarify_in_combo():          # 단계 clarify 스킬 → conflict
def test_unknown_skill():
def test_runtime_missing_command():   # commands=["definitely-not-a-cmd-xyz"] 변형, check_runtime=True → ok False, missing_commands == ["x:definitely-not-a-cmd-xyz"]
def test_cli_json(tmp_path):          # subprocess로 CLI 실행 → exit 1, JSON의 ok == False
```

- [ ] **Step 2: 실패 확인** — Run: `python3 -m pytest tests/test_combo_check.py -q` / Expected: FAIL (ImportError)
- [ ] **Step 3: `check_combo`와 CLI 구현** (`combo_check.py`, `registry_lib` import는 스크립트 디렉터리 기준 상대 경로)
- [ ] **Step 4: 통과 확인** — Run: `python3 -m pytest tests -q` / Expected: all passed
- [ ] **Step 5: Commit** — `git commit -m "feat: add writing-maestro combo conflict checker"`

### Task 3: 스킬별 원문 사실 추출 (병렬)

**Files:**
- Create: `research/registry-build/facts/<skill>.json` × 67 (설치 디렉터리명 기준; `doc-coauthoring`은 `~/.claude/skills/synced/*/doc-coauthoring/SKILL.md`)

**Interfaces:**
- Produces (Task 4가 소비): 각 파일 JSON
```json
{"name": "...", "wm_id": "WM-X#### | companion", "source": "owner/repo path @commit7, license",
 "role": "...", "fits": "...", "not_fits": "...", "unique_approach": "...",
 "directives": [{"topic": "자유 서술 주제", "main": true, "quote": "원문 인용"}],
 "requires": [{"skill": "...", "quote": "..."}], "forbids": [{"skill": "...", "quote": "..."}],
 "interactive": true, "task_types": ["new","edit","review","docs"],
 "stage_hint": "clarify|research|draft|genre|prose|check",
 "requirements": {"required": [], "optional": []}, "commands": [], "state_files": [], "cautions": ""}
```
  - `directives`: 스킬이 결과물에 대해 지시하는 규칙 주제. `main=true`는 본업, `false`는 곁가지 규칙(예: copywriting의 AI 표현 금지). 측면 분류는 Task 4가 하므로 여기서는 자유 서술.
  - `requires`: 원문이 실행에 필요하다고 한 것만("see also/related"는 제외). `interactive`: 사용자 대화·인터뷰·샘플 수집이 필요하면 true.
  - `cautions`: 매니페스트의 `limits_or_blocker`·`notes` 요약 포함.

- [ ] **Step 1:** 매니페스트로 67개 목록을 만들고 묶음·저장소 단위 8묶음으로 나눠 sonnet 서브에이전트 8개를 한 메시지에서 병렬 실행. 각 에이전트에 위 스키마와 "원문을 끝까지 읽고 인용은 원문 그대로" 지시. 이 레포와 `~/.claude/skills`는 읽기 전용.
- [ ] **Step 2: 검증** — Run: `python3 -c "import json,glob; fs=glob.glob('research/registry-build/facts/*.json'); [json.load(open(f)) for f in fs]; print(len(fs))"` / Expected: `67`. 각 파일에 `directives`가 1개 이상이고 모든 `quote`가 비어 있지 않은지 같은 방식으로 확인.
- [ ] **Step 3: Commit** — `git commit -m "research: extract per-skill source facts for registry"`

### Task 4: 측면 분류와 registry.md 조립

**Files:**
- Create: `skills/writing-maestro/registry.md`, `tests/test_registry_real.py`

**Interfaces:**
- Consumes: Task 3 facts, `parse_registry`/`validate` (Task 1), `check_combo` (Task 2)
- Produces: 형식 절을 따르는 `registry.md` (Task 5 SKILL.md가 읽음)

- [ ] **Step 1: 수용 테스트 작성** — `tests/test_registry_real.py` (실제 `skills/writing-maestro/registry.md` 대상)

```python
def test_registry_valid():  # registry_check와 같은 validate, installed는 매니페스트 기준 → []
def test_known_conflict():  # check_combo(["general-writing","prose-naturalizer"]).ok is False
def test_bundle_paper_flow(): # check_combo(["paper-writing","academic-voice","general-writing"]).ok is True
def test_copy_plus_humanizer_precedence():
    r = check_combo(reg, ["copywriting", "humanizer"])
    assert r.ok and any(s == "humanizer" for s in r.precedence.values())
def test_clarify_stage_skills():  # interview-me, requirements-clarity, idea-refine, brand-profile, voice-builder, awesome-content-voice 각각 "clarify" in stages
def test_check_stage_skills():    # citation-verification, docs-sync-audit 의 stages 에 "check" 포함
def test_every_skill_has_primary(): # 모든 스킬 primary 비어 있지 않음
```
- [ ] **Step 2: 실패 확인** — Run: `python3 -m pytest tests/test_registry_real.py -q` / Expected: FAIL (파일 없음)
- [ ] **Step 3: 측면 목록 확정** — 67개 facts의 `directives.topic`을 모아 스펙 §4.3 초안 10개를 기준으로 병합·분리. 한 측면 = "두 스킬이 동시에 다르게 지시하면 결과가 흔들리는 결과물 속성". 각 측면 id·이름·설명을 `## 측면` 표에.
- [ ] **Step 4: 스킬 항목 작성** — `main=true` directive → 주 측면, `false` → 부 측면, `interactive=true` → 단계 `clarify`, `requires`/`forbids`/`commands` 그대로. 인용은 `근거`에. 묶음 표는 스펙 §4.5 초안을 facts의 `requires`로 확인해 확정. 앞부분에 범위(다룸: 과제 종류 4개 / 다루지 않음: 게시·발송, 비작문 과제) 절 추가.
- [ ] **Step 5: 통과 확인** — Run: `python3 -m pytest tests -q && python3 skills/writing-maestro/scripts/registry_check.py --registry skills/writing-maestro/registry.md --manifest research/install/2026-10-29-install-manifest.json` / Expected: all passed, `OK 67 skills`
- [ ] **Step 6: 충돌 표본 점검** — 주 측면이 같은 클러스터 3개를 골라 원문 인용을 다시 대조하고, 결과를 커밋 메시지 본문에 적는다.
- [ ] **Step 7: Commit** — `git commit -m "feat: add writing-maestro skill registry"`

### Task 5: 오케스트레이터 SKILL.md, feedback.md, 설치

**Files:**
- Create: `skills/writing-maestro/SKILL.md`, `skills/writing-maestro/feedback.md`
- Create symlink: `~/.claude/skills/writing-maestro` → `/Users/chan/Developer/Skills/writing-maestro/skills/writing-maestro`
- Modify: `README.md` (Current state 절에 오케스트레이터 위치·사용법 3줄)

**Interfaces:**
- Consumes: `registry.md` (Task 4), `combo_check.py` CLI (Task 2), `registry_check.py` CLI (Task 1)

SKILL.md 절 구성(스펙 §3, §3.1, §3.2, §4.4, §6을 절차로 옮김; design-maestro SKILL.md를 문체 기준으로):
1. frontmatter: `name: writing-maestro`, `description`: 작문 과제(새 글, 고치기, 검토, 코드베이스 문서)를 레지스트리 스킬 조합에 매핑하고 사용자가 고른 조합·개수만큼 시안을 병렬 생성해 넘기고 멈춘다 + 트리거 문구 예시.
2. 고정 규칙: Global Constraints 중 런타임 규칙.
3. 과제 해석 → 과제 종류 4개 판정, 범위 밖이면 한 줄 보고 후 멈춤 (Review Focus 2).
4. 레지스트리 읽기: 매 호출 `registry.md`, `feedback.md` 새로 읽기. 시작 시 `registry_check.py` 실행, 실패하면 오류 그대로 보고하고 멈춤.
5. 명확화 단계: 단계 `clarify` 스킬을 메인에서 사용, 생략 조건, 산출 파일 위치.
6. 조합 후보: §4.4 배제 순서, 후보마다 `python3 <이 폴더>/scripts/combo_check.py --registry <이 폴더>/registry.md --check-runtime ...` 실행, ok인 것만 후보. 실패 사유(실행 불가 포함)는 "제외"/"실행 불가"에 기록, 임의 대체 금지 (Review Focus 3). 지명 스킬 처리와 미등록 지명 (Review Focus 1).
7. 질문 1회: `AskUserQuestion` 두 질문(조합 multiSelect, 조합당 개수 1/2/3 + 기타). 조합 1개면 개수만, 검토면 조합만. 총합으로 답하면 앞 조합부터 배분 (Review Focus 5). 질문 불가 경로 §3.2.
8. 시안 생성: 출력 폴더 구조, 서브에이전트 지시 템플릿(스펙 §6 항목 + combo_check의 `precedence`/`ignored`를 "측면별 따를 스킬" 절로 그대로 옮김 + 검수 단계 스킬 + 원본 복사 규칙), opus·동시 실행.
9. 넘기는 형식: 스펙 §6 표.
10. 평가를 받은 뒤: feedback.md 갱신 규칙.

- [ ] **Step 1: SKILL.md, feedback.md(design-maestro feedback.md 머리말 구조, 사용자 기준·사이클 기록 비어 있음) 작성**
- [ ] **Step 2: 구조 검증** — Run: `python3 -c "import re,sys;t=open('skills/writing-maestro/SKILL.md').read();m=re.match(r'^---\n(.*?)\n---\n',t,re.S);assert m and 'name: writing-maestro' in m.group(1) and 'description:' in m.group(1);[sys.exit('missing '+k) for k in ['combo_check.py','registry_check.py','AskUserQuestion','writing-drafts','opus','feedback.md'] if k not in t];print('ok')"` / Expected: `ok`
- [ ] **Step 3: 설치** — `ln -s /Users/chan/Developer/Skills/writing-maestro/skills/writing-maestro ~/.claude/skills/writing-maestro` (이미 있으면 덮어쓰지 말고 멈춰서 보고). Run: `test -f ~/.claude/skills/writing-maestro/SKILL.md && echo linked` / Expected: `linked`
- [ ] **Step 4: Commit** — `git add skills/writing-maestro README.md && git commit -m "feat: add writing-maestro orchestrator skill"`

### Task 6: 시험 실행

**Files:**
- Create: `research/trials/2026-10-29/<case>.md` × 사례 수, `research/trials/2026-10-29/README.md` (요약표)

시험 사례 (스펙 §9 + Review Focus):
- A 새 글: 한국어 블로그 글(주제는 사용자에게 받거나 "AI 글쓰기 도구 고르는 법"). 개수 질문에 "총 5개" 응답 시나리오 포함.
- B 새 글: 단편 소설 장면 (story 묶음, `story` CLI 경로)
- C 새 글: 논문 초록 (msimchowitz 묶음)
- D 고치기: AI 티 나는 한국어 문단 교정 (원문 불변 확인)
- E 검토: 기술 설계 문서 검토 (`docs/superpowers/specs/...design.md` 대상, 개수 질문 없음 확인)
- F 지명: "unknown-skill로 써줘" → 미등록 처리
- G 범위 밖: "엑셀 수식 짜줘" → 범위 밖 한 줄
- H 문서 작업: 이 레포 README 개선 (레포 파일 불변 확인)
- I 질문 불가: `claude -p`로 사례 A 축약 실행 → 모든 후보 × 1

- [ ] **Step 1:** 사례마다 새 세션 또는 이 세션에서 `writing-maestro` 호출. 질문이 나오면 사용자가 답한다(사용자 부재 시 첫 후보 2개 × 1개로 답하고 기록에 명시). 비용을 고려해 시안 수는 조합당 1~2개.
- [ ] **Step 2: 사례별 확인 항목 기록** — 후보 조합 각각의 `combo_check` 결과(ok, precedence), 질문 횟수, 생성된 시안 수, 원본 파일 `git status`/해시 불변, 넘긴 표 형식, 이상 동작.
- [ ] **Step 3:** 실패 항목이 있으면 SKILL.md 또는 registry.md를 고치고 해당 사례만 재실행. 고친 내용은 기록에 남긴다.
- [ ] **Step 4: Commit** — `git add research/trials skills/writing-maestro && git commit -m "test: record writing-maestro trial runs"`
