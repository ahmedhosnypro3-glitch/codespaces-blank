# Source Research: slide_002

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_002_source/docparse_run/`
- Full frame parse: `full/slide_002.parse.md`
- Composed: `composed/slide_002_composed.md`
- Crop cascade: 0 crops (simple content)
- Chat lane: DEGRADED (model `docparsechat` not available on gateway) — deterministic fallback used

## Extracted Content (verbatim)

### Slide Title / Section Header
**Revision of Perceptron Algorithm**

### Slide Number
2

---

## Web Search Verification

### Concepts to Verify
1. Perceptron Algorithm — foundational neural network algorithm
2. Context: "Revision of" suggests this is a review/recap slide

### Search Results

**Perceptron Algorithm (Rosenblatt, 1957/1958)** [[1]](https://pages.cs.wisc.edu/~tcmurphy4/docs/mapl_2017.pdf) [[3]](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/a/27637/files/2016/03/rosenblatt-1957.pdf) [[4]](https://deeplearning.cs.cmu.edu/S26/documents/readings/Perceptron_Learning_Algorithm_and_Convergence.pdf) [[9]](https://en.wikipedia.org/wiki/Perceptron)

**Model**: Single-layer perceptron maps input vector x ∈ ℝ^d to binary output y ∈ {+1, -1}
- ŷ = f(w·x + b) where f(z) = step function (sign)
- Weights w, bias b, activation f(z)

**Learning Rule (Error-Correction)**:
- For each sample (x_i, y_i): compute ŷ_i = f(w_k·x_i)
- If error (y_i ≠ ŷ_i): w_{k+1} = w_k + η y_i x_i
- If correct: w_{k+1} = w_k (no update)
- Learning rate η often = 1 for theoretical proofs

**Perceptron Convergence Theorem** (Novikoff, 1962) [[6]](https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2024fall/unit2/convergence.html):
- If data is linearly separable → algorithm converges in FINITE steps
- Proof: projection onto optimal w* grows linearly (k), ||w_k||² grows at most linearly (k) → bounded mistakes

**Limitations** (Minsky & Papert, 1969):
- Single-layer cannot compute XOR (non-linearly separable)
- Led to first "AI Winter" until multi-layer + backprop (1980s)
- Today: perceptron = artificial neuron, building block of deep networks

---

## Research Summary

This is a **section divider slide** (slide 2) titled "Revision of Perceptron Algorithm". It serves as a transition into a review of the Perceptron algorithm — the foundational single-layer neural network for binary classification.

The Perceptron (Rosenblatt, 1957/1958) is the historical precursor to modern neural networks. A "Revision of" slide typically precedes a detailed walkthrough of:
- Perceptron learning rule: w ← w + η(y - ŷ)x
- Convergence theorem (linearly separable data)
- Limitations (XOR problem, need for multi-layer networks)

No mathematical equations or complex visual elements on this slide — just the section title and slide number.

### Uncertain Items (marked [?])
- None — content is minimal and clear

---
*Generated: 2026-10-27*

---

## Wave-3 verification (2026-10-30)

**Content evidence**: `analysis/reanalysis_v2/slide_002_reanalysis.txt` (7.5 KB, banked
2026-10-28) — section-divider slide; badge "2" top-right; two centered red lines
"Revision of" / "Perceptron Algorithm"; no other text, no equations, no graphs, no tables.
Wave-1 doc-parse section above left unchanged.

**Search transport note**: `agy -p` CLI calls for this slide succeeded (perceptron rule +
Novikoff; Minsky/Papert XOR limits) before the agent-side quota hit HTTP 429 "Individual
quota reached" (resets ~154h); two further searches ran through the agy MCP web-search
tool (same Google grounding via the antigravity proxy, redirect URLs resolved). Every URL
below was returned by the search service — none invented.

### Slide content summary

Title-only divider introducing a recap of the Perceptron algorithm. There is no printed
math on the frame; the slide's technical content is what "Revision of Perceptron
Algorithm" announces. Verification therefore targets that concept set: the Rosenblatt
perceptron and its error-correction rule, the convergence theorem, and the classic
limitation that motivates multi-layer networks.

### Claim-by-claim verification

| # | Claim (concept announced by the frame) | Verdict | Wave-3 evidence |
|---|---|---|---|
| 1 | The Perceptron is Rosenblatt's single-layer binary classifier; model ŷ = f(w·x + b) with a step activation; weights w, bias b | CONFIRMED | Rosenblatt 1958, "The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain", Psychological Review 65(6):386–408 [[1]](https://doi.org/10.1037/h0042519); Cornell CS4780 lecture notes [[2]](https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html) |
| 2 | Error-correction learning rule: on a misclassified sample w(k+1) = w(k) + η·y·x; no update when correctly classified; η often = 1 in the theory | CONFIRMED | UPenn CIS5190 linear-classification/perceptron notes [[3]](https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf); Columbia COMS 4771 convergence proof [[4]](https://www.cs.columbia.edu/~mcollins/courses/6998-2012/notes/perc.converge.pdf); MIT/CMU 10-601 perceptron slides [[5]](https://www.cs.cmu.edu/~mgormley/courses/10601bd-f18/slides/lecture6-perc.pdf) |
| 3 | Perceptron Convergence Theorem (Novikoff 1962): if the data is linearly separable the algorithm converges in a finite number of updates, with mistake bound k ≤ (R/γ)² | CONFIRMED | Novikoff, "On convergence proofs on perceptrons", Proc. Symp. Mathematical Theory of Automata, Polytechnic Institute of Brooklyn, Vol. XII, 615–622, 1962 [[6]](https://dblp.org/rec/conf/automata/Novikoff62.html); Stanford CS229 perceptron notes [[7]](https://cs229.stanford.edu/notes2023fall/cs229-notes_perceptrons.pdf); Oregon State convergence lecture [[8]](https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2024fall/unit2/convergence.html); Math StackExchange proof sketch [[9]](https://math.stackexchange.com/questions/2183227/novikoff-s-proof-for-perceptron-convergence) |
| 4 | Single-layer perceptron cannot compute XOR (non-linearly separable) — Minsky & Papert 1969 | CONFIRMED | Minsky & Papert, *Perceptrons* (MIT Press, 1969) [[10]](https://doi.org/10.7551/mitpress/11301.001.0001); Wikipedia summary [[11]](https://en.wikipedia.org/wiki/Perceptrons_(book)); chapter walk-through [[12]](https://bnaskrecki.faculty.wmi.amu.edu.pl/nnets/_build/html/part3_limitations/ch09_minsky_papert.html) |
| 5 | The 1969 result contributed to the first "AI Winter"; multi-layer nets + backpropagation (Rumelhart, Hinton & Williams 1986) were the way forward | CONFIRMED | Backpropagation paper, *Nature* 323:533–536 (1986) [[13]](https://www.nature.com/articles/323533a0); AI-Winter account [[14]](https://xorit.ru/en/journal/minsky-rosenblatt-and-the-perceptron-how-the-book-perceptrons-influenced-the-ai-winter/) |
| 6 | The perceptron survives today as the artificial neuron / building block of deep networks (affine combination + activation; dense layers are banks of them) | CONFIRMED | Goodfellow, Bengio & Courville, *Deep Learning*, Ch. 6 (Deep Feedforward Networks) [[15]](https://www.deeplearningbook.org/contents/mlp.html); universal approximation background (Cybenko 1989) [[16]](https://doi.org/10.1007/BF02551274) |

**DATA-level clarification (not printed on the frame)**: the classic perceptron rule is
written with a **plus** sign, w ← w + η·y·x. Slides 003-004 of this lecture reach the same
rule through a gradient-descent form written with a **minus** sign, w_new = w_old − η·δ_i·x_i,
where δ_i is defined with the opposite sign convention (−1 for a class-I point
misclassified as class II). The two forms are algebraically identical; see slide_004
sources. Useful for slide notes; NOT printed on this frame.

### Wave-3 sources banked (new this wave)
1. https://doi.org/10.1037/h0042519
2. https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html
3. https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf
4. https://www.cs.columbia.edu/~mcollins/courses/6998-2012/notes/perc.converge.pdf
5. https://www.cs.cmu.edu/~mgormley/courses/10601bd-f18/slides/lecture6-perc.pdf
6. https://dblp.org/rec/conf/automata/Novikoff62.html
7. https://cs229.stanford.edu/notes2023fall/cs229-notes_perceptrons.pdf
8. https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2024fall/unit2/convergence.html
9. https://math.stackexchange.com/questions/2183227/novikoff-s-proof-for-perceptron-convergence
10. https://doi.org/10.7551/mitpress/11301.001.0001
11. https://en.wikipedia.org/wiki/Perceptrons_(book)
12. https://bnaskrecki.faculty.wmi.amu.edu.pl/nnets/_build/html/part3_limitations/ch09_minsky_papert.html
13. https://www.nature.com/articles/323533a0
14. https://xorit.ru/en/journal/minsky-rosenblatt-and-the-perceptron-how-the-book-perceptrons-influenced-the-ai-winter/
15. https://www.deeplearningbook.org/contents/mlp.html
16. https://doi.org/10.1007/BF02551274

### Uncertain items (marked [?])
- None — the frame carries only a title and the badge; all verified concepts are the
  announced review topic, not printed frame text.

---

## Verified 2026-10-30 (wave 4, `src_w4_001_004`)

Fresh independent re-verification pass. Wave-1 and wave-3 sections above are left untouched.

**Transport note**: `agy -p` CLI was quota-blocked this wave (HTTP 429 `RESOURCE_EXHAUSTED /
Individual quota reached`, resets ~131h). Searches ran through the **agy MCP web-search tool** — the
same Google grounding via the antigravity proxy with redirect URLs resolved. Every URL below was
returned by the search service; none invented. Unlike slide 001, several non-SPA academic pages
were **fetched live and returned full content** — marked "live-fetched".

Full register: `sources/slide_002_source/VERIFY_W4.md`.

### Claim → question → answer → citation

1. **The Perceptron is Rosenblatt's single-layer binary classifier.**
   *Question:* Is "Perceptron Algorithm" the Rosenblatt model, and what is the primary paper?
   *Answer:* Yes — Frank Rosenblatt, "The Perceptron: A Probabilistic Model for Information Storage
   and Organization in the Brain", *Psychological Review* 65(6):386–408 (1958), doi:10.1037/h0042519,
   PMID 13602029 — the paper that introduced the perceptron as the first computational model of an
   artificial neural network capable of learning from experience.
   *Citation:* https://en.wikipedia.org/wiki/Perceptrons_(book) (live-fetched; carries the full
   bibliographic citation) ; https://pubmed.ncbi.nlm.nih.gov/13602029/ ;
   https://homepages.math.uic.edu/~lreyzin/papers/rosenblatt58.pdf (search-resolved; direct fetch
   failed to extract — recorded as unextracted, not invalid)
   *Status:* **CONFIRMED**. Frame text unchanged.

2. **Model ŷ = f(w·x + b) with a step/sign activation; weights w, bias b.**
   *Question:* What is the classifier form, and is the bias absorbable into the weight vector?
   *Answer:* "h(x_i) = sign(wᵀx_i + b)", y_i ∈ {−1,+1}; the notes state "we 'absorb' it into the
   feature vector w by adding one additional constant dimension", giving h(x_i) = sign(wᵀx).
   *Citation:* https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html
   (live-fetched)
   *Status:* **CONFIRMED**. Frame text unchanged.

3. **Error-correction learning rule: on a misclassified sample w ← w + η·y·x; no update when
   correctly classified; η = learning rate.**
   *Question:* What is the update rule and when does it fire?
   *Answer:* "If y_n ŷ_n = −1, β̂ ← β̂ + η·y_n x_n" — the update fires **only** on misclassified
   samples; "an observation is correctly classified if y_n ŷ_n = 1 and misclassified if y_n ŷ_n = −1".
   *Citation:* https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html (live-fetched) ;
   https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched:
   "y_i(wᵀx_i) > 0 ⟺ x_i is classified correctly")
   *Status:* **CONFIRMED**. Frame text unchanged.

4. **Perceptron Convergence Theorem (Novikoff 1962): linearly separable data ⇒ convergence in a
   finite number of updates; mistake bound k ≤ R²/δ² (≡ M ≤ 1/γ² under unit-radius normalization).**
   *Question:* Who proved the theorem, under what hypothesis, and what is the bound?
   *Answer:* "While the perceptron algorithm was invented by Rosenblatt, this theorem and its proof
   were from NYU mathematician Albert B. J. Novikoff in 1962." If the training set is linearly
   separable with margin δ, the perceptron "must converge to a linear separator after at most R²/δ²
   mistakes (updates) where R = max ‖x‖"; the Cornell version gives "at most 1/γ² mistakes" with
   ‖x‖ ≤ 1. The bound is independent of dimensionality, of dataset size, and of cycling order, and
   scales quadratically with separation difficulty.
   *Citation:* https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2024fall/unit2/convergence.html
   (live-fetched) ; https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html
   (live-fetched) ; primary paper scan: https://cs.uwaterloo.ca/~y328yu/classics/novikoff.pdf ;
   proof sketch: https://math.stackexchange.com/questions/2183227/novikoff-s-proof-for-perceptron-convergence
   *Status:* **CONFIRMED**. Frame text unchanged.

5. **Single-layer perceptron cannot compute XOR (non-linearly separable) — Minsky & Papert 1969.**
   *Question:* What did *Perceptrons* (1969) prove, and which predicate is the canonical example?
   *Answer:* *Perceptrons: An Introduction to Computational Geometry*, Minsky & Papert, published 1969;
   "the most important one is related to the computation of some predicates, such as the XOR
   function", and the single-layer perceptron cannot compute parity under conjunctive localness
   (Theorem 3.1.1). The Cornell notes' history section cites "the XOR problem (Minsky 1969)" as the
   canonical non-linearly separable example.
   *Citation:* https://en.wikipedia.org/wiki/Perceptrons_(book) (live-fetched) ;
   https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched)
   *Status:* **CONFIRMED**. Frame text unchanged.

6. **The 1969 limitation contributed to the first "AI Winter"; multi-layer nets + backpropagation
   (Rumelhart, Hinton & Williams 1986) were the way forward.**
   *Question:* What was the historical consequence of the 1969 result?
   *Answer:* The book "is the center of a long-standing controversy … pessimistic predictions made
   by the authors were responsible for a change in the direction of research in AI, concentrating
   efforts on so-called 'symbolic' systems, a line of research that petered out and contributed to
   the so-called AI winter of the 1980s"; Cornell: "Then, contributed to the A.I. Winter."
   *Citation:* https://en.wikipedia.org/wiki/Perceptrons_(book) (live-fetched) ;
   https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html (live-fetched)
   *Status:* **CONFIRMED**. Frame text unchanged.

### Doc-parse corroboration

`sources/docparse_cascades/slide_002/composed/slide_002_composed.md` (nemotron-3.5-parse,
degraded: False, 2 elements, 0 failed calls) independently reads exactly two elements: the badge
"2" and the section header "Revision of Perceptron Algorithm". This corroborates the analysis
JSON's `subtitle_or_header: null`, empty `bullets`/`equations`, and its deliberate documentation of
the absence rather than fabrication of body content. **No analysis correction was required.**

### Corrections to the analysis record

**None.** No factual or DATA claim in `analysis/slide_002_final.json` was contradicted by any
source; nothing was patched. All verified items are the announced review topic, not printed frame
text.

### Law reminder

The frame wins for recreation; the source wins for understanding.
