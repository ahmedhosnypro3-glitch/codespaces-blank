#!/usr/bin/env python3
"""att27 frame measure 5 — clean ink-cluster scans (no windows):
slope-row numbers, inset boxes, next-x numbers, band value rows, insert text."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("unique_slides/slide_034.jpg").convert("RGB")).astype(int)
out = []
def w(s=""): out.append(s)

def clusters_dark(y0, y1, x0, x1, thr=130, gap=5):
    seg = im[y0:y1, x0:x1]
    m = seg.mean(axis=2)
    ink = (m < thr).any(axis=0)
    xs = np.nonzero(ink)[0]
    if len(xs) == 0: return []
    cl, cur = [], [xs[0]]
    for x in xs[1:]:
        if x - cur[-1] <= gap: cur.append(x)
        else: cl.append(cur); cur = [x]
    cl.append(cur)
    res = []
    for c in cl:
        cxs = [x0 + x for x in c]
        colsel = [x0 + x for x in c]
        ys, _ = np.nonzero((m[:, c[0]:c[-1] + 1] < thr))
        res.append((cxs[0], cxs[-1], round(sum(cxs) / len(cxs), 1),
                    y0 + ys.min(), y0 + ys.max()))
    return res

def runs_color(yy, test, x0=60, x1=900, gap=3):
    row = im[yy]
    xs = [x for x in range(x0, x1) if test(row[x])]
    if not xs: return []
    runs, cur = [], [xs[0]]
    for x in xs[1:]:
        if x - cur[-1] <= gap: cur.append(x)
        else: runs.append((cur[0], cur[-1])); cur = [x]
    runs.append((cur[0], cur[-1]))
    return [r for r in runs if r[1] - r[0] >= 4]

w("### A. slope-row ink clusters y464..473")
for c in clusters_dark(464, 474, 82, 868, thr=120):
    w("  x%s..%s cx=%s y%s..%s" % c)
w("### A2. slope-row inset boxes (salmon DEAC95) y468 runs")
sal = runs_color(468, lambda p: 195 <= p[0] <= 240 and 150 <= p[1] <= 192 and 125 <= p[2] <= 172)
w("  salmon: %s" % sal)
yel = runs_color(468, lambda p: p[0] >= 243 and p[1] >= 243 and 170 <= p[2] <= 208)
w("  yellow: %s" % yel)
grn = runs_color(468, lambda p: 170 <= p[0] <= 215 and p[1] >= 235 and 150 <= p[2] <= 205)
w("  palegreen bg: %s" % grn[:6])
w("### B. next-x ink clusters y487..499")
for c in clusters_dark(487, 500, 82, 868, thr=120):
    w("  x%s..%s cx=%s y%s..%s" % c)
w("### C. band value-row ink clusters")
for yy in (341, 359, 383, 401, 427, 445):
    cs = clusters_dark(yy - 6, yy + 7, 82, 868, thr=120)
    w("  y%d: %s" % (yy, [(c[0], c[1], c[2]) for c in cs]))
w("### D. insert text (dark green 006400) clusters")
seg = im[330:366, 620:800]
m = seg.mean(axis=2)
mask = (m < 140) & (seg[..., 1] > seg[..., 0]) & (seg[..., 1] > seg[..., 2])
ys, xs = np.nonzero(mask)
if len(xs):
    rows = sorted(set(ys.tolist()))
    rr, cur = [], [rows[0]]
    for y in rows[1:]:
        if y - cur[-1] <= 2: cur.append(y)
        else: rr.append((cur[0], cur[-1])); cur = [y]
    rr.append((cur[0], cur[-1]))
    w("  text rows: %s" % [(330 + a, 330 + b) for a, b in rr])
    for a, b in rr:
        sel = (ys >= a) & (ys <= b)
        cxs = sorted(xs[sel].tolist())
        cl, cur2 = [], [cxs[0]]
        for x in cxs[1:]:
            if x - cur2[-1] <= 6: cur2.append(x)
            else: cl.append((cur2[0], cur2[-1])); cur2 = [x]
        cl.append((cur2[0], cur2[-1]))
        w("  row y%d..%d cols: %s" % (330 + a, 330 + b, [(620 + c0, 620 + c1) for c0, c1 in cl]))
else:
    w("  none")
w("### E. next-x verticals vertical extent")
for xx in (139, 179, 220, 666, 829):
    col = im[478:508, xx]
    r, g, b = col[..., 0], col[..., 1], col[..., 2]
    red = (r > 140) & (r - g > 100)
    w("  x%d red rows(y478+i): %s" % (xx, [478 + i for i in np.nonzero(red)[0].tolist()]))
w("### F. label ink clusters per row (x82..140)")
for yy in (341, 359, 383, 401, 427, 445, 469, 493):
    cs = clusters_dark(yy - 6, yy + 7, 82, 141, thr=130)
    w("  y%d: %s" % (yy, cs))

txt = "\n".join(out)
with open("recreated_pptx/qa/slide034/att27_frame_measure5.txt", "w") as f:
    f.write(txt + "\n")
print(txt)
