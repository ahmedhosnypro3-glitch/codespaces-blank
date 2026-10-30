# Source verification — slide 029

## Claims checked

- "Taylor series expansion of (x): e^x = 1 + x/1! + (x)^2/2! + (x)^3/3! + (x)^4/4! + (x)^5/5! + ..... ∞" (right pane)
  — CONFIRMED — UBC Maclaurin expansion of e^x https://blogs.ubc.ca/infiniteseriesmodule/units/unit-3-power-series/taylor-series/maclaurin-expansion-of-ex/ ; edflik https://www.edflik.com/blog/mastering-taylor-and-maclaurin-series-expansions-in-edexcel-further-mathematics/
  Authoritative: e^x = Σ_{n=0}^∞ x^n/n!, convergent for all real x. The caption drops the base "e", but the boxed formula prints e^x — a label, not a formula error.
- "e^3 = 1 + 3/1! + (3)^2/2! + (3)^3/3! + (3)^4/4! + (3)^5/5! + ..... ∞" and the 4/5/6-term values 13, 16.375, 18.4
  — CONFIRMED — exact partial sums 13.0, 16.375, 18.400 (deterministic local arithmetic on the same series).
- "Approx. to 7 terms ⇒ 19.413" — CONFIRMED — exact 7-term sum 19.412500; 19.413 is standard half-up 3-dp rounding.
- "Approx. to 8 terms ⇒ 19.84" — CORRECTED — exact 8-term (n=0..7) sum is 19.846429; the authoritative 2-dp value is 19.85, so the slide truncates (rounds toward zero).
- "Approx. to 9 terms ⇒ 19.8420.01" — CORRECTED — exact 9-term (n=0..8) sum is 20.009152 → 20.01. The printed string is the 8-term "19.84" overprinting the true 9-term "20.01" (confirmed by two independent doc-parse passes on a zoomed crop, both returning the same merged string). Authoritative: 20.009152.
- "Actual Value ⇒ 20.086" — CONFIRMED — e^3 = 20.085536923187667874, 3-dp = 20.086 — Microsoft PowerQuery Number.Exp https://learn.microsoft.com/en-us/powerquery-m/number-exp ; Omnicalculator https://www.omnicalculator.com/math/e-power-x
- "e^(-1/2(a-b)^2) = e^(-1/2(a^2+b^2-2ab)) = e^(-a^2/2) e^(-b^2/2) e^(ab)" (left pane box 1) — CONFIRMED — Wikipedia RBF kernel https://en.wikipedia.org/wiki/Radial_basis_function_kernel ; Daily Dose of DS https://www.dailydoseofds.com/p/the-mathematics-behind-rbf-kernel/
  Authoritative: K(a,b) = exp(-1/2||a-b||^2) = exp(-||a||^2/2) exp(-||b||^2/2) exp(a·b).
- "e^(ab) = 1 + ab/1! + (ab)^2/2! + (ab)^3/3! + (ab)^4/4! + (ab)^5/5! + ..... ∞" (left pane box 2) — CONFIRMED — Maclaurin series at u = ab (same series source).
- Factorization "(1 + a/√1! + a^2/√2! + a^3/√3! + a^4/√4! + ...)^T (1 + b/√1! + b^2/√2! + ...)", labelled φ(a)^T φ(b) (left pane box 3) — CONFIRMED — Techietory kernel-trick lecture https://techietory.com/kernel-trick-svms-explained-intuitively/ ; simonensemble RBF post https://simonensemble.github.io/posts/2024-03-25-rbf-kernel/
  Authoritative φ(x) = e^(-γ||x||^2)[1, √(2γ)/1! x, √((2γ)^2/2!)(x⊗x), ...]; at γ = 1/2 each √((2γ)^n/n!) reduces to exactly 1/√(n!), matching the slide, and Σ a^n b^n/n! = e^(ab).
- Slide kernel exp(-1/2||a-b||^2) is the RBF/Gaussian kernel at γ = 1/2 (σ = 1, since γ = 1/(2σ^2)) — CONFIRMED — Wikipedia RBF kernel (γ = 1/(2σ^2)); sklearn K(x,z) = exp(-γ||x-z||^2) https://scikit-learn.org/stable/modules/metrics.html#rbf-kernel

## Overall

- VERDICT: CORRECTED
- 10 claims checked: 8 CONFIRMED, 2 CORRECTED (both numeric rounding artifacts in the e^3 ladder — the 8-term truncation and the overprinted 9-term line); 0 UNVERIFIABLE.
- Tolerance notes: frame text stays exactly as printed — keep "19.8420.01" and "19.84" verbatim (overlap/typo included) and never rewrite them as 20.01/19.85; those corrections live in this report only. Keep the caption "Taylor series expansion of (x)" without adding a base "e".
- Sign convention: the cross term is POSITIVE — render K(a,b) = e^(-a^2/2)·e^(-b^2/2)·e^(ab) with the minus sign only inside the exponent; never write e^(-ab).
- Symbol roles: "(a-b)^2" = ||a-b||^2 (squared Euclidean norm); "ab" inside e^(ab) = a·b (dot product); a and b are vectors, not scalars.
- The slide's φ(a)^T φ(b) = e^(ab) carries no e^(-a^2/2) factor (it sits in the preceding equality) — keep that split as printed. If a standalone infinite map is drawn instead, the authoritative φ(x) folds e^(-γ||x||^2) in.
- φ coefficients render as 1, a/√1!, a^2/√2!, a^3/√3!, a^4/√4! — i.e. 1/√(n!) per degree, exact at γ = 1/2.
- Ladder rounding is inconsistent on the slide (2-dp truncation at 8 terms; 3-dp half-up at 7 and 9 terms). Exact reference ladder: 13, 16.375, 18.4, 19.4125, 19.846429, 20.009152, 20.063393, e^3 = 20.085537.
