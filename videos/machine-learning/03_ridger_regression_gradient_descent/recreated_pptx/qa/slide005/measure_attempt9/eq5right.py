import numpy as np
from PIL import Image
ORIG = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_005.jpg"
REND = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/render_8.png"
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
SX, SY = 2001/960.0, 1125/540.0
print("ORIGINAL eq5: column ink counts (y456..508) for x600..690; thr<200 vs thr<150")
print("   x    n<200  n<150   verdict")
for x in range(600, 691):
    c200 = int((o[456:509, x].mean(axis=1) < 200).sum())
    c150 = int((o[456:509, x].mean(axis=1) < 150).sum())
    v = "INK" if c200 >= 3 else ("noise" if c200 > 0 else "")
    print("  %3d   %4d   %4d   %s" % (x, c200, c150, v))
print()
print("RENDER eq5: column ink counts for the same frame-x range")
for x in range(600, 691):
    X = int(x*SX)
    c = int((r[int(456*SY):int(509*SY), X:X+2].mean(axis=2) < 200).sum())
    v = "INK" if c >= 3 else ("noise" if c > 0 else "")
    print("  %3d   %4d   %s" % (x, c, v))
