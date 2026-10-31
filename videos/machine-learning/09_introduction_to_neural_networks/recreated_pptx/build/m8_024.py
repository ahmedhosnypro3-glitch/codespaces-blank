#!/usr/bin/env python3
"""Slide 024: title glyph bbox + underline row extents; remember-box interior; P5 colours."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o = np.array(Image.open(V + "/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]
BG = np.array([232, 232, 230])

print("=== TITLE rows 58..95 (x 60..600) non-bg runs ===")
nb = np.abs(o - BG).sum(axis=2) > 40
nb[:, 64:70] = False   # kill frame left edge
for y in range(58, 96):
    xs = np.nonzero(nb[y, 70:600])[0]
    if len(xs):
        print(y, "x", xs.min()+70, "..", xs.max()+70, " n=", len(xs),
              " mean=", o[y, 70:600][nb[y, 70:600]].mean(axis=0).round(0))

print("\n=== TITLE underline candidate rows: saturated red x-extent ===")
sat = (r > 150) & (r - g > 90) & (r - b > 90)
for y in range(78, 100):
    xs = np.nonzero(sat[y, 70:600])[0]
    if len(xs) > 30:
        print(y, "x", xs.min()+70, "..", xs.max()+70, " n=", len(xs))

print("\n=== P2 remember interior sample colours (x 640..780, y 108..146) ===")
sub = o[108:146, 640:780].reshape(-1, 3)
# quantise
from collections import Counter
q = Counter((tuple((c // 32) * 32) for c in sub))
for k, v in q.most_common(8):
    print(" ", k, v)

print("\n=== P5 desc: word colour probe rows ===")
for yy in range(255, 350, 6):
    row = o[yy, 630:840]
    reds = np.nonzero(((row[:,0]-row[:,1] > 50) & (row[:,0]-row[:,2] > 50) & (row[:,0] > 150)))[0]
    blus = np.nonzero(((row[:,2]-row[:,0] > 30) & (row[:,2]-row[:,1] > 25)))[0]
    drk  = np.nonzero(((row.max(axis=1) < 110)))[0]
    def rng(a):
        return (a.min()+630, a.max()+630, len(a)) if len(a) else None
    print(yy, "RED", rng(reds), "BLUE", rng(blus), "DARK", rng(drk))
