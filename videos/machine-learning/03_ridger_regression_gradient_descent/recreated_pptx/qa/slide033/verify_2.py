#!/usr/bin/env python3
"""Compare render_2.png against the original frame element-by-element."""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033/render_2.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
S = r.shape[0] / 540.0
print(f"scale render/frame = {S:.4f}")


def cv(v):
    return int(round(v * S))


def occ_report(name, x0, y0, x1, y1):
    """ink census (saturated + dark) in a frame-space window for both images"""
    for tag, im in (("ORIG", o), ("REND", r)):
        H, W = im.shape[:2]
        sc = H / 540.0
        sub = im[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]
        rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
        mx = np.maximum(np.maximum(rr, gg), bb)
        mn = np.minimum(np.minimum(rr, gg), bb)
        sat = mx - mn
        dark = mx < 110
        ink = int(((sat > 45) | dark).sum())
        print(f"  {name:>16} {tag}: ink={ink:>6}  ({100*ink/max(1,sub[:,:,0].size):.1f}%)  win={sub.shape[1]}x{sub.shape[0]}")
    print()


print("=== Region ink occupancy (orig vs render) ===")
occ_report("title", 185, 58, 460, 95)
occ_report("subtitle L1", 115, 92, 510, 115)
occ_report("subtitle L2", 300, 114, 800, 146)
occ_report("param box", 75, 245, 175, 309)
occ_report("center callout", 244, 252, 599, 301)
occ_report("plot area", 600, 58, 905, 325)
occ_report("table band0", 86, 332, 870, 368)
occ_report("table band1", 86, 376, 870, 410)
occ_report("table band2", 86, 420, 870, 455)
occ_report("table band3", 86, 458, 870, 479)
occ_report("table band4", 86, 482, 870, 504)

print("=== Measured band fills on the RENDER vs ORIGINAL ===")
bands = [(332, 368), (376, 410), (420, 455), (458, 479), (482, 504)]
for y0, y1 in bands:
    # original fill: mode over bright pixels
    from collections import Counter
    for tag, im in (("ORIG", o), ("REND", r)):
        H = im.shape[0]
        sc = H / 540.0
        sub = im[int(y0 * sc):int(y1 * sc), int(150 * sc):int(820 * sc):int(4 * sc)].reshape(-1, 3)
        sub = sub[sub.sum(axis=1) > 400]
        if len(sub):
            dom = Counter(map(tuple, sub)).most_common(1)[0][0]
            print(f"  band y{y0}-{y1} {tag}: fill #{dom[0]:02X}{dom[1]:02X}{dom[2]:02X}")
    print()

print("=== Curve smoothness on the render (2nd-difference ripple) ===")
g_r, g_g, g_b = r[:, :, 0], r[:, :, 1], r[:, :, 2]
green = (g_g - g_r > 18) & (g_g - g_b > 18) & (g_g > 80)
col = {}
ys_, xs_ = np.where(green[int(100 * S):int(300 * S), int(600 * S):int(860 * S)])
for y, x in zip(ys_, xs_):
    col.setdefault(int(x), []).append(int(y) + int(100 * S))
if len(col) > 30:
    xs = sorted(col)
    cy = np.array([np.median(col[x]) for x in xs], dtype=float)
    d2 = np.diff(cy, 2)
    print(f"  curve cols {xs[0]}..{xs[-1]} ({len(xs)} cols, render px)")
    print(f"  second-difference std = {np.std(d2):.3f} px, max|d2| = {np.abs(d2).max():.3f} px")
    print(f"  y range: {cy.min():.0f}..{cy.max():.0f} render px -> frame "
          f"{cy.min()/S:.0f}..{cy.max()/S:.0f}")
else:
    print(f"  only {len(col)} curve columns — TOO SPARSE / not drawn as one curve")

print("\n=== Match of table vertical gridlines (frame px) ===")
# expected grid: 121 + k*40 ; render gridlines drawn at the same
print("  expected (frame px):", [121 + k * 40 for k in range(20)])
