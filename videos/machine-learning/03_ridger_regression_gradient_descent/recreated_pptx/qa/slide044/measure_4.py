#!/usr/bin/env python3
"""Region-by-region measurement of slide_044.jpg."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]

sample = np.median(IM[460:470, 300:330].reshape(-1, 3), axis=0)
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
PANEL = (np.abs(r - sample[0]) < 6) & (np.abs(g - sample[1]) < 6) & (np.abs(b - sample[2]) < 6)
nearwhite = (r > 235) & (g > 235) & (b > 235)
ink = ~PANEL & ~nearwhite
ink[:, :63] = False; ink[:, 898:] = False
ink[:48] = False; ink[535:] = False

def runs_1d(cnt, thr):
    out = []; inr = False; n = len(cnt)
    for i in range(n):
        if cnt[i] > thr and not inr:
            inr = True; a = i
        elif cnt[i] <= thr and inr:
            inr = False; out.append((a, i - 1))
    if inr: out.append((a, n - 1))
    return out

def col_bands(y0, y1, thr=6):
    print(f"\n--- COL BANDS rows {y0}..{y1} ---")
    sub = ink[y0:y1+1]
    cnt = sub.sum(axis=0)
    for x0, x1 in runs_1d(cnt, thr):
        blk = sub[:, x0:x1+1]
        if not blk.any():
            continue
        rows = np.where(blk.any(axis=1))[0]
        rgb = IM[y0:y1+1, x0:x1+1][blk]
        rr, gg, bb = rgb[:, 0].mean(), rgb[:, 1].mean(), rgb[:, 2].mean()
        print(f"  x {x0:>3}-{x1:<3} w{x1-x0+1:>3}  y {y0+rows.min()}..{y0+rows.max()} h{rows.max()-rows.min()+1:>3}  "
              f"px={int(blk.sum()):>5}  avg #{int(rr):02X}{int(gg):02X}{int(bb):02X}")

for y0, y1 in [(48, 130), (136, 266), (270, 330), (329, 410), (410, 475), (476, 534)]:
    col_bands(y0, y1)
