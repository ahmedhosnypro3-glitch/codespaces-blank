# Source verification — slide 009

## Claims checked

- Objective "Minimize 0.5x^2 + 3x + 4y" over the stated feasible region — CONFIRMED —
  independent KKT derivation of the identical problem returns the same optimum — https://acme.byu.edu/0000017a-1bb8-db63-a97e-7bfa0bdb0000/vol2lab14-pdf
- Matrix form "Minimize 1/2 [x^T P x] + q^T x" — CONFIRMED — matches the standard convex-QP
  form minimize 1/2 x^T P x + q^T x s.t. Gx <= h — https://en.wikipedia.org/wiki/Quadratic_programming
- P = [[1,0],[0,0]], q = (3,4) — CONFIRMED — 1/2 x^T P x = 0.5x^2 and q^T x = 3x+4y reproduce the
  slide's original function; P is symmetric and equals the objective Hessian (leading factor is 1/2) —
  https://cvxopt.readthedocs.io/en/latest/coneprog.html
- "Subject to Gx <= h" with G = [[-1,0],[0,-1],[-1,-3],[2,5],[3,4]], h = (0,0,-15,100,80) — CONFIRMED —
  G is m x n (5x2), h is m x 1 (5x1); the two ">=" constraints are sign-flipped into "<=" form
  (x>=0 -> -x<=0, x+3y>=15 -> -x-3y<=-15) — https://cvxopt.readthedocs.io/en/latest/coneprog.html
- Constraint checks x+3y=15>=15, 2x+5y=25<=100, 3x+4y=20<=80 all (Satisfied) — CONFIRMED — all three
  hold at the reported point — https://acme.byu.edu/0000017a-1bb8-db63-a97e-7bfa0bdb0000/vol2lab14-pdf
- "Optimal Point: x = 0, y = 5" and "Minimum Value: 0.5x^2+3x+4y = 20" — CONFIRMED — reproduced three
  ways: scipy.optimize.minimize SLSQP (x~0, y=5, f=20.0), grid sweep on the active face x+3y=15
  (minimum 20.0 at x=0), and the independent KKT derivation —
  https://acme.byu.edu/0000017a-1bb8-db63-a97e-7bfa0bdb0000/vol2lab14-pdf

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: keep every ">=" constraint in its sign-flipped "<=" G/h form
  (negated coefficients and negated RHS); P equals the objective Hessian because the quadratic
  term carries the leading 1/2, so do not halve it again; the QP is convex, not strictly convex
  (P is PSD but not PD); optimum x=0, y=5, f=20 are exact integers — no rounding.
- Note: the doc-parse transcript renders the third G row as "-%" — an OCR glyph artifact; the row is
  (-1, -3), per the sign-flip of x+3y>=15. verbatim_text unchanged (data-only correction recorded here).
