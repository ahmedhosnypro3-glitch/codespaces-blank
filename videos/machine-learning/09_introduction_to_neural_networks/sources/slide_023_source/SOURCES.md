# Source Research for slide_023

## Doc-Parse Transcript
**File**: `slide_023.parse.md` (from nemotron-parse)
**Model**: nemotron-parse
**Finish Reason**: stop
**Output Tokens**: 206

### Parsed Content (Raw)
```
<x_0.0596><y_0.0781>**Derivatives of some Activation Functions** 23
f(x)=Uni-polar Unit Step = 0 for x<0 1 for x≥0 Derivative f' (x)= 0 for x≠0 ? for x=0
f(x)= Bi-polar Unit Step = −1 for x<0 1 for x≥0 Derivative f' (x)= 0 for x≠0 ? for x=0
f(x)= Sigmoid (x)= 1 +e−x 1+e−x > f' (x)=f(x) ( 1–f(x) )
f(x)=tanh(x)= sinh x cosh x Derive f' (x)= tan−1(x) Derive f' (x)= 1–f(x)2
IVative f' (x)= 1 x2+1
<x_0.9336><y_0.9547><class_Picture>
```

### Interpretation
This slide (number 23) presents derivatives of four common activation functions:
1. **Uni-polar Unit Step** (Heaviside step function) - outputs 0 or 1
2. **Bi-polar Unit Step** - outputs -1 or 1
3. **Sigmoid (Logistic)** - outputs between 0 and 1
4. **Tanh (Hyperbolic Tangent)** - outputs between -1 and 1

The `<class_Picture>` at bottom right likely indicates a visual diagram/plot of these functions.

## OCR Errors & Corrections (from web search verification)

| Slide Text (OCR) | Corrected Version | Notes |
|------------------|-------------------|-------|
| `f(x)= Sigmoid (x)= 1 +e−x 1+e−x >` | `f(x) = σ(x) = 1/(1 + e⁻ˣ)` | ">" is OCR error for "=" or division; missing parentheses |
| `f' (x)=f(x) ( 1–f(x) )` | `f'(x) = f(x)(1 - f(x)) = σ(x)(1 - σ(x))` | Correct formula |
| `f(x)=tanh(x)= sinh x cosh x` | `f(x) = tanh(x) = (eˣ - e⁻ˣ)/(eˣ + e⁻ˣ) = sinh(x)/cosh(x)` | "sinh x cosh x" means ratio sinh/cosh |
| `Derive f' (x)= tan−1(x)` | **WRONG on slide** — tan⁻¹(x) is arctan derivative | Slide likely has typo: should be `1 - tanh²(x)` or `sech²(x)` |
| `Derive f' (x)= 1–f(x)2` | `f'(x) = 1 - f(x)² = 1 - tanh²(x)` | Correct formula (using f(x)=tanh(x)) |
| `IVative f' (x)= 1 x2+1` | **WRONG on slide** — this is d/dx arctan(x) = 1/(1+x²) | "IVative" = "Derivative" OCR error; formula is for arctan, NOT tanh |

## Web Search Verification
**Query**: "neural network activation functions derivatives uni-polar unit step bi-polar unit step sigmoid tanh derivative formulas"
**Sources**:
1. Google ML Crash Course - Activation Functions: https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions
2. Baeldung - Sigmoid vs Tanh Functions: https://www.baeldung.com/cs/sigmoid-vs-tanh-functions

### Verified Formulas

| Function | Formula | Derivative |
|----------|---------|------------|
| Uni-polar Unit Step | φ(z) = 1 if z≥0 else 0 | φ'(z) = 0 (z≠0), undefined at z=0 |
| Bi-polar Unit Step | φ(z) = 1 if z≥0 else -1 | φ'(z) = 0 (z≠0), undefined at z=0 |
| Sigmoid | σ(z) = 1/(1+e⁻ᶻ) | σ'(z) = σ(z)(1-σ(z)) |
| Tanh | tanh(z) = (eᶻ-e⁻ᶻ)/(eᶻ+e⁻ᶻ) | tanh'(z) = 1 - tanh²(z) = sech²(z) |

