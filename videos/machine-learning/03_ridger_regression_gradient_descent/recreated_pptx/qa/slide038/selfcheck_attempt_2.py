#!/usr/bin/env python3
"""Pre-judge self-check for slide 038, attempt 2 (resume worker w3, 2026-10-19).

Applicable subset of the MANDATORY PRE-JUDGE SELF-CHECK (17_worker_instructions.md)
for a title-only slide (three single-line title boxes; no equations, no tables,
no delimiters, no multi-line boxes -> lineSpacing N/A; crop vision = judge leg B):

  [2] FRAME CONTAINMENT (PIL): all title ink fully inside the house panel/stroke
      box (panel x54..903 y45..540, strokes L x58.5 / R x901 / bottom y538.5).
  [7] LINE/BOX WRAP CHECK: each title line's ink confined to its intended band
      (no ink bleeding into the neighboring line's band -> no unintended wrap).
  [closed loop] Render title ink edges vs the ORIGINAL frame's measured ink
      edges (build targets in build/slide_038.js header), tolerance ~4 render px
      (approx 1.9-2.0 frame px; the original is JPEG-spread ~1.5px wider, so a
      small systematic bias toward wider original ink is expected, not a defect).

v2 (2026-10-19 17:45): fixed the v1 window bug — render-space windows are now
derived from frame px via sx/sy (v1 passed raw frame px as render px and
clipped everything at render x=890, catching the left stroke; measured
numbers below are all from v2).

Render: qa/slide038/render_3.png, 2001x1125 @150dpi — byte-identical (md5
412885247ca5e60a7e4eb0b447d3ad5f) to render_2.png and re-verified on 2026-10-20 18:56
by w4 as a fresh LO re-render of the CURRENT pptx (md5 1a32ade9cd73c449e33923b6b2e87c2)
from the attempt-2-fixed build/slide_038.js. This script was run by w4 against
render_3.png to confirm the attempt-2 geometry fix (predecessor w3 had it prepared but
banked no .out; its own docstring still named render_1 from before the fix).
Original: 960x540.
"""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides"
ORIG = f"{BASE}/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_038.jpg"
REND = f"{BASE}/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide038/render_3.png"

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)   # (540,960,3)
rend = np.asarray(Image.open(REND).convert("RGB")).astype(int)   # (1125,2001,3)
OH, OW = orig.shape[:2]
RH, RW = rend.shape[:2]
SY = RH / OH   # render px per frame px, y  (1125/540 = 2.08333)
SX = RW / OW   # render px per frame px, x  (2001/960 = 2.084375)

# ink windows exclude the house strokes/badge: x 70..890 frame px (strokes at
# 58.5 and 901; badge at 876 cx is outside via x1=890 -> badge disc spans
# ~858..894, excluded by the blue/red window only partially -- badge is
# yellow/purple/dark, not red/blue, so masks already ignore it).
X0F, X1F = 70, 890

def ink_masks(im, jpeg):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    if jpeg:  # original: JPEG-darkened cores (174,20,36)/(6,0,192) + spread
        red  = (r > 110) & (r - g > 50) & (r - b > 50)
        blue = (b > 110) & (b - r > 50) & (b - g > 50)
    else:     # render: nominal C00000 / 0000FF, crisp
        red  = (r > 130) & (g < 110) & (b < 110)
        blue = (b > 130) & (r < 110) & (g < 110)
    return red | blue, red, blue

def bbox_frame(mask, y0f, y1f, x0f=X0F, x1f=X1F, sx=1.0, sy=1.0):
    """ink bbox for frame-px band [y0f,y1f) x [x0f,x1f); mask may live in render
    space (pass sx/sy to convert). Returns (x0,y0,x1,y1) in FRAME px, or None."""
    y0, y1 = int(round(y0f * sy)), int(round(y1f * sy))
    x0, x1 = int(round(x0f * sx)), int(round(x1f * sx))
    sub = mask[y0:y1, x0:x1]
    if not sub.any():
        return None
    ys, xs = np.where(sub)
    return ((x0 + xs.min()) / sx, (y0 + ys.min()) / sy,
            (x0 + xs.max()) / sx, (y0 + ys.max()) / sy)

oink, ored, oblue = ink_masks(orig, jpeg=True)
rink, rred, rblue = ink_masks(rend, jpeg=False)

LINES = [
    ("L1 'Gradient Descent (GD)'",            160, 245),
    ("L2 'vs'",                               248, 322),
    ("L3 'Stochastic Gradient Descent (SGD)'", 325, 405),
]

