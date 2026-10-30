# wave-3 raw search log — slide_023

Date: 2026-10-30 · Agent: src-021-024

## Tool note

`agy -p "<query>"` was attempted first and returned HTTP 429 `RESOURCE_EXHAUSTED` (quota
exhausted, reset ~154h). Searches were therefore executed through the **agy MCP web-search tool**
(same Google grounding backend; grounding redirect URLs resolved to real page URLs).

## Queries run (4)

1. `Heaviside step function unipolar unit step derivative 0 for x not equal 0, undefined at x=0,
   why derivative does not exist at zero Dirac delta distribution`
   → https://en.wikipedia.org/wiki/Heaviside_step_function,
   https://math.fel.cvut.cz/cz/mt/txtb/4/txe3ba4l.htm,
   https://math.stackexchange.com/questions/238193/on-the-derivative-of-a-heaviside-step-function-being-proportional-to-the-dirac-d
2. `sign function bipolar step function 2*Heaviside(x)-1 derivative zero except undefined at zero
   neural network activation`
   → https://ai.stackexchange.com/questions/28395/an-explanation-involving-the-sign-activation-its-affect-on-the-loss-function-a,
   https://longcode.online/docs/deep-learning-ai-course-notes/neural-networks-and-deep-learning/week-3/derivatives-of-activation-functions/
3. `tanh derivative d/dx tanh(x) = 1 - tanh^2(x) = sech^2(x), sigmoid derivative sigma'(x) =
   sigma(x)(1-sigma(x)) proof`
   → https://derivative-calculator.org/proofs/tanh/,
   https://www.cuemath.com/calculus/derivative-of-hyperbolic-functions/,
   https://math.stackexchange.com/questions/78575/derivative-of-sigmoid-function-sigma-x-frac11e-x
4. `derivative of arctan x is 1/(1+x^2) tangent inverse function derivative formula`
   → https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/37028101f134cc6e0e41572fdc6735d8_MIT18_01SCF10_Ses15b.pdf,
   https://www.geeksforgeeks.org/maths/derivative-of-arctan/

All URLs above were returned by the search tool; none were constructed by hand.
