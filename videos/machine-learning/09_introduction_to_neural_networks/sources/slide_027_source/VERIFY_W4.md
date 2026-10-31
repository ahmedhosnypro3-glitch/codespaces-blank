# VERIFY_W4.md — slide_027 (wave 4, 2026-10-30)

**Scope**: `src_w4_025_028` · worker `w4-src-025` · sink deck `machine-learning/09_introduction_to_neural_networks`
**Analysis spec used**: `analysis/slide_027_final.json` (vision `images`, validated `validate_slides`, verdict PASS_WITH_FIXES, recreatability 9/10)
**Independent second read**: `sources/docparse_cascades/slide_027/composed/slide_027_composed.md` (frame md5 `1a43f3e516807fe6f191433c5a5b6996`) — only 2 positioned elements kept (badge + title/subtitle)
**Search transport**: `agy -p` CLI quota-exhausted (HTTP 429, resets ~131h); queries ran through the **agy web-search MCP** route. Every URL is search-returned; none invented.

## IMPORTANT correction to the banked Wave-1 SOURCES.md (enrichment, not a source change)

The Wave-1 `SOURCES.md` for this slide was written **before** vision analysis existed and *hypothesised* that the frame's "main content is a network architecture diagram". The validated analysis record (`slide_027_final.json`, `validation.verdict = PASS_WITH_FIXES`, recreatability 9/10) and the doc-parse transcript both say otherwise:

- `slide_027_final.json`: `verbatim_text.bullets` is genuinely empty; `imagery` is genuinely empty; the recreation brief's final step is "add no bullets, no images, and no animations; the slide is static".
- `slide_027_composed.md`: exactly 2 positioned elements — `<class_Page-header>` (badge `27`) and `<class_Title>` containing `**Multi-Layer Neural Network** **The complete Picture**`. Zero crops, zero failed calls, no unpositioned text, no picture/figure class at all.

So slide 027 is a **title-only section divider** ("the complete picture" of a multi-layer neural network), not a diagram slide. The **frame is ground truth**, and the frame shows no diagram — a builder must NOT invent one. The MLP facts below are verified as the *conceptual backdrop* this divider announces; they belong to the diagram that slide 028 actually carries. No frame text changes.

## Claim register

| # | Claim (DATA-level) | Status | Evidence / URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | The slide is a title-only divider: "Multi-Layer Neural Network" + subtitle "The complete Picture", badge 27, thin red frame, black bottom bar, light gray bg | CONFIRMED (frame-level; not a web claim) | Two independent reads agree: `slide_027_final.json` (empty bullets, empty imagery, "the slide is static") + `sources/docparse_cascades/slide_027/composed/slide_027_composed.md` (2 elements only) | none — records the correction of the Wave-1 diagram hypothesis |
| 2 | "Multi-layer" neural network = a network with at least one hidden layer between input and output | CONFIRMED | "Multi-layer Perceptron … input layer … one or more hidden layers … output layer" — https://en.wikipedia.org/wiki/Multilayer_perceptron ; https://www.teach.cs.toronto.edu/~csc311notes/neural_networks/multi_layer_perceptron.html ; https://www.geeksforgeeks.org/deep-learning/layers-in-artificial-neural-networks-ann/ | none — context for the divider's claim |
| 3 | Input layer performs no computation — pure pass-through | CONFIRMED | "No computations or transformations happen here. The input layer simply performs a pass-through function … a_i^[0] = x_i" — https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html ; https://pub.towardsai.net/the-multilayer-perceptron-built-and-implemented-from-scratch-70d6b30f1964 | none |
| 4 | Each hidden neuron computes a weighted sum plus bias then applies an activation: z = Σ(w·x) + b → a = f(z) | CONFIRMED | "Each neuron computes the linear combination of its inputs, adding a learnable bias term: z_j = Σ_i (w_ji · a_i) + b_j … then passed through a non-linear activation function" — https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html ; https://www.datacamp.com/tutorial/multilayer-perceptrons-in-machine-learning ; https://www.geeksforgeeks.org/deep-learning/multi-layer-perceptron-learning-in-tensorflow/ | none |
| 5 | The "complete picture" = feedforward flow, one or more hidden layers, learned weights/biases via backpropagation | CONFIRMED | "Weights & biases learned via backpropagation; feedforward flow left-to-right, no cycles" + MLP layer role breakdown — https://www.teach.cs.toronto.edu/~csc311notes/neural_networks/multi_layer_perceptron.html ; https://www.datacamp.com/tutorial/multilayer-perceptrons-in-machine-learning ; https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers | none |
| 6 | Output layer: for classification, one output neuron per class | CONFIRMED | "For a classification target, the output layer typically features one neuron per class (e.g. 10 neurons for a 10-class dataset like MNIST) … Multi-Class uses C neurons with Softmax" — https://ml-iitr.vlabs.ac.in/exp/multi-layer-perceptron/theory.html | none — consistent with slide 028's Output 1/2/m ↔ Class 1/2/m |
| 7 | Frame styling: #E8E8E8 background, #C00000 title/subtitle, #FFD966 badge with #800080 outline | CONFIRMED as house-rule values, not web claims | House frame rule (project AGENTS.md): light-gray bg, red frame, yellow badge. The spec's #E8E8E8/#C00000/#FFD966/#800080 are frame reads; sources never license restyling | none |
| 8 | Text cursor near "Picture" is a video artifact | CONFIRMED (spec-level) | Spec `animation_state` explicitly excludes it: "a text cursor visible near the word 'Picture' … is a video/editing artifact and must not be recreated" | none |

## Questions asked (all via agy web-search MCP)

1. "multilayer perceptron complete architecture: input layer pass-through, hidden layers compute weighted sum plus bias then activation, output layer one neuron per class classification target label ground truth error comparison"
2. "neural network notation net input of neuron net_i = Σ_j w_ji x_j + b_i … activation output o_i = f(net_i)" (run for slide 028; also corroborates 027's layer-math claim 4)
3. "neural network neuron symbol convention: sigma summation symbol for weighted sum junction and activation function symbol inside neuron circle (Haykin style model)" (slide-028 query; corroborates 027's background claim)

## Doc-parse cross-check

`sources/docparse_cascades/slide_027/composed/slide_027_composed.md` is the decisive independent read: it kept only the badge and the title element, **found no picture or figure class**, and reported 0 crops / 0 failed calls — i.e. the parser had nothing further to extract. That corroborates the "title-only divider" finding and contradicts the Wave-1 diagram hypothesis. The doc-parse's md5 matches the frame the vision analysis read (`1a43f3e516807fe6f191433c5a5b6996`).

## Net effect on the analysis spec

**0 changes to the JSON.** The spec already describes this correctly. The substantive output of this slide is the **correction of the banked Wave-1 SOURCES.md hypothesis** (a diagram was assumed; the frame shows a divider) — recorded here and in the appended SOURCES.md section, so a future builder does not "enrich" the slide with an invented MLP diagram. All `[?]` items from Wave-1 about diagram content (node counts, multiple hidden layers, weight/bias annotations, colors, equations) are **retired** — they are now known to be moot because the frame has no diagram.
