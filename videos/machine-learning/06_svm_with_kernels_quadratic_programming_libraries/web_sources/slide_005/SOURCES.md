# Source verification — slide 005

## Claims checked

- The matrix–vector product A·X expands into the three row·X components (a11x1+a21x2+a31x3),
  (a12x1+a22x2+a32x3), (a13x1+a23x2+a33x3) — CONFIRMED — UCI Lecture17 http://graphics.ics.uci.edu/ICS6N/NewLectures/Lecture17.pdf
- (row1·X)x1 + (row2·X)x2 + (row3·X)x3 gives a11x1²+a22x2²+a33x3² + (a21+a12)x1x2
  + (a31+a13)x1x3 + (a32+a23)x2x3 — CONFIRMED — FIU Math16 notes https://faculty.fiu.edu/~boydj/mathecon/math16.pdf
- a11, a22, a33 are the coefficients of the squared terms X1², X2², X3² — CONFIRMED —
  U of Lethbridge Math 3410 https://opentext.uleth.ca/Math3410/sec-quadratic.html
- a21+a12 is the coefficient of the cross term x1x2, and if a12 = a21 each is half of it — CONFIRMED —
  EulerPad, Quadratic Forms https://eulerpad.app/guides/quadratic-forms-and-positive-definite-matrices
- The same off-diagonal rule holds for the (1,3) pair: a13+a31 is the coefficient of x1x3 with
  a13 = a31 = ½ — CONFIRMED — Calc Workshop, Matrix of the Quadratic Form https://calcworkshop.com/symmetric-matrices/matrix-of-the-quadratic-form/
- The same off-diagonal rule holds for the (2,3) pair: a32+a23 is the coefficient of x2x3 with
  a32 = a23 = ½ — CONFIRMED — Calc Workshop, Matrix of the Quadratic Form https://calcworkshop.com/symmetric-matrices/matrix-of-the-quadratic-form/
- The reduced three-variable expression is a quadratic form (homogeneous degree-2 polynomial
  written xᵀAx with A symmetric) — CONFIRMED — U of Lethbridge Math 3410 https://opentext.uleth.ca/Math3410/sec-quadratic.html
- The bottom matrix's diagonal cells are the pure-square coefficients and each symmetric
  off-diagonal pair carries half its cross-term coefficient (the "0.5 coef of" labels) — CONFIRMED —
  Calc Workshop, Matrix of the Quadratic Form https://calcworkshop.com/symmetric-matrices/matrix-of-the-quadratic-form/
- The bottom matrix plays the role of the symmetric matrix of the quadratic form (the analysis's
  "likely the Hessian Q in ½xᵀQx" reading) — CONFIRMED as an interpretation, not on-slide text:
  ∇²(½xᵀQx) = Q when Q is symmetric — MathWorks MATLAB Central https://uk.mathworks.com/matlabcentral/answers/240150-how-can-we-calculate-the-hessian-matrix-in-general
- Course context, not stated on the slide: the SVM dual is the QP min ½αᵀQα − 1ᵀα with
  Q_ij = y_i y_j K(x_i,x_j), Q symmetric — CONFIRMED — Domino, Fitting SVMs with QP https://domino.ai/blog/fitting-support-vector-machines-quadratic-programming

## Overall

- VERDICT: CONFIRMED
- Every algebraic claim on the slide matches the standard quadratic-form expansion. No corrected
  data, no invented content.
- Tolerance notes for the rebuild (transcript artifacts — record, do NOT edit `verbatim_text`):
  the final reduction line reads `(a32+a23) x1 x3`; the authoritative pairing is (a32+a23) with
  **x2x3**. The line `a33 x2` should be `a33 x3²`, `a22 x2` should be `a22 x2²`, and
  `a33 ⇒ Coefficient of X2` should read Coefficient of **X3**. These are OCR/transcription
  artifacts: build the math correctly, keep the transcript verbatim.
- Symbol roles: `a_ij` is the (i,j) entry of the implicitly symmetric coefficient matrix; the slide
  writes `1/2` for the per-entry half coefficient. The derivation is symbolic — no rounding concerns.
