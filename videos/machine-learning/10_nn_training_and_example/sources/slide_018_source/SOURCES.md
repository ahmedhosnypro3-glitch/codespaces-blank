# Slide 18 — Neural Network Diagram (posed question: ∂E/∂w_ji = ?)

## Sources

- "Backpropagation", Brilliant wiki — https://brilliant.org/wiki/backpropagation/
  Confirms the multivariable chain rule the question calls for: ∂E/∂w_ji = Σ_k (∂E/∂Net_k · ∂Net_k/∂O_j) · ∂O_j/∂Net_j · ∂Net_j/∂w_ji, and why the sum over k appears (one hidden node fans out to several downstream nodes).
- BackPropDeriv, Swarthmore CS81 lecture notes — https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf
  Confirms the same decomposition and each factor's value: ∂E/∂Net_k = −δ_k, ∂Net_k/∂O_j = w_kj, ∂O_j/∂Net_j = O_j(1−O_j), ∂Net_j/∂w_ji = O_i.
- "Backpropagation step-by-step derivation" (Towards Data Science) — https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Confirms the equivalent compact result ∂E/∂w_ji = δ_j·O_i with δ_j = (Σ_k δ_k w_kj)·f'(Net_j).
- Michael Nielsen, "Neural Networks and Deep Learning", Ch. 2 — http://neuralnetworksanddeeplearning.com/chap2.html
  Confirms the same derivation in the "two assumptions / four fundamental equations" treatment (Hadamard-weighted δ from the next layer, times σ', times the input activation).

## Corrections / notes

- none found. This is a question slide: the certified spec records only the label "∂E/∂w_ji ?" over the diagram, which matches the sources' statement of the problem. The answer is derived on slides 19–20 and is verified there.
- Diagram geometry (input / hidden / output columns, error feed-back arrows, "Output1/Output2/Output3" labels) is a schematic; sources describe the same architecture. No data-level corrections.
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent agy
web-search (grounded Google search) plus independent recomputation; cross-read against
`analysis/parse/slide_018.parse.md` and `analysis/slide_018_final.json` (`slide_title`
"Neural Network Diagram", labels Input Data / Class 1 / Class 2 / Class m / Error /
Output1 / Output2 / Output3, equation `∂E/∂w_ij ?`).

Questions asked:
1. Is the multivariable chain rule for a hidden weight with a sum over the next layer's
   nodes `k` the standard form of the question this frame poses?
2. Is `w_ji` (upstream `i` → unit `j`) the correct subscript for the asked-about weight?
3. Do the frame's diagram labels (Class m / Error / Output m) have a source analogue?

Answers:
- Q1 CONFIRMED. The search returns the frame's structure verbatim:
  `∂E/∂w_ji = Σ_k ∂E/∂Net_k · ∂Net_k/∂O_j · ∂O_j/∂Net_j · ∂Net_j/∂w_ji`, and explains the
  `Σ_k` arises because one hidden unit's activation fans out to every next-layer node.
- Q2 CONFIRMED as the standard convention (weight from `i` to `j`). BUT the certified
  `slide_018_final.json` prints `∂E/∂w_ij` while the frame's own label (per the parse) is
  `∂E/∂w_ji`. The analysis JSON's index is inverted here; the parse + slides 19/20/21 all
  use `w_ji`. Recorded below.
- Q3 CONFIRMED. Outputs labelled "Class m" feeding a summed "Error" column is the standard
  multiclass-output / summed-error framing the sources use.

Verdicts per claim:
- "Question posed is ∂E/∂w_ji for a hidden weight" — **CONFIRMED** (standard backprop
  problem statement; matches the sources' derivation target).
- Frame label reads `w_ji` — **CONFIRMED** by parse transcript and by the slide-19/20 chain.
- Certified `slide_018_final.json` equation `∂E/∂w_ij ?` — **CONFLICT** with the frame and
  with the sources' `w_ji` convention. The build must print `∂E/∂w_ji`. (Same index error
  already flagged in slide 19's notes; it recurs in 018's JSON.)
- Schematic diagram geometry — **NOT-VERIFIABLE** (course drawing; no source counterpart
  is needed or expected).

New sources found during audit (real URLs, not previously cited):
- Math StackExchange, "Backpropagation hidden layer error" —
  https://math.stackexchange.com/questions/4686558/backpropagation-hidden-layer-error
  States the same four-factor chain rule for a hidden-layer weight.
- MIT OCW 9.641 Intro to Neural Networks, "Lecture 20: Backprop" —
  https://ocw.mit.edu/courses/9-641j-introduction-to-neural-networks-spring-2005/5d46d3b6e32a5120fe9893193c31e926_lec20_backprop.pdf
  Lecture-slide presentation of ∂w_ji = η·δ_j·O_i with the δ definitions this deck uses.

Audit summary: no data-level defects on the frame. One CONFLICT to carry into the build
(the `w_ij` index in the certified JSON).
