# Source verification — slide 003

## Claims checked
- Objective form: `1/2 [X^T P X] + q^T X`, with `X` vector size d*1, `P` matrix size d*d, `q^T` vector size 1*d — CONFIRMED — CVXOPT coneprog manual, https://cvxopt.readthedocs.io/en/latest/coneprog.html
  Canonical solver form is `minimize 1/2 x^T P x + q^T x` with `x` (n*1), `P` (n*n, symmetric positive semi-definite), `q` (n*1), hence `q^T` is 1*n. Slide's `d` plays the role of `n`.
- Inequality form: `G X <= h`, with `m` = number of constraints, `X` vector d*1, `G` matrix m*d, `h` vector m*1 — CONFIRMED — CVXOPT coneprog manual, https://cvxopt.readthedocs.io/en/latest/coneprog.html
  Solver form is `Gx <= h` (element-wise), `G` (m_ineq * n), `h` (m_ineq * 1). Slide's `d` plays the role of `n`.
- Equality form: `A X = b`, with `A` matrix m*d, `b` vector m*1 — CONFIRMED — Wikipedia, Quadratic programming, https://en.wikipedia.org/wiki/Quadratic_programming
  Standard form is `Ax = b` with `A` (p * n), `b` (p * 1), `p` = number of equality constraints. The slide reuses `m` for the equality-constraint count instead of the literature's distinct `p` — harmless, it still denotes the count of equality constraints.
- Slide instruction "Put all <=, >= constraints in the form G X <= h" — CONFIRMED as a valid canonical conversion — Berkeley CE 191 lecture notes, https://ecal.studentorg.berkeley.edu/files/ce191/CH02-QuadraticProgramming.pdf
  A `>=` constraint is negated to `-G x <= -h` to enter the solver's `<=` form; the slide's wording is consistent with that canonicalization.
- QP-form context of this SVM lecture (solver-input mapping of the SVM dual) — CONFIRMED (context only; slide shows no dual terms) — Math StackExchange, https://math.stackexchange.com/questions/2922661/how-to-map-quadratic-programming-formulation-to-dual-soft-margin-svm
  SVM dual maps to `1/2 alpha^T P alpha + q^T alpha`, `G alpha <= h`, `A alpha = b` with P = (yy^T) .* K, q = -1, G = [-I; I], h = [0; C*1], A = y^T, b = [0] — consistent with the slide's canonical input shape, but no dual content is on this slide.

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild (no transcript edits licensed):
  - The slide's `d` is the literature's `n` (number of decision variables); `q^T` being 1*d follows from `q` being d*1 — render heights exactly as printed (1*d).
  - Symbol `X` vs literature's lowercase `x`: keep the slide's uppercase `X` in frame text.
  - In this lecture sequence `m` denotes both the inequality and the equality constraint count; sources use `m_ineq` / `p` separately. Do not merge or re-letter the two `m` mentions — the slide prints `m` in both sections.
  - `P` is symmetric positive semi-definite in the solver contract; the slide states only "Matrix of size d*d" — record this only if a rebuild note asks about P's properties; do not add text the slide does not show.
  - `>=` constraints enter solvers negated (`-G X <= -h`); the slide's "Put all <=, >= constraints in the form G X <= h" is an instruction to canonicalize, so the rebuild must not restyle `<=` as `>=`.
