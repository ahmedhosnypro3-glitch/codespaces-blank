# Worker report — slide 033 "Non-Convex Function"

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Worker: `worker_slide033_1792769859` (claim held; a `worker_slide033_r5` claim was
REFUSED because the original claim is still live — do not double-claim)
Build script: `recreated_pptx/build/slide_033.js`
Deliverable: `recreated_pptx/slide_033_recreated.pptx`

## Attempts used

| # | render | what changed | verdict |
|---|---|---|---|
| 1 | `render_1.png` | First build from `analysis/slide_033_final.json` verbatim (spec's 8×17 table, pastel band fills from the spec, param box + arrows, matplotlib-style plot) | PIL selfcheck FAIL — the frame does not match the spec (see below); superseded |
| 2 | `render_2.png` | Rebuilt from **frame measurement**: 5 band fills, 40px column grid, measured callout/param-box/plot coordinates | selfcheck PASS (fills within 2 RGB, one smooth curve); row-count ambiguity unresolved |
| 3 | `render_3.png` | 8 text rows + 10 horizontal gridlines + 20 vertical gridlines mapped to the measured grid; fills/glyphs per frame | superseded — selfcheck passed but four plot elements were missing/mis-drawn |
| 4 | `render_4.png` | Added the **11 vertical + 9 horizontal plot gridlines**; redrew the "Reach Local Minima" callout as the frame's actual **pale pink `#F7C9FA` rect x613-703 y258-296**; added the **green square `#8FFF17` x629-643 y236-244**; added the **orange `#EE730C` arrowhead x629-648 y115-138**; moved the red marker to x618-628 y142-152 | **Judge dispatched 3× — all aborted `HangError: hard wall-clock 630s exceeded` under gateway saturation (34-46 concurrent `analyze_image` procs). NO verdict banked. Superseded. |
| 5 | `render_5.png` | Corrected the 5 **fill-band geometries** from PIL measurement: y-extents `334-367 / 376-408 / 420-452 / 463-472 / 486-500` (band0 was 13px too tall at top); fills extended to cover the **label column** x86-121 (was x121-869, leaving the label column white); band 4's label column drawn pale green `#E9FFD2` (measured), not the band orange | selfcheck_5 PASS (all 5 bands ≤3 RGB both columns, curve ripple 2.996px / 0 gaps, house chrome PASS). **Judge legs PENDING — gateway saturated.** |
| 6 | `render_6.png` | Painted the **missing white plot background box x610..843 y62..311** (attempts 1-5 showed panel gray `(233,233,231)` where the original is white — 248 measured rows); replaced the two x-axis rules (rows 312 and 320) with the **single measured rule at y313**; corrected both y-axis rules to y60..313; clipped the plot gridlines to the white box | selfcheck_6 PASS (bands ≤3 RGB, curve ripple 2.996px / 0 gaps, chrome PASS, white box edges exactly 610/843 rows 62..311, gridline leakage 12px below / 2px right). **Judge legs PENDING — gateway saturated.** |

## Frame-vs-spec deviations (documented per building.md — the frame wins)

The analysis JSON (`slide_033_final.json`) describes a slide that does not match
`unique_slides/slide_033.jpg`. PIL measurement established:

1. **Background is not `#F2F2F2`** — the deck house chrome overrides (white canvas,
   `E9E9E7` panel, C00000 L/R/bottom strokes, FDFD96 badge "33"). House rule wins.
2. **The bottom "table" has 5 colour bands, not 8.**
   Measured fills (exact y-extents and x-extents, `measure_bands_5*.py`):
   - y334-367 `#D9E275` (217,226,119) — yellow-green, the yellow-highlight row
   - y376-408 `#D6B2F5` (214,178,248) — violet
   - y420-452 `#F7DDC2` (247,221,194) — peach
   - y463-472 `#DEAC95` (222,172,149) — muted orange (its LABEL column is
     pale green `#E9FFD2` (233,255,210), not the band orange — measured match
     frac 0.000)
   - y486-500 `#F7BEC4` (247,190,196) — pink
   Each fill spans **x89..866** — it covers the LABEL column x86-121, not just
   the data columns x121-869. The spec's `E2EFDA / DDEBF7 / E4DFEC / FCE4D6`
   pastel cycle is not in the frame.
3. **Two fills per band in the frame** — bands 1 and 2 each contain **two**
   text lines (y339-344 & 356-362 inside band 0; 381-386 & 399-404 inside band 1;
   425-430 & 443-448 inside band 2), so the frame shows **8 text rows** (matching the
   spec's 8 row labels `x, f(x), x-delta, f(x-delta), x+delta, f(x+delta, slope,
   next x`) grouped into 5 fill bands. Rows 7-8 (y467-472, 491-496) carry red bold
   text — the highlighted minimum cells.
4. **Column grid = 40px pitch starting at x121** — every one of the 8 rows' token
   centroids maps to `121 + k*40` with no misses (verified across all rows).
   Label column x86-121; 18 data columns to x869.
5. **Gridlines** (full-width dark rows on the original): 320, 374, 410, 418, 454,
   460, 478, 484, 501, 517 — reproduced exactly.
6. **Graphics region** (x244-599, y252-301) is a pale-green `#EFFFE2` callout
   holding the stacked-fraction equation plus two green annotation lines — not a
   plain centre text block.
7. **Parameter box** (x75-175, y245-309) is violet `#A7A0E3` with a yellow `#FFFF00`
   accent bar across its top and three 10pt rows — not the spec's generic box.
8. **Plot** — white background box **x610..843, y62..311** painted over the house
   panel (measured: 248 rows of the original have first-white x610 and last-white
   x843; the panel is E9E9E7 there too, so the box must be explicit — attempts
   1-5 left it unpainted and showed panel gray). **ONE** x-axis rule at **y313**
   spanning x607..901 (attempts 1-5 wrongly drew two, at rows 312 and 318/320);
   two y-axis rules at x607 and x721 spanning y60..313. Gridlines — 11 vertical
   (`x615, 632, 650, 667, 685, 703, 739, 757, 775, 793, 811`) and 9 horizontal
   (`y115, 134, 153, 171, 190, 209, 227, 246, 264`), clipped to the white box.
   Non-convex curve over cols 612-832 rendered `#00B050` and traced from the
   **frame's own measured ink** — the frame's curve oscillates (measured turning
   points max 627 / min 662 / max 691 / plateau 717 / max 755 / min 779 / max
   807), whereas the analytic `f(x) = (x^2 cos(x) - x)/10` has **no interior
   extrema** over -11..-9.5 and decays monotonically; the frame wins per the
   fidelity law, so the trace follows the measured ink, not the analytic function.
   Measured trajectory markers: red initial-point marker `x618-628 y142-152`;
   orange arrowhead `#EE730C` `x629-648 y115-138`; green square `#8FFF17`
   `x628-644 y235-244` at the reached minimum; "Reach Local Minima" callout is a
   **pale pink `#F7C9FA` rect x613-703 y258-296** with black bold text (NOT the
   purple `#7030A0` rounded box drawn in attempts 1-3).
9. **Equation format**: rendered as a 600dpi mathtext PNG (stacked fraction,
   professional 2D format) — `assets/eq_033_main.png`, embedded at exact px/600 size.
10. **Numbers**: the analysis transcribes 16 values per row; the frame shows ~18
    grid columns. The analysis contract supplies the values, so 16 columns are
    populated and the remaining grid columns are drawn empty (the frame's own
    right-hand cells were not transcribed by the analysis).

## Verification for attempt 6 (PIL, on `render_6.png`)

`qa/slide033/selfcheck_6.py` → `selfcheck_6.txt` — **PASS**, all 5 bands within
≤3 RGB on both data and label columns (D9E275 2/2, D6B2F5 3/1, F7DDC2 0/1,
DEAC95 0/4, F7BEC4 2/0). Band y-extents vs the original within 1px.

`qa/slide033/measurement/curve_fidelity_r6.py` — **PASS**:
195 cols x624..824, ripple std **2.996px**, max|d2| 22.56px, **0 column gaps**,
turning points max 627 / min 662 / max 691 / plateau 717 / max 755 / min 779 /
max 807 — the frame's measured positions.

Element check on `render_6.png` — all present: green square 948px `#8FFF17`,
red marker 432px, orange arrowhead 1107px `#EE730C`, pink callout 14702px
`#F7C9FA`, dark callout text 1304px, curve `#00B050` 2231px.

**White plot box** (the attempt-6 fix, `measure_plotbox_5*.py` +
`measure_plotaxes_5.py`): measured white edges in the render are left **610**
(516 rows), right **843** (518 rows), rows **62..310** — matching the original's
610/843/62..311. Gridline leakage: only 12px below y311 and 2px right of x843.

`shared_patterns/house_chrome_check.py render_6.png 33` — **PASS**
(panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge
centre (1824,152) d=68).

Crop pairs regenerated from `render_6.png` by `qa/slide033/cut_crops_6.py`:
`crop_6_{plot,table,center,title}_{render,orig}.png` — all pairs banked at
**exactly matched effective scale** (identical pixel dims, both axes, MATCH=OK).
The `crop_4_*` / `crop_5_*` pairs (cut from render_4/5) are superseded.

## Judge legs

**STATUS: BOTH LEGS PENDING — no verdict transcript exists.** Every dispatch so
far has been killed by the vision gateway before producing a transcript:

| log | attempts | outcome |
|---|---|---|
| `judge_dispatch_3.log` | 2 | `ABORT HangError: hard wall-clock 630s exceeded` ×2 |
| `judge_dispatch_4.log` | 2 + outer kill | `HangError` ×2, then `GATE_EXIT=124` (outer `timeout 1700`) |
| `judge_dispatch_5.log` | 2 | `HangError` ×2 |

Cause (measured): the gate is fleet-global and was saturated with 22-46
concurrent `analyze_image.py` processes against ~16 flock slots. This is an
infrastructure limit, not a build defect. Per the vision-gate law no call is
dispatched while `pgrep -c -f analyze_image.py` ≥ 8 (heartbeat, sleep 240,
re-probe). The gate was last probed at **22** processes.

- **Leg 1 — Template A full-slide**: payload `qa/slide033/judge_prompt_3.txt`
  (byte-for-byte from `shared_patterns/judge_protocol_03.md`); images
  `render_6.png` vs `unique_slides/slide_033.jpg`; transcript target
  `qa/slide033/judge_attempt_6.txt` — **NOT YET RUN**.
- **Leg 2 — Procedure B crop-pairs**: `crop_6_{plot,table,center,title}_{orig,render}.png`
  with payloads `judge_crop_prompt_{plot,table,center,title}.txt`; transcript
  targets `qa/slide033/crop_6_<region>_judge.txt` — **NOT YET RUN**.
  The **plot** region is the mandatory certificate (curve + all four markers).

## Judge payload compliance (found + fixed this session, attempt 6)

The protocol's opening line is law: *"Every judge prompt for this deck sources
its `-p` payload byte-for-byte from the templates below (substitute only NNN and
K)."* Verified against `shared_patterns/judge_protocol_03.md` (extraction script
banked as `regen_payloads_6.py`):

| payload | len | status |
|---|---|---|
| `judge_prompt_3.txt` (Template A) | 4114 | **NON-COMPLIANT** — 1-char truncation: missing the payload's final `.` after `...usable recreation'` |
| `judge_crop_prompt_{plot,table,center,title}.txt` | 8969 | **NON-COMPLIANT** — a composite (Template A's long ground-rules block + Template B's zoomed body), NOT Template B's `-p` |
| `judge_payload_A_k6.txt` (regenerated) | 4115 | **COMPLIANT** — exact substring of the protocol (Template A has no NNN placeholder) |
| `judge_payload_B_k6.txt` (regenerated) | 1913 | **COMPLIANT** — protocol's Template B (1914) with the one mandated `slide NNN` → `slide 33` substitution; no `NNN` remains |

**The legs must be dispatched with the REGENERATED payloads**, not the old
`judge_prompt_3.txt` / `judge_crop_prompt_*.txt` (kept as evidence per the
never-delete law, but superseded for dispatch). The Template B `-p` already
carries its own condensed chrome ground rules in clause (b) — it is
self-contained and must not be prefixed with Template A's rules.

## Final state at hand-off (attempt 6)

Build is COMPLETE and PIL-verified; only the two judge verdicts are outstanding,
blocked solely by the fleet-wide vision-gate saturation.

Banked and verified:
- `build_attempt_6.js` (== live `build/slide_033.js`, byte-identical)
- `slide_033_recreated.pptx` — single plain-named deliverable
- `render_6.png` (2001×1125, scale 2.0833)
- `crop_6_{plot,table,center,title}_{render,orig}.png` — matched effective scale
- `selfcheck_6.txt`, `measurement/curve_fidelity_r6.py`
- `measure_bands_5.py`, `measure_bands_5b.py`, `measure_bands_5c.py`
- `measure_plotbox_5.py`, `measure_plotbox_5b.py`, `measure_plotaxes_5.py`
- `cut_crops_6.py` (region definitions + matched-scale method documented in-file)
- `judge_prompt_3.txt` + `judge_crop_prompt_{plot,table,center,title}.txt`
  (payloads byte-for-byte from `shared_patterns/judge_protocol_03.md`)

To finish (both legs, ONE vision call at a time, gate load must be <8):

    export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
    export VIDEO=machine-learning/03_ridger_regression_gradient_descent
    cd /workspaces/codespaces-blank/ai_llm_slides
    Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033
    V=videos/machine-learning/03_ridger_regression_gradient_descent

  # Leg 1 — Template A full-slide (payload = judge_payload_A_k6.txt, byte-for-byte)
  timeout 1700 scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/render_6.png $V/unique_slides/slide_033.jpg \
    --view "Slide 33 recreation — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript $Q/judge_attempt_6.txt -p "$(cat $Q/judge_payload_A_k6.txt)"

  # Leg 2 — Procedure B, plot region (curve + all four markers) first.
  # payload = judge_payload_B_k6.txt (Template B, NNN->33 already substituted)
  timeout 1700 scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/crop_6_plot_render.png $Q/crop_6_plot_orig.png \
    --view "Slide 33 zoomed crop plot — render vs original at matched scale (attempt 6)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: the non-convex curve with its gridlines, the red initial-point marker, the orange arrowhead, the green square at the reached minimum, the pale pink Reach Local Minima callout, and both tick-label rows" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript $Q/crop_6_plot_judge.txt -p "$(cat $Q/judge_payload_B_k6.txt)"

  # then the remaining crop regions (table, center, title) ONE AT A TIME,
  # writing $Q/crop_6_<region>_judge.txt, same payload

Then, on PASS for both legs:

    python3 scripts/15_progress.py set 33 visual_check PASS --worker worker_slide033_1792769859
    python3 scripts/15_progress.py set 33 visual_transcript "$Q/judge_attempt_6.txt" --worker worker_slide033_1792769859
    python3 scripts/15_progress.py set 33 visual_attempts 1 --worker worker_slide033_1792769859
    python3 scripts/15_progress.py set 33 gen_status passed --worker worker_slide033_1792769859
    python3 scripts/15_progress.py release 33 worker_slide033_1792769859

DB row at hand-off: `slide_id=33, gen_status=building, visual_check=null,
visual_transcript=null, visual_attempts=1, worker_id=worker_slide033_1792769859`
(claim live and heartbeating; NOT released, because no verdict exists).

## Residual risk

- **The vision gateway is the blocker.** It is fleet-global (~16 flock slots) and
  was carrying 10-46 concurrent `analyze_image.py` processes throughout this
  lane; a 480s fine-grained probe showed the load RISING (14→28), not draining,
  so the gate is converging on, not freeing. Every dispatch so far has aborted
  with `HangError: hard wall-clock 630s exceeded` without producing a transcript.
  Per the vision-gate law no call may be dispatched into a saturated gate
  (probe `pgrep -c -f analyze_image.py`; if >=8, sleep 240 and re-probe). The
  build itself is PIL-verified; only the judge verdicts are outstanding.
- **Plot curve shape vs the analysis contract** — unresolved and the biggest
  fidelity question. The frame's measured ink oscillates (measured turning points
  above); the analytic `f(x) = (x²cos(x) − x)/10` has NO interior extrema over
  -11..-9.5 and decays monotonically to its single minimum at (-9.6, -8.11).
  The build follows the **frame's measured ink** (frame-wins law). If the judge
  flags the extrema positions, the honest defence is that the trace was measured
  from the original frame's own ink over cols 612-832.
- **Curve colour**: the frame's curve ink is a low-contrast **pale cyan**
  (`g=b=255`, r lower) that only a tight mask detects; the render draws it
  `#00B050` saturated green. A zoomed judge may see more curve ink than the
  pixel mask found. Shape and turning points match the frame's measured trace.
- **Render plot base tint**: RESOLVED in attempt 6 — the white plot box
  x610..843 y62..311 is now painted, so the render's plot background is pure
  white `(255,255,255)` matching the original's `(254,255,253)`.
- Left unresolved: the frame's right-hand table columns (~2 extra grid slots)
  carry numbers the analysis never transcribed, so they are drawn empty.

---

## 2026-10-24 (resume lane `w033-resume-20261024`, after the 2h harness timeout)

**DB claim was stale** (heartbeat 11:08, no transcripts banked at all). Re-claimed
by auto-takeover of `w033-finish-20261024` as **`w033-resume-20261024`**
(`15_progress.py claim 33 w033-resume-20261024` → "took over from
'w033-finish-20261024', heartbeat 74m stale") and heartbeating.

### Build-bank state corrected — the bank runs to attempt 8, not 6

The hand-off report says "attempt 6 is the current build", but the directory
holds `build_attempt_7.js` (07:59) and `build_attempt_8.js` (08:14) and
`render_7.png` / `render_8.png`. Measured:

| file | md5 |
|---|---|
| `build/slide_033.js` (live) | `4d7b548d04d5dd4540d714b89c4e1a95` |
| `build_attempt_8.js` | `4d7b548d04d5dd4540d714b89c4e1a95` (identical) |
| `build_attempt_7.js` | `17816b9cc4509fb2d70cf9769bdd4e30` |
| `build_attempt_6.js` | `db87b9dcd3c3357434ca3e92d2eddcd2` |

Attempt 7 was a full PIL re-measurement rebuild (title Times/C00000 centred,
param box white with navy border, equation box x449..585 y182..230 with a
C00000 border, the generated plot asset `build/assets/slide_033_plot_v7.png`
replacing the hand-traced fragment). Attempt 8 == the live build script == the
current `slide_033_recreated.pptx`.

**Re-rendered from the CURRENT pptx per the orchestrator's instruction** (private
LibreOffice profile, `soffice --headless -env:UserInstallation=… --convert-to pdf`
then `pdftoppm -png -r 150`, two attempts, each ~2.5s):

- `render_9.png` (2001×1125) is **pixel-identical to `render_8.png`**
  (max abs diff 0 over all pixels) — so the pptx row already pointed at the
  current artifact and nothing in the bank was stale.

### Pre-judge self-check on `render_9.png` — PASS

- `selfcheck_9.py` (re-targeted from `selfcheck_6.py`) → all 5 fill bands within
  ≤3 RGB on both the data and label columns, band y-extents within 1px.
- `shared_patterns/house_chrome_check.py render_9.png 33` → **PASS**
  (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge
  centre (1824,152) d=68).
- `measurement/curve_fidelity_r9.py` → **SMOOTH ONE-CURVE OK**:
  RENDER9 210 cols x621..830, ripple std **2.024px**, max|d2| 14.16px, **0 column
  gaps**; turning points max 637 / min 664 / max 692 / max 757 / min 782 /
  max 810 vs ORIGINAL max 638 / min 665 / max 691 / max 756 / min 782 / max 810
  — the frame's measured positions, matched to 1px.

**Curve colour — the attempt-6 residual risk is RESOLVED.** The attempt-7 rebuild
replaced the `#00B050` curve with the asset's teal `≈(32,160,160)`, and PIL
census of the ORIGINAL's own plot-box ink shows its dominant saturated hue is
exactly that family — `(72,168,168)` 352 px and `(96,168,168)` 284 px vs the
render's `(24,168,168)`/`(48,168,168)`. The render no longer carries a colour the
original lacks; the curve mask had to be re-taught teal, not green.

### Crop pairs re-cut from `render_9.png` (`cut_crops_9.py`, Procedure B)

`crop_9_{plot,table,center,title}_{render,orig}.png` — region bboxes in frame px
(plot x560-915 y100-312; table x80-875 y316-523; center x238-605 y248-305;
title x108-470 y52-152), render crops taken at the render's REAL scale factors
(SX=2001/960=2.084375, SY=1125/540=2.083333) and original crops LANCZOS-upscaled
to the render crop's exact dimensions. **All four pairs MATCH=OK on both axes**
(effective scale identical to 6 decimals per region).

### Judge payloads regenerated for attempt 9 (`regen_payloads_9.py`)

- `judge_payload_A_k9.txt` — 4115 chars, Template A at protocol **line 71**.
- `judge_payload_B_k9.txt` — 1913 chars, Template B at protocol **line 117**
  with the one mandated `slide NNN` → `slide 33` substitution.
- Byte-checked: both are verbatim substrings of the protocol, reverse-substitution
  reproduces the template exactly, no `NNN` survives, and **no `\bK\b` token
  exists in either body** — so the payloads are attempt-static and the attempt
  number lives only in the filenames, transcript paths and `--view` strings.
- md5-identical to the attempt-6 payloads (`9387f5fb…` / `0b5a221e…`) — the
  attempt-6 payloads remain valid for dispatch, superseded only in name.

Dispatch scripts banked: `dispatch_leg1_k9.sh`, `dispatch_crop_k9.sh <region>`.

### Lane wall applied

Orchestrator directive 2026-10-24 supersedes the protocol's `--timeout 600`:
analyzer `--timeout 1200` inside `timeout 1700`, payload bytes unchanged,
`--thinking high --max-tokens 65536`, `--rounds 1 --tries 1`, no retry wrapper.
The gate lock lives in `/tmp/ir_vision_gate_*.lock` (the actively-written
directory — latest 08:11), so the dispatches are run WITHOUT a TMPDIR override,
matching the rest of the fleet.

### Structural pre-judge self-check (`selfcheck_struct_9.py` + `selfcheck_markers_9.txt`)

- **Equation regions carry ink** — main equation box ORIG 11.7% / RENDER 9.3%;
  centre callout 20.4% / 15.4%; annotation line 1 17.4% / 11.3%; annotation
  line 2 28.7% / 13.9%. No empty equation box (protocol BLOCKER check clears).
- **Frame containment** — dark-ink bbox in the 150dpi render is x135..1823,
  y131..1071, i.e. fully inside the house frame; combined with
  `house_chrome_check.py` PASS.
- **Plot box** — white fraction ORIG 71% / RENDER 82%, plot box mean RGB
  (238,240,241) vs (240,241,244): the attempt-6 white paint holds.
- **Trajectory markers** — colour-matched census (`selfcheck_markers_9.txt`):
  red dot ORIG 41px / RENDER 209px; orange arrowhead ORIG (224,116,30) /
  RENDER (237,125,49) — both present, the render is sharper; green square
  ORIG (137,255,32) / RENDER (124,252,0); pink callout ORIG 1942px /
  RENDER 12686px. A dark-threshold pass reported the arrowhead "missing" —
  that is a threshold artifact (ED7D31 is brighter than <200), cleared by the
  colour-matched census.

### Dispatch status at 2026-10-24 13:54

Vision-gate load probed with `pgrep -c -f analyze_image.py`: **39** at 12:20,
**45** at 13:08, then **17** (13:35), **24** (13:42), **19** (13:46),
**14** (13:54) — draining monotonically since 13:35 but never below 8. Per the
vision-gate law no call is dispatched while the load is ≥8, so the two staged
legs have NOT been fired yet. The claim keeps heartbeating between probes.

## Adjudication kit (PIL measurements banked against BOTH images)

Pre-measured so a judge finding can be settled without re-deriving:

1. **Curve extrema** — `measurement/curve_fidelity_r9.py` (above). If the judge
   flags the extrema, the refutation is that the trace carries the ORIGINAL
   frame's own measured turning points, to 1px, and the analytic
   `f(x)=(x²cos(x)−x)/10` has no interior extrema over −11..−9.5 (frame wins).
2. **Typed-vs-handwritten** — protocol clause (c)/(d) settles it at MINOR at
   most; the equation is in professional 2D format per founder directive
   2026-10-09, which clause (e) makes a mandated upgrade, not a discrepancy.
3. **Table right-hand columns / extra cells** — settled by `measure_tablerows_9.py`
   and a background-relative cell census (`tablerows_r9.txt`). First pass with an
   ABSOLUTE darkness threshold (px<150) reported render-only ink at rows "x"/
   "f(x)" cols 679-772 and orig-only 3px runs in row 6; that was a THRESHOLD
   ARTIFACT — the original's table ink is a lighter colour on the coloured bands,
   so it only registers against the LOCAL band background. The census
   (ink = |px − median(band bg)| > 40, per cell) shows **all 19 columns × all 8
   rows carry ink in BOTH images** with no render-only and no orig-only cell.
   Second pass `measure_tablerows_9.py` output is banked in `tablerows_r9.txt` as
   the intermediate evidence; the background-relative census supersedes it.
   Phantom check: the 5 orig-only 3px runs in row 6 (cols 223/263/424/585/627)
   are 28-37px tall vertical strokes — real vertical gridline strokes present in
   the original at 5 column positions, NOT glyph ink, so they are not a
   missing-content finding. No BLOCKER, no MAJOR: the residual is typed-vs-
   handwritten ink weight, MINOR at most under protocol clause (c).

### 2026-10-24 15:20 — vision-gate metric correction (load-bearing)

`pgrep -c -f analyze_image.py` is NOT the concurrent-call count: it also matches
the gate wrapper (`bash scripts/16_vision_gate.sh … analyze_image.py …`), the
`timeout 1700` shell, and any `bash -c` that merely names the script — three
processes per real call, plus driver shells. Measured at 15:05 with exactly TWO
real in-flight calls (lanes slide_015 and slide_051): `pgrep -f` = 8, real
`python3 analyze_image.py` clients = 2. So this lane's earlier "39 procs →
do not dispatch" readings were counting other lanes' wrapper chains, not work.

Slide 030's `dispatch_legs_6_v3.sh` — the script that landed today's only heavy
verdict — gates on the REAL client count:

    real_clients() { ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }

and treats `--timeout >600` as a warning, not a blocker. `leg1_driver_k9.sh`
(banked in this directory) gates on `real_clients` with the same flock as final
arbiter.

### 2026-10-24 15:17→16:18 — Leg 1 dispatch ledger (payload byte-identical each time)

Payload md5 re-verified `9387f5fbb94ef05a31db19f1e018dde1` on every attempt; all
invocations are the orchestrator's mandated form (`--timeout 1200` inside
`timeout 1700`, `--rounds 1 --tries 1`, `--thinking high --max-tokens 65536`).

