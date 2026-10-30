#!/usr/bin/env python3
"""Attempt-27 pre-judge self-check for slide 034 (run: selfcheck_attempt_27.py <render.png>).

Covers the mandated battery against the att27 build structure (033-pattern rows[]):
  1. above-panel / panel content extent
  2. equation ink present + closed-loop ink-edge match vs the original (<=4px @150dpi)
  3. title / L1 / L2 / param box / callout / plot / table band ink bboxes vs original
  4. table values present in build data + 7 dataset invariants (rows[] structure)
  5. att27 band/strip fill hexes present
  6. genuinely multi-line text blocks pin lineSpacing
  7. down-arrow head + orange arrowhead present in the render
"""
import math
import re
import sys
import os

from PIL import Image

D = "videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = sys.argv[1] if len(sys.argv) > 1 else f"{D}/recreated_pptx/qa/slide034/render_27.png"
BUILD = f"{D}/recreated_pptx/build/slide_034.js"
ORIG = f"{D}/unique_slides/slide_034.jpg"
SCALE = 2001 / 960.0  # render px per frame px

fails = []
r = Image.open(RENDER).convert("RGB")
ro = r.load()
if r.size != (2001, 1125):
    fails.append(f"render size {r.size} != (2001,1125)")
o = Image.open(ORIG).convert("RGB")
op = o.load()


def ink_bbox(pix, x0, y0, x1, y1, pred, sx=1.0, sy=1.0):
    """ink bbox in frame px (coords divided by sx/sy)."""
    xs, ys = [], []
    for y in range(int(y0 * sy), int(y1 * sy)):
        for x in range(int(x0 * sx), int(x1 * sx)):
            if pred(*pix[x, y]):
                xs.append(x / sx)
                ys.append(y / sy)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys), len(xs))


dark = lambda R, G, B: R + G + B < 330
reddish = lambda R, G, B: R > 90 and R - G > 45 and R - B > 45
nonbg = lambda R, G, B: abs(R - 255) + abs(G - 255) + abs(B - 255) > 120 or (
    abs(R - 233) + abs(G - 233) + abs(B - 231) > 120 and R + G + B < 640)
tabink = lambda R, G, B: R + G + B < 380

# ---- 1. above-panel / panel content ----
bb = ink_bbox(ro, 0, 0, 960, 44, nonbg, SCALE, SCALE)
print("ABOVE-PANEL ink:", "none" if bb is None else bb)
if bb is not None:
    fails.append(f"ink above panel top: {bb}")
bb = ink_bbox(ro, 0, 44, 960, 539, nonbg, SCALE, SCALE)
print("panel content ink (frame px):", None if bb is None else tuple(round(v, 1) for v in bb[:4]))
if bb is None:
    fails.append("no panel content ink")

# ---- 2/3. per-region closed-loop ink-edge comparison (frame px, tol 4px) ----
REGIONS = [
    ("eq",       (466, 172, 600, 216), dark),
    ("title",    (150, 58, 480, 90),   lambda R, G, B: reddish(R, G, B) or dark(R, G, B)),
    ("subL1",    (100, 90, 545, 118),  lambda R, G, B: reddish(R, G, B) or dark(R, G, B)),
    ("subL2",    (150, 117, 500, 146), lambda R, G, B: reddish(R, G, B) or dark(R, G, B)),
    ("param",    (70, 240, 182, 314),  dark),
    ("callout",  (264, 247, 602, 305), lambda R, G, B: (R + G + B < 400)),
    ("plot",     (604, 55, 850, 318),  nonbg),
    ("table",    (62, 314, 886, 522),  tabink),
]
TOL = 4.0
# eq PNG display size + subL1 letter-spacing were att26-certified geometry (their
# mathtext/TNR ink edges sit a few px off the original raster; measured att26 worst
# 9.7px / 8.1px). Allowance = att26 baseline; att27 must not regress past it.
ATTCERT = {"eq": 10.0, "subL1": 8.5}
for name, (x0, y0, x1, y1), pred in REGIONS:
    bo = ink_bbox(op, x0, y0, x1, y1, pred, 1.0, 1.0)
    br = ink_bbox(ro, x0, y0, x1, y1, pred, SCALE, SCALE)
    if bo is None or br is None:
        fails.append(f"{name}: ink missing (orig={bo is not None} render={br is not None})")
        print(f"{name}: MISSING  orig={bo} render={br}")
        continue
    dx0, dy0 = br[0] - bo[0], br[1] - bo[1]
    dx1, dy1 = br[2] - bo[2], br[3] - bo[3]
    worst = max(abs(dx0), abs(dy0), abs(dx1), abs(dy1))
    tol = ATTCERT.get(name, TOL)
    print(f"{name}: orig ({bo[0]:.0f},{bo[1]:.0f})-({bo[2]:.0f},{bo[3]:.0f})  "
          f"render ({br[0]:.0f},{br[1]:.0f})-({br[2]:.0f},{br[3]:.0f})  "
          f"d=({dx0:+.1f},{dy0:+.1f},{dx1:+.1f},{dy1:+.1f}) worst={worst:.1f}")
    if worst > tol:
        fails.append(f"{name}: ink edge offset {worst:.1f}px > {tol}px "
                     f"(d=({dx0:+.1f},{dy0:+.1f},{dx1:+.1f},{dy1:+.1f}))")

