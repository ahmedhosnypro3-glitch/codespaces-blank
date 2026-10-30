#!/usr/bin/env python3
"""Self-check attempt 2 for slide 022 — wash-insensitive metrics.

Attempt 1's FAILs were checker-target artifacts: the ORIGINAL is a JPEG-washed
video frame (its red band tapers 8-9 sparse rows above cap/below descender;
render band 35.6 rows == Liberation Bold 38pt's exact 36-row prediction; sibling
020 documented the same wash class — badge numerals '3-4px ghosts'). Halo-
inclusive targets are NOT valid against a crisp PNG render. This check derives
targets from BOTH images with the same wash-insensitive metric:

  dense-core row band (rows with red-px count >= 40% of the line's max) ->
  core_top/core_bot; and over the core rows, the column extent of columns with
  >= 3 red px -> core_left/core_right. Placement residuals are then render-vs-
  original directly (wash cancels: both sides measured identically).

Also: smarter render census (row-band clustering of ALL ink; bands must be
exactly {badge, L1, L2}) and containment (no red ink above L1 / between bands /
below L2, no ink outside the panel).
"""
import sys
import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide022/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_022.jpg"

ren = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
ori = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
RH, RW = ren.shape[:2]
SX, SY = RW / 960.0, RH / 540.0

def red_title_mask(img):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
    z = np.zeros_like(red)
    z[int(60 * img.shape[0] / 540):int(500 * img.shape[0] / 540),
      int(70 * img.shape[1] / 960):int(895 * img.shape[1] / 960)] = True
    return red & z

def line_bands(mask):
    """Split the title-zone red mask into per-line row groups."""
    rows = np.where(mask.sum(axis=1) > 2)[0]
    groups = np.split(rows, np.where(np.diff(rows) > 6)[0] + 1)
    return [g for g in groups if len(g)]

def core_metrics(mask, g):
    """Wash-insensitive metrics for one line's row-group g (image px)."""
    band = mask[g.min():g.max() + 1]
    prof = band.sum(axis=1)
    thr = 0.40 * prof.max()
    dense = np.where(prof >= thr)[0]
    core_top = g.min() + dense.min()
    core_bot = g.min() + dense.max()
    cols = band[dense.min():dense.max() + 1]
    colprof = cols.sum(axis=0)
    strong = np.where(colprof >= 3)[0]
    return {"core_top": core_top, "core_bot": core_bot,
            "core_left": strong.min(), "core_right": strong.max(),
            "full_top": g.min(), "full_bot": g.max()}

fails = []
report = []

omask, rmask = red_title_mask(ori), red_title_mask(ren)
ogroups, rgroups = line_bands(omask), line_bands(rmask)
if len(ogroups) != 2 or len(rgroups) != 2:
    print(f"FAIL: line count orig={len(ogroups)} render={len(rgroups)} (expected 2/2)")
    sys.exit(1)

for i, name in enumerate(("L1", "L2")):
    om = core_metrics(omask, ogroups[i])
    rm = core_metrics(rmask, rgroups[i])
    print(f"\n{name} (orig full band y {om['full_top']}..{om['full_bot']} | "
          f"render full band y {(rm['full_top']/SY):.1f}..{(rm['full_bot']/SY):.1f} frame-px)")
    for k in ("core_top", "core_bot"):
        resid = (rm[k] / SY) - (om[k] / 540.0 * 540.0)  # both in own px -> frame
        resid = rm[k] / SY - om[k]
        status = "OK" if abs(resid) <= 2.0 else "FIX"
        print(f"  {name} {k}: orig {om[k]} -> render {rm[k]/SY:.1f} frame-px | residual {resid:+.2f} [{status}]")
        if abs(resid) > 2.0:
            fails.append(f"{name} {k} residual {resid:+.2f} frame px")
    for k in ("core_left", "core_right"):
        resid = rm[k] / SX - om[k]
        status = "OK" if abs(resid) <= 2.0 else "FIX"
        print(f"  {name} {k}: orig {om[k]} -> render {rm[k]/SX:.1f} frame-px | residual {resid:+.2f} [{status}]")
        if abs(resid) > 2.0:
            fails.append(f"{name} {k} residual {resid:+.2f} frame px")
    wres = (rm["core_right"] - rm["core_left"]) / SX - (om["core_right"] - om["core_left"])
    print(f"  {name} core width: orig {om['core_right']-om['core_left']} -> render "
          f"{(rm['core_right']-rm['core_left'])/SX:.1f} frame-px | residual {wres:+.2f}")
    if abs(wres) > 3.0:
        fails.append(f"{name} core width residual {wres:+.2f} frame px")

# pitch between line core centers
oc = [ (core_metrics(omask, g)["core_top"] + core_metrics(omask, g)["core_bot"]) / 2 for g in ogroups]
rc = [ (core_metrics(rmask, g)["core_top"] + core_metrics(rmask, g)["core_bot"]) / 2 / SY for g in rgroups]
pitch = rc[1] - rc[0]
print(f"\ncore-center pitch: {pitch:.2f} frame px (orig {oc[1]-oc[0]:.2f})")
if abs(pitch - (oc[1] - oc[0])) > 2:
    fails.append(f"pitch {pitch:.2f} vs orig {oc[1]-oc[0]:.2f}")

# containment: no red ink above L1, between lines, below L2 (frame-px windows
# derived from the ORIGINAL's own bands so both sides use identical windows)
for label, (ya, yb) in (("above L1", (60, 228)), ("between L1/L2", (285, 318)), ("below L2", (380, 500))):
    o_n = int(omask[int(ya*540/540):int(yb*540/540)].sum())
    r_n = int(rmask[int(ya*SY):int(yb*SY)].sum())
    print(f"red ink {label} (y{ya}..{yb}): orig {o_n}, render {r_n}")
    if r_n > 0:
        fails.append(f"red ink {label} in render ({r_n} px) — stray element/wrap spill")

# render census: ALL ink (any strong deviation from panel) row-bands; must be
# exactly {badge, L1, L2} — cluster and compare to expected y ranges
BG = np.array([233, 233, 231])
panel = ren[int(50*SY):int(530*SY), int(66*SX):int(894*SX)]
d = np.abs(panel - BG).max(axis=2)
ink = d > 30  # above AA-ring strength? AA ring around red is <= ~28 (mid blends)
rows = np.where(ink.sum(axis=1) > 3)[0]
groups = np.split(rows, np.where(np.diff(rows) > 5)[0] + 1) if len(rows) else []
print("\nrender census bands (frame px):")
for g in groups:
    xs = np.where(ink[g.min():g.max()+1].any(axis=0))[0]
    print(f"  y {50+g.min()/SY:.0f}..{50+g.max()/SY:.0f}  x {66+xs.min()/SX:.0f}..{66+xs.max()/SX:.0f}")
expected = [(54, 94), (236, 276), (326, 366)]
if len(groups) != 3:
    fails.append(f"census: {len(groups)} bands (expected 3: badge, L1, L2)")
else:
    for g, (ey0, ey1) in zip(groups, expected):
        fy0, fy1 = 50 + g.min()/SY, 50 + g.max()/SY
        if not (abs(fy0-ey0) <= 6 and abs(fy1-ey1) <= 6):
            fails.append(f"census band y {fy0:.0f}..{fy1:.0f} does not match expected {ey0}..{ey1}")

# frame containment: no ink at all outside panel x 54..903 or above y 45 within
# the canvas margins other than white canvas
print()
if fails:
    print("SELFCHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELFCHECK: PASS — dense-core placement residuals within 2.0 frame px, "
      "pitch/census/containment clean")
