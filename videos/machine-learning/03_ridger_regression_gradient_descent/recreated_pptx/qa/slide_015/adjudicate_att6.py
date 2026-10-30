#!/usr/bin/env python3
"""PIL-first adjudication of the att6 legA findings (judge_attempt_6.txt),
measured on the CURRENT bytes: render_6.png (md5 81ed97f213977703e6c6aeb1e5b453f1)
vs unique_slides/slide_015.jpg.  Frame coords: 960x540, 1px = 1pt.
Render scale sx=2001/960, sy=1125/540.

Findings under test (from judge_attempt_6.txt):
  1 BLOCKER blue J(W) collides with "= 0", x2 lower panel
  2 MAJOR   spurious floating green lambda duplicates
  3 MAJOR   missing "=>" arrow before the green box
  4 MAJOR   trailing lambda-terms black w/ green underline (not green text)
  5 MAJOR   spurious blue J(W) labels in the top panel
  6 MINOR   irregular line spacing (consequence of 1/2/5)
  7 MINOR   (Y-XW) vs (X-XW) in eq line 1
"""
import json
import os

import numpy as np
from PIL import Image

VID = "videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = os.path.join(VID, "recreated_pptx/qa/slide_015/render_6.png")
ORIG = os.path.join(VID, "unique_slides/slide_015.jpg")

out = []


def say(line=""):
    print(line)
    out.append(line)


