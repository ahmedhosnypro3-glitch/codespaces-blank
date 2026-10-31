#!/usr/bin/env python3
"""Measure slide_024 title ink extent + underline; panel fills/borders; body colors."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o = np.array(Image.open(V + "/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
H, W, _ = o.shape
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]
XS = np.arange(W)

def hx(y, x): return "#%02x%02x%02x" % (r[y, x], g[y, x], b[y, x])

# ---- TITLE: dark-red ink only, exclude frame line (x>=58) ----
print("=== TITLE ink (redness>60 & r>120), x<500 ===")
for y in range(60, 95):
    m = ((r - (g+b)/2) > 60) & (r > 120) & (XS > 60) & (XS < 560)
    xs = np.nonzero(m)[0]
    if len(xs):
        print(y, "x", xs.min(), "..", xs.max(), "n", len(xs))

print("\n=== underline scan y 83..95 : saturated red runs ===")
for y in range(83, 96):
    m = ((r - (g+b)/2) > 90) & (r > 150) & (XS > 60) & (XS < 400)
    xs = np.nonzero(m)[0]
    if len(xs):
        # contiguous run
        print(y, "x", xs.min(), "..", xs.max(), "n", len(xs), "color", hx(y, xs.min()))

# ---- PANEL fills: sample interior points from v2 regions ----
print("\n=== PANEL FILL SAMPLES ===")
regions = {
  "p1 sigmoid  78-310,100-152 (peach?)":   (126, 200),
  "p2 remember 592-800,100-148 (white?)":  (124, 700),
  "p3 step1    78-620,158-227 (white?)":   (192, 300),
  "p4 step2    78-575,235-375 (white?)":   (300, 300),
  "p5 desc     600-840,240-360 (peach?)":  (300, 700),
  "p6 step3    78-465,393-470 (white?)":   (430, 200),
  "p7 final    498-815,410-452 (peach?)":  (430, 650),
  "bg outside  600,60":                    (60, 600),
}
for k, (y, x) in regions.items():
    print(f"  {k:44s} -> {hx(y,x)}")

# ---- PANEL borders: scan up/down columns ----
print("\n=== BORDER colors (scan x=100 col, top->bottom) ===")
prev = None
for y in range(95, 180):
    c = hx(y, 100)
    if c != prev:
        print(y, c)
        prev = c
