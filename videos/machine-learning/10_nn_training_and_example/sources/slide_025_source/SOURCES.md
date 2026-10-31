# Source Research — slide_025 (ReLU)

Topic: ReLU definition and derivative (piecewise form), with tanh/sigmoid vs their
derivatives illustrating the vanishing-gradient problem.

## Verified definitions (match slide verbatim)
- ReLU: f(x) = max(0, x) — i.e. 0 for x<0, x for x≥0. Matches the slide's definition.
- ReLU derivative: 0 for x<0, 1 for x≥0. Undefined exactly at 0; implementations use
  0 or 1 there. Slopes of ±1 never shrink a backprop gradient (except "dying ReLU"
  when a unit stays negative — gradient 0, unit stops updating).
- Sigmoid σ(x) = 1/(1+e^−x); derivative σ(x)(1−σ(x)), max 0.25 at x=0, →0 at
  |x|≳2 (saturation) ⇒ strong vanishing gradient across layers.
- Tanh(x); derivative 1−tanh²(x), max 1.0 at x=0, →0 at saturation ⇒ milder but still
  vanishing gradient; zero-centered, so converges faster than sigmoid.
- The two paired "Vanishing Gradients" charts (activation curves + derivative curves
  for Tanh and Sigmoid) are the standard comparison illustrating why ReLU is used.

## Sources
- "Intuitions behind different activation functions in deep learning" (Towards Data
  Science) — https://towardsdatascience.com/intuitions-behind-different-activation-functions-in-deep-learning-a2b1c8d044a/
  Piecewise ReLU f/deriv, dying-ReLU caveat, vanishing-gradient intuition.
- "Tanh vs Sigmoid vs ReLU" (GeeksforGeeks) —
  https://www.geeksforgeeks.org/deep-learning/tanh-vs-sigmoid-vs-relu/
  Derivative formulas 1−tanh²(x) and σ(x)(1−σ(x)); saturation ranges.
- "Tanh, Sigmoid and ReLU Activation Functions: A Comparative Study" (Medium) —
  https://medium.com/@anjansingla/tanh-sigmoid-and-relu-activation-functions-a-comparative-study-c97729fafb3f
  Vanishing-gradient comparison (sigmoid max deriv 0.25 vs tanh 1.0).
- "Comparison of ReLU's derivative and ÂD" figure (ResearchGate) —
  https://www.researchgate.net/figure/Comparison-of-ReLUs-derivative-and-AD_fig1_348825567
  Derivative-curve comparison figures for ReLU vs saturating activations.

## Corrections / notes
- Data caveat (parse transcript, not sources): the derivative line in
  analysis/parse/slide_025.parse.md reads "f'(x)= 1 for x<0 for x≥0" — partially
  garbled OCR; the standard (and near-certain on-frame) values are 0 for x<0 and
  1 for x≥0. Verify against slide_025.jpg before drawing.
- Data caveat: the parse transcript's chart series values are scrambled. Correct
  standard values for the activation chart: tanh(-3)=-1.00, σ(-3)=0.05;
  tanh(-2)=-0.96, σ(-2)=0.12; tanh(-1)=-0.76, σ(-1)=0.27; tanh(0)=0.00, σ(0)=0.50;
  tanh(1)=0.76, σ(1)=0.73; tanh(2)=0.96, σ(2)=0.88; tanh(3)=1.00, σ(3)=0.95.
  Derivative chart: tanh'(0)=1.0, σ'(0)=0.25; both →0 for |x|≳3; tanh' is symmetric,
  σ' is maximally asymmetric. Do not build charts from the parse rows.
