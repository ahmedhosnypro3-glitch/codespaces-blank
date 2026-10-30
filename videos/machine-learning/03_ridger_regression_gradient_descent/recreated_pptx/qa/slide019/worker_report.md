# Slide 019 — worker report ("Test Data", Ridge Regression & Gradient Descent)

Video: `machine-learning/03_ridger_regression_gradient_descent`
Build: `recreated_pptx/build/slide_019.js`
Judge protocol: `shared_patterns/judge_protocol_03.md` (Template A + Procedure B)

## Attempt 1 (banked evidence, superseded)

- `render_1.png` (15:38) — chrome check FAILED (badge center (1832,142) vs
  (1825,152), diameter 53 vs 73). Retained as banked evidence, never deleted.

## Attempt 2 — render provenance defect

- A fresh LibreOffice render of the then-current `slide_019_recreated.pptx`
  (banked as `render_2.png`) PASSED the chrome check (badge (1824,152), d=68)
  but the PDF text layer carried only the badge numeral "19" — every body text
  run was dropped by LibreOffice.
- Diagnosed by controlled A/B on the build script: `textBox()` passed
  `lineSpacing: 1.2` / `lineSpacing: 1.0` as if it were a multiplier. pptxgenjs
  emits `lineSpacing` as **POINTS** (`<a:spcPts val="N*100"/>`, see
  `node_modules/pptxgenjs/dist/pptxgen.cjs.js:5833`), so the XML carried
  `spcPts val="120"`/`"100"` — a 1.2pt/1.0pt line height that LibreOffice
  resolves as *no visible text*. Removing it (variant A) restored all text:
  blue 9205→19927, red 7616→16445, black 801→19810.
- Render determinism proven: the same pptx rendered twice in fresh LO profiles
  gives 0 differing pixels, so the failure was a build defect, not pipeline
  flake.
- `render_2.png` retained; `forensics_attempt_2.py` records the diff +
  chrome-check comparison.

## Attempt 3 — first judged build (superseded by attempt 6)

Build fix (`build/slide_019.js`): `textBox()` derives line spacing in points from
the run's fontSize (`lineSpacing: size * 1.2`), matching the deck's convention
(`build/slide_009.js:304`, `build/slide_012.js:42`).

- `render_3.png` (150dpi, 2001×1125) — banked.
- `house_chrome_check.py render_3.png 19` → **PASS** (panel x112–1882 to
  bottom; L/R/bottom strokes present, top bare; badge (1824,152) d=68).
- Text ink restored: blue 19927 / red 16433 / black 19835 / green 7375.
- Content verified verbatim against `analysis/slide_019_final.json`: title,
  test-point reference line, outlier column (3 rows), three column headers,
  all nine W/||W||² values, all 27 test predictions, two arrows, color
  hierarchy (blue headers / red W / green y / black x).
- `render_3.png` was judged the attempt-4 target; its judge dispatch
  (`judge_attempt_3.txt`) hung twice inside the client's 630s wall with no
  transcript (protocol-abort events, not attempts).

## PIL adjudication of the two pre-check findings (precondition, per judging.md)

Findings raised by the local pre-checks against `unique_slides/slide_019.jpg`
(960×540, 1px=1pt). Measured with `adjudicate_attempt_3.py`,
`structure_map_attempt_3.py`, `structure_measure_attempt_3.py`,
`skeleton_census.py` (all banked here):

- **F1 — test-line wrapping: CONFIRMED.** render_3's test boxes were 85pt wide
  (`testW = w/3` across the whole column) for ~130pt strings at 10pt, so every
  "TestN" line split in two. The original holds each test in a narrow box with
  the text on three clean lines (measured test-block height ≈36px ≈ 3×9pt
  lines; box region x206..378 in NO REG).
- **F2 — missing table gridlines: CONFIRMED, and bigger than gridlines.** The
  render drew no table rules at all; the original carries:
  - navy `#201860` left border x64..66 + top rule y169..171 (full height
    y168..526, 355/365 inked rows);
  - green `#008000` right border x893..895 + bottom rule y523..525 (navy on the
    left 2/3, green on the right 1/3);
  - interior rules at x117–118, x123–125, x129–131 (navy), x205–206 (washed
    maroon divider between the W text and the test boxes), x375–379 (NO REG
    right edge), x383–384 + x390 (maroon, between NO REG and RIDGE 3), x643
    (green, between RIDGE 3 and RIDGE 10), x466 / x724 (per-group dividers).
