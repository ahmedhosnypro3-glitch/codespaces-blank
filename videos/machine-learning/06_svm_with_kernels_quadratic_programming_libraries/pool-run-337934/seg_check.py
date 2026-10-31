import sys, os
sys.path.insert(0, "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
import numpy as np
import render_math

rows = {
    "eq1": "CC0000:\\boldsymbol{K}||000000:(a,b)=||CC0000:a^{T}b",
    "eq2": "CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:a^{T}b||000000:]^{2}",
    "eq6": "CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:e^{-\\gamma\\|a-b\\|^{2}}||000000:]",
}
for name, row in rows.items():
    segs = render_math.parse_row(row)
    print(f"== {name}: {len(segs)} segments")
    for color, latex in segs:
        arr, base, be, bt = render_math._draw(latex, color, 30, 30.0, 8.0, 72, 0.05)
        ink = arr[:, :, 3] > 40
        ys, xs = np.nonzero(ink)
        print(f"  {color} {latex!r}: ink x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] base={base} shape={arr.shape}")
