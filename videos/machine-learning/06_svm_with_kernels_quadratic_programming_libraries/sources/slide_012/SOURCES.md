# Slide 012 — SVM Primal/Dual QP Formulation — Source Research

## Core References

1. **McGill University — CS COMP 551: SVM Dual Formulation (Lecture 12)**
   - URL: https://www.cs.mcgill.ca/~jpineau/comp551/Lectures/12SVM2.pdf
   - Covers: Primal QP, Lagrangian, dual formulation, KKT conditions, kernel trick introduction
   - Authority: University ML course material

2. **Medium — "The Optimization Behind SVM: Primal and Dual Form"**
   - URL: https://medium.com/aiguys/the-optimization-behind-svm-primal-and-dual-form-5cca1b052f45
   - Covers: Step-by-step derivation from primal to dual, complementary slackness, support vectors
   - Authority: Technical blog with mathematical derivation

3. **StackExchange — "Why bother with the dual problem when fitting SVM?"**
   - URL: https://stats.stackexchange.com/questions/19181/why-bother-with-the-dual-problem-when-fitting-svm
   - Covers: Motivation for dual formulation, inner product dependency, computational advantages
   - Authority: Stats community Q&A with expert answers

## Mathematical Formulation (from Slide 012)

### Primal (Soft-Margin)
```
Minimize: ½ ||w||² + C Σ ξ_i
Subject to: y_i(w·x_i + b) ≥ 1 - ξ_i, ξ_i ≥ 0
```

### Dual (via Lagrangian)
```
Maximize: Σ α_i - ½ Σ_i Σ_j α_i α_j y_i y_j (x_i·x_j)
Subject to: 0 ≤ α_i ≤ C, Σ α_i y_i = 0
```

### KKT Conditions
- α_i [y_i(w·x_i + b) - 1 + ξ_i] = 0
- Support vectors: α_i > 0
- w = Σ α_i y_i x_i
- Σ α_i y_i = 0

## Slide 012 Specific Content

The slide shows a specific 4-sample QP problem with:
- Objective: Minimize ½ αᵀPα + qᵀα
- P matrix (4×4): Given explicitly
- q vector: [α₁+α₂+α₃+α₄]
- Constraints: Σ y_i α_i = 0, 0 ≤ α_i ≤ 1

This matches the standard SVM dual formulation for a small toy dataset.

## Verification Notes

- The P matrix values on the slide correspond to P_ij = y_i y_j (x_i·x_j) for the given 4 samples
- The constraint α₁+α₂-α₃-α₄=0 reflects y = [+1, +1, -1, -1]
- Box constraints α_i ≤ 1 match C=1 soft-margin