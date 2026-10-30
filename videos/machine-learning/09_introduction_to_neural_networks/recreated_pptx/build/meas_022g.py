"""Precise box edge + border color sampling for slide_022 original; also analyze zoom crops."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def hx(px):
    return "#%02x%02x%02x" % tuple(int(v) for v in px)

print("=== RGB samples along y=120 (row1, above text) ===")
for x in list(range(52, 96)) + list(range(470, 490)) + list(range(628, 648)) + list(range(858, 900)):
    print("  x=%3d %s" % (x, hx(a[120, x])))

print("\n=== RGB samples along y=250 (row2) at candidate edges ===")
for x in list(range(52, 96)) + list(range(470, 490)) + list(range(628, 648)) + list(range(858, 900)):
    print("  x=%3d %s" % (x, hx(a[250, x])))

print("\n=== row-profile of saturated-dark pixels in row1 (find box top/bottom) ===")
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = a.max(axis=2); mn = a.min(axis=2)
sat = mx - mn
dark = mx < 210
for x0, x1, lbl in [(87, 477, "left box"), (637, 869, "right box")]:
    print(" %s (x %d..%d):" % (lbl, x0, x1))
    for y in range(110, 209):
        seg = a[y, x0:x1]
        m = (seg.max(axis=1) < 215) & ((seg.max(axis=1) - seg.min(axis=1)) > 30)
        c = int(m.sum())
        if c > 100:
            print("    y=%3d  colored=%3d  %s" % (y, c, hx(seg[m].mean(axis=0))))
