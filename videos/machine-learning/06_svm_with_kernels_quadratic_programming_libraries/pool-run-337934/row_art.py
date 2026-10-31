import sys, os
sys.path.insert(0, "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
import numpy as np
import render_math
from PIL import Image

row = sys.argv[1]
pt = float(sys.argv[2]) if len(sys.argv) > 2 else 30
canvas = render_math.render_row(row, pt)
ink = canvas[:, :, 3]
h, w = ink.shape
cols = 170
rows = max(1, int(cols * h / w * 0.5))
small = np.asarray(Image.fromarray(ink).resize((cols, rows)))
chars = " .:-=+*#%@"
for r in small:
    print("".join(chars[min(9, int(v / 256 * 10))] for v in r))
print(f"canvas {w}x{h}")
