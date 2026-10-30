# Source verification — slide 034

## Claims checked

- Dual objective `L_D(α) = Σ_{i=1}^N α_i − ½ Σ_{j=1}^N Σ_{i=1}^N α_i α_j y_i y_j X_i^T X_j` (linear, unmapped form) — CONFIRMED — Stanford CS229 Lecture Notes III (kernel notes) https://see.stanford.edu/materials/aimlcs229/cs229-notes3.pdf
  Authoritative form: `W(α) = Σ_i α_i − ½ Σ_i Σ_j α_i α_j y_i y_j K(x_i, x_j)`, maximised over `α` under `Σ α_i y_i = 0`, `α_i ≥ 0`. Slide omits the constraints and denotes the objective `L_D`; the algebra shown matches. Standard-dual writeup: https://kuleshov-group.github.io/aml-book/contents/lecture13-svm-dual.html

- Weight vector `W = Σ_{i=1}^N α_i y_i X_i` — CONFIRMED — Stanford CS229 Lecture Notes III https://see.stanford.edu/materials/aimlcs229/cs229-notes3.pdf
  Authoritative form `w = Σ_i α_i y_i x_i` from the KKT stationarity condition; equals `Σ α_i y_i φ(x_i)` once inputs are mapped. Only non-zero-α (support vector) terms survive.

- Bias `b = −½ [ max_{i : y_i = −1} W^T X_i + min_{i : y_i = +1} W^T X_i ]` — CONFIRMED — Stanford CS229 Lecture Notes III https://see.stanford.edu/materials/aimlcs229/cs229-notes3.pdf
  Authoritative form identical to the slide. Derived from the margin conditions `w^T x_i + b = +1` (min over `y_i=+1`) and `w^T x_i + b = −1` (max over `y_i=−1`), averaging the two. A single-support-vector estimate `b = 1 − w^T x_i` (or `−1 − w^T x_i`) is the common code shortcut but is a subset of the same margin condition.

- Classification rule `Class of vector Z ⇒ sign(W^T Z + b)` — CONFIRMED — Sugiyama (NII, Data Mining 2017) lecture https://mahito.info/files/Sugiyama_NII_datamining_2017_10.pdf
  Authoritative form: `f(z) = sign(Σ_i α_i y_i K(x_i, z) + b)` in the kernelized setting, algebraically equal to `sign(W^T Z + b)` since `W^T Z = Σ α_i y_i φ(x_i)^T φ(z) = Σ α_i y_i K(x_i, z)`. Kernelized decision-function derivation also at https://www.datacamp.com/tutorial/kernel-trick

- Mapping step `Instead of using X_i (of dimension d) use φ(X_i) (with higher dimension)`, `X_i^T X_j ⇒ φ(X_i)^T φ(X_j)` — CONFIRMED — CMU 10-701 Kernels lecture slides https://www.cs.cmu.edu/~guestrin/Class/10701-S07/Slides/kernels.pdf
  Authoritative form: `φ : R^d → R^D, D ≫ d`, then the inner product is taken in the mapped space `φ(x_i)^T φ(x_j)`. Matches the slide exactly.

- Kernelization step `Instead of using φ(X_i)^T φ(X_j) use K(X_i^T, X_j)` (K = one of the kernel functions) — CONFIRMED — DataCamp, "Kernel Trick" https://www.datacamp.com/tutorial/kernel-trick
  Authoritative form: `K(x_i, x_j) = φ(x_i)^T φ(x_j)`, e.g. linear `x_i^T x_j`, polynomial `(x_i^T x_j + c)^d`, RBF `exp(−γ‖x_i − x_j‖²)`. The slide's transpose placement `K(X_i^T, X_j)` is a transcription artefact; the intended meaning is `K(X_i, X_j)`. Kernel functions substituting the inner product also at https://mldemystified.com/posts/basics-of-ml/support-vector-machines/svm-kernel-machines/

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild (no source-driven DATA changes; `verbatim_text` stays exactly as recorded):
  - Symbol role: `W` is the feature-space weight vector (equivalently `Σ α_i y_i φ(x_i)`); the slide uses capital `W` where textbooks use lowercase `w`. Keep the slide's `W`.
  - The slide writes the dual objective with the inner product `X_i^T X_j` (the linear/pre-mapping form) and only later substitutes `K` — this is the standard presentation order. Do not merge the two into one line.
  - `L_D` (slide's symbol for the objective) plays the role of textbook `W(α)`; the slide shows no maximisation, no constraints (`Σ α_i y_i = 0`, `α_i ≥ 0`) and no `C` slack parameter. Do not add any — they are not on the slide.
  - Bias formula's max/min subscripts are over the two class sets exactly as the slide prints them; the averaging (the outer `−½`) is intentional, not a typo.
  - Kernel-trick substitution is the only place a kernel `K` enters; the decision rule `sign(W^T Z + b)` keeps the pre-`W` form, which is valid because `W^T Z = Σ α_i y_i K(x_i, z)`.
  - No dataset name, library name, numeric constant, hyperparameter name, or theorem attribution appears on the slide; nothing to reconcile.
