# Source verification — slide 036

## Claims checked

- `ℒ_D(α) = Σ_{i=1}^{N} α_i − 1/2 Σ_{j=1}^{N} Σ_{i=1}^{N} α_i α_j y_i y_j (X_i^T X_j)` (upper panel) — CONFIRMED — Kuleshov AML book, lecture 13 https://kuleshov-group.github.io/aml-book/contents/lecture13-svm-dual.html — obtained by substituting the stationarity result w = Σ α_i y_i x_i into the hard-margin primal Lagrangian; α_i ≥ 0, Σ α_i y_i = 0.
- `W = Σ_{i=1}^{N} α_i y_i X_i` (upper panel) — CONFIRMED — same source — stationarity ∇_w ℒ = 0 gives exactly w = Σ_i α_i y_i x_i.
- `b = −1/2 { max_{i,y=−1}(W^T X_i) + min_{i,y=+1}(W^T X_i) }` (upper panel) — CONFIRMED — stats.stackexchange.com/questions/451868 — averaging b = 1 − min_pos(w^T x) and b = −1 − max_neg(w^T x) collapses to exactly −1/2(max_neg + min_pos) under the ±1 margin convention.
- `Class of vector Z ⇒ sign(W^T Z + b)` (upper panel) — CONFIRMED — scikit-learn SVM docs https://scikit-learn.org/stable/modules/svm.html — sign of the decision value gives the class.
- Kernelizing the dual: `(X_i^T X_j)` → `(X_i^T X_j)^2` in the lower-panel objective — CONFIRMED — same AML book — the dual depends on the training data only through the inner products x_i^T x_j, so replacing each by K(x_i, x_j) is the kernelization step.
- `K(a,b) = [a^T b]^2` (mid-slide "Kernelize using" strip; doc-parse reads `K(a,b)=[aTb)2`, the `)` being an OCR of `]`) — CONFIRMED, with a DATA transcription note — URI CSC581 kernel notes https://homepage.cs.uri.edu/faculty/hamel/courses/2014/spring2014/csc581/lecture-notes/15-kernels.pdf — this is the degree-2 HOMOGENEOUS polynomial kernel (c = 0), 2-D → 3-D via φ(x) = (x1², √2 x1x2, x2²). Note: both analysis/slide_036_raw.json and analysis/slide_036_final.json garbled this string as `K(α,b) = α^T b^2`; the frame shows the [a^T b]^2 form. DATA note only — verbatim_text and the frame are unchanged.
- Kernelized `b = −1/2 { max_{i,y=−1} [W^T X_i]^2 + min_{i,y=+1} [W^T X_i]^2 }` (lower panel) — CORRECTED (notation; transcript stays verbatim) — the authoritative kernelized bias uses w^T φ(x_s) = Σ_i α_i y_i K(x_i, x_s), giving b = y_s − Σ_i α_i y_i (x_i^T x_s)² (stats.stackexchange.com/questions/362046). The slide's `[W^T X]²` = (Σ_i α_i y_i x_i^T X)² squares a SUM; the kernel rule needs the SUM of squares Σ_i α_i y_i (x_i^T X)². The two are not equal in general.
- Kernelized `Class of vector Z is sign([W^T Z]^2 + b)` (lower panel) — CORRECTED (notation; transcript stays verbatim) — the authoritative kernelized classifier is sign( Σ_i α_i y_i K(x_i, z) + b ) = sign( Σ_i α_i y_i (x_i^T z)² + b ) (scikit-learn SVM docs; kernel-SVM notes). `[W^T Z]²` squares the whole projection Σ_i α_i y_i x_i^T Z instead of summing per-term squares.
- Lower panel repeats `W = Σ_{i=1}^{N} α_i y_i X_i` unchanged — CONFIRMED as the dual/primal relation, with a rebuild note — in a kernelized model w lives in feature space as Σ_i α_i y_i φ(x_i) and is never formed explicitly; only α, y and K(x_i, x_j) are computable (scikit-learn SVM docs).

## Overall

- VERDICT: CORRECTED
- Tolerance notes for the rebuild: every equation stays verbatim on the slide — the two corrections above are recorded here only, not a licence to edit the transcript.
- Symbol roles: `K(a,b) = [a^T b]^2` is the degree-2 homogeneous polynomial kernel (c = 0); the 6-D map φ(x) = (x1², x2², √2x1x2, √2x1, √2x2, 1) belongs to the INHOMOGENEOUS `[a^T b + 1]^2` — do not mix the two when recreating.
- Squaring convention: in the lower panel the square belongs INSIDE the sum, per term (Σ_i α_i y_i (x_i^T ·)²); the slide's brackets square the whole projection — treat as notation tolerance, not a data conflict.
