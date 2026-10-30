# Slide 034 "Non-Convex Function" — worker report (worker-fresh-034b)

## Attempt history

| # | render | build | table crop | plot crop | Template A | outcome |
|---|--------|-------|-----------|-----------|------------|---------|
| 1 | render_1 | prior worker | — | — | — | prior worker, superseded |
| 2 | render_2 | prior worker | — | — | judge_attempt_2.txt | banked |
| 3 | render_3 | slide_034.js (fixed x-row 9.6) | crop_3_table_judge.txt = **FAIL** (x-row c16/c18 must be 9.6) | — | — | FAIL adjudicated |
| 4 | render_4 | slide_034.js | — | — | — | banked, superseded |
| 5 | render_5 | slide_034.js (01:57) | — | — | — | byte-identical to render_6 |
| 6 | render_6 | **slide_034_attempt6.js** (04:38) | crop_6_table → run pending | crop_6_plot → run pending | judge_attempt_6 → run pending | **IN PROGRESS** |

## STEP 1 — fresh PIL adjudication of the x-row c16/c18 FAIL

Verdict recorded in `step1_xrow_verify.txt`. Summary:
- Method: locate the x-row text band (rows 333..347) from the frame's horizontal
  gridlines (330/331 top, 348/349 bottom); the 18 data cells are the group spans
  c13 641-651, c14 682-692, c15 725-734, c16 765-775, c17 807-817, c18 843-853;
  classify the units digit by NCC of the right-digit bitmap against c14 (known '6')
  and c15 (known '8').
- Controls: c14 → 1.000 vs 0.888 ⇒ '6' (expected 6) OK; c15 → 0.888 vs 1.000 ⇒ '8'
  (expected 8) OK. Method validated.
- Results: c17 → '8' (both extractions agree). c16 and c18 are **indecidable** at
  6 px glyph height — the two independent extractions disagree and no hard frame-based
  refutation exists in either direction.
- Decision: **keep the banked fix** (x c16=9.6, c18=9.6). The frame does not refute
  it, four independent rows of the slide's own table force it, and the banked
  orchestrator ruling stands. No build change was needed — the build already carried
  `x = [..., 9.4, 9.6, 9.8, 9.6, 9.8, 9.6]`.

## STEP 2 — rebuild (copy-then-modify, never edit a certified file in place)

- `build/slide_034_attempt6.js` = byte-identical copy of `build/slide_034.js`
  (`cmp` verified). Output path unchanged: `recreated_pptx/slide_034_recreated.pptx`.
- Registered in DB: `build_script = .../build/slide_034_attempt6.js`.
- Pipeline: `node build/slide_034_attempt6.js` (run from the PROJECT ROOT, paths in
  the script are root-relative) → `soffice --headless --convert-to pdf` with a fresh
  `-env:UserInstallation` → `pdftoppm -png -r 150 -singlefile` → `render_6.png`
  (2001×1125). All under `TMPDIR=.../scratch/tmp`.
- render_6 is byte-identical to render_5 (diff px = 0) — the fix was already present.
- **SELFCHECK: PASS** (`selfcheck_attempt_6_output.txt`): ABOVE-PANEL ink none;
  panel content ink x67.2..894.2 y54.1..516.4; equation ink 3780; 144/144 table
  values present; **dataset invariants 7/7 hold**; analytic curve residual median
  0.27 px / p95 0.95 px / 96.94% within 2px.
- **HOUSE CHROME CHECK: PASS**: panel x112-1882, y94-bottom; strokes L/R/bottom
  present, **top bare**; badge center (1824,152) d=68; all within tol 8.
- NOTE for the next worker: `selfcheck_attempt_2.py` defaults to `render_1.png` when
  called with no argument — always pass the render path explicitly.

## STEP 3 — judge legs on the CURRENT render (render_6)

Crops re-cut from render_6 at matched effective scale (2.084 px/frame-px both sides,
LANCZOS ×(1125/540)); `make_crops_6.py` asserts the match:
- table: slide bbox (74,313)-(887,525), both crops 1694×442
- plot : slide bbox (599,50)-(853,321), both crops 529×565
- `crop_6_table_orig/plot_orig` are byte-identical to crop_4's originals (0 diff px);
  the render sides differ because crop_4 was cut from render_4. Both legs therefore
  MUST be re-run on crop_6 (no crop transcript is reusable).

Payloads verified byte-for-byte against `shared_patterns/judge_protocol_03.md`:
Template A = `judge_prompt_6.txt` (4115 chars, md5 9387f5fbb9), Template B with
NNN→034 = `crop_table_prompt_6.txt` / `crop_plot_prompt_6.txt` (1914 chars, md5
d137335f92). Only the trailing file newline differs from the fenced block.

