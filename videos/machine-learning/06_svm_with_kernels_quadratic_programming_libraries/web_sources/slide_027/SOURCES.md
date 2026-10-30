# Source verification — slide 027

## Claims checked
- Title formula "Polynomial Kernel (of order 2)": K(a,b) = [a^T b + 1]^2 — CONFIRMED — COMS4771 kern-handout, Columbia — http://www.cs.columbia.edu/~djhsu/coms4771-f25/lectures/kern-handout.pdf
  Standard degree-2 polynomial kernel with constant term; K(x,z) = (x^T z + c)^p with c=1, p=2.
- Derivation line [a^T b+1]^2 = (a^T b)^2 + 2 a^T b + 1 = (a1b1 + a2b2)^2 + 2(a1b1 + a2b2) + 1 — CONFIRMED — same source
  Authoritative expansion = a1^2 b1^2 + a2^2 b2^2 + 2 a1b1 a2b2 + 2 a1b1 + 2 a2b2 + 1 — matches the slide term-for-term.
- Matrix form: (a1^2 a2^2 √2 a1a2 √2a1 √2a2 1)(b1^2, b2^2, √2 b1b2, √2b1, √2b2, 1)^T — CONFIRMED — same source
  This is φ(a)^T φ(b) for the quadratic map; √2·√2 = 2 reproduces every cross/linear coefficient in the expansion above.
- Feature map φ(x) ≡ (x1, x2) ⇒ (x1^2, x2^2, √2 x1x2, √2 x1, √2 x2, 1) — CONFIRMED — same source
  The literature's φ(x) = (1, √2x1, √2x2, x1^2, x2^2, √2x1x2) has the same six monomials in a different order.
- "2D ⇒ 6D" feature-space dimension — CONFIRMED — same source
  d=2 with constant term gives dimension C(d+p, p) = C(4,2) = 6; the c=0 (no +1) variant would be C(3,2)=3.

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild (sign conventions, symbol roles, value rounding).
  - Symbol roles: slide's `a`, `b` play the role of literature's x, z; `φ` plays the role of the explicit feature map. No content change needed.
  - The √2 factors on the cross and linear terms are EXACT, not rounding: they are the c=1 map's scaling. Never render them as 2.0 or drop them.
  - Component ORDER differs between the slide and some sources (constant `1` last here, first there). Keep the slide's order verbatim; the dot product is order-invariant.
  - "Order 2" = polynomial degree p=2 with c=1 (kernel includes the +1 constant). Do not render as homogeneous (a^T b)^2 — that would drop the linear terms and be a 3-D map.
