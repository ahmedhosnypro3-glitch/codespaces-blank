#!/usr/bin/env python3
"""Probe slide_008.jpg: element extents, colors, edges in slide inches (960x540 -> 13.33x7.5in)."""
from PIL import Image
import numpy as np

im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
SX = 13.333 / W
SY = 7.5 / H
print(f"image {W}x{H}, scale x={SX:.5f} y={SY:.5f}")

def rgba(px):
    r, g, b = px
    return f"#{r:02X}{g:02X}{b:02X}"

def probe(name, y, x):
    print(f"  {name:30s} ({x:4d},{y:3d}) -> ({x*SX:.2f}in, {y*SY:.2f}in) {rgba(a[y,x])}")

# Background
print("corners:", rgba(a[5,5]), rgba(a[5,W-5]), rgba(a[H-5,5]), rgba(a[H-5,W-5]))

# --- locate red plot border: scan for strong red large rectangles
red = (a[:,:,0] > 150) & (a[:,:,1] < 90) & (a[:,:,2] < 90)
ys, xs = np.where(red)
print(f"red pixels: n={len(ys)} bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
if len(ys):
    print(f"  red bbox in inches: x[{xs.min()*SX:.2f},{xs.max()*SX:.2f}] y[{ys.min()*SY:.2f},{ys.max()*SY:.2f}]")

# row profile of red count to find border lines
rowcnt = red.sum(axis=1)
colcnt = red.sum(axis=0)
rows = np.where(rowcnt > W*0.3)[0]
cols = np.where(colcnt > H*0.3)[0]
print("red-dominant rows:", rows[:20], "..." if len(rows)>20 else "")
print("red-dominant cols:", cols[:20], "..." if len(cols)>20 else "")

# --- white plot fill region
white = (a[:,:,0] > 240) & (a[:,:,1] > 240) & (a[:,:,2] > 240)
wys, wxs = np.where(white)
print(f"white pixels: n={len(wys)} bbox x[{wxs.min()},{wxs.max()}] y[{wys.min()},{wys.max()}]")
print(f"  white bbox inches: x[{wxs.min()*SX:.2f},{wxs.max()*SX:.2f}] y[{wys.min()*SY:.2f},{wys.max()*SY:.2f}]")

# --- colnt profiles for key color families to locate clusters/lines
def color_profile(name, mask):
    ys_, xs_ = np.where(mask)
    if not len(ys_):
        print(f"{name}: none")
        return None
    cx, cy = int(xs_.mean()), int(ys_.mean())
    print(f"{name:28s} n={len(ys_):6d} bbox x[{xs_.min():4d},{xs_.max():4d}] y[{ys_.min():3d},{ys_.max():3d}] centroid ({cx},{cy}) in ({cx*SX:.2f},{cy*SY:.2f}) {rgba(a[cy,cx])}")
    return (xs_.min(), xs_.max(), ys_.min(), ys_.max())

color_profile("green (C1 dots/line)", (a[:,:,1] > 150) & (a[:,:,0] < 120) & (a[:,:,2] < 120))
color_profile("blue (C2/line)", (a[:,:,2] > 150) & (a[:,:,0] < 120) & (a[:,:,1] < 150))
color_profile("red-dark (C3/line)", (a[:,:,0] > 140) & (a[:,:,1] < 80) & (a[:,:,2] < 80))
color_profile("yellow boxes", (a[:,:,0] > 220) & (a[:,:,1] > 200) & (a[:,:,2] < 100))
color_profile("orange boxes", (a[:,:,0] > 200) & (a[:,:,1] > 110) & (a[:,:,1] < 180) & (a[:,:,2] < 60))
color_profile("purple box", (a[:,:,0] > 180) & (a[:,:,2] > 180) & (a[:,:,1] < 150))
color_profile("palegreen box", (a[:,:,0] > 190) & (a[:,:,1] > 230) & (a[:,:,2] < 220) & (a[:,:,2] > 180))

# grid sample of the slide for layout feel
print("\nvertical strips (mean rgb every 10% width):")
for i in range(0, 11):
    x = int(W * i / 10)
    col = a[:, x:x+10].reshape(-1,3).mean(axis=0)
    print(f"  x={i*10:3d}% mean {rgba(col.astype(int))}")
print("horizontal strips:")
for i in range(0, 11):
    y = int(H * i / 10)
    row = a[y:y+5, :].reshape(-1,3).mean(axis=0)
    print(f"  y={i*10:3d}% mean {rgba(row.astype(int))}")
