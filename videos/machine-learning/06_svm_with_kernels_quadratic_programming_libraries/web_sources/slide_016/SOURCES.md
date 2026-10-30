# Source verification — slide 016

## Claims checked

- Feature mapping `x → (x, x²)` written on the slide as `Mapping x → φ(x)` with formula `x → (x, x²)` is the standard non-linear feature map that lifts a 1-D input into a 2-D feature space so that data not linearly separable in the original space becomes linearly separable there — CONFIRMED — Western University CS434a/541a Lecture 11 (Kernels) https://www.csd.uwo.ca/~oveksler/Courses/CS434a_541a/Lecture11.pdf
  Authoritative form: `φ(x) = [x, x²]ᵀ` (column vector with first coordinate `x`, second coordinate `x²`); identical in content to the slide's `x → (x, x²)`. Same mapping is presented as the canonical kernel-trick introduction example at https://www.geeksforgeeks.org/machine-learning/kernel-trick-in-support-vector-classification/.

- Callout claim `Data is linearly separable In the new representation` — CONFIRMED — Western University CS434a/541a Lecture 11 (Kernels) https://www.csd.uwo.ca/~oveksler/Courses/CS434a_541a/Lecture11.pdf
  Under `φ(x) = [x, x²]ᵀ` all points lie on the parabola `z₂ = z₁²` in the 2-D feature plane; the near-origin class sits low and the outer classes sit high, so a straight (horizontal) linear decision boundary separates them in the mapped space. Also confirmed at https://slds-lmu.github.io/i2ml/chapters/17_nonlinear_svm/.

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild (no source-driven DATA changes; `verbatim_text` stays exactly as recorded, including the callout's inline `In` capitalisation):
  - Symbol role: `φ(x) = (x, x²)` — the second coordinate is the quadratic feature `x²`. The slide carries NO coefficient, scale, or gamma factor on the second coordinate and none is implied; do not add one in the rebuild.
  - Sign convention: `x²` is always non-negative, so every mapped point sits on the upper parabola arm pair. The slide's red `x²` arrow at the top of the plot card is consistent with that direction.
  - The `Linear Decision Boundary` legend is consistent with the standard treatment: the boundary is linear in the mapped (new) representation and corresponds to a non-linear boundary in the original space. The blue horizontal line in the plot card matches the horizontal-separator form.
  - The slide applies the mapping to a single feature `x` (1-D input), matching the canonical example. No dataset name, library name, hyperparameter name, numeric constant, or theorem attribution appears on the slide, so no numeric or attribution drift is possible.
  - No equations or numbers on the slide were contradicted by the sources; nothing in the transcript requires correction.
