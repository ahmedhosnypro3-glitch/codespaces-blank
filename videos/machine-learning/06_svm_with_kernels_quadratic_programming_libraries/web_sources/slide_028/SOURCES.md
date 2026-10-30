# Source verification — slide 028

## Claims checked
- Kernel identity [aᵀb+1]² = φ(a)ᵀφ(b), i.e. the degree-2 inhomogeneous polynomial
  kernel equals an inner product of the explicit 6-D feature map — CONFIRMED — NUS
  CS5339 kernel notes https://www.comp.nus.edu.sg/~scarlett/CS5339_notes/05-Kernel_Notes.pdf
- Feature map for 2-D inputs, φ(x) ≡ [x₁ x₂ √2x₁x₂ √2x₁ √2x₂ 1]ᵀ, where the √2 on the
  cross/linear terms splits the coefficient 2 across both maps (√2·√2 = 2) — CONFIRMED —
  Xavier Bourret Sicotte, Kernel feature map
  https://xavierbourretsicotte.github.io/Kernel_feature_map.html
- Feature count: 6 components for the degree-2 map in 2-D (= C(n+d, d) = C(4,2) = 6) —
  CONFIRMED — Columbia COMS4771 kernel handout
  http://www.cs.columbia.edu/~djhsu/coms4771-f25/lectures/kern-handout.pdf and
  Wikipedia "Polynomial kernel" https://en.wikipedia.org/wiki/Polynomial_kernel
- Numeric example a = [1 2], b = [3 4]: φ(a)ᵀφ(b) = 1·9 + 4·16 + 2√2·12√2 + √2·3√2 +
  2√2·4√2 + 1 = 9+64+48+6+16+1 = 144, and (aᵀb+1)² = (3+8+1)² = 12² = 144 —
  CONFIRMED (self-consistent arithmetic, re-derived independently)

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: the slide's φ column order is
  [x₁² x₂² √2x₁x₂ √2x₁ √2x₂ 1] vs the textbook order
  [1 √2x₁ √2x₂ x₁² x₂² √2x₁x₂] — same six components, order irrelevant to the dot
  product, so keep the slide's order and transpose alignment exactly as shown.
- The √2 factors are load-bearing: with a plain x₁x₂ term the identity fails
  (φ(a)ᵀφ(b) = 144−48+... ≠ 144), so render them, never as 2x₁x₂.
- Constant term is +1 inside the square, not +c or +2; no γ/scale parameter appears.
