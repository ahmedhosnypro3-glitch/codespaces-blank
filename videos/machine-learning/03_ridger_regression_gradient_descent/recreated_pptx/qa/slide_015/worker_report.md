# Worker report — slide 015, attempt 4 (build-first; judge PARKED on gateway congestion)

Worker `w015-buildfirst-20261024`, claimed 2026-10-24 08:42 UTC with `--force`
(took over from `worker_slide015`, heartbeat 191 min stale).

## Verdict

**BUILD-VERIFIED, JUDGE NOT RUN.** The build, render, crops and payloads are all
staged and byte-checked, but the vision gateway never drained below 8 concurrent
`analyze_image.py` during this run (peak observed 17, final 15), so no vision call
was dispatched. **No `FINAL VERDICT:` line exists for slide 015** and therefore,
by law, `visual_check` stays unset and the slide is NOT certified. Everything
needed to finish is banked; resume commands are at the bottom.

## Resume point (from prior lanes)

Resumed from the banked attempt-2 state: `qa/slide_015/build_attempt_1.js`,
`render_1.png`, `render_2.png`, the `build_eq_015.py` recipe and the crops/prompt
preparations for attempt 1. Attempt 2's `render_2.png` re-measured identical to
attempt 1's (`readjudicate_2.txt`); the build was already current. No banked
evidence was deleted; pre-change copies are banked as
`qa/slide_015/slide_015.js.attempt3_pre` and
`qa/slide_015/slide_015_recreated.pptx.attempt3_pre`.

## Build and render

| artifact | path | md5 |
|---|---|---|
| build source | `recreated_pptx/build/slide_015.js` | `eea7931bc53d0a9193123b3c28c8f435` |
| pptx deliverable | `recreated_pptx/slide_015_recreated.pptx` | `1bc9cd265612bfe7ff37f56466c8ecf4` |
| original frame | `unique_slides/slide_015.jpg` | `c6cbe225c783c6f86caf076cca26594f` |
| currency re-render | `qa/slide_015/render_3.png` | `57ef7bd99c8e90de7ee61073c440c5e2` |
| attempt-4 render | `qa/slide_015/render_4.png` | `3abacfed815d978ca8e8b6d5ba0b9391` |

**Currency proven, not assumed.** Rebuilding from `build/slide_015.js` reproduced
the banked pptx byte-for-byte (unzipped contents identical; only
`docProps/core.xml` timestamps differ), then `render_3.png` was cut from it.
`render_3.png` re-measured element-for-element identical to the banked
`render_2.png` (±1 px on every ink bbox in `readjudicate_3.txt`) — the residual
difference between the two PNGs is glyph-edge antialiasing only (7.8 % of pixels
differ, all at sub-threshold luma; every element bbox agrees to ±1 px).

`render_4.png` is 2001×1125 at 150 dpi (1 px = 1/200 in), matching the fleet
convention and the deck's 1px=1pt frame law (2001/960 = 2.0844 = 1125/540).

## Checks run (all PASS)

- **House chrome** (`shared_patterns/house_chrome_check.py`, banked
  `house_chrome_check_2.txt` → re-run on `render_4.png`):
  `PASS — panel x 112-1882, y 94-bottom; strokes L/R/bottom present, top bare;
  badge center (1824,152) d=68; all within tol 8`.
- **PIL element verification** — `verify_015_build.py` →
  `verify_build_4.txt`: every element's ink bbox and luma<150 census, compared
  at equal effective area (the render covers F²=4.34 px per frame px, so its raw
  count is scaled down before comparison). Fills sampled in BOTH images: cream
  `FBFDE5`, pink `F7D0D3`, peach `F7DCBE`, green `CFFFE3`, title red `C00000` and
  blue `00008B` all land exactly (err 0) on the render; the original's own
  JPEG-darkened samples are within the expected tolerance.
- **Frame containment** — `containment_015.py` → `containment_4.txt`:
  **0 spills** on the render. Every element sits inside its enclosing box, and the
  render is equal to or tighter than the original's own containment on all ten
  elements.
- **Ink spills past the house panel**: 0 (verified directly on `render_4.png`).

## What changed, and why

Three census/width findings were adjudicated PIL-first against both images
(`adjudicate_attempt_3.py`, `adjudicate_arrow_015.py`).

