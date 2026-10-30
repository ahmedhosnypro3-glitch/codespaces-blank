#!/usr/bin/env python3
"""Closed-loop self-check for slide 027 render_K (150dpi, 2001x1125).

Compares every element's rendered ink band against the banked dossier geometry
(qa/slide027/measured_geometry.md, frame 960x540, 1px=1pt). Scale: render_px =
frame_px * (H_render/540). Prints per-element measured-vs-expected and, for text,
the DY correction (frame px) that would align the render to the target band.

Usage: selfcheck.py <render.png>
"""
import sys

import numpy as np
from PIL import Image

RENDER = sys.argv[1] if len(sys.argv) > 1 else \
    "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide027/render_1.png"
im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
S = H / 540.0
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def cv(v):  # frame px -> render px
    return v * S

def band(mask, axis):
    idx = np.where(mask.sum(axis=axis) > 0)[0]
    return (idx.min(), idx.max()) if len(idx) else (None, None)

def region(mask, y0, y1, x0, x1):
    """mask restricted to a frame-px window -> bbox in frame px."""
    sub = mask[int(cv(y0)):int(cv(y1)) + 1, int(cv(x0)):int(cv(x1)) + 1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return ((ys.min() / S, ys.max() / S), (xs.min() / S + x0, xs.max() / S + x0),
            int(sub.sum()))

print(f"render {W}x{H}, scale {S:.4f}")

# masks (LO renders are clean; JPEG halo absent)
title_red = (r > 100) & (g < 80) & (b < 80) & (r - g > 60)          # 8B0000-ish
box_red = (r > 190) & (g < 90) & (b < 90)                            # FF0000 border
black = (r < 90) & (g < 90) & (b < 90)                              # axes/curve/text
blue = (b > 140) & (b > r + 40) & (g < 120)                        # violet 5F41C4 dots (w8 attempt 3)
yellow = (r > 200) & (g > 200) & (b < 120)                           # FFFF00

def show(name, mask, y0, y1, x0, x1, exp):
    got = region(mask, y0, y1, x0, x1)
    if got is None:
        print(f"  {name:16s} NO INK in window rows {y0}-{y1}, cols {x0}-{x1}  <<< CHECK")
        return None
    (ry0, ry1), (rx0, rx1), n = got
    ey0, ey1, ex0, ex1 = exp
    print(f"  {name:16s} rows {ry0:6.1f}..{ry1:6.1f} (exp {ey0}..{ey1}, dy_bot {ry1-ey1:+.1f})"
          f"  cols {rx0:6.1f}..{rx1:6.1f} (exp {ex0}..{ex1}, dx_c {(rx0+rx1)/2-(ex0+ex1)/2:+.1f})  ink {n}")
    return got

print("== TITLE (dark red 8B0000) ==")
show("title L1", title_red, 60, 110, 120, 800, (73, 100, 191, 744))
show("title L2", title_red, 100, 150, 260, 700, (108, 135, 321, 621))

print("== GRAPH BOX (FF0000 border) ==")
show("box left", box_red, 160, 512, 185, 200, (167, 507, 193, 194))
show("box right", box_red, 160, 512, 710, 722, (167, 507, 715, 717))
show("box top", box_red, 160, 175, 185, 722, (166, 168, 193, 717))
show("box bottom", box_red, 500, 512, 185, 722, (506, 508, 193, 717))

print("== AXES + HEADS (black) ==")
show("y-axis", black, 225, 430, 215, 230, (222, 435, 222, 224))
show("y-head", black, 200, 226, 212, 235, (206, 222, 218, 228))
show("x-axis", black, 428, 445, 230, 665, (431, 442, 222, 685))
show("x-head", black, 425, 450, 665, 692, (431, 442, 670, 686))

print("== DASHES (black, count bands on the dashed columns) ==")
for cx, lo, hi in [(262.5, 265, 440), (444.5, 410, 440)]:
    col = black[:, int(cv(cx)) - 1:int(cv(cx)) + 2].sum(axis=1) > 0
    seg = col[int(cv(lo)):int(cv(hi))]
    rows_ = np.where(seg)[0]
    runs = []
    if len(rows_):
        s_ = p_ = rows_[0]
        for yv in rows_[1:]:
            if yv == p_ + 1:
                p_ = yv
            else:
                runs.append((round(s_ / S, 1), round(p_ / S, 1))); s_ = p_ = yv
        runs.append((round(s_ / S, 1), round(p_ / S, 1)))
    print(f"  x={cx}: {len(runs)} dashes rows(frame) {runs}")

print("== PARABOLA (point-to-ink from banked trace knots) ==")
try:
    from scipy.spatial import cKDTree
    TRACE = [(253,230),(254,236),(255,242),(256,246),(259,252),(262,272),(268,280),
             (270,286),(272,292),(274,296),(276,300),(278,302),(288,318),(290,322),
             (291,324),(293,326),(294,328),(296,330),(297,332),(299,334),(313,350),
             (316,352),(318,354),(320,356),(322,358),(324,360),(363,386),(365,388),
             (383,395),(400,400),(420,404),(436,406),(445,408),(463,406),(479,404),
             (497,400),(525,390),(543,380),(561,368),(571,360),(584,348),(595,336),
             (604,324),(612,312),(619,300),(624,288),(628,280),(632,268),(635,260),
             (637,252),(638,248),(639,244),(640,240),(641,236)]
    curve_win = black.copy()
    curve_win[: int(cv(160)), :] = False
    curve_win[int(cv(510)):, :] = False
    # exclude text/dot/head zones by windows: keep only near the trace path
    ys_, xs_ = np.where(curve_win)
    pts = np.stack([xs_ / S, ys_ / S], axis=1)   # (x,y) order to match TRACE — w8 bugfix 2026-10-20
    tree = cKDTree(pts)
    d, _ = tree.query(np.array(TRACE, dtype=float))
    print(f"  trace->render-ink distance: max {d.max():.2f} frame px, mean {d.mean():.2f}")
except ImportError:
    print("  (scipy unavailable — skipped)")

print("== DOTS ==")
BLUE = [(262.0,263.5),(283.0,310.5),(306.5,342.0),(332.0,366.5),(354.5,380.5),
        (374.5,390.0),(392.0,396.5),(411.0,403.5),(426.5,403.5)]
for i, (cx, cy) in enumerate(BLUE, 1):
    got = region(blue, cy - 12, cy + 12, cx - 12, cx + 12)
    if got:
        (ry0, ry1), (rx0, rx1), n = got
        print(f"  dot {i}: rows {ry0:6.1f}..{ry1:6.1f} cols {rx0:6.1f}..{rx1:6.1f}"
              f" (exp center {cx},{cy}; d~{rx1-rx0:.1f}x{ry1-ry0:.1f}) ink {n}")
got = region(yellow, 393, 420, 431, 458)
if got:
    (ry0, ry1), (rx0, rx1), n = got
    print(f"  yellow dot: rows {ry0:.1f}..{ry1:.1f} cols {rx0:.1f}..{rx1:.1f} (exp 401..413, 439..450) ink {n}")

print("== TEXT LABELS (black) ==")
show("Cost", black, 170, 195, 195, 245, (176, 189, 200, 238))
show("Learning step", black, 265, 295, 290, 412, (272, 289, 297, 404))
show("Minimum", black, 358, 382, 422, 503, (364, 376, 428, 497))
show("Random", black, 438, 462, 224, 302, (444, 457, 230, 295))
show("initial value", black, 460, 484, 213, 312, (466, 479, 219, 306))
show("theta axis", black, 420, 448, 692, 714, (427, 444, 697, 709))
show("thetahat body", black, 484, 510, 434, 455, (488, 504, 439, 449))
show("thetahat hat", black, 476, 489, 435, 454, (480, 484, 440, 448))

print("== CONTAINMENT (graph content inside box 193.5..716 x 167..507) ==")
inner = black & False
inner = black.copy()
inner[: int(cv(167)) + 2, :] = False       # above box top (title is title_red)
# restrict to graph box interior minus border ring
sub = inner[int(cv(168)):int(cv(506)), int(cv(195)):int(cv(715))]
ys_, xs_ = np.where(sub)
if len(ys_):
    print(f"  graph-ink (black) bbox rows {ys_.min()/S+168:.1f}..{ys_.max()/S+168:.1f}"
          f" cols {xs_.min()/S+195:.1f}..{xs_.max()/S+195:.1f} (must be inside 168..506 x 195..715)")
else:
    print("  no black ink inside box?!")
# title containment inside panel: 54..903
tr = title_red.copy()
tr[int(cv(140)):, :] = False
ys_, xs_ = np.where(tr)
print(f"  title ink cols {xs_.min()/S:.1f}..{xs_.max()/S:.1f} (panel 54..903), rows {ys_.min()/S:.1f}..{ys_.max()/S:.1f}")
