# Source verification — slide 022

## Claims checked

- Kernel shown as `[a^T b + 1]^2` is the **inhomogeneous polynomial kernel of degree 2** (coef0 = 1, gamma = 1, d = 2) — CONFIRMED — Wikipedia, Polynomial kernel https://en.wikipedia.org/wiki/Polynomial_kernel
  • matches the library form K(x,x') = (gamma <x,x'> + coef0)^degree with gamma = 1, coef0 = 1, degree = 2 — scikit-learn SVC docs https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
- "Map Input data from 2-D to 6-D": the explicit feature space of the inhomogeneous degree-2 kernel on 2-D input has exactly 6 monomials `{1, a1, a2, a1^2, a2^2, a1 a2}` = C(n+d, d) = C(4,2) = 6 — CONFIRMED — Wikipedia, Polynomial kernel (feature map for d = 2) https://en.wikipedia.org/wiki/Polynomial_kernel
- Mapped-vector terms `sqrt(2) a1 a2` and `sqrt(2) b1 b2` are the correct normalized interaction coefficients: the expansion `(a1b1 + a2b2 + 1)^2` carries a coefficient 2 on the cross term, which splits symmetrically as `(sqrt2 a1 a2)(sqrt2 b1 b2) = 2 a1a2 b1b2` — CONFIRMED — Columbia COMS 4771 kernel handout http://www.cs.columbia.edu/~djhsu/coms4771-f25/lectures/kern-handout.pdf
  • an unnormalized `2 a1a2` on one side only would make `u^T v` not equal `[a^T b+1]^2`; keep `sqrt(2)` exactly as printed.
- Constant component `1` in the mapped vector is present because the kernel is inhomogeneous (`+1` inside the bracket) — CONFIRMED — Wikipedia (c = 0 gives the homogeneous case, so c = 1 adds the constant feature) https://en.wikipedia.org/wiki/Polynomial_kernel
- "Kernelized Model — Calculate u^T v" equals the plain scalar kernel evaluation `[a^T b+1]^2` (kernel: inner product in the mapped space) — CONFIRMED — Wikipedia, Polynomial kernel https://en.wikipedia.org/wiki/Polynomial_kernel
- Exact component ORDER of the 6-D vector/column vectors and the contents of the "Normal Model" 2x2 matrix — UNVERIFIABLE: not resolvable from the frame at this resolution (validator already flags them as inferred in `analysis/slides_final.json`); term order is author-dependent and does not change `u^T v`.
- Slide's `sqrt(2) a1` / `sqrt(2) a2` (linear terms of the map) — CONFIRMED: the expansion `(a1b1+a2b2+1)^2` carries coefficient 2 on `a1b1` and `a2b2`, split symmetrically as `(sqrt2 a1)(sqrt2 b1)` etc. — Columbia COMS 4771 kernel handout http://www.cs.columbia.edu/~djhsu/coms4771-f25/lectures/kern-handout.pdf
- Slide's "Higher Computational Complexity?!!" against the explicit-map route — CONFIRMED: the map is O(d^n) (6 terms here) vs the scalar kernel's O(d) per pair, and Wikipedia notes the implicit space avoids "the combinatorial blowup in the number of parameters to be learned" — Wikipedia, Polynomial kernel https://en.wikipedia.org/wiki/Polynomial_kernel

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: `a = (a1, a2)`, `b = (b1, b2)` are 2-D inputs; `u = phi(a)`, `v = phi(b)` the mapped
  6-D vectors with `u = (a1^2, a2^2, sqrt(2)a1a2, sqrt(2)a1, sqrt(2)a2, 1)` and matching v-terms. The 6 (not 3,
  slide 021) dimension comes from the inhomogeneous `+1`: a homogeneous map has no `1`, `a1`, `a2` terms. Keep the
  `sqrt(2)` scale verbatim; re-ordering components is value-preserving. Equations render in normalized monomial
  order (squares, interaction, linear, constant).
