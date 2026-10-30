# Source Research for slide_015

## Slide Content (from doc-parse)
- **Slide number**: 15
- **Title**: "Using Two Perceptron Layers with non-Linearity"
- **Subtitle**: "Adding Non-Linearity Solves the XOR Problem"
- **Visual elements**: Network diagram with activation functions
- **XOR Truth Table** shown:
  | X1 | X2 | Output |
  | --- | --- | --- |
  | 0 | 0 | 0 |
  | 0 | 1 | 1 |
  | 1 | 0 | 1 |
  | 1 | 1 | 0 |

## Web Search Findings
**Source**: Multiple sources on MLP and activation functions

**Key facts verified**:
1. **Non-Linear Activation Functions**: The key to solving XOR
   - Sigmoid: σ(x) = 1/(1+e⁻ˣ)
   - Tanh: tanh(x)
   - ReLU: max(0, x)
2. **Hidden Layers + Non-Linearity**: Allows network to learn non-linear decision boundaries
3. **XOR Solution**: Two-layer network with non-linear hidden layer can solve XOR
   - First layer: creates two linear boundaries
   - Non-linearity: bends/warps the space
   - Second layer: combines into XOR decision region

## Slide-Specific Analysis
- This slide shows the solution: two perceptron layers WITH non-linearity
- The XOR truth table is shown as the target problem
- Network diagram likely shows activation functions between layers
- Title explicitly states "Adding Non-Linearity Solves the XOR Problem"
- This is the pedagogical payoff for slides 9-14

## Citations
- [1] GeeksforGeeks: "What is Perceptron - The Simplest Artificial Neural Network"
- [2] Medium: "Perceptron in Deep Learning - Basics & Limitations"
- [5] Educative: "XOR Problem in Neural Network"
- [6] Towards Data Science: "Terribly Perceptive - The Perceptron, The XOR"
- [8] Towards Data Science: "Terribly Perceptive - The Perceptron, The XOR"

## Notes for Analysis
- Visual: network diagram with activation functions (likely sigmoid/ReLU shown)
- XOR truth table as reference
- Title is the key message