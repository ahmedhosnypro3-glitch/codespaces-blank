# PIL ADJUDICATION — Template A attempt 2 (render_2) — both MAJORs REFUTED

Source: `judge_attempt_2_fix.txt` (frozen Template A, render_2).
Verdict: FAIL. Both raised MAJORs are PIL-refuted below.

## A1 MAJOR — "Added region boxes around two middle text blocks; original has none"
=> **REFUTED** (pixel proof)

The judge asserts the original shows the "standard matrix inversion…" and
"For Example: …" paragraphs as plain text with no enclosing box.

Direct measurement in the ORIGINAL frame (`unique_slides/slide_023.jpg`,
960x540), at the banked blue-box stroke positions:

- **Left stroke** (vertical): rows y250, y300, y330, y350, y400, y420 all show
  a dark value at x87 (lum **197-198**) against a background of 231 — a real
  vertical border. Rows y150/y200 (above the box) show 232 with no stroke.
- **Right stroke**: same family, per banked forensics (R x868.5, measured on the
  original during the geometry pass).
- **Top stroke** (horizontal): column x480, rows y228/y229 = lum **197/203**
  against 231 above it — a real horizontal border.
- **Bottom stroke** y425.5; rows y430+ show 231 (no stroke) confirming the
  bottom edge.

Border core measured in the original: (175,172,206) — the light lavender
B9B6D8 the build uses; fill (248,248,255) = F8F8FF.

The banked `selfcheck_attempt_1.txt` measures the render's strokes at
L@87.4 / R@867.8 / T@227.9 / B@424.7 against targets 87.75 / 868.5 / 228.5 /
425.5 — all within 0.8px. The render reproduces the original's box exactly.

The original also has a green "Recall" box (x97..754, y110..219) and a yellow
"Solution" box (x87..874, y435..530), all measured on the original frame in the
banked forensics (`box_edges.py`, `geom_boxes.py`). **No build change.**

## A2 MAJOR — "Recreation: 'size 1,000'; Original: 'size 1000' (no comma)"
=> **REFUTED — the observation is INVERTED** (pixel + source proof)

1. **Source text** (`analysis/slide_023_final.json`, verbatim_text.bullets[1]):
   "For Example: if Features vector is of size **1000** then Inverse calculation
   is or order **1,000,000,000** which is impractical"
   — `1000` has NO comma; `1,000,000,000` does.
2. **Build** (`build/slide_023.js:233`): `r("1000", { color: RED })` — verbatim,
   no comma.
3. **Pixels**: in the EX1 run at baseline ~382, the four digits sit at
   x537..582 in BOTH images with no trailing comma in either.
4. The commas the judge saw belong to **EX2's "1,000,000,000"**
   (`build/slide_023.js:239`), whose below-baseline comma tails are present in
   BOTH images: render tails at frame x201, 246/247, 292/293; original tails at
   x237..239, 282..285 (and more).

So the render's "1000" matches the original's "1000" and the source's "1000"
byte-for-byte, and the commas in "1,000,000,000" are reproduced. **No build
change.** (If anything the judge attached the comma from the line below to the
line above.)

## Outcome
Template A attempt 2 (render_2): **both MAJORs PIL-refuted — the FAIL is not a
fidelity defect.** No build change is warranted; no re-render needed.
