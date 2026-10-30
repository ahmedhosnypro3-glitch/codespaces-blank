# Source verification — slide 038

## Claims checked
- `Minimize L_D(α) = 1/2 ∑_j ∑_i α_i α_j y_i y_j [X_i^T X_j + 1]^2 - ∑_i α_i` (soft-margin SVM dual QP, minimization form) — CONFIRMED — CMU 10701 Lecture 6, https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/Lecture6_inked.pdf
  Authoritative form: min 1/2 ΣΣ α_i α_j y_i y_j K(x_i,x_j) - Σ α_i. The slide omitting the explicit 1/n=∑-range labels is notation only; structure matches exactly.
- `0 ≤ α1 ≤ C, …, 0 ≤ α4 ≤ C` plus `α_i ≥ 0` and `α_i ≤ 1` with `Use C=1` (box constraints, C = slack penalty / cost parameter) — CONFIRMED — CMU 10701 Lecture 6, https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/Lecture6_inked.pdf
  C bounds α_i from above in the dual; 0 ≤ α_i ≤ C is the standard box. C=1 is the LIBSVM/scikit-learn SVC default (blog.paperspace.com/multi-class-classification-using-libsvm, https://blog.paperspace.com/multi-class-classification-using-libsvm/).
- `∑ α_i y_i = 0` (dual equality constraint) — CONFIRMED — CMU 10701 Lecture 6, https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/Lecture6_inked.pdf
- `[X_i^T X_j + 1]^2` as the kernel (degree-2 polynomial kernel) — CONFIRMED — Columbia COMS 4771 kernels handout, http://www.cs.columbia.edu/~djhsu/coms4771-f25/lectures/kern-handout.pdf
  K(x,z) = (x^T z + 1)^2 is the homogeneous-plus-constant degree-2 polynomial kernel; no gamma/RBF or RBF-like term is implied.
- `Minimize:` objective written as 1/2 α^T Q α - 1^T α (QP solver form) — CONFIRMED — Stanford CS229 problem set 2 solution, https://see.stanford.edu/materials/aimlcs229/ps2_solution.pdf
  This is the same dual negated from the maximize form max(1^T α - 1/2 α^T Q α) that textbooks/CS229 use; minimizing L_D = -W is the QP-solver convention and yields identical α*.
- `α_i ≤ 1` under `Use C=1` (upper bound equals the stated C) — CONFIRMED — derived from the two claims above; consistent, no external source needed.

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild:
  • Keep `Minimize` (QP-solver convention). Textbook and CS229-style sources state the dual as a maximization with the sign flipped; same optimum α*, so this is a notation difference, not a slide error. Do not flip the slide's sign.
  • `[X_i^T X_j + 1]^2` is exactly the degree-2 polynomial kernel; render literally with the `[ ]^2` bracket — no gamma, no RBF form.
  • `0 ≤ α_i ≤ C` with C=1 bounds each α_i at 1; the slide's separate `α_i ≥ 0` and `α_i ≤ 1` lines are that box split into two inequalities — reproduce both.
  • `∑ α_i y_i = 0` is the equality constraint; the slide expands it to `α1+α2-α3-α4=0`, implying labels y = (+1,+1,-1,-1) for T1–T4. Keep that expansion verbatim; only record that it assumes the +/- labelling.
  • N=4 training points (α1…α4) matches the four 4×4 matrix rows and the T1–T4 / X1–X4 row labels.
  • The bracketed 4×4 coefficient matrix is the Q matrix of 1/2 α^T Q α (entries ~4.5…3280.5, symmetric); no source changes those numbers — they are slide-internal data.
  • Data credit: vision analysis (`analysis/slide_038_final.json`) + doc-parse transcript; upper table's numeric cell values were never captured, so treat them as `[?]` rather than invented.
