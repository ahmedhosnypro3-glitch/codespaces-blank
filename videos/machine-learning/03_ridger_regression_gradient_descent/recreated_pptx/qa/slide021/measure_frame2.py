#!/usr/bin/env python3
"""measure_frame2.py — pass-2 precise geometry of slide_021.jpg.

Per panel: blue outline bbox + edges; fill census; inside content:
labels (red/green/blue ink), table gridlines, chain text bands, arrows.
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

blue = (b > 120) & (b - r > 60) & (b - g > 60)

# --- panel segmentation by row bands found in pass 1 ---
bands = [(120, 265), (280, 425), (430, 535)]
panels = []
for i, (y0, y1) in enumerate(bands):
    m = blue[y0:y1, :]
    rows = np.where(m.any(axis=1))[0] + y0
    cols = np.where(m.any(axis=0))[0]
    # column projection: the left/right vertical outline edges are col-clusters
    colcount = m.sum(axis=0)
    # find the outermost col clusters (edges) — print them
    clusters = []
    in_c = False
    for x in range(W):
        if colcount[x] > 0 and not in_c:
            cs = x; in_c = True
        elif colcount[x] == 0 and in_c:
            clusters.append((cs, x - 1)); in_c = False
    if in_c:
        clusters.append((cs, W - 1))
    print(f"panel {i+1}: rows {rows.min()}..{rows.max()}  blue col clusters: {clusters}")
    rowcount = m.sum(axis=1)
    rclusters = []
    in_r = False
    for y in range(y0, y1):
        if rowcount[y - y0] > 0 and not in_r:
            rs = y; in_r = True
        elif rowcount[y - y0] == 0 and in_r:
            rclusters.append((rs, y - 1)); in_r = False
    if in_r:
        rclusters.append((rs, y1 - 1))
    print(f"   blue row clusters: {rclusters}")
    panels.append((rows.min(), rows.max()))

# --- fill census inside each panel (sample a 5x5 grid of interior points) ---
print("\n== panel fill census (sample points, avoiding ink):")
for i, (py0, py1) in enumerate(panels):
    # horizontal extent of the panel: use pass-1 col extent 76..888 refined per panel
    m = blue[py0:py1, :]
    cols = np.where(m.any(axis=0))[0]
    x0, x1 = cols.min(), cols.max()
    print(f" panel {i+1} x {x0}..{x1}")
    for fy in np.linspace(py0 + 8, py1 - 8, 5):
        row = []
        for fx in np.linspace(x0 + 10, x1 - 10, 8):
            px = a[int(fy), int(fx)]
            row.append(f"({px[0]},{px[1]},{px[2]})")
        print(f"   y={int(fy)}: {' '.join(row)}")

# --- red ink EXCLUDING chrome strokes: find title + red labels ---
print("\n== red ink (excluding chrome stroke cols/rows):")
red = (r > 100) & (r - g > 60) & (r - b > 60)
red_excl = red.copy()
red_excl[:, 54:63] = False   # left stroke
red_excl[:, 897:906] = False # right stroke
red_excl[533:, :] = False    # bottom stroke zone
rows = np.where(red_excl.any(axis=1))[0]
if len(rows):
    # row clusters
    clusters = []
    s = rows[0]; p = rows[0]
    for y in rows[1:]:
        if y - p > 5:
            clusters.append((s, p)); s = y
        p = y
    clusters.append((s, p))
    for (cy0, cy1) in clusters:
        m = red_excl[cy0:cy1 + 1, :]
        cols = np.where(m.any(axis=0))[0]
        # col clusters
        ccl = []
        s = cols[0]; p = cols[0]
        for x in cols[1:]:
            if x - p > 12:
                ccl.append((s, p)); s = x
            p = x
        ccl.append((s, p))
        print(f"  red band y {cy0}..{cy1}: col clusters {ccl}")

# --- green label ---
green = (g > 100) & (g - r > 50) & (g - b > 50)
if green.any():
    ys, xs = np.where(green)
    print(f"\n== green ink bbox: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")

# --- yellow content (diagonal highlights) ---
yellow = (r > 180) & (g > 180) & (b < 140)
if yellow.any():
    ys, xs = np.where(yellow)
    print(f"== yellow ink bbox: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
    # exclude the badge zone (x>850, y<95)
    ym = yellow.copy(); ym[:100, 840:] = False
    ys, xs = np.where(ym)
    if len(ys):
        print(f"   yellow (content only) bbox: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
        # row clusters
        rows = np.where(ym.any(axis=1))[0]
        ccl = []
        s = rows[0]; p = rows[0]
        for y in rows[1:]:
            if y - p > 5:
                ccl.append((s, p)); s = y
            p = y
        ccl.append((s, p))
        print(f"   yellow row clusters: {ccl}")

# --- dark ink per panel (tables, chain text, arrows) ---
dark = (r < 110) & (g < 110) & (b < 110)
for i, (py0, py1) in enumerate(panels):
    m = dark[py0:py1 + 1, :]
    rows = np.where(m.any(axis=1))[0] + py0
    if not len(rows):
        continue
    print(f"\n== dark ink in panel {i+1} (y {py0}..{py1}):")
    # row clusters with gap > 3
    ccl = []
    s = rows[0]; p = rows[0]
    for y in rows[1:]:
        if y - p > 4:
            ccl.append((s, p)); s = y
        p = y
    ccl.append((s, p))
    for (cy0, cy1) in ccl:
        mm = dark[cy0:cy1 + 1, :]
        cols = np.where(mm.any(axis=0))[0]
        xcl = []
        s2 = cols[0]; p2 = cols[0]
        for x in cols[1:]:
            if x - p2 > 15:
                xcl.append((s2, p2)); s2 = x
            p2 = x
        xcl.append((s2, p2))
        print(f"   y {cy0}..{cy1}: x clusters {xcl}")
