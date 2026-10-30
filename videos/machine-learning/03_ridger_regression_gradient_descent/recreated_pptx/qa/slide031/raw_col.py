import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(DECK + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(DECK + "/recreated_pptx/qa/slide031/render_9.png").convert("RGB")).astype(int)
K = 1125 / 540.0

print("=== ORIGINAL: column x=573 raw colors, y=60..310 (only non-panelish) ===")
panelish = lambda c: abs(c[0]-233) < 12 and abs(c[1]-233) < 12 and abs(c[2]-231) < 12
for y in range(60, 312):
    c = o[y, 573]
    if not panelish(c):
        print("  y=%3d  %s" % (y, tuple(c)))
print()
print("=== ORIGINAL: column x=809 raw colors, y=60..310 ===")
for y in range(60, 312):
    c = o[y, 809]
    if not panelish(c):
        print("  y=%3d  %s" % (y, tuple(c)))
print()
print("=== ORIGINAL: row y=250 colors across x=565..815 (non-panel) ===")
for x in range(565, 816):
    c = o[250, x]
    if not panelish(c):
        print("  x=%3d  %s" % (x, tuple(c)))
