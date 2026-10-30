# Source verification — slide 013

## Claims checked
- Objective "Minimize: [ +1 α₁²+2α₁α₂−5.5α₁α₃−6α₁α₄ … +40α₄² ] − [α₁+α₂+α₃+α₄]" (expanded quadratic) — CONFIRMED — SJSU Math251F SVM lecture notes (lec6svm.pdf) https://www.sjsu.edu/faculty/guangliang.chen/Math251F18/lec6svm.pdf ; CVXOPT QP tutorial https://cvxopt.org/examples/tutorial/qp.html
  Authoritative dual is min ½αᵀPα − 1ᵀα with P = YKY, Y = diag(y). The printed bracket is ½·αᵀPα: its entries are exactly ½Pᵢⱼ for P = [[2,4,−11,−12],[4,8,−22,−24],[−11,−22,65,72],[−12,−24,72,80]] — the same matrix slide 012 prints outright. Offline reproduction: with slide 011's own training set X = [(1,1),(2,2),(4,7),(4,8)], y = [+1,+1,−1,−1], C = 1, outer(y,y)·(XXᵀ) reproduces all 16 entries, so the numbers need no external source.
- "Subject to: ∑αᵢyᵢ = 0 → α₁+α₂−α₃−α₄ = 0" — CONFIRMED — Berkeley EECS281B lec6 https://people.eecs.berkeley.edu/~jordan/courses/281B-spring04/lectures/lec6.pdf
  Standard dual equality (from ∂L/∂b = 0); it also implies y = [+1,+1,−1,−1].
- "α₁≤1, α₂≤1, α₃≤1, α₄≤1" and "αᵢ≥0" — CONFIRMED — CVXOPT QP tutorial (same URL)
  Soft-margin dual box is 0 ≤ αᵢ ≤ C; slide 011 states "Use C = 1", so the printed bound 1 is C.
- "Constraint simplification: αᵢ≥0, αᵢ≤1 ⇒ −αᵢ≤0, αᵢ≤1" — CONFIRMED — qpsolvers QP form https://qpsolvers.github.io/qpsolvers/quadratic-programming.html ; CVXPY QP example https://www.cvxpy.org/examples/basic/quadratic_program.html
  The −I/I stacking of box bounds is the standard conversion; the arrow shows αᵢ≥0 → −αᵢ≤0 while αᵢ≤1 stays as is.
- "Gα ≤ h form: G = [−I; I] (8×4), h = [0,0,0,0,1,1,1,1]ᵀ" — CONFIRMED — CVXOPT QP tutorial (same URL)
  Authoritative form for 0 ≤ α ≤ C is G = [[−I],[I]], h = [[0],[C·1]]; with n = 4, C = 1 this is exactly 8×4 with h = [0;1]ᵀ.
- "Aα = b form: A = [1 1 −1 −1]₁×₄, b = [0]₁×₁" — CONFIRMED — Berkeley lec6 (same URL)
  Standard mapping of yᵀα = 0: A = yᵀ as a 1×n row vector, b = 0 scalar.
- "Solution: α₁=0.0690, α₂=0.0690, α₃=0.0690, α₄=0.000008" — CORRECTED — no web source can settle a dataset-specific value; corrected by exact recomputation of the QP the slide itself prints
  The printed set violates the slide's own constraint α₁+α₂−α₃−α₄ = 0 (0.0690+0.0690−0.0690−0.000008 = 0.068992 ≠ 0), so it cannot be the optimum. Solving the printed problem (P above, q = −1, G = [−I;I], h = [0;1], Aα = b): unique minimiser α* = (0, 2/29, 2/29, 0) ≈ (0, 0.0690, 0.0690, 0), objective −2/29 ≈ −0.0690. Reached independently by SLSQP from 8 starts, by sklearn SVC(kernel="linear", C=1) (α₂ = α₃ = 0.0689655, α₁ = α₄ = 0), and verified by a KKT certificate (multipliers ≥ 0, interior residuals zero). Frame text stays verbatim; the data error is recorded, not edited.

## Overall
- VERDICT: CORRECTED
- Tolerance notes for the rebuild:
  - All six formulation claims are CONFIRMED by the cited web sources; the one CORRECTED item is a numeric solution value, settled by exact recomputation (the training set is not shown on the slide, so no web source can decide it).
  - Sign convention: objective is ½αᵀPα − 1ᵀα = ½αᵀPα + qᵀα with qᵀ = −[1,1,1,1]ᵀ (CVXOPT convention). The slide's "− [α₁+α₂+α₃+α₄]" already carries that minus sign; do not add a second one.
  - The printed bracket is ½·αᵀPα: diagonal entries are ½Pᵢᵢ and the printed off-diagonal pairs (e.g. +2α₁α₂ with +2α₂α₁) sum to Pᵢⱼ. Do not halve the coefficients again in the rebuild.
  - G rows 1–4 are the −I block (−α ≤ 0); rows 5–8 the I block (α ≤ 1). G is 8×4, h is 8×1, and h's lower half is all 1s (C = 1).
  - A = [1,1,−1,−1] is a 1×4 row, b = [0] is 1×1; keep both dimensions (the slide-012 worker noted the same yᵀ/b = 0 mapping).
  - Solution box: the printed α₁ = 0.0690 and α₄ = 0.000008 contradict the slide's own printed constraint; the QP's unique optimum has α₁ = α₄ = 0 and α₂ = α₃ = 0.0690. Reproduce the slide's text verbatim and record the correction here — no silent fix.
