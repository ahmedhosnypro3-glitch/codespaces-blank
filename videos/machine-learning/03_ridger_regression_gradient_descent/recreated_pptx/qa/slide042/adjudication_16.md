# Adjudication of judge_attempt_10 FAIL — slide 042 "Iteration 1"

Worker: `w042-finish-20261024` · date 2026-10-24 · frame `unique_slides/slide_042.jpg`
(md5 `c8913083a18f76039b5abc2b9f8bbcf5` — unchanged since analysis, `_reconcile_md5_snapshot`
matches), render under adjudication `qa/slide042/render_16.png`.

Every finding below is measured against BOTH images before any build change
(960×540 frame, 1px = 1pt; render 2001×1125 @150dpi, scale 2.08333).
Noisy rows/columns below 3 ink px are rejected before measuring.

---

## Framing: what the verdict was rendered against

`judge_attempt_10.txt` (FINAL VERDICT: FAIL, conf ~0.7) was produced on
`render_10.png`, i.e. **attempt 10's build**. Attempt 11 already replaced the
per-box line B with ONE horizontal mathtext PNG per box (five distinct W
equations), which is the substance of judge items 1–2. The current lane therefore
adjudicates items 1–6 on the **current** build (post-fix, `build_attempt_16.js`)
rather than re-fixing solved ones.

## PIL defects found on the CURRENT build (independent of the judge) — FIXED

These two were found by measurement, not by the judge, and are hard protocol
violations (clause (5) FRAME CONTAINMENT, clause (4) alignment/collision):

| defect | measurement | fix |
|---|---|---|
| **box1 W equation crosses its box border** | eq image top y258, h 14.4 → ink y258..272; box1 bottom border y263. Render ink in the y264..272 inter-box gap = **750 dark px**, frame ink there = **0**. The spill also rendered into the gap as 130/129/96/139/88/77 px per row y264..269. | `BAND_B[0]` 258 → 247 |
| **box4 W equation sits ABOVE its d(x4) line** | `BAND_B[3]=420 < BAND_A[3]=434`; the W4 image (y420..434) overlapped the "= 6" text (x610..642) and inverted the frame's order (frame: d-line y426..437 ABOVE W-line y444..452). Render y420..443 was one merged dense band vs the frame's two separated bands. | `BAND_B[3]` 420 → 442, `BAND_A[3]` 434 → 427 |

