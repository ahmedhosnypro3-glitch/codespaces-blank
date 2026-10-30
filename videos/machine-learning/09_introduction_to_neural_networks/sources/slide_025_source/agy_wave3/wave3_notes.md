# agy wave-3 evidence notes — slide_025 (Linear and Unit Step Activation Functions)

Date: 2026-10-30. Agent: src-025-028.
Transport note: `agy -p` CLI succeeded for 3 queries (raw transcripts in
`search_01_linear_and_step.txt`, `search_02_bipolar_step.txt`,
`search_03_step_not_differentiable.txt`; these CLI answers carry no inline
citation URLs). A 4th CLI query hit per-user quota HTTP 429
(`search_04_history.txt` = the 429 error). Remaining queries ran through the
agy web-search MCP (same Google grounding service), which returns grounded
citations; URLs below are exactly those returned, none invented.

## Queries run
1. CLI: linear identity activation f(x)=x and binary step (Heaviside) threshold canonical formulas and ranges.
2. CLI: bipolar step / signum activation: -1 for x<0, +1 for x>=0, zero-centered, perceptron learning rule.
3. CLI: why step activations cannot be trained with backpropagation (derivative zero a.e., undefined at threshold).
4. MCP: canonical bipolar step/signum definition, range {-1,+1}, zero-centered encoding rationale.
5. MCP: why binary step breaks backpropagation (chain-rule collapse), motivating sigmoid/tanh/ReLU.
6. MCP: McCulloch-Pitts (1943) and Rosenblatt perceptron (1958) threshold-activation history, unipolar {0,1} vs bipolar {-1,+1}.

## Findings (all confirm the slide's verbatim equations)
- Linear/identity: f(x) = x, range (-inf,+inf), f'(x) = 1; stacking identity layers
  collapses to one linear map; used in regression output layers.
- Unipolar (binary/Heaviside) step: f(x) = 1 if x >= 0 else 0; range {0,1};
  derivative 0 for x != 0 and undefined at x = 0 -> no gradient for backpropagation.
- Bipolar step (signum): f(x) = +1 if x >= 0, -1 if x < 0; range {-1,+1};
  zero-centered -> mixed-sign gradients, balanced updates, faster convergence.
  This confirms the frame's `Bi-polar Unit Step = -1 for x<0, 1 for x>=0`
  (wave-1 OCR had rendered the -1 as 1; wave-2 and wave-3 sources agree on -1).
- Historical: McCulloch-Pitts neuron (1943) used unipolar {0,1} with fixed weights;
  Rosenblatt's perceptron (1958) learned weights with a hard-limiter step
  (0/1 or -1/+1). Perceptron update: w <- w + eta*y*x for y in {-1,+1}.

## Sources (URLs returned by the agy web-search MCP)
- https://www.analyticsvidhya.com/blog/2022/01/activation-functions-for-neural-networks-and-their-implementation-in-python/
- https://mohitmishra786687.medium.com/activation-functions-in-neural-networks-56dc526ad63c
- https://www.guvi.in/blog/bipolar-sigmoid-function-in-neural-networks/
- https://www.datacamp.com/tutorial/introduction-to-activation-functions-in-neural-networks
- https://adl1995.github.io/an-overview-of-activation-functions-used-in-neural-networks.html
- https://ai.stackexchange.com/questions/48981/why-function-of-a-neuron-need-to-be-in-range-1-1-or-0-1
- https://datascience.stackexchange.com/questions/28037/backpropagation-with-step-or-threshold-activation-function
- https://iq.opengenus.org/binary-step-function/
- https://en.wikipedia.org/wiki/Backpropagation
- https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
- https://blog.devops.dev/exploring-activation-functions-in-deep-learning-properties-derivatives-and-impact-on-model-7585aad8a757
- https://medium.com/@lmpo/the-evolution-of-artificial-neurons-90619f224f63
- https://mbrenndoerfer.com/writing/history-perceptron-neural-network-foundation
- https://machinelearning.uchicago.edu/history/
- https://com-cog-book.github.io/com-cog-book/features/perceptron.html
- https://home.csulb.edu/~cwallis/artificialn/History.htm
- https://www.cs.ucdavis.edu/~vemuri/classes/ecs170/neuralnets_files/neural-networks.htm
- https://en.wikipedia.org/wiki/Perceptron
- https://www.pearsonhighered.com/assets/samplechapter/0/1/3/1/0131471392.pdf
