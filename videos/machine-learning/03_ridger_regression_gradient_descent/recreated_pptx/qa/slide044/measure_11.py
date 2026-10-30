#!/usr/bin/env python3
"""Luminance + colour ink masks. Report per text line the glyph clusters
with colour class, inside/outside the blue box."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf

# real ink: dark (below both panel 232 and cream 252) OR strongly saturated
dark = LUM < 195
satred = (rf - gf > 45) & (rf - bf > 45) & (rf > 110)
satblue = (bf - rf > 40) & (bf - gf > 25) & (bf > 110)
satyel = (rf > 200) & (gf > 200) & (bf < 190)
ink = dark | satred | satblue
ink[:, :63] = False; ink[:, 898:] = False
ink[:48] = False; ink[535:] = False
print("ink px:", int(ink.sum()), "dark:", int(dark.sum()),
      "satred:", int(satred.sum()), "satblue:", int(satblue.sum()))

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

def classify(px):
    R, G, B = px
    if B > 110 and B - R > 40 and B - G > 25: return "BLUE"
    if R > 110 and R - G > 45 and R - B > 45: return "RED"
    if R > 200 and G > 200 and B < 190: return "YEL"
    if R < 140 and G < 140 and B < 140: return "blk"
    return "?"

def lines(x0, x1, y0, y1, label, lthr=4):
    print(f"\n### {label}  x{x0}..{x1} y{y0}..{y1}")
    rc = ink[y0:y1+1, x0:x1+1].sum(axis=1)
    for ly0, ly1 in runs(rc, lthr, 0):
        band = ink[ly0:ly1+1, x0:x1+1]
        cc = band.sum(axis=0)
        cl = []
        for a, bb in runs(cc, 1, 0):
            if bb - a < 2:
                continue
            blk = band[:, a:bb+1]
            rgb = IM[ly0:ly1+1, x0:x1+1][:, a:bb+1][blk]
            from collections import Counter
            cl.append((x0+a, x0+bb, int(blk.sum()), Counter(classify(p) for p in rgb).most_common(2)))
        print(f"  LINE y{ly0}..{ly1} h{ly1-ly0+1} nclust={len(cl)}")
        print("    " + "  ".join(f"[{a}-{b} p{p} {m}]" for a, b, p, m in cl))

# The top blue box interior (x72..715, y57..125) minus borders
lines(72, 715, 60, 123, "TOP BOX INTERIOR")
