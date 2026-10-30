#!/usr/bin/env python3
"""Tighter measurement: sample panel core, then classify ink."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

# Sample the truly-empty panel region: x 300..330, y 460..470 should be bare panel
sample = IM[460:470, 300:330].reshape(-1, 3)
print("empty panel sample mean:", sample.mean(axis=0), "min", sample.min(axis=0), "max", sample.max(axis=0))

# Panel core measurement
core = np.median(sample, axis=0)
print("panel core median:", core, f"= #{int(core[0]):02X}{int(core[1]):02X}{int(core[2]):02X}")
# tight panel: within 6 of median per channel
PANEL = (np.abs(r - core[0]) < 6) & (np.abs(g - core[1]) < 6) & (np.abs(b - core[2]) < 6)
print("panel px tight:", PANEL.sum())
ys, xs = np.where(PANEL)
print("tight panel bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max())

# ink: NOT panel AND not near-white AND not near-black-bg
nearwhite = (r > 235) & (g > 235) & (b > 235)
ink = ~PANEL & ~nearwhite
# exclude the chrome strokes zone (x<63, x>899, y<48, y>535)
ink[:, :63] = False; ink[:, 898:] = False
ink[:48] = False; ink[535:] = False
print("content ink px:", ink.sum())

def runs_1d(cnt, thr):
    out = []; inr = False; n = len(cnt)
    for i in range(n):
        if cnt[i] > thr and not inr:
            inr = True; a = i
        elif cnt[i] <= thr and inr:
            inr = False; out.append((a, i - 1))
    if inr: out.append((a, n - 1))
    return out

print("\n=== ROW BANDS (thr=8) ===")
for y0, y1 in runs_1d(ink.sum(axis=1), 8):
    cols = np.where(ink[y0:y1+1].any(axis=0))[0]
    if len(cols):
        print(f"  y {y0:>3}-{y1:<3} (h{y1-y0+1:>3})  x {cols.min():>3}..{cols.max():>3}  px={int(ink[y0:y1+1].sum())}")

print("\n=== COL BANDS (thr=8) ===")
for x0, x1 in runs_1d(ink.sum(axis=0), 8):
    rows = np.where(ink[:, x0:x1+1].any(axis=1))[0]
    if len(rows):
        print(f"  x {x0:>3}-{x1:<3} (w{x1-x0+1:>3})  y {rows.min():>3}..{rows.max():>3}  px={int(ink[:,x0:x1+1].sum())}")
