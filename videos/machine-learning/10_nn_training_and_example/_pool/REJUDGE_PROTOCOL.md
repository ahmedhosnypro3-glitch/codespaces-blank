# REJUDGE_PROTOCOL.md — Re-analysis + Re-judge of All Certified Slides

**Mission:** For every CERTIFIED slide of `10_nn_training_and_example` (21 slides:
1,2,3,4,5,6,7,8,10,11,12,13,14,17,18,21,22,23,24,26,27):
1. RE-ANALYZE visually (fresh vision analysis + fresh text validation)
2. RE-RENDER the certified deliverable
3. RE-JUDGE with the frozen template (fresh transcript, real verdict)
4. Adjudicate + fix loop; re-certify; keep the final deck in sync

**Run dir:** `_pool/` — DB `mission.db`. Claim: `scope-claim _pool/mission.db <scope> <agent-id>`.
Done: `scope-done _pool/mission.db <scope> [note]`. Blocker: `scope-fail <reason>` + `task-add`.

**Binding rules:** project root AGENTS.md + video AGENTS.md + this file.
Supplementary (project root `scripts/17_worker_instructions.md`): build pattern,
judge template use, DB update duties. Pool rules in fleet.md hold (liveness,
storms, collisions).

**File-write limit: ≤75 lines per single Write tool call.**

---

## PER-SLIDE PROCEDURE (repeat for each slide N in your scope)

### Step 1 — Fresh visual analysis (NEVER touch certified specs)
```bash
mkdir -p analysis/reanalysis
python3 /home/codespace/ai_llm_slides/scripts/12_analyze_slides.py \
  unique_slides analysis/reanalysis --from N --to N --slides 10
python3 /home/codespace/ai_llm_slides/scripts/13_validate_slides.py \
  analysis/reanalysis --from N --to N --slides 10
```
- Output: `analysis/reanalysis/slide_NNN_raw.json` + `slide_NNN_final.json`
  (+ `slides_final.json`/`summary.md` derived in that dir — it is a SCOPED
  aggregate; the project-level `analysis/slides_final.json` remains the
  certified one and must not be clobbered).
- Certified `analysis/slide_NNN_*.json` are READ-ONLY for you. Never delete,
  never overwrite.
- If the vision call stalls (`finish=length`, `content=null`): re-run once;
  if still failing, raise `--max-tokens` to 32000 then 16000 retry; record
  the failure as a task and continue to Step 4 (judge) — the judge does not
  depend on the fresh analysis.

### Step 2 — Compare fresh analysis vs certified spec
- Read BOTH `analysis/slide_NNN_final.json` (certified) and
  `analysis/reanalysis/slide_NNN_final.json` (fresh).
- Write `qa/slideNNN/rejudge/analysis_diff.md` (≤75 lines/Write): for each
  field (slide_title, verbatim_text, layout.regions, visual_elements, colors,
  recreation_brief items) list MATCH / DIVERGENT + the exact divergence.
- A fresh analysis that MISSES content the certified spec has (or vice versa)
  is a JUDGE-ADJUDICATION INPUT, not an automatic defect. Frame pixels decide.
- If the fresh analysis reveals the certified build has a REAL content error
  (wrong equation, missing label, wrong value): record it in
  `qa/slideNNN/rejudge/findings.md` and fix per Step 5.