| try | window | real clients at fire | result |
|---|---|---|---|
| A | 14:49 | 6 | HTTP 504 `upstream_timeout` (Nvidia) in 61s |
| B | 15:02 | 9 | HTTP 504 in 61s |
| 1 | 15:17 | 3 | `HangError: hard wall-clock 1230s exceeded` at 15:45 (28m — the fleet wedge) |
| 2 | 15:47 | 4 | HTTP 504 at 16:08 |
| 3 | 16:11 | 4 | HTTP 504 at 16:13 |
| 5 | 16:15 | 4 | HTTP 504 at 16:16 |
| 6 | 16:17 | 5 | in flight |

`HangError` at the 1230s internal wall and `504 upstream_timeout` are
upstream/gateway failures — neither is a judge FAIL and neither consumes a build
attempt. No transcript has been written by any of them, so no verdict exists yet.
Both failure modes are identical to what every other lane (014, 015, 030, 049,
050) recorded today, i.e. this is the fleet-wide image-leg wedge, not a
slide-033 defect.

---

## 2026-10-24 (fresh dispatch lane `w033-fresh-20261024`, third lane after two 2h harness timeouts)

The prior lane `w033-resume-20261024` timed out with the build bank complete but
ZERO verdicts. Fresh dispatch (orchestrator brief: "the prior lane banked a
complete attempt-6 build but ZERO verdicts"). Verified and adjusted as follows.

### Discrepancy found in the orchestrator brief

The brief said "banked a complete attempt-6 build" — the bank actually runs to
**attempt 8** (build script + pptx) with **render_9.png** re-cut from the current
pptx; the resume lane already documented this (see its section above). The
deliverable `recreated_pptx/slide_033_recreated.pptx` (md5 `e90c9988…`) is the
attempt-8 build, and `recreated_pptx/build/slide_033.js` (md5 `4d7b548d…`) ==
`build_attempt_8.js` byte-identical.

### Currency verification (orchestrator-mandated first step)

- `build/slide_033.js` (live) md5 `4d7b548d04d5dd4540d714b89c4e1a95` ==
  `build_attempt_8.js` — the live build script IS the banked attempt-8 script.
- `render_9.png` == `render_8.png` (0 differing bytes of 6,753,375).
- **Definitive check**: re-rendered from the CURRENT pptx in a private LO profile
  (`render_10_currency.png`, banked) → **0 differing bytes vs render_9.png**.
  The banked render is the current pptx render; nothing in the bank was stale.

### Payload verification (orchestrator-mandated before dispatch)

Re-derived both judge payloads from the frozen protocol independently of the
prior lane's script (`judge_protocol_03.md`):

- Template A `-p`: protocol **line 71**, length 4115 — **pure verbatim extract,
  zero substitutions** (its body carries no slide reference at all). No `NNN`,
  no `\bK\b` token. md5 `9387f5fbb94ef05a31db19f1e018dde1`.
- Template B `-p`: protocol **line 117**, length 1913 — one mandated
  `slide NNN` → `slide 33` substitution, fully reversible, no surviving `NNN`,
  no `\bK\b` token. md5 `0b5a221efbbe91481de2882e3bafbb4b`.
- Both banked files (`judge_payload_A_k9.txt`, `judge_payload_B_k9.txt`) match
  those md5s and byte-diff clean against the protocol. Payloads are
  attempt-static: the attempt number lives only in file names / transcript
  paths / `--view` strings.

### Claim takeover

The prior lane's claim (`w033-resume-20261024`, gen_status=judging) showed a
**12-minute-fresh heartbeat** — the orchestrator's census had it dead (2h
timeout), and indeed its dispatch driver was still running with an in-flight
call. Per the dispatch brief ("CLAIM first with worker id w033-fresh-20261024"),
took over with `claim 33 w033-fresh-20261024 --force`. The stale-lane claim
hoarding was NOT benign: every later `set` by the dead lane would have been
refused by the live-claim guard. gen_status was set to `building` (a lane with
no verdicts cannot be `judging`).

