# Source verification — slide 023

## Claims checked

- RBF example formula e^(−y‖a − b‖²) — CONFIRMED (as to form) — scikit-learn rbf_kernel, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.rbf_kernel.html
  Authoritative RBF/Gaussian kernel: K(a, b) = exp(−γ‖a − b‖²) over vectors a, b in Rᵈ, equivalently
  exp(−‖a − b‖²/2σ²). The slide's expression is the standard RBF kernel form.

- The symbol printed as `y` in e^(−y‖a − b‖²) plays the role of γ (gamma) — CONFIRMED (symbol role; `verbatim_text` unchanged) — same scikit-learn rbf_kernel page (reused per "never fetch a page twice") plus the RBF-parameter example, https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
  γ is the free hyperparameter setting the kernel's radius of influence, with γ = 1/(2σ²). Both doc-parse and image-analysis render the glyph as the Latin `y`; the authoritative glyph is Greek γ.

- "Map Input data from 2-D to infinite Dimension": RBF maps 2-D inputs to an infinite-dimensional feature space — CONFIRMED — CSCI 5525 lecture 8 (https://zstevenwu.com/courses/s20/csci5525/resources/slides/lecture08.pdf) and Cornell CS4787 lecture 15 (https://www.cs.cornell.edu/courses/cs4787/2019sp/notes/lecture15.pdf)
  exp(xᵀy/σ²) = Σⱼ (xᵀy)ʲ/(j!σ²ʲ) with the multinomial theorem yields components indexed by multi-indices of unbounded degree — for 2-D input that is u₁, u₂, u₃, … without end, an ℓ₂-sequence space.

- "Kernelized Model / Calculate uᵀv" and "Normal Model / Calculate aᵀb" — the inner product of the mapped vectors equals the kernel value, so uᵀv = K(a, b) = exp(−γ‖a − b‖²), while aᵀb = a₁b₁ + a₂b₂ is the unmapped 2-D inner product — CONFIRMED — wikipedia, Kernel method (https://en.wikipedia.org/wiki/Kernel_method) and Datacamp, The Kernel Trick (https://www.datacamp.com/tutorial/kernel-trick). K(x, z) = ⟨φ(x), φ(z)⟩ is the defining identity of a kernel: Φ(a)→u, Φ(b)→v, so uᵀv is obtained from the 2-D inputs without ever forming u and v.

- "Higher Computational Complexity !!!" callouts on the explicit infinite-dimension mapping path — CONFIRMED — wikipedia, Kernel method (https://en.wikipedia.org/wiki/Kernel_method). Explicitly computing the RBF feature map needs an infinite number of coordinates per point (infinite cost and memory) and is intractable; the kernel form evaluates in one step on the low-dimensional inputs. The penalty attaches to the left (mapping) flow, not to the kernelized path.

- Both-pane contrast, emphasis only (data unchanged) — CORRECTED — dailydoseofds, The mathematics behind
  the RBF kernel (https://www.dailydoseofds.com/p/the-mathematics-behind-rbf-kernel/) and CMU 10624
  lecture 7 (https://www.cs.cmu.edu/~hchai2/courses/10624/lectures/Lecture7.pdf). Some lectures print the
  complexity warning on BOTH panes; the authoritative statement puts the penalty on the explicit mapping
  only, the kernelized pane evaluating uᵀv via K(a,b) at low-dimensional cost. Keep both chips as frame
  text; place the emphasis per this reading.

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: render exp(−γ‖a − b‖²) with Greek γ (the transcripts' Latin `y` is an OCR artifact — do not copy it into `verbatim_text`, do not use a Latin y in the math). ‖a − b‖² is the squared Euclidean distance Σ(aᵢ − bᵢ)². No sign or rounding concerns — the formula is symbolic. u = [u₁ u₂ u₃ … u∞]ᵀ and v = [v₁ v₂ v₃ … v∞]ᵀ are the infinite-length images of a and b, and uᵀv = K(a, b).