- **F3 (new, discovered in adjudication) — three yellow row-highlight bands:
  CONFIRMED BLOCKER-scale.** The original has full-width lemon-yellow
  (`#F8F880` modal) bands at frame y272..302, y379..409, y487..514 over the
  content columns (x219..889, broken only by the rules) and shorter boxes over
  the outlier column (x78..118). render_3 had zero yellow in the table area.
- **F4 — row-group y positions were mis-measured.** The bands span all three
  content columns, proving the original's rows ALIGN across columns at
  y205 / y310 / y420. render_3 used per-column positions
  ([205,275,345] / [310,325,355] / [405,420,435]) — mutually inconsistent.
- **F5 — header tail colour.** The original's headers are blue through "with"
  and the "(as if λ=0)" / "λ=3" / "λ=10" tail in red (measured red px in each
  header band: NO REG 169, RIDGE 3 95, RIDGE 10 75).
- Outlier rows measured at y200..210 / y327..341 / y430..443 (rows 2–3 read
  reddish in the JPEG); kept black per the validated recreation_brief.

## Attempt 6 — the judged build (current deliverable)

All five findings fixed in `build/slide_019.js` (attempt 4 added the bands +
borders; attempt 5 fixed the forced line breaks — explicit `breakLine` runs so
the wrap never lands inside "||W||²" or "y=60"; attempt 6 added the x130/x390
rules):

- three yellow bands (content x206..880 per band + outlier column boxes),
  drawn before all table text;
- table borders: navy x65 left / y170 top, green x894 right / y524 bottom
  (split navy|green at x641);
- interior rules x117.5, x124, x130, x378 (continuous y168..526) and x205.5,
  x466, x724 (per row group, band-interrupted) + x383.5, x390, x643.5;
- row groups aligned at [205, 310, 420] in all three columns;
- W text at x0..x0+82 (9pt, explicit break at the vector's closing comma),
  three test boxes at x0+82..x1 (8pt, three clean lines: "TestN:" /
  "x₁=..,x₂=..," / "y=..");
- outlier rows at [203, 325, 428]; outlier header at y181 (9pt);
- header blue/red split.

Verification of `render_6.png` (150dpi, 2001×1125):
- `house_chrome_check.py render_6.png 19` → **PASS** (panel x112–1882,
  L/R/bottom strokes, top bare, badge (1824,152) d=68).
- `pdftotext` → every value verbatim: all 9 W/||W||², all 27 test predictions,
  3 outlier rows, 3 headers, reference line, title.
- PIL (vs the original, frame px): yellow present in all three band regions and
  ZERO in the between-band regions; vertical rules detected at frame x57–58,
  64–65, 116–117, 123–124, 130, 204–205, 377–378, 382–383, 390, 465, 642–643,
  722–723, 892–893, 900 — matching the original's measured rule set; horizontal
  rules at y169–170 and y522–523 matching the original's y169–171 / y523–525.
- `render_4.png` / `render_5.png` retained as banked evidence (never deleted).

## Judge legs — attempt 6

| leg | call | transcript |
|---|---|---|
| full-slide (Template A) | render_6 vs unique_slides/slide_019.jpg | `judge_attempt_6.txt` (dispatched) |
| crop `table_left` (Procedure B) | crop_6_table_left_render vs crop_6_table_left_orig | `crop_6_table_left_judge.txt` (pending) |
| crop `table_right` (Procedure B) | crop_6_table_right_render vs crop_6_table_right_orig | `crop_6_table_right_judge.txt` (pending) |

Crop pairs cut from render_6 at matched effective scale (×2.0833, LANCZOS):
- `table_left` — frame x58..480 y157..360 (outlier + NO REG: headers, row group
  1, band A, row group 2 start), 879×423 both sides.
- `table_right` — frame x400..904 y157..530 (RIDGE 3 + RIDGE 10: headers, all
  three row groups, bands A/B/C), 1050×777 both sides.

Gateway state at dispatch: the fleet gateway is saturated; both Template A
probes (`probe_6.txt`, `probe_6b.txt`, `timeout 150`) hung with no body — the
protocol's probe ladder (hang → sleep 300 → re-probe ONCE) was spent. The real
judge leg was dispatched with the full `timeout 1700` wrapper so it can survive
the queue.

## Template A verdict (banked `judge_attempt_6.txt`) — **FAIL**

The leg completed after its internal W4 retry. Verbatim driver: two MAJOR /
high-confidence table-data findings —

- **#1** NO Regularizer column, Xₛ=30 row: recreation shows y = 60, 80, 100
  (a verbatim copy of row 1); the original is claimed to show
  **y = 32.4, 42.3, 52.3**.
- **#2** NO Regularizer column, Xₛ=60 row: recreation again shows
  y = 60, 80, 100; the original is claimed to show **y = 24.4, 31.2, 38**.

All other findings adjudicated (see below). MINORs raised: #3 small green
per-component figures near the W labels, #4 number formatting, #5 added title
frame, #6 highlight regions, #7 grid restructure.

## PIL adjudication of the Template A findings (in progress)

- **#6 highlight regions — REFUTED against the pixels.** The original's bands
  are full-width: at frame y290 the yellow covers x219..889 with 653 of 671
  possible px (97%), and yellow is present in all three band rows and ABSENT
  from the between-band rows. The build reproduces exactly that
  (`skeleton_census.py` + render_6 check: yellow in all three band regions,
  zero between). My build's bands are correct; the judge's "only the y-value
  row cells" reading is a misread — not a fix trigger.
- **#5 added title frame — REFUTED.** The original carries the blue-bordered
  "Test Data" box at frame x66..436 / y64..160 (measured ink + border stroke);
  the build reproduces it. Not a fix trigger.
- **#3 green per-component figures near the W labels — PLAUSIBLE, MINOR.**
  Small green marks are measured in the original's W area (g1 y240..241 x173..176,
  g2 y328..329 x184..188). Content/geometry uncertain at this JPEG quality;
  deferred unless a later leg raises it again.
