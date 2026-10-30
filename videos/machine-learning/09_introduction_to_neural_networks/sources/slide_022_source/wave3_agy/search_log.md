# wave-3 raw search log — slide_022

Date: 2026-10-30 · Agent: src-021-024

## Tool note

`agy -p "<query>"` was attempted first and returned HTTP 429 `RESOURCE_EXHAUSTED` (quota
exhausted, reset ~154h). Searches were therefore executed through the **agy MCP web-search tool**
(same Google grounding backend; grounding redirect URLs resolved to real page URLs).

## Queries run (4)

1. `derivative of ELU activation function piecewise f'(x) = alpha*e^x for x<0 equals f(x)+alpha,
   1 for x>=0, proof why f(x)+alpha form is used in backpropagation`
   → https://arxiv.org/html/1704.07483v1,
   https://serengil.wordpress.com/2018/01/02/elu-as-a-neural-networks-activation-function/
2. `softplus derivative d/dx ln(1+e^x) = e^x/(1+e^x) = 1/(1+e^-x) = sigmoid(x) derivation step by
   step`
   → https://www.analyticsvidhya.com/blog/2025/12/softplus-activation-function/,
   https://www.datacamp.com/tutorial/softplus
3. `PReLU parametric ReLU derivative f'(x) = alpha for x<0 and 1 for x>=0, also gradient with
   respect to alpha df/dalpha = x for x<0, backpropagation He 2015`
   → https://arxiv.org/abs/1502.01852,
   https://www.microsoft.com/en-us/research/publication/delving-deep-into-rectifiers-surpassing-human-level-performance-on-imagenet-classification/
4. `dying ReLU problem derivative zero for negative inputs dead neurons, motivation for Leaky ReLU
   PReLU ELU with nonzero negative gradient`
   → https://towardsdatascience.com/the-dying-relu-problem-clearly-explained-42d0c54e0d24/,
   https://datascience.stackexchange.com/questions/5706/what-is-the-dying-relu-problem-in-neural-networks,
   https://medium.com/@MrBam44/the-dying-relu-problem-causes-and-solutions-1a970f177c,
   https://apxml.com/courses/introduction-to-deep-learning/chapter-2-activation-functions-architecture/relu-variants

All URLs above were returned by the search tool; none were constructed by hand.
