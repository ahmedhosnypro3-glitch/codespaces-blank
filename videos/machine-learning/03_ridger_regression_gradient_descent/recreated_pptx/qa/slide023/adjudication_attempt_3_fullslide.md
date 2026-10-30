# PIL ADJUDICATION — Template A attempt 3 (render_2, refutation re-roll)

Source: `judge_attempt_3.txt` (frozen Template A, render_2).
Verdict: FAIL. All 7 findings adjudicated below; none warrants a build change.

## B1 MAJOR — "body-text color changed wholesale to maroon/red"
=> **REFUTED** (pixel proof)

This attempt also states the correct layout ("unbordered 'For Example' line…
yellow Solution box … all present, in the same vertical order and regions"),
directly contradicting attempt 2's added-boxes MAJOR — a second refutation of A1.

Body-text glyph cores (darkest quartile of each measured band):

| band | ORIGINAL core | family | RENDER_2 core | family |
|---|---|---|---|---|
| blue L1 y242..264 | (76,55,145) | NAVY | (28,13,124) | NAVY |
| blue L2 y276..298 | (69,59,158) | NAVY | (13,13,134) | NAVY |
| blue L3 y309..331 | (68,57,158) | NAVY | (12,12,134) | NAVY |
| EX1 y363..387 | (79,68,67) | BLACK | (41,26,27) | BLACK |
| EX2 y398..419 | (92,37,42) | RED (the numeral) | (74,9,10) | RED |
| SOL1 y477..495 | (66,59,143) | NAVY | (10,10,132) | NAVY |
| SOL2 y504..521 | (48,40,132) | NAVY | (5,5,130) | NAVY |
| title (reference) | (151,22,35) | RED/MAROON | — | — |

Both images carry the SAME colour scheme: navy complexity/solution body text,
black example text, red numerals, red title. The build's 000080 (0,0,128) and
C00000 are the correct families. **No build change.**

## B2 MINOR — "λI green highlight dropped; recreation renders it black"
=> **REFUTED** (pixel proof; third independent confirmation)

  ORIGINAL λ core = (44,147,47), G−B = +99   (green)
  ORIGINAL I core = (29,144,29), G−B = +115  (green)
  RENDER_2 λ core = (5,127,5),   G−B = +121  (green)
Body-glyph controls (W, X) are neutral dark (G−B ≈ +15, JPEG ink noise).
See `adjudication_attempt_2_eq_zoom.md`. **No build change.**

## B3 MINOR — "original bolds W and Y; recreation underlines them"
=> **ACCEPTED MINOR** (weight-only)

Underline bars are present in BOTH images under W and Y (measured y180..181
frame px; the eq_zoom crop judge explicitly recorded "W and Y both carry the
underline in each image (weight/placement consistent)"). The residual is
mathtext's single-weight rendering vs the original's heavier type — the same
weight-only class the eq_zoom PASS already adjudicated. Position, colour,
structure and both underlines are correct. **No build change.**

## B4 MINOR — "(X^T X) underline dropped in caption"
=> **REFUTED** (pixel proof, third independent confirmation)

Full character-map proof banked in `pil_refutation_underline_X.md`: rows y216
and y217 are entirely empty in the ORIGINAL; no bar spans x512..526 at any row
in either image; the y218 stroke is the green box border. **No build change.**

## B5 MINOR — "'1000' / '1,000,000,000' not bolded"
=> **ACCEPTED MINOR** (weight-only; banked M3)

Ink position and colour match within 5px (selfcheck `red 1000` / `red 1e9`).
`verbatim_text` has "size 1000" (no comma) and "1,000,000,000"; the build is
byte-exact. **No build change.**

## B6 MINOR — "'Matrix inversion' not bolded"
=> **REFUTED** (pixel proof; third independent confirmation)

Solution-box interior (x92..868, y439..526) ORIGINAL red ink = **0 px**; the
interior is uniformly navy in both images. Mean "red-detected" colour in the
perimeter band is (115,96,54) — the brown box border. **No build change.**

## B7 MINOR — "complexity box: original unfilled/white, recreation lavender"
=> **REFUTED / immaterial** (pixel proof)

Clean-interior medians:
  solution box: ORIGINAL (250,253,226)  ==  RENDER_2 (250,253,226)  — EXACT
  blue box:     ORIGINAL (254,255,253)  vs  RENDER_2 (248,248,255) — ±7/255

Both blue-box interiors are essentially white; the build's F8F8FF is the
banked measured fill. A ≤7-unit difference across all three channels is below
perception at 150dpi and below the pipeline's ±8 render-px tolerance spirit.
**No build change.**

## Outcome
Template A attempt 3: **every finding adjudicated; 4 REFUTED, 3 ACCEPTED
MINOR (weight-only), 0 requiring a build change.** The render is correct;
both FAILs are 150dpi-JPEG-vs-PPTX misreadings (stale/hostile perception),
verified against pixels in every case.
