# MISSION_PROTOCOL.md — 10_nn_training_and_example (Pool Size: 24)

**Video Namespace:** `videos/machine-learning/10_nn_training_and_example/`
**Run Dir:** `_pool/` (DB: `mission.db`)
**Scope Partition:** 5 scopes, ~7 slides each
**Pool Size:** 24 background subagents (saturate, refill on completion)

---

## 1. BINDING RULES — READ FIRST

1. Read `/home/codespace/ai_llm_slides/AGENTS.md` (project root) AND
   `/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/AGENTS.md`
   (this video) — follow both.
2. This protocol is the binding contract. Do not deviate.
3. All DB writes go through the helper:
   `/home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh`
   (stamps `datetime('now')` automatically).
4. Claim your scope at start:
   `scope-claim _pool/mission.db <scope_name> <your_agent_id>`
4. Complete with `scope-done` (or `scope-fail <reason>`).
5. Every work item you cannot honestly complete: `task-add` with detail
   or record blocker in scope note — **silent skipping is forbidden**.
6. **File-write limit: ≤75 lines per single Write tool call.**
   Use append mode for continuation.
7. Never commit. Never delete anything. Unsolicited files → `_pool/orphans/`.
8. Clock discipline: never write a remembered date — use the helper.

---

## 2. SCOPE DONE CRITERIA (MEASURABLE)

A scope is `done` IFF **every slide in the scope** has:
- `slide_NNN_recreated.pptx` in `recreated_pptx/build/` (judge-certified PASS)
- Its final-deck page replaced in `10_nn_training_and_example_final.pptx`
- DB row `gen_status=certified` (or equivalent terminal state)
- All evidence banked in `qa/slideNNN/`

---

## 3. PER-SLIDE PIPELINE (WORKER END-TO-END)

For each slide number N in your scope (1–34):

### 3.1 Source Research (Optional, Best-Effort)
- If the slide has advanced graphs/algorithms/datasets: web search via
  `mcp__agy-cli-mcp__agy_web_search` to verify library choice, algorithm,
  data. Save under `sources/slide_NNN_source/SOURCES.md`.
- Never block on research (operations.md). On auth failure: refresh once,
  retry, proceed on ratified plan.

### 3.2 Doc-Parse (Advisory)
- Run `scripts/parse_document.py` from `.agents/skills/doc-parse/` on
  `unique_slides/slide_NNN.jpg` → output to `analysis/parse/slide_NNN.parse.md/.json`
- If dense content: run `scripts/crop_cascade.py` per `parse-playbook.md`.
- Lane state recorded once; failed parse never blocks downstream.

### 3.3 Vision Analysis (Script 12)
- `python3 scripts/12_analyze_slides.py <unique_slides_dir> <analysis_dir>`
  (idempotent, skips existing `slide_NNN_raw.json`)
- Streaming always (operations.md). Check log for `finish=stop`.
- If `finish_reason=length` + `content=null`: raise max-tokens or re-run.

### 3.4 Text Validation (Script 13)
- `python3 scripts/13_validate_slides.py <analysis_dir>`
  (idempotent, retries only missing finals)
- Empty content → transient, re-run.

### 3.5 Content Gate
- Ready iff `validation.verdict ∈ {PASS, PASS_WITH_FIXES}` AND
  `recreatability_score ≥ 8` (pipeline.md).
- If fail: delete raw+final for that slide, re-run analysis→validation
  (range-scoped), cap 3 retries, then report/block.

### 3.6 Build (pptxgenjs)
- Write `recreated_pptx/build/slide_NNN.js` using patterns from
  `references/patterns/index.json` (read FIRST).
- House chrome: machine-learning family (measured from slide 3 reference).
  - Outer red frame: x=0.15,y=0.15,w=13.03,h=7.2, border C00000 1.5pt
  - Yellow badge: x=12.48,y=0.30,w=0.5,h=0.5, fill/line FFF9C4, bold 18pt 333333
  - Title box: y=0.28,x=0.6,w=12.13, centered
  - Badge numeral = N (file name = printed badge)