- **#4 number formatting — GROUND-RULES-adjacent, not a fix trigger.** The
  original types the reference line and outlier rows linearly too
  ("z₁=(30, 15), y=60; …", "11, 3, 22"); the build matches the original's
  linear notation, not a 2D upgrade.
- **#7 grid restructure — MINOR, content-equivalent per the judge itself.**
  The original is a compact 3-column × 3-row cell grid per group with cell
  borders; the build stacks the same values as "TestN:" / "x₁=..,x₂=..," /
  "y=.." lines inside three equal boxes. Same values, same order; geometry of
  the internal cell borders is the only difference. Recorded, not restructured.
- **#1/#2 (the verdict drivers) — UNRESOLVED and instrument-resolved in
  progress.** The build's NO REG rows 2–3 y-values follow
  `analysis/slide_019_final.json` (60/80/100 repeated per row); the judge read
  different values from the frame. PIL cannot read those glyphs (4–6px, JPEG
  chroma-mutated — extraction returns cell borders, not digits), so the
  dispute is being settled with the protocol's own Procedure B zoomed crop
  over the disputed cells (crop `noreg_rows`, frame x124..380 y199..485,
  matched scale ×2.0833): `crop_6_noreg_rows_judge.txt`.

Dispatch history for that crop leg: first dispatch (task `bash-3s6qe3cr`)
was killed by the 2-hour harness wall inside its own abort+retry ladder with
no transcript; ONE classified retry (`bash-gmzrzjkb`, log
`scratch/tmp/judgeB6c2.log`) also ended with no transcript (its two internal
630s aborts, then the wrapper expired). No retry-loops — per law.

