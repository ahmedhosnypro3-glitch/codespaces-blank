#!/usr/bin/env python3
"""Text-line detection inside the top blue box (x72..715), with colour per cluster."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

PANEL = (np.abs(r - 233) < 9) & (np.abs(g - 232) < 9) & (np.abs(b - 231) < 9)
BG = (r > 236) & (g > 236) & (b > 205)
ink = ~PANEL & ~BG
ink[:, :63] = False; ink[:, 898:] = False
ink[:48] = False; ink[535:] = False

def runs(cnt, thr, gap=0):
    out = []; i = 0; n = len(cnt)
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
    if B > 110 and B - R > 40 and B - G > 25: return "BLUE"
    if R > 110 and R - G > 45 and R - B > 45: return "RED"
    if G > R + 18 and G > B + 18: return "GRN"
    if R < 140 and G < 140 and B < 140: return "blk"
    return "?"

def lines(x0, x1, y0, y1, label, thr=4, gap=4):
    print(f"\n### {label}  x{x0}..{x1} y{y0}..{y1}")
    sub = ink[y0:y1+1, x0:x1+1]
    rc = sub.sum(axis=1)
    for ly0, ly1 in runs(rc, thr, 0):
        band = ink[ly0:ly1+1, x0:x1+1]
        cc = band.sum(axis=0)
        clusters = []
        for a, bb in runs(cc, 1, 0):
            if bb - a < 2:
                continue
            blk = band[:, a:bb+1]
            rgb = IM[ly0:ly1+1, x0:x1+1][:, a:bb+1][blk]
            from collections import Counter
            ccc = Counter(classify(px) for px in rgb)
            clusters.append((x0 + a, x0 + bb, int(blk.sum()), ccc.most_common(2)))
        print(f"  LINE y{ly0}..{ly1} (h{ly1-ly0+1}) x{x0}..{x0+cc.shape[0]-1}")
        print("    " + "  ".join(f"[{a}-{b} p={p} {m}]" for a, b, p, m in clusters))

# inside the top box, excluding borders
lines(72, 715, 57, 125, "TOP BOX INTERIOR")
