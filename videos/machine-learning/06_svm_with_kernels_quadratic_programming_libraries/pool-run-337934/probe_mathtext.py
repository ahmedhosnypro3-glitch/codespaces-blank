import sys, os
sys.path.insert(0, "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
import numpy as np
import render_math

tests = {
    "empty_base_sup_T": r"{}^{T}",
    "a_sup_T": r"a^{T}",
    "br_sup_2": r"]^{2}",
    "double_sup": r"e^{-\gamma}{}^{\|a-b\|^{2}}",
    "rbf_fixed": r"e^{-\gamma\|a-b\|^{2}}",
    "K_sub": r"K_{1}(a,b)",
    "K_sub_plain": r"K_1(a,b)",
}
for name, latex in tests.items():
    try:
        arr, base, be, bt = render_math._draw(latex, "#000000", 20, 6.0, 3.0, 72, 0.02)
        ink = arr[:, :, 3] > 40
        ys, xs = np.nonzero(ink)
        print(name, "ink", xs.max() - xs.min() + 1, "x", ys.max() - ys.min() + 1,
              "px @72dpi, baseline_y=", base)
    except Exception as e:
        print(name, "FAIL", type(e).__name__, str(e)[:120])
