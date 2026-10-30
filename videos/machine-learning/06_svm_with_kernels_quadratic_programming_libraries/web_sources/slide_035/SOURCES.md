# Source verification — slide 035
## Claims checked
- "L_D(α) = Σ_{i=1}^N α_i − ½ Σ_j Σ_i α_i α_j y_i y_j X_i^T X_j" (upper + lower band) — CONFIRMED — CMU 10-701 Lecture 6 https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/Lecture6_inked.pdf
  Exactly the hard-margin (linearly-separable) SVM dual objective; the leading source derivation gives the same term-for-term form, and the ½ factor multiplies the double sum only. No C (soft-margin/box constraint) is shown — correct for the hard-margin case, so do not add C when rebuilding.
- "W = Σ_{i=1}^N α_i y_i X_i" — CONFIRMED — CMU 10-701 Lecture 6 (same URL)
  The stationarity condition ∇_w L = 0 gives W = Σ α_i y_i x_i. Slide's uppercase W/X and N-indexed sum are notation, not a different quantity.
- "b = −½ [max_{i:y_i=−1} W^T X_i + min_{i:y_i=+1} W^T X_i]" — CONFIRMED — MIT 6.034 SVM Notes https://web.mit.edu/6.034/wwwbob/svm-notes-long-08.pdf
  Identical formula; it is the exact midpoint between the closest negative support vector (−1 − b) and the closest positive one (+1 − b). Confirmed independently by StackOverflow calc-margin-and-bias https://stackoverflow.com/questions/10885322/calculating-margin-and-bias-for-svms — max is over y_i = −1, min over y_i = +1, signs as the slide shows.
- "Class of vector Z ⇒ sign(W^T Z + b)" — CONFIRMED — GeeksforGeeks Dual SVM https://www.geeksforgeeks.org/machine-learning/dual-support-vector-machine/
  The classifier is f(x) = sign(w^T x + b) on labels {−1, +1}; the slide's arrow form is the same decision rule. Cornell CS4780 SVM-duality notes agree: https://www.cs.cornell.edu/courses/cs4780/2011fa/lecture/07-svm_duality.pdf
- "X_i^T X_j ⇒ φ(X_i)^T φ(X_j)" (Mapping row) — CONFIRMED — Wikipedia Kernel Method https://en.wikipedia.org/wiki/Kernel_method
  Mapping = the explicit feature map φ to a higher-dimensional space; the vector space of the dual then holds φ(X_i).
- "use K(X_i^T , X_j) (Where K is one of kernel functions)" (Kernelization row) — CONFIRMED — Wikipedia Kernel Method https://en.wikipedia.org/wiki/Kernel_method
  A kernel is precisely K(x_i, x_j) = φ(x_i)^T φ(x_j), and the kernel trick substitutes it wherever data appears as an inner product, which is exactly what the two green ovals mark in the lower band.
## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: (1) y ∈ {−1, +1} and b is the margin-midpoint, so the visual result must have the hyperplane centred between the two margin lines. (2) The slide's first kernel argument is written K(X_i^T, X_j) — a transpose artifact of X_i being laid out as a row; render it as K(X_i , X_j) in Professional Format with X_i and X_j as arguments. Keep frame text verbatim ("(with higher dimension )" keeps its trailing space, "K(X_i^T , X_j)" keeps the stray transpose and spacing). (3) The lower band repeats W and b unchanged and circles only the W^T X_i terms — in the strictly kernelized form W is never built explicitly, so treat the ovals as "these inner products get kernelized", not as an error to fix. (4) No soft-margin C and no slack variables anywhere on the slide; do not add them. (5) Render φ as a single serif glyph (phi), not as text "phi", per the Professional-Format rule.
