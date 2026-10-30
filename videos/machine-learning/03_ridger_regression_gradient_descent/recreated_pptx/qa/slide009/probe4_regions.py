#!/usr/bin/env python3
"""Probe 4: precise region boundaries, axes, annotation boxes, captions."""
import numpy as np
from PIL import Image
from collections import Counter

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(idx, gap=1):
    idx = [int(v) for v in idx]
    if not idx:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v <= p + gap:
            p = v
            continue
        out.append((s, p))
        s = p = v
    out.append((s, p))
    return out

# ---------- A. WHITE chart-panel regions inside the gray panel ----------
print("=== WHITE chart panels (near-white inside x54..903, y50..470) ===")
white = (r > 250) & (g > 250) & (b > 250)
zone = np.zeros_like(white)
zone[50:470, 54:904] = True
wz = white & zone
# per-column white fraction in rows 120..470 (body, avoiding boxes/axes)
sub = wz[120:470, :]
cf = sub.mean(axis=0)
print("  cols >0.7 white:", runs(np.where(cf > 0.7)[0]))
rf = wz[:, 54:904].mean(axis=1)
print("  rows >0.7 white:", runs(np.where(rf > 0.7)[0]))
# for each panel find the white bbox
for nm, c0, c1 in (("LEFT", 60, 460), ("RIGHT", 480, 900)):
    m = wz[110:470, c0:c1]
    ys, xs = np.where(m)
    print(f"  {nm} white-ink bbox x {xs.min()+c0}..{xs.max()+c0} y {ys.min()+110}..{ys.max()+110}")

# ---------- B. annotation box (pale blue) ----------
print("\n=== ANNOTATION BOXES (b>240 & b-r>6 & g>=r) ===")
lb = (b > 240) & ((b - r) > 6) & (g >= r - 4)
print("  total px:", int(lb.sum()))
for nm, c0, c1 in (("LEFT", 60, 460), ("RIGHT", 480, 900)):
    m = lb[:, c0:c1]
    if not m.any():
        print(f"  {nm}: none")
        continue
    ys, xs = np.where(m)
    print(f"  {nm}: bbox x {xs.min()+c0}..{xs.max()+c0} y {ys.min()}..{ys.max()} n={int(m.sum())}")
    # exact rows: rows with >30 lb px
    rh = m.sum(axis=1)
    rr = runs(np.where(rh > 30)[0])
    print(f"    rows>30px: {rr}")
    # exact cols in that row band
    if rr:
        y0, y1 = rr[0]
        band = m[y0:y1 + 1]
        ch = band.sum(axis=0)
        print(f"    cols>3 in band: {runs(np.where(ch > 3)[0]+c0)}")
        # histogram of interior colors
        yr = (y0 + y1) // 2
        row = a[yr, xs.min() + c0:xs.max() + c0 + 1]
        c = Counter(map(tuple, row))
        print(f"    row y={yr} color hist (top 8): {c.most_common(8)}")

# ---------- C. RED vertical axis strokes inside panels ----------
print("\n=== RED vertical axis strokes ===")
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
# inside each panel only, excluding house strokes
for nm, c0, c1, y0, y1 in (("LEFT", 61, 459, 100, 470), ("RIGHT", 481, 899, 100, 470)):
    sub = red[y0:y1, c0:c1]
    rc = sub.sum(axis=0)
    print(f"  {nm} red cols count>60: {[(x+c0, int(rc[x])) for x in range(c1-c0) if rc[x] > 60]}")

print("\n=== RED horizontal axis strokes ===")
for nm, c0, c1, y0, y1 in (("LEFT", 61, 459, 100, 470), ("RIGHT", 481, 899, 100, 470)):
    sub = red[y0:y1, c0:c1]
    rr2 = sub.sum(axis=1)
    print(f"  {nm} red rows count>60: {[(y+y0, int(rr2[y])) for y in range(y1-y0) if rr2[y] > 60]}")

