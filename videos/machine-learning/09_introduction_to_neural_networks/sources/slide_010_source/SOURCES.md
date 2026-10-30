# Source Research for slide_010

## Slide Content (from doc-parse)
- **Slide number**: 10
- **Content**: "Classification of 'AND' Truth Table"
- **Table**:
  | X1 | X2 | O/P |
  | --- | --- | --- |
  | 0 | 0 | 0 |
  | 0 | 1 | 0 |
  | 1 | 0 | 0 |
  | 1 | 1 | 1 |
- **Visual elements**: Decision boundary plot with X1/X2 axes, threshold line, and formula "d(X)=-5x1-3x2+6"
- **Equation**: d(X) = -5x1 - 3x2 + 6

## Web Search Findings (Perceptron Decision Boundaries)

**Source**: Multiple sources (GeeksforGeeks, Medium, Codecademy, Scribd)

**Key facts verified**:
1. **Perceptron Model**: d(X) = Σwᵢxᵢ + b (weighted sum + bias)
2. **Decision Boundary**: d(X) = 0 defines a line in 2D space (w₁x₁ + w₂x₂ + b = 0)
3. **AND Gate**: Linearly separable
   - Weights: w₁=1, w₂=1, bias b=-1.5
   - Boundary: x₁ + x₂ - 1.5 = 0 → x₂ = -x₁ + 1.5
   - Isolates (1,1) from other points
4. **OR Gate**: Linearly separable
   - Weights: w₁=1, w₂=1, bias b=-0.5
   - Boundary: x₁ + x₂ - 0.5 = 0 → x₂ = -x₁ + 0.5
   - Separates (0,0) from positive points

## Slide-Specific Analysis

This slide shows the AND gate truth table with a visual decision boundary plot. The formula d(X) = -5x1 - 3x2 + 6 represents the weighted sum:
- w₁ = -5, w₂ = -3, b = 6
- Decision boundary: -5x₁ - 3x₂ + 6 = 0 → 3x₂ = -5x₁ + 6 → x₂ = (-5/3)x₁ + 2
- Threshold: d(X) > 0 ⇒ output 1, d(X) ≤ 0 ⇒ output 0

## Citations
- [1] GeeksforGeeks: "What is Perceptron - The Simplest Artificial Neural Network"
- [2] Medium: "Day 2: The Perceptron"
- [3] Scribd: "AND Gate Perceptron Learning"
- [4] Codecademy: Perceptron cheatsheet
- [5] Medium: "Decision Boundaries Perceptron Learning"
- [6] itnext.io: "Linear Predictors: The Perceptron from Theory to Algorithms"

## Notes for Analysis
- This is a demonstration of perceptron classifying AND logic gate
- Shows decision boundary visualization (2D plot with line)
- The specific weights (-5, -3, bias 6) are an example, not the canonical AND gate weights
- The table and equation must be reproduced verbatim
- Visual elements: 2D scatter/plot with decision boundary line