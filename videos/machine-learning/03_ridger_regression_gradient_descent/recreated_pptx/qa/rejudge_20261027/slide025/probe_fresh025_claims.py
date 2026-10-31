#!/usr/bin/env python3
"""Probe v2: judge-claim-targeted PIL measurements on slide 025 fresh render (k14, 03:37).
Panel regions from build/slide_025.js addImage calls (slide-space px):
  TL x85-265 y115-288 | TR x616-879 y115-317 | BL x83-376 y290-527 | BR x615-880 y344-531"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
r = Image.open(f"{RJ}/slide025/render.png").convert("RGB").resize((960, 540), Image.LANCZOS)
o = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
R = np.asarray(r).astype(int); O = np.asarray(o).astype(int)

def masks(A):
    red = (A[:, :, 0] > 120) & (A[:, :, 1] < 100) & (A[:, :, 2] < 100)
    dark = A.sum(axis=2) < 330
    white = (A[:, :, 0] > 245) & (A[:, :, 1] > 245) & (A[:, :, 2] > 245)
    gray = (np.abs(A[:, :, 0] - 233) < 14) & (np.abs(A[:, :, 1] - 233) < 14) & (np.abs(A[:, :, 2] - 231) < 14)
    surf = (~white) & (~gray) & (~red) & (~dark)
    return red, dark, surf, white

rred, rdark, rsurf, rwhite = masks(R)
ored, odark, osurf, owhite = masks(O)

PANELS = {"TL": (85, 115, 265, 288), "TR": (616, 115, 879, 317),
          "BL": (83, 290, 376, 527), "BR": (615, 344, 880, 531)}
for name, (x0, y0, x1, y1) in PANELS.items():
    sl = (slice(y0, y1), slice(x0, x1))
    print(f"{name} x{x0}-{x1} y{y0}-{y1}: red r={rred[sl].sum()} o={ored[sl].sum()} | "
          f"dark r={rdark[sl].sum()} o={odark[sl].sum()} | surf r={rsurf[sl].sum()} o={osurf[sl].sum()} | "
          f"white r={rwhite[sl].sum()} o={owhite[sl].sum()}")

# Claim 2: BR bottom-edge containment — non-bg ink in rows just above bottom stroke (y536-538)
print("\n-- claim 2: BR bottom rows (x615-880) non-white non-gray ink:")
rgray = (np.abs(R[:, :, 0] - 233) < 14) & (np.abs(R[:, :, 1] - 233) < 14) & (np.abs(R[:, :, 2] - 231) < 14)
ogray = (np.abs(O[:, :, 0] - 233) < 14) & (np.abs(O[:, :, 1] - 233) < 14) & (np.abs(O[:, :, 2] - 231) < 14)
for y0, y1 in [(515, 522), (522, 528), (528, 534), (534, 538), (538, 540)]:
    sl = (slice(y0, y1), slice(615, 880))
    rb2 = (~rwhite[sl]) & (~rgray[sl])
    ob2 = (~owhite[sl]) & (~ogray[sl])
    print(f"  y{y0}-{y1}: render non-bg={rb2.sum():5d} orig non-bg={ob2.sum():5d}")

# Claim 3: BL label swap. Find dark-text bands in BL panel for both images, get x-extents, cross-compare
def bands(dark, x0, y0, x1, y1, thr=8):
    sub = dark[y0:y1, x0:x1]
    rows = sub.sum(axis=1)
    out, start = [], None
    for i, v in enumerate(rows):
        if v > thr and start is None: start = i
        elif v <= thr and start is not None:
            if i - start >= 4: out.append((y0 + start, y0 + i))
            start = None
    if start is not None: out.append((y0 + start, y0 + len(rows)))
    return out

def textline(dark, x0, y0, x1, y1):
    b = dark[y0:y1, x0:x1]
    cols = b.sum(axis=0)
    xs = np.where(cols > 0)[0]
    return (x0 + xs.min(), x0 + xs.max()) if len(xs) else None

print("\n-- claim 3: BL panel dark-text bands (x83-376):")
rb_ = bands(rdark, 83, 290, 376, 527); ob_ = bands(odark, 83, 290, 376, 527)
print("  render bands:", [(a, b, textline(rdark, 83, a, 376, b)) for a, b in rb_])
print("  orig   bands:", [(a, b, textline(odark, 83, a, 376, b)) for a, b in ob_])

def grab(dark, x0, y0, x1, y1):
    return dark[y0:y1, x0:x1]
def ncc(a, b):
    if a.shape != b.shape:
        bb = Image.fromarray((b * 255).astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.LANCZOS)
        b = np.asarray(bb) > 127
    a = a.astype(float); b = b.astype(float)
    a -= a.mean(); b -= b.mean()
    d = (np.sqrt((a * a).sum()) * np.sqrt((b * b).sum()))
    return float((a * b).sum() / d) if d else 0.0

# pair render bands with orig bands by order; cross NCC
if len(rb_) >= 2 and len(ob_) >= 2:
    print("  cross-NCC of binarized label bands (render band i vs orig band j):")
    for i, (ra, rb) in enumerate(rb_[:3]):
        row = []
        for j, (oa, ob) in enumerate(ob_[:3]):
            x0, x1 = 83, 376
            A = grab(rdark, x0, ra, x1, rb)
            B = grab(odark, x0, oa, x1, ob)
            row.append(f"r{i}x o{j}={ncc(A, B):.3f}")
        print("   ", " ".join(row))

# Claim 4: red x markers at maxima — red ink clusters in TL panel top area
print("\n-- claim 4: red ink in TL panel (x85-265 y115-288): render", int(rred[115:288, 85:265].sum()),
      "orig", int(ored[115:288, 85:265].sum()))
# red cluster x-positions in TL
for nm, red in (("render", rred), ("orig", ored)):
    sub = red[115:288, 85:265]
    cols = sub.sum(axis=0)
    xs = np.where(cols >= 3)[0]
    print(f"  {nm} TL red clusters x(px+85):", [int(x) + 85 for x in xs][:20])

# Claim 5: TR red ink profile — diagonal line?
print("\n-- claim 5: TR red ink by row (x616-879 y115-317):")
for nm, red in (("render", rred), ("orig", ored)):
    rows = red[115:317, 616:879].sum(axis=1)
    hot = [(115 + i, int(v)) for i, v in enumerate(rows) if v >= 4]
    print(f"  {nm}: {hot[:25]}")

# Claim 1: BR surface — dark path ink and NCC of surface region
def region_ncc(x0, y0, x1, y1):
    A = rsurf[y0:y1, x0:x1]; B = osurf[y0:y1, x0:x1]
    return ncc(A, B)
print("\n-- claim 1: BR panel interior surf NCC render-vs-orig:", round(region_ncc(615, 344, 880, 531), 3))
print("   BR interior dark ink r=", int(rdark[350:525, 620:875].sum()), "o=", int(odark[350:525, 620:875].sum()))
print("   TR interior surf NCC:", round(region_ncc(616, 115, 879, 317), 3))
print("   TL interior surf NCC:", round(region_ncc(85, 115, 265, 288), 3))
print("   BL interior surf NCC:", round(region_ncc(83, 290, 376, 527), 3))