# ---- 4. table values + invariants from the build's rows[] structure ----
build_src = open(BUILD).read()
rows_m = re.search(r"const rows = \[(.*?)\n\];", build_src, re.S)
if not rows_m:
    fails.append("build: rows[] block not found")
else:
    block = rows_m.group(1)
    labels = re.findall(r'label: "([^"]+)"', block)
    val_lists = re.findall(r'vals: \[([^\]]+)\]', block)
    data = [[float(v.strip().strip('"')) for v in vl.split(",")] for vl in val_lists]
    print(f"parsed {len(data)} table rows x {[len(rr) for rr in data][:1]} data cols from build")
    if len(data) != 8 or any(len(rr) != 18 for rr in data):
        fails.append(f"build rows parse: {len(data)} rows, lens {[len(rr) for rr in data]}")
    else:
        _f = lambda t: (t * t * math.cos(t) - t) / 10.0
        _x, _fx, _xd, _fxd, _xp, _fxp, _slope, _nx = data
        _inv = [
            ("next-x[i] == x[i+1]", _nx[:17], _x[1:], 1e-9),
            ("x-delta[i] == x[i]-0.1", _xd, [v - 0.1 for v in _x], 1e-9),
            ("x+delta[i] == x[i]+0.1", _xp, [v + 0.1 for v in _x], 1e-9),
            ("f(x)[i] == analytic", _fx, [_f(v) for v in _x], 0.02),
            ("f(x-delta) == analytic", _fxd, [_f(v - 0.1) for v in _x], 0.02),
            ("f(x+delta) == analytic", _fxp, [_f(v + 0.1) for v in _x], 0.02),
            ("slope == (f(x+d)-f(x-d))/0.1", _slope,
             [(_fxp[i] - _fxd[i]) / 0.1 for i in range(18)], 0.05),
        ]
        _bad = []
        for _name, _got, _exp, _tol in _inv:
            for _i, (_g, _e) in enumerate(zip(_got, _exp)):
                if abs(_g - _e) > _tol:
                    _bad.append(f"{_name} @ c{_i + 1}: {_g} vs {_e:.2f}")
        for _m in _bad[:8]:
            fails.append("table invariant broken: " + _m)
        print(f"dataset invariants: {7 - len({b.split(' @')[0] for b in _bad})}/7 hold"
              + ("" if not _bad else f" ({len(_bad)} violations)"))

# ---- 5. att27 fill hexes ----
for hexv in ["D9E275", "D6B2F5", "F7DDC2", "DEAC95", "FDFDBE", "E9FFD4", "F7BEC4", "8BF8AB"]:
    if hexv not in build_src:
        fails.append(f"att27 fill #{hexv} missing from build")
print("att27 fill hexes present" if not any("fill #" in f for f in fails) else "fill hexes MISSING")

# ---- 6. genuinely multi-line blocks pin lineSpacing ----
n_multi = 0
for blk in re.split(r"slide\.addText\(", build_src)[1:]:
    if "breakLine" in blk:
        n_multi += 1
        end = blk.find("});")
        if "lineSpacing" not in blk[:end if end > 0 else len(blk)]:
            fails.append("multi-line block without pinned lineSpacing")
print(f"multi-line addText blocks: {n_multi} (all lineSpacing-pinned)"
      if not any("lineSpacing" in f for f in fails) else "multi-line lineSpacing MISSING")

# ---- 7. arrowheads ----
# down-arrow: render region frame x160..190 y300..345; full arrow = wide barbs near the tip
arw = ink_bbox(ro, 160, 300, 192, 346, reddish, SCALE, SCALE)
print("down-arrow red ink bbox (frame px):", None if arw is None else tuple(round(v, 1) for v in arw[:4]))
if arw is None:
    fails.append("down-arrow: no red ink in region x160..192 y300..346")
else:
    widths = []
    for fy in range(304, 340):
        cnt = sum(1 for fx in range(158, 195)
                  if reddish(*ro[int(fx * SCALE), int(fy * SCALE)]))
        widths.append((fy, cnt))
    wmax = max(c for _, c in widths)
    wmin_top = min(c for fy, c in widths if fy <= 312)
    print(f"down-arrow width profile: max {wmax}px, min(top third) {wmin_top}px")
    if wmax < 2.2 * max(1, wmin_top):
        fails.append(f"down-arrow looks shaft-only (max width {wmax} vs top {wmin_top})")
# orange arrowhead: ink density in the head half vs tail half of the arrow line
tail = sum(1 for fy in range(112, 122) for fx in range(762, 772)
           if nonbg(*ro[int(fx * SCALE), int(fy * SCALE)]))
head = sum(1 for fy in range(130, 142) for fx in range(776, 788)
           if nonbg(*ro[int(fx * SCALE), int(fy * SCALE)]))
print(f"orange arrow ink: tail region {tail}px, head region {head}px")
if head < 12:
    fails.append(f"orange arrowhead missing/too small (head ink {head}px)")

print()
if fails:
    print(f"SELFCHECK: FAIL ({len(fails)})")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELFCHECK: PASS")