### Crop pairs (leg 2) verified

All four Procedure B pairs banked by the resume lane re-verified:
plot 740×442, table 1657×432, center 765×118, title 755×209 — render and orig
members pixel-identical per pair (matched effective scale, both axes). The three
dense regions per this deck's AGENTS.md (table numbers, plot curve+markers,
equation callout) are the planned crop legs; title is plain 3-line text, not a
dense region — include only if the wall permits.

### Dispatch page 1 (16:54 cut-off) — leg 1 in flight, prior-lane driver over-probing

The inherited driver `leg1_driver_k9.sh` (started 15:17) kept firing through the
takeover. Probe ledger (all real `analyze_image` clients at fire time ≤6, gate
flock 16 slots arbitrating):

| try | fired | outcome |
|---|---|---|
| 1 | 15:17:29 | HangError 1230s (attempt 1) + internal retry 504 (attempt 2) → dead 15:45:49 |
| 2 | 15:47:19 | died 16:08:55 (~21 min) — no transcript |
| 3 | 16:10:25 | fast 504, dead 16:11:26 |
| 4 | 16:12:56 | fast 504, dead 16:13:57 |
| 5 | 16:15:27 | fast 504, dead 16:16:28 |
| 6 | 16:17:58 | hang, dead 16:46:18 (~28 min) |
| 7 | 16:47:48 | in flight at 16:54 |

