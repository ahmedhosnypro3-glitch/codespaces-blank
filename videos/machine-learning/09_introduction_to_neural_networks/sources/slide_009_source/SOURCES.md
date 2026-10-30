# Source Research for slide_009

## Slide Content (from doc-parse)
- **Slide number**: 9 (printed badge)
- **Title**: "Test Single Perceptron with [AND – OR – XOR] Logic (Binary Classification)"
- **Key concepts**: Single Perceptron, AND gate, OR gate, XOR gate, Binary Classification

## Web Search Findings

### Perceptron AND/OR/XOR Logic Gates

**Source**: Multiple sources (Medium, GeeksforGeeks, Educative, etc.)

**Key facts verified**:
1. **Single-Layer Perceptron (SLP)** - Introduced by Frank Rosenblatt (1958), foundational building block of ANNs
2. **Binary Classifier** - Maps inputs to two categories (0/1 or -1/+1) using linear decision boundary
3. **AND Gate** - Linearly separable: outputs 1 only when both inputs are 1
   - Perceptron solution: w1=1, w2=1, b=-1.5 (or -1)
   - Single straight line isolates (1,1) from (0,0), (0,1), (1,0)
4. **OR Gate** - Linearly separable: outputs 1 if at least one input is 1
   - Perceptron solution: w1=1, w2=1, b=-0.5
   - Single straight line separates (0,0) from the rest
5. **XOR Gate** - **NOT linearly separable**: outputs 1 only when inputs differ
   - Cannot be solved by single-layer perceptron
   - No single straight line can separate (0,0)/(1,1) from (0,1)/(1,0)
   - Minsky & Papert (1969) proved this limitation in "Perceptrons" book
   - Triggered first "AI Winter"

### Perceptron Limitations
- Cannot model non-linear functions (XOR problem)
- Binary/restricted outputs (hard step function)
- No hidden layers → cannot build hierarchical representations
- Overcome by Multi-Layer Perceptrons (MLPs) with hidden layers, non-linear activations (Sigmoid, Tanh, ReLU), and backpropagation

### Mathematical Foundation
- Perceptron computation: Output = f(Σwᵢxᵢ + b) where f is step activation
- Linear separability is the core requirement for single-layer perceptrons
- XOR demonstrates the need for non-linear decision boundaries

## Citations
- [1] Medium: "The Limitations of Perceptron - Why it Struggles with XOR"
- [2] Scribd: "Neural Network" presentation
- [3] Medium: "Perceptron in Deep Learning - Basics & Limitations"
- [4] APXML: "Perceptron Limitations" course material
- [5] Educative: "XOR Problem in Neural Network"
- [6] GeeksforGeeks: "What is Perceptron - The Simplest Artificial Neural Network"
- [7] Hashnode: "The Perceptron Algorithm - Some Limitations"
- [8] Towards Data Science: "Terribly Perceptive - The Perceptron, The XOR"

## Notes for Analysis
- This slide likely shows the classic demonstration of perceptron limitations using logic gates
- The title mentions "Test Single Perceptron with [AND – OR – XOR] Logic" - suggests visual comparison of decision boundaries
- May include 2D plots showing linear separability for AND/OR vs non-separability for XOR
- Key visual elements: truth tables, decision boundary plots, possibly weight/bias values