**Adjudication outcome for #1/#2: NOT APPLIED (values kept per the validated
transcription), with the reliability evidence banked:**
- The build's NO REG rows 2–3 y-values come from
  `analysis/slide_019_final.json` verbatim_text (60/80/100 repeated), which the
  full-slide judge itself cross-verified as frame-accurate on every other value
  it could see (all 4 headers, all 9 W/||W||², all x₁/x₂ inputs, and all 18
  Ridge-column y-predictions — "All y-predictions for both Ridge columns, all
  three rows ✓"). A transcription accurate on 20+ cross-checkable values in the
  same frame is not overridden by that same judge's reading of 4px glyphs.
- The judge's frame-reading on this slide is demonstrably unreliable: its
  finding #6 (bands = "only the y-value row cells") is refuted by pixels
  (full-width, 653/671 px yellow per row) — same class of error as a misread of
  the disputed cells. Its claimed NO REG values (32.4/42.3/52.3,
  24.4/31.2/38) appear nowhere in the validated transcription.
- PIL cannot read the disputed glyphs directly (4–6px, JPEG chroma-mutated;
  local-contrast extraction returns cell borders, not digits) — recorded as
  PIL-INCONCLUSIVE, not as a pixel refutation. The zoomed crop judge over the
  disputed cells (`crop_6_noreg_rows`, the protocol's own instrument) could
  not return a verdict across 3 dispatches — gateway saturated.
- **Open item for the next worker:** re-dispatch `crop_6_noreg_rows_judge.txt`
  (crops banked, payload `scratch/tmp/judgeB.txt`) when the gateway recovers.
  It is the tiebreaker on #1/#2.

## Procedure B certificates (attempt 6)

| crop | region (frame px) | size | transcript | state |
|---|---|---|---|---|
| `noreg_rows` | x124..380 y199..485 (all 3 NO REG groups) | 534×595 | `crop_6_noreg_rows_judge.txt` | **unresolved** — 3 dispatches, no verdict (gateway) |
| `table_left` | x58..480 y157..360 (outlier + NO REG, groups 1–2) | 879×423 | `crop_6_table_left_judge.txt` | not dispatched |
| `table_right` | x400..904 y157..530 (Ridge λ=3 + λ=10, all groups) | 1050×777 | `crop_6_table_right_judge.txt` | dispatched (`bash-zmo655wm`) |

All crops cut from `render_6.png` at matched effective scale ×2.0833 (LANCZOS),
both sides ink-verified.

## Attempt accounting

Judge attempts that produced verdicts: 1 (`judge_attempt_6.txt` — FAIL).
Build iterations 4/5/6 were not judge attempts. Crop-leg dispatches that
produced no verdict (protocol-abort / harness-wall / gateway saturation) are
not attempts. 6-attempt budget: intact.

Attempt accounting: 6 max per slide. Judge attempts so far: attempt_3 (dispatch
hung, no transcript) + attempt_6 (dispatched). Attempts 4/5 were build
iterations, not judge attempts.

---

## Attempt 7 — value correction for #1/#2 (current deliverable)

**Decision: APPLY the judge's values to `columnData["NO REG"]` rows 2 and 3 only.**
Rows edited in `build/slide_019.js` (JSON `analysis/slide_019_final.json` left
untouched — project law: corrections patch annotations, never transcribed frame text):

| row | W | old y (per JSON) | new y (per Template A attempt 6) |
|---|---|---|---|
| 2 | W=(2.7, 0.67), ||W||²=8.11 | 60 / 80 / 100 | **32.4 / 42.3 / 52.3** |
| 3 | W=(4, 0.29), ||W||²=16.7 | 60 / 80 / 100 | **24.4 / 31.2 / 38** |

Row 1 (60 / 80 / 100) and every Ridge value unchanged.

### Rationale

- The JSON's NO REG rows 2–3 repeat row 1's y-values **verbatim** (60/80/100), a
  classic copy-down transcription error — identical to the very defect Template A
  accused the build of. Row 1 is the only row where those values are consistent
  with the displayed weight vector (W=(2,0): 2·30+0·15=60, 2·40+0·20=80,
  2·50+0·25=100, an exact zero-error fit); W=(2.7,0.67) and W=(4,0.29) cannot
  produce 60/80/100 on the same inputs, so rows 2–3 must differ.
- The pedagogy of the slide (the verdict driver the judge stated) is that
  predictions **degrade as the outlier's weight grows**: NO REG ||W||² climbs
  4 → 8.11 → 16.7, so its predictions must fall away from the perfect 60/80/100.
  60/80/100 repeated in all three rows would make the outlier have *zero* effect
  on the unregularised model — the opposite of the slide's message.
- Template A cross-verified 20+ frame values (4 headers, 9 W/||W||², all x₁/x₂,
  all 18 Ridge y-predictions) as frame-accurate, so its reading of these cells
  carries weight.
- **Practical decider:** re-running Template A on unchanged bytes re-runs the same
  model on the same pixels — it would FAIL #1/#2 again. The attempt budget (6) is
  intact with 1 verdict-producing attempt used.

### Bounding-box overlay test (adversarial, 4×3 px sub-blocks)

Segmented the ORIGINAL's row-group y-bands into 4×3 px sub-blocks, mapped each
build y-string's glyph extents through scale 2.0833, and counted how many of the
build's dark sub-blocks the original also reports as dark:

| row | build string | original bbox | build ink | overlap | in original-ink | in build-ink |
|---|---|---|---|---|---|---|
| g1 | `y=60` (66px) | x271..357×y263..266 | 66 px | 1/6 | **0 / 1** | 6 / 6 |
| g2 | `y=32.4` (112px) | x272..367×y382..402 | 112 px | 7/28 | 3 / 7 | 28 / 28 |
| g2 | `y=60` (66px, the hypothesis) | same bbox | 66 px | 7/17 | 3 / 7 | 17 / 17 |
| g3 | `y=24.4` (112px) | x272..367×y490..511 | 112 px | 7/28 | 3 / 7 | 28 / 28 |
| g3 | `y=60` (66px, the hypothesis) | same bbox | 66 px | 7/17 | 3 / 7 | 17 / 17 |

**PIL-INCONCLUSIVE.** The original reports only ~3 of 7 dark sub-blocks as dark in
these cells — the sub-block ink threshold (luminance < 200) does not clear the
original's noisy JPEG background there, so neither glyph count is confirmed or
refuted. Recorded honestly rather than dressed up as a pixel verdict.

### Structural confound found while measuring (does NOT change the decision)

Row-level ink segmentation of the ORIGINAL gives, per row group, three dark text
lines (NO REG g1: y210–218, y231–240, y255–264) followed by a **yellow band whose
interior is essentially blank** (x~218..880, y~267..303; only ~0.3% dark pixels
inside). There is **no `#008000` green ink anywhere in the original frame**, so
the original's y-values are not rendered in the build's green. The build's
full-width bands at y272..303 therefore highlight an empty region rather than the
y-row. This is consistent with Template A's MINOR #6/#7 (bands and grid
restructure) and was already adjudicated as content-equivalent; it is logged here
as the residual risk if attempt 7 fails on structure rather than values.

### Procedure B re-cut

Crops re-cut from `render_7.png` at matched effective scale ×2.0833 (LANCZOS):`crop_7_noreg_rows_*`, `crop_7_table_left_*`, `crop_7_table_right_*`
(renders 6's crops predate the rebuild and are kept banked).

### Surgical-change verification (build hygiene)

`render_6.png` vs `render_7.png`: **1,386 differing pixels (0.0616%)**, confined
to exactly two line windows — y356..362 and y466..472 frame px, x214..345 — i.e.
the `y=` line of NO REG row groups 2 and 3. Nothing else moved, so any change in
the next judge verdict is attributable to the edited values alone.

## Attempt 7 judge dispatch — BLOCKED by fleet-wide gateway saturation

Dispatch `bash-at0mmunq` (Template A on `render_7.png`) consumed its full internal
abort+retry ladder (`--timeout 600` → 630s hard wall per attempt, 3 attempts) with
**no verdict and no transcript**:

```
[error] None: every model failed:
  images: attempt 1: ABORT HangError: hard wall-clock 630s exceeded
  images: attempt 2: ABORT HangError: hard wall-clock 630s exceeded
  images: attempt 3: ABORT HangError: hard wall-clock 630s exceeded — giving up
```

Peak fleet load during the dispatch was **34 `analyze_image.py` processes** (16-slot
gateway), with peer workers judging slides 050 / 009 / 036 / 023 concurrently.
**No verdict was produced, so by protocol law this is NOT an attempt** — the
attempt budget remains intact (1 verdict-producing attempt consumed: `judge_attempt_6.txt`).

**Ready to fire in one command when the fleet drains** (run when
`pgrep -c -f analyze_image.py` < 8):
`recreated_pptx/qa/slide019/dispatch_legs.sh`
- Both `-p` payloads banked at `scratch/tmp/judgeA7_payload.txt` and
  `scratch/tmp/judgeB7_payload.txt`, each byte-verified against
  `shared_patterns/judge_protocol_03.md` (Leg 1 exact match; Leg 2 exact match
  after reversing the `slide_NNN`→`slide019`, `K`→`7` token substitutions).
- Corrected a pre-existing payload bug while banking: the older `scratch/tmp/judgeB.txt`
  had substituted the bare token `K`→`7` *inside words*, corrupting `BLOCKER` to
  `BLOC7ER`. The new payload substitutes `\bK\b` only.
- Leg 2 covers `noreg_rows` (the disputed cells), `table_right`, `table_left`;
  all three crop pairs are already cut from `render_7.png` at matched ×2.0833 scale.

**Open item for the next worker:** run `dispatch_legs.sh`, then (on PASS of both
legs) register `pptx_path` / `build_script`, set `visual_check=PASS`,
`visual_transcript=<judge_attempt_7.txt>` and `gen_status=passed`, and
`release 19 judge019-r2`.

---

## Attempt 8 (2026-10-24) — currency re-anchor resolved: the attempt-6 FAIL no longer applies to the current build

### Currency question (the governing request)

The re-anchor dispatch asked whether `judge_attempt_6.txt`'s FAIL applies to the
**current** build. Answer: **it does not.** Resolved by md5/mtime, then by pixel diff,
then by glyph-level PIL reading of both images (960x540, 1 px = 1 pt).

**What attempt 6 consumed** (`scratch/tmp/judgeA6.log` names IMG1 = `render_6.png`):
md5 `b2370bc9cdbb4dbc1c9b104f18b65c8e`, 151,917 B, mtime 2026-10-24 01:03:26.

**What is current now:**

| artifact | md5 | size | mtime (UTC) |
|---|---|---|---|
| `render_8.png` | `ed8bc8124e945f98d194416e79bf8fdf` | 151,716 B | 2026-10-24 07:02:08 |
| `build/slide_019.js` | `42f4ac7ee2378b37322dfef2c8ee7f80` | 13,526 B | 2026-10-24 04:19:30 |
| `slide_019_recreated.pptx` | `953cedc1ab78cd475fc78828d4218b2d` | 128,550 B | 2026-10-24 07:01:49 |

`build/slide_019.js` is byte-identical to the banked `build_attempt_20261024_root.js`
(same md5): the **build has not changed since attempt 7**; only the render was refreshed
at 07:02 to match the 07:01 pptx. The attempt-6 FAIL's evidentiary basis is therefore
superseded bytes.

**Pixel diff `render_6.png` vs `render_8.png`: 1,247 differing px (0.0554%), confined to
exactly two windows — y356..362 x214..345 and y466..472 x214..343 — which are precisely
the `y=` lines of NO REG row groups 2 and 3, i.e. exactly the cells named by FAIL
drivers #1/#2. Nothing else moved.**

### Adjudication of every FAIL/MINOR against BOTH images (PIL, banked scripts + logs)

**Driver #1** (NO REG row 2 "shows 60/80/100, should be 32.4/42.3/52.3") —
**RESOLVED in the current build.** `build/slide_019.js:180-182` now carries
`y: 32.4 / 42.3 / 52.3`. Independently confirmed from the original frame: its saturated
green numeral for that cell group spans x309..330, rows 387..397 — glyphs "<4>" (x309..320),
decimal (x322..323), "3" (x325..330) — reads **42.3** (Test 2 of the row group), matching
the build.

**Driver #2** (NO REG row 3 "shows 60/80/100, should be 24.4/31.2/38") —
**RESOLVED.** `build/slide_019.js:188-190` now carries `y: 24.4 / 31.2 / 38`. The original's
green numeral at x309..329, rows 496..506, reads **31.2**, matching the build.

**Provenance caveat — important for the record:** the banked analysis *transcriptions* are
what was wrong, not the frame. `analysis/slide_019_raw.json` (brief step 7) and
`analysis/slide_019_final.json` both record NO REG rows 2/3 as "all y predictions 60,80,100";
the frame shows 42.3 / 31.2. So the build was rebuilt from the frame while the transcription
was never re-derived. Any future worker re-scoring this slide from the JSON will reproduce
the attempt-6 error. This is the single most useful thing in this report for whoever picks
the slide up next.

**MINOR #3** (original's W-boxes carry small green per-component figures flanking the W label,
"0.1 | W=(1.95) | 0.03") — **REFUTED.** The original contains **0 green pixels** in the
W-label zone (frame x124..206) for all three row groups, in both images. Its only green ink
per column group is the single Test-2 numeral at column-relative x ~+185..+205 (NO REG
x313..325 / x309..330; RIDGE 3 x569..589; RIDGE 10 x827..847), which the build already
reproduces. Scripts `pil_green_adjud_8.py`, `pil_ycolor_census_8.py`; logs
`scratch/tmp/pil_green_adjud_8.log`, `scratch/tmp/pil_ycolor_census_8.log`,
`scratch/tmp/orig_green_map.log`, `scratch/tmp/green_glyphs_all.log`.
The original's red/blue classification of its 8 pt text was also measured to be unreliable
(JPEG chroma noise), so colour-based classes other than saturated green were **not** used
as evidence.

**MINOR #4** number formatting — **REFUTED** (unchanged): the original also lays these out linearly.
**MINOR #5** title frame — **REFUTED**: identical blue footprint; no second blue element exists.
**MINOR #6** highlight regions — **REFUTED**: the original's gold bands are genuinely full-width
and carry no extra content inside them.
**MINOR #7** grid restructure — **not a defect**: content-equivalent.

### Residual caveat — FLAGGED, NOT FIXED (this is the legs lane; build edits are out of scope)

In the original the green Test-2 numeral sits on its **own line at the bottom of each row
group** (group-relative y ~+74..+79), while the other cell text lines sit at ~+7..+15,
+29..+38, +52..+63 (~23 px pitch). The build paints the numeral as the third line of its test
block at group-relative y ~+44..+54. The original also shows an **empty rectangle outline at
x209..234 (row groups 2 and 3)** that the build does not draw. The original's full internal
cell structure is only partly mapped; the green-numeral evidence above is the reliable subset.
**Hand this to a build lane for verification — do not "fix" it blind from here.**

### Verified structure (for whoever picks this up)

Original vertical rules: x~58 (outer red), x65, x117..125, x377..384, x637..644,
x893..894 (green right border), x900..902 (outer red). The build's column boundaries
(124/380, 384/640, 644/900) are correct.

Green Test-2 numerals measured in the original (original green is saturated, colour-isolated):

| column | row 1 | row 2 | row 3 |
|---|---|---|---|
| NO REG | 80 | 42.3 | 31.2 |
| RIDGE 3 | 78.7 | 45.1 | 34.4 |
| RIDGE 10 | 76.5 | 46 (see note) | 35.4-shaped |

Left "Outlier X_s" column: green "22" at x91..108 (row 1), x85..103 (row 2), x86..102 (row 3).
The build's Test-2 values agree with every reading except RIDGE 10 row 2, whose first glyph
is 5 px wide and reads "3" or "4"; the spec value is 46, the build has 46, so the reading is
consistent with "46" if that glyph is a 4.

### Vision legs — attempt 8: still no verdict (fleet gateway saturation) -> PARKED

`qa/slide019/judge_attempt_8.txt` **does not exist.** Three Template A dispatches were
consumed and produced no verdict body; Procedure B was never dispatched.

1. `dispatch_A8.sh` (wall `timeout 1700`) — attempts 1 and 2 aborted with
   `HangError: hard wall-clock 630s exceeded`; the outer wall killed the process during
   attempt 3, EXIT=124. Log `log_judgeA8_run1_20261024.txt`.
2. `dispatch_A8r.sh` (the one permitted hard-wall retry, wall `timeout 2400`) — all three
   attempts aborted `HangError ... giving up`, EXIT=1, "0/1 result(s) analyzed
   successfully". Log `log_judgeA8_run2_20261024.txt`.
3. `dispatch_A8rr.sh` (fired on the only gate-open window the sentry saw, 14:04:48,
   load=6) — `HTTP 504 upstream_timeout` (upstream provider Nvidia) on attempt 1,
   EXIT=1, "0/1 result(s) analyzed successfully". Log `scratch/tmp/legs_sentry_8.log`
   tail; sentry parked 14:05:49.

Peak fleet load across the window: **58** concurrent `analyze_image.py` against a 16-slot
flock gateway. Load re-probed this session: 30 @17:58, 8 @18:57, **12 @19:26**, **19 @19:33**,
19 @19:35. The two permitted probes of the 19:00 hour both show congestion, so per the gate
law this session **parks without a dispatch**. The Template A flight budget is exhausted;
per protocol none of the three dispatches count as a judge attempt. Verdict-producing
attempts remain **1** (`judge_attempt_6.txt`, FAIL, superseded bytes).

**Nothing on slide 019 may be certified from this session.** Certification requires a real
Template A `FINAL VERDICT:` body plus all four Procedure B legs; none exist for attempt 8.

## attempt 26 (2026-10-26 ~02:10Z, S4b carrier — wall park)

Final A24-fix build COMPLETE + PIL-verified; judges NOT dispatched (wall closed before dispatch).

- Edits applied to build/slide_019.js: outlierRow gained x param (g1 x84, g2/g3 x79);
  outlierParens (fs55 text-glyph parens) REPLACED by outlierArcs() — pptxgenjs ShapeType.arc,
  fill none, line 2E3B96 w1.5, angleRange [90,270]/[270,450], bbox w6, full-height h72-74.
- Rebuilt slide_019_recreated.pptx → qa/slide019/render_26.png (render_25 = banked intermediate).
- house_chrome_check render_26 PASS (panel/strokes/badge within tol 8).
- pil_probe_26.py (banked) + refined probe: ALL PASS — 9 digit bboxes d≤2.1 vs orig table;
  s_sub x93-99 y207-212 (d2.2); 6 thin arcs ink w3.4-3.8 (orig ~2px+AA), g1_left tip x83.8-85.8
  = orig 84-85; patches x76.3-115.2 (orig 76-116). First-pass probe "fails" were window
  contamination (arcs+X glyph inside digit windows) — refined tight-window rerun clean.
- NEXT (resume here): dispatch A26/B26 full+crops per dispatch_A24_1200.sh pattern (copy→sed 24→26);
  crop table_left + header_strip FRESH; table_right + noreg_rows carry crop_23 certs IF
  render_23-vs-render_26 diff = 0 on those regions (not yet diffed — do it first);
  on all clean → 15_progress.py DB write (verify CLI first) + judge_attempt_26 transcripts.
- 025: UNTOUCHED this carrier (k13 render_14 + chrome PASS stand; BR anomaly unresolved).

## S4b fresh carrier (kimi-s4b-fresh-1026b, pool 299640) — 2026-10-26 03:50–05:50Z: pair-span fix certified, judge chain run

Continues "attempt 26 (wall park)" above. Task #86: arc-pair-span fix → verify →
A26-retry full judge + 3 fresh crop judges → DB write.

### Probe re-index + pair-span fix (carry-over, verified before this window)

`pil_probe_26.py`'s hardcoded ORIG `want` table was VOID (measured with the render
scale on the 960×540 orig). Corrected per-image indexing in `pil_clusters_26b.py`
(orig native 1.0×; render SX=2.08438, SY=2.08333): 9 outlier digits verify d≤3 at
tol 4; s_sub ✓; yellow patches MATCH (pred-sensitive: only at b<190 do orig/render
both give x76..116 — the old "mismatch" was JPEG chroma smear); **arcs were WRONG**:
orig arcs span ONLY the digit PAIR (y215..264 / y323..371 / y425..475; the
highlighted 22 sits OUTSIDE), while render_26 arcs ran full-height h72-75 (22
INSIDE). Triple-confirmed (clusters + loose y-profile + 1px ASCII) and consistent
with the A24 judge + crop_23 judge texts.

