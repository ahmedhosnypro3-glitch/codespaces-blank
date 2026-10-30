# agy wave-3 evidence notes — slide_028 (Neural Network Model)

Date: 2026-10-30. Agent: src-025-028.
Transport note: `agy -p` CLI is per-user quota-blocked (HTTP 429; attempt
logged in `cli_attempt_01.txt`). Wave-3 searches ran through the agy
web-search MCP (same Google grounding); URLs below are exactly those returned,
none invented.

## Queries run (3)
1. Origin of the classical notation Net_i = sum_j w_ji O_j + b_i (w_ji = weight
   from neuron j to neuron i), O_i = f(Net_i), one output per class.
2. Haykin "Neural Networks: A Comprehensive Foundation" notation: net_j =
   sum_i w_ji x_i + b_j, output o_j = phi(net_j), weight convention
   "to neuron j, from neuron i", m hidden + n output neurons.
3. How neural-network model diagrams are drawn: neuron circle containing Sigma
   then sigma activation, weights w_ji on edges, one output neuron per class
   with class labels, error computed against the target label.

## Findings (confirm the slide's diagram labels)
- `w_ji` subscript convention = "to neuron i/j (current), from neuron j/i
  (previous)" — destination-first indexing, classical connectionist/Haykin
  style. The frame's `w_ji` between layers i and j matches this.
- Neuron anatomy: Net_i = sum_j w_ji * O_j + b_i (weighted sum + bias),
  O_i = f(Net_i) — the frame's circles containing `Σ` (and `σ`) are exactly
  this two-step computation (sum then activation).
- Layer semantics: I/P layer = pass-through (frame: "Previous Layer");
  hidden layer(s) = where weighted-sum + activation happens (frame: "Current
  Layer (You are here)"); O/P layer = one output per class (frame: "Output 1..m"
  paired with "Class 1..m"), classification with m classes.
- Supervised training: each Input Sample is paired with a Target Label (frame's
  top boxes); error = Loss(output, target) (frame's "Error" bar) drives
  backpropagation.
- Notation lineage: Rumelhart/Hinton/Williams 1986 backpropagation papers and
  1990s textbooks (Haykin 1994; Zurada 1992; Hagan/Demuth/Beale 1996).

## Sources (URLs returned by the agy web-search MCP)
- https://yudiagusta.wordpress.com/2008/10/09/artificial-neural-networks/
- https://people.engr.tamu.edu/choe/choe/courses/08spring/lectures/slide04.pdf
- https://blog.gopenai.com/introduction-to-neural-networks-sigmoid-neurons-ce374d71aae3
- https://ml-cheatsheet.readthedocs.io/en/latest/nn_concepts.html
- https://cs230.stanford.edu/files/Notation.pdf
- https://mallahyari.github.io/ml_tutorial/neural_network/
- https://medium.com/data-science/sigmoid-neuron-deep-neural-networks-a4cd35b629d7
- https://people.cs.pitt.edu/~xianeizhang/notes/NN/NN.html
- https://towardsdatascience.com/understanding-neural-networks-19020b758230/