1. **`redbox_eq` was rendered 32 % too wide — FIXED.** The equation PNG's ink
   measured 128.4 pt against the original's 97 pt (`build_eq_015.py`'s
   `render_fit` only ever *shrank* from a hardcoded font size, so the width
   match the header comment claimed never happened). The equation now renders at
   **97 pt, ratio 1.00**, with ink bbox x83..177 against the original's x81..177,
   and the census ratio went from 0.59 → 1.02. It no longer crowds the
   "Get Best W…" sentence.
2. **No right-pointing arrow exists — REFUTED, nothing added.** The slide's
   analysis JSON claims an arrow after the normal-equation line. The original
   does carry faint diagonal ink at x503..510 y488..496, and attempt 2 nearly
   mistook it for an arrowhead. Pixel-first adjudication settles it: the
   original's ink in the gap between the equation's right edge (x510) and the
   green box's left edge (x547) is **zero pixels** at luma<200 over y466..521
   (`adjudicate_arrow.txt`). Those marks are the equation's final glyph — the
   closing paren at x501..502 y485..507 plus the trailing Y's stroke. The render
   has no ink in that gap either. **An arrow was therefore NOT drawn**: adding one
   would invent an element the original does not have, which is a defect, not a fix.
3. **Two residual width deviations are geometrically forced, not defects.**
   - `eq1_l1/l2/l3` render at w-ratio 0.88/0.87/0.90. Cream rect A's interior
     (y104..266) holds three lines with the original's own 16/11 pt gaps, which
     caps the ink at ~45 pt per line; the original achieves 695 pt width at a
     44 pt ink height, and mathtext's stacked `\frac` cannot reproduce that
     aspect without the three lines touching. This is the deck's documented and
     certified h-ratio 1.0..1.3 / w-ratio ~1.0 regime.
   - `solution` renders at w-ratio 0.76 with census ratio 1.61. The green box's
     interior is 333×40 pt; the original's solution ink is 332×33 pt
     (aspect 10:1), and a 332 pt-wide 2D stacked form is ~57 pt tall, which
     cannot fit a 40 pt box. Filling the box's width is impossible without
     spilling it.

   Both are recorded rather than "fixed", because the fix that would close them
   would violate frame containment or line separation.

## Equation assets rebuilt

`qa/slide_015/build_eq_015.py` was extended with a width-matching solver
(`INK_W` targets + a 2-iteration Newton solve on the composite, so coloured
parts found by FFT correlation widen the ink as they do in the real render) and
the table now writes to `build/assets/eq015_table.json` where the build script
reads it. The render canvas was reduced from 16×4 in to 12×2 in at 600 dpi —
9 equations × several 35 MB buffers exhausted the box's RAM at the larger size
and OOM-killed the build mid-run. Per-tag `gc.collect()` was added for the same
reason. Resulting widths: `redbox_eq` 97 (was 128), `peach_eq` 98, `deriv_l1` 572,
`deriv_l2` 408, `normal` 266, `solution` 251.

## Crop pairs (Procedure B, matched effective scale)

Five crop pairs cut from `render_4.png` by `cut_crops_4.py` →
`crops_4.txt`, one per dense region. Both images in each pair are resized to
`round(frame_px × 1125/540)` so `output_px/frame_px` is identical on both axes
(±0.003, never the 8 % that fabricates drift findings); the original is
LANCZOS-upscaled.

| region | frame bbox | out px | eff scale | ink r/o (luma<150) |
|---|---|---|---|---|
| eq_stack (3× J(W)) | x89..799 y100..271 | 1481×358 | 2.0830 | 27590 / 31337 |
| pinkbox (∂J/∂W=0 + sentence) | x73..710 y268..325 | 1329×121 | 2.0831 | 16046 / 20429 |
| peachbox (Remember + identity) | x783..898 y271..337 | 242×140 | 2.0862 | 2996 / 3304 |
| deriv_stack (gradient steps) | x71..518 y343..475 | 933×277 | 2.0826 | 16608 / 16167 |
| solution (closed-form W) | x545..893 y466..523 | 727×121 | 2.0831 | 7997 / 10883 |

## Payloads (byte-checked, frozen template)

