#!/usr/bin/env python3
"""Comprehensive per-box interior measurement of slide_004.jpg — pass 5.

For each measured box: isolate the interior (exclude the border stroke by a
small margin), then report, per text-line band (dark/red/blue ink combined),
the exact column extent (frame px). Border/fill colors are sampled at safe
interior points. This gives the build the exact geometry for every text line
and every equation ink region. 1px = 1pt.
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

red = (r > 100) & ((r - g) > 50) & ((r - b) > 30)
blue = (b > 90) & ((b - r) > 50) & ((b - g) > 30)
dark = (r + g + b) < 330
text = dark | red | blue


def runs(m1, min_len=1):
    out, d = [], np.diff(np.concatenate(([0], m1.astype(int), [0])))
    for s, e in zip(np.where(d == 1)[0], np.where(d == -1)[0] - 1):
        if e - s + 1 >= min_len:
            out.append((int(s), int(e)))
    return out


# box -> (name, x0,x1,y0,y1 outer border, interior margin px)
BOXES = [
    ("BOX1_OrigLabels_red",   80, 394,  99, 222, 5),
    ("BOX2_PredLabels_red",  426, 744,  99, 222, 5),
    ("Remember_blue",        785, 877, 102, 151, 5),
    ("Objective_blue",        78, 302, 243, 301, 5),
    ("Error_blue",            78, 486, 307, 365, 5),
    ("PredWhere_red",        494, 884, 232, 371, 5),
    ("Define_salmon_red",      78, 655, 388, 444, 5),
    ("Formula_blue",          78, 486, 462, 522, 5),
]


def fill_probe(x0, x1, y0, y1, m):
    """Sample fill color: median RGB of a safe interior patch (text excluded)."""
    sub = im[y0:y1, x0:x1].reshape(-1, 3)
    # keep pixels that are not strong text ink
    k = ~m[y0:y1, x0:x1].reshape(-1, 3) if m.ndim == 3 else ~m[y0:y1, x0:x1]
    sub = sub[k]
    if len(sub) == 0:
        return None
    return tuple(int(np.median(sub[:, c])) for c in range(3))


for name, x0, x1, y0, y1, mg in BOXES:
    print(f"\n========== {name}: outer x{x0}..{x1} y{y0}..{y1} ==========")
    xi0, xi1, yi0, yi1 = x0 + mg, x1 - mg, y0 + mg, y1 - mg
    # fill sample: big patch, text removed
    subtext = text[yi0 + 6:yi1 - 6, xi0 + 6:xi1 - 6]
    rgb = im[yi0 + 6:yi1 - 6, xi0 + 6:xi1 - 6]
    keep = ~subtext
    if keep.any():
        fc = tuple(int(np.median(rgb[:, :, c][keep])) for c in range(3))
        print(f"  fill (median, text-removed): RGB{fc}")
    # text row bands (combined), inside full interior
    ti = text[yi0:yi1, xi0:xi1]
    rowsum = ti.sum(axis=1)
    bands = runs(rowsum > 0, min_len=3)
    print(f"  interior x{xi0}..{xi1} y{yi0}..{yi1}")
    for s, e in bands:
        band = ti[s:e + 1]
        cols = np.where(band.sum(axis=0) > 0)[0]
        cmin, cmax = xi0 + cols.min(), xi0 + cols.max()
        # column-cluster split: find gaps > 8px inside the band
        colsel = band.sum(axis=0) > 0
        cruns = runs(colsel, min_len=1)
        # merge runs separated by <=6px
        merged = []
        for s2, e2 in cruns:
            if merged and s2 - merged[-1][1] - 1 <= 6:
                merged[-1] = (merged[-1][0], e2)
            else:
                merged.append((s2, e2))
        segs = [(xi0 + a, xi0 + cc) for a, cc in merged]
        # per-segment ink class
        def clsof(a, cc):
            m = band[:, a:cc + 1]
            dk, rd, bl = dark[yi0:yi1, xi0 + a:xi0 + cc + 1].sum(), red[yi0:yi1, xi0 + a:xi0 + cc + 1].sum(), blue[yi0:yi1, xi0 + a:xi0 + cc + 1].sum()
            tot = dk + rd + bl
            lab = []
            if rd / tot > 0.3: lab.append(f"R{rd*100//tot}%")
            if bl / tot > 0.3: lab.append(f"B{bl*100//tot}%")
            if dk / tot > 0.3: lab.append(f"K{dk*100//tot}%")
            return "/".join(lab) if lab else "mix"
        print(f"  band y{yi0+s}..{yi0+e} (h{e-s+1}): segs={[f'x{a}..{c} {clsof(a-x0,c-x0)}' for a,c in segs]}")

# Title precise (dark/red/blue split) — full range
print("\n========== TITLE (x280..672, y60..100) ==========")
ti = text[60:100, 280:672]
rowsum = ti.sum(axis=1)
for s, e in runs(rowsum > 0, min_len=2):
    band = ti[s:e + 1]
    cols = np.where(band.sum(axis=0) > 0)[0]
    # split into color runs across x
    rd = red[60:100, 280:672].sum(axis=0) > 0
    bl = blue[60:100, 280:672].sum(axis=0) > 0
    dk = dark[60:100, 280:672].sum(axis=0) > 0
    print(f"  band y{60+s}..{60+e} (h{e-s+1}): ink x{280+cols.min()}..{280+cols.max()}; red x{280+np.where(rd)[0].min() if rd.any() else -1}..{280+np.where(rd)[0].max() if rd.any() else -1}; blue x{280+np.where(bl)[0].min() if bl.any() else -1}..{280+np.where(bl)[0].max() if bl.any() else -1}")
