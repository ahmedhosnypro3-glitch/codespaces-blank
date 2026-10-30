# Source verification — slide 012

## Claims checked

- P as printed (4×4: rows "2 4 −11 −12" / "4 8 −22 −24" / "−11 −22 65 72" / "−12 −24 72 80") is a symmetric matrix — CONFIRMED — Jabrekh/CU-Denver, "Symmetric Matrices and Quadratic Forms" slides https://jabrekh.github.io/assets/materials/fall%202023%20-%20slides/25-Symmetric%20Matrices%20and%20Quadratic%20Forms.pdf
  Exact check by Fraction arithmetic: P[i][j] == P[j][i] for all 16 pairs.

- Printed P is positive semidefinite — CONFIRMED — CMU 10-701 Lecture 6 (SVM dual; Q PSD) https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/Lecture6_inked.pdf
  Eigenvalues exactly 0, 0, 0.9151, 154.0849; min = 0 ≥ 0, so the QP is convex and bounded below.

- "Minimize: ½ αᵀPα" expands to exactly the slide's 16-term quadratic, i.e. the lower box's coefficients are 2× the upper box's — CONFIRMED — Kadeishvili, "Quadratic Forms" lecture notes https://rmi.tsu.ge/~kade/LecturesT.Kadeishvili/MathEconomics/Term3/Week3QuadraticLEC.pdf
  Rule: coefficient of αᵢ² is P_ii; coefficient of αᵢαⱼ is P_ij + P_ji = 2P_ij for symmetric P. Verified numerically at α = (1,2,3,4): αᵀ(P/2)α = ½αᵀPα = 2833/2.

- Soft-margin SVM dual in canonical QP form is "min ½αᵀPα − 1ᵀα" subject to yᵀα = 0 and 0 ≤ αᵢ ≤ C — CONFIRMED — Chang & Lin, LIBSVM paper (CMU-hosted) https://www.cs.cmu.edu/~pakyan/compbio/references/Chang_LIBSVM_2001.pdf

- qᵀ = [1, 1, 1, 1] paired with a "+ qᵀα" objective — CORRECTED — Chang & Lin, LIBSVM paper https://www.cs.cmu.edu/~pakyan/compbio/references/Chang_LIBSVM_2001.pdf
  The canonical linear term is −1ᵀα (the minimization flip of max 1ᵀα − ½αᵀPα). The slide's own expanded objective prints "− [ α₁+α₂+α₃+α₄ ]", so under the printed "+ qᵀα" form qᵀ must be [−1,−1,−1,−1]; equivalently keep qᵀ = [1,1,1,1] and write "− qᵀα". Sign convention only — verbatim_text unchanged.

- Slide title calls the α-formulation the "SVM Primal Problem" — CORRECTED — Chang & Lin, LIBSVM https://www.cs.cmu.edu/~pakyan/compbio/references/Chang_LIBSVM_2001.pdf
  A formulation in the multiplier vector α with Q = yᵢyⱼK(xᵢ,xⱼ), yᵀα = 0 and 0 ≤ αᵢ ≤ C is the Lagrangian DUAL of the soft-margin SVM, not the primal (the primal is in w and ξ). Panel-heading wording is the slide's own label and stays verbatim; recorded here as an attribution correction for the rebuild, not as an edit.

- "∑ αᵢyᵢ = 0 → α₁+α₂−α₃−α₄ = 0", "αᵢ ≤ 1", "αᵢ ≥ 0" — CONFIRMED — CMU 10-701 Lecture 6 https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/Lecture6_inked.pdf
  Those signs imply labels y = (+1,+1,−1,−1); the printed αᵢ ≤ 1 is the box 0 ≤ αᵢ ≤ C with C = 1; αᵢ ≥ 0 is the canonical lower bound.

## Overall

- VERDICT: CORRECTED
- Tolerance notes for the rebuild: build the objective as ½αᵀPα − 1ᵀα (or qᵀ = [−1,−1,−1,−1] with a plus sign) so the compact form matches the expanded quadratic and the slide's visible "− [ Σαᵢ ]" bracket. P is exactly symmetric and PSD — no symmetrization needed. The lower panel's coefficients are deliberately 2× the upper panel's; do not "fix" that ratio. Transcript artifact recorded, not edited: the doc-parse line prints the αᵢ≥0 constraint with "α₃≥0" twice where "α₂≥0" is meant; the spec's verbatim is already correct (α₁, α₂, α₃, α₄ ≥ 0).
