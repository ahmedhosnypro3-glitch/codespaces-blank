# VERIFY_W4.md — slide_025 (wave 4, 2026-10-30)

**Scope**: `src_w4_025_028` · worker `w4-src-025` · sink deck `machine-learning/09_introduction_to_neural_networks`
**Analysis spec used**: `analysis/slide_025_final.json` (vision `images`, validated `validate_slides`, verdict PASS_WITH_FIXES, recreatability 9/10)
**Independent second read**: `sources/docparse_cascades/slide_025/composed/slide_025_composed.md` (frame md5 `a82380b2460d1b93d2a3e0e52bedea34`)
**Search transport**: `agy -p` CLI is quota-exhausted (HTTP 429 `RESOURCE_EXHAUSTED`, resets ~131h; probe transcript banked at `agy_wave4/w4_cli_probe_429.txt`). All queries ran through the **agy web-search MCP** route — the same Google grounding service, same citation discipline. Every URL below was returned by that search service; none invented.

## Claim register

| # | Claim (DATA-level, from analysis spec + frame) | Status | Evidence / URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | Linear (identity) activation is `F(x) = x` — passes the input through unchanged, f′(x)=1, range (−∞,+∞) | CONFIRMED | "Linear (Identity) Activation … Equation: f(x)=x … Range: (−∞,+∞) … used in the output layer for regression … stacked linear layers collapse into a single linear operation" — https://medium.com/@sushmita2310/12-types-of-activation-functions-in-neural-networks-a-comprehensive-guide-a441ecefb439 ; https://www.roboflow.com/blog/activation-function-computer-vision ; https://en.wikipedia.org/wiki/Activation_function | none — spec's `F(x) = x    Linear (No Activation)` matches canonical identity |
| 2 | Unipolar / binary unit step = 0 for x<0, 1 for x≥0 (output range {0,1}) | CONFIRMED | "f(x) = 1 if x ≥ 0, 0 if x < 0 … Range: {0,1} … not differentiable at x=0 and derivative 0 elsewhere, impossible to train with gradient descent/backprop" — https://towardsdatascience.com/what-are-activation-functions-in-deep-learning-cc4f01e1cf5c/ ; https://en.wikipedia.org/wiki/Activation_function ; https://encord.com/blog/activation-functions-neural-networks/ | none |
| 3 | Bipolar unit step = −1 for x<0, +1 for x≥0 (output range {−1,+1}) | CONFIRMED (Wave-1 OCR ambiguity stays resolved) | "f(x) = +1 if x ≥ 0, −1 if x < 0 … Range: {−1,+1} … used in Adaline / Hopfield where bipolar representations are preferred" — https://en.wikipedia.org/wiki/Activation_function ; https://encord.com/blog/activation-functions-neural-networks/ ; https://towardsdatascience.com/what-are-activation-functions-in-deep-learning-cc4f01e1cf5c/ | none — doc-parse rendered `1 for x<0` in one lane; LaTeX crop + Wave-2/Wave-3/Wave-4 sources all give −1. Frame text is reproduced verbatim as captured; −1 is corroborated |
| 4 | The three panels are schematic function curves, not plots of measured data | CONFIRMED | Identity line, {0,1} step and {−1,+1} step are textbook schematic activation curves; no dataset or fitted values exist behind them — https://en.wikipedia.org/wiki/Activation_function | none — build as matplotlib line plots (f(x) vs x), not data charts |
| 5 | Step-activation nets cannot be trained by backpropagation (f′=0 a.e., undefined at threshold) | CONFIRMED (context only — NOT printed on frame) | "not differentiable at x=0 and has a derivative of 0 everywhere else, making it impossible to train using gradient descent / backprop" — https://en.wikipedia.org/wiki/Activation_function ; https://encord.com/blog/activation-functions-neural-networks/ | none — conceptual bridge to slide 026; DATA-level note only |
| 6 | Badge numeral on the frame | UNVERIFIABLE from web — needs the frame | Web research cannot settle a printed numeral. `slides_index.json` maps `slide_025.jpg` → badge `25`; the analysis spec reads **17**. Both readings are banked. `???` — builder must read the numeral off `unique_slides/slide_025.jpg` per the house badge rule | none — flagged, not resolved by this worker |
| 7 | Axis tick ranges/values on the three plots | UNVERIFIED | Not recoverable from doc-parse (the `composed/` file for 025 recovered only the title; the graph panels were one `<class_Picture>` element) and not derivable from the frame text. No numeric ticks are readable from the analysis spec either | none — keep schematic (x ≈ [−3,3], f(x) ticks at −1/0/1) pending vision measurement; the y-levels 1 / ±1 derive from the paired equations, not axis readings |

## Questions asked (all via agy web-search MCP)

1. "sigmoid activation function σ(x)=1/(1+e^-x) range (0,1) σ(0)=0.5 derivative σ(x)(1−σ(x)) maximum 0.25 at x=0" (run to corroborate slide 026; also serves 025's step-family context)
2. "linear identity activation function f(x)=x no activation; binary step unipolar unit step 1 if x≥0 else 0 range {0,1}; bipolar unit step sign function +1 if x≥0 else −1 range {−1,+1}" — the primary 025 query
3. `agy -p` CLI probe (transcript: `agy_wave4/w4_cli_probe_429.txt`) failed with the 429 quota error — the honest failure record for this slide.

## Doc-parse cross-check

`sources/docparse_cascades/slide_025/composed/slide_025_composed.md` recovers only the badge numeral and the title as one `<class_Picture>` item across two passes — it does **not** corroborate or contradict any of the three formulas. All geometry here rests on `slide_025_final.json` plus vision. The doc-parse's bipolar `1 for x<0` lane is superseded by its own LaTeX crop lane and by this wave's sources.

## Net effect on the analysis spec

**0 changes.** Every DATA-level claim in `slide_025_final.json` is either CONFIRMED by this wave's sources or is a frame-pixel question web research cannot answer (badge numeral, axis tick values). No `[?]` was removed. Existing banked evidence in `SOURCES.md` (Wave-1/-2/-3) is untouched; this register is additive.