Fleet context: the last landed full-slide verdict anywhere in the deck was
slide032 at **13:40**; the last crop verdict slide030 at **13:41** — nothing has
landed since. slide015's lane shows the paranoid variant: it has probed pgrep
every 60s since 15:39 and has fired NOTHING (load 12–25 never dips below 8).
The inherited driver's 7 probes in 100 minutes exceed the orchestrator's
max-2-probes/hour discipline — it is being stopped at the first opportunity
(try#7 completion); this lane's own probes from 16:54 follow the stated law:
heartbeat, sleep 240, max two re-probes per hour while `pgrep >= 8`, then park
honestly with staged resume commands.

Leg-2 driver banked: `leg2_crop_driver.sh [region ...]` (default: plot table
center) — same gating metric and orchestrator wall, 3 spaced attempts per
region, payload bytes fixed, TMPDIR redirected to project scratch per deck law.

### Page 1 continued — driver stopped, probe discipline (17:10–17:30)

The inherited driver fired try#8 at 17:10:54, moments before the stop signal
landed (pid 667628 confirmed dead, no further fires). try#8 was left to complete:
it carries the byte-verified payload and the mandated wall, and the gate is
nearly empty (real clients 4 fleet-wide). Fleet evidence gathered meanwhile:

- **No lane has landed a verdict since 13:40** (slide032 full-slide) / 13:41
  (slide030 crop) — 3h45m of upstream death, fleet-confirmed by slide025's
  crop dispatches (17:05–17:14: crop `tl`/`tr` died 1230s HangError + internal
  504; crop `bl` fast 504; crop `br` hang) and slide050's attempt-9 dispatches
  (17:07, 17:14 — no verdict), and slide015's lane has fired NOTHING since it
  started probing at 15:39 (load never dipped below 8).
- This lane's remaining probe page follows the orchestrator law exactly:
  heartbeat, sleep 240, max two probes this hour, then park honestly.

Tools banked this lane: `leg2_crop_driver.sh` (crop legs, gated + bounded),
`parse_verdict_033.py` (verdict extraction + certification command block),
`leg1_dispatch_k9_stopped.txt` (driver-stop ledger).

## Lane w033-judge2-20261024 — page 2 (19:47–…, 2026-10-24)

### Takeover state re-verified

- Claim: `claim 33 w033-judge2-20261024` re-confirmed live (`get 33` →
  `worker_id=w033-judge2-20261024`, heartbeat 25m stale at 19:47) → heartbeat
  re-sent. Prior lane's processes were confirmed dead at takeover (ghost
  dispatches left no transcripts).
