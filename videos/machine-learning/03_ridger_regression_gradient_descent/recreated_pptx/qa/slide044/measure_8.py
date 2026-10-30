#!/usr/bin/env python3
"""For each row band, list ink column-runs with dominant colour.
Text lines resolve into glyph clusters this way."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

PANEL = (np.abs(r - 233) < 8) & (np.abs(g - 232) < 8) & (np.abs(b - 231) < 8)
WHITE = (r > 238) & (g > 238) & (b > 238)
ink = ~PANEL & ~WHITE
ink[:, :63] = False; ink[:, 898:] = False
ink[:48] = False; ink[535:] = False

def runs_1d(cnt, thr, gap=0):
    out = []
    i = 0
    n = len(cnt)
    while i < n:
        if cnt[i] > thr:
            a = i
            last = i
            j = i + 1
            while j < n:
                if cnt[j] > thr:
                    last = j
                elif all(cnt[k] <= thr for k in range(j, min(j + gap + 1, n))):
                    break
                j += 1
            out.append((a, last))
            i = last + 1
        else:
            i += 1
    return out

def line_detail(y0, y1, label="", gap=6):
    print(f"\n### rows {y0}..{y1}  ({label})")
    sub = ink[y0:y1+1]
    for x0, x1 in runs_1d(sub.sum(axis=0), 1, gap):
        blk = sub[:, x0:x1+1]
        rgb = IM[y0:y1+1, x0:x1+1][blk]
        rr, gg, bb = rgb[:, 0].mean(), rgb[:, 1].mean(), rgb[:, 2].mean()
        rows = np.where(blk.any(axis=1))[0]
        print(f"   x{x0:>3}-{x1:<3} w{x1-x0+1:>3} y{y0+rows.min()}..{y0+rows.max()} h{rows.max()-rows.min()+1:>2} "
              f"px={int(blk.sum()):>4} avg #{int(rr):02X}{int(gg):02X}{int(bb):02X}")

# inner box y54..130: text lines
line_detail(60, 82, "TOP BOX line 1")
line_detail(104, 126, "TOP BOX line 2")