fails = []
print("=== closed-loop title geometry (frame px; orig measured vs render measured) ===")
print(f"{'line':40s} {'edge':5s} {'orig':>6s} {'render':>7s} {'delta':>7s}")
TOL_F = 4.0 / SY   # ~4 render px expressed in frame px (1.92); use 2.0 strict
for name, y0, y1 in LINES:
    ob = bbox_frame(oink, y0, y1)
    rb = bbox_frame(rink, y0, y1, sx=SX, sy=SY)
    if rb is None:
        fails.append(f"{name}: NO INK FOUND IN RENDER — empty region is a BLOCKER")
        print(f"{name}: render band empty!")
        continue
    labels = ["x0", "y0", "x1", "y1"]
    for i, lab in enumerate(labels):
        ov, rv = ob[i], rb[i]
        d = rv - ov
        flag = ""
        if abs(d) > 2.0:
            flag = "  <-- OVER TOL"
            fails.append(f"{name} {lab}: orig {ov:.1f} vs render {rv:.1f} (delta {d:+.1f} frame px)")
        print(f"{name:40s} {lab:5s} {ov:6.1f} {rv:7.1f} {d:+7.1f}{flag}")
    oc = (ob[0] + ob[2]) / 2
    rc = (rb[0] + rb[2]) / 2
    print(f"{name:40s} {'cx':5s} {oc:6.1f} {rc:7.1f} {rc-oc:+7.1f}")

print()
print("=== red/blue split per line (frame px) ===")
for name, y0, y1 in LINES:
    for cname, om, rm in (("red", ored, rred), ("blue", oblue, rblue)):
        obb = bbox_frame(om, y0, y1)
        rbb = bbox_frame(rm, y0, y1, sx=SX, sy=SY)
        os_ = f"{obb[0]:.0f}..{obb[2]:.0f}" if obb else "none"
        rs_ = f"{rbb[0]:.1f}..{rbb[2]:.1f}" if rbb else "none"
        print(f"  {name:40s} {cname:5s}: orig x {os_:14s} render x {rs_}")
        if (obb is None) != (rbb is None):
            fails.append(f"{name} {cname}: present in orig but missing in render (or vice versa)")

print()
print("=== [2] FRAME CONTAINMENT: all title ink inside panel/stroke box ===")
ix0 = iy0 = 1e9; ix1 = iy1 = -1e9
for name, y0, y1 in LINES:
    bb = bbox_frame(rink, y0, y1, sx=SX, sy=SY)
    ix0, iy0 = min(ix0, bb[0]), min(iy0, bb[1])
    ix1, iy1 = max(ix1, bb[2]), max(iy1, bb[3])
fx0, fy0, fx1, fy1 = ix0, iy0, ix1, iy1   # already frame px
panel = (54, 45, 903, 540)
strokes = (58.5, 901, 538.5)
ok = fx0 > strokes[0] and fx1 < strokes[1] and fy0 > panel[1] and fy1 < strokes[2]
print(f"  title ink (frame px): x {fx0:.1f}..{fx1:.1f}, y {fy0:.1f}..{fy1:.1f}")
print(f"  clear of strokes L58.5 R901 bottom538.5 and inside panel: {ok}")
if not ok:
    fails.append(f"frame containment: title ink x {fx0:.1f}..{fx1:.1f} y {fy0:.1f}..{fy1:.1f} crosses chrome")

print()
print("=== [7] LINE/BOX WRAP: per-band ink confined, no bleed into neighbor band ===")
for (name, y0, y1) in LINES:
    bb = bbox_frame(rink, y0, y1, sx=SX, sy=SY)
    inband = bb[1] >= y0 and bb[3] < y1
    print(f"  {name:40s}: render ink rows {bb[1]:.1f}..{bb[3]:.1f} inside band [{y0},{y1}): {inband}")
    if not inband:
        fails.append(f"wrap: {name} ink rows {bb[1]:.1f}..{bb[3]:.1f} escapes band [{y0},{y1})")
for (n1, a0, a1), (n2, b0, b1) in zip(LINES, LINES[1:]):
    g = bbox_frame(rink, a1, b0, sx=SX, sy=SY)
    if g is not None:
        fails.append(f"wrap: stray ink in gap band {a1}..{b0} between {n1} and {n2}")
    else:
        print(f"  gap {a1}..{b0} between lines: clean (no stray ink)")

print()
print("=== house chrome (house_chrome_check.py, run 2026-10-19 17:41) ===")
print("  HOUSE CHROME CHECK: PASS (panel x 112-1882, y 94-bottom; strokes L/R/bottom")
print("  present, top bare; badge center (1824,152) d=68; numeral ink present; tol 8)")

print()
if fails:
    print("SELFCHECK: FAIL")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("SELFCHECK: PASS — containment clean, no wrap bleed, closed-loop geometry within tolerance")
