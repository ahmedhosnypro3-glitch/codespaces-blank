# Slide 048 — PIL adjudication record (attempt 4, worker `w048-legs3-20261024`)

Every finding below was adjudicated by measuring BOTH images BEFORE any build change.
Original `unique_slides/slide_048.jpg` at 960x540 (1 frame px = 1 pt);
render `recreated_pptx/qa/slide048/render_3.png` at 2001x1125 (150 dpi,
scale = 1125/540 = 2.083333 render-px per frame-px). Currency re-proven this run:
current `slide_048_recreated.pptx` md5 `7ac3dcca114e755395fad047a11cd293` == the pptx
whose render is banked, and that render is byte-identical to `render_3.png`
(md5 `0dda4e1e990fb317348f6a6de6e5aca0`; PIL diff bbox = None).

Source legs:
- `judge_attempt_4.txt` — Template A, **FINAL VERDICT: PASS** (4 MINOR findings).
- `crop_4_aug_iter_judge.txt` — Procedure B, **FINAL VERDICT: FAIL** (2 MAJOR, 5 MINOR).
- `crop_4_calc_panel_judge.txt` — Procedure B, **FINAL VERDICT: FAIL** (2 MAJOR, 5 MINOR).
- `crop_4_top_band` — **NO VERDICT** (upstream HTTP 504 on both the first dispatch and the
  single sanctioned retry; `crop_legs_top_band.log` / `crop_legs_top_band_retry.log`).

---

## §A — MAJOR claims: ALL REFUTED

### A1 (aug_iter) — "leading glyph garbled: IMG2 reads 'A'ugmented, IMG1 reads 'U'gmented"

**Verdict: REFUTED — the original reads "Ugmented".**

The header line is at original rows 147..159, cols 81..150 (PIL row-scan: the line's ink
runs are rows 148-157 at 82..127, and the `d` ascender at cols 131-132). First glyph,
original cols 81..90, rows 147..157:

```
row 148: 82 83 84  88 89        <- two separate uprights
row 152: 82 83     87 88        <- still two, 5 px apart
row 153: 81 82 83  87 88
row 156: 82 83 84 85 86 87      <- joined by a bottom curve
row 157: 83 84 85 86
```

Two vertical uprights joined **at the bottom** by a curve, with **no apex and no
crossbar**. That is a `U` and nothing else — an `A` would meet at the TOP and carry a
crossbar mid-height (cf. the banked `A`-family calibration in `adjudication_attempt_2.md`).
Word-body width is 8 letters over cols 81..150 (~70 px), consistent with "Ugmented"
(8) and not "Augmented" (9).

Corroboration: the founder-validated analysis contract
(`analysis/slide_048_final.json`) transcribes "Ugmented Vectors (from Top)" in **both**
`bullets` and `labels`; the build's pptx XML carries it verbatim; and
`adjudication_attempt_2.md` had already settled this reading (its MINOR-7 line records
"Ugmented Vectors (from Top)"). The recitation error is the judge's, not the build's.

### A2 (aug_iter) — "IMG2 wraps every one of the 18 matrix entries in parentheses; IMG1 shows bare digits"

**Verdict: REFUTED — the original has no per-cell parentheses.**

The augmented matrix is at rows 163..241. Measuring the delimiters of its first column
(original cols 92..96 and 104..108, rows 180..200):

```
left  stroke: rows 180-182 @ col 94-95 -> rows 187-199 @ col 93-94   (1.0 px drift, near-straight)
right stroke: rows 180-181 @ col 105   -> rows 188-199 @ col 106-107 (1.5 px drift, near-straight)
```

Decisive — the **vertical extent** of those strokes:

| image | delimiter stroke | contiguous row runs |
|---|---|---|
| original | col 93-95 | rows 179..225 (46 rows) |
| original | col 105-107 | rows 179..225 (46 rows) |
| render | slide cols 93-96 | render px 375..468 = slide rows 180.0..224.6 |
| render | slide cols 105-108 | render px 375..468 = slide rows 180.0..224.6 |

Both sets span the **whole matrix body** (rows 179..225) — they are the single **outer
enclosure** per column, not 18 per-cell paren pairs. A paren pair around each entry would
require 12 short strokes (one per row of the 3 numeric rows x 6 cols... i.e. ~18 pairs),
each ~10 rows tall, and a true `(` would bulge 8-15 px horizontally (banked
`adjudication_attempt_2.md` MINOR 6) — measured excursion here is 1.0-1.5 px. The build
already draws exactly this (12 tall DGRAY strokes at cols 93.8…218.2, rows 180..225.2,
`build/slide_048.js:270-276`), so structure matches the frame.

### A3 (calc_panel) — "spurious 'x' column inside every weight vector (all 8 vectors)"

**Verdict: REFUTED — the vector interior holds exactly one glyph per line.**