`gen_dispatch_4.py` extracts Template A and Template B **verbatim** from
`shared_patterns/judge_protocol_03.md`, applies only the legal token
substitutions, writes the dispatch, then re-reads each file and re-derives the
payload from the frozen template for a byte comparison. All 6 payloads pass
(`judge_attempt_4.txt` 4115 bytes; five crop payloads 1914 bytes each). The
`\bK\b` rule is applied with word boundaries so **BLOCKER's K is never
corrupted** — verified: every payload still carries BLOCKER×2–4, MAJOR×2–5,
MINOR×2 and exactly one `FINAL VERDICT:`. No `<one-line description…>`
placeholder or `_K` token remains in any dispatch.

Substitution note: `render_K`, `probe_K`, `judge_attempt_K` and `crop_K_NAME`
carry an underscore-joined K that `\b` cannot see (`_` is a word character), so
those four path tokens are anchored and substituted first; the remaining
standalone prose K (`attempt K`) is matched with `\b`. The protocol's
`cd /home/ahmed/Projects/ai_llm_slides` was replaced with a
`git rev-parse --show-toplevel` derivation so the dispatch runs from any
checkout; no other byte of the commands or payloads changed.

## Banked artifacts (all under the deck root)

Deliverable, sources and renders as tabled above, plus:

| file | purpose |
|---|---|
| `qa/slide_015/readjudicate_015.py` | element re-measure, render-parameterised |
| `qa/slide_015/readjudicate_3.txt` | attempt-3/4 element bboxes vs original |
| `qa/slide_015/verify_015_build.py` | ink census + alignment + fills |
| `qa/slide_015/verify_build_4.txt` | its output on render_4 |
| `qa/slide_015/containment_015.py` | frame-containment check |
| `qa/slide_015/containment_4.txt` | its output on render_4 (0 spills) |
| `qa/slide_015/adjudicate_attempt_3.py` | pink/green/normal census scan |
| `qa/slide_015/adjudicate_3.txt` | its output |
| `qa/slide_015/adjudicate_arrow_015.py` | arrow adjudication |
| `qa/slide_015/adjudicate_arrow.txt` | its output (0 ink in the gap) |
| `qa/slide_015/build_eq_015.py` | equation builder with width solver |
| `qa/slide_015/cut_crops_4.py` | crop-pair cutter |
| `qa/slide_015/crops_4.txt`, `crops_4.json` | crop manifest + bboxes |
| `qa/slide_015/crop_4_*_render.png`, `crop_4_*_orig.png` | 5 crop pairs |
| `qa/slide_015/gen_dispatch_4.py` | payload generator + byte-check |
| `qa/slide_015/dispatch_4_probe.txt` | probe dispatch |
| `qa/slide_015/dispatch_4_judgeA.txt` | Template A full-slide judge |
| `qa/slide_015/dispatch_4_crop_<slug>.txt` | Template B × 5 |
| `qa/slide_015/dispatch_driver_4.sh` | staged driver (gate-policed) |
| `qa/slide_015/slide_015.js.attempt3_pre`, `slide_015_recreated.pptx.attempt3_pre` | pre-change copies |
| `scratch/tmp/eq015_attempt2_backup/` | pre-rebuild equation assets (18 files) |
| `scratch/tmp/widthmatch_probe*.py`, `sweep_eq1_015.py`, `calib_015_fast.py` | font-size calibration |
| `scratch/tmp/eq15_build_3.log` | equation builder log |

Attempt-2 evidence (`judge_prompt_1.txt`, `crop_prompt_1_*.txt`,
`build_attempt_1.js`, `render_1.png`, `render_2.png`, `reink_015.py`,
`colours_015.py`, `boxes_015.py`, …) is untouched.

## Resume commands (gate is congested; do not force it)

```bash
cd <repo root>
# 1) confirm the gateway is drained before ANY call
pgrep -c -f analyze_image.py          # must read < 8

# 2) drive the whole leg sequence, gate-policed (waits, heartbeats, re-probes)
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/dispatch_driver_4.sh all

# or leg by leg:
bash .../dispatch_driver_4.sh probe
bash .../dispatch_driver_4.sh judgeA
bash .../dispatch_driver_4.sh crop eq_stack      # then pinkbox, peachbox,
                                                 # deriv_stack, solution
```

Each leg writes its transcript to `qa/slide_015/`:
`probe_4.txt`, `judge_attempt_4.txt`, `crop_4_<slug>_judge.txt`. A leg counts as
clean only when its transcript ends `FINAL VERDICT: PASS` or every finding is
PIL-refuted; banked numbers above are the refutation record for the three
findings adjudicated here.

