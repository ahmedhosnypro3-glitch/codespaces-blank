# Slide 002 — Neural Network Model diagram (node = summation + activation; layer topology; classification outputs)

Frame facts (from `analysis/parse/slide_002.parse.md`, data only): title "Neural Network Model
(Each node consists of Summation + Activation)"; "Input Sample"; "Target Label"; node net
labels "Net_i / Net_j / Net_k"; output classes "Class 1, Class 2, ..., Class m";
"Previous Layer Layer (i) / Current Layer (You are here) / Next Layer Layer (k)".
Method: agy web search (best-effort), diagram conventions checked against architecture guides.

## Sources

- Codecademy — "Introduction to Neural Network Architectures (cheatsheet)" (https://www.codecademy.com/learn/learn-neural-network-architectures/modules/introduction-to-neural-network-architectures/cheatsheet) — confirms the previous/current/next layer convention (layers l−1, l, l+1) and node/weight indexing the slide uses.
- H2O.ai — "Neural Network Architectures" (https://h2o.ai/wiki/neural-network-architectures) — confirms input layer receives the input sample, intermediate layers transform it feedforward, output layer emits per-class responses.
- Conceptviz — "How to draw a neural network architecture diagram" (https://conceptviz.app/blog/how-to-draw-neural-network-architecture-diagram-guide) — confirms the canonical layout: input sample → hidden/current layer → output classes, with the target label used to compute the loss.
- Scaler — "Neural Network Architecture: How It Works" (https://www.scaler.com/blog/neural-network-architecture-how-it-works/) — confirms that a single node computes a weighted sum then applies an activation, i.e. the slide's "Summation + Activation".

## Corrections / notes

- "Each node consists of Summation + Activation" — CONFIRMED: the canonical neuron model (net input → activation function), as documented by all four sources.
- Layer labels "Previous Layer Layer (i) / Current Layer / Next Layer Layer (k)" — CONFIRMED as standard (l−1, l, l+1) with per-node index letters; the slide's "(You are here)" and repeated "Class 1" line are course-authored pedagogy, not source text — do not normalize.
- Node labels "Net_i / Net_j / Net_k" — CONFIRMED naming convention for the pre-activation net input of nodes indexed i, j, k; consistent with slide 003's `Net_j`.
- "Class 1 … Class m" — CONFIRMED as the output layer of a classification network (one output per class; standard implementations apply softmax/sigmoid there — the slide itself uses sigmoid per slide 3).
- No numeric data on the slide (generic m-class diagram), so no dataset verification applies.
