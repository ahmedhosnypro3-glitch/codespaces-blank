#!/usr/bin/env python3
"""Measure MAJOR element ink bboxes in the ORIGINAL 960x540 frame (1px = 1pt).

Only measures what the judge findings name: panel boxes, arctan in-panel title
inset, tan/tanh axis titles, connector arrow, tan asymptote lines, sigmoid legend.
"""
import os
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
V = os.path.join(ROOT, "videos/machine-learning/09_introduction_to_neural_networks")
im = Image.open(os.path.join(V, "unique_slides/slide_019.jpg")).convert("RGB")
W, H = im.size
px = im.load()
print(f"image {W}x{H}")


def bbox(pred, x0, y0, x1, y1):
    pts = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
           if pred(px[x, y])]
    if not pts:
        return None
    return (min(p[0] for p in pts), min(p[1] for p in pts),
            max(p[0] for p in pts), max(p[1] for p in pts), len(pts))


def is_bluepurple(c):
    r, g, b = c
    return b > 90 and b - r > 40 and b - g > 40 and r < 140


def is_ink(c, lo=60):
    r, g, b = c
    return r < lo and g < lo and b < lo


def is_rose_red(c):
    r, g, b = c
    return r > 140 and g < 120 and b < 130 and r - g > 40


# --- panel boxes (blue-purple border, ~2.5px) ---
print("\n== PANEL BOXES (blue-purple border ink) ==")
# scan for long vertical blue runs in columns outside plot interiors
for name, (gx0, gx1, gy0, gy1) in {
    "TL": (90, 420, 40, 280),
    "TR": (455, 790, 40, 280),
    "BL": (90, 420, 270, 500),
    "BR": (455, 790, 270, 500),
}.items():
    # vertical border candidates
    cols = {}
    for x in range(gx0, gx1):
        n = sum(1 for y in range(gy0, gy1) if is_bluepurple(px[x, y]))
        if n > 100:
            cols[x] = n
    print(f"{name}: strong vertical blue cols: {sorted(cols.items(), key=lambda t: -t[1])[:6]}")
    rows = {}
    for y in range(gy0, gy1):
        n = sum(1 for x in range(gx0, gx1) if is_bluepurple(px[x, y]))
        if n > 100:
            rows[y] = n
    print(f"    strong horizontal blue rows: {sorted(rows.items(), key=lambda t: -t[1])[:6]}")

# --- dark ink inside panels (axes, tick labels, titles) ---
print("\n== DARK INK (<60) INSIDE TOP-LEFT PANEL 98..386 x 57..230 ==")
b = bbox(lambda c: is_ink(c), 100, 60, 384, 228)
print("bbox:", b)
print("\n== DARK INK INSIDE TOP-RIGHT PANEL 470..757 x 57..230 ==")
b = bbox(lambda c: is_ink(c), 472, 60, 755, 228)
print("bbox:", b)
print("\n== DARK INK INSIDE BOTTOM-LEFT PANEL 98..386 x 290..463 ==")
b = bbox(lambda c: is_ink(c), 100, 293, 384, 461)
print("bbox:", b)
print("\n== DARK INK INSIDE BOTTOM-RIGHT PANEL 470..757 x 290..463 ==")
b = bbox(lambda c: is_ink(c), 472, 293, 755, 461)
print("bbox:", b)

# --- arctan in-panel title: 'Inverse Tangent Graph' — dark text near top-left of BR panel
print("\n== BR PANEL TOP-LEFT REGION dark ink rows (y 293..330) ==")
for y in range(292, 342, 2):
    xs = [x for x in range(476, 760) if is_ink(px[x, y], 80)]
    if xs:
        print(f"  y={y}: x {min(xs)}..{max(xs)} n={len(xs)}")

# --- connector arrow between bottom panels (gutter x 386..470, y 360..400)
print("\n== ARROW GUTTER x 386..470 ==")
b = bbox(lambda c: is_rose_red(c), 384, 330, 478, 430)
print("red ink bbox:", b)
for y in range(360, 405, 2):
    xs = [x for x in range(384, 478) if is_rose_red(px[x, y])]
    if len(xs) > 3:
        print(f"  y={y}: x {min(xs)}..{max(xs)} n={len(xs)}")

# --- tan panel asymptotes: vertical rose/red dashed lines inside BL panel
print("\n== BL PANEL vertical rose/red columns (asymptotes) ==")
for x in range(100, 385, 1):
    n = sum(1 for y in range(300, 460) if is_rose_red(px[x, y]))
    if n > 25:
        ys = [y for y in range(300, 460) if is_rose_red(px[x, y])]
        print(f"  x={x}: n={n} y {min(ys)}..{max(ys)}")

# --- sigmoid legend region (upper-left of TL panel)
print("\n== TL PANEL upper-left rose/red ink (legend swatch) x 110..190, y 70..95 ==")
b = bbox(lambda c: is_rose_red(c), 110, 70, 200, 100)
print("bbox:", b)
print("probe TL (130,82):", px[130, 82], " (120,80):", px[120, 80])
