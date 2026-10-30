#!/usr/bin/env python3
"""att27 frame measure 6 — final probes: slope verticals/fills, insert rect extent,
mid-band separators, tick-label metrics, band/next-x edges."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("unique_slides/slide_034.jpg").convert("RGB")).astype(int)
out = []
def w(s=""): out.append(s)

w("### 1. slope strip verticals color")
for xx in (179, 220, 301, 666, 788):
    w(" x%d y465..472: %s" % (xx, [(y, tuple(int(v) for v in im[y, xx])) for y in range(465, 473, 2)]))
w("### 2. slope col14/col16 fills")
for xx in (710, 730, 795, 820):
    w(" x%d y464..474: %s" % (xx, [(y, tuple(int(v) for v in im[y, xx])) for y in range(464, 475, 2)]))
w(" col14 row y468 x706..750: %s" % [(x, tuple(int(v) for v in im[468, x])) for x in range(706, 751, 6)])
w(" col16 row y468 x790..830: %s" % [(x, tuple(int(v) for v in im[468, x])) for x in range(790, 831, 6)])
w("### 3. slope label col + strip extent")
w(" y468 x84..140 step4: %s" % [(x, tuple(int(v) for v in im[468, x])) for x in range(84, 141, 4)])
w(" y468 x856..868 step4: %s" % [(x, tuple(int(v) for v in im[468, x])) for x in range(856, 869, 4)])
w("### 4. slope h-rules x400 y456..481")
w(" %s" % [(y, tuple(int(v) for v in im[y, 400])) for y in range(456, 482)])
w("### 5. insert rect probes")
w(" fill (640,341): %s (700,341): %s (700,331): %s (640,360): %s" % (
    tuple(int(v) for v in im[341, 640]), tuple(int(v) for v in im[341, 700]),
    tuple(int(v) for v in im[331, 700]), tuple(int(v) for v in im[360, 640])))
seg = im[335:350, 608:800]
m = seg.mean(axis=2)
dk = (m < 150).sum(axis=0)
w(" dark cols y335..349 x608..799: %s" % {608 + i: int(dk[i]) for i in range(len(dk)) if dk[i] > 2})
col = im[320:378, 640]
mc = col.mean(axis=1)
w(" dark rows x640 y320..377: %s" % [320 + i for i in range(len(mc)) if mc[i] < 150])
col = im[320:378, 760]
mc = col.mean(axis=1)
w(" dark rows x760 y320..377: %s" % [320 + i for i in range(len(mc)) if mc[i] < 150])
w("### 6. mid-band separators (per-row light counts x84..866)")
for nm, y0, y1 in (("band1", 334, 368), ("band2", 376, 410), ("band3", 419, 453)):
    seg = im[y0:y1, 84:866]
    br = seg.mean(axis=(1, 2))
    light = [(y0 + i, round(float(br[i]), 1)) for i in range(len(br)) if br[i] > np.median(br) + 18]
    w(" %s: %s" % (nm, light))
w("### 7. band edges x400")
for nm, ys in (("band1 top", range(327, 335)), ("band1 bot", range(365, 373)),
               ("band2 top", range(371, 378)), ("band2 bot", range(408, 415)),
               ("band3 top", range(414, 420)), ("band3 bot", range(452, 459)),
               ("nextx top", range(480, 487)), ("nextx bot", range(500, 507))):
    w(" %s: %s" % (nm, [(y, tuple(int(v) for v in im[y, 400])) for y in ys]))
w("### 8. tick label '10' metrics")
seg = im[174:195, 804:830]
m = seg.mean(axis=2)
rows = {174 + i: int((m[i] < 150).sum()) for i in range(len(m)) if (m[i] < 150).sum() > 0}
w(" per-row dark counts: %s" % rows)
cols = {804 + i: int((m[:, i] < 150).sum()) for i in range(len(m[0])) if (m[:, i] < 150).sum() > 0}
w(" per-col dark counts: %s" % cols)
w("### 9. y-label '-12' zone x696..721 y266..296")
seg = im[266:296, 696:722]
m = seg.mean(axis=2)
rows = {266 + i: int((m[i] < 150).sum()) for i in range(len(m)) if (m[i] < 150).sum() > 0}
w(" per-row: %s" % rows)
ys, xs = np.nonzero(m < 150)
if len(xs):
    w(" bbox x%d..%d y%d..%d n=%d" % (696 + xs.min(), 696 + xs.max(), 266 + ys.min(), 266 + ys.max(), len(xs)))
w("### 10. y-label '8' zone x696..721 y90..114")
seg = im[90:114, 696:722]
m = seg.mean(axis=2)
ys, xs = np.nonzero(m < 150)
if len(xs):
    w(" bbox x%d..%d y%d..%d n=%d" % (696 + xs.min(), 696 + xs.max(), 90 + ys.min(), 90 + ys.max(), len(xs)))
else:
    w(" none")
w("### 11. slope strip fill left edge x80..90 y468 / next-x left x80..90 y492")
w(" %s" % [(x, tuple(int(v) for v in im[468, x])) for x in range(80, 91)])
w(" %s" % [(x, tuple(int(v) for v in im[492, x])) for x in range(80, 91)])

txt = "\n".join(out)
with open("recreated_pptx/qa/slide034/att27_frame_measure6.txt", "w") as f:
    f.write(txt + "\n")
print(txt)
