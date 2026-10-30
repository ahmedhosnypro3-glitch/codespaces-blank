#!/usr/bin/env python3
"""Probe 5: exact colors — y-vector chips (#48), 'N x d+1'/'d+1 x 1' labels, y-vector ellipsis tint.
Direct slide-space measurement on unique_slides/slide_003.jpg (1px=1px) and render_33 (x2.084375/x2.083333)."""
import numpy as np
from PIL import Image

Q = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"
D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
r = np.asarray(Image.open(Q + "/render_33.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(D + "/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
SRX, SRY = 2001 / 960.0, 1125 / 540.0

def rimg(x0, y0, x1, y1):
    return r[int(y0 * SRY):int(y1 * SRY), int(x0 * SRX):int(x1 * SRX)]

def oimg(x0, y0, x1, y1):
    return o[y0:y1, x0:x1]

def fill_stats(img, tag, exclude_dark=False):
    rr, gg, bb = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    mx = img.max(axis=2); mn = img.min(axis=2)
    sat = (mx - mn) > 25
    if exclude_dark:
        sat &= mx > 150
    n = int(sat.sum())
    if not n:
        print(f"  {tag}: no sat px")
        return
    px = img[sat]
    print(f"  {tag}: sat n={n} mean=({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f})")

print("=== y-vector chip fills (ORIG slide-space rects) ===")
fill_stats(oimg(114, 372, 134, 388), "chip1 yellow interior x114..134 y372..388")
fill_stats(oimg(114, 404, 134, 418), "chip2 cyan  interior x114..134 y404..418")
fill_stats(oimg(114, 460, 134, 474), "chip3 pink  interior x114..134 y460..474")
print("=== build band fills for reference (REND) ===")
fill_stats(rimg(200, 370, 390, 388), "band yellow REND")
fill_stats(rimg(200, 400, 390, 420), "band cyan REND")
fill_stats(rimg(200, 458, 390, 476), "band pink REND")
print("=== chip exact extents in ORIG (scan row/col runs) ===")
for tag, ymid, xlo, xhi in [("chip1", 380, 100, 145), ("chip2", 410, 100, 145), ("chip3", 467, 100, 145)]:
    row = o[ymid, xlo:xhi]
    sat = (row.max(axis=1) - row.min(axis=1)) > 25
    xs = np.where(sat)[0]
    print(f"  {tag} y{ymid}: sat x-extent {xlo + xs.min()}..{xlo + xs.max()}" if len(xs) else f"  {tag} y{ymid}: none")
for tag, xmid in [("chip1", 124), ("chip2", 124), ("chip3", 124)]:
    col = o[350:500, xmid]
    sat = (col.max(axis=1) - col.min(axis=1)) > 25
    ys = np.where(sat)[0] + 350
    if len(ys):
        # find runs
        runs, start = [], ys[0]
        for a, b in zip(ys, ys[1:]):
            if b - a > 3:
                runs.append((start, a)); start = b
        runs.append((start, ys[-1]))
        print(f"  {tag} x{xmid}: sat y-runs {runs}")
    else:
        print(f"  {tag} x{xmid}: none")

print("=== 'N x d+1' label (ORIG x395..465 y466..490 / REND same) ===")
def ink_colors(img, tag, x0, y0, x1, y1, isrender):
    im = rimg(x0, y0, x1, y1) if isrender else oimg(x0, y0, x1, y1)
    mx = im.max(axis=2)
    ink = mx < 200
    n = int(ink.sum())
    print(f"  {tag}: ink(n<200)={n}", end="")
    if n:
        px = im[ink]
        print(f" mean=({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f}) min-lum px={px[px.sum(axis=1).argmin()]}")
    else:
        print()

ink_colors(None, "ORIG Nxd+1", 395, 466, 465, 490, False)
ink_colors(None, "REND Nxd+1", 395, 466, 465, 490, True)
print("=== 'd+1 x 1' label (ORIG x446..532 y482..508, EXCLUDING box border x530..534) ===")
ink_colors(None, "ORIG d+1x1 (x446..528)", 446, 482, 528, 508, False)
ink_colors(None, "REND d+1x1 (x446..528)", 446, 482, 528, 508, True)
ink_colors(None, "ORIG d+1x1 narrow (x450..500)", 450, 482, 500, 508, False)
ink_colors(None, "REND d+1x1 narrow (x450..500)", 450, 482, 500, 508, True)

print("=== y-vector ellipsis zone x106..140 y438..452 (ORIG ink px, exclude brackets x106..109/x133..137) ===")
im = o[438:452, 110:132]
mx = im.max(axis=2)
ink = mx < 190
print(f"  ORIG: ink n={int(ink.sum())}")
if ink.sum():
    px = im[ink]
    print(f"    mean=({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f})")
    red = (px[:, 0] > px[:, 1] + 40) & (px[:, 0] > px[:, 2] + 40)
    print(f"    red-family px: {int(red.sum())}")
im2 = rimg(110, 438, 132, 452)
mx2 = im2.max(axis=2)
ink2 = mx2 < 190
print(f"  REND: ink n={int(ink2.sum())}")
if ink2.sum():
    px2 = im2[ink2]
    print(f"    mean=({px2[:,0].mean():.0f},{px2[:,1].mean():.0f},{px2[:,2].mean():.0f})")
    red2 = (px2[:, 0] > px2[:, 1] + 40) & (px2[:, 0] > px2[:, 2] + 40)
    print(f"    red-family px: {int(red2.sum())}")

print("=== 1px map ORIG y438..452 x108..140 (ellipsis zoom) ===")
def cmap(px):
    r, g, b = px
    if max(r, g, b) > 235 and min(r, g, b) > 225: return "."
    if max(r, g, b) < 110: return "#"
    if r > g + 40 and r > b + 40: return "R"
    return "+"
for yy in range(438, 452):
    print("%4d %s" % (yy, "".join(cmap(o[yy, xx]) for xx in range(108, 140))))