- Equations: 2D format (matplotlib mathtext → 600dpi PNG → addImage at
  `w=px/600`). Direction law + straight-bar law closed-loop checks MANDATORY
  before judging. OMML wrap post-cert (pattern omml-wrap).
- Graphs: Generated images per `graph-panel-generated` pattern (correct
  lib/algorithm/data). Single version — slide's own pptx HAS the graph.
- Run: `NODE_PATH=$(npm root -g) node build/slide_NNN.js` from project root.### 3.7 Render (Closed-Loop PIL Checks)
- `soffice --headless --convert-to pdf --outdir qa/slideNNN <pptx>`
  (private profile: `-env:UserInstallation=file:///home/codespace/lo_profile_<N>`)
- `pdftoppm -png -r 150 <pdf> qa/slideNNN/render`
- PIL-compare render vs original frame (1px = 1pt, scale ×2000/960):
  ink edges within ~4px tolerance. Iterate placement until pass.
- Gap-band assertions for z-order masking (building.md).
- Fix checker first, then re-run (building.md closed-loop discipline).

### 3.8 Visual Judge (image-analysis + visual-judge Skills)
- Comparison mode: recreation render (IMG1) vs original frame (IMG2).
- Frozen judge template per deck (ground-rules prelude from judging.md):
  (a) house template intentional, (b) contentless match, (c) video artifacts
  omitted, (d) typed-vs-handwritten MINOR, (e) 2D equations upgrade,
  (f) fidelity-only.
- Route: DEFAULT no-params (`images` alias). glm leg DEFERRED/BLOCKED.
- **MANDATORY VISION GATE — every vision call runs through the local gate
  `_pool/vision_gate.sh`** (the shared gateway is saturated; unwrapped calls
  hit the 270s hard wall and die):
  ```bash
  cd <video_dir> && ./_pool/vision_gate.sh timeout 540 \
    python3 /home/codespace/.agents/skills/image-analysis/scripts/analyze_image.py \
    <mode> <imgs...> --view "..." --capture "..." -p "$(cat judge_template.txt)" \
    --timeout 420 --rounds 1 --tries 1 > <out.txt> 2>&1
  ```
- **Wall: `--timeout 420` wrapped in `timeout 540`** (a 270s-style hard wall is
  usually a WALL artifact under gateway load; W4 doctrine — widen before
  banking debt). Probe first on an already-banked PNG (short wall 120s in
  `timeout 150`); a hang means sleep 300s and re-probe ONCE.
- Dispatch: background jobs in ONE Bash call ending `wait`. ≤2 concurrent per
  Bash call, ~15s spacing. Never call the script directly without the gate.
- Verdicts banked to FILES. Banned-route verdicts VOID.
- PIL adjudication MANDATORY before any fix (measurement outranks judge).
- Max 6 attempts then park slide, report.

### 3.9 Post-Passes (After Judge PASS)
- Equations: OMML wrap (`scripts/18_omml_wrapper.py` + manifest from
  render_eq sidecars). Apply to plain-named pptx. Verify 0-pixel-diff.
  Never LO-resave wrapped deck.
- Graphs: Already embedded in build (single version).

### 3.10 Certify & Final-Deck Replace
- On PASS: set DB `gen_status=certified`, `visual_check=PASS`.
- Replace page in `10_nn_training_and_example_final.pptx` via OPC
  byte-verbatim merge (`python3 merge_final_deck.py update <N> <pptx> <deck>`).
- **NEVER run two merges concurrently** — the script holds a fleet-global flock
  (`<deck>.lock`) and uses unique tmp names; concurrent writers corrupted the
  deck zip on 2026-10-27 (archived at `_pool/evidence/`). If a merge fails with
  "Bad magic number", the deck was raced: rebuild from placeholder + re-merge.
- Update ledger `final_deck_ledger.json` (placeholder|certified + md5s).

