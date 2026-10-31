#!/usr/bin/env python3
"""Slide 024: per-panel red/blue/black ink bboxes + bottom strip check."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o = np.array(Image.open(V + "/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
H, W, _ = o.shape
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

RED   = (r > 110) & (r - g > 60) & (r - b > 60)
BLUE  = (b > 110) & (b - r > 40) & (b - g > 40)
BLACK = (r < 95) & (g < 95) & (b < 95)
YEL   = (r > 195) & (g > 165) & (g < 240) & (b < 135)

def report(name, x0, x1, y0, y1, mask):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if not len(xs):
        print(f"  {name}: none"); return
    print(f"  {name}: n={len(xs):5d} x={xs.min()+x0}..{xs.max()+x0} y={ys.min()+y0}..{ys.max()+y0}")

panels = [
    ("P1 sigmoid  78-310,100-152",  78, 310, 100, 152),
    ("P2 remember 592-800,100-148", 592, 800, 100, 148),
    ("P3 step1    78-620,158-227",  78, 620, 158, 227),
    ("P4 step2    78-575,235-375",  78, 575, 235, 375),
    ("P5 desc     600-840,240-360", 600, 840, 240, 360),
    ("P6 step3    78-465,393-470",  78, 465, 393, 470),
    ("P7 final    498-815,410-452", 498, 815, 410, 452),
]
for name, x0, x1, y0, y1 in panels:
    print(name)
    for lbl, m in (("RED", RED), ("BLUE", BLUE), ("BLACK", BLACK)):
        report(lbl, x0, x1, y0, y1, m)

print("\n=== per-row RED/BLUE ink detail in P3 step1 (x 78..620, y 158..227) ===")
for y in range(158, 228, 4):
    rs = np.nonzero(RED[y, 78:620])[0]
    bs = np.nonzero(BLUE[y, 78:620])[0]
    print(y, "RED", (rs.min()+78, rs.max()+78, len(rs)) if len(rs) else None,
             "BLUE", (bs.min()+78, bs.max()+78, len(bs)) if len(bs) else None)

print("\n=== per-row RED/BLUE detail P4 step2 (y 235..375) ===")
for y in range(236, 376, 5):
    rs = np.nonzero(RED[y, 78:575])[0]
    bs = np.nonzero(BLUE[y, 78:575])[0]
    print(y, "RED", (rs.min()+78, rs.max()+78, len(rs)) if len(rs) else None,
             "BLUE", (bs.min()+78, bs.max()+78, len(bs)) if len(bs) else None)

print("\n=== BOTTOM STRIP y 480..540 (mean color per row) ===")
for y in range(478, 540, 2):
    print(y, o[y].mean(axis=0).round(1))

print("\n=== YELLOW badge bbox ===")
ys, xs = np.nonzero(YEL)
if len(xs):
    print(f"x={xs.min()}..{xs.max()} y={ys.min()}..{ys.max()} n={len(xs)}")
    print("fill sample", "#%02x%02x%02x" % tuple(o[(ys.min()+ys.max())//2, (xs.min()+xs.max())//2]))
