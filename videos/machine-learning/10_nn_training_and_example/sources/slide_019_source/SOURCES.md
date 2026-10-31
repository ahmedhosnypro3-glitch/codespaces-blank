# Slide 19 — Backpropagation: Chain Rule Derivation (hidden-node gradient ∂E/∂w_ji)

## Sources

- "Backpropagation", Brilliant wiki — https://brilliant.org/wiki/backpropagation/
  Confirms the summed chain rule exactly as printed: ∂E/∂w_ji = [Σ_k ∂E/∂Net_k · ∂Net_k/∂O_j] · ∂O_j/∂Net_j · ∂Net_j/∂w_ji, and that the Σ_k arises because O_j feeds every node k of the next layer.
- BackPropDeriv, Swarthmore CS81 lecture notes — https://www.cs.swarthmore.edu/~meeden/cs81/s10/BackPropDeriv.pdf
  Confirms all four factor values used on the frame: ∂E/∂Net_k = −δ_k, ∂Net_k/∂O_j = w_kj, ∂O_j/∂Net_j = O_j(1−O_j) (sigmoid derivative), ∂Net_j/∂w_ji = O_i.
- "Derivation of backpropagation" (The Clever Machine) — https://dustinstansbury.github.io/theclevermachine/derivation-backpropagation
  Confirms the same index convention (w_kj connects hidden unit j to downstream unit k; w_ji connects upstream unit i to unit j) and the recursive δ definition.
- Michael Nielsen, "Neural Networks and Deep Learning", Ch. 2 — http://neuralnetworksanddeeplearning.com/chap2.html
  Confirms the equivalent statement δ_j = Σ_k w_kj δ_k^{k+1} · σ'(z_j) — the summed upstream gradient times the activation derivative.
- "Forward and backward propagation in multilayered neural networks" (Medium) — https://medium.com/@jainvidip/forward-and-backward-propagation-in-multilayered-neural-networks-a-deep-dive-d596e875dedf
  Confirms the cause-effect chain the slide lists: w_ji affects Net_j, Net_j affects O_j, O_j affects every Net_k, and those Net_k affect the error.

## Corrections / notes

- Weight subscript read as "w_β" in the certified equations (∂E/∂w_β, ∂Net_j/∂w_β) and as "w_ij" in the two supporting lines. The frame's own derivation consistently targets the weight from node i to node j, so the correct symbol is w_ji (also confirmed by the parse transcript's plain-text body, which prints w_ji). Recreate with w_ji.
- "Net_j = Σ_i w_ij O_j ⇒ ∂Net_j/∂O_j = w_ij" has an index/derivative mismatch on the frame: the weighted sum is Net_j = Σ_i w_ji·O_i, and the derivative that yields a bare weight is ∂Net_k/∂O_j = w_kj (from the NEXT layer's net, not Net_j itself). The intended statement — the factor that makes ∂Net_k/∂O_j equal to the connecting weight — is confirmed correct by the sources.
- One supporting line reads "Net_j = Σ_j w_ij O_j"; the summation index must be i, not j (Net_j = Σ_i w_ji O_i). Same for "∂Net_j/∂w_ij = O_i", which should read ∂Net_j/∂w_ji = O_i.
- The sign convention ∂E/∂Net_k = −δ_k (δ defined as the negative error gradient) is a legitimate textbook variant; it is internally consistent with slide 20's Δw = −η∂E/∂w = ηδ_jO_i. Flag as a convention note, not an error.
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent agy
web-search plus independent algebra; cross-read against `analysis/parse/slide_019.parse.md`
and `analysis/slide_019_final.json` (title "Backpropagation: Chain Rule Derivation").

Questions asked:
1. Is `∂E/∂w_β = [∂E/∂Net_k·∂Net_k/∂O_j]+⋯] · ∂O_j/∂Net_j · ∂Net_j/∂w_β` the correct chain rule?
2. Are the four factor values on the frame correct: `∂E/∂Net_k = −δ_k`,
   `∂Net_k/∂O_j = w_kj`, `∂O_j/∂Net_j = O_j(1−O_j)`, `∂Net_j/∂w_ji = O_i`?
3. Is the frame's "Net_j = Σ_i w_ij O_j ⇒ ∂Net_j/∂O_j = w_ij" line correct as printed?

Answers:
- Q1 **CONFIRMED**. The search independently returns the frame's exact form and explains the
  `Σ_k` sum (the hidden activation `O_j` feeds every next-layer node `k`).
- Q2 **CONFIRMED** (all four). The search's derivation states `∂net_j/∂w_ji = O_i`,
  `∂net_k/∂O_j = w_kj`, `∂O_j/∂net_j = O_j(1−O_j)` for a sigmoid, and `−δ_k` as a standard
  `∂E/∂Net_k` convention.
- Q3 **CONFLICT as printed, correct in intent.** `Net_j = Σ_i w_ji·O_i` (summation index is
  `i`, and the weight is `w_ji`), so `∂Net_j/∂O_j` is not a bare weight. The factor that
  *does* equal a bare weight is `∂Net_k/∂O_j = w_kj`, taken from the NEXT layer's net. The
  existing note already records this; the audit confirms it independently.
- Also confirmed: `∂Net_j/∂w_ij` should read `∂Net_j/∂w_ji`.

Verdicts per claim:
- Chain-rule structure and the `Σ_k` fan-out — **CONFIRMED**.
- `∂E/∂Net_k ⇒ −δ_k` — **CONFIRMED** (a legitimate sign convention; δ = local gradient).
- `Net_k = Σ_k w_kj O_j ⇒ ∂Net_k/∂O_j = w_kj` — **CONFIRMED**.
- `O_j = 1/(1+e^−Net_j) ⇒ ∂O_j/∂Net_j = O_j(1−O_j)` — **CONFIRMED** (sigmoid derivative).
- `Net_j = Σ_i w_ji O_i ⇒ ∂Net_j/∂w_ji = O_i` — **CONFIRMED**.
- Frame line `Net_j = Σ_i w_ij O_j ⇒ ∂Net_j/∂O_j = w_ij` — **CONFLICT** (index/derivative
  mismatch); recreate as `Net_j = Σ_i w_ji O_i ⇒ ∂Net_j/∂w_ji = O_i`.
- `w_β` / `w_ji` symbol mixing in the certified JSON — **CONFLICT** with the frame; use `w_ji`.
- Sign convention consistency with slide 20's `Δw = −η∂E/∂w = ηδ_jO_i` — **CONFIRMED**
  internally consistent (textbook variant, not an error).

New sources found during audit (real URLs, not previously cited):
- Math StackExchange, "Backpropagation hidden layer error" —
  https://math.stackexchange.com/questions/4686558/backpropagation-hidden-layer-error
- MIT OCW 9.641, "Lecture 20: Backprop" —
  https://ocw.mit.edu/courses/9-641j-introduction-to-neural-networks-spring-2005/5d46d3b6e32a5120fe9893193c31e926_lec20_backprop.pdf

Audit summary: every formula the frame prints is standard; the only defects are index typos
inside one printed supporting line, already recorded. No numeric claims on this slide.
