# Source verification — slide 19

## Claims checked
- Kernels represent a dot product of two vectors in a higher dimensional feature space — CONFIRMED — DataCamp "Kernel Trick" https://www.datacamp.com/tutorial/kernel-trick
  A kernel is defined as K(x,z) = <phi(x), phi(z)>, an inner product in the (possibly infinite-dimensional) feature space.
- Any Machine Learning Model that contains dot product of input samples can be kernelized — CONFIRMED — Wikipedia "Kernel method" https://en.wikipedia.org/wiki/Kernel_method
  Any algorithm that processes data exclusively through dot products can be kernelized by replacing x_i^T x_j with k(x_i, x_j) — kernel perceptron, kernel PCA, kernel ridge regression are the standard examples.
- Instead of calculating the dot product between input vectors, calculate the dot product after mapping them to higher dimensional space — CONFIRMED — GeeksforGeeks "Kernel Trick in SVM" https://www.geeksforgeeks.org/machine-learning/kernel-trick-in-support-vector-classification/
  The dual/decision function depends only on inner products of mapped vectors, so the kernel evaluates them implicitly from input-space coordinates.
- Equation a^T b -> phi(a) and phi(b) -> phi(a)^T phi(b) = K(a,b) — CONFIRMED — Wikipedia "Kernel method" https://en.wikipedia.org/wiki/Kernel_method
  Authoritative form is K(a,b) = phi(a)^T phi(b) = <phi(a), phi(b)>; the slide's arrows are didactic sequence, not an extra algebraic claim.
- Different Kernel functions are based on different mapping functions — CONFIRMED — Cornell CS4787 lecture notes (kernel methods) https://www.cs.cornell.edu/courses/cs4787/2019sp/notes/lecture15.pdf
  Each valid kernel implies its own feature space and phi: linear kernel = identity map, polynomial = all monomials up to degree d, RBF = infinite-dimensional space.
- Calculations of the mapping and of the dot product in the higher dimensional space are very expensive; the Kernel Trick minimizes both at no extra cost — CONFIRMED — DataCamp "Kernel Trick" https://www.datacamp.com/tutorial/kernel-trick
  Explicitly computing phi(x) is computationally expensive or impossible (feature space may be infinite-dimensional); the trick computes the inner product directly.

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild:
  - No numbers, dataset names, library names, sign conventions, or attributions appear on this slide; nothing requires spec correction.
  - Symbol roles: phi = the feature-space mapping, K = the kernel function (= inner product of mapped vectors), a and b = the two input vectors.
  - Render the equation per the house Professional-Format math rule as a 2D chain (phi(a)^T phi(b) on one line over K(a, b), or as the slide's arrow sequence), keeping the slide's verbatim text unchanged.
