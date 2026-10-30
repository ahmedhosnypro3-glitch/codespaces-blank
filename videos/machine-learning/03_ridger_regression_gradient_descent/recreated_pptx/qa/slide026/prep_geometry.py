#!/usr/bin/env python3
"""Slide 026 consolidated probe (extends the 8-pass bank).

Verifies the banked geometry and pins the blue nominal color, using the SAME
red/ink masks on the ORIGINAL frame so JPEG halo cancels on both sides
(closed-loop checker discipline, building.md).
"""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_026.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = im.shape
print("frame", W, "x", H)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# ---------- masks ----------
# red: R notably above G/B (title + headers are red on white)
red = (R - G > 40) & (R - B > 40)
# blue-ish: B above R+G/2 significantly (blue text/border over white)
blue = (B - R > 40) & (B - G > 40)
# any ink vs white panel interior
ink = (np.abs(im - 255).max(axis=2) > 30)

print("\n== (1) TITLE red ink, full frame excl. badge zone x845..960, y45..110 ==")
sub = red.copy(); sub[:45] = False; sub[110:] = False; sub[:, :70] = False; sub[:, 849:] = False
ys, xs = np.where(sub)
print("  red ink bbox x %d..%d (w %d) y %d..%d (h %d) center=(%.1f, %.1f)"
      % (xs.min(), xs.max(), xs.max()-xs.min()+1, ys.min(), ys.max(),
         ys.max()-ys.min()+1, (xs.min()+xs.max())/2, (ys.min()+ys.max())/2))
print("  red px count", sub.sum())
# darkest cores per word run
cols = {}
for x in range(xs.min(), xs.max()+1):
    cols[x] = sub[:, x].sum()
# word runs (gap>=6)
runs, start = [], None
for x in range(xs.min(), xs.max()+2):
    if x <= xs.max() and cols.get(x, 0) > 0:
        if start is None: start = x
    else:
        if start is not None: runs.append((start, x-1)); start = None
print("  word runs:", runs)
for (a, b) in runs:
    band = sub[:, a:b+1]
    py, px = np.where(band)
    core = [im[py[i], a+px[i]] for i in range(len(py))]
    core.sort(key=lambda c: c[0]+c[1]+c[2])
    print("    x %d..%d  n=%d darkest3=%s median=%s"
          % (a, b, len(core), core[:3], tuple(np.median(np.array(core), axis=0).astype(int))))

print("\n== (2) CONTENT BOX — blue column/row profile ==")
cols_blue = blue.sum(axis=0)
rows_blue = blue.sum(axis=1)
hc = [x for x in range(W) if cols_blue[x] > 100]
hr = [y for y in range(H) if rows_blue[y] > 100]
print("  heavy cols(>100):", hc)
print("  heavy rows(>100):", hr)
# exact core values on each edge
for (label, pts) in {
    "left col 83":  [(y, 83) for y in range(200, 330)],
    "left col 82":  [(y, 82) for y in range(200, 330)],
    "right col 862":[(y, 862) for y in range(200, 330)],
    "right col 864":[(y, 864) for y in range(200, 330)],
    "top row 91":   [(91, x) for x in range(300, 500)],
    "top row 90":   [(90, x) for x in range(300, 500)],
    "bot row 499":  [(499, x) for x in range(300, 500)],
    "bot row 500":  [(500, x) for x in range(300, 500)],
}.items():
    vals = [tuple(im[y, x]) for y, x in pts]
    print("   %-14s median=%s darkest=%s" % (label, tuple(np.median(np.array(vals),axis=0).astype(int)),
          min(vals, key=lambda c: c[0]+c[1]+c[2])))
# interior fill check (should be white)
print("  interior px (400,500):", tuple(im[400, 500]), " (300,700):", tuple(im[300, 700]))
print("  panel px (y300,x20):", tuple(im[300, 20]), "| outside-panel px (y300,x930):", tuple(im[300, 930]) if 300<540 else "oob")

