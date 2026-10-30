# Source verification — slide 002

## Claims checked
- The slide is a "Python Quadratic Programming Libraries" slide; that CVXOPT is a Python convex-optimization library with a quadratic-programming solver (`cvxopt.solvers.qp`) — CONFIRMED — CVXOPT official site https://cvxopt.org/ and source https://github.com/cvxopt/cvxopt/blob/master/src/python/solvers.py (interior-point QP solver, min ½xᵀPx+qᵀx s.t. Gx≤h, Ax=b)
- That QuadProg is a Python quadratic-programming library — CONFIRMED — quadprog GitHub https://github.com/quadprog/quadprog and PyPI https://pypi.org/project/quadprog/ (Goldfarb-Idnani dual-method QP solver, strictly convex problems; `meq` marks leading constraints as equalities)
- That both named libraries are the Python QP libraries used to solve the SVM dual (the slide's own framing: SVM training is solved as a QP) — CONFIRMED — CVXOPT SVM application note https://cvxopt.org/applications/svm/index.html (dual SVM built as P_ij=y_i y_j K(x_i,x_j), q=−1, box 0≤α_i≤C, equality Σy_iα_i=0) and Domino blog https://domino.ai/blog/fitting-support-vector-machines-quadratic-programming
- No numeric values, formulas, dataset names, hyperparameter names, theorem attributions or sign conventions appear on the slide — nothing further to check; the only frame data are the two library names and the word "call".

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: spell the library names exactly as the slide shows them — "CVXOPT" and "QuadProg" (all-caps CVXOPT, mixed-case QuadProg); verbatim_text is unchanged. Note "QuadProg" also names R's `solve.QP` package, but in this Python-QP-library framing it is the Python `quadprog` package (pip-installable). Rebuild should render these as plain text names, not code/API calls.
