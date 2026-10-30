# Source verification — slide 017

## Claims checked

- Title `Non-Linearly Separable Data` — CONFIRMED — LibreTexts, "Non-Linearly Separable Data and the Kernel Trick" https://biz.libretexts.org/Courses/Aurora_University/Data_Analytics_with_Applications_in_Business/10%3A_Support_Vector_Machines/10.05%3A_Non-Linearly_Separable_Data_and_the_Kernel_Trick
  Standard SVM term: data no single straight line (2-D) / flat hyperplane (n-D) can divide the classes without error. Same usage at DataCamp, "Kernel Trick" https://www.datacamp.com/tutorial/kernel-trick.

- Bullet / red italic instruction `Each Sample is represented by two features "x" and "y"` — CONFIRMED — GeeksforGeeks, "Non-Linear SVM" https://www.geeksforgeeks.org/machine-learning/ml-non-linear-svm/
  In this 2-D setup every training sample is one two-coordinate point; the slide's `x` and `y` are the two plotted feature axes, i.e. the standard `x₁` / `x₂` pair. Symbol-role note only — the slide's own wording stays verbatim.

- Callout `Linear Decision Boundary` (leader line to the blue straight diagonal line) — CONFIRMED — MIT 6.034, SVM notes https://web.mit.edu/6.034/wwwbob/svm-notes-long-08.pdf
  A linear SVM boundary is the hyperplane `wᵀx + b = 0`, which in 2-D is exactly a straight line; `w` is orthogonal to it, `b` the bias/intercept. The blue diagonal line is that form.

- Callout `Linear Decision Boundary` drawn as visibly failing on this data — CONFIRMED — LibreTexts (same URL above)
  On concentric / ringed arrangements no straight line cuts the classes cleanly, so the blue line is meant to look visibly inadequate. Do not "fix" it into a working separator.

- Callout `Non-Linear Decision Boundary` (leader line to the red closed circle) — CONFIRMED — scikit-learn, `sklearn.datasets.make_circles` https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_circles.html
  Canonical concentric-circles case: one class is the inner cluster, the other a surrounding ring. An RBF/Gaussian kernel SVM produces a closed non-linear boundary `K(x,x′) = exp(-γ‖x-x′‖²)` wrapping the inner cluster. Same arrangement at scikit-learn, "SVMs with different kernels" https://scikit-learn.org/stable/auto_examples/svm/plot_svm_kernels.html.

- Axis labels `x` / `y` (red arrowed axes crossing at the plot centre) — CONFIRMED — scikit-learn, `make_circles` (same URL above)
  `make_circles` returns a 2-column feature matrix plotted on the standard `x₁` / `x₂` axes; the slide's `x` / `y` are those two axes.

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild (no DATA corrections; `verbatim_text` unchanged):
  - Symbol roles: `x` / `y` are the two feature coordinates of one 2-D point per sample (standard `x₁` / `x₂`); "two features" describes one sample's coordinate pair, not two separate scalar inputs.
  - Spatial convention: the red circle is the non-linear boundary ENCLOSING the inner cluster, the ring class sitting outside it (validation already removed the opposite "orange inside / cyan outside" claim).
  - The blue straight line is a *failing* linear boundary — keep it visibly inadequate, not a working separator.
  - The red instruction line and the bullet are the same string on this slide (`Each Sample is represented by two features "x" and "y"`).
  - No numbers, constants, formulas, dataset names, hyperparameters or theorem attributions appear on the slide (only the badge numeral `17`, the printed slide number per the house badge rule), so no numeric or attribution drift is possible.
