#!/usr/bin/env python3
"""Slide 045 mandatory pre-judge self-check (PIL).

Asserts the render against the measured original frame (960x540, 1px=1pt).
Render is 150 dpi -> 1 frame px = 150/72 = 2.0833 render px.
Exit 0 = all pass; non-zero = at least one FAIL.
"""
import sys
import numpy as np
from PIL import Image

FRAME = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_045.jpg"
RENDER = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045/render_1.png"

S = 150 / 72.0  # render px per frame px

fa = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
ra = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
RH, RW, _ = ra.shape
print("frame %dx%d   render %dx%d   scale=%.4f" % (fa.shape[1], fa.shape[0], RW, RH, S))

results = []


def check(name, ok, detail):
    results.append((name, ok, detail))
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", name, detail))


def rpx(x, y):
    """frame px -> render px (rounded)."""
    return int(round(x * S)), int(round(y * S))


def region_mode(arr, x0, y0, x1, y1):
    """Most common colour in a render region given frame coords."""
    rx0, ry0 = rpx(x0, y0)
    rx1, ry1 = rpx(x1, y1)
    sub = arr[ry0:ry1 + 1, rx0:rx1 + 1].reshape(-1, 3)
    if len(sub) == 0:
        return None
    vals, counts = np.unique(sub, axis=0, return_counts=True)
    return tuple(int(v) for v in vals[counts.argmax()])


def has_color(arr, x0, y0, x1, y1, target, tol=42):
    rx0, ry0 = rpx(x0, y0)
    rx1, ry1 = rpx(x1, y1)
    sub = arr[ry0:ry1 + 1, rx0:rx1 + 1].astype(int)
    d = np.abs(sub - np.array(target)).max(axis=2)
    return int((d <= tol).sum())


def near(c, target, tol):
    return c is not None and max(abs(int(c[i]) - int(target[i])) for i in range(3)) <= tol


# ---------------- 1. canvas + house chrome ----------------
c = region_mode(ra, 700, 12, 760, 20)          # above the panel, inside canvas
check("canvas white (FFFFFF)", near(c, (255, 255, 255), 12), "mode=%s" % (c,))

# NB: sample panel gray in the free column between the augmented table (ends x246)
# and the calc panel (starts x274) — most of the panel body is covered by content.
c = region_mode(ra, 252, 300, 268, 320)
check("panel gray E9E9E7", near(c, (233, 233, 231), 10), "mode=%s" % (c,))

# No top stroke: the band above the panel must contain no red
n = has_color(ra, 60, 48, 900, 52, (192, 0, 0), 60)
check("NO top red stroke (y48..52)", n == 0, "red px=%d" % n)

for label, x, y in [("left stroke x58.5", 58, 300), ("right stroke x901", 900, 300)]:
    n = has_color(ra, x - 2, 200, x + 2, 480, (192, 0, 0), 60)
    check("red %s" % label, n > 5, "red px=%d" % n)

n = has_color(ra, 100, 536, 860, 540, (192, 0, 0), 60)
check("red bottom stroke y538.5", n > 20, "red px=%d" % n)

# badge: yellow circle with purple ring around (876,73)
cb = region_mode(ra, 868, 66, 884, 80)
check("badge fill FDFD96", near(cb, (253, 253, 150), 30), "mode=%s" % (cb,))
nb = has_color(ra, 862, 58, 892, 90, (106, 90, 172), 70)
check("badge purple ring 6A5ACD", nb > 4, "purple px=%d" % nb)

# ---------------- 2. top example panel ----------------
c = region_mode(ra, 200, 90, 260, 100)
check("top panel interior WHITE", near(c, (255, 255, 255), 14), "mode=%s" % (c,))
nb = has_color(ra, 66, 56, 74, 124, (0, 0, 255), 70)
check("top panel blue outline 0000FF", nb > 20, "blue px=%d" % nb)

# header row x1..x6 must be blue
nb = has_color(ra, 86, 62, 216, 76, (0, 0, 255), 70)
check("top header blue x1..x6", nb > 20, "blue px=%d" % nb)

# "Step eta = 2" red at x365..435 y66..80
nr = has_color(ra, 363, 64, 437, 82, (216, 38, 44), 60)
check("'Step eta = 2' red D8262C", nr > 10, "red px=%d" % nr)

# ---------------- 3. augmented table ----------------
c = region_mode(ra, 90, 165, 230, 170)
check("aug table interior white", near(c, (255, 255, 255), 12), "mode=%s" % (c,))
nb = has_color(ra, 148, 145, 240, 161, (0, 0, 255), 70)
check("aug title blue", nb > 8, "blue px=%d" % nb)
nr = has_color(ra, 92, 229, 110, 245, (216, 38, 44), 60)
check("aug class row C1 red", nr > 4, "red px=%d" % nr)
nb2 = has_color(ra, 112, 229, 130, 245, (0, 0, 255), 70)
check("aug class row C2 blue", nb2 > 4, "blue px=%d" % nb2)

# ---------------- 4. iteration badge ----------------
c = region_mode(ra, 90, 285, 200, 298)
check("iteration badge red fill D8262C", near(c, (216, 38, 44), 45), "mode=%s" % (c,))

# ---------------- 5. stop box ----------------
c = region_mode(ra, 80, 345, 220, 350)
check("stop box interior white", near(c, (255, 255, 255), 12), "mode=%s" % (c,))
nr = has_color(ra, 64, 332, 244, 340, (216, 38, 44), 60)
check("stop box red border", nr > 10, "red px=%d" % nr)
nr = has_color(ra, 68, 376, 170, 392, (255, 0, 0), 60)
check("'Stop Iterations' red FF0000", nr > 8, "red px=%d" % nr)

# ---------------- 6. calc panel ----------------
c = region_mode(ra, 420, 150, 480, 160)
check("calc panel interior white", near(c, (255, 255, 255), 10), "mode=%s" % (c,))

# grey rules present at measured positions (y140,197,206,263,272,329,338,395,404,461,470,528)
for y in [140, 197, 206, 263, 272, 329, 338, 395, 404, 461, 470, 528]:
    n = has_color(ra, 300, y - 1, 700, y + 1, (217, 217, 217), 26)
    check("calc grey rule at y%d" % y, n > 100, "grey px=%d" % n)

# black text present in each of the six rows
for i, (y0, y1) in enumerate([(150, 190), (219, 259), (283, 324), (350, 392), (412, 458), (478, 522)]):
    n = has_color(ra, 280, y0, 800, y1, (0, 0, 0), 90)
    check("calc row %d has black text" % (i + 1), n > 200, "black px=%d" % n)

# left bracket verticals for row 1 at x379.5 and x403.5, spanning y146..191
for label, x in [("d-vec left bracket x379.5", 379), ("d-vec right bracket x403.5", 403)]:
    n = has_color(ra, x - 1, 147, x + 1, 190, (0, 0, 0), 110)
    check("calc %s" % label, n > 30, "black px=%d" % n)

# W bracket verticals row 1 at x729.5 / x753.5
for label, x in [("W-vec left bracket x729.5", 729), ("W-vec right bracket x753.5", 753)]:
    n = has_color(ra, x - 1, 147, x + 1, 190, (0, 0, 0), 110)
    check("calc %s" % label, n > 30, "black px=%d" % n)

# ---------------- summary ----------------
npass = sum(1 for _, ok, _ in results if ok)
nfail = len(results) - npass
print("\n%d checks: %d PASS, %d FAIL" % (len(results), npass, nfail))
if nfail:
    print("FAILED: " + "; ".join(n for n, ok, _ in results if not ok))
sys.exit(1 if nfail else 0)