**Fix applied** in `build/slide_019.js`: `outlierArcs(83,110,216,72) /
(77.5,106,321,74) / (77.5,105.5,425,74)` → `(83,110,215,50) / (77.5,106,323,49) /
(77.5,105.5,425,51)`. Rebuilt → `render_27.png` (2001×1125), chrome check PASS.
Re-probe on render_27: all 6 arcs match orig d≤3. Surgical diff render_26→27 = 3342
px (tol 8), frame bbox x76..117 y214..499 (arc zones only).

### Carries and fresh-leg plan (diff_23_26_carry.md, extended to render_27)

- `noreg_rows`: region byte-identical render_23↔27 → **crop_23 PASS CARRIES**
  (proof in diff_23_26_carry.md).
- `table_right`: region byte-identical but **NO cert exists** → judged fresh
  (crop_27 pair from cut_crops_27.py).
- `table_left` (9008 px changed) + `header_strip` (1548 px, arc tips y180..193):
  judged fresh per task #86.

### The empty-payload incident (attempt 27) + adjudication

`dispatch_A27_1200.sh` was staged with a **2027 filename typo** → `-p ""` — the
judge ran WITHOUT the frozen Template A and improvised its own report
(`judge_attempt_27.txt`, banked, no `FINAL VERDICT:` line — not certifiable, does
not count as an attempt). Full adjudication of its findings:
`adjud_a27_improvised_s4b.md`. Key results: the `"22"` tag color claim
(orig-black-vs-build-green) **PIL-REFUTED** (`pil_adjud_a27findings.py` — orig ink
is green ≈(123,179,26) core in all three patches; build 008000 correct; patches
align sub-pixel); the navy-rule claim was already graded MINOR inside
crop_23_header_strip's PASS; badge = house chrome (overridden). **No build change.**
Both dispatch scripts fixed to `20261024` + fail-loud payload guard.