## Research Summary
- **Slide title**: "Derivatives of some Activation Functions" (slide 23)
- **Content**: Four activation functions with their derivatives
- **Issues found on original slide**: Two derivative formulas appear incorrect (tanh derivative shown as tan⁻¹(x) and 1/(1+x²) which are arctan derivatives)
- **Visual element**: `<class_Picture>` at bottom right suggests a chart/diagram of the functions
- **Next step**: Vision analysis to capture layout, colors, and visual elements precisely

## Research Status
- Doc-parse: ✅ Complete
- Web search: ✅ Complete (verified formulas, found slide errors)
- Sources banked: ✅ Yes
---

## Wave-2 verification (wave-3 dispatch, agent src-021-024, 2026-10-30)

Content evidence used: `analysis/reanalysis_v2/slide_023_reanalysis.txt` is MISSING, so per
mandate fell back to `analysis/slide_023_final.json` (title "Derivatives of some Activation
Functions"; FIVE rows: Uni-polar Unit Step, Bi-polar Unit Step, Sigmoid, tanh, tan^-1(x)) and
`sources/docparse_cascades/slide_023/composed/slide_023_composed.md`.

Search method: `agy -p` CLI quota-exhausted (429, reset ~154h), so the 4 searches ran through
the agy MCP web-search tool (Google grounding, redirects resolved). All URLs returned by the
tool — none invented. Raw log: `wave3_agy/search_log.md`.

### Verified claims (wave-2)

1. **Uni-polar Unit Step (Heaviside) `f(x) = { 0 for x<0 ; 1 for x>=0 }`, derivative `f'(x) = 0
   for x != 0`, UNDEFINED at x = 0** (classical: jump discontinuity; distributional: Dirac
   delta). The slide's `f'(x) = { 0 for x≠0 ; ? for x=0 }` is exactly right — the `?` marks the
   undefined point. — CONFIRMED.
   - https://en.wikipedia.org/wiki/Heaviside_step_function
   - https://math.fel.cvut.cz/cz/mt/txtb/4/txe3ba4l.htm
   - https://math.stackexchange.com/questions/238193/on-the-derivative-of-a-heaviside-step-function-being-proportional-to-the-dirac-d
2. **Bi-polar Unit Step (= sign function / `2*H(x)-1`) `f(x) = { -1 for x<0 ; 1 for x>=0 }`,
   derivative 0 for x != 0, undefined at 0; zero gradient makes it unusable with backprop** —
   CONFIRMED.
   - https://ai.stackexchange.com/questions/28395/an-explanation-involving-the-sign-activation-its-affect-on-the-loss-function-a
   - https://longcode.online/docs/deep-learning-ai-course-notes/neural-networks-and-deep-learning/week-3/derivatives-of-activation-functions/
3. **Sigmoid `f'(x) = f(x)(1-f(x))`** — CONFIRMED with full chain-rule derivation.
   - https://math.stackexchange.com/questions/78575/derivative-of-sigmoid-function-sigma-x-frac11e-x
4. **tanh `f(x) = sinh x / cosh x`, `f'(x) = 1 - f(x)^2 = sech^2(x)`** (quotient rule +
   cosh^2 - sinh^2 = 1) — CONFIRMED.
   - https://derivative-calculator.org/proofs/tanh/
   - https://www.cuemath.com/calculus/derivative-of-hyperbolic-functions/
5. **tan^-1(x) (arctan) `f'(x) = 1/(x^2+1)`** (implicit differentiation, sec^2 y = 1+tan^2 y) —
   CONFIRMED.
   - https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/37028101f134cc6e0e41572fdc6735d8_MIT18_01SCF10_Ses15b.pdf
   - https://www.geeksforgeeks.org/maths/derivative-of-arctan/

### Correction to the earlier wave's note

The earlier section above flagged the tanh row as "WRONG on slide" (claiming the slide showed
`tan^-1(x)` as tanh's derivative). That was an artifact of the doc-parse OCR interleaving rows.
Per `analysis/slide_023_final.json` the slide has FIVE rows and every row is correct:
tanh -> `f'(x) = 1 - f(x)^2`, and arctan is its OWN fifth row -> `f'(x) = 1/(x^2+1)`. No slide
error; the earlier "slide typo" claims are withdrawn.
