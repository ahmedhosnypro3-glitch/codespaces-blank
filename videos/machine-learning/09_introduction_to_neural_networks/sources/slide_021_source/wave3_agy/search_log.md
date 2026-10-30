# wave-3 raw search log — slide_021

Date: 2026-10-30 · Agent: src-021-024

## Tool note

`agy -p "<query>"` was attempted first for every query and returned HTTP 429
`RESOURCE_EXHAUSTED` ("Individual quota reached. Please upgrade your subscription to increase
your limits. Resets in 154h22m20s."). Raw CLI error files: `q1_prelu.txt`, `q2_elu.txt`,
`q3_softplus.txt`. Searches were therefore executed through the **agy MCP web-search tool**
(same Google grounding backend; grounding redirect URLs resolved to real page URLs).

## Queries run (4)

1. `Parametric ReLU (PReLU) activation function definition f(x) = x for x>0, alpha*x for x<=0,
   multiple alpha curves 0.1 0.2 0.5 1.0, He et al. 2015 arXiv 1502.01852 "Delving Deep into
   Rectifiers"`
   → https://arxiv.org/abs/1502.01852, https://en.wikipedia.org/wiki/Rectified_linear_unit,
   https://medium.com/@shauryagoel/prelu-activation-e294bb21fefa,
   https://www.emergentmind.com/topics/parametric-rectified-linear-unit-prelu
2. `ELU Exponential Linear Unit activation definition f(x) = alpha*(e^x - 1) for x<0, x for x>=0,
   alpha typically 1, asymptote -alpha, Clevert 1511.07289`
   → https://arxiv.org/abs/1511.07289,
   https://www.geeksforgeeks.org/deep-learning/elu-activation-function-in-neural-network/,
   https://tungmphung.com/elu-activation-a-comprehensive-analysis/,
   https://closeheat.com/blog/elu-activation-function
3. `Softplus activation function definition softplus(x) = ln(1 + e^x), smooth approximation of
   ReLU, value at x=0 is ln 2, derivative is sigmoid`
   → https://www.geeksforgeeks.org/deep-learning/softplus-function-in-neural-network/,
   https://www.datacamp.com/tutorial/softplus,
   https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.activation.Softplus.html,
   https://www.neura.market/directories/chatgpt/blog/softplus-activation-function-the-smooth-powerful-relu-alternative-every-ml-engineer-needs
4. `ReLU rectified linear unit definition f(x) = max(0, x) piecewise 0 for x<0 x for x>=0 graph
   hockey stick ramp Wikipedia`
   → https://en.wikipedia.org/wiki/Rectified_linear_unit,
   https://builtin.com/machine-learning/relu-activation-function,
   https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks/,
   https://hyper.ai/en/wiki/3604, https://www.dremio.com/wiki/relu-activation-function/,
   https://www.kaggle.com/getting-started/281209

All URLs above were returned by the search tool; none were constructed by hand.
