# Source verification — slide 004

## Claims checked

- Box 1, eq. 1: (x₁ x₂)·[[a₁₁ a₁₂; a₂₁ a₂₂]]·(x₁; x₂) = (a₁₁x₁ + a₂₁x₂, a₁₂x₁ + a₂₂x₂)·(x₁; x₂) — CONFIRMED — Khan Academy, "Expressing a quadratic form with a matrix" https://www.khanacademy.org/math/multivariable-calculus/applications-of-multivariable-derivatives/quadratic-approximations/v/expressing-a-quadratic-form-with-a-matrix
- Box 1, eq. 1 intermediate row vector (a₁₁x₁ + a₂₁x₂, a₁₂x₁ + a₂₂x₂): the first entry comes from row 1 of A on the left factor and the second from row 2 — CONFIRMED — Math Insight, "Matrix vector multiplication" https://mathinsight.org/matrix_vector_multiplication
- Box 1, eq. 2: the distributed expansion is a₁₁x₁² + a₂₁x₁x₂ + a₁₂x₁x₂ + a₂₂x₂² — CONFIRMED — UOMustansiriyah lecture notes https://uomustansiriyah.edu.iq/media/lectures/6/6_2020_12_22!11_07_29_AM.pdf
- Box 1, eq. 3: collecting the cross terms gives a₁₁x₁² + (a₂₁ + a₁₂)x₁x₂ + a₂₂x₂², a quadratic form — CONFIRMED — UOMustansiriyah lecture notes https://uomustansiriyah.edu.iq/media/lectures/6/6_2020_12_22!11_07_29_AM.pdf
- Box 2, line 1: a₁₁ is the coefficient of x₁² — CONFIRMED — U of Lethbridge Math 3410 https://opentext.uleth.ca/Math3410/sec-quadratic.html
- Box 2, line 3: a₂₂ is the coefficient of x₂² — CONFIRMED — U of Lethbridge Math 3410 https://opentext.uleth.ca/Math3410/sec-quadratic.html
- Box 2, line 2: a₂₁ + a₁₂ is the coefficient of the cross term x₁x₂ — CONFIRMED — UOMustansiriyah lecture notes https://uomustansiriyah.edu.iq/media/lectures/6/6_2020_12_22!11_07_29_AM.pdf
- Box 2, line 2 second arrow: under the symmetric convention a₁₂ = a₂₁ = ½(coefficient of x₁x₂) — CONFIRMED — Calc Workshop, "Matrix of the Quadratic Form" https://calcworkshop.com/symmetric-matrices/matrix-of-the-quadratic-form/
- Box 3 result matrix: the symmetric matrix of the quadratic form has diagonal = pure-square coefficients and both off-diagonal entries = ½ the cross-term coefficient — CONFIRMED — Calc Workshop, "Matrix of the Quadratic Form" https://calcworkshop.com/symmetric-matrices/matrix-of-the-quadratic-form/
- Box 3's "0.5 coef of x₁x₂" off-diagonal labels therefore read as a₂₁ = a₁₂ = ½(a₁₂ + a₂₁), with the two off-diagonal entries equal, not complementary — CONFIRMED — Purdue Math, "Symmetric matrices and quadratic forms" https://www.math.purdue.edu/~eremenko/dvi/lect4.7
- Implicit premise behind the ½ rule: a matrix represents a quadratic form only up to its skew-symmetric part; the symmetric representative A = (M + Mᵀ)/2 is the unique one — CONFIRMED — Purdue Math, "Symmetric matrices and quadratic forms" https://www.math.purdue.edu/~eremenko/dvi/lect4.7

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: all four display equations are standard and need no numeric correction. The ½ factor in "a₁₂ = a₂₁ = ½ Coefficient of x₁x₂" holds only because A is taken symmetric; if the rebuild renders a₁₂ ≠ a₂₁ the coefficient of x₁x₂ would be a₁₂ + a₂₁, so keep the Box 3 matrix symmetric with both off-diagonal entries showing the same 0.5 multiplier. Box 3's ⇒ result matrix is the symmetric matrix of the quadratic form, so its top-left cell must equal a₁₁ and its bottom-right cell a₂₂ — do not relabel them as independent "coef of" values.
