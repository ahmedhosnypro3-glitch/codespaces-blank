# Source verification — slide 032

## Claims checked

- "Sum of Kernels is a Kernel": `K(a,b) = K1(a,b) + K2(a,b)` — CONFIRMED — Cortes & Vapnik, "Support-Vector Networks", JMLR 5 (2004) https://www.jmlr.org/papers/volume5/cortes04a/cortes04a.pdf
  Authoritative closure rule: if `k1`, `k2` are positive-definite kernels on `X × X`, then `k1 + k2` is again a valid kernel (the Gram matrix of the sum is `K1 + K2`, a sum of two PSD matrices). Same rule stated in the kernel construction chapter https://mlweb.loria.fr/book/en/constructingkernels.html and in Jordan's Kernels chapter (Berkeley) https://people.eecs.berkeley.edu/~jordan/kernels/0521813972c03_p47-84.pdf.

- "Scalar Product of Kernel is a kernel": `K(a,b) = αK1(a,b)` — CONFIRMED — Jordan's Kernels chapter (Berkeley EECS) https://people.eecs.berkeley.edu/~jordan/kernels/0521813972c03_p47-84.pdf
  Authoritative closure rule: `k1` a valid kernel and `α ≥ 0` a non-negative scalar ⇒ `α·k1` is a valid kernel (Gram matrix `αK1` stays PSD). The slide states the formula correctly but omits the gating condition on `α` — see tolerance notes. CMU 10-701 Kernels lecture https://www.cs.cmu.edu/~ninamf/ML11/lect1020.pdf states the same rule with `α ≥ 0`.

- "Product of Kernels is a Kernel": `K(a,b) = K1(a,b) ∗ K2(a,b)` — CONFIRMED — Schur Product Theorem, as cited in the kernel construction chapter https://mlweb.loria.fr/book/en/constructingkernels.html
  Authoritative closure rule: the pointwise (element-wise / Hadamard) product of two positive-definite kernels is again positive-definite — the Hadamard product of two PSD Gram matrices is PSD. Equivalently the feature maps compose by tensor product, `φ(x) = φ1(x) ⊗ φ2(x)`. Also listed among the closure properties at https://en.wikipedia.org/wiki/Positive-definite_kernel and https://www.cs.cmu.edu/~ninamf/ML11/lect1020.pdf.

- "Combination of the above rules is a Kernel": `K(a,b) = K1(a,b) ∗ K2(a,b) + αK3(a,b)` — CONFIRMED — Cortes & Vapnik, JMLR 5 (2004) https://www.jmlr.org/papers/volume5/cortes04a/cortes04a.pdf
  Authoritative form: the result of applying the product rule, then the non-negative scalar multiple, then the sum rule is again a valid kernel; valid kernels form a convex cone (finite non-negative linear combinations and finite products of kernels are kernels). The slide's expression is exactly that composition, so it holds provided `α ≥ 0`.

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild (sign conventions, symbol roles, value rounding):
  - Sign convention: the scalar-multiple rule requires `α ≥ 0`. The slide prints no condition on `α`; do not add one to `verbatim_text`, but keep the combined formula (card 4) gated on the same `α ≥ 0` when reasoning about it. A negative `α` is not a kernel in general.
  - Symbol roles: `K` is the new kernel built from `K1`, `K2`, `K3` (the slide's capitalisation); `a`, `b` are the two input points (the role of textbook `x`, `x'`); `α` (alpha) is a non-negative scalar weight. No subscript origin is shown on the slide — do not attribute it.
  - The `∗` glyph on cards 3 and 4 denotes the pointwise/Hadamard kernel product, not matrix multiplication and not convolution. Render as a centered dot or standard multiplication sign in Professional Format; keep the slide's `K1 ∗ K2` token order.
  - No numeric constant, dataset name, library name, or hyperparameter name appears on the slide; nothing to round or reconcile.