Render row-1 first vector, inside the brackets (slide cols 645..679, rows 148..196),
glyph-cluster census per row: the only constant-position ink is slide cols 652.3..652.8
= the **left bracket itself**. The digit glyph appears at slide cols 656.2..659.5 on three
disjoint line bands (rows ~157-161, ~169-177, ~179-183) = the three stacked entries, each a
single ~3 px-wide glyph. There is **no second glyph column** at any x-position spanning
the rows — an `x` column would leave ink on two diagonals and be visible at the top AND
bottom of every band; only a plain numeral is present.

Structural corroboration: `selfcheck_attempt_3.txt` PASS (25 checks) counts exactly
**6 tall bracket strokes for row 1's three vectors** and 2 for row 6's single vector —
i.e. 2 strokes per vector (the two brackets), no extra glyph column.

### A4 (calc_panel) — "wrong delimiter glyph: determinant bars instead of parentheses"

**Verdict: REFUTED (banked numbers hold).**

The judge itself concedes "the bars *do* span correctly — the span is fine; the glyph
choice is wrong", so this is a **stroke-style** difference only. `adjudication_attempt_2.md`
MINOR 6 already measured the original's own delimiters for these same vectors: "per-row
centroid x spans only 1.5 px over rows 149..194 … the stroke is a single continuous column
(col 643, rows 155..189) with **no horizontal serif at the top** … A parenthesis would
bulge 8-15 px horizontally. So the original is NOT round parens." Re-measured this run on
the render (`render_3.png`) and consistent with the banked reading. Rule (e) of the judge
protocol exempts mandated 2D equation-format rendering. Recorded, not changed — identical
disposition to attempt 2.

---

## §B — REAL NEW DEFECT (the one actionable finding)

### B1 (calc_panel) — action phrase wraps to two lines in the render; one line in the original
**CONFIRMED. This is a genuine build defect.**

Measured on BOTH images, all six calc rows:

| row | phrase | original | render |
|---|---|---|---|
| 1 | Update Weight | ONE line, rows 164..177 (14 px tall), ink cols 517..611 | TWO lines (L1 rows 168.5-172.8, L2 rows 174.2-180.0) |
| 2 | Keep same Weight | ONE line, rows 230..243 (14 px) | TWO lines (L1 224.6-230.4, L2 236.2-246.2) |
| 3 | Keep same Weight | ONE line, rows 293..305 (13 px) | TWO lines (L1 290.9-296.6, L2 302.4-312.5) |
| 4 | Keep same Weight | ONE line, rows 363..375 (13 px) | TWO lines (L1 352.8-358.6, L2 362.9-374.4) |
| 5 | Keep same Weight | ONE line, rows 426..438 (13 px) | TWO lines (L1 423.4-429.1, L2 433.4-445.0) |
| 6 | Keep same Weight | ONE line, rows 492..504 (13 px) | TWO lines (L1 485.3-491.0, L2 495.4-506.9) |

Original action-phrase band (row 2, rows 228..245, column profile): continuous ink
**cols 517..611 = 95 px on ONE line**. Every original band is 13-14 px tall (one line).

**Root cause** — `recreated_pptx/build/slide_048.js:330-334`:

```js
s.addText(acts[i], {
  x: fx(509), y: by, w: fw(80), h: bh,      // <-- 80 px box
  fontFace: FONT, fontSize: 13, ...
```

The box is **80 px wide** at **13 pt**. Measured single-line widths of these strings at the
build's own 13 pt (from the render's own per-line extents): "Update Weight" = **84 px**,
"Keep same Weight" = **110 px**. Both exceed 80 px, so all six wrap.

