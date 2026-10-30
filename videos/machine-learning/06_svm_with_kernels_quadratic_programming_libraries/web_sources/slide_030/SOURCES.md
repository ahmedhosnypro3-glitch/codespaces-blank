# Source verification — slide 030

## Claims checked

- Title "Radial Basis Function (RBF) Kernel" — the RBF kernel is the Gaussian kernel, a standard SVM kernel — CONFIRMED — wikipedia, Radial basis function kernel (https://en.wikipedia.org/wiki/Radial_basis_function_kernel)

- Boxed result formula printed as `e −y(a−b)2` = e^(−γ(a−b)²) — CONFIRMED (form) — same wikipedia RBF-kernel page plus Cornell CS4787 lecture 15 (https://www.cs.cornell.edu/courses/cs4787/2019sp/notes/lecture15.pdf). Authoritative form: K(a, b) = exp(−γ‖a − b‖²), equivalently exp(−‖a − b‖²/(2σ²)) with γ = 1/(2σ²); for scalar inputs a, b the norm term reduces to (a − b)².

- The glyph printed as Latin `y` in the exponent plays the role of γ (gamma), the RBF coefficient — CONFIRMED (symbol role; `verbatim_text` unchanged) — same wikipedia RBF-kernel page and Cornell CS4787 lecture 15 (reused per "never fetch a page twice"). γ is the free kernel width hyperparameter, γ = 1/(2σ²).

- Left-panel prefactor structure e^(−a²/2) … e^(−b²/2) with a trailing e^(−b²/2) factor — CONFIRMED — wikipedia RBF kernel + Cornell CS4787 lecture 15 (reused). exp(−γ‖a‖²)·exp(−γ‖b‖²)·exp(2γaᵀb) is the standard factorization of exp(−γ‖a − b‖²); the slide's e^(−a²/2) / e^(−b²/2) prefactors are the γ = 1/2 (σ = 1) case.

- Left-panel expansion: the series row with φ(a)ᵀ and φ(b) pills and the bⁿ/√n! column — CONFIRMED — Columbia COM4771 kernel handout (http://www.cs.columbia.edu/~djhsu/coms4771-f25/lectures/kern-handout.pdf) and CSCI 5525 lecture 08 (https://zstevenwu.com/courses/s20/csci5525/resources/slides/lecture08.pdf). φ(x) = exp(−x²/2)·[1, x, x²/√2!, x³/√3!, …]ᵀ, and φ(a)ᵀφ(b) = exp(−a²/2)exp(−b²/2)·Σ(a b)ʲ/j! = exp(−(a − b)²/2).

- Implicit infinite-dimensional feature space behind the RBF kernel — CONFIRMED — wikipedia RBF kernel, Cornell CS4787 lecture 15 (both reused). exp(u) = Σⱼ₌₀∞ uʲ/j! is an unbounded Taylor/Maclaurin series, so the expansion's terms run to unbounded degree, giving coordinates u₁, u₂, … without end; the kernel still evaluates in O(d) on the inputs.

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: render the exponent coefficient as Greek γ — the transcripts' Latin `y` is a glyph artifact (do not copy it into `verbatim_text`; do not use a Latin y in the math). The left derivation panel is the γ = 1/2 (σ = 1) normalization: exp(−(a − b)²/2) = exp(−a²/2)·exp(−b²/2)·exp(ab) with 1/√n! coefficients — build it exactly in that form; the general-γ family would carry (√(2γ))ʲ/√n! coefficients. For vector inputs the exponent takes ‖a − b‖² (squared Euclidean distance ‖a‖² + ‖b‖² − 2aᵀb); the slide's transcript drops the norm bars — notation tolerance, not a data correction. φ(a)ᵀφ(b) is the kernel identity K(a, b) = ⟨φ(a), φ(b)⟩, so uᵀv is obtained from a, b without forming u, v.
