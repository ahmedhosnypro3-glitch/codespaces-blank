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
