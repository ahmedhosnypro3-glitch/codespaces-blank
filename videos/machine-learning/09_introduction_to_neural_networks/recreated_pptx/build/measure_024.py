#!/usr/bin/env python3
"""Measure slide_024 original frame: box borders + per-box ink bboxes -> slide inches."""
from PIL import Image
import numpy as np, sys

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o = np.array(Image.open(V + "/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
H, W, _ = o.shape

# calibration: red frame left/right x, top/bottom y  (measured separately)
FRAME_L, FRAME_R, FRAME_T, FRAME_B = 58.0, 902.0, 44.0, 517.0
SX = (FRAME_R - FRAME_L) / 13.03
SY = (FRAME_B - FRAME_T) / 7.2
OX = FRAME_L - 0.15 * SX
OY = FRAME_T - 0.15 * SY
def inx(x): return (x - OX) / SX
def iny(y): return (y - OY) / SY
print(f"scale x={SX:.2f} y={SY:.2f} px/in ; origin=({OX:.1f},{OY:.1f})")

r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]
redness = r - (g + b) / 2

def mask_peach():
    return (r > 243) & (g > 215) & (g < 246) & (b > 195) & (b < 240) & (r - g > 12) & (g - b > 8)
def mask_blue():
    return (b > 200) & (b - r > 6) & (g > 200) & (r < 240)
def mask_white():
    return (r > 246) & (g > 246) & (b > 246)
def mask_redink():
    return (redness > 70) & (r > 120)
def mask_blueink():
    return (b - r > 25) & (b > 120) & (g < 200)
def mask_blackink():
    return (r < 90) & (g < 90) & (b < 90)

def spans(mask, y, minlen=8):
    row = mask[y]; out = []; st = None
    for x in range(W):
        if row[x] and st is None: st = x
        elif not row[x] and st is not None:
            if x - st >= minlen: out.append((st, x - 1))
            st = None
    if st is not None and W - st >= minlen: out.append((st, W - 1))
    return out

print("\n=== peach fill row extents (y where count>60) ===")
P = mask_peach()
for y in range(40, 520):
    s = spans(P, y, 20)
    if s and sum(e - st for st, e in s) > 60:
        print(y, s)
