# SOURCES.md — slide_013_source

**Slide**: 13 of 32 (printed badge "13")
**Image**: `unique_slides/slide_013.jpg`
**Topic**: Classification of the "XOR" Truth Table — not linearly separable

---

## 1. Doc-parse transcript

From `slide_013.parse.md` (nemotron-parse, single full-frame read):

```
<x_0.292><y_0.1242>**Classification of "XOR" Truth Table**<x_0.7441><y_0.175><class_Section-header>
<x_0.9033><y_0.1172>13<x_0.9238><y_0.1516><class_Text>
<x_0.0996><y_0.2547>tabular{ccc}
  thead{X<sub>1</sub>} & thead{X<sub>2</sub>} & thead{O/P}\\
  0 & 0 & 0\\
  0 & 1 & 1\\
  1 & 0 & 1\\
  1 & 1 & 0\\<x_0.3281><y_0.5672><class_Table>
<x_0.5576><y_0.2023>X2 / X / X1 / X1<x_0.876><y_0.6805><class_Picture>
<x_0.1455><y_0.6508>X1 / ? / X2 / ? / Z O/P / 1 / ?<x_0.5361><y_0.9062><class_Picture>
<x_0.6152><y_0.7859>_Not Linearly Separable_<x_0.833><y_0.8359><class_Page-footer>
```

### Adjudication vs source image (single-read, parse claims pending vision cross-check)

- Title text and badge number 13: REAL (top of frame).
- Truth-table header `X1 | X2 | O/P` with rows 00→0, 01→1, 10→1, 11→0: REAL (class_Table at x≈0.10–0.33, y≈0.25–0.57); classic XOR semantics, matching the documented table exactly.
- `X2` axis label at top with `X1` axis labels in the diagram region (x≈0.56–0.88, y≈0.20–0.68): REAL (two axes of an input plane).
- Scattered `X` marks and `?` tokens in the lower diagram (x≈0.15–0.54, y≈0.65–0.91): PARTIAL — `?` tokens are the parser's uncertainty glyphs for small/low-contrast glyphs (likely small point labels or question marks marking the failure case); flagged `[?]`.
- `Z O/P` and `1` near the diagram: PARTIAL — likely a small "O/P = 1"-style region annotation or point label; flagged `[?]`.
- Footer text `_Not Linearly Separable_` (italic on slide, class_Page-footer at x≈0.62–0.83, y≈0.79–0.84): REAL — THE KEY MESSAGE of the slide.

## 2. Web-verified facts (agy search, 2026 run)

**XOR gate definition:**

- XOR outputs 1 only when the inputs differ; 0 when the inputs are the same. Verified table:
  | X1 | X2 | O/P |
  |----|----|-----|
  | 0  | 0  | 0   |
  | 0  | 1  | 1   |
  | 1  | 0  | 1   |
  | 1  | 1  | 0   |
- Plotted on the X1×X2 plane: class 0 = {(0,0), (1,1)} (diagonal), class 1 = {(0,1), (1,0)} (anti-diagonal).
- Sources:
  - https://www.geeksforgeeks.org/artificial-intelligence/how-neural-networks-solve-the-xor-problem/
  - https://www.playwithml.com/xor-problem
  - https://apxml.com/courses/introduction-to-deep-learning/chapter-1-neural-network-foundations/perceptron-limitations

**Not linearly separable (the classic perceptron limitation):**

- A single-layer perceptron draws exactly one straight decision boundary (w1x1 + w2x2 + b = 0).
- The four XOR constraints b < 0, w2 + b ≥ 0, w1 + b ≥ 0, w1 + w2 + b < 0 are mutually contradictory
  (w2 + b ≥ 0 and w1 + b ≥ 0 imply w1 + w2 + 2b ≥ 0, which conflicts with w1 + w2 + b < 0 given b < 0).
- Hence no single straight line separates the classes — "Not Linearly Separable", the slide's footer, verified.
- Historical anchor: Minsky & Papert, *Perceptrons* (1969), proved the SLP cannot compute XOR.
- Fix: a multi-layer perceptron with a hidden layer creates a non-linear boundary (region-combining).
- Sources:
  - https://www.geeksforgeeks.org/artificial-intelligence/how-neural-networks-solve-the-xor-problem/
  - https://bnaskrecki.faculty.wmi.amu.edu.pl/nnets/_build/html/part3_limitations/ch08_xor_problem.html
  - https://www.cs.toronto.edu/~axgao/cs486686_f21/lecture_notes/Lecture_08_on_Neural_Networks_1.pdf
  - https://medium.com/kritrimlabs-ai/introduction-to-neural-networks-part-2-879d9660b929

## 3. Net corrected facts for the build

