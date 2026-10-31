import sys
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
slide = sys.argv[1]  # e.g. 031
x0, y0, x1, y1 = [float(v) for v in sys.argv[2:6]]
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 170

im = Image.open(f"{NS}/recreated_pptx/renders/slide_{slide}_recreated-1.png").convert("RGB")
a = np.asarray(im).astype(int)
h, w = a.shape[:2]
sub = a[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
ink = (sub.sum(axis=2) < 600).astype(np.uint8) * 255
img = Image.fromarray(ink)
sh, sw = img.size[1], img.size[0]
rows = max(1, int(cols * sh / sw * 0.5))
small = np.asarray(img.resize((cols, rows)))
chars = " .:-=+*#%@"
for r in small:
    print("".join(chars[min(9, int(v / 256 * 10))] for v in r))
