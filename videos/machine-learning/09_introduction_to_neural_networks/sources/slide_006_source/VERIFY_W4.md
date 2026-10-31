# VERIFY_W4.md — slide 006 "Visualization of Single Layer Perceptron"

Wave 4 web-source audit · scope `src_w4_005_008` · worker `w4-src-005` · date 2026-10-30
Spec audited: `analysis/slide_006_final.json` · banked record: `sources/slide_006_source/SOURCES.md`
Independent second read: `sources/docparse_cascades/slide_006/composed/slide_006_composed.md` + `analysis/reanalysis_v2/slide_006_reanalysis.txt` (14,773 B)
Tooling: `agy -p` CLI quota-exhausted (HTTP 429 RESOURCE_EXHAUSTED, resets ~131 h — re-tested this wave); searches ran through the agy MCP web-search tool (same Antigravity/Google grounding backend; `agy_check_setup` reports no blockers). Every URL marked CONFIRMED was re-fetched live on 2026-10-30.

## Claim register

| # | Claim (from the spec) | Status | Evidence URL | Change to the analysis spec |
|---|---|---|---|---|
| 1 | m output discriminant equations d_k(X) = W_kᵀX with per-class weight row w_k1…w_kn and per-class bias b_k·1 | CONFIRMED | https://cseweb.ucsd.edu/~dasgupta/151/multiclass-handout.pdf | none. UCSD verbatim: "Multiclass Perceptron — Model: w1, . . . , wk ∈ Rᵈ and b1, . . . , bk ∈ R" |
| 2 | One shared augmented input vector X = [x1, x2, x3, ..., xn, 1] broadcast to every output unit | CONFIRMED | https://blog.gopenai.com/mastering-multiclass-classification-with-single-layer-perceptrons-matlab-implementation-from-d8d30e979dec | none. "The output layer has c neurons, one for each class"; logits Z = X·W + b over one shared input matrix |
| 3 | Colour-grouped weights (w1j red, w2j blue, wmj green) with matching bias labels b1, b2, bm | CONFIRMED | https://cseweb.ucsd.edu/~dasgupta/151/multiclass-handout.pdf | none (course styling of the frame's own per-class weights; frame wins for pixels). Doc-parse crop-table x→w pairings remain a column-extraction artifact — not frame data, already flagged in wave 3 |
| 4 | One Σ summation node per output, each followed by a step/threshold activation box | CONFIRMED | https://blog.gopenai.com/mastering-multiclass-classification-with-single-layer-perceptrons-matlab-implementation-from-d8d30e979dec | none (canonical SLP layer schematic: per-class linear score + activation) |
| 5 | Per-unit output wording ">0 Class k / <0 Not Class k" = one-vs-all hard-threshold framing; joint rule is argmax_k d_k(X) | CONFIRMED | https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 | none. MS Learn: "a binary model is created for each of the multiple output classes… against its complement (all other classes in the model)"; UCSD: "Prediction: On instance x, predict label arg max_j (w_j · x + b_j)". Frame wording preserved verbatim |
| 6 | Scope: one linear hyperplane per output unit → solves linearly-separable multiclass, not non-linearly-separable ones such as XOR | CONFIRMED | https://en.wikipedia.org/wiki/Perceptrons_(book) | none. Minsky & Papert 1969 parity/XOR limitation; "The perceptron convergence theorem was proved for single-layer neural nets" |
| 7 | Activation-box inner content, ellipse rows, node shapes/fills, exact font sizes | UNVERIFIED (visual only — no source counterpart) | — | none; not DATA |

Corroborating reads (no web spend): doc-parse composed parse prints verbatim "d1(X) = W1 T X = w11 x1+w12x2+......+w1n xn+b1*1" (and d2, dm), the shared input column x1…xn, 1, the per-class weight rows w11…wmn with b1…bm, the Σ node, and the "Multi-Class Classification" label.

## Questions asked (agy, this wave)
1. single-layer perceptron multiclass — per-class weight row and bias over a shared augmented input; argmax versus one-vs-all thresholding
2. single-layer perceptron / one-vs-all cannot solve non-linearly-separable problems such as XOR (Minsky & Papert 1969)
3. re-fetch check of the UCSD multiclass handout (per-class weights/biases + argmax readout)

## Verification summary
- Claims checked: 7
- CONFIRMED: 6 · CORRECTED: 0 · UNVERIFIED: 1 (visual-only)
- Verified URLs (live-fetched 2026-10-30): 4
  1. https://cseweb.ucsd.edu/~dasgupta/151/multiclass-handout.pdf — HTTP 200, pdftotext extracted
  2. https://blog.gopenai.com/mastering-multiclass-classification-with-single-layer-perceptrons-matlab-implementation-from-d8d30e979dec — HTTP 200, text extracted
  3. https://en.wikipedia.org/wiki/Perceptrons_(book) — HTTP 200, text extracted
  4. https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 — HTTP 200, text extracted
- Honest failures (not cited as verified): none this slide
- Spec patches applied: none (0 corrected claims; frame text unchanged)
- Open build-time check (unchanged from wave 3): the fresh vision pass read ">0" where the frame prints "<0" in each "Not Class k" pair — confirm against `unique_slides/slide_006.jpg` at build time; no source resolves a frame-text question.
