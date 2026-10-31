#!/usr/bin/env python3
"""Find the tick-label / axis-label glyph clusters inside each slide_021 panel,
restricted to the label zones (above top gridline, below bottom gridline,
left of left gridline, right of right gridline)."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

# per-panel: frame box, and measured gridline pixel coords
PANELS = {
    "TL": dict(f=(121, 109, 400, 272), gx=[163, 211.5, 260, 308.5, 356.5], gy=[124, 188.5, 253],
               xt=[-10, -5, 0, 5, 10], yt=[10, 5, 0]),
    "TR": dict(f=(563, 109, 842, 275), gx=[597, 621.5, 645.5, 669.5, 693.5, 717.5, 741.5, 765.5, 802.5],
               gy=[145, 157, 168.5, 204, 216, 228, 240, 263.5],
               xt=[-4, -2, 0, 2, 4], yt=[1, 2, 3, -1]),
    "BL": dict(f=(121, 346, 400, 508), gx=[159, 265, 371], gy=[358.5, 455.5, 486.5],
               xt=[-3, 0, 3], yt=[3, 1, -1]),
    "BR": dict(f=(564, 346, 842, 508), gx=[595.5, 659.5, 711.5, 777.5], gy=[357.5, 369, 381, 393],
               xt=[-4, -2, 0, 2], yt=[1, 2, 3]),
}


def clusters(mask, x0, y0, min_n=1):
    """4-connected clusters -> list of (x0,x1,y0,y1,n)."""
    H, W = mask.shape
    lab = np.zeros(mask.shape, int)
    cur = 0
    for yy in range(H):
        for xx in range(W):
            if mask[yy, xx] and lab[yy, xx] == 0:
                cur += 1
                stack = [(yy, xx)]
                lab[yy, xx] = cur
                while stack:
                    cy, cx = stack.pop()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur
                            stack.append((ny, nx))
    out = []
    for c in range(1, cur + 1):
        ys, xs = np.nonzero(lab == c)
        if len(xs) >= min_n:
            out.append((x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max(), len(xs)))
    return out


for name, p in PANELS.items():
    fx0, fy0, fx1, fy1 = p["f"]
    sub = a[fy0:fy1 + 1, fx0:fx1 + 1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    dark = (sr < 165) & (sg < 165) & (sb < 165) & \
           (np.maximum.reduce([sr, sg, sb]) - np.minimum.reduce([sr, sg, sb]) < 50)
    left, right = min(p["gx"]), max(p["gx"])
    top, bot = min(p["gy"]), max(p["gy"])
    zones = {
        "ABOVE": np.zeros_like(dark),
        "BELOW": np.zeros_like(dark),
        "LEFT": np.zeros_like(dark),
        "RIGHT": np.zeros_like(dark),
        "INSIDE": np.zeros_like(dark),
    }
    zones["ABOVE"][:int(round(top)) - fy0, :] = True
    zones["BELOW"][int(round(bot)) - fy0 + 1:, :] = True
    zones["LEFT"][:, :int(round(left)) - fx0] = True
    zones["RIGHT"][:, int(round(right)) - fx0 + 1:] = True
    zones["INSIDE"][int(round(top)) - fy0:int(round(bot)) - fy0 + 1,
                     int(round(left)) - fx0:int(round(right)) - fx0 + 1] = True
    print(f"\n=== {name} frame x{fx0}..{fx1} y{fy0}..{fy1}  grid x{left}..{right} y{top}..{bot}")
    for z, m in zones.items():
        cl = clusters(dark & m, fx0, fy0)
        print(f"  {z}: " + " ".join(f"({x0}..{x1},{y0}..{y1},n={n})" for x0, x1, y0, y1, n in sorted(cl, key=lambda c: (c[2], c[0]))))
