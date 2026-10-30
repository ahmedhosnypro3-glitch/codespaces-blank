# SOURCES.md — slide_012_source

**Slide**: 12 of 32 (printed badge "12")
**Image**: `unique_slides/slide_012.jpg`
**Topic**: Classification of the "OR" Truth Table by a single-layer perceptron

---

## 1. Doc-parse transcript

From `slide_012.parse.md` (nemotron-parse, single full-frame read):

```
<x_0.292><y_0.1242>**Classification of "OR" Truth Table**<class_Section-header>
<x_0.9043><y_0.1164>12<x_0.9209><y_0.1508><class_Text>
<x_0.0996><y_0.2547>tabular{ccc}
  **X<sub>1</sub>** & **X<sub>2</sub>** & **O/P**\\
  0 & 0 & 0\\
  0 & 1 & 1\\
  1 & 0 & 1\\
  1 & 1 & 1\\<x_0.3281><y_0.5672><class_Table>
<x_0.5615><y_0.2031>X2 / 0.4 / 0.28 / X1<x_0.876><y_0.6805><class_Picture>
<x_0.1455><y_0.6508>-7 / >0 = 1 / <0 = 0 / X2 -5 / Σ O/P / 1 / 2<x_0.5322><y_0.9062><class_Picture>
<x_0.6104><y_0.7891>d(X)=-7x1-5x2+2<x_0.8262><y_0.8422><class_Formula>
```

### Adjudication vs source image (single-read, parse claims pending vision cross-check)

- Title text and badge number 12: REAL (top of frame).
- Truth-table header row `X1 | X2 | O/P` with the four OR rows: REAL (class_Table at x≈0.10–0.33, y≈0.25–0.57).
- Axis labels `X2` (top) / `X1` (bottom) with tick values `0.4` and `0.28`: PARTIAL — tick positions plausible but the two numbers could be misread tick labels; flagged `[?]`.
- Annotation `>0 = 1` and `<0 = 0` with coefficients `-7` and `-5`: REAL (annotation region beside decision line).
- Formula `d(X) = -7x₁ - 5x₂ + 2`: REAL (class_Formula at x≈0.61–0.83, y≈0.79–0.84).
- `Σ O/P` over `1` / `2`: PARTIAL — likely "O/P = 1" / "O/P = 2" style region labels on the diagram; flagged `[?]`.

## 2. Web-verified facts (agy search, 2026 run)

**OR gate + single-layer perceptron (linear separability):**

- OR outputs 1 when at least one input is 1; outputs 0 only at (0,0). Verified table:
  | X1 | X2 | O/P |
  |----|----|-----|
  | 0  | 0  | 0   |
  | 0  | 1  | 1   |
  | 1  | 0  | 1   |
  | 1  | 1  | 1   |
- A single-layer perceptron computes z = (w1·x1) + (w2·x2) + b with a step activation:
  output = 1 if z ≥ 0, else 0 (some slides write >0 = 1, <0 = 0 — matches the slide annotation).
- The OR function IS linearly separable; one standard weight set is w1 = 1, w2 = 1, b = -0.5,
  boundary x1 + x2 - 0.5 = 0.
- Sources:
  - https://www.kaggle.com/code/abdulrahmanelbanna/single-layer-perceptron
  - https://people.sabanciuniv.edu/berrin/cs512/lectures/2015/7-nn2-perceptron.pdf
  - https://beingneuron.com/single-layer-perceptron/
  - https://medium.com/@ngneha090/perceptron-algorithm-basics-to-advanced-5567a8035e42

**The on-slide equation d(X) = -7x₁ - 5x₂ + 2:**

- Decomposes to w1 = -7, w2 = -5, b = +2.
- Checked against OR: d(0,0) = +2 → step gives 1, but OR expects 0; d(0,1) = -3 → 0, but OR expects 1.
  So with the >0 ⇒ 1 / <0 ⇒ 0 rule shown on the slide, the printed weights give INVERTED (NAND-like) logic.
- Verified against the web summary: "The given function does not implement an OR gate… a perceptron
  requires positive weights and a negative bias (e.g. w1=1, w2=1, b=-0.5)". Source:
  https://pages.cs.wisc.edu/~dyer/cs540/notes/09_neuralNets.pdf
- DISCREPANCY FLAG `[?]`: the slide's equation is reproduced verbatim in the recreation (output contract:
  never invent content, verbatim text wins). The build reproduces d(X)=-7x₁-5x₂+2 exactly as printed;
  the visual judge compares to the original frame, not to textbook-correct weights.
- The line is still a valid linear separator of the plane (7x1 + 5x2 = 2), which is the geometric
  point of the slide (OR is linearly separable → a single line decides).
- Sources:
  - https://pages.cs.wisc.edu/~dyer/cs540/notes/09_neuralNets.pdf
  - https://nucs-349-fall21.github.io/lectures/eecs349_linear_discriminants.pdf

## 3. Net corrected facts for the build

1. Title: `Classification of "OR" Truth Table` — verbatim.
2. Table: 3 columns (X1, X2, O/P) × 4 data rows, OR semantics.
3. Diagram: 2-D X1×X2 plane, decision line, annotation `>0 = 1` / `<0 = 0`, region labels near O/P.
4. Equation: `d(X) = -7x₁ - 5x₂ + 2` — rendered in 2D professional format (mathtext PNG).
5. House frame rule applies (frame / badge 12 / title y=0.28) — overrides analysis.
6. Uncertain items `[?]`: tick label values `0.4` / `0.28`; the `Σ O/P / 1 / 2` region labels.

## 4. Verdict confidence

single-read (one parse pass + one web-search corroboration pass). All numeric claims about the
truth table and the equation are corroborated by arithmetic; the geometric annotations are
panel-layout claims awaiting the vision-analysis read.