1. Title: `Classification of "XOR" Truth Table` — verbatim.
2. Table: 3 columns (X1, X2, O/P) × 4 data rows, XOR semantics (00→0, 01→1, 10→1, 11→0).
3. Diagram(s): X1×X2 input plane showing the diagonal class-0 / anti-diagonal class-1 point pattern,
   with axis labels X1 and X2 and an "O/P" region annotation — the point positions are the classic XOR layout.
4. Footer: `_Not Linearly Separable_` — rendered italic, positioned near bottom-center-right.
5. House frame rule applies (frame / badge 13 / title y=0.28) — overrides analysis.
6. Uncertain items `[?]`: the `?` glyphs, `Z O/P / 1` label, exact point-mark styling (X marks vs dots).

## 4. Verdict confidence

single-read (one parse pass + one web-search corroboration pass). The truth-table content is
corroborated by arithmetic and by every cited source; the diagram annotations are layout claims
awaiting the vision-analysis read.

---

## Wave-3 verification (2026-10-30, agy web search)

Content evidence used: `analysis/reanalysis_v2/slide_013_reanalysis.txt` (fresh vision
re-read, 2026-10-29; full slide geometry) cross-checked with `analysis/slide_013_final.json`
(validation verdict PASS_WITH_FIXES). Searches: 2 via `agy -p` CLI, 1 via the agy MCP
Google-grounding endpoint (CLI individual quota hit 429 mid-run; same agy service, file token).

### Concepts on the slide, web-verified

1. **XOR truth table (verbatim match to the slide's table).** XOR outputs 1 iff the inputs
   differ: 00→0, 01→1, 10→1, 11→0. Class 0 = diagonal {(0,0),(1,1)}, class 1 =
   anti-diagonal {(0,1),(1,0)}.
   - https://dev.to/jbahire/demystifying-the-xor-problem-1blk
   - https://www.geeksforgeeks.org/artificial-intelligence/how-neural-networks-solve-the-xor-problem/
   - https://www.playwithml.com/xor-problem
2. **"Not Linearly Separable" (the slide's caption).** A single-layer perceptron draws exactly
   one straight decision boundary `w1·x1 + w2·x2 + b = 0`; the four XOR constraints
   (b<0, w2+b≥0, w1+b≥0, w1+w2+b<0) are mutually contradictory, so no single line separates
   the classes. AND and OR are linearly separable; XOR is not. Minsky & Papert, *Perceptrons*
   (1969) proved the SLP cannot compute XOR (first AI winter); MLPs with hidden layers fix it.
   - https://mitpress.mit.edu/9780262631112/perceptrons/
   - https://en.wikipedia.org/wiki/Perceptrons_(book)
   - https://web.stanford.edu/group/pdplab/pdphandbook/handbookch5.html (XOR inequality proof)
   - https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/
   - https://www.cs.cmu.edu/~mgormley/courses/ (10-601; perceptron readings PDF)
   - https://www.cs.toronto.edu/~rgrosse/courses/csc321_2018/
   - http://lxmls.it.pt/2018/Lecture.fin.pdf
   - https://seantrott.substack.com/p/perceptrons-xor-and-the-first-ai
3. **Single-neuron schematic (x1, x2, bias 1 → Σ → step → O/P, weights "?").** The perceptron
   computes `z = Σ wᵢxᵢ + b` then applies a threshold/step activation `f(z)`; the bias can be
   modeled as a fixed input x₀=1 with weight w₀ (the "bias trick"). The printed "?" glyphs mark
   the unknown weights — consistent with a not-yet-trained single neuron that cannot solve XOR.
   - https://cs231n.github.io/neural-networks-1/ (bias trick, activation functions)
   - http://neuralnetworksanddeeplearning.com/chap1.html (Nielsen, ch.1 — perceptron, threshold vs bias)
   - https://psycnet.apa.org/record/1959-09865-001 (Rosenblatt 1958, original perceptron)
   - https://hdl.handle.net/1813/40306 (Rosenblatt 1958 Cornell report)
   - https://www.microsoft.com/en-us/research/people/cmbishop/prml-book/ (Bishop PRML §4.1.7)
   - https://www.deeplearningbook.org/contents/mlp.html (Goodfellow ch.6, Learning XOR)
4. **Scatter plot with two parallel lines.** Two parallel lines bracketing one class is the
   classic picture of "needs two boundaries, has one" — the visual form of non-separability;
   a two-hidden-unit MLP supplies exactly the two lines.
   - https://www.playwithml.com/xor-problem
   - https://cs-114.org/wp-content/uploads/2025/02/7_NN_Apr_28_2021.pdf

### Verdict
No content corrections needed: title, truth table, caption, and schematic semantics all match
web-verified facts. House frame rule still overrides frame/badge/title-y for the build.
