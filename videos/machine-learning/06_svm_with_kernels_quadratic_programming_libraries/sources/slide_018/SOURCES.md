# Slide 018 — Mapping to 3D (Z → φ(Z)) — Source Research

## Core References

1. **Wikipedia — Polynomial Kernel** (same as slide 016)
   - For 2D input x = [x₁, x₂], quadratic kernel gives 6D mapping

2. **Steven Wu — CSCI5525 Lecture 8** (same as slide 016)
   - Explicit feature mapping for 2D quadratic kernel

## Mathematical Content

For Z = [x, y] (2D input), kernel K(Z,Z') = (Z·Z' + 1)²:
```
K = (x₁x₂ + y₁y₂ + 1)²
  = 1 + 2x₁x₂ + 2y₁y₂ + x₁²x₂² + y₁²y₂² + 2x₁y₁x₂y₂
```

Feature mapping φ(Z) ∈ ℝ⁶:
```
φ(x, y) = [1, √2 x, √2 y, x², y², √2 xy]ᵀ
```

The slide shows: Z = (x, y) → (x², y², √2xy) — the quadratic/interaction terms only (omitting constant and linear terms for visual clarity).

## Slide 018 Specifics
- Title: "Non-Linearly Separable Data"
- Shows 3D visualization with plane separator
- Formula shows mapping to 3 components (quadratic terms)

## Verification
- Full mapping is 6D, slide shows 3 key quadratic components
- The orange plane in 3D represents linear separator in mapped space
- Standard polynomial kernel degree 2 for 2D input