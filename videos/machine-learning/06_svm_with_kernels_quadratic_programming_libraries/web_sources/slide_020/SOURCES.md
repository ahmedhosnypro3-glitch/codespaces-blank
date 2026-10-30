# Source verification — slide 020
## Claims checked
- "Normal Model — Calculate a^T b": the plain model takes the dot product of the raw input
  vectors — CONFIRMED — DataCamp, "Kernel Trick" https://www.datacamp.com/tutorial/kernel-trick
  Kernelized algorithms only ever touch the data through inner products (dot products); the
  un-mapped a^T b is exactly that baseline computation.
- "Kernelized Model — Calculate u^T v": the kernelized model takes the dot product of the
  feature-mapped vectors — CONFIRMED — Wikipedia, "Kernel method" https://en.wikipedia.org/wiki/Kernel_method
  Standard form: K(x, z) = φ(x)ᵀ φ(z) = ⟨φ(x), φ(z)⟩, i.e. u = φ(a), v = φ(b) and u^T v is the
  mapped-space dot product. No number, sign or symbol is misstated on the slide.
- "Map Input data to higher dimensions Before Apply to the model" — CONFIRMED — Jonathan Hui,
  "Kernels for Machine Learning" https://jonathan-hui.medium.com/kernels-for-machine-learning-3f206efa9418
  Explicit feature mapping φ first lifts each input vector into a higher-dimensional feature
  space; the model then runs there.
- "Higher Computational Complexity" (warning attached to the explicit-mapping route) — CONFIRMED —
  chenxing.space, "The Kernel Trick" https://chenxing.space/blog/the-kernel-trick
  Explicit mapping is the brute-force route the kernel trick avoids: dimension counts explode
  combinatorially (curse of dimensionality), so storing φ(x) and its dot products is
  memory- and compute-prohibitive; for the RBF/Gaussian kernel the space is infinite-dimensional.
- "Vectors Mapping — a, b -> u, v" — CONFIRMED — Towards Data Science, "Explicit feature maps for
  non-linear kernel functions" https://towardsdatascience.com/explicit-feature-maps-for-non-linear-kernel-functions-171a9043da38/
  u and v are the images of a and b under the feature map (a, b ↦ u, v; u = φ(a), v = φ(b)).
## Overall
- VERDICT: CONFIRMED
- Symbol roles for the rebuild: a/b are raw input samples, u/v are their feature-space images,
  and u^T v equals the kernel value K(a, b) = φ(a)ᵀφ(b). Keep the slide's own symbols (a, b, u,
  v) verbatim in the recreation — do not substitute φ-notation into the slide text; the source
  form only explains what the slide's symbols stand for.
- "Higher Computational Complexity" is a correct caveat on the *explicit-mapping* path the bottom
  flow draws (curve through Vectors Mapping), not a claim that kernels are slow — a kernel
  function computes the same u^T v without materializing u and v.
- No numeric values, hyperparameters or sign conventions appear on this slide, so no rounding or
  sign-convention fixes apply. "O/P" and "O/R" are slide-local labels (output / result region
  captions) not resolvable from sources; render them verbatim and unchanged.
