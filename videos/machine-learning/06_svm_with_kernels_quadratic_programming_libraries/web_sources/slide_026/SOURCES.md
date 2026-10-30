# Source verification — slide 026

## Claims checked

- The quadratic (degree-2 homogeneous) kernel K(a,b) = (aᵀb)² is realised by the feature map
  φ(x) = [x₁², x₂², √2 x₁x₂], i.e. φ(a)ᵀφ(b) = (aᵀb)² — CONFIRMED — D. Rosenberg, ML course
  Lecture 06a "kernel methods" https://davidrosenberg.github.io/mlcourse/Archive/2017Fall/Lectures/06a.kernel-methods.pdf
- The cross-term coefficient 2 in (a₁b₁ + a₂b₂)² = a₁²b₁² + a₂²b₂² + 2a₁b₁a₂b₂ is split symmetrically
  as (√2 a₁a₂)(√2 b₁b₂); that is exactly why the √2 factor appears in φ — CONFIRMED — Wikipedia,
  "Polynomial kernel" https://en.wikipedia.org/wiki/Polynomial_kernel (fetched live)
- K(x,z) = (xᵀz)² is the degree-2 homogeneous (c = 0) special case of K = (xᵀz + c)ᵈ — CONFIRMED —
  Wikipedia, "Polynomial kernel" https://en.wikipedia.org/wiki/Polynomial_kernel (fetched live)
- The slide's "2D ⇒ 3D" annotation: with n = 2 variables and degree d = 2 the degree-2 monomials are
  x₁², x₁x₂, x₂² — three of them, C(n+d−1, d) = C(3,2) = 3 — CONFIRMED — Rosenberg Lecture 06a
  https://davidrosenberg.github.io/mlcourse/Archive/2017Fall/Lectures/06a.kernel-methods.pdf
- The numeric instantiation a = [1; 2], b = [3; 4]: φ(a) = [1, 4, 2√2], φ(b) = [9, 16, 12√2],
  giving 9 + 64 + 48 = 121, and (1·3 + 2·4)² = 11² = 121 — CONFIRMED — deterministic exact-arithmetic
  check, no external source required (the cross term (2√2)(12√2) = 48 exactly)

## Overall

- VERDICT: CONFIRMED
- Every mathematical claim printed on the slide — the feature map, the √2 normalisation, the 2D⇒3D
  dimensionality claim, and the 121 worked example — matches the standard quadratic-kernel
  derivation. No corrections needed; nothing invented.
- Tolerance notes for the rebuild (transcript artifacts — record, do NOT edit `verbatim_text`): the
  OCR line `[a1 a2 √2a1a2]` drops the superscript squares; the authoritative column is
  φ(a) = [a₁², a₂², √2a₁a₂]. Likewise `[12 22 √2 1*2]` = [1², 2², √2·1·2] = [1, 4, 2√2] and
  `[32 42 42]` = [3², 4², √2·3·4] = [9, 16, 12√2].
- Symbol/column order: the slide prints φ with the two square terms first and the √2 cross-term last;
  most references write [x₁², √2x₁x₂, x₂²]. The dot product is order-independent — build it in the
  slide's printed order. All terms are positive and √2 is the positive normaliser, so no sign
  ambiguity arises. Keep the "2D ⇒ 3D" annotation exactly as the frame shows it.
- Do-not-reuse note: a search attributed the √2 derivation to arXiv 2410.12635, but the live text of
  that page is a K^{-1/2}-based feature-map paper containing no quadratic φ — do not cite it here.
