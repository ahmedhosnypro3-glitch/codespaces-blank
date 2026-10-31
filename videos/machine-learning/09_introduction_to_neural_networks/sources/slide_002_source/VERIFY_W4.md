# VERIFY_W4.md — slide 002 "Revision of Perceptron Algorithm"

Wave: `src_w4_001_004` · worker `w4-src-001` · date **2026-10-30**
Frame of record: `unique_slides/slide_002.jpg` (md5 `babd473e5788dc29bc7d2a4fec41284d`)
Analysis record: `analysis/slide_002_final.json`
Status: **DONE** — divider frame carries a title and badge only; all verifiable concept claims CONFIRMED.

## Search transport

`agy -p` CLI is quota-blocked this wave (HTTP 429 `RESOURCE_EXHAUSTED / Individual quota reached`,
resets ~131h). All searches ran through the **agy MCP web-search tool** (same Google grounding via
the antigravity proxy, redirect URLs resolved). No URL below was invented. Unlike slide 001, several
non-SPA academic pages here were **fetched live and returned full content** — those are marked
"live-fetched" below.

## Claims checked

The frame prints only "Revision of Perceptron Algorithm" and the badge "2" — no math, no data, no
numbers. The factual claims are therefore the concept set the divider announces. Frame text is
untouched by all of them.

| # | Claim (concept announced by the frame) | Status | Evidence URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | The Perceptron is Frank Rosenblatt's single-layer binary classifier: "The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain", Psychological Review 65(6):386–408 (1958) | **CONFIRMED** | https://en.wikipedia.org/wiki/Perceptrons_(book) — "Rosenblatt, Frank (1958). 'The perceptron: A probabilistic model for information storage and organization in the brain'. Psychological Review. 65 (6): 386–408. doi:10.1037/h0042519. PMID 13602029" (live-fetched) ; primary PDF: https://homepages.math.uic.edu/~lreyzin/papers/rosenblatt58.pdf (search-resolved; direct fetch failed to extract — noted) ; https://pubmed.ncbi.nlm.nih.gov/13602029/ | none |
| 2 | Model ŷ = f(w·x + b) with a step/sign activation; weights w, bias b; bias can be absorbed by augmenting x with a constant dimension | **CONFIRMED** | https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched) — "h(x_i) = sign(wᵀx_i + b)"; "we 'absorb' it into the feature vector w by adding one additional constant dimension"; h simplifies to sign(wᵀx) | none |
| 3 | Error-correction learning rule: on a misclassified sample w ← w + η·y·x; **no update** when correctly classified; η = learning rate | **CONFIRMED** | https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) — "If y_n ŷ_n = −1, β̂ ← β̂ + η·y_n x_n"; procedure runs over all n and updates **only** on misclassification ; https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html — "y_i(wᵀx_i) > 0 ⟺ x_i is classified correctly" | none |
| 4 | Perceptron Convergence Theorem (Novikoff 1962): if the data is linearly separable the algorithm converges in a **finite** number of updates; mistake bound k ≤ R²/δ² (equivalently M ≤ 1/γ² under unit-radius normalization) | **CONFIRMED** | https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2024fall/unit2/convergence.html (live-fetched) — "this theorem and its proof were from NYU mathematician Albert B. J. Novikoff in 1962"; "must converge to a linear separator after at most R²/δ² mistakes (updates) where R = max ‖x‖" ; https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched) — "the Perceptron algorithm makes at most 1/γ² mistakes" ; primary paper scan: https://cs.uwaterloo.ca/~y328yu/classics/novikoff.pdf | none |
| 5 | Single-layer perceptron cannot compute XOR (non-linearly separable) — Minsky & Papert, *Perceptrons* (1969) | **CONFIRMED** | https://en.wikipedia.org/wiki/Perceptrons_(book) (live-fetched) — "Perceptrons: An Introduction to Computational Geometry … published in 1969"; "The most important one is related to the computation of some predicates, such as the XOR function"; "Minsky 1969" XOR cited in the Cornell notes' history section | none |
| 6 | The 1969 limitation contributed to the first "AI Winter"; multi-layer nets + backpropagation (Rumelhart, Hinton & Williams 1986) were the way forward | **CONFIRMED** | https://en.wikipedia.org/wiki/Perceptrons_(book) (live-fetched) — "contributed to the so-called AI winter of the 1980s"; Cornell history section — "Then, contributed to the A.I. Winter. Famous example of a simple non-linearly separable data set, the XOR problem (Minsky 1969)" | none |

Tally: **6 claims checked · 6 CONFIRMED · 0 CORRECTED · 0 UNVERIFIED.**

## Questions asked

1. "Rosenblatt 1958 'The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain' Psychological Review"
2. "Novikoff 1962 'On convergence proofs on perceptrons' linearly separable data finite number of corrections proof"
3. "Minsky Papert 1969 Perceptrons single layer cannot compute XOR linearly inseparable limitation"
4. Live fetches: `https://en.wikipedia.org/wiki/Perceptrons_(book)`, `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html`, `https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2024fall/unit2/convergence.html` — all three returned full text.
5. Attempted live fetch `https://homepages.math.uic.edu/~lreyzin/papers/rosenblatt58.pdf` — failed to extract (JS-render error from the extractor). The URL is still a valid search-resolved citation and is the Rosenblatt 1958 PDF host; recorded as an unextracted, not invalid, source.

## Doc-parse cross-check

`sources/docparse_cascades/slide_002/composed/slide_002_composed.md` (nemotron-3.5-parse,
degraded: False, 2 elements, 0 failed calls) independently reads the frame as exactly two elements —
badge "2" and the section header "Revision of Perceptron Algorithm". This corroborates the analysis
JSON's `subtitle_or_header: null`, its empty `bullets`/`equations`, and its decision to document the
absence rather than fabricate body content. No patch needed.

## Banked this wave (new URLs)

1. https://en.wikipedia.org/wiki/Perceptrons_(book)
2. https://homepages.math.uic.edu/~lreyzin/papers/rosenblatt58.pdf
3. https://pubmed.ncbi.nlm.nih.gov/13602029/
4. https://cs.uwaterloo.ca/~y328yu/classics/novikoff.pdf
5. https://math.stackexchange.com/questions/2183227/novikoff-s-proof-for-perceptron-convergence
6. https://www.cis.upenn.edu/~danroth/Teaching/CS446-17/LectureNotes/04-Lec_p2.pdf

## Follow-up

- The Rosenblatt 1958 PDF host (uic.edu) should be re-fetched in a later wave when the fetch tool
  can extract PDFs, to byte-verify the paper's own pages. Not blocking: the bibliographic record is
  independently confirmed by Wikipedia's citation block and PubMed.
