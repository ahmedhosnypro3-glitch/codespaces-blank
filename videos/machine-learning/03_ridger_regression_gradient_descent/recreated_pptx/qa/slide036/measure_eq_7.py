#!/usr/bin/env python3
"""Measure the ORIGINAL slide 036 equation row (ink-run census) so the equation
asset can be re-rendered against measured glyph positions/colors.

Prints, for the original frame: column runs of ink in the equation band, the
per-run ink bbox, and the dominant colors of a few key pieces.
Also prints the same census for render_7 for comparison.
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
IMG = {
    "orig": f"{V}/unique_slides/slide_036.jpg",
    "rend": f"{V}/recreated_pptx/qa/slide036/render_7.png",
}
BANDS = {"main": (366, 398), "sub": (396, 418)}
X0, X1 = 80, 760


def load(p):
    return np.array(Image.open(p).convert("RGB")).astype(int)


def runs(a, y0, y1, x0, x1, thr=170, min_gap=2):
    sub = a[y0:y1, x0:x1]
    lum = sub.mean(axis=2)
    cols = (lum < thr).any(axis=0)
    out = []
    i = 0
    while i < len(cols):
        if cols[i]:
            j = i
            while j + 1 < len(cols) and cols[j + 1]:
                j += 1
            out.append((x0 + i, x0 + j))
            i = j + 1
        else:
            i += 1
    # merge runs separated by < min_gap px
    merged = []
    for r in out:
        if merged and r[0] - merged[-1][1] <= min_gap:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(list(r))
    return merged


for tag, path in IMG.items():
    a = load(path)
    H = a.shape[0]
    s = H / 540.0
    print(f"\n===== {tag} {path.split('/')[-1]} ({a.shape[1]}x{H}, scale {s:.4f}) =====")
    for bname, (fy0, fy1) in BANDS.items():
        y0, y1 = int(fy0 * s), int(fy1 * s)
        rr = runs(a, y0, y1, int(X0 * s), int(X1 * s))
        rr = [(round(x0 / s, 1), round(x1 / s, 1)) for x0, x1 in rr]
        print(f"  {bname} band y{fy0}..{fy1}: {len(rr)} runs")
        print("   ", " ".join(f"{a0:.0f}-{a1:.0f}" for a0, a1 in rr))

# color probes on the original
o = load(IMG["orig"])
def core(x0, y0, x1, y1, k=60):
    a = o[y0:y1, x0:x1]
    lum = a.mean(axis=2).flatten()
    idx = np.argsort(lum)[:k]
    return a.reshape(-1, 3)[idx].mean(axis=0).round().astype(int).tolist()

print("\n===== original color probes =====")
probes = {
    "limit 'all'":        (160, 402, 183, 414),
    "limit 'misclassified'": (185, 402, 262, 414),
    "limit 'vectors'":    (263, 402, 315, 414),
    "limit '(i)'":        (316, 402, 340, 414),
    "X1 green":           (333, 375, 358, 395),
    "sub i of X1":        (358, 390, 372, 405),
    "W1":                 (283, 375, 305, 395),
    "sup T1":             (305, 366, 320, 380),
    "phrase first word":  (507, 378, 545, 395),
    "Sigma":              (218, 365, 240, 398),
    "Error =":            (84, 372, 150, 395),
}
for name, (x0, y0, x1, y1) in probes.items():
    print(f"  {name:24s} x{x0}..{x1} y{y0}..{y1} core={core(x0, y0, x1, y1)}")
