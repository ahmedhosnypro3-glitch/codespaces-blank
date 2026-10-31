import sys, os
sys.path.insert(0, "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
import numpy as np
import render_math
from PIL import Image

latex = sys.argv[1]
pt = float(sys.argv[2]) if len(sys.argv) > 2 else 40
arr, base = render_math.render_segment(latex, "#000000", pt, 4.0, 1.0)
ink = arr[:, :, 3]
h, w = ink.shape
cols = 90
rows = max(1, int(cols * h / w * 0.5))
small = np.asarray(Image.fromarray(ink).resize((cols, rows)))
chars = " .:-=+*#%@"
for r in small:
    print("".join(chars[min(9, int(v / 256 * 10))] for v in r))
print(f"shape={arr.shape} base={base}")