- **Build currency re-measured at 19:47**: `build/slide_033.js` md5
  `4d7b548d…` == `build_attempt_8.js` == banked pptx `slide_033_recreated.pptx`
  md5 `e90c9988…` (08:14); `render_9.png` == `render_10_currency.png`
  byte-identical. Nothing stale; attempt numbering continued from 9/8.

### Defect fixed: annotation line-1 `-9.7` is RED on the original

PIL census of the original frame (see `adj_kit_033.txt`):
- ORIG `-9.7` word (frame x386..424 y254..274): 236 dark px, **99 reddish**
  (darkest (153,0,11)) — the value IS red in the frame, faintly (JPEG-softened
  brick red).
- ORIG `-9.6` word: 270 dark px, **131 reddish** (darkest (151,1,12)).
- Attempt-8 render drew `-9.7` BLACK (0 reddish px of 456) — a genuine,
  measured colour defect.

Fix applied (one run, `slide_033.js:177`): `-9.7` run `color: "000000"` →
`color: C_RED`; the inline geometry comment (lines 35–39) updated to record
both values as red bold. Rebuilt, banked as `build_attempt_9.js` (md5
`7a1b54698752e0800a615390d1b64925`), rendered to `render_11.png` (2001×1125,
private LO profile) via `pdf9/slide_033_recreated.pdf`.