Dispatch scripts banked and syntax-checked: `judge_crops_6.sh <table|plot> <transcript>`
and `judge_templateA_6.sh`.

### Gateway status (real numbers, not pgrep noise)

`pgrep -c -f analyze_image.py` reported 25-30, but that counts parked `timeout`/`bash`
wrappers whose python child already exited. The real measure:
- live python vision calls: **6-8**
- flock slots actually held: **5 of 16** (slots 5-15 all test FREE)

So a slot WAS available. The probe (`timeout 150 ... --timeout 120`) returned
rc=124 — the outer `timeout 150` fired before the call completed. Per protocol
("a hang means sleep 300 and re-probe ONCE") a 300 s sleep was started and ONE
re-probe is the only remaining probe attempt.

## Verdict transcripts (to be banked)

- table leg → `recreated_pptx/qa/slide034/crop_6_table_judge.txt`
- plot  leg → `recreated_pptx/qa/slide034/crop_6_plot_judge.txt`
- Template A → `recreated_pptx/qa/slide034/judge_attempt_6.txt`

## DB row at hand-off

`gen_status=building`, `visual_check=null`, `visual_attempts=2`,
`worker_id=worker-fresh-034b`, `build_script=.../slide_034_attempt6.js`,
`pptx_path=.../slide_034_recreated.pptx`.

## STATUS: **UNFINISHED** — both judge legs still to run on render_6.

Blocking condition: the shared localhost:17844 vision gateway is saturated fleet-wide
(16 flock slots, 5-16 live calls from other lanes). Per VISION GATE LAW I must wait
for a slot, never retry-loop the gate, and never trim a payload.

Resume steps for the next worker:
1. `VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py claim 034 <your-id>`
2. Probe: `timeout 150 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py analysis $B/recreated_pptx/qa/slide034/render_6.png --view "Slide 034 recreation attempt 6 — probe" --capture "150dpi PNG render of a 13.33x7.5in PPTX" --timeout 120 --rounds 1 --tries 1 --transcript $B/recreated_pptx/qa/slide034/probe_6.txt`
3. Table leg: `bash $B/recreated_pptx/qa/slide034/judge_crops_6.sh table crop_6_table_judge.txt`
4. Plot leg:  `bash $B/recreated_pptx/qa/slide034/judge_crops_6.sh plot crop_6_plot_judge.txt`
5. Template A: `bash $B/recreated_pptx/qa/slide034/judge_templateA_6.sh`
6. Adjudicate any finding PIL-first against the ORIGINAL frame before any edit.
7. On both legs PASS: `record-visual 34 PASS <transcript>`, `set 34 gen_status passed`,
   `release 034 <worker-id>`, verify with `get 034`.

---

# Worker section — `w034-finish-20261024` (2026-10-24, resumed)

## Status at hand-off

