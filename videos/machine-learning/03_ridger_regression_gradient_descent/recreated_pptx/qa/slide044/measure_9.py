#!/usr/bin/env python3
"""Corrected ink mask: background = gray panel OR near-white/cream.
Then per-line glyph-cluster analysis with colour classification."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

PANEL = (np.abs(r - 233) < 9) & (np.abs(g - 232) < 9) & (np.abs(b - 231) < 9)
BG = (r > 236) & (g > 236) & (b > 205)          # white + cream
ink = ~PANEL & ~BG
ink[:, :63] = False; ink[:, 898:] = False
ink[:48] = False; ink[535:] = False
print("content ink px:", ink.sum())

def runs(cnt, thr, gap=0):
    out = []
    i = 0; n = len(cnt)
    while i < n:
        if cnt[i] > thr:
            a = i; last = i; j = i + 1
            while j < n:
                if cnt[j] > thr:
                    last = j; j += 1
                elif all(cnt[k] <= thr for k in range(j, min(j + gap + 1, n))):
                    break
                else:
                    j += 1
            out.append((a, last)); i = last + 1
        else:
            i += 1
    return out

def classify(rgb):
    R, G, B = rgb
    if B > 110 and B - R > 40 and B - G > 25:
        return "BLUE"
    if R > 110 and R - G > 45 and R - B > 45:
        return "RED"
    if R > 200 and G > 200 and B < 190:
        return "YEL"
    if G > R + 18 and G > B + 18:
        return "GRN"
    if R < 140 and G < 140 and B < 140:
        return "blk"
    return "?"

def line_detail(y0, y1, label="", gap=5):
    print(f"\n### rows {y0}..{y1} ({label})")
    sub = ink[y0:y1+1]
    cnt = sub.sum(axis=0)
    for x0, x1 in runs(cnt, 1, gap):
        blk = sub[:, x0:x1+1]
        if not blk.any():
            continue
        rgb = IM[y0:y1+1, x0:x1+1][blk]
        from collections import Counter
        cc = Counter(classify(px) for px in rgb)
        rows = np.where(blk.any(axis=1))[0]
        top = cc.most_common(3)
        print(f"   x{x0:>3}-{x1:<3} w{x1-x0+1:>3} y{y0+rows.min()}..{y0+rows.max()} h{rows.max()-rows.min()+1:>2} "
              f"px={int(blk.sum()):>5} {[f'{k}:{v}' for k, v in top]}")

line_detail(58, 84, "TOP BOX line 1")
line_detail(104, 127, "TOP BOX line 2")