Certification sequence once both legs are clean (runbook
`scripts/17_worker_instructions.md:329`; there is no `record-visual` subcommand):

```bash
cd <repo root>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 15 visual_check PASS --worker w015-buildfirst-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 15 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/judge_attempt_4.txt --worker w015-buildfirst-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 15 gen_status passed --worker w015-buildfirst-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 15 w015-buildfirst-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py release 15 w015-buildfirst-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py get 15   # expect gen_status=passed, visual_check=PASS, worker_id=""
```

## DB state at hand-off

`gen_status=building`, `visual_check=null`, `visual_attempts=0`,
`worker_id=w015-buildfirst-20261024` (claim held, heartbeat current). No verdict
was recorded and none was fabricated.

## Honest limits

- No judge ran, so the census/width/containment numbers above are the
  *only* fidelity evidence for this build. They are strong for geometry,
  containment, colour and element presence; they cannot certify glyph-level
  accuracy inside the equations, which is exactly what Procedure B's crop legs
  are for.
- The three eq1 line widths and the solution width are knowingly below the
  original's, for the geometric reasons stated. A judge may still flag them;
  the refutation record is banked, but a judge insisting on a filled solution
  box cannot be satisfied without breaking containment.
- Gateway load was observed at 10–17 concurrent `analyze_image.py` over the
  whole run; it never reached the < 8 threshold, so no leg was attempted.

## APPENDIX — judge-s2-20261025 (2026-10-25): attempt-4 legA all-REFUTED adjudication + garbage-retry

Attempt-4 legA (render_4.png, verified CURRENT: fresh LO render of
slide_015_recreated.pptx is md5-identical to render_4.png, 0019627f1ec…)
returned FINAL VERDICT: FAIL with 3 MAJORs. All three REFUTED by pixel
measurement (full evidence: adjudicate_attempt_4.md; refuted transcript banked
judge_attempt_4_refuted_garbage.txt):
- "green term on extra line" — the original's ½ is a full-height STACKED
  handwritten fraction (1/bar/2, decoded at x166..200); the render's mathtext
  \frac{1}{2} is the same stacked mandated-2D form, and the green ink sits
  INSIDE each line's dark band (inline) in both images.
- "missing ⇒ arrow" — the gap (x501..547, y466..521) is ZERO-ink in the original
  (banked attempt-3 adjudicate_arrow.txt agrees). Nothing to reproduce.
- "missing Y underlines" — the runs are the BASES OF THE STACKED ½ (4 runs in L1
  = 4 stacked-½ occurrences; 2+2 in L2/L3 = leading+trailing ½). The zoomed Y
  at x412..418 has no stroke beneath it. \underline{W} already reproduces the
  only underlined symbols.

Disposition: garbage verdict on unchanged bytes -> garbage-retry of the SAME
frozen Template A payload (no new attempt; spent count stays 1 of 6). Retry
dispatched via dispatch_driver_4.sh judgeA (scratch/tmp/s2_015_legA_retry.log).
Certification path after a real PASS verdict body: 5 crop legs (eq_stack,
pinkbox, peachbox, deriv_stack, solution) via dispatch_driver_4.sh crop <SLUG>,
one leg at a time at pgrep -c -f analyze_image.py < 8, then visual_attempts=4,
visual_check=PASS, visual_transcript, gen_status passed, heartbeat, release.

## APPENDIX 3 — judge-s2-20261025 (2026-10-25): slide 015 PARKED

Third attempt-4 legA FAIL (judge_attempt_4.txt) claims: (a) duplicated blue
J(W) — ink census shows exactly ONE J(W) cluster per line; (b) text/boundary
collisions — containment_015.py reports 0 spills. Both refuted. With 3 garbage
re-invokes burned on identical bytes and every claim refuted by pixel/doc-parse
evidence (adjudicate_attempt_4.md, adjudicate_arrow.txt), the slide is PARKED:
no coherent verdict is obtainable on this render, the cert cannot be written,
and the 6-attempt judge cap is not exhausted (1 spent) but the garbage-retry
cap is. Resume = re-dispatch dispatch_4_judgeA.txt (NOT dispatch_driver_4.sh —
its load() integer test is buggy and sleep-loops) with fresh eyes, then the 5
crop legs. DB last_error carries the park note; gen_status stays 'building'
because no verdict chain exists to mark passed.
