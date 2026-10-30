#!/usr/bin/env python3
"""Detailed reconstruction: row bands -> column bands -> dominant colour,
with a fine 4px ASCII map of sub-regions."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

CORE = np.array([233, 232, 231])
PANEL = (np.abs(r - 233) < 8) & (np.abs(g - 232) < 8) & (np.abs(b - 231) < 8)

def cls(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if abs(R - 233) < 8 and abs(G - 232) < 8 and abs(B - 231) < 8:
        return "."
    if R > 240 and G > 240 and B > 240:
        return " "
    if R > 235 and G > 235 and B < 210:
        return "c"          # cream
    if R > 200 and G > 200 and B < 190:
        return "Y"
    if B > 110 and B - R > 40 and B - G > 25:
        return "B"
    if R > 110 and R - G > 45 and R - B > 45:
        return "R"
    if G > R + 18 and G > B + 18:
        return "G"
    if R < 140 and G < 140 and B < 140:
        return "#"
    return ":"

# fine ascii over the top box interior and other areas of interest
def ascii_map(x0, x1, y0, y1, cw=4, ch=4, label=""):
    print(f"\n=== {label} x{x0}..{x1} y{y0}..{y1} (cell {cw}x{ch}) ===")
    hdr1 = "".join(str((x0 + c * cw) // 100 % 10) for c in range((x1 - x0) // cw))
    hdr2 = "".join(str((x0 + c * cw) // 10 % 10) for c in range((x1 - x0) // cw))
    print("     " + hdr1)
    print("     " + hdr2)
    for yy in range(y0, y1, ch):
        line = ""
        for xx in range(x0, x1, cw):
            blk = IM[yy:yy+ch, xx:xx+cw].reshape(-1, 3)
            from collections import Counter
            cnt = Counter(cls(p) for p in blk)
            strong = {k: v for k, v in cnt.items() if k not in (".", " ")}
            if strong and max(strong.values()) >= 2:
                line += max(strong, key=strong.get)
            else:
                line += max(cnt, key=cnt.get)
        print(f"{yy:>4} {line}")

ascii_map(60, 730, 50, 135, 4, 4, "TOP BOX")
ascii_map(60, 260, 135, 270, 4, 4, "LEFT-MIDDLE TABLE")
