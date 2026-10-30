# AGENTS.md — Video: 10_nn_training_and_example (Machine Learning Course)

## Project Context

This namespace is `videos/machine-learning/10_nn_training_and_example/`.
Parent project: ai_llm_slides (root AGENTS.md at `/home/codespace/ai_llm_slides/AGENTS.md`).
Course: Machine Learning (Zewail CSAI). No course-level AGENTS.md exists.

## Hard Stop: Human Review — COMPLETE

**Owner review of unique frames: APPROVED 2026-10-27** (in-session confirmation).
The unique slide set in `unique_slides/` (34 slides, `slide_001.jpg`–`slide_034.jpg`, named by
printed badge number) has been reviewed and approved. The HARD STOP is lifted.

`slides_index.json` written ONCE from confirmed files in printed-badge order
(no `new2old_mapping.json` needed — this is a clean namespace with no pre-approval
artifacts).

## Continuous Final Deck — Placeholder Initialization

Per slide-recreation pipeline law: at approval time, initialize
`10_nn_training_and_example_final.pptx` as a PLACEHOLDER deck:
- 34 pages (one per confirmed frame, in printed-badge order)
- Each page: original frame image full-bleed (presentable from day one)
- Pattern: `references/patterns/final-deck-merge/example.sh` (MODE=init)
- State ledger: `_pool/final_deck_ledger.json` (placeholder|certified per page, source md5s)

Subsequent certifications REPLACE pages in-place at the OPC package level
(byte-verbatim, never re-encode). Deck closes when all 34 pages are certified
and the merge gate (0/N pixel-diff) passes.

## Pooled Missions — Coordination Engine

**Engine:** `pooled-missions` skill (user scope). All coordination through a
per-run SQLite DB under `_pool/`.

### Run Directory

`_pool/` (inside this video namespace — NO writes outside
`videos/machine-learning/10_nn_training_and_example/`).

### Database

`_pool/mission.db` (schema from `pool-db.sh init`).

### Pool Size

**24 background subagents** — never foreground, never swarm. Spawn via
`Agent(run_in_background=true, subagent_type="coder")`. Saturate the pool.

### Scope Partitioning

Work items = the 34 slides (each slide = one end-to-end unit per
slide-recreation worker protocol). Partition into scopes of ~5–8 slides each
(natural boundary: slide number ranges). Per scope: claim → build → judge →
certify → final-deck page replace → release.

Register scopes via `scope-add` with explicit slide lists. Done criteria per
scope: every slide in the scope has a judge-certified `slide_NNN_recreated.pptx`
(PASS from visual-judge), its final-deck page replaced, DB row `gen_status=certified`.

### Protocol File

`_pool/MISSION_PROTOCOL.md` — written BEFORE any spawn. Every worker prompt:
"Read `_pool/MISSION_PROTOCOL.md` and follow it exactly."

Protocol must state:
- Read project root AGENTS.md + this video AGENTS.md and follow them.
- Claim scope: `scope-claim <db> <scope> <your agent id>`.
- Complete scope: `scope-done` (or `scope-fail` with reason).
- Done criteria (measurable): certified pptx exists + final-deck page replaced.
- Smallest correct change; no unrelated edits; never touch items outside scope.
- Blockers: `task-add` with detail or scope note — silent skipping forbidden.
- Clock discipline: every DB write stamped via helper (`datetime('now')`).
- Never commit; never delete — unsolicited files → `_pool/orphans/`.
- Per-slide run: analysis/validation (scripts 12/13), build (pptxgenjs per
  patterns), render (LO headless → 150dpi PNG), closed-loop PIL checks,
  visual judge (image-analysis + visual-judge skills), fix loop, certify.
- Post-passes: equations (2D mathtext→PNG + OMML wrap), graphs (generated
  images per graph-panel-generated pattern).
- File-write limit: ≤75 lines per single Write tool call.

### Recovery

Interrupted/dead workers → `Agent(resume=<agent-id>)`. DB is source of truth.
Drifted workers → stop, redispatch FRESH agent with DB rows for that scope.

## Parallel Skill Lanes (All Active Simultaneously)

### 1. image-analysis + visual-judge (Vision Lane)

- **Tool:** `scripts/analyze_image.py` from `.agents/skills/image-analysis/` (run
  from skill root or resolve path).
- **Route:** DEFAULT no-params route (`images` alias) — NEVER add `--models`.
- **glm-5.3-flash leg:** DEFERRED/BLOCKED (8/8 HangError @330s fleet-wide).
  Single-model default-route certificates are VALID but state "glm leg
  DEFERRED/BLOCKED".
- **Banned:** kimi-k3, gemini, claude routes (founder law).
- **Dispatch:** Background jobs inside ONE Bash call ending `wait`. ≤2 concurrent
  per lane per Bash call, ~15s spacing. Probe first (short wall 120s on banked
  PNG), then 270s walls wrapped in `timeout 300`.
- **Verdicts:** Banked to FILES at run time (stdout-only = no evidence).
  Banned-route verdicts VOID.
- **Judging:** Comparison mode (recreation vs original). Frozen judge template
  per deck (ground-rules prelude: house chrome, contentless match, video
  artifacts omitted, typed-vs-handwritten MINOR, 2D equations upgrade,
  fidelity-only). PIL adjudication mandatory before any fix (measurement
  outranks judge). 6 attempts max then park.

