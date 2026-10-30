# Source verification — slide 006
## Claims checked
- "x₁ ≤ z₁, x₂ ≤ z₂, x₃ ≤ z₃ ⟹ [1 0 0; 0 1 0; 0 0 1][x₁; x₂; x₃] ≤ [z₁; z₂; z₃]" (identity 3×3, Box 1) — CONFIRMED — cvxopt QP standard form https://cvxopt.org/examples/tutorial/qp.html
  QP solvers take constraints as Gx ≤ h evaluated component-wise; the identity row selects xᵢ with RHS zᵢ.
- "x₁ ≥ z₁, x₂ ≥ z₂, x₃ ≥ z₃ ⟹ [−1 0 0; 0 −1 0; 0 0 −1] x ≤ [−z₁; −z₂; −z₃]" (Box 2, 'Greater-than converted') — CONFIRMED — cvxopt QP docs https://media.readthedocs.org/pdf/cvxopt/dev/cvxopt.pdf ; inequality rules https://www.mathcentre.ac.uk/resources/uploaded/mc-bus-manipinequ-2009-1.pdf
  Authoritative rule: a lower bound xᵢ ≥ zᵢ is rewritten by multiplying both sides by −1, giving −xᵢ ≤ −zᵢ (symbol flips ≥→≤).
- "y₁ ≤ x₁ ≤ z₁, … ⟹ [−1 0 0; 0 −1 0; 0 0 −1; 1 0 0; 0 1 0; 0 0 1] x ≤ [−y₁; −y₂; −y₃; z₁; z₂; z₃]" (Box 3, 6×3, '6 constraints, 3 variables') — CONFIRMED — cvxopt QP docs https://cvxopt.org/examples/tutorial/qp.html ; SVM-dual mapping https://math.stackexchange.com/questions/2922661/how-to-map-quadratic-programming-formulation-to-dual-soft-margin-svm
  Box constraints are stacked explicitly as G = [−I; I] with h = [lower-bounds; upper-bounds]; with 3 variables this is exactly 6×3, i.e. 6 rows of constraints over 3 variables.
- Callouts "Gx ≤ h" (Boxes 1 and 3) as the standard form for QP/SVM libraries — CONFIRMED — cvxopt QP docs https://media.readthedocs.org/pdf/cvxopt/dev/cvxopt.pdf ; SJSU SVM QP lecture https://www.sjsu.edu/faculty/guangliang.chen/Math251F18/lec6svm.pdf
  Standard QP: minimize ½xᵗPx + qᵗx s.t. Gx ≤ h, Ax = b; the same Gx ≤ h form hosts the SVM dual constraints (e.g. G = [−I; I], h = [0; C]).
## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: Gx ≤ h is component-wise (one scalar inequality per row). Keep the ≥→≤ conversion sign convention exactly
  as the slide shows: multiply both sides by −1 and flip the symbol (never divide or reorder rows). Preserve Box 3's row order lower-bounds-first
  (the −I/−y block above the I/z block) — that is the cvxopt/SVM-dual convention. The slide shows no Hessian term, so the P-vs-H naming
  difference across libraries is irrelevant here. verbatim_text stays exactly as the slide prints it; no source required any edit.
