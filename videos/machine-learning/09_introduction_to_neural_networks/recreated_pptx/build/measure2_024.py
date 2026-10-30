#!/usr/bin/env python3
"""Full geometry measurement of slide_024 original frame."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o = np.array(Image.open(V + "/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
H, W, _ = o.shape
FRAME_L, FRAME_R, FRAME_T, FRAME_B = 58.0, 902.0, 44.0, 517.0
SX = (FRAME_R - FRAME_L) / 13.03
SY = (FRAME_B - FRAME_T) / 7.2
OX, OY = FRAME_L - 0.15 * SX, FRAME_T - 0.15 * SY
def inx(x): return (x - OX) / SX
def iny(y): return (y - OY) / SY

r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]
redness = r - (g + b) / 2

def hx(y, x): return "#%02x%02x%02x" % (r[y, x], g[y, x], b[y, x])

# ---- 1. badge (yellow circle) ----
yellow = (r > 200) & (g > 170) & (g < 235) & (b < 130) & (r - g > 20)
ys, xs = np.nonzero(yellow)
print(f"YELLOW badge px: n={len(xs)} bbox x={xs.min()}..{xs.max()} y={ys.min()}..{ys.max()}")
print(f"  -> slide inches x={inx(xs.min()):.3f}..{inx(xs.max()):.3f}  y={iny(ys.min()):.3f}..{iny(ys.max()):.3f}")
print(f"  center=({(inx(xs.min())+inx(xs.max()))/2:.3f},{(iny(ys.min())+iny(ys.max()))/2:.3f}) size={inx(xs.max())-inx(xs.min()):.3f}x{iny(ys.max())-iny(ys.min()):.3f}")
# badge fill sample
cy, cx = (ys.min() + ys.max()) // 2, (xs.min() + xs.max()) // 2
print(f"  fill sample {hx(cx and cy, cx)}")

# ---- 2. background gray sample ----
print("bg sample:", hx(500, 300), hx(40, 300), hx(200, 700))

# ---- 3. per-row ink extents per box, tight borders ----
def spans(row, minlen=6):
    out = []; st = None
    for x in range(W):
        if row[x] and st is None: st = x
        elif not row[x] and st is not None:
            if x - st >= minlen: out.append((st, x - 1))
            st = None
    if st is not None and W - st >= minlen: out.append((st, W - 1))
    return out

notbg = np.abs(o - np.array([232, 232, 230])).sum(axis=2) > 30
for name, y0, y1 in [("rowA", 99, 160), ("rowB", 159, 240), ("rowC", 247, 392), ("rowD", 409, 492)]:
    print(f"\n=== {name} y={y0}..{y1} : outer non-bg extents ===")
    for y in range(y0, y1, 6):
        s = spans(notbg[y], 12)
        print(y, [(a, b, round(inx(a), 2), round(inx(b), 2)) for a, b in s])
