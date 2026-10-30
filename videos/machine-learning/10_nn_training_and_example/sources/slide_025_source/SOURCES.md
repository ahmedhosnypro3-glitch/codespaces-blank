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