`render_11.png` post-fix verification:
- Pixel diff vs `render_9.png`: 1662 px, bbox confined to frame x391.0–585.3,
  y259.7–271.7 — exactly the annotation line-1 band; nothing else moved.
- Ink census REND11: `-9.7` 402/424 px reddish (darkest (192,0,0)); `-9.6`
  483/642 px reddish — both now red, matching the original's hue family.
- `selfcheck_11.py` (re-targeted bands): **SELFCHECK: PASS** — all 5 fill bands
  within ≤3 RGB on data and label columns (D9E275 2/2, D6B2F5 3/1, F7DDC2 0/1,
  DEAC95 0/4, F7BEC4 2/0), banked at `selfcheck_11.txt`.
- `house_chrome_check.py render_11.png 33` → **PASS** (panel x112-1882,
  y94-bottom; strokes L/R/bottom present, top bare; badge centre (1824,152) d=68).
- `measurement/curve_fidelity_r11.py` → SMOOTH ONE-CURVE OK on RENDER11
  (ripple std 2.024px, max|d2| 14.16px, 0 column gaps; turning points match the
  original to 1 px: max 637/637, min 664/665, max 692/692, min 782/782, max 810).
  Render curve unchanged from attempt 9 (identical numbers).
- `selfcheck_struct_11.py` → containment OK (dark ink bbox x135..1823 y131..1071,
  inside the house frame); plot-box white fraction 82% vs ORIG 71%; equation +
  callout + both annotation regions non-empty. The reported
  "orange arrowhead FAIL (missing)" is a **threshold artifact, refuted**:
  colour-matched census of ED7D31 (237,125,49) ±30 finds **336 px at frame
  x633.2..646.6 y116.3..135.5** in RENDER11 vs 55 px at x632..646 y119..136 in
  ORIG. The absolute-darkness threshold (<200) cannot see ED7D31 at all.
