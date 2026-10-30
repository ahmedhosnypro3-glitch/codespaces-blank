# Source verification — slide 039
## Claims checked
- "Develop your own SVM library (from Scratch)" (instruction; checked as a documented pattern) — CONFIRMED — Domino https://domino.ai/blog/fitting-support-vector-machines-quadratic-programming ; Sandipanweb https://sandipanweb.wordpress.com/2018/04/23/implementing-a-soft-margin-kernelized-support-vector-machine-binary-classifier-with-quadratic-programming-in-r-and-python/ ; shenoynikhil https://github.com/shenoynikhil/svm-dual-optimization
- "quadprog" is a Quadratic Programming solver — CONFIRMED — quadprog GitHub https://github.com/quadprog/quadprog and PyPI https://pypi.org/project/quadprog/ (Goldfarb-Idnani dual active-set; min ½xᵀGx−aᵀx s.t. Cᵀx≥b, equalities via `meq`)
- "CVXOPT" is a Quadratic Programming solver — CONFIRMED — CVXOPT official site https://cvxopt.org/ (`cvxopt.solvers.qp`: min ½xᵀPx+qᵀx s.t. Gx≤h, Ax=b)
- A QP solver can solve what the slide calls "the Lagrangian Equation" (the SVM Lagrangian DUAL) — CONFIRMED — CVXOPT SVM application note https://cvxopt.org/applications/svm/index.html (P_ij=y_i y_j K(x_i,x_j), q=−1, box 0≤α_i≤C, equality Σ y_i α_i=0) and quadprog mapping https://scaron.info/blog/quadratic-programming-in-python.html
- "Quadratic" is a valid SVM kernel function — CONFIRMED — the degree-2 polynomial kernel K(x,z)=(x·z)² ; CMU 10601 SVM lecture https://www.cs.cmu.edu/~mgormley/courses/10601-s19/slides/lecture27-svm.pdf
- "Polynomial" and "RBF" are valid SVM kernel functions — CONFIRMED — scikit-learn `SVC` docs https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html ('poly' K=(γ⟨x,z⟩+c₀)^d, 'rbf' K=exp(−γ‖x−z‖²)) and Data Flair https://data-flair.training/blogs/svm-kernel-functions/
- Remaining slide text ("For each of the given dataset (2-D)", grid background coloring, same color per class) — UNVERIFIABLE — this is a plotting instruction: it carries no number, dataset name, formula, or attribution, so there is nothing for a source to check and nothing was invented.
## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild:
  - Keep `verbatim_text` byte-exact as printed — the stray space in "Quadratic , Polynomial" and the "..)" in "CVXOPT, ..)" are the slide's own characters; sources correct DATA only and license no frame-text edit.
  - Sign convention: the SVM dual is a maximization (max_α Σαᵢ − ½ΣΣαᵢαⱼyᵢyⱼK(xᵢ,xⱼ) s.t. Σαᵢyᵢ=0, 0≤αᵢ≤C). QP libraries minimize, so a compliant rebuild negates the objective (q=−1, P_ij=yᵢyⱼK(xᵢ,xⱼ)) while keeping the equality Σαᵢyᵢ=0 and the box 0≤αᵢ≤C intact — never flip either.
  - Symbol roles if any kernel equation is drawn: Quadratic K(x,z)=(x·z)²; Polynomial K(x,z)=(γ(x·z)+c₀)^d; RBF K(x,z)=exp(−γ‖x−z‖²) — the RBF exponent is negative. The slide names no symbol or parameter values, so none were added.
  - "Quadratic" is a legitimate textbook kernel name but is NOT a separate scikit-learn option: it is `kernel='poly'` with `degree=2`. The slide's word stands as-is; this is a naming note, not a correction.
  - 2-D inputs and grid-based background coloring have no checkable numeric data; no source was needed for them and none was invented.
