#!/usr/bin/env python3
"""Numeric pixel probe for slide_013 original frame — definitive colors + edges."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_013.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

pts = [(450, 150), (600, 150), (700, 150), (800, 150), (660, 100),
       (538, 200), (540, 200), (545, 200), (615, 200), (618, 200), (620, 200),
       (625, 200), (650, 329), (650, 331), (650, 326),
       (270, 190), (270, 225), (270, 260), (270, 290), (250, 190), (300, 190),
       (120, 190), (200, 190),
       (350, 100), (350, 400), (450, 440), (700, 440), (780, 440),
       (470, 470), (640, 440), (80, 40), (500, 40)]
print("POINT PROBES (x,y) -> RGB")
for x, y in pts:
    print(f"  ({x:4d},{y:4d}) = #{a[y,x,0]:02X}{a[y,x,1]:02X}{a[y,x,2]:02X}")

print("\nSCAN ROW y=200 x=500..860 (runs of constant-ish color)")
prev, start = None, None
for x in range(500, 861):
    c = tuple((a[200, x] // 12 * 12).tolist())
    if c != prev:
        if prev is not None:
            print(f"  x{start}..{x-1} = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")
        prev, start = c, x
print(f"  x{start}..860 = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")

print("\nSCAN COL x=660 y=40..539 (runs)")
prev, start = None, None
for y in range(40, 540):
    c = tuple((a[y, 660] // 12 * 12).tolist())
    if c != prev:
        if prev is not None:
            print(f"  y{start}..{y-1} = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")
        prev, start = c, y
print(f"  y{start}..539 = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")

print("\nSCAN ROW y=190 x=85..330 (table)")
prev, start = None, None
for x in range(85, 331):
    c = tuple((a[190, x] // 16 * 16).tolist())
    if c != prev:
        if prev is not None:
            print(f"  x{start}..{x-1} = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")
        prev, start = c, x
print(f"  x{start}..330 = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")

print("\nSCAN COL x=275 y=130..320 (O/P column)")
prev, start = None, None
for y in range(130, 321):
    c = tuple((a[y, 275] // 16 * 16).tolist())
    if c != prev:
        if prev is not None:
            print(f"  y{start}..{y-1} = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")
        prev, start = c, y
print(f"  y{start}..320 = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")

print("\nSCAN COL x=450 y=400..530 (callout)")
prev, start = None, None
for y in range(400, 531):
    c = tuple((a[y, 450] // 16 * 16).tolist())
    if c != prev:
        if prev is not None:
            print(f"  y{start}..{y-1} = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")
        prev, start = c, y
print(f"  y{start}..530 = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")

print("\nSCAN ROW y=440 x=560..900 (callout row)")
prev, start = None, None
for x in range(560, 901):
    c = tuple((a[440, x] // 16 * 16).tolist())
    if c != prev:
        if prev is not None:
            print(f"  x{start}..{x-1} = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")
        prev, start = c, x
print(f"  x{start}..900 = #{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}")

# near-white plot panel bbox (all channels > 244) inside x 400..930
nw = (a[:, :, 0] > 244) & (a[:, :, 1] > 244) & (a[:, :, 2] > 244)
reg = np.zeros((H, W), bool)
reg[60:420, 400:940] = True
m = nw & reg
ys, xs = np.where(m)
print(f"\nNEAR-WHITE plot panel bbox: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)}")

# pinkish-white (peach) bbox in plot area
pk = (a[:, :, 0] > 240) & (a[:, :, 1] > 230) & (a[:, :, 1] < 250) & \
     (a[:, :, 2] > 230) & (a[:, :, 2] < 250) & (a[:, :, 0] - a[:, :, 1] > 6)
m = pk & reg
ys, xs = np.where(m)
if len(xs):
    print(f"PINKISH plot area bbox: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)}")
