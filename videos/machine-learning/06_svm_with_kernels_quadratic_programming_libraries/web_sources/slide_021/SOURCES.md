# Source verification — slide 021

## Claims checked

- Kernel shown is the quadratic kernel `K(a,b) = (a^T b)^2` (homogeneous degree-2 polynomial kernel) — CONFIRMED — StackExchange / CS kernel notes https://stats.stackexchange.com/questions/401304/how-does-this-transformation-from-2d-to-3d-work-mathmatically
- "Map Input data from 2-D to 3-D": explicit feature map `phi(x) = (x1^2, x2^2, sqrt(2) x1 x2)` for 2-D input, so `phi(a)^T phi(b) = a1^2 b1^2 + (sqrt2 a1a2)(sqrt2 b1b2) + a2^2 b2^2 = (a^T b)^2` — CONFIRMED (dimension 3 = n(n+1)/2 for n = 2) — https://compphysics.github.io/MachineLearningMSU/doc/pub/svm/html/._svm-bs020.html
- Slide's mapped-vector terms `sqrt(2) a1a2` and `sqrt(2) b1b2` are the correct normalized cross-term coefficients — CONFIRMED (an unnormalized `2 a1a2` cross term would represent a *different* kernel) — https://arxiv.org/abs/2410.12635
- "Kernelized Model" evaluating `u^T v` equals the explicit mapped-space inner product (kernel trick), i.e. the same value is obtained without materializing the 3-D vectors — CONFIRMED — Duke CS kernel notes https://users.cs.duke.edu/~cynthia/CourseNotes/KernelNotes.pdf
- Slide's warning "Higher Computational Complexity !!!" for the explicit 2-D→3-D mapping route — CONFIRMED: explicit mapping costs O(d^2) per sample and O(N d^2) storage, versus O(d) for the kernel function — https://chenxing.space/blog/the-kernel-trick/
- `K(a,b) = (a^T b)^2` is a valid positive semi-definite (Mercer) kernel, since it is a dot product of an explicit feature map — CONFIRMED — Wikipedia, Mercer's theorem https://en.wikipedia.org/wiki/Mercer%27s_theorem

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: slide vectors are `a = (a1, a2)`, `b = (b1, b2)`; mapped vectors
  `u = phi(a)`, `v = phi(b)` play the role of the feature vectors. Keep the `sqrt(2)` scale on the
  cross term exactly as printed; component ordering inside the 3-D vector does not change the value.
  The 2-D→3-D dimension claim is exact (3, not 6: the slide's map is the reduced symmetric one).