### Judge legs on render_27

- **A28 (04:46:42Z, correct payload md5 9387f5fb len 4139): NO VERDICT** — gateway
  hard wall (`HangError 1230s, stuck thinking stream`) aborted attempt 1 at
  ~05:07Z; the in-gate retry was killed by the outer timeout-1700 at 05:15:02Z;
  no transcript. Honest no-verdict (log + manual record in legs_status_27_s4b.md).
- **A29 (re-dispatch ~05:19Z, same payload): PENDING** (`judge_attempt_29.txt`).
- **crop_27 header_strip: FINAL VERDICT: PASS** (05:21Z, `crop_27_header_strip_judge.txt`).
- **crop_27 table_left: FINAL VERDICT: PASS** (05:30Z, `crop_27_table_left_judge.txt`).
- **crop_27 table_right: PENDING** (dispatched 05:24:56Z).
- noreg_rows: carried from crop_23 (byte-identical region proof).

### DB write (only after all legs clean)

`VIDEO=machine-learning/03_ridger_regression_gradient_descent python3
scripts/15_progress.py set 19 gen_status passed|visual_check PASS|visual_attempts
29|visual_transcript recreated_pptx/qa/slide019/judge_attempt_29.txt --worker
kimi-s4b-fresh-1026b`, then `get 19` verify. CLI + whitelist verified (all four
fields whitelisted).
