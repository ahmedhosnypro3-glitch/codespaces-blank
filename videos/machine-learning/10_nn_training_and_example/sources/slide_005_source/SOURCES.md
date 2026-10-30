# Slide 005 — Revision: Derivative of the Sigmoid Function

Frame facts (from `analysis/parse/slide_005.parse.md`, data only): `O_j = f(Net_j) = 1/(1+e^(−Net_j))`,
then a quotient/chain-rule derivation ending at `f'(Net_j) = O_j(1−O_j)`. Method: agy web search
(best-effort), proof steps verified against independent calculus derivations.

## Sources

- Story of Mathematics — "Derivative of Sigmoid Function" (https://www.storyofmathematics.com/derivative-of-sigmoid-function/) — confirms σ(x)=1/(1+e^(−x)) and σ'(x)=σ(x)(1−σ(x)).
- Hausetutorials — "Deriving the Sigmoid Derivative" (https://hausetutorials.netlify.app/posts/2019-12-01-neural-networks-deriving-the-sigmoid-derivative/) — confirms the quotient-rule route via e^(−x)/(1+e^(−x))² then the 1−f(x) split, as shown on the slide.
- Sebastian Raschka — "Logistic sigmoid derivative" (https://www.sebastianraschka.com/faq/docs/logistic-sigmoid-derivative.html) — confirms the algebraic rearrangement f(x)·(1−f(x)) step by step.

## Corrections / notes

- Final result `f'(Net_j) = O_j(1−O_j)` — CONFIRMED verbatim by all three sources; it is the identity that makes backpropagation's δ rule possible.
- The intermediate stacked-fraction lines (e.g. `1/(1+e^{−Net_j})(1+e^{−Net_j})`) are the slide's own working; the standard presentation reaches the same `e^{−x}/(1+e^{−x})²` form documented above — no correction, the frame wins for recreation.
- The slide writes `O_j = f(Net_j) = 1/(1+e^{−Net_i})` on its second line — parse artifact of the stacked fraction; standard notation indexes `Net_j`.
- No course-authored elements: this is a standard textbook derivation with no independent figure.
