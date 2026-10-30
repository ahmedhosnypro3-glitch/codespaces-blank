#!/usr/bin/env python3
"""Probe 6 — exact color slices for the ambiguous structures.

Sampled on the ORIGINAL frame:
- y-axis columns (LEFT x124..130, RIGHT x538..544) at several y
- x-axis rows (y432..437) at several x
- LEFT green horizontal line rows y235..242
- RIGHT green dotted line rows y284..290
- green x-axis markers (LEFT (353,432), RIGHT (766,432)): full bbox dump
- point (242.5,327) horizontal + vertical color slices (outline check)
- orange point core color
"""
from PIL import Image
import sys

img_path, label = sys.argv[1], sys.argv[2]
im = Image.open(img_path).convert("RGB")
W, H = im.size
px = im.load()
print(f"== {label}: {img_path} {im.size}")

def dump_slice(desc, pts):
    print(f"   {desc}: " + " ".join(f"{p}={px[p[0], p[1]]}" for p in pts))

print("\n-- LEFT y-axis column slices --")
for y in (160, 200, 250, 300, 350, 400, 420, 430):
    dump_slice(f"y={y}", [(x, y) for x in range(123, 131)])

print("\n-- RIGHT y-axis column slices --")
for y in (160, 200, 250, 300, 350, 400, 420, 430):
    dump_slice(f"y={y}", [(x, y) for x in range(537, 545)])

print("\n-- LEFT x-axis row slices --")
for x in (200, 300, 400, 420, 426, 430, 432, 434):
    dump_slice(f"x={x}", [(x, y) for y in range(431, 438)])

print("\n-- RIGHT x-axis row slices --")
for x in (600, 700, 800, 836, 840, 844, 848):
    dump_slice(f"x={x}", [(x, y) for y in range(431, 438)])

print("\n-- LEFT green horizontal line (y235..242) --")
for x in (131, 140, 150, 170, 200, 250, 300, 340, 346):
    dump_slice(f"x={x}", [(x, y) for y in range(235, 243)])

print("\n-- RIGHT green dotted line (y283..291) --")
for x in (545, 550, 556, 560, 566, 600, 640, 700, 730):
    dump_slice(f"x={x}", [(x, y) for y in range(283, 292)])

print("\n-- LEFT green marker bbox (x348..359, y426..439) --")
for y in range(426, 440):
    row = []
    for x in range(348, 360):
        r, g, b = px[x, y]
        row.append(f"{x}:{r:3d},{g:3d},{b:3d}")
    print(f"   y={y}: " + " ".join(row))

print("\n-- RIGHT green marker bbox (x761..772, y426..439) --")
for y in range(426, 440):
    row = []
    for x in range(761, 773):
        r, g, b = px[x, y]
        row.append(f"{x}:{r:3d},{g:3d},{b:3d}")
    print(f"   y={y}: " + " ".join(row))

print("\n-- point (242.5,327) horizontal slice y=327 --")
dump_slice("y=327", [(x, 327) for x in range(237, 249)])
print("-- point (242.5,327) vertical slice x=242 --")
dump_slice("x=242", [(242, y) for y in range(322, 333)])
print("-- point (197.5,144.5) horizontal slice y=144 --")
dump_slice("y=144", [(x, 144) for x in range(192, 204)])

print("\n-- LEFT red dash near x325 (y283..300) --")
for y in range(283, 301, 2):
    dump_slice(f"y={y}", [(x, y) for x in range(322, 328)])

print("\n-- LEFT green vertical dash x352 (y240..250, y290..300) --")
for y in (243, 245, 247, 291, 293, 295):
    dump_slice(f"y={y}", [(x, y) for x in range(349, 357)])
