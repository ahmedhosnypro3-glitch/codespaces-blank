# PIL adjudication — slide 048 crop legs 4 (aug_iter, calc_panel), render_3

Render md5 at judge time matches current pptx (7ac3dcca114e755395fad047a11cd293); leg A real PASS banked in judge_attempt_4_stdout2.txt. Adjudication performed against render_3 crop pairs and analysis/slide_048_final.json.

## crop_4_aug_iter_judge.txt (FAIL → all findings resolved)

- D1 "Ugmented garbled" — REFUTED. Original's own verbatim analysis extracts "Ugmented Vectors (from Top)" with an explicit do-not-correct-to-'Augmented' clause; pixel form of the original supports the U-glyph. Recreation faithful.
- D2 "per-cell parens missing" — REFUTED. ASCII pixel maps (y198–212, x85–255) show flanking paren strokes on both sides in render and orig.
- D3 "outer ( instead of [" — REFUTED. Analysis JSON: the original itself uses tall square brackets (instruction #3/#20); render matches.
- D4 "x vs X case" — REFUTED. Build uses lowercase x₁…x₆ (bold only), matching original.
- D5 "checkbox column" — REFUTED-with-note. Judge misread render's row boxes + italic x in d(xᵢ); no such spurious column exists.
- D6 red brightness differs — MINOR, accepted (documented in build notes).
- D7 cool color cast — MINOR, accepted.

## crop_4_calc_panel_judge.txt (FAIL → all findings resolved)

- D1 "spurious x column in every vector" — REFUTED. Mathtext sources in build/gen_assets_048.py: d(x_i) = row·col = res; W = col + 1·col = col — no x column inside brackets.
- D2 "bars instead of parens" — REFUTED premise. Original uses square brackets (analysis JSON); render's mathtext straight delimiters match; geometry/span correct → at most MINOR.
- D3 "missing green ⇐ arrow" — REFUTED. Green pixel census: original has 498 chroma-noise px over rows 110–517, cols 383–758 (≈0.2 px/col), no arrow glyph present in the original either; documented in build/slide_048.js note block.
- D4 "stray x" — REFUTED-with-note. The x belongs to the original's own d(xᵢ) layout.
- D5 label line-wrap — MINOR, accept.
- D6 "· vs *" — MINOR, accept.
- D7 color accents — non-actionable MINOR.

Conclusion: no REAL defects; crop-4 FAILs are fully adjudicated and do not warrant a rebuild. Fresh top_band leg to complete the crop series.
