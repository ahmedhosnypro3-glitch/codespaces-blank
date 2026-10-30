import numpy as np
from PIL import Image
ORIG = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_005.jpg"
REND = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/render_8.png"
o = np.asarray(Image.open(ORIG).convert("L")).astype(int)
r = np.asarray(Image.open(REND).convert("L")).astype(int)
SX, SY = 2001/960.0, 1125/540.0

print("=== ORIGINAL row profile, x678..762, y128..172 (what's in the Remember band?) ===")
for y in range(128, 173):
    row = o[y, 678:763]
    print("  y=%3d ink=%3d min=%3d" % (y, int((row < 200).sum()), row.min()))
print()
print("=== ORIGINAL row profile, x77..170, y286..340 (pinkfrac) ===")
for y in range(286, 341):
    row = o[y, 77:171]
    print("  y=%3d ink=%3d min=%3d" % (y, int((row < 200).sum()), row.min()))
