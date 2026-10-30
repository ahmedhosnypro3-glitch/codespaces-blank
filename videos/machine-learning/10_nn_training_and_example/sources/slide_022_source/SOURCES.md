# Source Research — slide_022 (Back Propagation Training Algorithm)

## Query
backpropagation training algorithm equations delta weight update O_j(1-O_j)(t_j-O_j) neural network

## Verified Equations (Confirmed by Multiple Sources)

### Output Layer Delta (δ_j)
$$\delta_j = O_j(1 - O_j)(t_j - O_j)$$

Where:
- $O_j$ = predicted output of neuron j (sigmoid activation)
- $t_j$ = target/true value for neuron j
- Matches slide exactly: $\delta_j = O_j(1-O_j)(t_j-O_j)$

### Weight Update (Δw_ji)
$$\Delta w_{ji} = \eta \cdot \delta_j \cdot O_i$$
$$\Delta w_{ji} = \eta \cdot O_j(1-O_j)(t_j-O_j) \cdot O_i$$

Where:
- $\eta$ = learning rate
- $O_i$ = output from previous layer neuron i
- Matches slide: $\Delta w_{ji} = \eta O_i O_j(1-O_j) (t_j-O_j)$

### Hidden Layer Delta (δ_j)
$$\delta_j = O_j(1 - O_j) \sum_k (\delta_k w_{kj})$$

Matches slide: $\delta_j = O_j(1-O_j) [\Sigma_k (\delta_k w_{kj})]$

## Sources
1. [Medium - Backpropagation](https://medium.com/@jorgesleonel/backpropagation-cc81e9c772fd) — derives δ_j and weight update
2. [Scribd - Gradient Descent & Back-Propagation](https://www.scribd.com/document/881286643/Gradient-Descent-Algorithm-and-Back-Propagation-Derivation)
3. [KrishnaIK - Backpropagation Tutorial](https://www.krishnaik.in/ai-tutorials/deep-learning/backpropagation)
4. [Towards Data Science - Backpropagation](https://towardsdatascience.com/neural-networks-backpropagation-by-dr-lihi-gur-arie-27be67d8fdce/)
5. [MartinLWX - Backpropagation Tutorial](https://martinlwx.github.io/en/backpropagation-tutorial/)

## Notes
- All equations on slide_022 are **verified correct** for standard backpropagation with sigmoid activation
- The slide uses $O$ for output (not $y$ or $a$) — consistent with some textbook conventions
- $\eta$ (eta) is the learning rate symbol used on the slide
- Subscript notation: $w_{ji}$ means weight from i to j (consistent with slide)