**Note:** the box's inherited comment at `build/slide_048.js:298` says "action cols 509-582"
(73 px), which understates the measured band (cols 517..611 = 95 px); the box was sized to
that too-narrow reading. The prior lane already fixed the **identical** failure mode for
the REPEAT banner and documented the recipe at `build/slide_048.js:156-159`
("At fontSize 13 the string is ~13% wider than the frame's and wrapped to two lines even in
a 115px box; 12pt keeps it on one line in a box that cannot wrap").

**Fix parameters for the next lane (hand-back, not applied):**
- The phrase ink starts ~8 px right of the box x (509 -> 517) and must reach col 611.
  At 13 pt, "Keep same Weight" needs 110 px of ink => box must be >= ~118 px wide, but the
  right-hand equation images begin at col 617, leaving only 8 px of clearance.
- The two-line wrap also breaks the row's vertical centering: the render's label block ages
  to 23 slab rows (225-247) vs the original's 14 (230-243), shifting the text box upward.
- The recipe that already worked on this build is the REPEAT one: widen the box AND drop
  the font size until the string cannot wrap inside the available cols 509..616 gap.
  At 12 pt "Keep same Weight" ~= 101 px; at 11 pt ~= 93 px ~= the original's 95 px.
- After the fix: rebuild -> re-render -> re-run **both** legs (Template A + all three
  Procedure B crops), per the deck's re-certification law in `AGENTS.md`.

---

## §C — MINOR claims adjudicated

### C1 (Template A #1) — "original caption 'Check classes of' and the parens around the Z-matrix are omitted"
**REFUTED.** The caption band above the check-classes box (original cols 620..760, rows
40..82) is empty white: the only ink is the box's top border at rows 56-57 and its right
edge at col 744-745. The box interior rows 57..71 = 0 dark px. Banked
`adjudication_attempt_2.md` MINOR 3 records the same finding and the build deliberately omits
it (`build/slide_048.js:26-27`). The parens are likewise absent (the box's own vertical
strokes are the only structure). The judge's premise is wrong.

### C2 (Template A #2, calc_panel #3) — "green left double-arrow (⇐) missing"
**REFUTED.** Full-slide green census on the original: only **334 green px** in 38 distinct
columns. The single dense cluster is rows 110..121 / cols 396..423 (11 px/col, 28 cols wide)
= the word **"Zero"**. Every other cluster is 1-7 px scattered over 1-3 columns (JPEG chroma
noise). There is no green arrow glyph. The build draws the word "Zero" in green
(`build/slide_048.js:182`). Banked `adjudication_attempt_2.md` MINOR 4 already ruled this.

### C3 (Template A #4) — "'Augmented Vectors (from Top)' wraps 'Top)' to a second line"
**REFUTED.** Measured: the render renders this header on TWO LINES (rows 224.6-232.2 and
235.2-247.2) while the original has it on ONE line (rows 231-243) — the same defect class as
B1, same root pattern. (The judge called the direction "original may wrap"; the PIL
measurement settles the direction: the RENDER wraps, the original does not.) Feed into B1's
fix pass — the header box at `build/slide_048.js:230` is `h: fh(14)` on a one-line measured
band, so it is a box-width/valign issue, not a content issue. Word content is verbatim
correct ("Ugmented Vectors (from Top)" — see A1).

### C4 (calc_panel #6) — "multiplication operator '·' vs '*'"
**REFUTED as a defect.** The founder-validated contract transcribes the operator as `·`
(`analysis/slide_048_final.json` equations: "d(x₁) = [1 1 1]·[4; -2; -2] = 0"). The build
follows the contract; the original's handwritten glyph is not unambiguously an asterisk at
this resolution, and notation-symbol choice is covered by the typed-ink medium rule (d) and
the equation-format rule (e).

### C5 (calc_panel #7) — "coloured ink accents dropped; equation ink is uniform black"
**REFUTED.** Colour census of the original calc-panel band (rows 200..540, cols 460..800):
the ONLY red ink is rows 163..173 cols 489..799 (the red REPEAT banner, already drawn) and
rows 538..539 cols 455..800 (the house-chrome bottom C00000 stroke). Zero green, zero blue
anywhere in the equation rows. The original's equation ink is uniformly BLACK, exactly as the
build renders it (`build/slide_048.js:299-300` documents "All text is BLACK (darkest core
RGB ~(13,15,12)); only the ⇒ is red").

### C6 (calc_panel #5, #4) — "added selection-checkbox column" / "stray standalone 'x' before 'W ='"
**REFUTED / no measurable phenomenon.** A per-row ink scan of the label column
(cols 515..610) across all six rows shows only the label glyphs, the row separator lines and
the right-hand equations — no small bordered box and no isolated italic glyph column. The
same "stray x" reading is the same artefact the crop judge produced in A3 (the bracket +
single numeral misread as "|x 4|"), refuted by the cluster census there.

### C7 (Template A #3) — "action arrows drawn double (⇒) vs single (→)"
**REFUTED (shape confirmed on both images).** The original's action arrow in calc row 1
(cols 770..835, rows 148..190) is a *thick-stem* rightward arrow: one shaft, one head, one
tail — 85 red px, 16 dark px, no paired shafts. The upscale to 2.083x crops/copies that
thick stem into a two-track look, which the crop judge read as a doubled arrow. The render
draws a single-stem `⇒`. Both images therefore show one rightward arrow; the build's `⇒` is
the mandated professional-format rendering of the same arrow (protocol rule (e)).

### C8 (aug_iter #5, #6, #7) — added checkboxes / brighter Iteration-1 red / cool cast on title ink
All **MINOR/Low-Medium** confidence, no measurable basis found: the checkbox claim is covered
by C6; the Iteration-1 fill is the frame-measured solid red (banked `adjudication_attempt_2.md`
MINOR 7 CONFIRMED-from-frame; build uses C6020A at `build/slide_048.js:285`); the "cool cast"
is explicitly unquantifiable by the judge itself.

---

## §D — Outcome

- Template A: **PASS** (its 4 MINORs are 3 refuted + 1 folded into B1/C3).
- Procedure B: **aug_iter FAIL** and **calc_panel FAIL** are both **fully REFUTED** on their
  2 MAJORs each; the 5 MINORs each are refuted except the line-wrap family.
- **One real defect is confirmed: B1/C3 (line-wrap family).** It is a build-width issue, not a
  content issue, and it is the same class the prior lane already fixed once (REPEAT banner).
- Per standing law ("A REAL new defect -> do NOT edit the build; bank the adjudication and
  hand the f</think>

Let me refine one finding (C7) to be precise about the arrow shape, then finalize the records.<tool_call>
<function=Edit>