#!/usr/bin/env python3
"""Slide 026 halo + bar probe (resume worker 2026-10-21).

Quantifies (a) the original's JPEG halo vs the render's clean AA by scanning each
ink band with THREE thresholds on BOTH images, and (b) the underline-bar spans
with an identical solid-run predicate on BOTH images. Output: which selfcheck
FAILs are halo/mask noise and which are real width residuals to close with
charSpacing (building.md: charSpacing, never font size).
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ren = np.asarray(Image.open(QA + "/recreated_pptx/qa/slide026/render_3.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(QA + "/unique_slides/slide_026.jpg").convert("RGB")).astype(int)
HR, WR = ren.shape[:2]
SY, SX = HR / 540.0, WR / 960.0

def bbox(mask, y0, y1, x0, x1, sx, sy):
    sub = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    ys, xs = np.where(sub)
    if len(ys) == 0: return None
    return ((int(x0*sx)+xs.min())/sx, (int(x0*sx)+xs.max())/sx,
            (int(y0*sy)+ys.min())/sy, (int(y0*sy)+ys.max())/sy)

def masks_for(im):
    R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
    red = (R-G > 40) & (R-B > 40)
    blue = (B-R > 40) & (B-G > 40)
    d = np.abs(im-255).max(axis=2)
    return dict(red=red, blue=blue, w30=d>30, w60=d>60, w90=d>90)
mr, mo = masks_for(ren), masks_for(org)

LINES = [  # name, maskkey, window (frame px)
    ("rowA",  "blue", 138, 168, 140, 860),
    ("rowB",  "blue", 172, 202, 140, 860),
    ("rowCbl","blue", 205, 236, 140, 516),
    ("rowCred","red",  205, 236, 515, 860),
    ("rowD",  "blue", 238, 268, 140, 860),
    ("gdhdr", "red",  105, 133, 100, 860),
    ("N1",    "w30",  338, 366, 86, 860),
    ("N2",    "w30",  372, 400, 100, 860),
    ("N3",    "w30",  437, 465, 86, 860),
    ("N4",    "w30",  470, 496, 100, 860),
    ("title", "w60",  56, 86, 280, 650),
]
print("== ink right edge (x1) under 3 thresholds, ORIGINAL vs RENDER (frame px) ==")
print("%-7s | %-21s | %-21s | right-edge delta (ren-org) per threshold" % ("line","ORIGINAL x0..x1 @w30/w60/w90","RENDER x0..x1 @w30/w60/w90"))
res = {}
for name, mk, y0, y1, x0, x1 in LINES:
    row = []
    for th in ("w30", "w60", "w90"):
        mkth = mk if mk in ("red", "blue") else th
        bo = bbox(mo[mkth], y0, y1, x0, x1, 1.0, 1.0)
        br = bbox(mr[mkth], y0, y1, x0, x1, SX, SY)
        row.append((bo, br))
    os = " ".join("%.1f..%.1f" % (r[0][0], r[0][1]) for r in row)
    rs = " ".join("%.1f..%.1f" % (r[1][0], r[1][1]) for r in row)
    ds = " ".join("%+.1f" % (r[1][1]-r[0][1]) for r in row)
    res[name] = row
    print("%-7s | %-21s | %-21s | %s" % (name, os, rs, ds))

print("\n== vertical: top/bottom under w60 on BOTH (halo-reduced) ==")
for name, mk, y0, y1, x0, x1 in LINES:
    mkth = mk if mk in ("red", "blue") else "w60"
    bo = bbox(mo[mkth], y0, y1, x0, x1, 1.0, 1.0)
    br = bbox(mr[mkth], y0, y1, x0, x1, SX, SY)
    if bo and br:
        print("%-7s orig y %.1f..%.1f (h %.1f) | ren y %.1f..%.1f (h %.1f) | dtop %+.1f dbot %+.1f"
              % (name, bo[2], bo[3], bo[3]-bo[2], br[2], br[3], br[3]-br[2],
                 br[2]-bo[2], br[3]-bo[3]))

print("\n== underline bars: identical solid-run scan on BOTH images ==")
def barscan(mask, y0, y1, x0, x1, sx, sy, minlen):
    sub = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    best = None
    for i in range(sub.shape[0]):
        rowm = sub[i]
        n = len(rowm); j = 0
        while j < n:
            if rowm[j]:
                k = j
                while k < n and rowm[k]: k += 1
                if (k-j) >= minlen*sx and rowm[j:k].mean() > 0.85:
                    best = ((int(x0*sx)+j)/sx, (int(x0*sx)+k)/sx, (int(y0*sy)+i)/sy)
                j = k
            else:
                j += 1
    return best
BARS = [  # name, y window, x window, expected bar length (frame px)
    ("rowB", 188, 198, 300, 860, 367),
    ("rowD", 254, 264, 280, 500, 185),
    ("N3a",  452, 464, 150, 300, 100),
    ("N3b",  452, 464, 500, 760, 190),
]
for name, y0, y1, x0, x1, ln in BARS:
    bo = barscan(mo["blue"] if name.startswith("row") else mo["w30"], y0, y1, x0, x1, 1.0, 1.0, ln*0.5)
    br = barscan(mr["blue"] if name.startswith("row") else mr["w30"], y0, y1, x0, x1, SX, SY, ln*0.5)
    if bo and br:
        print("%-5s orig x %.1f..%.1f y %.1f | ren x %.1f..%.1f y %.1f | d %+.1f %+.1f %+.1f"
              % (name, bo[0], bo[1], bo[2], br[0], br[1], br[2], br[0]-bo[0], br[1]-bo[1], br[2]-bo[2]))
    else:
        print("%-5s orig=%s ren=%s" % (name, bo, br))
