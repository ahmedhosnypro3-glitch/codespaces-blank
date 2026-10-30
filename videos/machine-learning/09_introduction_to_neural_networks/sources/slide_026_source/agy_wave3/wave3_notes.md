# agy wave-3 evidence notes — slide_026 (Sigmoid vs Tanh)

Date: 2026-10-30. Agent: src-025-028.
Transport note: `agy -p` CLI is per-user quota-blocked (HTTP 429, "resets in
~154h"; the attempt is logged in `cli_attempt_01.txt`). All wave-3 searches
for this slide ran through the agy web-search MCP (same Google grounding
service); URLs below are exactly those returned, none invented.

## Queries run (3)
1. Verify sigmoid sigma(x)=1/(1+e^-x) range (0,1), derivative sigma(x)(1-sigma(x))
   max 0.25 at x=0; tanh range (-1,1), derivative 1-tanh^2(x) max 1 at x=0;
   identity tanh(x) = 2*sigma(2x) - 1.
2. Numerical values of sigmoid/tanh and their derivatives at x = -4,-2,0,2,4;
   why tanh is preferred in hidden layers (zero-centered, faster convergence).
3. Sigmoid vs tanh comparison: range, slope/rate-of-change, saturation and
   vanishing gradient, hidden vs output layer usage.

## Findings (confirm the slide's verbatim text)
- Slide claim [1]: sigmoid range fixed 0..1, tanh range fixed -1..1. CONFIRMED
  (ranges (0,1) and (-1,1)).
- Slide claim [2]: sigmoid has slower rate of change than tanh -> smaller
  derivative for a given input near 0. CONFIRMED: sigma'(0) = 0.25 (max),
  tanh'(0) = 1.0 (max); tanh max slope is 4x sigmoid's.
- Frame equations CONFIRMED: f(x)=Sigmoid(x)=1/(1+e^-x) => f'(x)=f(x)(1-f(x));
  at x=0 f(0)=0.5, f'(0)=0.25. f(x)=tanh(x)=sinh x/cosh x => f'(x)=1-f(x)^2;
  at x=0 f(0)=0, f'(0)=1. tanh(x) = 2*sigma(2x)-1 verified algebraically.
- Canonical value table (for re-plotting the two charts; the doc-parse tables in
  wave-1 had OCR variance):
  | x | sigma | sigma' | tanh | tanh' |
  |---|-------|--------|------|-------|
  | -4 | 0.0180 | 0.0177 | -0.9993 | 0.0013 |
  | -2 | 0.1192 | 0.1050 | -0.9640 | 0.0707 |
  |  0 | 0.5000 | 0.2500 |  0.0000 | 1.0000 |
  |  2 | 0.8808 | 0.1050 |  0.9640 | 0.0707 |
  |  4 | 0.9820 | 0.0177 |  0.9993 | 0.0013 |
  This matches the frame's right-panel annotations (derivative peaks 1.0 vs 0.25).
- Zero-centeredness: sigmoid outputs strictly positive -> all-same-sign weight
  gradients (zigzagging, LeCun Efficient BackProp); tanh zero-centered ->
  faster convergence. Both saturate (vanishing gradient) far from 0; sigmoid
  shrinks gradients by >=75% per layer (max 0.25).

## Sources (URLs returned by the agy web-search MCP)
- https://www.baeldung.com/cs/sigmoid-vs-tanh-functions
- https://longcode.online/docs/deep-learning-ai-course-notes/neural-networks-and-deep-learning/week-3/derivatives-of-activation-functions/
- https://awni.github.io/jiro/practice/2017/01/12/tanh.html
- https://medium.com/@cloudtwodata/know-about-the-activation-function-sigmoid-cloud2data-f27a5eca3538
- https://www.kaggle.com/discussions/getting-started/429326
- https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/tanh-activation
- https://stats.stackexchange.com/questions/330559/why-is-tanh-almost-always-better-than-sigmoid-as-an-activation-function
- https://datahacker.rs/activation-functions-and-derivatives/
- https://www.datacamp.com/tutorial/tanh-function
- https://eureka.patsnap.com/article/why-use-relu-instead-of-sigmoid-or-tanh
- https://medium.com/ai-enthusiast/mastering-tanh-a-deep-dive-into-balanced-activation-for-machine-learning-4734ec147dd9
- https://www.geeksforgeeks.org/deep-learning/tanh-vs-sigmoid-vs-relu/
- https://www.cs-visualizations.com/blog/activation-functions-compared
- https://medium.com/data-science/intuitions-behind-different-activation-functions-in-deep-learning-a2b1c8d044a
- https://towardsdatascience.com/activation-functions-in-neural-networks-how-to-choose-the-right-one-cb20414c04e5/
- https://community.deeplearning.ai/t/better-activation-functions-tanh-sigmoid/224869