# ---------- D. BLUE fitted line: per-column centerline ----------
print("\n=== BLUE fitted line centerline (exclude box text rows 106..190) ===")
blue = (b > 120) & ((b - r) > 40) & ((b - g) > 30)
for nm, c0, c1 in (("LEFT", 60, 456), ("RIGHT", 480, 900)):
    print(f"  {nm}:")
    pts = []
    for x in range(c0, c1 + 1, 10):
        col = blue[195:470, x]      # exclude annotation box band
        ys = np.where(col)[0]
        if len(ys):
            # cluster: take the largest contiguous group
            grp, s, p = [], ys[0], ys[0]
            for v in ys[1:]:
                if v <= p + 2:
                    p = v
                    continue
                grp.append((s, p))
                s = p = v
            grp.append((s, p))
            grp.sort(key=lambda t: t[1] - t[0], reverse=True)
            s0, s1 = grp[0]
            mid = (s0 + s1) / 2 + 195
            pts.append((x, mid, s0 + 195, s1 + 195, len(ys)))
            print(f"    x={x:4d} y {s0+195}..{s1+195}  mid={mid:6.1f}  n={len(ys)}")
    if len(pts) >= 2:
        xs = np.array([p[0] for p in pts], float)
        ys = np.array([p[1] for p in pts], float)
        A = np.vstack([xs, np.ones_like(xs)]).T
        m, c = np.linalg.lstsq(A, ys, rcond=None)[0]
        print(f"    LSQ fit: y = {m:.5f}*x + {c:.2f}   (n={len(pts)})")
        pred = m * xs + c
        print(f"    max|resid| = {np.abs(ys-pred).max():.2f} px; rms = "
              f"{np.sqrt(((ys-pred)**2).mean()):.2f}")

# ---------- E. caption text: rows and per-line extents ----------
print("\n=== CAPTION red text ===")
redcap = red & (np.arange(H)[:, None] > 480)
for nm, c0, c1 in (("LEFT", 60, 460), ("RIGHT", 480, 900)):
    m = redcap[:, c0:c1]
    ys, xs = np.where(m)
    if not len(ys):
        continue
    print(f"  {nm}: bbox x {xs.min()+c0}..{xs.max()+c0} y {ys.min()}..{ys.max()} n={int(m.sum())}")
    # row histogram -> line bands
    rh = m.sum(axis=1)
    bands = runs(np.where(rh > 0)[0])
    print(f"    row bands: {bands}")
    for (b0, b1) in bands:
        sel = m[b0:b1 + 1]
        ch = sel.sum(axis=0)
        cc = runs(np.where(ch > 0)[0] + c0, gap=3)
        print(f"      line y {b0}..{b1} (h={b1-b0+1}): col runs {cc}")

# ---------- F. caption font size estimate ----------
print("\n=== CAPTION glyph height / stem widths ===")
# measure stem width of a tall glyph in caption line 2 (y 508..519)
for nm, c0, c1 in (("LEFT", 150, 460), ("RIGHT", 560, 900)):
    m = redcap[505:522, c0:c1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {nm} line2 ink x {xs.min()+c0}..{xs.max()+c0} y {ys.min()+505}..{ys.max()+505}")
        # sample a column's vertical run length
        for x in range(xs.min() + c0 + 3, xs.max() + c0, 7):
            col = np.where(redcap[500:525, x])[0]
            if len(col):
                print(f"      x={x}: y {col.min()+500}..{col.max()+500} (h={col.max()-col.min()+1})")

# ---------- G. grid lines inside chart panels ----------
print("\n=== GRID lines (very light gray, inside white panel) ===")
# grid = slightly darker than white
grid = (r > 225) & (r < 250) & (abs(r - g) < 10) & (abs(g - b) < 10) & (r < 249)
for nm, c0, c1 in (("LEFT", 62, 458), ("RIGHT", 482, 898)):
    m = grid[110:470, c0:c1]
    print(f"  {nm} grid-ish px {int(m.sum())}")
    rr3 = m.sum(axis=1)
    bands = runs(np.where(rr3 > 20)[0])
    print(f"    rows>20: {bands}")
    rc4 = m.sum(axis=0)
    print(f"    cols>20: {runs(np.where(rc4 > 20)[0]+c0)}")

# ---------- H. residual arrows: red thin marks between line and points ----------
print("\n=== RED thin marks (residual arrows) — red excluding stroked axes/box ===")
# vertical red segments that are short (height < 40) inside panel body
from scipy import ndimage
lab_r, n = ndimage.label(red, structure=np.ones((3, 3)))
print(f"  red components: {n}")
sizes = ndimage.sum(red, lab_r, range(1, n + 1))
objs = ndimage.find_objects(lab_r)
for nm, c0, c1 in (("LEFT", 61, 459), ("RIGHT", 481, 899)):
    print(f"  {nm} components (n>=10):")
    for i, (sl, sz) in enumerate(zip(objs, sizes), 1):
        if sz >= 10 and sl[1].start >= c0 - 2 and sl[1].stop <= c1 + 2:
            h = sl[0].stop - sl[0].start
            w = sl[1].stop - sl[1].start
            print(f"    comp{i}: x {sl[1].start}..{sl[1].stop-1} (w={w}) "
                  f"y {sl[0].start}..{sl[0].stop-1} (h={h}) n={int(sz)}")
