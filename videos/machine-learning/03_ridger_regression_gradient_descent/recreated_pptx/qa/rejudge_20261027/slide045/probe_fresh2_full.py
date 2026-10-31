#!/usr/bin/env python3
"""Targeted PIL probes for slide045 FULL fresh2 FAIL claims 1-4 (read-only)."""
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
D = f"{RJ}/slide045"

r = np.asarray(Image.open(f"{D}/render.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
sc = r.shape[1] / 960.0  # 2.084

def R(x): return int(round(x * sc))

def band_ink(img, x0, y0, x1, y1, th=600):
    """count dark-ink px in slide-space box"""
    a = img[R(y0):R(y1), R(x0):R(x1)]
    return int((a.sum(axis=2) < th).sum())

print("== claim 1: sidebar heading strip (slide-space bbox) ==")
# build comment: title at y147..159 x81..236
for name, img in (("orig", o), ("render", r)):
    n = band_ink(img, 78, 144, 240, 163)
    print(f"  {name}: heading strip ink px = {n}")
# cross-slide: same heading on sibling frames 042/047/048/049/051
for s in ("042", "047", "048", "049", "051"):
    im = np.asarray(Image.open(f"{NS}/unique_slides/slide_{s}.jpg").convert("RGB")).astype(int)
    print(f"  slide_{s}.jpg heading strip ink px = {band_ink(im, 78, 144, 240, 163)}")
# IoU of binarized heading strips orig045 vs siblings
def strip(img):
    a = img[144:163, 78:240]
    return (a.sum(axis=2) < 600)
s45 = strip(o)
for s in ("047", "048", "049", "051"):
    im = np.asarray(Image.open(f"{NS}/unique_slides/slide_{s}.jpg").convert("RGB")).astype(int)
    b = strip(im)
    inter = (s45 & b).sum(); union = (s45 | b).sum()
    print(f"  IoU 045 vs {s}: {inter/union:.3f}")

print("== claim 2: top blue-frame fill color ==")
# sample interior points of the top worked-example panel, away from ink: use median of a patch
for name, img in (("orig", o), ("render", r)):
    # slide-space patch inside top frame, e.g. x400-500 y60-80 (between elements) and x600-700 y150-170
    for (x0, y0, x1, y1) in ((400, 60, 500, 80), (620, 150, 720, 170), (300, 95, 380, 105)):
        if name == "orig":
            a = img[y0:y1, x0:x1]
        else:
            a = img[R(y0):R(y1), R(x0):R(x1)]
        med = np.median(a.reshape(-1, 3), axis=0).astype(int)
        print(f"  {name} patch x{x0}-{x1} y{y0}-{y1}: median RGB {tuple(med)} n={a.shape[0]*a.shape[1]}")

print("== claim 3: six d(x_i) row cards vs continuous field ==")
# main six-row panel approx x35%-99% y41%-97% => slide x336-950 y221-524.
# Look for vertical border segments at row boundaries: scan a column inside panel, count dark rows
colx = 500
for name, img in (("orig", o), ("render", r)):
    x = R(colx) if name == "render" else colx
    y0, y1 = (R(221), R(524)) if name == "render" else (221, 524)
    col = img[y0:y1, x-1:x+2].sum(axis=2)
    dark_rows = (col < 400).sum(axis=1)
    runs = []
    inrun = False
    for i, v in enumerate(dark_rows):
        if v > 0 and not inrun:
            start = i; inrun = True
        elif v == 0 and inrun:
            runs.append((y0 and (start + (y0 if name=='render' else 0)) or start, i))
            inrun = False
    # convert run positions back to slide space
    sl = [(round(a/sc if name=='render' else a), round(b/sc if name=='render' else b)) for a, b in runs if b-a >= 1]
    print(f"  {name}: dark-row runs at x={colx} (slide y): {sl[:20]}")

print("== claim 4: delimiter glyphs in column vectors ==")
# Initial W vector near top frame right side; green vector + W in main area.
# Just report build-side: grep handled outside; here measure bracket vs paren bow via column profile in orig
# orig 'Initial W = (4;-2;-2)' around x640-780 y55-105 per slide048-style layout; find dark column profile
def colprof(img, x0, y0, x1, y1, slide=True):
    if slide:
        a = img[y0:y1, x0:x1]
    else:
        a = img[R(y0):R(y1), R(x0):R(x1)]
    return (a.sum(axis=2) < 450).sum(axis=0)
print("  orig vector zone x640-790 y55-110 col ink profile (slide px):")
print("   ", list(colprof(o, 640, 55, 790, 110)))
print("  render same zone:")
print("   ", list(colprof(r, 640, 55, 790, 110, slide=False)))
