# Parse adjudication — slide 011 (10_nn_training_and_example)

SOURCE IMAGE: `unique_slides/slide_011.jpg` (960x540 px, md5 48834aef85730aa5e096e5faab2e66b1)
PARSE TRANSCRIPT: `analysis/parse/slide_011.parse.md` + `analysis/parse/slide_011.parse.json`
ENVELOPE: finish_reason=`stop`, usage.output_tokens=160, content_len=418 -> **valid call**
SECOND READ TYPE: **corroborated** — (a) re-analysis vision read `analysis/reanalysis/slide_011_final.json` (verdict PASS_WITH_FIXES, independent vision model; question asked: full layout/regions/labels extraction); (b) image-analysis cross-check `analysis/parse/adjudication/vision/slide_011.vision.txt` (independent vision read; question asked: transcribe every text item region by region, reproduce fractions/sums/superscripts as seen).
MEASUREMENT: `analysis/parse/adjudication/measurements/slide_011.pil.txt`, glyph census `glyphs.py`.

## Severity-ranked findings

### MAJOR — `hallucinated-content` — `e li` is an invented symbol run (confidence: high, corroborated)
Parse line: `Δ ji = −η ∂E ∂ e li = −∂ E ∂ Netj ∂ wji = η δj * Oi`.
The token `e li` has no counterpart in any read. The second read gives the rule as
`Δ_ji = η (t_j - O_j) * O_j(1-O_j) * O_i` with `∂E/∂Net_j`; the `e li` run sits where a `Net_j` or `O_j`
subscripted base should be. -> A symbol string with no counterpart on the frame. REAL.

### MAJOR — `dropped-region` — `Output 2` and `Output m` missing (confidence: high, corroborated)
Parse contains `Output 1` only. The second read lists `Output 1`, `Output 2`, `Output m` as three on-slide labels.
Local corroboration (measured): the right output column shows **two** separate label blocks at the same x span
(x=677..761 at y=171..192 and x=677..760 at y=245..266) plus a third output-class stack at x=517..760, y=307..353 —
a 3-fold vertical repetition that one `Output 1` cannot cover. REAL.

### MAJOR — `reading-order-inversion` — the diagram label run is emitted as an unordered flat list (confidence: high, corroborated)
Parse order: `Input Sample / Target Label / Label / Class 1 / Σ / Neti Oi Wji / Output 1 / Wjj / Class 2 / Class m / Node Bias`.
`Class 1` is emitted before the node labels it sits to the right of, `Σ` (the node glyph) is emitted mid-list rather than
at the nodes, `Output 1` is interleaved between `Neti Oi Wji` and `Wjj`, and `Class 2`/`Class m` trail `Node Bias`.
The measured diagram has three label rows (y=168..194, y=233..277, y=307..353) each spanning the three node columns —
the parse's order does not track that row/column structure. REAL.

### MAJOR — `hallucinated-content` — `Wjj` (confidence: high, corroborated)
Parse emits `Wjj` as a diagram label. The second read gives the weight label as `W_ji`; every sibling parse in this
range that reads the same weight reads `Wji`/`W ji`/`w ji` — never `Wjj`. The final `j` is a subscript misread.
REAL.

### MINOR — `hallucinated-content` — the standalone label `Label` (confidence: medium-high, corroborated)
Parse emits `Label` as its own label, immediately after `Target Label`. Neither vision read lists a bare `Label` on the
frame; `Target Label` is the only label string of that family. The parse appears to have split `Target Label` into two
tokens. REAL as a defect, MINOR (it duplicates a string already present).

### MINOR — `math-normalization-loss` — stacked fractions flattened (confidence: high, corroborated)
`Δ ji = −η ∂E ∂ e li` and `δj = −∂E ∂ Netj` render numerators and denominators as sequential linear runs with no
division structure. The second read keeps the fraction form. REAL (format only).

### MINOR — `dropped-region` / glyph-floor — the bottom green-bordered caption box is unparsed (confidence: medium, corroborated)
The second read reports a green-bordered caption box at the bottom of the slide. Measured: the bottom strip
x=70..930, y=390..540 carries **127 glyph-scale components across 4 distinct text lines** (y=390, 413-418, 426-441,
482-498) — heavy text ink that the parse's content does not cover as a distinct region. The parse's last line is the
δ rule, which sits above this strip. REAL as a coverage gap; the exact box contents are DEBATABLE.

## Explicit classification list

- REAL (high, corroborated): `e li` symbol run invented — `hallucinated-content`, MAJOR.
- REAL (high, corroborated): `Output 2` and `Output m` dropped — `dropped-region`, MAJOR.
- REAL (high, corroborated): diagram labels emitted as an unordered flat run — `reading-order-inversion`, MAJOR.
- REAL (high, corroborated): `Wjj` misread for `W_ji` — `hallucinated-content`, MAJOR.
- REAL (medium-high, corroborated): spurious standalone `Label` token — `hallucinated-content`, MINOR.
- REAL (high, corroborated): stacked fractions flattened inline — `math-normalization-loss`, MINOR.
- REAL (medium, corroborated): bottom green caption box unparsed — `dropped-region`, MINOR.
- DEBATABLE (advisory): the badge numeral `11` is present in the parse (`( Calculated Error is affected by Net) 11`) but the
  second read renders the subtitle as `( Calculated Error is affected by Net_i )` — the parse drops the `_i` subscript. Whether the
  trailing `11` is the badge numeral or a second copy of the subtitle's final glyph is resolved in favour of the badge
  (both reads place a `11` badge top-right), but the `_i` loss is a real MINOR subscript loss.
- HALLUCINATED: `e li`, `Wjj`, standalone `Label`.

## Uncertainty markers

- `[?]` Whether the bottom green caption box holds a fourth equation or a prose annotation — the parse does not cover it and my local census cannot resolve letterforms at 6-14 px.
- `[?]` The activation-box glyph the second read calls `[f/∫] activation-box glyph`; the parse emits `Σ` once, which may or may not be that glyph.

PARSE ADJUDICATION: DEGRADED — the parse captures the title, subtitle, badge and the δ rules, but it invents `e li` and `Wjj`, splits `Target Label` into a spurious `Label`, drops two output labels, inverts the diagram reading order, and leaves the bottom caption box uncovered.
