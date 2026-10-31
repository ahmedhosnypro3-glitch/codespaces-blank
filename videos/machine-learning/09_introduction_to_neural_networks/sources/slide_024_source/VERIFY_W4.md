# VERIFY_W4 — slide_024 claim register (wave 4, 2026-10-30)

Scope: `src_w4_021_024` · Worker: `w4-src-021` · Slide: `slide_024_source`
Content evidence: `analysis/slide_024_final.json` (title "For Sigmoid Function"; left column
sigmoid definition + 3 derivation boxes ending in `⇒ f'(x) = f(x)[1 − f(x)]`; right column
"Remember: ∂/∂x (1/x) = −1/x²", "Sigmoid (aka Logistic function)" squashing description) and
`sources/docparse_cascades/slide_024/composed/slide_024_composed.md` (14 elements, 4 formula
crops).
Search method: `agy -p` CLI quota-exhausted (HTTP 429, ~131 h reset), so all queries ran
through the **agy MCP web-search tool** (Google grounding, redirects resolved to real
page URLs). Every URL below was returned by the tool — none constructed by hand.

## Claim register

| # | Claim (DATA, not frame text) | Status | Evidence URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | Sigmoid definition `f(x) = Sigmoid(x) = 1/(1+e^{-x})` written as `(1+e^{-x})^{-1}` so the chain rule applies | CONFIRMED (re-confirmed) | https://builtin.com/articles/derivative-of-sigmoid-function — "Let the sigmoid function be denoted as f(x) … Rewrite this using a negative exponent so it is ready for the chain rule: f(x) = (1+e^{-x})^{-1}" | none |
| 2 | The derivation's first step `f'(x) = e^{-x}/(1+e^{-x})^2` from the chain rule on u⁻¹ with u = 1+e^{-x}` (minus one times minus one) | CONFIRMED | https://builtin.com/articles/derivative-of-sigmoid-function — "d/dx[u^{-1}] = −1·u^{-2}·du/dx, du/dx = −e^{-x} → f'(x) = e^{-x}/(1+e^{-x})^2"; https://courses.csail.mit.edu/6.034f/ai3/netmath.pdf | none |
| 3 | The add/subtract-one manipulation the slide performs — rewrite `e^{-x} = (1+e^{-x}) − 1`, then split `f'(x) = 1/(1+e^{-x}) × (1+e^{-x}−1)/(1+e^{-x})`, then `(1+e^{-x})/(1+e^{-x}) − 1/(1+e^{-x}) = 1 − f(x)` — arriving at `f'(x) = f(x)(1−f(x))` | CONFIRMED (the slide's intermediate boxes are each a step of this canonical derivation) | https://builtin.com/articles/derivative-of-sigmoid-function — "apply the clever algebraic manipulation … adding and subtracting 1 in the numerator of the second fraction … f'(x) = f(x)·(1 − f(x))"; https://www.gyansetu.in/machine-learning/sigmoid-function/ | none |
| 4 | "Sigmoid (aka Logistic function) … squashing function … unbounded values to a bounded probabilistic space (from 0 to 1)" — output range (0,1) with σ(0)=0.5, probability interpretation | CONFIRMED | https://developers.google.com/machine-learning/crash-course/logistic-regression/sigmoid-function — "the sigmoid function … its outputs are used to represent probabilities"; https://www.geeksforgeeks.org/machine-learning/derivative-of-the-sigmoid-function/ | none |
| 5 | The "Remember" box `∂/∂x (1/x) = −1/x²` (power rule applied to x⁻¹) | CONFIRMED (re-confirmed) | https://en.wikipedia.org/wiki/Power_rule — "d/dx(x^n) = n·x^{n−1}" with n = −1 → −x⁻²; https://www.mathsisfun.com/calculus/derivatives-rules.html — "rewrite 1/x as x^{−1}, apply power rule, convert back → −1/x²" | none |

### UNVERIFIED (kept as `[?]` / carried)

- The `| … |` delimiters in derivation boxes 4–6 are only described as "absolute value-style";
  they may actually be large parentheses/brackets on the original slide. Kept verbatim from the
  extraction; no source speaks to slide glyph style.
- Red `#c0392b` inside the peach boxes: whether it is text color or box border is unverifiable
  without the image.
- Whether the final red `⇒` is a drawn arrow shape or a text glyph is unverifiable.
- Equation 5's `-1/(1+e^{-x})` may originally read `− 1/(1+e^{-x})`; kept verbatim.
- Exact pixel coordinates / box dimensions are not in the source; positions are relative.

### Doc-parse cross-check (independent second read)

`composed/slide_024_composed.md` independently read 4 dedicated formula crops
(`slide_024.crop0{1..4}__formula`) plus the full-frame pass, and they agree with the vision
spec step by step:
- crop01 `f(x)= Sigmoid (x) = 1 /(1+e−x)` → claim 1
- crop02 `f '(x)= e^{-x} /((1+e^{-x})(1+e^{-x})) = 1*(1+ e^{-x} -1) /((1+e^{-x})(1+e^{-x}))` → **the slide's add/subtract-one manipulation, read independently** → claim 3
- crop03 `f '(x)= 1/(1+e^{-x}) ( (1+e^{-x}-1)/(1+e^{-x}) )` and
  `= 1/(1+e^{-x}) ( (1+e^{-x})/(1+e^{-x}) · -1/(1+e^{-x}) )` → claims 2–3 (split + rewrite steps)
- crop04 `f '(x)= 1/(1+e^{-x}) (1 - 1/(1+e^{-x}))` and the unpositioned `⇒ f '(x)= f(x) [1−f(x)]` → claim 3's final result
- `Remember: ∂/∂x (1/x) = −1/x²` (level-0 `<class_Text>` with `x<sup>2</sup>`) → claim 5
- `Sigmoid (aka Logistic function)` + `It is a **squashing** function used to convert an unbounded values to a bounded **probabilistic** space (from 0 to 1)` → claim 4, including the word-level emphasis the recreation must carry.

### Queries spent (3, all fresh this wave)

1. `sigmoid derivative step by step chain rule e^-x equals (1+e^-x) - 1 manipulation to get f(x)(1-f(x))`
2. `sigmoid function squashing function unbounded real line to bounded 0 to 1 probabilistic output sigma(0) = 0.5 logistic`
3. `derivative of 1/x is -1/x^2 power rule d/dx x^-1 calculus`

**Net effect: 0 changes to `analysis/slide_024_final.json`. All 5 data claims standing.**

## URL liveness check (2026-10-30, same work window as the recording)

All cited URLs were live-fetched in this window per the trust discipline. 21 of 29 returned
HTTP 200. The remaining eight (`apxml.com`, three `geeksforgeeks.org` pages, `datacamp.com`,
two `math.stackexchange.com` pages, `datascience.stackexchange.com`) returned HTTP 403 to a
scripted fetch — that is bot-blocking on those hosts (Cloudflare/Imperva user-agent
filtering), not a dead link: all eight were returned by the Google-grounding search tool
with quoted page content in the same window, i.e. they exist and are indexed. Every URL was
produced by the search tool; none were constructed by hand, and none went into the
do-not-reuse section as fabricated or dead.