def luma(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


def masks(rgb):
    L = luma(rgb.astype(float))
    r, g, b = rgb[:, :, 0].astype(int), rgb[:, :, 1].astype(int), rgb[:, :, 2].astype(int)
    dark = L < 150
    green = (g > r + 50) & (g > b + 50) & (g > 60)
    blue = (b > r + 40) & (b > g + 40) & (b > 60)
    red = (r > g + 60) & (r > b + 60) & (r > 90)
    return dark, green, blue, red


def row_bands(mask, x0, x1, y0, y1, min_count, tol):
    rows = np.where(mask[y0:y1, x0:x1].sum(axis=1) >= min_count)[0] + y0
    bands = []
    for y in rows:
        if bands and y - bands[-1][1] <= tol:
            bands[-1][1] = y
        else:
            bands.append([y, y])
    return bands


def x_clusters(mask, x0, x1, y0, y1, min_count, gap):
    cols = np.where(mask[y0:y1, x0:x1].sum(axis=0) >= min_count)[0] + x0
    cl = []
    for x in cols:
        if cl and x - cl[-1][1] <= gap:
            cl[-1][1] = x
        else:
            cl.append([x, x])
    return cl


def bbox(mask, x0, x1, y0, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return (int(xs.min()) + x0, int(xs.max()) + x0, int(ys.min()) + y0, int(ys.max()) + y0)


def fpx(v, s):
    return int(round(v * s))


rend = np.asarray(Image.open(RENDER).convert("RGB"))
orig = np.asarray(Image.open(ORIG).convert("RGB"))
SRX, SRY = rend.shape[1] / 960.0, rend.shape[0] / 540.0
say(f"render {rend.shape[1]}x{rend.shape[0]}  scale sx={SRX:.6f} sy={SRY:.6f}")
say(f"orig   {orig.shape[1]}x{orig.shape[0]}")
dR, gR, bR, rR = masks(rend)
dO, gO, bO, rO = masks(orig)

# ---------- finding 2/4: green inline census, cream rect A (x72..892 y104..266)
say("\n== CREAM RECT A (x72..892, y104..266) — dark bands + green census ==")
for name, dark, green, s in (("render", dR, gR, (SRX, SRY)),
                             ("orig  ", dO, gO, (1.0, 1.0))):
    x0, x1 = fpx(74, s[0]), fpx(890, s[0])
    y0, y1 = fpx(104, s[1]), fpx(266, s[1])
    tol = max(2, int(round(3 * s[1])))
    bands = row_bands(dark, x0, x1, y0, y1, min_count=3, tol=tol)
    fs = lambda v: round(v / s[1], 1)
    say(f"{name} dark bands(frame y): {[(fs(a), fs(b)) for a, b in bands]}")
    for a, b in bands:
        gap = max(4, int(round(8 * s[0])))
        cl = x_clusters(green, x0, x1, a, b + 1, min_count=2, gap=gap)
        desc = [(round(c[0] / s[0], 1), round(c[1] / s[0], 1),
                 int(green[a:b + 1, c[0]:c[1] + 1].sum())) for c in cl]
        say(f"   band y{fs(a)}..{fs(b)} green x-clusters(frame x, px): {desc}")
    # green rows OUTSIDE the dark bands (a 'floating duplicate' would land here)
    g_rows = set(np.where(green[y0:y1, x0:x1].sum(axis=1) >= 2)[0])
    in_band = set()
    for a, b in bands:
        in_band.update(range(a - tol, b + tol + 1))
    stray = sorted(g_rows - in_band)
    say(f"   green rows outside dark bands(+/-{tol}): {len(stray)} -> "
        f"{[fs(y) for y in stray[:12]]}")

# lambda colour sample (line 2 band)
for name, img, green, s in (("render", rend, gR, (SRX, SRY)),
                            ("orig  ", orig, gO, (1.0, 1.0))):
    ya, yb = fpx(170, s[1]), fpx(211, s[1])
    xa, xb = fpx(74, s[0]), fpx(890, s[0])
    sel = img[ya:yb, xa:xb][green[ya:yb, xa:xb]]
    if len(sel):
        say(f"{name} line-2 green mean RGB = "
            f"({sel[:, 0].mean():.0f},{sel[:, 1].mean():.0f},{sel[:, 2].mean():.0f}) "
            f"n={len(sel)}")

# ---------- finding 5/1: blue J(W) clusters, rect A + rect B
say("\n== BLUE J(W) clusters per equation line ==")
for name, blue, s in (("render", bR, (SRX, SRY)), ("orig  ", bO, (1.0, 1.0))):
    for label, (X0, X1, YA, YB) in (
            ("eq1_l1", (74, 890, 106, 154)), ("eq1_l2", (74, 890, 165, 213)),
            ("eq1_l3", (74, 890, 218, 266)), ("deriv_l1", (74, 890, 348, 404)),
            ("deriv_l2", (74, 890, 413, 468))):
        x0, x1 = fpx(X0, s[0]), fpx(X1, s[0])
        y0, y1 = fpx(YA, s[1]), fpx(YB, s[1])
        cl = x_clusters(blue, x0, x1, y0, y1, min_count=2,
                        gap=max(4, int(round(8 * s[0]))))
        desc = [(round(c[0] / s[0], 1), round(c[1] / s[0], 1),
                 int(blue[y0:y1, c[0]:c[1] + 1].sum())) for c in cl]
        say(f"{name} {label}: {len(cl)} blue cluster(s) {desc}")

# finding 1: J(W)-vs-"= 0" collision geometry on the deriv lines
say("\n== deriv lines: blue (J(W) head) bbox vs black baseline ink ==")
for name, blue, dark, s in (("render", bR, dR, (SRX, SRY)),
                            ("orig  ", bO, dO, (1.0, 1.0))):
    for label, (YA, YB) in (("deriv_l1", (348, 404)), ("deriv_l2", (413, 468))):
        x0, x1 = fpx(74, s[0]), fpx(660, s[0])
        y0, y1 = fpx(YA, s[1]), fpx(YB, s[1])
        bb = bbox(blue, x0, x1, y0, y1)
        if bb is None:
            say(f"{name} {label}: NO blue ink")
            continue
        bx0, bx1, by0, by1 = bb
        # black ink to the RIGHT of the blue cluster within its y-span
        rx0, rx1 = fpx(bx1 + 3, s[0]), min(x1, fpx(bx1 + 60, s[0]))
        right_dark = int(dark[by0:by1 + 1, rx0:rx1].sum())
        # black ink INSIDE the blue bbox (an overlap would put dark glyphs there)
        inside_dark = int(dark[by0:by1 + 1, bx0:bx1 + 1].sum()
                          - (dark[by0:by1 + 1, bx0:bx1 + 1] & blue[by0:by1 + 1, bx0:bx1 + 1]).sum())
        say(f"{name} {label}: blue bbox frame x{bx0/s[0]:.0f}..{bx1/s[0]:.0f} "
            f"y{by0/s[1]:.0f}..{by1/s[1]:.0f}; dark px right of it: {right_dark}; "
            f"non-blue dark px inside bbox: {inside_dark}")

# ---------- finding 3: arrow gap x503..545 y466..521
say("\n== ARROW GAP x503..545, y466..521 (dark ink census) ==")
for name, dark, s in (("render", dR, (SRX, SRY)), ("orig  ", dO, (1.0, 1.0))):
    x0, x1 = fpx(503, s[0]), fpx(546, s[0])
    y0, y1 = fpx(466, s[1]), fpx(522, s[1])
    say(f"{name}: {int(dark[y0:y1, x0:x1].sum())} dark px")

# ---------- green-box interior (stray lambda-I claim) + normal-line tail
say("\n== GREEN BOX x547..885 y472..516 — dark-green ink (lambda I of solution) ==")
for name, green, s in (("render", gR, (SRX, SRY)), ("orig  ", gO, (1.0, 1.0))):
    x0, x1 = fpx(550, s[0]), fpx(883, s[0])
    y0, y1 = fpx(475, s[1]), fpx(514, s[1])
    n = int(green[y0:y1, x0:x1].sum())
    bb = bbox(green, x0, x1, y0, y1)
    say(f"{name}: {n} green px, bbox frame "
        f"x{bb[0]/s[0]:.0f}..{bb[1]/s[0]:.0f} y{bb[2]/s[1]:.0f}..{bb[3]/s[1]:.0f}" if bb
        else f"{name}: 0")

# ---------- banked fix check: red W in the pink box sentence
say("\n== PINK BOX x73..709 y275..334 — red ink (the fixed Best W) ==")
for name, red, s in (("render", rR, (SRX, SRY)), ("orig  ", rO, (1.0, 1.0))):
    x0, x1 = fpx(75, s[0]), fpx(707, s[0])
    y0, y1 = fpx(277, s[1]), fpx(332, s[1])
    bb = bbox(red, x0, x1, y0, y1)
    n = int(red[y0:y1, x0:x1].sum())
    say(f"{name}: {n} red px" + (f", bbox frame x{bb[0]/s[0]:.0f}..{bb[1]/s[0]:.0f} "
        f"y{bb[2]/s[1]:.0f}..{bb[3]/s[1]:.0f}" if bb else ""))

# ---------- finding 6: line-band spacing (rect A, dark bands, gap list)
say("\n== RECT A line-band gaps (frame px between band ends) ==")
for name, dark, s in (("render", dR, (SRX, SRY)), ("orig  ", dO, (1.0, 1.0))):
    x0, x1 = fpx(74, s[0]), fpx(890, s[0])
    y0, y1 = fpx(104, s[1]), fpx(266, s[1])
    bands = row_bands(dark, x0, x1, y0, y1, min_count=3, tol=max(2, int(round(3 * s[1]))))
    gaps = [round((bands[i + 1][0] - bands[i][1]) / s[1], 1) for i in range(len(bands) - 1)]
    say(f"{name}: bands={len(bands)} gaps={gaps}")

with open(os.path.join(VID, "recreated_pptx/qa/slide_015/adjudicate_att6.out.txt"), "w") as f:
    f.write("\n".join(out) + "\n")
print("\nWROTE adjudicate_att6.out.txt")
