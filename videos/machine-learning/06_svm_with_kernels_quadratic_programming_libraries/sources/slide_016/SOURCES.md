# Slide 016 — Feature Mapping x → φ(x) = (x, x²) — Source Research

## Core References

1. **Wikipedia — Polynomial Kernel**
   - URL: https://en.wikipedia.org/wiki/Polynomial_kernel
   - Covers: General polynomial kernel K(x,z) = (x·z + c)^d, feature mapping for d=2

2. **Steven Wu — CSCI5525 Lecture 8 Slides**
   - URL: https://zstevenwu.com/courses/s20/csci5525/resources/slides/lecture08.pdf
   - Covers: Explicit feature mapping for quadratic kernel, dimension calculation

## Mathematical Content (from Slide 016)

For 1D input x, quadratic kernel K(x,y) = (xy + 1)² expands to:
```
K(x,y) = (xy + 1)²
       = x²y² + 2xy + 1
       = 1·1 + (√2 x)·(√2 y) + (x²)·(y²)
```

Explicit mapping: φ(x) = [1, √2 x, x²]ᵀ

This maps 1D input to 3D feature space where data becomes linearly separable.

## Slide 016 Specifics
- Shows x → (x, x²) mapping (simplified, omitting √2 scaling and constant 1)
- Demonstrates non-linear decision boundary in 1D becomes linear in 2D
- Visual: parabola in original space, straight line in mapped space

## Verification
- The mapping φ(x) = [1, √2 x, x²] is standard for (x·y + 1)²
- The slide shows simplified version x → (x, x²) which captures the essence
- The √2 scaling ensures the cross-term has correct coefficient in dot product