# Slide 019 — Kernels Concept & Kernel Trick — Source Research

## Core References

1. **Wikipedia — Kernel Method**
   - URL: https://en.wikipedia.org/wiki/Kernel_method
   - Covers: General kernel trick, dot product in feature space, Mercer's theorem

2. **McGill COMP 551** (same as slide 012)
   - Covers: Kernel trick motivation, computational savings

## Slide 019 Content Verification

The slide states:
1. "Kernels Represent a dot product of two vectors in a higher dimensional feature space" ✓ Correct - this is the definition
2. "Any Machine Learning Model that contains dot product of input samples can be kernelized" ✓ Correct - any algorithm using only inner products
3. "Instead of calculating dot product between input vectors, calculate dot product between input vectors after mapping them to higher dimensional space" ✓ Correct
4. Formula: aᵀb ↦ φ(a), φ(b) ↦ φ(a)ᵀφ(b) ≡ K(a,b) ✓ Standard kernel trick notation
5. "Different Kernel functions are based on different mapping functions" ✓ Correct
6. "Calculations of mapping and calculations of dot product in higher dimensional space are very expensive" ✓ Correct - explicit mapping is O(d²) for polynomial
7. "Use Kernel Trick to minimize both calculations (at no extra cost)" ✓ Correct - kernel computes inner product directly in O(d)

## Key Insight
The kernel trick avoids explicit φ(x) computation. For polynomial kernel K(x,y) = (x·y + c)^d:
- Explicit φ(x): O(d²) space/time for degree 2
- Kernel evaluation: O(d) time
- Dual SVM only needs K(x_i, x_j) = (x_i·x_j + c)^d