- "Node Bias" label near the ReLU figure is consistent with net = Σw·x + b (cf.
  slide 21's b_k notation); no correction needed.
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent agy
web-search; cross-read against `analysis/parse/slide_025.parse.md` and
`analysis/slide_025_final.json` (title "Vanishing and Exploding Gradients"; bullets
"Long Chain of Derivatives", "Exploding Gradients", "Vanishing Gradients"; equations
`f(x) = ReLU = { 0 for x<0, x for x>=0 }`, `f'(x) = { 0 for x<0, 1 for x>=0 }`; two charts
titled "Sigmoid vs Tanh" and the two derivative curves).

Questions asked:
1. Is `f(x) = ReLU = 0 for x<0, x for x≥0` the correct definition?
2. Is `f'(x) = 0 for x<0, 1 for x≥0` the correct derivative (and what happens at 0)?
3. Are the numeric claims `σ′(0) = 0.25` and `tanh′(0) = 1.0` correct, and do the
   saturation/vanishing-gradient claims follow?
4. Does the "long chain of derivatives" framing correctly explain both vanishing AND
   exploding gradients?
5. Are the chart series values in the parse transcript usable as data?

Answers:
- Q1 **CONFIRMED**. Search returns `ReLU(z) = max(0, z)`, range `[0, ∞)`.
- Q2 **CONFIRMED**. Derivative is 0 for `z < 0` and 1 for `z > 0`; undefined exactly at 0
  (implementations pick 0 or 1). Note the certified JSON prints `x>=0` for the 1-branch,
  which is the standard rendering choice and is acceptable.
- Q3 **CONFIRMED**. `σ′(0) = 0.25` is the absolute maximum sigmoid gradient, so each
  sigmoid layer scales the gradient by at most 0.25 and `0.25ⁿ` decays exponentially across
  n layers — the vanishing-gradient mechanism. `tanh′(0) = 1.0` (four times larger than
  sigmoid), still saturating but milder. ReLU's derivative is a constant 1 for `x > 0`, so
  it neither shrinks the signal nor dies on positive inputs.
- Q4 **CONFIRMED**. The backprop gradient is a multiplicative chain `Π(W·g′(z))`: factors
  below 1 ⇒ vanishing; factors consistently above 1 ⇒ exploding. ReLU solves vanishing but
  not exploding (too-large initial weights still explode the chain), which is why gradient
  clipping / He initialization / batch norm are the standard mitigations.
- Q5 **NO**. The parse chart tables are scrambled (e.g. the "Sigmoid" column carries the
  value −1.00 at x=−2, and the derivative table has a "1.0" sigmoid derivative at x=0).
  Recomputed standard values: tanh(−3…3) = −1.00, −0.96, −0.76, 0.00, 0.76, 0.96, 1.00;
  σ(−3…3) = 0.05, 0.12, 0.27, 0.50, 0.73, 0.88, 0.95; tanh′(0)=1.0, σ′(0)=0.25, both →0
  for |x|≳3.

Verdicts per claim:
- ReLU definition — **CONFIRMED**.
- ReLU derivative — **CONFIRMED**.
- σ′(0)=0.25 / tanh′(0)=1.0 / vanishing-gradient mechanism — **CONFIRMED**.
- Exploding-gradient mechanism (chain factors > 1) — **CONFIRMED**.
- "Long Chain of Derivatives" framing for both phenomena — **CONFIRMED**.
- "Dying ReLU" caveat (a unit stuck negative gets zero gradient) — **CONFIRMED**.
- Parse chart series values — **CONFLICT** (scrambled; do not build the charts from the
  parse rows — use the standard values listed above or the frame itself).
- Parse's garbled `f'(x)= 1 for x<0 for x≥0` — **CONFLICT** (OCR artifact; the certified
  JSON's `0 for x<0, 1 for x>=0` is correct).
- "Node Bias" label near the ReLU figure — **CONFIRMED** as consistent with net = Σw·x + b.
- Chart axis tick labels (−10…10, −4…4, and the 0.0–1.0 / −1.00–1.00 scales) — **NOT-VERIFIABLE**
  without the frame; the certified JSON carries them, so take them from there.

New sources found during audit (real URLs, not previously cited):
- GeeksforGeeks, "Vanishing and Exploding Gradients Problems in Deep Learning" —
  https://www.geeksforgeeks.org/deep-learning/vanishing-and-exploding-gradients-problems-in-deep-learning/
  Chain-rule product formulation, sigmoid/tanh saturation, dying ReLU, gradient clipping.
- Oniani, "Exploding and Vanishing Gradients" —
  https://oniani.org/notes/exploding-and-vanishing-gradients/
- Longcode, "Derivatives of Activation Functions" (Nielsen-derived course notes) —
  https://longcode.online/docs/deep-learning-ai-course-notes/neural-networks-and-deep-learning/week-3/derivatives-of-activation-functions/
  ReLU derivative is 1 for x>0; tanh′ max 1.0, sigmoid′ max 0.25.
- Stats StackExchange, "Why is tanh almost always better than sigmoid?" —
  https://stats.stackexchange.com/questions/330559/why-is-tanh-almost-always-better-than-sigmoid-as-an-activation-function
  Zero-centering and the fourfold max-derivative advantage of tanh over sigmoid.
- Data Science StackExchange, "What's the correct reasoning behind solving the vanishing/
  exploding gradient problem?" —
  https://datascience.stackexchange.com/questions/45322/whats-the-correct-reasoning-behind-solving-the-vanishing-exploding-gradient-pro

Audit summary: all conceptual and numeric claims confirmed. Two parse-artifact CONFLICTs
(the derivative OCR line and the scrambled chart tables) — both already documented above and
both must be corrected at build time.