### Step 3 — Re-render the CURRENT deliverable
```bash
mkdir -p qa/slideNN/rejudge
cp recreated_pptx/build/slide_NNN_recreated.pptx <short-tmp>/slide_NNN_recreated.pptx
TMPDIR=<video_dir>/_pool soffice --headless \
  -env:UserInstallation=file://<video_dir>/_pool/lo_rejudge \
  --convert-to pdf --outdir qa/slideNN/rejudge <short-tmp>/slide_NNN_recreated.pptx
pdftoppm -png -r 150 qa/slideNN/rejudge/slide_NNN_recreated.pdf \
  qa/slideNN/rejudge/render
```
- The render must come from the CURRENT on-disk deliverable bytes (md5-check
  against the deck's embedded source if the ledger records it).
- If an OMML-wrapped variant was applied to the deliverable, render THAT file.
- PIL-check the PNG (dimensions 2000×1125, non-blank mean) before judging.
### Step 4 — Fresh visual judge (the actual re-judge)

**Tool:** `/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py`
(the skill is PROJECT-LOCAL: `.agents/skills/image-analysis/` in this repo —
NOT `~/.agents/skills/`; that path does not exist here and every call to it
dies rc=2 "can't open file").

**Route law:** DEFAULT route, NO `--models` flag. `glm-5.3-flash` second leg is
DEFERRED/BLOCKED — state that honestly in your report. `kimi-k3`, gemini, claude
are BANNED (a verdict from them is VOID).

**Frozen template (verbatim, byte-for-byte):**
```bash
cd /home/codespace/.agents/skills/image-analysis
PROMPT="$(cat /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/judge_template.txt)"
```
Never edit the template. Facts travel via `--view` / `--capture` values.

**Probe first** (cheap, short wall, on an ALREADY-BANKED PNG):
```bash
timeout 150 python3 analyze_image/analyze_image.py analysis \
  <banked.png> -p "Reply with the single word READY" \
  --timeout 120 --rounds 1 --tries 1 > _pool/probe_<N>.txt 2>&1
```
A valid body opens the window; a hang ⇒ sleep 300 and re-probe ONCE.

**The comparison call (IMG1 = recreation render, IMG2 = original frame):**
```bash
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
./_pool/vision_gate.sh timeout 540 \
  python3 /home/codespace/.agents/skills/image-analysis/scripts/analyze_image.py \
  comparison qa/slideNN/rejudge/render-1.png unique_slides/slide_NNN.jpg \
  --view "Slide NNN recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
  > qa/slideNNN/rejudge/judge_attempt_1.txt 2>&1
```
- **The gate is MANDATORY** — the shared gateway is saturated and unwrapped
  calls hit the 270s hard wall and abort with no verdict.
- Wall `--timeout 420` in `timeout 540` (a hard-wall Abort under load is
  usually a WALL artifact — widen before banking debt; W4 doctrine).
- Also probe through the gate (short wall `--timeout 120` in `timeout 150`).
- Dispatch in BACKGROUND jobs inside ONE Bash call ending `wait`; ≤2 concurrent
  per lane per Bash call, ~15 s spacing.
- The transcript MUST be banked to a FILE (stdout-only = no evidence).
- A verdict exists only if the body is coherent AND ends with a
  `FINAL VERDICT: PASS|FAIL ...` line. Timeout / empty / garbage = FAIL, retry.

### Step 5 — Adjudicate (PIL outranks prose)
For EVERY MAJOR/BLOCKER finding: measure the flagged region in BOTH the render
and the original frame with PIL before touching the build.
- Finding REFUTED by pixels → dismiss it, record the refutation with numbers in
  `qa/slideNNN/rejudge/adjudication.md`, and RE-ROLL the same frozen judge on
  UNCHANGED bytes for a clean PASS (banked as `judge_attempt_2.txt`).
- Finding CONFIRMED → fix it (copy-then-modify the build script; never edit the
  certified deliverable in place — write `slide_NNN_attemptK.js`, rebuild, and
  only replace `slide_NNN_recreated.pptx` after the new attempt passes).
- Small-text / dense-region claims: use a zoomed CROP-PAIR comparison at
  MATCHED effective scale (pattern `dense-region-crop-compare`) — never pass a
  full frame as IMG2 to a crop judge.
- The ORIGINAL frame is ground truth. The house chrome (red frame, badge,
  title box) is NEVER a defect. 2D equations are an upgrade, never a defect.

### Step 6 — Re-certify and sync the final deck
- If the deliverable bytes changed: re-merge the page under the flock:
  `python3 merge_final_deck.py update <N> recreated_pptx/build/slide_NNN_recreated.pptx 10_nn_training_and_example_final.pptx`
  (the script holds a fleet-global lock — never run two merges at once).
- Update `final_deck_ledger.json` (the script does it) and the DB row.
- Post-passes still apply after a change: OMML wrap for equation slides
  (`scripts/18_omml_wrapper.py` + manifest re-derived from the CURRENT pptx),
  graph embedding for advanced-graph slides.

### Step 7 — Close the slide
Write `qa/slideNNN/rejudge/REJUDGE_REPORT.md` (≤75 lines/Write) containing:
- fresh analysis verdict + validation score (from `analysis/reanalysis/`)
- analysis diff vs certified spec (MATCH/DIVERGENT summary)
- judge attempts: file names + verdict lines (quoted)
- adjudication: each finding → CONFIRMED/REFUTED + pixel numbers
- final state: PASS (no change) / PASS (fixed, attempt K) / PARKED (6 attempts)
- deliverable md5 + final-deck page status
Then `task-done` for the slide's tasks and `scope-done` for the scope.

---

## SCOPE DONE CRITERIA (measurable)
For EVERY slide in your scope:
1. `analysis/reanalysis/slide_NNN_raw.json` + `_final.json` exist
2. `qa/slideNNN/rejudge/` holds the fresh render + ≥1 judge transcript with a
   `FINAL VERDICT` line + `adjudication.md` + `REJUDGE_REPORT.md`
3. The deliverable is certified (judge PASS) or explicitly PARKED with reason
4. The final deck page matches the current deliverable bytes (ledger md5)
5. DB tasks closed

## BLOCKERS
Endpoint storm → sleep 120s, retry 3×, bank, continue. Provider error (502/504
from the HARNESS, not the vision gateway) → sleep 120s and retry the TOOL CALL;
if the AGENT dies, the scope is re-dispatched with this storm clause.
Report blockers via `task-add` + scope note — never silently skip a slide.

## NEVER
- Never delete certified artifacts, banked transcripts, renders or prior attempts.
- Never edit `judge_template.txt`, `analysis/slide_NNN_*.json` (certified),
  or another scope's slides.
- Never run two final-deck merges concurrently.
- Never commit. Never write outside this video namespace.

## MERGE TOOL RULE (2026-10-27 23:07)

- Merge ONLY with the project-root `merge_final_deck.py` (`update` mode).
  `_pool/merge_page_safe.py` is superseded and parked in `_pool/orphans/` — do not use.
- A `certified` ledger row is NOT certification: the judge transcript decides.
  Slides 4,10,11,17,21,22,24 currently carry FAIL verdicts — their pages are
  placeholder until a fresh PASS lands and the fix is re-merged.
- Re-merge a page ONLY when the deliverable bytes actually changed (md5 vs
  `final_deck_ledger.json`), and never run two merges concurrently (flock).