### 2. doc-parse (Parse Lane, Advisory)

- **Tool:** `scripts/parse_document.py` + `scripts/crop_cascade.py` from
  `.agents/skills/doc-parse/` (skill-local config at
  `scripts/.doc-parse-config`).
- **Crop cascade:** Automated per `parse-playbook.md` (anchor law, hard floors,
  transform math, budgets). Chat adjudicator for non-determinism (advisory,
  never a gatekeeper).
- **Role:** Analysis anchor for vision call, verbatim-text cross-check at
  validation, adjudication aid at judging, dense-slide crop cascade feed.
- **Never blocks:** Missing/failed parse records lane state once and proceeds.
- **Output:** `<video>/analysis/parse/slide_NNN.parse.md` + `.parse.json`.

### 3. Web Search (Source Research)

- **Tool:** `agy` CLI via `mcp__agy-cli-mcp__agy_web_search` (MCP).
- **Best-effort only:** Never a hard dependency (operations.md). On 401 after
  token refresh, proceed on ratified plan.
- **Mandate:** Not required per-slide (no video-specific source-research
  directive). Use for algorithm/library verification for graph slides,
  equation symbol confirmation, dataset references.
- **Output:** `sources/slide_NNN_source/SOURCES.md` + fleet `SOURCES_MAP.md` per
  `references/source-research.md` if research happens.

### 4. slide-recreation (Build & Pipeline Resources)

- **Patterns:** `references/patterns/index.json` — read FIRST before every
  build. Use applicable patterns, run companion checkers.
- **Building:** `references/building.md` + engine laws in `references/pptx-engine.md`
  (native bullets, rich-text traps, option-object mutation, dLblPos repair).
- **House Chrome:** Machine-learning family measured from slide 3 (reference
  render). Outer red frame `x=0.15,y=0.15,w=13.03,h=7.2` border `C00000` 1.5pt;
  yellow badge `x=12.48,y=0.30,w=0.5,h=0.5` fill/line `FFF9C4` bold 18pt `333333`;
  title box `y=0.28,x=0.6,w=12.13` centered. Badge numeral = printed number
  (file name = badge).
- **Equations:** 2D format law (stacked fractions, large Σ with limits,
  aligned sub/superscripts). Mechanism: matplotlib mathtext → 600dpi PNG →
  `addImage` at exact size (`w=px/600`). Direction law + straight-bar law
  mandatory closed-loop checks before judging. OMML wrap post-certification
  (pattern `omml-wrap`).
- **Graphs:** Advanced graphs via generated images (correct library/algorithm/
  data per slide). Pattern `graph-panel-generated`. Single-version rule:
  slide's own pptx HAS the graph; no `_graphed` variants.
- **Dependencies:** If owner supplies `slide_dependencies.json`, builds gate on
  parent certification; pre-phase packs while blocked.

## Environment Contract

| Concern | Value |
|---|---|
| Vision endpoint | `http://localhost:17844/v1` (IronRouter dist lane, streaming) |
| API key | `.analyze-image-key` at project root (mode 600); `IR_API_KEY` env override |
| Vision model | `images` (IronRouter virtual model) |
| Validation model | `validate_slides` (IronRouter model, 2026-10-21) |
| Doc-parse endpoint | From `.agents/skills/doc-parse/scripts/.doc-parse-config` (probe first) |
| LibreOffice | `soffice --headless --convert-to pdf` + `pdftoppm -png -r 150` |
| Private LO profile | Mandatory (`-env:UserInstallation=file:///...`) |
| TMPDIR | Redirected to project scratch (never host /tmp) |
| pptxgenjs | `npm install` (project root `package.json` has it) |

## Hard-Won Operational Facts (Do Not Relearn)

1. Always stream vision requests (non-streaming dies at ~60s).
2. `finish_reason=length` + `content=null` + filled `reasoning` = raise
   max-tokens OR re-run (some endpoints cap completions ~32k).
3. ~540 vision tokens/frame at 960px JPEG q4.
4. phash threshold 8, keep LAST frame of group (fully-built slide).
5. Analysis ~3–5 min/slide. Check `finish=stop` in log. Retry: delete
   `slide_XXX_raw.json` and re-run (idempotent).
6. Validation empty content = transient, re-run script 13.
7. YouTube blocks anonymous datacenter downloads — use `--cookies`.

## Evidence Discipline

- Never delete banked evidence (per-attempt builds, transcripts, renders,
  pre-fix backups, archived runs). Overwrite nothing certified; copy-then-modify.
- `qa/slideNNN/` trees for per-slide evidence. `_pool/orphans/` for unsolicited.
- Per-slide re-certification mandatory after any fix (judge template in
  `scripts/17_worker_instructions.md`).
- Final deck merge gate: 0/N mismatched pages, merged render vs every source
  render, one LO session. Deliver `10_nn_training_and_example_final.pptx` +
  md5 + gate report.

## Tool Installation

sudo allowed (no password) for any tool install needed by the pipeline
(ffmpeg, imagemagick, python packages, node packages, etc.).

## File Write Constraint

**Maximum 75 lines per single Write tool call.** Use append mode for
continuation. Applies to ALL file writes in this namespace.