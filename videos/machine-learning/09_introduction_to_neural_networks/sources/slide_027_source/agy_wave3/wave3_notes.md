# agy wave-3 evidence notes — slide_027 (Multi-Layer Neural Network / The complete Picture)

Date: 2026-10-30. Agent: src-025-028.
Transport note: `agy -p` CLI is per-user quota-blocked (HTTP 429; attempt
logged in `cli_attempt_01.txt`). Wave-3 searches ran through the agy
web-search MCP (same Google grounding); URLs below are exactly those returned,
none invented.

## Queries run (2)
1. MLP architecture: input/hidden/output layers; neuron = weighted sum + bias
   then activation; feedforward left-to-right; universal approximation theorem;
   what a "complete picture" diagram of a multi-layer network must show.
2. Multi-layer network diagram components and the role of hidden layers; why a
   diagram subtitled "The Complete Picture" shows the whole forward pass from
   input features to the final prediction.

## Findings (context for the title-only frame)
- Slide 027 is a title-only frame: "Multi-Layer Neural Network" +
  "The complete Picture", badge 27, red frame, black bottom bar. The web
  sources define exactly what "the complete picture" of an MLP means, which is
  the diagram the following slides (028) decompose:
  - Input layer: pass-through, no computation; one node per feature.
  - Hidden layer(s): each neuron computes z = sum(w_i x_i) + b, then
    a = f(z) with a non-linear activation; non-linearity is what makes stacked
    layers more powerful than a single linear map.
  - Output layer: one node per class (classification) or continuous value
    (regression); sigmoid/softmax for classes, linear for regression.
  - Feedforward: information flows strictly left-to-right, no cycles.
  - Universal approximation theorem (Cybenko/Hornik): one hidden layer with a
    non-linear activation can approximate any continuous function on compact
    sets given enough neurons.
  - A "complete picture" diagram shows: labeled layers, node circles with
    explicit dimensionality, directed left-to-right edges with weights,
    bias terms, activation markers inside neurons, and the final output.
- Hidden layers learn hierarchical features (low-level -> abstract), which is
  why they are the "engine room" and the focus ("You are here") in slide 028.

## Sources (URLs returned by the agy web-search MCP)
- https://www.datacamp.com/tutorial/multilayer-perceptrons-in-machine-learning
- https://medium.com/data-science/multilayer-perceptron-explained-a-visual-guide-with-mini-2d-dataset-0ae8100c5d1c
- https://www.scribd.com/document/961087665/Multilayer-Perceptron-Detailed-with-Diagrams
- https://en.wikipedia.org/wiki/Multilayer_perceptron
- http://d2l.ai/chapter_multilayer-perceptrons/mlp.html
- https://medium.com/@nlunge786/a-deep-architecture-multi-layer-perceptron-164bc5ff3842
- https://www.geeksforgeeks.org/deep-learning/multi-layer-perceptron-learning-in-tensorflow/
- https://www.researchgate.net/figure/Architecture-of-Multi-Layer-Perceptron_fig1_364384447
- https://www.geeksforgeeks.org/deep-learning/layers-in-artificial-neural-networks-ann/
- https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/network-layers-overview
- https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2024fall/unit4/multilayer.html
- https://www.youtube.com/watch?v=v2hMdVLZ8-U
- https://www.articsledge.com/post/hidden-layer-neural-network
- https://muneebsa.medium.com/deep-learning-101-lesson-9-multi-layer-neural-network-7cd3a53066c8
- https://www.scribd.com/document/588999995/IML