Root cause of both: attempt 11 calibrated `BAND_*` from the frame and then applied
one blanket "+8" shift, but the shift was measured for **text** boxes while line B
is an **image** (an image places its ink at its top edge; LibreOffice centres a
h=14 text box's ink ~2 px *below* its box top). Every derived band is now checked
against its box's interior (219..262 / 274..327 / 342..393 / 408..458 / 474..526).

**Verification after fix** (`scratch/tmp/042measure.py`, `042bands.py`,
`042boxbands.py`, `042clean.py`, `042adjudicate.py`):
- gap ink y264..271 / y330..337 / y396..403 / y462..469: **0 / 0 / 0 / 0** render px
  (frame is ink-free there; prior build spilled 750 px into gap 1)
- per-box ink now contained: box1 231..259, box2 287..322, box3 353..388,
  box4 426..454, box5 485..520 — all inside their boxes
- lineA precedes lineB in every box (frame order restored)
- matrix row pitch 11 → 7 px: the frame's per-box 2-row d(x_i) matrix fits a
  12–13 px line (rows ~6.5 px apart), not 11
- `house_chrome_check.py render_16.png 42` → **PASS**

## Judge item-by-item

### Item 1 — "per-step weight-result equations … omitted" — MAJOR conf 0.6
**OUTCOME: REFUTED for the current build (evidence), partially real for attempt 10.**

The judge's own downgrade condition ("if a higher-resolution capture shows IMG1
actually contains clean, separate W = … result equations … items 1–2 would
downgrade") is satisfied by the current build: attempt 11 gives each box its own
distinct mathtext PNG — `eq_042_w1.png` (W=(4;−2)+2·(1;1)=(6;0)), `w2`/`w3`
(W=(6;0)), `w4` (W=(6;0)−2·(1;5)=(4;−10)), `w5` (W=(4;−10)) — via the mandated
pipeline (matplotlib mathtext → 600 dpi transparent PNG → addImage at px/600 +
`assets/eq_index_042.json` sidecar). All five are distinct and legible, one per
box, in the line-B position.

**Partial substance (real):** on the FRAME the W result is not a wide horizontal
equation at the position the build uses. Measured: the frame's box1 line-B band
(x395..704, y250..258) is **100% ink-free** (darkest px lum 735–760 ≈ pure white;
per-column scan of 10-px buckets darkest = 760 everywhere between x395 and x704).
The only ink in that band is the green ⇐ at x384..393 (frame RGB 130,157,124 —
greenest px, green excess +39) and a narrow dark paren pair at x713..729 spanning
the whole box height (y215..262). The judge's phrase "at the right of every
iteration row" agrees with the frame: the frame's W result lives at the **right**
of each row (narrow, parenthesized, spanning the box), not at x384..632.

This is carried as an open item for the re-judge (see "open item" below) rather
than silently conceded, because the analysis JSON's `verbatim_text.equations`
mandates all five W equations and the judge read them in the original.

### Item 2 — "garbled/incorrect merged step equations" — MAJOR conf 0.7
**OUTCOME: REFUTED for the current build.**
Attempt 10 stacked 2×1 tiles for line B (that is what read as "cluttered stray
stacked numerals" and caused the x1 "W× 4/−2 + … = −6 0" reading). Attempt 11's
single horizontal mathtext PNG per row removes the stacking; measured render
line-B ink per box is one clean 14-px-tall band: box1 y231..259 (lineA+lineB),
box2 y287..322, box3 y353..388, box4 y426..454, box5 y485..520 — no merged
stray tokens. Verified by per-row ink census plus the gap checks above.

### Item 3 — Z / "Check classes of" arrangement — POSSIBLE MAJOR conf 0.4
**OUTCOME: the judge's arrangement reading is REFUTED; two real frame mismatches
found instead and FIXED.**

- The frame's block is *caption → header → two digit rows* (the analysis's own
  structure), not the judge's "Z1 Z1 Z1 / (0)(0)(7) · Z2 Z2 Z2 / (3) · Z3 Z3 Z3 /
  (2)". Measured frame ink row-runs x490..670: (55,56) box border, (64,76)
  caption+header, (79,121) digit rows — no evidence of the 3×3 arrangement the
  judge could not reconcile.
- **Real defect 1:** the build printed headers `Z1 Z2 Z3`. The frame prints
  `Z1` **three times** — 1-px ASCII of the frame's y60..78 shows three glyph
  groups at x595..610 / 616..631 / 638..653 whose ink x-masks and glyph shapes are
  identical. Fixed to `Z1 Z1 Z1`.
- **Real defect 2:** the build drew those headers BLUE. The frame's header ink is
  DARK — darkest px RGB **(31,33,11)** (blue is the *lowest* channel, so not
  blue), 0 px matching a blue test `b>r+25 & b>120`; the analysis lists this
  block's colours as only `#FFFFFF`/`#000000`. Fixed to black.

### Item 4 — upgraded-vector delimiter / transposition — MINOR conf 0.7
**OUTCOME: REFUTED.**
The judge's premise (IMG2 prints repeated blue x1..x6 headers with cells in
parentheses) does not hold for the FRAME, and the frame shows the LM data as
**column-major with thin vertical strokes**, not row-major with "(n)" cells.
Measured frame ink row-runs x76..240: (148,159) caption, (166,175), (184,191),
(199,206), (215,222) four digit bands, (231,243) class row — i.e. the four digit
bands ARE separate (the build's `LM_BANDS` order), and the paren span y166..222
is the build's measured `LM_PAREN_PAIRS` geometry. Prior frame measurements
banked in `calibrate_*.txt`/`selfcheck_*.txt` (84/84 self-check) agree.
No transpose fix required; the build already matches the frame's column-major
layout with thin 0.75 pt paren strokes (the frame carries thin 1 px strokes, not
48 pt glyph parens).

### Item 5 — missing repeated header row above the LM matrix — MINOR conf 0.6
**OUTCOME: REFUTED with numbers.**
There is no second x1..x6 header on the frame. Frame blue-ink census in the
candidate header zone y140..168 = **236 px**, while the zone y168..230 (matrix
itself) = **132 px**; the y140..168 count is accounted for by the single blue
"Upgraded Vectors (From Top)" caption, whose ink runs (148,159) are the only ink
between the caption and the first digit band (166). The gap y160..166 carries
**0** ink. Adding a header row would fabricate an element the frame does not have.

### Item 6 — top grouping box: rounded, ~#FFF2CC fill — MINOR conf 0.75
**OUTCOME: REFUTED.**
- **Fill:** frame interior px are (254,255,234) @ (300,90), (255,247,224) @ (400,70),
  (254,255,232) @ (700,90) — i.e. the frame's cream is **FEFFE9 ≈ FEFFE8**, not
  #FFF2CC and not white. The build already uses `CREAM = "FEFFE8"`; the judge's
  "IMG1 … rectangular white box" is wrong (the render's box is cream, matching).
- **Rounded:** the frame's extreme corner px (69,58) is dark border ink
  RGB (33,24,103) — a rounded container would leave that corner empty. The frame's
  box is RECTANGULAR, matching the build.
- **Border:** frame border RGB (34,27,107)/(162,156,230) — blue, matching the
  build's 0000FF 1 pt.

### Visual-quality note — "Keep same Weight" wraps onto two lines
**OUTCOME: REAL, FIXED.**
Measured: the frame's action ink for row2 occupies x688..727 in ONE line (its
line-A band is a single y-band). The pre-fix render rendered rows 2/3/5 action
text as two separate row-bands (row2: y285..298 + y304..318 = 31 px tall, two
lines) because the 130 px box was too narrow for 16 pt "Keep same Weight" before
LibreOffice's line-height rounding. Widened the action box 130 → 148 px.
After the fix each action renders as ONE band (row2 294..308, row3 360..374,
row5 492..506) — frame order and single-line form restored.

---

## Open item for the re-judge (not conceded, not fabricated)

Where the frame's W result actually sits (narrow parenthesised element at the
right of each row, spanning the box) versus the build's wide line-B equation
image. The build keeps the analysis-mandated five W equations (content fidelity
per the founder's verbatim-equation law) but now places them safely inside their
boxes in the frame's line-B band. If the re-judge's crop pair reads the frame's
right-hand element as the sole W representation and faults the wide image as
extra ink, that finding will be adjudicated against the banked numbers in this
file (the analysis JSON's `verbatim_text.equations` requires all five W
equations) and a decision recorded then.

## Audit note — corrupted payload in the bank (fixed for this lane)

`qa/slide042/judge_prompt_10.txt` and `crop_10_*_prompt.txt` contain
"**BLOC10ER**" where the protocol template says "BLOCKER" — the prior lane
substituted `K`→`10` with a naive (non-word-boundary) replace and corrupted the
severity keyword. The 2026-10-24 standing law requires `\bK\b` word-boundary
substitution; this lane's payloads (`judge_prompt_16.txt`,
`crop_16_<name>_prompt.txt`) are generated by `\bK\b`-only substitution and
byte-verified: `judge_prompt_16.txt` md5 `65de405e669cf6574e9465221fbec5f3` ==
protocol line 71 md5, Template B == protocol line 117 with `NNN`→`042` only.
"BLOCKER" intact in all 6 payloads, no `BLOC\d+ER` anywhere.