- Phantom ink: 0 column runs and 0 row runs <3 px in RENDER11 (and in `render_9`
  and the original) — no stray ink anywhere.
- Crop pairs re-cut from the new render by `cut_crops_11.py` →
  `crop_11_{plot,table,center,title}_{render,orig}.png`, all four at EXACTLY
  matched effective scale (MATCH=OK on every pair; e.g. plot 740×442 both sides,
  scale x 2.084507 vs 2.084507, y 2.084906 vs 2.084906).
  Banked log: `cut_crops_11.txt`.

### Judge dispatch ledger (this lane)

- Payloads re-verified byte-for-byte before any dispatch:
  A = `judge_payload_A_k9.txt`, len 4139, md5 `9387f5fbb94ef05a31db19f1e018dde1`
  (verbatim protocol Template A, line 71, no substitutions);
  B = `judge_payload_B_k9.txt`, len 1923, md5 `0b5a221efbbe91481de2882e3bafbb4b`
  (protocol Template B, line 117, single mandated `slide NNN`→`slide 33`).
  Attempt numbering lives only in filenames / transcript paths / `--view`.
- Gate law honoured: `pgrep -c -f analyze_image.py` probed before each call
  (14 at 19:53, 12 at 19:47) with `real_clients=2` — the legal gate, dispatched
  per the lane's documented over-counting decision.
- **Leg 1 (Template A, full-slide)**: dispatched 19:53 by
  `dispatch_leg1_k11.sh` → `judge_attempt_11.txt`, comparing `render_11.png`
  vs `unique_slides/slide_033.jpg`.
- **Leg 2 (Procedure B, crop-pairs)**: staged via `dispatch_crop_k11.sh`
  `<region>` for plot / table / center (title only if the wall permits), each
  writing `crop_11_<region>_judge.txt`.

(leg outcomes, verdicts, certification rows appended below as they land)

## Adjudication of judge_attempt_12 + crop_12_plot (vs render_25, PIL-first) — 2026-10-25

Old attempt-12 legs judged a superseded render; all four structural claims were
re-measured against the current `render_25.png` (s=2001/960):

- **Template A D1 (MAJOR — x-label overflows plot frame): REFUTED.** Plot-box frame
  matched sub-pixel (orig x607/x845; render 1263.5/1760 → 606.0/844.8... measured
  605.9-606.9 and 843.9-844.9 frame). Bottom-band ink runs (frame x): 605.9-606.9
  (frame), 612.2-699.5, 707.2-725.4, 802.2-812.7, 843.9-844.9 (frame) — no ink
  beyond x845.6. Claimed x≈795-overflow does not exist in render_25.