### 3.11 Release
- `scope-done` for scope when all slides certified.
- Heartbeat during long phases (every ~10-15 min).

---

## 4. LIVENESS CONTRACT (FLEET.MD)

- Claim at start, heartbeat after every step + every 10-15 min, release at end.
- `set` refuses writes claimed by live foreign worker.
- Dispatchers claim atomically (gen_status=building + worker launch same breath).
- Death evidence: ≥40 min ZERO file movement + DB row mid-state + stale claim.
- Process absence ≠ death for session-scoped agents.
- Sweep classifies building rows: live / ZOMBIE / unclaimed (40-min default).
- Storm: live workers' file activity = cheapest "provider back" probe.

---

## 5. COLLISIONS & HANDOFFS

- Two builders on one slide: claim-holder watches (poll ~10 min), active
  builder proceeds. Conflict-free knowledge = ONE notes file in watcher's
  scratch/QA (evidence-cited). Takeover triggers: (a) newest foreign artifact
  60-min stale, (b) certification with measured divergence VISIBLE, (c)
  RELEASED marker. Archive overridden build in slide's QA dir.
- Pre-contract workers: stand-down on fresh writes (read-only).
- Resume: verify what banked artifacts RENDER (md5-diff vs predecessor's
  last scratch render). Resume from RESUME log's NEXT line.
- Marker = LAST artifact (chain complete: reconstruct → 0-diff → judge →
  certify → marker).

---

## 6. PROVIDER STORMS

- Signature: batch same-duration failures (~19 min or ~65 min) with "upstream
  temporarily unavailable" = fleet event.
- Recovery: disk sweep → file-activity liveness (10 min fresh = alive) → ONE
  batch resume workers with banked-state summary + STORM-RESILIENCE clause
  (sleep 120s, retry 3×, atomic per-step banking, logs in project scratch).
- Probe-gated chain: cheap 8-token text probe (75s cap) → real call only on
  probe body → sleep 120 between cycles → max 3 attempts/phase.
- Banked-skip judge loops: skip transcripts with FINAL VERDICT.

---

## 7. VERIFICATION GATE (FINAL)

Run after all scopes `done`:
```bash
# Merge gate on fully-replaced deck
bash references/patterns/final-deck-merge/example.sh MODE=gate \
  <video_dir> 10_nn_training_and_example_final.pptx
```
- 0/N mismatched pages
- Merged render vs every source render (one LO session)
- Deliver `10_nn_training_and_example_final.pptx` + md5 + gate report

---

## 8. REPORT

Consolidated report: per-scope completion table, every task with resolution,
failure/wontfix rationales, open items, `_pool/mission.db` as complete ledger.
Recommend: APPROVE / RE-RUN OPEN SCOPES / NEEDS DECISIONS.

---

**WORKER PROMPT:** "Read `_pool/MISSION_PROTOCOL.md` and follow it exactly."

---

## 9. MERGE TOOL RULE (2026-10-27 23:07 — binding on all workers)

- The ONLY sanctioned final-deck merge tool is the project-root
  `merge_final_deck.py` (`update` mode). It was repaired at 23:07 and validated:
  34 slides / 117 media parts / 0 dangling rels (evidence: `_pool/evidence/`).
- `_pool/merge_page_safe.py` is SUPERSEDED and parked in `_pool/orphans/`
  (md5 `cff6e8402c46a360b122303c385f01a2`) — never invoke it; the root script also
  tolerates its `page{N}_*` media naming when cleaning stale parts.
- Current deck state (23:07 rebuild): 34 pages, 10 certified pages merged
  (1,5,6,7,8,12,13,14,23,26 — each build older than its PASS verdict).
  Slides with a FAIL but a `certified` ledger row are DECEIVING: 4,10,11,17,21,22,24
  — do NOT treat a ledger row as certification; the judge transcript decides.
- If a merge ever fails with "Bad magic number" the deck was raced: report it and
  do NOT self-repair by re-merging — the orchestrator rebuilds from placeholder.