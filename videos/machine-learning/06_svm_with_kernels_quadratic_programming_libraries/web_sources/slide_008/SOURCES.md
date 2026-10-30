# Source verification — slide 008

## Claims checked
- Standard QP form: "minimize ½[xᵀPx] + qᵀx subject to Gx ≤ h" — CONFIRMED — CVXOPT solvers.qp documentation, https://cvxopt.org/examples/tutorial/qp.html
  The full canonical form is min ½xᵀPx + qᵀx s.t. Gx ⪯ h, Ax = b. The slide omits
  the Ax = b equality row (none apply here); Gx ⪯ h is componentwise.
- Worked example coefficients: "Minimize 0.5x² + 3x + 4y" with x ≥ 0, y ≥ 0,
  x + 3y ≥ 15, 2x + 5y ≤ 100, 3x + 4y ≤ 80 — CONFIRMED (coefficients/inequality
  directions as written) — solved numerically (scipy SLSQP, multi-start) — result
  x* = (0, 5), f* = 20. Standard-form mapping: P = [[1,0],[0,0]] (PSD), q = [3,4].
  Caveat for any restated solution: the KKT optimum **without** the x ≥ 0, y ≥ 0 rows is
  x* = (−5/3, 50/9) ≈ (−1.667, 5.556), f* ≈ 18.611 — that point violates x ≥ 0 and is
  NOT the slide's problem. Do not transcribe it.
- Trailing "+" in "Minimize 0.5x² + 3x + 4y +" — CORRECTED — no objective cross terms
  or missing funded terms exist in the problem; the expression is exactly
  0.5x² + 3x + 4y (P is diagonal, q = [3,4]). The slide's "+" is a truncation artifact,
  kept in verbatim_text per protocol.
- "½[xᵀPx] + qᵀx" symbol roles: x (bold variable), P, q, G, h — CONFIRMED —
  same documentation convention.

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: the slide's leading "0.5" and the standard form's
  "½" are the same factor — keep ½ stacked as a fraction on the equation side.
  Gx ⪯ h encodes all five inequalities componentwise; the two ≤ rows and the three
  mixed rows need no sign change in a rebuild, only convention choice. No value
  rounding beyond x* = (0, 5) / f* = 20, recorded as data-only and not added to the slide.
