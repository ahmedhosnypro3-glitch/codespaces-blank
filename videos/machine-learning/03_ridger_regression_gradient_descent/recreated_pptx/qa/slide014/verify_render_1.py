#!/usr/bin/env python3
"""Verify render_1.png band positions against measured original geometry."""
import numpy as np
from PIL import Image

rv = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/render_1.png"
).convert("RGB")).astype(int)
H, W = rv.shape[:2]
sc = W / 960.0
print(f"render {W}x{H}, scale {sc:.4f} render-px per frame-px")

r, g, b = rv[:, :, 0], rv[:, :, 1], rv[:, :, 2]

# yellow band FFF9C4
yel = (r > 240) & (g > 240) & (b > 200) & (b < 240) & (r - b > 15)
rows = np.where(yel.sum(axis=1) > 400)[0]
if len(rows):
    print(f"Yellow band rows {rows.min()}-{rows.max()} (frame px {rows.min()/sc:.1f}-{rows.max()/sc:.1f})")
    d = np.diff(rows); splits = np.where(d > 5)[0]
    start = rows[0]
    groups = []
    prev = rows[0]
    for y in rows[1:]:
        if y - prev > 5:
            groups.append((start, prev)); start = y
        prev = y
    groups.append((start, prev))
    for a, c in groups:
        print(f"  yellow band y {a}-{c} -> frame {a/sc:.1f}..{c/sc:.1f}")

# pink FFEBEE - broader detection
pink = (r > 240) & (g > 220) & (g < 250) & (b > 220) & (b < 250)
rows = np.where(pink.sum(axis=1) > 400)[0]
if len(rows):
    print(f"Pink band rows {rows.min()}-{rows.max()} (frame {rows.min()/sc:.1f}-{rows.max()/sc:.1f})")
else:
    print("Pink band: NOT FOUND with threshold >400")

# light blue E1F5FE
lb = (r > 215) & (r < 240) & (g > 235) & (b > 240)
rows = np.where(lb.sum(axis=1) > 400)[0]
if len(rows):
    print(f"Light blue band rows {rows.min()}-{rows.max()} (frame {rows.min()/sc:.1f}-{rows.max()/sc:.1f})")
    start, prev = rows[0], rows[0]
    groups = []
    for y in rows[1:]:
        if y - prev > 5:
            groups.append((start, prev)); start = y
        prev = y
    groups.append((start, prev))
    for a, c in groups:
        print(f"  blue band y {a}-{c} -> frame {a/sc:.1f}..{c/sc:.1f}")

# Check panel gray
gray = (np.abs(r - 233) < 20) & (np.abs(g - 233) < 20) & (np.abs(b - 231) < 20)
rows = np.where(gray.sum(axis=1) > 800)[0]
if len(rows):
    print(f"Panel gray rows {rows.min()}-{rows.max()} (frame {rows.min()/sc:.1f}-{rows.max()/sc:.1f})")

# Check red strokes
red = (r > 80) & ((r - g) > 30) & ((r - b) > 30)
rows = np.where(red.sum(axis=1) > 50)[0]
if len(rows):
    print(f"Red strokes rows {rows.min()}-{rows.max()} (frame {rows.min()/sc:.1f}-{rows.max()/sc:.1f})")
    bot = rows[rows > int(530*sc)]
    if len(bot):
        print(f"  bottom stroke: frame ~{bot.min()/sc:.1f}")
    left = red[int(270*sc):int(275*sc), :int(70*sc)].sum()
    right = red[int(270*sc):int(275*sc), int(880*sc):].sum()
    print(f"  left stroke mid: {left}, right: {right}")

# Check badge
yel_b = (r > 200) & (g > 200) & (b < 120)
ys = np.where(yel_b)
if len(ys[0]):
    cx = ys[1].mean()
    cy = ys[0].mean()
    print(f"Badge yellow center: render ({cx:.0f},{cy:.0f}) -> frame ({cx/sc:.1f},{cy/sc:.1f})")

# Title area
print("\nTitle area y 50..100 render:")
for y in range(50, 100, 5):
    prof = (np.abs(rv[y, 60:1000] - 255).max(axis=1) > 30).sum()
    if prof > 10:
        print(f"  y={y}: ink={prof}")