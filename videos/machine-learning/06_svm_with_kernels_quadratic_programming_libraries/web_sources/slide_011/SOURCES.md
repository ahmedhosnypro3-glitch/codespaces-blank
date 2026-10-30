# Source verification — slide 011

## Claims checked
- Maximize L = Σαᵢ − ½ΣΣ αᵢαⱼ yᵢyⱼ xᵢᵀxⱼ ⇒ Minimize L_D(α) = ½ΣΣ αᵢαⱼ yᵢyⱼ xᵢᵀxⱼ − Σαᵢ — CONFIRMED — CMU 10-701 SVM dual notes https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/svm_dual.pdf
  Minimization form is the standard sign-flipped QP objective written for solvers; the two are equivalent.
- Soft-margin SVM dual constraints: Σαᵢyᵢ = 0 — CONFIRMED — Cornell CS4780 https://www.cs.cornell.edu/courses/cs4780/2011fa/lecture/07-svm_duality.pdf
  Equality constraint comes from ∂/∂b of the Lagrangian; holds for any label signs.
- With labels y = (1, 1, −1, −1) the constraint reads α₁ + α₂ − α₃ − α₄ = 0 — CONFIRMED — JHU Vision-as-Bayesian-Inference SVM lecture https://www.cs.jhu.edu/~ayuille1/JHUcourses/VisionAsBayesianInference2025/12/Lecture12_SVM.pdf
  Slide's explicit expansion matches substituting those four labels into the sum.
- Box constraints 0 ≤ αᵢ ≤ C, listed individually as α₁≤1 … α₄≤1 — CONFIRMED — CMU 10-701 SVM dual notes https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/svm_dual.pdf
  Upper bound C is the soft-margin penalty parameter; αᵢ = C points sit inside the margin or are misclassified.
- C = 1 as the cost/regularization value — CONFIRMED — scikit-learn/LIBSVM docs https://www.csie.ntu.edu.tw/~cjlin/libsvm/
  C=1 is the LIBSVM default (-c 1) and scikit-learn's SVC default; a free choice for a worked example.
- Training vectors x₁=(1,1), x₂=(2,2), x₃=(7,4), x₄=(8,4) with labels +1,+1,−1,−1 — CONFIRMED — CMU 10-701 Lecture 6 https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/Lecture6_inked.pdf
  x₄=(8,4) appears in the slide's X matrix (rows shown as "1 2 7 8" / "1 2 4 4") and the label rows y₁=y₂=1, y₃=y₄=−1.
- Gram-matrix values shown as rows 2 4 11 12 and 4 8 22 24 ( i.e. XᵀX for those vectors) — CONFIRMED — recomputed from the cited vector set
  xᵢᵀxⱼ = 2, 4, 11, 12 / 4, 8, 22, 24 / 11, 22, 65, 72 / 12, 24, 72, 80 exactly.
- Expanded quadratic coefficients 1, 2, −5.5, −6 / 2, 4, −11, −12 / −5.5, −11, 32.5, 36 / −6, −12, 36, 40 — CORRECTED-role, content confirmed — same sources as above
  Every term equals ½·yᵢyⱼ·xᵢᵀxⱼ (e.g. −5.5 = ½·(−1)·11, 32.5 = ½·65, 40 = ½·80); the ½ must be carried into each coefficient.
- Framing of the result as a "Quadratic Equation in α with constraints" — CONFIRMED — SVM dual is a QP, CMU 10-701 https://www.cs.cmu.edu/~aarti/Class/10701_Spring23/Lecs/svm_dual.pdf

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: keep the max-to-min sign flip (the expanded bracket is subtracted
  by −[α₁+α₂+α₃+α₄]); half-integer coefficients (−5.5, 32.5) are ½·(odd Gram diagonal/cross terms), not typos;
  x₄=(8,4) and y₄=−1 are printed on the slide though the header row labels only x₁..x₃ — keep all four.
