# Slide 031 — Example: Backpropagation Worked Example (sigmoid + delta rule + weight update)

Frame topic: a fully worked numeric backpropagation example on a 2-3-2 network
(x₁=1, x₂=5, hidden nodes 3/4/5 + Bias, output nodes 6/7, targets t₆=0, t₇=1,
learning rate η=5). Shows output deltas, hidden-layer deltas, ΔW values, and
new W values. Data taken from `analysis/slide_031_raw.json` + `slide_031.parse.md`.

## Sources

- Matt Mazur — "A Step by Step Backpropagation Example"
  (https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/) —
  canonical worked example of exactly this sequence: forward pass, output-layer
  delta, hidden-layer delta, weight update; confirms the teaching structure.
- 365 Data Science — "What Is Backpropagation?"
  (https://365datascience.com/trending/backpropagation/) — confirms the
  hidden-layer delta as `δ = O(1-O)·(Σ δ_next · w)`.
- Wikipedia — "Logistic function" (https://en.wikipedia.org/wiki/Logistic_function)
  — confirms σ(z)=1/(1+e^(−z)) and σ'(z)=σ(z)(1−σ(z)), the identity behind δⱼ.
- SciPy — `scipy.special.expit`
  (https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.expit.html)
  — the standard library implementation of σ; matches `O = 1/(1+e^-z)` exactly.
- Langformers — "Forward Pass & Backpropagation Example"
  (https://blog.langformers.com/forward-pass-backpropagation-example/) —
  independent worked example of the same η·δ·O update arithmetic.

## Corrections / notes

- Every arithmetic line on the frame was recomputed and matches to the digits shown:
  O₃=σ(2.2)=0.900, O₄=σ(2.8)=0.943, O₅=σ(3.4)=0.968, O₆=O₇=σ(1.3312)=0.791;
  δ₆=0.791·(1−0.791)·(0−0.791)=−0.131; δ₇=0.791·(1−0.791)·(1−0.791)=0.035;
  δ₃, δ₄, δ₅ = 0.0049 / 0.0026 / 0.0013, rounded to 0.005 / 0.003 / 0.001 on frame.
  ΔW and new-W lines are consistent with ΔW = η·δⱼ·Oᵢ and W ← W + ΔW.
- **Sign convention (not an error):** the frame uses δⱼ = Oⱼ(1−Oⱼ)(tⱼ−Oⱼ) with
  ΔW = +η·δ·Oᵢ. Several sources instead write δⱼ = (Oⱼ−tⱼ)·Oⱼ(1−Oⱼ) with
  W ← W − η·δ·Oᵢ (e.g. the Illinois/MRCET lecture notes in slide 34's sources).
  The two are algebraically identical (flipped δ sign + flipped update sign) — the
  recreation must reproduce the frame's `+` form verbatim, not the minus form.
- Line `ΔW32=5*0.005*1=0.125` is internally inconsistent as printed: its siblings use
  x₂=5 (`ΔW42=5*0.003*5`, `ΔW52=5*0.001*5`) and 5·0.005·5 = 0.125 is the correct
  product. Unverified whether the frame's printed multiplier is a typo or a parse
  mis-read — flag for a vision re-check of that one line, do not silently "fix" it.
- η=5 is very large (see slide 34 sources); the example is arithmetic demonstration,
  not a recommended learning rate. Nothing on the frame to correct.
