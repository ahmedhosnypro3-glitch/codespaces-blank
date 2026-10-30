"""Definitive structure: vertical strokes with RGB, per-row, for slide_022 original."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def hx(px):
    return "#%02x%02x%02x" % tuple(int(v) for v in px)

mx = a.max(axis=2); mn = a.min(axis=2)
sat = mx - mn
dark = mx < 215
# "stroked" = dark enough AND saturated enough to be a colored border line
stroke = dark & (sat > 25)

print("=== vertical strokes (col has >40 dark-saturated px within content band) ===")
band = slice(110, 504)
colhits = stroke[band].sum(axis=0)
for x in range(W):
    if colhits[x] > 40:
        col = a[band, x][stroke[band, x]]
        print("  x=%3d hits=%3d  median=%s  n=%d" % (x, colhits[x], hx(np.median(col, axis=0)), len(col)))

print("\n=== horizontal strokes (row has >100 dark-saturated px) ===")
for y in range(H):
    r = stroke[y].sum()
    if r > 100:
        seg = a[y][stroke[y]]
        print("  y=%3d hits=%3d  median=%s" % (y, r, hx(np.median(seg, axis=0))))

print("\n=== vertical stroke detail within row1 only (y 110..208) ===")
b1 = slice(110, 208)
for x in range(W):
    if stroke[b1, x].sum() > 30:
        col = a[b1, x][stroke[b1, x]]
        print("  x=%3d hits=%3d median=%s" % (x, stroke[b1, x].sum(), hx(np.median(col, axis=0))))

print("\n=== vertical stroke detail within row4 only (y 404..503) ===")
b4 = slice(404, 503)
for x in range(W):
    if stroke[b4, x].sum() > 25:
        col = a[b4, x][stroke[b4, x]]
        print("  x=%3d hits=%3d median=%s" % (x, stroke[b4, x].sum(), hx(np.median(col, axis=0))))
