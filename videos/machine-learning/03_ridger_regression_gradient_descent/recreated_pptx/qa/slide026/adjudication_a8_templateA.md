# Adjudication — judge_attempt_4.txt (Template A full-slide, render_8)

Verdict banked: **FAIL**, 1 MAJOR + 2 MINOR. PIL-FIRST adjudication against BOTH images
(`unique_slides/slide_026.jpg` 1px = 1 frame px, `render_8.png` SR = 2.0844), identical
predicates, halo bound ±2.5px/edge (banked measurement bank). Evidence:
`probe_a8_findings.out`, `probe_a8_findings2.out`, `adjudication_a7_algcrop.md`,
`diff_render7_render8.out`.

## Finding 1 — MAJOR "blue box stretched downward ~60–80px, empty framed white space, content sits lower" — **REFUTED**

| quantity | ORIGINAL frame | render_8 | delta |
|---|---|---|---|
| box TOP border row | y91 (760 ink px over x100..860) | y89–90 (1585 px = 760·SR) | +2 px |
| box BOTTOM border row | y498–499 | y500–501 | +2 px |
| box LEFT/ RIGHT border col | x82–83 / x862–864 | 170–171 / 1801–1802 px = x81.6–82.1 / x863.9–864.4 | ≤0.5 px |
| box height | 409 px | 413 px | +4 px |
| LAST content ink inside box | y493 (6 px, descender fragments) | y491 (6 px) | −2 px |
| empty interior below last line | y494–497 = 4 rows | y492–499 = 8 rows | +4 rows |

* Both boxes hug their own last line: the ORIGINAL's box bottom (y498–499) sits 5 px
  below its last ink (y493); render_8's (y500–501) sits 10 px below its last ink (y491).
  There is no 60–80 px of "extra framed white space" — the empty band differs by 4 rows
  and both images show the same 4–8 row whitespace band.
* "Gray panel visible beneath it" is true of the ORIGINAL too and of the render: box
  bottom (y499 / y501) → slide lower red stroke (y538) is panel gray in both.
* "Content sits lower" is refuted by the first/last-inside-box rows: first ink y111 in
  BOTH images; last ink y493 (orig) vs y491 (render) — the render's content ends 2 px
  HIGHER than the original's.
* Both images' interiors are white below the last line (orig (254,255,253) → interior
  sample (241,239,255) at the border halo; render (255,255,255)).
* Box side borders match within 0.5 px (vertical extent claim has no basis either: the
  box spans y91..499 vs y89..501, i.e. ±2 px on a 409 px span).
Conclusion: geometry matches the original within the halo bound; no build change.

## Finding 2 — MINOR "original title is underlined, recreation's is not" — **REFUTED**

Title ink band x294..639 (both images). Row profiles under the title, y78..90:

* ORIGINAL: y78:181 y79:205 y80:176 y81:16 y82:1 y83:1 y84:1 y85:1 y86:2 y87:0 y88:0
  y89:0 y90:0 — glyph ink ENDS at y81; y82–90 is **pure panel gray** (min lum 696 =
  232·3 = E8E8E8; zero red-ish pixels at every row).
* render_8: y82–88 pure panel gray (697); the y89/y90 ink (740 px) is the blue content
  box's TOP BORDER, which sits at y91 in the ORIGINAL as well — i.e. BOTH images carry
  the same horizontal stroke 9–10 px below the title's ink, and neither carries an
  underline inside the title band.
* A title underline of any tone present in the original would have to be dark
  (red 192,0,0 → lum 192 < 430) or at least non-gray; y82..90 min lum in the original is
  352 (JPEG noise), with ≤2 ink px per row. No bar exists in either image.
Conclusion: neither image underlines the title; no build change.

## Finding 3 — MINOR (low confidence) "[1] underlined 'Random Weights (W)' — recreation's underline stops at 'Weights'" — **REFUTED**

* The deliverable has exactly 6 underlined runs (XML audit of
  `slide_026_recreated.pptx`: 32 runs, `u="sng"` on "moving along the direction of ",
  "negative gradient", "gradient is ", "almost zero", "approximatly", "variable number
  of steps"). None is on rowA/rowC's "Random Weights (W)" span, so the render physically
  cannot "stop at Weights" — it draws no rowA underline at all.
* Ink runs at the rowA underline band (rowA baseline y144 → bar band y150..158):
  ORIGINAL y154/y156 = **no runs** (x100..700); render_8 y154 = 8–13 px descender
  fragments only (glyph bottoms of p/y/W), y156 = no runs. No horizontal stroke of the
  100–190 px a real bar in this deck spans exists in either image.
* rowA is UNTOUCHED by attempt 8: `diff_render7_render8.out` — 16,738 changed px, all
  inside frame y440..457 (the N3 band); the attempt-6 Template A and attempt-7 alg-crop
  claims of a rowA bar were already refuted the same way
  (`adjudication_a7_algcrop.md`).
Conclusion: three contradictory vision reads of the same region (bar exists / render
adds it / render's bar stops early) against pixel evidence showing no bar in either
image. Refuted with banked proof; no build change.

## Net

render_8 requires NO build change: every attempt-8 Template A finding is PIL-refuted
against both images. The leg set stands as: Template A = refuted-FAIL (this record),
Template B alg = PASS (crop_7_alg_judge.txt, 1 MINOR refuted in a7 algcrop record),
Template B notes = pending re-judge on crop_8_notes (render_8's diff is N3-band only,
so the attempt-7 alg crop evidence remains valid).
