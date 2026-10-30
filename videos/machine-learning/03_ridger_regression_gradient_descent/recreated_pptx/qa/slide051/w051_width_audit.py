#!/usr/bin/env python3
"""Width + curvature audit: generated eq_051 column PNGs vs the original frame.

For each PNG: ink bbox (px + pt at 600dpi), thin-tall paren cluster x-ranges,
left/right cluster direction (extremum test).
For the original slide_051.jpg: per-region ink cluster x-ranges and the
left-paren belly profile (x-centroid per row band) to see the true paren width
and curvature.
"""
import json
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ASSETS = f"{BASE}/recreated_pptx/build/assets"
MAN = json.load(open(f"{BASE}/recreated_pptx/qa/slide051/w051_eq_assets.json"))

def ink_of(path, lum=200):
    im = Image.open(path)
    if im.mode in ("RGBA", "LA"):
        return np.array(im.convert("RGBA"))[:, :, 3] > 64
    return np.array(im.convert("L")).astype(float) < lum

def clusters_x(ink, min_h_frac=0.5):
    H = ink.shape[0]
    colcount = ink.sum(axis=0)
    tall = np.where(colcount >= min_h_frac * H)[0]
    if len(tall) == 0:
        return []
    out, s = [], tall[0]
    for i in range(1, len(tall)):
        if tall[i] != tall[i - 1] + 1:
            out.append((int(s), int(tall[i - 1]))); s = tall[i]
    out.append((int(s), int(tall[-1])))
    return out

def shape_of(ink, x0, x1):
    win = ink[:, x0:x1 + 1]
    rows = np.where(win.any(axis=1))[0]
    if len(rows) == 0:
        return "none"
    runs, s = [], rows[0]
    for i in range(1, len(rows)):
        if rows[i] != rows[i - 1] + 1:
            runs.append((s, rows[i - 1])); s = rows[i]
    runs.append((s, rows[-1]))
    r0, r1 = max(runs, key=lambda t: t[1] - t[0])
    span = r1 - r0
    mid0, mid1 = r0 + span // 3, r0 + 2 * span // 3
    bx = np.mean([np.where(win[y])[0].mean() for y in range(mid0, mid1 + 1) if win[y].any()])
    tip = list(range(r0, r0 + 4)) + list(range(max(r1 - 3, r0), r1 + 1))
    tx = np.mean([np.where(win[y])[0].mean() for y in tip if win[y].any()])
    return "(" if tx > bx + 1 else (")" if tx < bx - 1 else "STRAIGHT")

print("=" * 30, "GENERATED PNGs", "=" * 30)
for key in ["col_sample_1", "col_sample_2", "col_sample_6", "col_z_2",
            "col_aug_1", "col_aug_6", "col_initw", "col_green",
            "rowvec_1", "dzlabel_1", "step"]:
    m = MAN[key]
    ink = ink_of(m["path"])
    H, W = ink.shape
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]
    iw, ih = cols[-1] - cols[0] + 1, rows[-1] - rows[0] + 1
    cl = clusters_x(ink[:, cols[0]:cols[-1] + 1], min_h_frac=0.45)
    shapes = [(f"{a+cols[0]}..{b+cols[0]}", shape_of(ink[:, cols[0]:cols[-1] + 1], a, b)) for a, b in cl]
    print(f"{key:14s} png {W}x{H}px  ink {iw}px={iw/600*72:.1f}pt x {ih}px={ih/600*72:.1f}pt"
          f"  (sidecar w {m['w_in']*72:.1f}pt h {m['h_in']*72:.1f}pt)  clusters {shapes}")

print("=" * 30, "ORIGINAL slide_051.jpg", "=" * 30)
orig = np.array(Image.open(f"{BASE}/unique_slides/slide_051.jpg").convert("L")).astype(float)
ink = orig < 200

def region(name, y0, y1, x0, x1, min_h_frac):
    sub = ink[y0:y1, x0:x1]
    H = y1 - y0
    cl = clusters_x(sub, min_h_frac)
    print(f"-- {name} (y{y0}..{y1}, x{x0}..{x1}) tall-clusters:", 
          [(f"x{a+x0}..{b+x0}", shape_of(sub, a, b)) for a, b in cl])
    return sub

region("sample matrix", 76, 108, 84, 220, 0.55)
region("Z matrix", 78, 110, 592, 662, 0.55)
region("augmented", 179, 226, 88, 224, 0.55)
region("initw col", 57, 108, 325, 358, 0.5)
region("green row1", 145, 193, 377, 410, 0.5)

# paren belly profile: for the leftmost paren of sample col 1 (x~90) and aug col 1 (x~94)
for label, (yy0, yy1, xx0, xx1) in [("sample col1 left paren", (74, 110, 86, 96)),
                                    ("sample col1 right paren", (98, 110, 96, 106)),
                                    ("aug col1 left paren", (177, 228, 90, 100))]:
    print(f"-- {label}: x-centroid per 4-row band")
    for y in range(yy0, yy1, 4):
        band = ink[y:y + 4, xx0:xx1]
        cols = np.where(band.any(axis=0))[0]
        if len(cols):
            xs = [np.where(band[r])[0] for r in range(band.shape[0]) if band[r].any()]
            allx = np.concatenate([c + xx0 for c in xs])
            print(f"   y{y}: x {allx.min()}..{allx.max()}  centroid {allx.mean():.1f}")
        else:
            print(f"   y{y}: -")