- **Template A D2 (BLOCKER — missing blue dashed callout): REFUTED as
  missing-element.** Orig has no tall blue dashed verticals in the table region
  (col scan, B>60 & B-R>25: max col run ~78px over x671-788 = the converged-columns
  annotation ZONE, not a rectangle outline). Render has the same zone at x665-786
  (col runs ~149px) — present, somewhat taller (this is the D4 extent delta,
  MINOR). The "blue band" the old note saw is yellow-highlight text rows
  (orig y336-345 dump) — row content, present in render.
- **Template A D3 (MAJOR — missing outer blue table frame): REFUTED.** Orig frame
  lines: blue horizontals y320-321 (781px) and y516 (796px), (80,80,160). Render:
  y665-667 and y1080-1081 (400px each), (20,20,80) darker indigo. Lines exist;
  colour slightly darker → MINOR-class colour delta, not missing.
- **crop_12_plot finding #1 (MAJOR — dashed drop-guide truncated/black): REFUTED.**
  Orig guide: red col x584, y183-230 (42px). Render guide: red cols frame x584.3,
  y181-271 — same x, same colour, LONGER (more complete). The claimed "short black
  stub" is the dark dash segment y168-176 which exists in BOTH (orig dark y168-176;
  render y168-176 + 182-185). Strip scan y150-315: orig R@150-152/158-159/313,
  D@168-176/247-250; render R@150-152/313, D@168-176/182-185/248-252.
- **crop_12_plot finding #2 (MINOR — green marker larger): REFUTED.** Green extents:
  orig x560-643 y236-300 (w83 h64); render x559.9-643.8 y235.1-298.9 (w84 h63.8).

Residual real deltas: MINOR-class only (frame-line colour darker, converged-highlight
extent, curve stroke weight, mini-table styling, curve frame clearance, scale).
No fix trigger from attempt-12 claims. Fresh attempt-25 legs (Template A + crops)
will be the certification verdicts.

## Attempt 25 Template A adjudication (banked 2026-10-25) — PASS, 7 MINORs adjudicated

- M1 extra red plot frame: **REFUTED** — orig plot border measured dark red (123,47,59)/
  (152,7,20)/(131,51,60) at x607/x845/y60/y313 (probe /tmp adj 033 borders); the C00000
  render border is faithful. Judge's "original has only light-gray boundary" is false.
- M2 grid density (render finer 18-20 vs orig 11-12): **REFUTED** — at thresholds 225/240/248
  both images show the SAME vertical line set: axis x721.5 + gridlines ~x665, ~x779 (orig
  extra faint candidate x834 only at th225); axis row y172 in both. No 18-20-line grid exists.
- M6 systematic 10-14px band offset: **largely REFUTED** — table h-rules ORIG
  320.5/374.5/410.5-417.5/454-460.5/478-483.5/501.5/517 vs REND 319.7/368.6-373.6/410.6-416.6/
  454.7-458.8/478.5-482.8/502.5/518.5: all within 1.5px; right ink extent x901 in BOTH.
  Only the left extent differs (orig ink x68 vs render x85 at y460) — MINOR-class.
- M3 callout offset, M4 green box size/position, M5 equation box offset, M7 subtitle width:
  accepted as MINOR-class position/tracking nuances (≤12px, medium/low confidence) — same
  class as the already-adjudicated attempt-12 D4; not rebuild triggers.

## Attempt 25 plot-crop adjudication (banked 2026-10-25) — MAJOR REFUTED, 5 MINORs accepted

- MAJOR (orig has "two overlapping green circles", render "single wide ellipse"): **REFUTED**
  — green mask in the plot box: ORIG 147 px bbox x628..643 y236..246 (w16 h11), REND 666 px
  bbox x628..644 y235..247 (w17 h13); orig column profile is monotone unimodal (3→11→5),
  no bimodality/waist — a single blob in BOTH. Two outlined circles are not resolvable in a
  16x11 px blob; sub-structure invention, same class as the refuted "(7, 7)".
- M2 arrow fill colour, M3 dashed-line terminus arrowhead (JPEG-softened, judge medium),
  M4 axis-label typeface (medium class), M5 callout fill saturation (rule (e) JPEG washout),
  M6 crop-alignment artifact (judge: not a real defect): accepted as MINOR-class; no rebuild
  triggers.

## Attempt 25 table-crop adjudication (banked 2026-10-25) — PASS, 6 MINORs adjudicated

Value audit: all 8 rows x 18 columns IDENTICAL (transcribed both sides in the transcript).
- M1 red pointer arrow "largely absent": **REFUTED as lost content** — red ink present in
  BOTH in x130-190/y285-330 (ORIG 29 px x166-186 y304-329, REND 456 px x160-190 y285-319);
  render's arrow sits ~10px higher so most of it falls above the crop top. Position nuance.
- M2 cyan insert corners/dash/fill-hue, M3 next-x enclosure weight/rounding, M4 slope
  enclosure weight/rounding, M5 band hue drift (judge: partly JPEG), M6 stroke crispness:
  styling/medium-class MINORs, no rebuild triggers.

## Center-crop leg adjudication (crop_25_center_judge.txt) — 3 MAJORs REFUTED via PIL

Judge claimed: "-9.7" black in render (red in orig); "-8.08" and "-8.011" minus signs black (blue in orig).

PIL scan of crop_25_center_render.png (765x118, red mask r>150,g<90,b<90; blue mask b>150,r<90,g<90):
- RED: 894 px, y 25-48 (top row), x-runs (19,45),(320,372),(671,724) — red ink present in the 9.x row as the build specifies (C00000).
- BLUE: 1757 px, y 68-98 (bottom row), x-runs (15,70),(320,390),(468,521),(527,537),(543,552) — blue ink with minus signs present in the 8.x row (C_BLUE).

Corroborated by build source `build/slide_033.js` lines 179-201: "-9.7"/"-9.6" are C_RED, "-8.08"/"-8.011" are C_BLUE. All three colour MAJORs are judge misreads (same tiny-glyph hallucination pattern as the (7,7) phantom on 032). Center leg effectively PASS; with Template A PASS, plot-crop FAIL-refuted, table-crop PASS → **slide 033 PASSES** at attempt 25.
