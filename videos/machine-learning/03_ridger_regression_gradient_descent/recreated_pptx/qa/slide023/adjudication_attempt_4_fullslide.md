# PIL ADJUDICATION — Template A attempt 4 (render_2) — VERDICT: PASS

Source: `judge_attempt_4.txt` (frozen Template A, render_2).
**Verdict: PASS.** All 5 MINORs adjudicated below; none is a build change.

Notable independent confirmations from this transcript:
- "No BLOCKER or MAJOR defects: nothing is omitted (title, Recall box with
  equation + conditional line, complexity box, Example box, Solution box, '23'
  badge all present)… FRAME CONTAINMENT is clean… DELIMITER GEOMETRY is fine…
  the under-W underline is fully drawn."
- "Layout regions, ordering and gaps of the four panel boxes track the
  original; house chrome … matches the mandated template."
- "no text overflow/clipping, no wrong wrapping, no collisions, no illegibility."

This is the third independent refutation of attempt 2's "added boxes" MAJOR
(this transcript explicitly counts the four boxes as tracking the original).

## C1 MINOR — "original uses a serif face; recreation uses sans"
=> **REFUTED** (glyph-form proof)

Direct glyph-form inspection of the original's complexity L1 (x96..176, y242..261,
blue-box band): the `T`, `h`, `e`, `s`, `t`, `a`, `n`, `d` forms show uniform
stroke width (single-`#` stems throughout), flat/rounded terminals, and **no
serifs, flares, or brackets at the stems**. These are sans-serif glyphs.

The banked font forensics (`fit_fonts.py`, `iou_fit.py`, `font_fit.py`) selected
Arial on advance metrics (23.5pt: 749 vs measured 740; 20pt: 468 vs 463) and
detected the frame's ~-7.5° lean, which Carlito Italic (-7°) cannot combine with
the frame's single-storey `a` and Arial-identical advance. Italic is already
carried as the banked ACCEPTED MINOR **M1** (font-availability limitation).
**No build change.**

## C2 MINOR — "Solution-box emphasis lost (bold-italic Least Squares / Matrix inversion / Gradient Descent; italic 'iterative solution')"
=> **REFUTED (colour/bold) / ACCEPTED (italic, same grounds as M1)**

- Red: solution-box interior (x92..868, y439..526) ORIGINAL red ink = **0 px**
  (control: the example band has 1710 px). Both images are uniformly navy.
- Bold: the render carries `Solution:` bold (selfcheck cap-height/advance match);
  the "Least Squares / Matrix inversion / Gradient Descent" weight reading has
  already been adjudicated as weight-only under **M3**.
- Italic emphasis on those runs falls under the same italic font-availability
  limitation as M1 (no installed face reproduces the frame's slant and advance).
**No build change.**

## C3 MINOR — "green Recall panel and lavender/example panels more saturated / heavier-bordered"
=> **REFUTED / immaterial** (pixel proof)

Clean-interior medians:
  solution (yellow) box: ORIGINAL (250,253,226) == RENDER (250,253,226) — EXACT
  blue complexity box:  ORIGINAL (254,255,253) vs RENDER (248,248,255) — ±7/255
  Both blue-box interiors are essentially white; the build's F8F8FF is the
  banked measured fill. A ≤7-unit spread on all three channels is below
  perception at 150dpi. Border weights match within the selfcheck's ≤1.0px on
  all twelve strokes. **No build change.**

## C4 MINOR — "equation prints '(λI)^{-1}X^TY' with no space; original has '(λI)^{-1} X^T Y'"
=> **CONFIRMED, ACCEPTED MINOR** (pixel proof)

Baseline-band (y164..186) column structure:

  ORIGINAL: `)` lower bowl ends x341 → next ink (X) begins x370  = **29pt gap**
            (the `-1` superscript, x347..363 y150..162, occupies part of it)
  RENDER_2: `)` ends x349 → next ink (X) begins x365.3            = **16pt gap**

The render's post-inverse `X^T` is measurably closer to the paren than the
original's. Cause: matplotlib mathtext collapses literal whitespace in math mode,
so the `"^{-1} X^T"` space renders ~13pt narrower than the original's.

Severity is genuinely MINOR (glyphs, order, superscript position, colour and the
enclosure geometry are all correct; the eq_zoom zoomed judge — which examines
this exact band at 2.08× — returned PASS and did not flag it). No mathtext
mechanism adds a natural-width space inside the same string without perturbing
the calibrated ink extent (x104..429) and baseline (259), both of which the
OMML sidecar records. **Accepted as a MINOR; no build change.**

## C5 MINOR — "title sits slightly right of the original's optical centering"
=> **REFUTED** (sub-pixel)

Banked `selfcheck_attempt_1.txt`: title render x221..652 y78..103 vs orig
x219..654 y78..104 → **d(+1.6, -1.6, -0.2, -0.8)** — a ≤1.6px difference, inside
the pipeline's ±8 render-px (≈4 frame-px) tolerance and below optical
perception. **No build change.**

## Outcome
Template A attempt 4: **PASS.** 3 REFUTED / 1 immaterial / 1 CONFIRMED-minor
(equation inter-symbol space, accepted). No build change warranted.
Together with attempt 1's PASS and the crop-pair PASS certificates, both legs
are banked.