print("\n== (3) BLUE text core vs RED text core (calibration for nominal) ==")
# blue text core: rowA run x 302..434 y 143..162
band = blue[143:163, 302:435]
py, px = np.where(band)
vals = [tuple(im[143+py[i], 302+px[i]]) for i in range(len(py))]
vals.sort(key=lambda c: c[0]+c[1]+c[2])
print("  blue text (rowA 'Random Weights') n=%d darkest5=%s median=%s" % (len(vals), vals[:5], tuple(np.median(np.array(vals),axis=0).astype(int))))
# red header core: GD header x 109..392 y 110..129
band = red[110:130, 109:393]
py, px = np.where(band)
vals = [tuple(im[110+py[i], 109+px[i]]) for i in range(len(py))]
vals.sort(key=lambda c: c[0]+c[1]+c[2])
print("  red  hdr  (GD hdr)        n=%d darkest5=%s median=%s" % (len(vals), vals[:5], tuple(np.median(np.array(vals),axis=0).astype(int))))
# red title core
band = red[59:84, 294:640]
py, px = np.where(band)
vals = [tuple(im[59+py[i], 294+px[i]]) for i in range(len(py))]
vals.sort(key=lambda c: c[0]+c[1]+c[2])
print("  red  title (TITLE)        n=%d darkest5=%s median=%s" % (len(vals), vals[:5], tuple(np.median(np.array(vals),axis=0).astype(int))))
# border core
band = blue[100:490, 80:86]
py, px = np.where(band)
vals = [tuple(im[100+py[i], 80+px[i]]) for i in range(len(py))]
vals.sort(key=lambda c: c[0]+c[1]+c[2])
print("  blue border (left edge)   n=%d darkest5=%s median=%s" % (len(vals), vals[:5], tuple(np.median(np.array(vals),axis=0).astype(int))))

print("\n== (4) ROW C red extent (word level) y 205..238 ==")
sub = red.copy(); sub[:205] = False; sub[238:] = False; sub[:, :80] = False; sub[:, 900:] = False
sub[:208] = False; sub[232:] = False
ys, xs = np.where(sub)
print("  red ink bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
colcount = {}
for x in range(xs.min(), xs.max()+1):
    colcount[x] = sub[:, x].sum()
runs, start = [], None
for x in range(xs.min(), xs.max()+2):
    if x <= xs.max() and colcount.get(x, 0) > 0:
        if start is None: start = x
    else:
        if start is not None: runs.append((start, x-1)); start = None
print("  red word runs:", runs)
# blue side
subb = blue.copy(); subb[:205] = False; subb[238:] = False; subb[:, :80] = False; subb[:, 900:] = False
ys, xs = np.where(subb)
print("  blue ink bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))

print("\n== (5) UNDERLINE BARS: per-row fill census ==")
def barscan(name, y0, y1, x0, x1, mask):
    print("  -- %s rows %d..%d x %d..%d" % (name, y0, y1, x0, x1))
    for y in range(y0, y1+1):
        row = mask[y, x0:x1+1]
        xs = np.where(row)[0]
        if len(xs) == 0: continue
        # contiguous runs
        runs, start = [], None
        for i in range(len(xs)+1):
            if i < len(xs) and (i == 0 or xs[i] == xs[i-1]+1):
                if start is None: start = xs[i]
            else:
                if start is not None: runs.append((x0+start, x0+xs[i-1])); start = None
        big = [r for r in runs if r[1]-r[0] >= 12]
        if big:
            print("     y%d: %s fill=%.2f" % (y, big, row.mean()))
barscan("rowB (blue)", 188, 200, 300, 860, blue)
barscan("rowD (blue)", 253, 266, 270, 500, blue)
barscan("N3  (dark-ish)", 452, 466, 80, 860, ink)
barscan("N4  (dark-ish)", 470, 496, 80, 860, ink)
print("\n== (6) bullets / left margins ==")
for (nm, y0, y1) in {"N1": (338, 366), "N3": (437, 465)}.items():
    sub = ink.copy(); sub[:y0] = False; sub[y1:] = False
    xs = np.where(sub.any(axis=0))[0]
    # leftmost cluster
    x = xs.min(); run_end = x
    while run_end+1 in xs and run_end+1 - x < 30: run_end += 1
    print("  %s leftmost ink x %d..%d" % (nm, x, run_end))
    py, px = np.where(sub[:, x:run_end+1])
    print("     rows %d..%d" % (py.min(), py.max()))
