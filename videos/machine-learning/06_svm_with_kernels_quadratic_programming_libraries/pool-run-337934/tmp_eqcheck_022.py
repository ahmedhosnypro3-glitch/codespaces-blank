import json, os
from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
m = json.load(open(NS + "/recreated_pptx/build/eq_022/manifest.json"))
for name, info in m.items():
    im = Image.open(info["path"]).convert("RGBA")
    a = np.asarray(im)
    alpha = a[..., 3]
    ink = alpha > 40
    print(f"{name}: {im.size} ink={ink.mean():.3f} px={info['w_px']}x{info['h_px']} match={im.size==(info['w_px'],info['h_px'])}")
