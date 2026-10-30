#!/usr/bin/env python3
"""probe68 — locate any RED shaft ink between the outlier and the fitted line.

Frame: unique_slides/slide_009.jpg (960x540, 1 px = 1 pt).
Question: does the original carry a visible red dimension shaft from the outlier
down to the blue fitted line, and where exactly does the red segment live?
"""
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
img = Image.open(f"{ROOT}/unique_slides/slide_009.jpg").convert("RGB")
A = np.asarray(img).astype(int)
H, W, _ = A.shape
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]

# strong red ink (saturated red family), excluding pale rose / pink halos
strong = (r > 120) & (g < 80) & (b < 90) & ((r - g) > 60)

CHARTS = {
    "LEFT": dict(outlier=(197.5, 145.0), disc=(232.5, 241.0), disc_r=15.0,
                 blue=((141, 351), (433, 201)), box=(180, 130, 290, 310)),
    "RIGHT": dict(outlier=(611.0, 145.0), disc=None, disc_r=0.0,
                  blue=((555, 387), (849, 247)), box=(595, 130, 710, 345)),
}


def fit_segment(mask, box):
    x0, y0, x1, y1 = box
    m = np.zeros_like(mask)
    m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(m)
    if len(xs) < 8:
        return None
    pts = np.stack([xs, ys], 1).astype(float)
    c = pts.mean(0)
    u, s, vt = np.linalg.svd(pts - c, full_matrices=False)
    d = vt[0]
    ang = np.degrees(np.arctan2(d[1], d[0]))
    if ang < 0:
        ang += 180
    if ang > 90:
        ang -= 180
    t = (pts - c) @ d
    p0 = c + d * t.min()
    p1 = c + d * t.max()
    return dict(n=len(xs), ang=ang, p0=p0, p1=p1, xs=xs, ys=ys)


for name, cfg in CHARTS.items():
    ox, oy = cfg["outlier"]
    (bx0, by0), (bx1, by1) = cfg["blue"]
    dx, dy = bx1 - bx0, by1 - by0
    l2 = dx * dx + dy * dy

    def foot(px, py):
        t = ((px - bx0) * dx + (py - by0) * dy) / l2
        return bx0 + t * dx, by0 + t * dy

    fx, fy = foot(ox, oy)
    print(f"\n===== {name} =====")
    print(f"outlier ({ox},{oy})  blue {cfg['blue']}  foot on blue = ({fx:.2f},{fy:.2f})")
    ux, uy = fx - ox, fy - oy
    L = np.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    print(f"perp direction u=({ux:.5f},{uy:.5f})  angle={np.degrees(np.arctan2(uy,ux)):.2f} deg  len={L:.2f}")

    m = strong.copy()
    # kill the orange points family, the axes, the parallel streak zone, and the disc
    if cfg["disc"]:
        Y, X = np.mgrid[0:H, 0:W]
        m &= ~((X - cfg["disc"][0]) ** 2 + (Y - cfg["disc"][1]) ** 2 <= cfg["disc_r"] ** 2)
    # exclude a band around the blue line
    for yy in range(H):
        for xx in range(W):
            pass
    # corridor analysis: sample the shaft path (outlier -> foot) in 1px steps
    print("--- red ink sampled ALONG the perpendicular path (outlier -> foot) ---")
    for t in np.linspace(0, 1, 31):
        px, py = ox + ux * L * t, oy + uy * L * t
        xi, yi = int(round(px)), int(round(py))
        if 0 <= xi < W and 0 <= yi < H:
            print(f"  t={t:4.2f} ({px:7.2f},{py:7.2f}) rgb={tuple(A[yi,xi])} strong={bool(strong[yi,xi])}")

    # red pixels within 3px of the path
    Y, X = np.mgrid[0:H, 0:W]
    px_ = X - ox
    py_ = Y - oy
    tproj = (px_ * ux + py_ * uy)
    perp = np.abs(-px_ * uy + py_ * ux)
    onpath = (tproj > -3) & (tproj < L + 3) & (perp < 3.5)
    print(f"red pixels within 3.5px of path: {int((strong & onpath).sum())}")

    # fit any red segment in a window just BELOW the label band (label covers upper shaft)
    for lbl, box in [("window below label", (int(ox) - 5, int(oy) + 60, int(ox) + 110, int(oy) + 150)),
                     ("whole annotation box", cfg["box"])]:
        seg = fit_segment(strong & onpath, box)
        if seg is None:
            print(f"  [{lbl}] no red run")
        else:
            print(f"  [{lbl}] n={seg['n']} ang={seg['ang']:.2f} p0=({seg['p0'][0]:.1f},{seg['p0'][1]:.1f}) p1=({seg['p1'][0]:.1f},{seg['p1'][1]:.1f})")
