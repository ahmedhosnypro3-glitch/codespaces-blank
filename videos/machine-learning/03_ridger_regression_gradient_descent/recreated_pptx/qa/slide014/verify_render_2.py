#!/usr/bin/env python3
"""More detailed render verification."""
import numpy as np
from PIL import Image

rv = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/render_1.png"
).convert("RGB")).astype(int)
H, W = rv.shape[:2]
sc = W / 960.0
r, g, b = rv[:, :, 0], rv[:, :, 1], rv[:, :, 2]

# yellow band - lower threshold
yel = (r > 240) & (g > 240) & (b > 200) & (b < 240) & (r - b > 15)
rows = np.where(yel.sum(axis=1) > 100)[0]
if len(rows):
    print(f"Yellow band rows {rows.min()}-{rows.max()} (frame px {rows.min()/sc:.1f}-{rows.max()/sc:.1f})")
    start, prev = rows[0], rows[0]
    groups = []
    for y in rows[1:]:
        if y - prev > 5:
            groups.append((start, prev)); start = y
        prev = y
    groups.append((start, prev))
    for a, c in groups:
        print(f"  yellow band y {a}-{c} -> frame {a/sc:.1f}..{c/sc:.1f}")

# Check red strokes at mid-height
red = (r > 80) & ((r - g) > 30) & ((r - b) > 30)
mid_y = slice(int(270*sc)-20, int(270*sc)+20)
left_red = red[mid_y, :int(70*sc)].sum()
right_red = red[mid_y, int(880*sc):].sum()
print(f"\nLeft stroke mid: {left_red} px, Right stroke mid: {right_red} px")

# Check top band for red (should be NONE)
top_band = red[int(44*sc):int(52*sc), int(80*sc):int(880*sc)].sum()
print(f"Top band red px: {top_band} (should be low/zero)")

# Check title area
print("\nTitle area (y 50..150 render = frame 24..72):")
for y in range(50, 150, 10):
    prof = (np.abs(rv[y, 60:1000] - 255).max(axis=1) > 30).sum()
    if prof > 10:
        print(f"  y={y}: ink={prof}")

# Check vector boxes area y 250..500 render
print("\nVector boxes area (y 250..500 render = frame 120..240):")
for y in range(250, 500, 50):
    prof = (np.abs(rv[y, 60:1000] - 255).max(axis=1) > 30).sum()
    print(f"  y={y}: ink={prof}")

# Black border on left/right boxes
print("\nBlack borders in vector box band (y 300..400 render = 144..192 frame):")
blk = (rv.max(axis=2) < 100)
for y in range(300, 400, 20):
    row = blk[y, :int(500*sc)]
    if row.sum() > 100:
        cols = np.where(row)[0]
        print(f"  y={y}: black x {cols.min()}-{cols.max()} -> frame {cols.min()/sc:.1f}-{cols.max()/sc:.1f}")

# Badge
yel_b = (r > 200) & (g > 200) & (b < 120)
ys = np.where(yel_b)
if len(ys[0]):
    cx, cy = ys[1].mean(), ys[0].mean()
    print(f"\nBadge yellow center: ({cx:.0f},{cy:.0f}) -> frame ({cx/sc:.1f},{cy/sc:.1f})")

# Purple ring
pur = (b > 140) & (r > 80) & (r < 180) & (g < 130)
ys = np.where(pur)
if len(ys[0]):
    cx, cy = ys[1].mean(), ys[0].mean()
    print(f"Badge purple center: ({cx:.0f},{cy:.0f}) -> frame ({cx/sc:.1f},{cy/sc:.1f})")