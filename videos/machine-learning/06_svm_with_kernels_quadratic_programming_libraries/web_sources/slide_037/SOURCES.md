# Source verification — slide 037

## Claims checked

- `K(α,b) = [α^T b + 1]^d` (connector strip) — CONFIRMED — scikit-learn kernel-approximation docs, https://scikit-learn.org/stable/modules/kernel_approximation.html
  Standard inhomogeneous polynomial kernel `K(x,z) = (x^T z + c)^d` with `c = 1`; maps to a C(N+d, d)-dim feature space of all monomials of degree ≤ d. No gamma/RBF factor implied.

- Kernelized `ℒ_D(α) = Σ α_i − 1/2 Σ_j Σ_i α_i α_j y_i y_j [X_i^T X_j + 1]^d` (lower panel) — CONFIRMED — Sugiyama (NII) datamining notes, https://mahito.info/files/Sugiyama_NII_datamining_2017_10.pdf; CMU 10315 Lecture 16, https://www.cs.cmu.edu/~aarti/Class/10315_Fall21/lecs/Lecture16_inked.pdf; Wisc CS760 L19, https://pages.cs.wisc.edu/~khodak/cs760fall2025/lecture19-svms.pdf
  The dual depends on data only via inner products, so replacing each with `K(x_i,x_j)` is exactly the kernelization step; max-form with `Σαy = 0`, `α ≥ 0` is standard.

- `W = Σ_{i=1}^{N} α_i y_i X_i` (repeated verbatim in BOTH panels) — CONFIRMED — NUS CS5339 kernel notes, https://www.comp.nus.edu.sg/~scarlett/CS5339_notes/05-Kernel_Notes.pdf; stationarity ∇_w L = 0 confirmed for slide 036 via stats.stackexchange.com/questions/331931
  Unchanged by kernelization: w stays the input-space weight vector; the kernel trick only removes the need to compute it explicitly.

- `b = −1/2 { max_{i,y=−1} [W^T X_i + 1]^d + min_{i,y=+1} [W^T X_i + 1]^d }` (lower panel) — CONFIRMED (as notation) — MIT 6.034 SVM notes, https://web.mit.edu/6.034/wwwbob/svm-notes-long-08.pdf; Cornell CS4780 Notes13, https://www.cs.cornell.edu/courses/cs4780/2022sp/notes/Notes13.pdf
  With the ±1 margin convention `max_{y=−1}(w^T x) + min_{y=+1}(w^T x) = −2b`, so the −½ sum is the margin midpoint. `max` is over y=−1, `min` over y=+1 (do not swap); leading minus required. `[W^T X_i + 1]^d` plays the role of the kernel-evaluated decision value `h(X_i)`.

- `Class of vector Z is sign([W^T Z + 1]^d + b)` (lower panel, peach strip) — CORRECTED (notation only; verbatim text stays exactly as printed) — scikit-learn SVM docs, https://scikit-learn.org/stable/modules/svm.html; Stanford STATS202 Kernels notes, https://web.stanford.edu/class/stats202/notes/Support-vector-machines/Kernels.html
  Authoritative kernelized classifier: `f(z) = sign( Σ_i α_i y_i K(x_i,z) + b ) = sign( Σ_i α_i y_i (x_i^T z + 1)^d + b )`. The slide raises a SUM to the power d; the rule needs the SUM of per-term kernel values. `(Σ_i α_i y_i x_i^T z + 1)^d ≠ Σ_i α_i y_i (x_i^T z + 1)^d` in general. Same defect as slide 036. Record only — do NOT edit the transcript.

- `Class of vector Z ⇒ sign(W^T Z + b)` (upper panel) — CONFIRMED — Cornell CS4780 Notes13 (same URL): w^T x + b = 0 is the boundary, sign() gives the ±1 label. Correct pre-kernelization decision rule.

- Kernel-parameter note (library names) — CONFIRMED — scikit-learn pairwise polynomial_kernel, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.polynomial_kernel.html
  `K(X,Y) = (γ⟨X,Y⟩ + coef0)^degree`; sklearn defaults `degree=3`, `coef0=1`, `gamma=None` → `1/n_features`. The slide's form is `γ=1, coef0=1, degree=d`.

## Overall

- VERDICT: CORRECTED
- Tolerance notes for the rebuild: every equation stays verbatim on the slide — the correction is recorded here only, not a licence to edit the transcript or the parse.
- Symbol roles: `K(α,b)` takes two vector arguments; that `α` is an input vector, NOT the dual multiplier α_i. Render the two meanings distinctly.
- The closing parenthesis of `K(α,b) = [α^T b + 1]^d` renders as a vertical stroke before the superscript d (analysis uncertain_items); keep that visual, intended as `( )^d`.
- Apply the kernel per training point inside the sum, never to the whole projection; keep `max` over y=−1, `min` over y=+1, leading −1/2.
- No gamma/scaling term: `K = [a^T b + 1]^d` exactly. Degree stays symbolic `d` — never substitute a numeric degree (slide 038's example uses d = 2; that is a different slide).
