# Slide 004 — Revision: Chain Rule and ∂b/∂w_i for a weighted sum

Frame facts (from `analysis/parse/slide_004.parse.md`, data only): composition `b=f(a), c=f(b) ⇒ c=f(a)`;
`∂c/∂a = ∂c/∂b * ∂b/∂a` (labelled Chain Rule); `b=f(W) = w₁a₁+...+wₙaₙ = Σᵢ wᵢaᵢ`; `∂b/∂w_i = a_i`;
"Conclusion: ... then ∂b/∂w_i = a_i One Term ONLY"; multi-path case `∂c/∂b = Σᵢ (∂c/∂aᵢ · ∂aᵢ/∂b)`.
Method: agy web search (best-effort), verified against multivariable-chain-rule references.

## Sources

- Varsity Tutors — "Multivariable Chain Rule" (https://www.varsitytutors.com/practice/subjects/multivariable-calculus/lessons/multivariable-chain-rule) — confirms the single-path form ∂C/∂A = ∂C/∂B · dB/∂A and the sum-over-paths form ∂C/∂A = Σᵢ (∂C/∂Bᵢ · ∂Bᵢ/∂A) exactly as the slide states.
- IBM — "Backpropagation" (https://www.ibm.com/think/topics/backpropagation) — confirms ∂Net_j/∂w_ji = O_i ("one term only"), the weighted-sum specialisation the slide's conclusion is steering toward.

## Corrections / notes

- `∂b/∂w_i = a_i` for `b = Σᵢ wᵢaᵢ` — CONFIRMED: a weighted sum is linear in each weight, so the partial derivative picks out exactly one term (the slide's "One Term ONLY" note is the correct intuition).
- Multi-path chain rule `∂c/∂b = Σᵢ (∂c/∂aᵢ · ∂aᵢ/∂b)` — CONFIRMED as the standard multivariable chain rule for a common dependency; this is the mechanism that later yields the hidden-layer delta's Σ over downstream nodes.
- Course-authored elements: the variable naming (a, b, c, wᵢ) and the "(if a is changed, c will be changed accordingly)" phrasing are course pedagogy, not a source's notation — do not "fix" toward textbook variable names.
- The parse line `dc a3` (OCR of `∂c/∂a₃`) is an extraction artifact of the stacked fraction, not a slide error.