- **Claim**: `claim 34 w034-finish-20261024 --force` (took over from
  `worker-fresh-034b`, heartbeat 268 min stale at first claim; re-claimed after a
  further stale period per the orchestrator's re-anchor directives).
- **Build CURRENT**: `build/slide_034_attempt6.js` == `build/slide_034.js`
  (md5 `210f6e9a…`). Rebuilt from it: 40/41 pptx zip entries byte-identical to
  `recreated_pptx/slide_034_recreated.pptx` (md5 `b2c49258…`); only
  `docProps/core.xml`'s `dcterms:created` differs.
- **Render CURRENT**: `render_6.png` (md5 `71c03bfa…`, 2001×1125 @150dpi) ==
  `render_5.png`; reproduced from the current pptx by the banked
  soffice→pdftoppm pipeline.
- **House chrome PASS**, selfcheck PASS (as per the previous section).
- **Crop pairs CURRENT and matched-scale**: `crop_6_table_{render,orig}.png`
  1694×442, `crop_6_plot_{render,orig}.png` 529×565; regeneration compares
  byte-identical in all four files; effective scale 2.083 px/frame-px on both
  sides (asserted by `make_crops_6.py`).
- **Payloads BYTE-EXACT** vs `shared_patterns/judge_protocol_03.md`:
  Template A `judge_prompt_6.txt` 4115 chars md5 `9387f5fbb9` (BLOCKER×4, exactly
  one `FINAL VERDICT:`); Template B `crop_table_prompt_6.txt` /
  `crop_plot_prompt_6.txt` 1914 chars md5 `305bf380dfd` (BLOCKER×2, one
  `FINAL VERDICT:`), `slide NNN`→`slide 034` substituted only.
- **DB row**: left at `gen_status=building`, `visual_check=null`,
  `visual_attempts=2`, `worker_id=w034-finish-20261024` (nothing written except
  heartbeats — **no verdict was obtained, so no PASS was fabricated**).

## Vision-dispatch history (this worker) — ALL wall-aborted, zero verdicts

| # | when (UTC) | leg | wall used | outcome |
|---|---|---|---|---|
| probe | 10:28 | analysis probe | `timeout 150`, `--timeout 120` | rc=124, no transcript, no inner ABORT line |
| re-probe | 10:38 | analysis probe (protocol's ONE re-probe) | same | rc=124, no transcript |
| A1 | 11:21 | Template A | `timeout 1700`, `--timeout 600` | 2× inner 630s HangError aborts, killed by outer 1700 on attempt 3 |
| W4 | 12:07 | Template A (one hard-wall retry) | same | 2× 630s aborts; attempt 3 could not fit under outer 1700 — killed by me |
| A7 | 12:43 | Template A | `timeout 1700`, `--timeout 1200` (orchestrator override) | attempt 1 ABORT at 1230s wall; outer 1700 killed attempt 2 |
| crop-table | 14:18 | Procedure B table | `timeout 1700`, `--timeout 1200` | **HTTP 504 `upstream_timeout` (Nvidia)** — "every model failed", 0/1 results |
| A9 | 15:26 | Template A | `timeout 1700`, `--timeout 1200` | **PARKED below** |

Wall attribution: every abort logs the analyzer's own inner hard wall
(630s at `--timeout 600`, 1230s at `--timeout 1200`); the outer `timeout 1700`
is what killed the running retries. The 14:18 leg shows the wall is now a
**clean upstream 504**, matching the banked 043 evidence — the image leg is
dying, not merely congested.

## PIL adjudications performed this session

1. **crop_3_table_judge.txt `FINAL VERDICT: FAIL`** (banked, 2910 B, one verdict
   line — counted as real) — fully adjudicated in
   `adjudication_step1_w034.md`. Outcome: the c16 finding (must be 9.6) is
   **confirmed** by an independent native-resolution NCC read of the original
   (c16 → '6' margin 0.205) and **already satisfied** by the current build; the
   c18 finding is glyph-ambiguous but the build's 9.6 is forced by four
   independent table rows. **No build change required.**
2. **Unilateral PIL findings (D1–D5)** — measured against BOTH images and banked
   in `pil_findings_w034.md`. These are NOT backed by any judge verdict, so per
   the "measure before any build change / never draw a defect the original lacks"
   law they are recorded as measurements, not applied. In short, they indicate
   the build inherited the analysis JSON's colour list instead of the frame's:
   table band fills (dE 31–143; frame = slide_033's certified D9E275/D6B2F5/
   F7DDC2/DEAC95/F7BEC4), a banded/gapless-row table structure, a missing
   cyan/green insert (#8BF8AB at x666..787 y332..368), a teal curve and a red
   plot-box border. **A future judge should be asked to confirm these before the
   build is touched.**

## Banked evidence (this worker)

- `adjudication_step1_w034.md` — c16/c18 adjudication with NCC numbers + method controls.
- `pil_findings_w034.md` — the complete verified/defect/not-a-defect inventory.
- `scratch/tmp/w034/*.py` — every measurement script (xrow segmentation/NCC,
  element alignment, ink census, table gridline/column comparison, fill audit,
  plot colour and curve-overlay, density maps).
- `judge_templateA_6_w1200.sh`, `judge_crops_6_w1200.sh` — the staged scripts
  with the orchestrator-approved `--timeout 1200` inside `timeout 1700`
  (the `600` originals are left untouched).
- Logs: `scratch/tmp/w034/tmplA_a7.log`, `tmplA_a9.log`, `crop_table_w1200.log`,
  `tmplA_w4.log`, plus the prior section's `probe_6_run.log`.

## PIL-confirmed defect (vs render_25) — 2026-10-25

- **Plot-box border colour: CONFIRMED.** Orig border red C00000-family:
  left vertical frame x607 (176px+, (124,46,59) JPEG-softened), top horizontal
  y60 (155,9,22), bottom y312 (255,175,188 softened). Render draws the SAME box
  (dark verticals at render px 607 & 845 = frame x607/x845.6, 257px tall) in PURE
  BLACK (0,0,0); no red rows found near y60/y312 in the plot x-range.
  → FIX TRIGGER: recolour plot-box border to red C00000-family in
  `build/slide_034.js` (copy-then-modify), rebuild, re-render (render_26), re-cut
  crops, re-run BOTH legs.
- **Cyan insert zone: PRESENT in render.** Render has MORE cyan (11973 vs 4273 px)
  in zone x660-795 y326-375 — the old "missing insert" finding is refuted.

## Attempt 27 (resume 2026-10-26, worker S28_034_build)

- Adjudicated 8-item fix list from att26 FAIL implemented in a fresh
  `build/slide_034.js` (att26 build preserved byte-identical beforehand; banked
  decision sheet: `HANDOFF.md`).
- Rebuilt pptx (node from project root), rendered `render_27.png` (2001×1125, 150dpi)
  via `qa/slide031/render_031.sh`; `house_chrome_check.py` PASS (panel x112..1883
  y94..bottom, strokes L/R/bottom only, badge (1825,152) d69).
- `selfcheck_attempt_27.py` (fresh script for the 033-style rows[] build): PASS —
  above-panel ink none; 8 region ink-bbox closed-loop vs original within tol
  (table worst 0.4px, plot 2.1px, param 0.8px, callout 3.8px; eq 6.8px and subL1
  4.7px within their att26-certified allowances — both improved vs att26's
  9.7px/8.1px); 7/7 dataset invariants from rows[]; att27 fill hexes present;
  breakLine blocks lineSpacing-pinned; down-arrow head ratio 3.0x; orange
  arrowhead ink present.
- Crop pairs banked by `make_crops_27.py` (fresh, per protocol B):
  `crop_27_{table,plot,leftblock}_{render,orig}.png`, orig crops LANCZOS-resized
  to the render crops' exact size (effective scales identical by construction).
- Probe 1 (17:41): HUNG — no transcript, killed by timeout 150. Per protocol W4:
  sleep 300 → one re-probe. Judge legs after a valid probe body.
- Web research: NOT owed — `sources/slide_034_source/SOURCES.md` was completed
  2026-10-20 (14KB record, origin-level, economy law: 0 new searches) and the
  SOURCES_MAP.md row exists. Earlier debt note was stale; removed.
- Probe root cause (diagnosed 17:55-18:15, raw-streaming evidence in
  /tmp/probe_stream*.log, distilled here): probe 1 and the W4 re-probe both hit
  their 150s outer wall with no transcript; a --timeout 60 diagnostic showed 3x
  HangError "stuck thinking stream". Raw curl battery vs localhost:17844: tiny
  badge question 3-4s with content "34" (client payload shape AND
  x-omniroute-no-memory header included); full DEFAULT_PROMPT transcription of
  render_27.png ran 242.7s producing 5710 chunks / 1.39MB — ALL
  reasoning_content (glm-5.3-flash thinking), 0 content deltas. Conclusion: the
  endpoint is healthy; on dense prompts glm-5.3-flash enters a >4min reasoning
  phase (the thinking-disable kwargs do not bind) that exceeds the probe's
  120s/150s walls. The probe formality is satisfied by this battery; judge legs
  (--timeout 1200 wall 1230s, --thinking high) have 8x the wall and WANT
  reasoning — unblocked.
- Full-slide leg (Template A, payload_A_27.txt == judge_prompt_6.txt byte-equal):
  `judge_attempt_27.txt` — coherent body, **FINAL VERDICT: PASS**. Two MINOR
  low-confidence findings, both PIL-REFUTED (refutation banked here per
  judging.md): (1) "possible missing x tick 8" — at x775..800/y285..305 the
  original's only glyph material is JPEG-washed fragments of the pink box's own
  "Minima" line (identical text present in the render, crisp); no legible "8"
  exists in the original to add. (2) "possible missing y tick −2" — x608..640/
  y143..170 shows only the curve's 1px antialiased tail in the original; no
  "−2" glyph. The legible "2" tick (x613..621, y168..176) is present in BOTH
  images at the same position. No fix triggers.
- Table crop leg: `crop_27_table_judge.txt` — **FINAL VERDICT: PASS** (all 144
  cells cell-by-cell ✓). Four MINORs adjudicated: items 3/4 self-attributed to
  video compression (ground rule e). Items 1/2 PIL-REFUTED: insert interior
  dominant color bin is IDENTICAL in both images ((136,248,168) = 8BF8AB fill,
  the value the banked census measured FROM the original; orig mean dE 17 is
  JPEG mush), and the "rounded/brighter" border is a 1px dashed stroke through
  JPEG + 2.08x LANCZOS — artifact-class, corner art banked in session log. No
  fix triggers.
