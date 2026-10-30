# Source verification — slide 025

## Claims checked
- Feature map "φ(x) ≡ [x1 x2] ⇒ [x1² x2² √2x1x2]" (the cross term carries the √2 factor) — CONFIRMED — Columbia COMS4771 "kernels" handout — http://www.cs.columbia.edu/~djhsu/coms4771-f25/lectures/kern-handout.pdf
  Literature writes φ(x) = [x1², √2 x1x2, x2²]; same three components, different order. The dot product is order-invariant.
- "φ(a)ᵀ φ(b) = [aᵀ b²]" i.e. the 3-D inner product collapses to the square of the 2-D dot product — CONFIRMED — Wikipedia, "Polynomial kernel" — https://en.wikipedia.org/wiki/Polynomial_kernel
  φ(a)ᵀφ(b) = a1²b1² + (√2 a1a2)(√2 b1b2) + a2²b2² = a1²b1² + 2a1a2b1b2 + a2²b2² = (a1b1 + a2b2)².
- First-line expansion "[aᵀ b]₁₂ = [a1b1+a2b2]² = a1²b1² + a2²b2² + 2a1b1a2b2" — CONFIRMED — exact-arithmetic check, no URL needed
  With a=[1;2], b=[3;4]: φ(a)=[1,4,2√2], φ(b)=[9,16,12√2], product 9+64+48=121 = 11² = (1·3+2·4)². Exact, not rounded.
- Why √2 appears: the cross term of (a1b1+a2b2)² is 2a1b1a2b2, split symmetrically as (√2 a1a2)(√2 b1b2) — CONFIRMED — University of Utah Math DS Lecture 4 — https://www.math.utah.edu/~bwang/mathds/Lecture4.pdf
  Without √2 the product would be a1x2b1x2... (i.e. a1²b1² + a1a2b1b2 + a2²b2²), which does NOT factor into (aᵀb)². √2 is exact, never 2.0 and never dropped.
- "K(x,z) = [xᵀ z]²" is the degree-2 homogeneous (c = 0) special case of K = (xᵀz + c)ᵈ — CONFIRMED — Wikipedia, "Polynomial kernel" — https://en.wikipedia.org/wiki/Polynomial_kernel
  Distinguished from slide 022's inhomogeneous (aᵀb + 1)² → 6-D map; this slide's c = 0 case has no linear/constant terms.
- "2D ⇒ 3D" annotation: degree-2 monomials in n=2 variables number C(n+d−1, d) = C(3,2) = 3 (x1², x1x2, x2²) — CONFIRMED — CMU 10-701/11 Lecture 10/20 — https://www.cs.cmu.edu/~ninamf/ML11/lect1020.pdf
  Same count reached via the monomial enumeration on Cornell stats.SE — https://stats.stackexchange.com/questions/401304/how-does-this-transformation-from-2d-to-3d-work-mathmatically
- Title's "Kernel Trick" framing (compute φ(a)ᵀφ(b) implicitly as (aᵀb)² without materializing the 3-D vectors) — CONFIRMED — UW CSE446 kernels lecture — https://courses.cs.washington.edu/courses/cse446/23wi/schedule/lecture_17_kernels_annotated.pdf

## Overall
- VERDICT: CONFIRMED
- All data on the frame is correct. The only defects are OCR transcript artifacts, recorded here and NOT to be applied to `verbatim_text`.
- Tolerance notes for the rebuild:
  - Symbols: slide's `a`, `b` = literature's x, z; φ(a), φ(b) = literature's u, v. No content change.
  - √2 is EXACT and positive (2 = √2·√2); never render as 2.0, 1.414, or drop it. All terms positive — no sign convention risk.
  - Component order is free (dot product order-invariant), but build in the slide's printed order: [x1², x2², √2x1x2].
  - Transcript artifacts to keep verbatim, not fix: raw OCR `[a1 a2 √2a1a2]` omits the squares (authoritative: [a₁², a₂², √2a₁a₂]); raw OCR `b1 2 b2 2 v2 b1b2` reads `√2 b1b2` (v = √).
  - Keep "2D ⇒ 3D" exactly as printed; it is correct (C(3,2) = 3), not a typo.
  - Do not confuse with slide 022's inhomogeneous (aᵀb+1)² → 6-D; this slide is homogeneous (c = 0) → 3-D.
