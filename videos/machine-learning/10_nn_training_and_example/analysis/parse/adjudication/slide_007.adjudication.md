# Parse adjudication — slide 007 (10_nn_training_and_example)

SOURCE IMAGE: `unique_slides/slide_007.jpg` (960x540 px, md5 51a252b67fee81775c47cbc733aa2dc9)
PARSE TRANSCRIPT: `analysis/parse/slide_007.parse.md` + `analysis/parse/slide_007.parse.json`
ENVELOPE: finish_reason=`stop`, usage.output_tokens=112, content_len=303 -> **valid call, no re-parse on transport grounds**
SECOND READ TYPE: **corroborated** — (a) script-12 vision analysis `analysis/slide_007_final.json` (verdict PASS_WITH_FIXES, independent vision model, full-frame layout+text read); (b) image-analysis transcript `analysis/parse/adjudication/vision/slide_007.vision.txt` (independent vision read, question asked: "transcribe every piece of text verbatim, region by region, with approximate positions").
MEASUREMENT: `analysis/parse/adjudication/measurements/slide_007.pil.txt`; glyph census: `analysis/parse/adjudication/glyphs.py`.

## Severity-ranked findings

### MAJOR — `dropped-region` — the subtitle is absent from the parse (confidence: high, corroborated)
Parse text begins `Neural Network Model` then `7`; there is **no** subtitle string anywhere in the 303-char content.
Second read (script-12, `verbatim_text.labels`) carries `"(Weights of Output Layer AFFECTS Calculated Error)"` and the
image-analysis cross-check independently returned it as the blue subtitle directly under the title.
Local geometry corroborates a second text line under the title band (title ink at y=41 anchor, a distinct row band below).
-> The parse drops one whole visible text line. REAL.

### MAJOR — `reading-order-inversion` — diagram labels are emitted as a flat unordered run (confidence: high, corroborated)
Parse order is: `Neural Network Model / 7 / _Input Sample_ / _Target Label_ / Neti Oi W ji / Output 1 / Class 1 / Wji / Class 2 / Class m / Node Bias / ...`.
The badge numeral `7` is emitted **second**, before any diagram content, and the three output labels are not contiguous;
`Neti Oi W ji` (three separate node labels) is fused into one token, and `Output 1` is interleaved between node labels.
Second read: the diagram is a 3-column network with Output 1/2/m as a vertical stack at the right and Class 1/2/m beside them.
-> The parse's linear sequence does not follow the visual reading order. REAL.

### MAJOR — `hallucinated-content` / garbled glyph merge — `Neti Oi W ji`, `Wji` (confidence: medium-high, corroborated)
`Neti Oi W ji` is three distinct labels (Net_i, O_i, W_ji) collapsed with no separators; the second read lists the
per-node labels `Net_j`, `O_j`, `w_ji` as **separate** labels. Same for `Wji` vs `w_ji`.
-> Parse emits fused/mangled strings with no counterpart as a single glyph run on the frame. REAL as a defect; the exact
underlying label set is DEBATABLE (subscript style `Wji` vs `w_ji` is a font/subscript-rendering difference).

### MAJOR — `dropped-region` — output labels `Output 2` and `Output m` missing (confidence: high, corroborated)
Parse contains `Output 1` only. Second read (script-12 labels) lists `Output 1`, `Output 2`, `Output m`.
Local block measurement shows **three** right-column label blocks (x=677..761 at y=171..192 and y=245..266, plus the
x=649..879 y=414..505 output-class stack) — a 3-fold vertical repetition that a single `Output 1` cannot cover.
-> REAL.

### MINOR — `math-normalization-loss` — fractions flattened to inline text (confidence: high, corroborated)
`Net j = ∑ i (wijOi)` and `E= 1/2 ∑ T(tj -Oj)2` are the fraction/summation stack rendered inline; `E= 1+e-Neti`
is the sigmoid rule with its numerator/denominator split into a linear run.
Second read gives the same three equations with explicit numerators/denominators and index limits.
-> REAL (format loss; the equation content itself is not invented).

### MINOR — `hallucinated-content` — stray glyph `T` in `T(tj -Oj)2` (confidence: medium, single-read)
`E= 1/2 ∑ T(tj -Oj)2` — the `T` has no counterpart in either second read, which reads `E = 1/2 ∑_j (t_j - O_j)^2`.
The sum index is `j`, not `T`. Advisory at most: the two reads do not directly contradict the parse on this token.

### MINOR — `class-token-mismatch` — single trailing `<class_Picture>` (confidence: medium, single-read)
Parse closes with `<x_0.9424><y_0.9586><class_Picture>` -> px (905, 518). Measured ink in the 120x40 window around
that point is 3636 px (frac 0.790) — i.e. the box lands on a **filled** area (the bottom annotation strip's right-hand
box, measured x=649..879 y=414..505), not on empty canvas. The class is a picture but the token carries no content.
-> The coordinate resolves to real ink; the label is plausible but uninformative. DEBATABLE.

## Explicit classification list

- REAL (high, corroborated): subtitle `(Weights of Output Layer AFFECTS Calculated Error)` missing — `dropped-region`.
- REAL (high, corroborated): `Output 2` and `Output m` missing — `dropped-region`.
- REAL (high, corroborated): reading order of the diagram label run is inverted/fused — `reading-order-inversion`.
- REAL (high, corroborated): fractions/summations flattened inline — `math-normalization-loss`.
- REAL (medium-high, corroborated): fused glyph strings `Neti Oi W ji`, `Wji` — `hallucinated-content`.
- DEBATABLE: `Previous Layer Layer (I)` — parse says `(I)`, script-12 read says `(0)`; a 1-vs-0 glyph ambiguity at small size, not bankable as a defect.
- DEBATABLE: `Wji` vs `w_ji` subscript styling; `E= 1/2 ∑ T(tj -Oj)2` stray `T`.
- HALLUCINATED: none banked — every parse string maps to a plausible mark on the frame; the defects above are omissions and mangling, not invention.

## Uncertainty markers

- `[?]` The exact glyph run behind `Neti Oi W ji` (Net_i / O_i / W_ji vs a single label) — unresolvable at this scale.
- `[?]` Whether `Error Error Error` is one vertical `Error` bar read three times or three separate bars — local census shows three distinct error-bar glyph lines in the right column, consistent with 3, but the bar count is not resolved.
- `[?]` The `T` in `∑ T(tj -Oj)2` — a sum-index glyph misread, or a distinct on-frame character.

PARSE ADJUDICATION: DEGRADED — every substantive string on the frame is present, but the subtitle and two output labels are dropped, the diagram label run is fused/inverted, and fractions are flattened.
