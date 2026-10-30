#!/usr/bin/env python3
"""Robust line + arrowhead extraction for slide 007 decision lines and axes."""
import json

import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_007_lines_v2.json"

im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

PX0, PX1, PY0, PY1 = 156, 757, 115, 477

red = (r > 150) & (g < 110) & (b < 110) & (r - g > 70) & (r - b > 70)
blue = (b > 120) & (r < 130) & (b - r > 55) & (b - g > 45)
green = (g > 95) & (r < 135) & (b < 135) & (g - r > 40) & (g - b > 40)


def panelize(m):
    out = np.zeros_like(m)
    out[PY0:PY1, PX0:PX1] = m[PY0:PY1, PX0:PX1]
    return out


def remove_blobs(m, min_px=90, max_dim=26):
    lab, n = ndimage.label(m)
    out = np.zeros_like(m)
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_px:
            continue
        w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        if w <= max_dim and h <= max_dim:
            continue  # dot
        out[ys, xs] = True
    return out


def ransac_line(m, iters=6000, thresh=2.2, seed=7):
    ys, xs = np.nonzero(m)
    pts = np.stack([xs, ys], 1).astype(float)
    if len(pts) < 50:
        return None
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(iters):
        i, j = rng.choice(len(pts), 2, replace=False)
        p, q = pts[i], pts[j]
        if np.hypot(*(p - q)) < 40:
            continue
        d = q - p
        n = np.array([-d[1], d[0]]) / np.linalg.norm(d)
        dist = np.abs((pts - p) @ n)
        inl = dist < thresh
        if best is None or inl.sum() > best[0].sum():
            best = (inl, p, q)
    inl, p, q = best
    # refit with total least squares on inliers
    P = pts[inl]
    mean = P.mean(0)
    u, s, vt = np.linalg.svd(P - mean)
    direction = vt[0]
    normal = np.array([-direction[1], direction[0]])
    d = (P - mean) @ normal
    keep = np.abs(d) < thresh
    P = P[keep]
    mean = P.mean(0)
    u, s, vt = np.linalg.svd(P - mean)
    direction = vt[0]
    t = (P - mean) @ direction
    return {
        "point": [round(float(mean[0]), 1), round(float(mean[1]), 1)],
        "dir": [round(float(direction[0]), 4), round(float(direction[1]), 4)],
        "t_min": round(float(t.min()), 1),
        "t_max": round(float(t.max()), 1),
        "n_inliers": int(len(P)),
        "total": int(len(pts)),
    }


res = {}
for name, m in [("red", red), ("green", green), ("blue", blue)]:
    pm = panelize(m)
    lm = remove_blobs(pm)
    fit = ransac_line(lm)
    res[f"line_{name}"] = fit
    if fit:
        mean = np.array(fit["point"])
        direction = np.array(fit["dir"])
        ends = []
        for t in (fit["t_min"], fit["t_max"]):
            ends.append([round(float(x), 1) for x in (mean + direction * t)])
        res[f"line_{name}"]["ends"] = ends
    # remaining (non-line) pixels = dots + arrowheads
    lab, n = ndimage.label(pm)
    extras = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 120:
            continue
        w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        extras.append({"cx": round(float(xs.mean()), 1), "cy": round(float(ys.mean()), 1),
                       "n": int(len(xs)), "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                       "w": int(w), "h": int(h)})
    res[f"blobs_{name}"] = sorted(extras, key=lambda d: -d["n"])

# axes: red vertical/horizontal runs inside panel
pm = panelize(red)
colsum = pm.sum(axis=0)
rowsum = pm.sum(axis=1)
res["red_col_runs"] = sorted([(int(c), x) for x, c in enumerate(colsum) if c > 60], key=lambda t: -t[0])[:10]
res["red_row_runs"] = sorted([(int(c), y) for y, c in enumerate(rowsum) if c > 60], key=lambda t: -t[0])[:10]

# candidates for axes (long thin structures)
res["red_col_runs_40"] = sorted([(int(c), x) for x, c in enumerate(colsum) if c > 40], key=lambda t: -t[0])[:14]
res["red_row_runs_40"] = sorted([(int(c), y) for y, c in enumerate(rowsum) if c > 40], key=lambda t: -t[0])[:14]

with open(OUT, "w") as fh:
    json.dump(res, fh, indent=1)
print(json.dumps({k: v for k, v in res.items() if not k.startswith("blobs")}, indent=1))
for k in ("red", "green", "blue"):
    print(k, "blobs:")
    for bb in res[f"blobs_{k}"]:
        print("   ", bb)
