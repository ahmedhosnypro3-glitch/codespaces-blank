# Slide 013 — Constraint Transformation to Gx ≤ h, Ax = b — Source Research

## Core References

1. **Standard QP Standard Form** (Boyd & Vandenberghe, Convex Optimization)
   - Inequality constraints: Gx ≤ h
   - Equality constraints: Ax = b
   - SVM dual maps naturally to this form

2. **McGill COMP 551 Lecture 12** (same as slide 012)
   - Shows transformation from α_i ≥ 0, α_i ≤ C to -α_i ≤ 0 and α_i ≤ C

3. **SVM Standard Form Derivation**
   - Inequality constraints: 
     - α_i ≥ 0  →  -α_i ≤ 0
     - α_i ≤ C  →   α_i ≤ C
   - Combined: G = [-I; I], h = [0; C·1]
   - Equality constraint: A = yᵀ, b = 0

## Slide 013 Specific Content

The slide shows:
- Original: α_i ≥ 0, α_i ≤ 1
- Transformed: -α_i ≤ 0, -α_i ≤ 1 (wait, this seems wrong - should be α_i ≤ 1)
- G matrix (8×4): Stack of -I and I
- h vector: [0,0,0,0,1,1,1,1]ᵀ
- A = [1 1 -1 -1], b = [0]
- y = [+1, +1, -1, -1] from constraint Σ y_i α_i = 0

### Correction Note
The slide shows "-α ≤ 1" which should be "α ≤ 1" (positive inequality). The G matrix has 8 rows:
- Rows 1-4: -I (for -α ≤ 0)
- Rows 5-8: I (for α ≤ 1)

But the slide's G matrix appears to have 0/1 entries that don't match standard form. The G matrix shown:
```
[ 1  0  0  0]
[ 0  0 -1  0]
[ 0  0  0 -1]
[ 0  0  0 -1]
[ 1  0  0  0]
[ 0  1  0  0]
[ 0  0  1  0]
[ 0  0  0  1]
```
This doesn't match the expected [-I; I] structure. The slide may have transcription errors in the matrix display.

## Verification
- Standard form is well-established in QP literature
- SVM dual-to-QP mapping is textbook material (Bishop PRML Ch.7, Boyd CVX Ch.11)