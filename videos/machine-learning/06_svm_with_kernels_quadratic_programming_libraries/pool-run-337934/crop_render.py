import sys
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = [float(v) for v in sys.argv[3:7]]
scale = float(sys.argv[7]) if len(sys.argv) > 7 else 4.0
im = Image.open(f"{NS}/{src}").convert("RGB")
w, h = im.size
box = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
crop = im.crop(box)
crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.LANCZOS)
crop.save(f"{NS}/{dst}")
print(dst, crop.size)
