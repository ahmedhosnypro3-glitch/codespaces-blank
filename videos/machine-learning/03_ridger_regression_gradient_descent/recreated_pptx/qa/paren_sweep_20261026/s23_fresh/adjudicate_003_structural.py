#!/usr/bin/env python3
"""PIL adjudication of crop_ps_eq_bottom_judge.txt structural findings (slide 003).

Findings to check against pixels:
  F1 BLOCKER: render left matrix delimiter = vertical bar (orig = paren)
  F2 MAJOR:   render right matrix delimiter doubled (bar + paren)
  F3 MAJOR:   orig per-row parentheses missing in render
  F4 MAJOR:   render highlight fills collide with y-vector closing paren
Crop space: 979x334, cut from the 2001x1125 render at frame (90,340)-(560,500),
scale 2001/960 = 2.0844 (crop_x -> frame_x = 90 + crop_x/2.0844).
"""
import numpy as np
from PIL import Image
from scipy import ndimage

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/paren_sweep_20261026/s23_fresh/adjudication_003_structural.txt"

SC = 2001 / 960.0
OX, OY = 90.0, 340.0

def frame_x(cx): return OX + cx / SC
def frame_y(cy): return OY + cy / SC

def load(name):
    im = Image.open(f"{D}/crop_ps_eq_bottom_{name}.png").convert("RGB")
    g = np.array(im.convert("L")).astype(int)
    a = np.array(im)
    return g, a

def components(g, x0, x1, thr=160, min_h=6):
    """Dark connected components in a column window. Returns list of dicts."""
    sub = g[:, x0:x1] < thr
    lab, n = ndimage.label(sub)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_h * 2 and (ys.max() - ys.min() + 1) < min_h:
            continue
        out.append(dict(x0=x0, comp=i, lab=lab == i, ys=ys, xs=xs + x0,
                        h=int(ys.max() - ys.min() + 1), w=int(xs.max() - xs.min() + 1),
                        cx=float(xs.mean() + x0), cy=float(ys.mean()),
                        ytop=int(ys.min()), ybot=int(ys.max())))
    return out

def belly(lab, ys, xs, frac=0.15):
    """+ = belly right, - = belly left. Mean x of middle band vs tip bands."""
    ytop, ybot = ys.min(), ys.max()
    span = ybot - ytop
    mt = ytop + frac * span
    mb = ybot - frac * span
    mid = (ys >= mt) & (ys <= mb)
    tip = ~mid
    if mid.sum() < 3 or tip.sum() < 3:
        return None, None
    return float(xs[mid].mean() - xs[tip].mean()), (float(xs[mid].mean()), float(xs[tip].mean()))

def profile_line(g, y0, y1, x0, x1, thr=160):
    """For each row in [y0,y1): leftmost and rightmost dark x in window."""
    rows = []
    for y in range(y0, min(y1, g.shape[0])):
        xs = np.where(g[y, x0:x1] < thr)[0]
        if len(xs):
            rows.append((y, x0 + xs.min(), x0 + xs.max()))
    return rows

lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    lines.append(s)

P("=== PIL adjudication — slide 003 crop_ps_eq_bottom structural findings ===")
P("crop 979x334 | frame origin (90,340) | scale %.4f crop px per frame px" % SC)
P("")

for name in ("render", "orig"):
    g, a = load(name)
    P(f"---- {name.upper()} crop ----")

    # F1/F2: matrix delimiter zones. Left delim ~crop x395-430 (frame ~x280? no:)
    # census frame x194 -> crop (194-90)*2.0844 = 216.8 ; frame x388 -> crop 621.2
    for tag, cx0, cx1 in (("LEFT-delim zone", 180, 280), ("RIGHT-delim zone", 570, 700)):
        comps = components(g, cx0, cx1)
        tall = [c for c in comps if c["h"] >= 100]
        short = [c for c in comps if c["h"] < 100]
        P(f"[{tag}] crop x{cx0}..{cx1} (frame x{frame_x(cx0):.1f}..{frame_x(cx1):.1f})")
        for c in tall:
            d, (midm, tipm) = belly(c["lab"], c["ys"], c["xs"])
            P(f"  TALL comp x[{c['xs'].min()}..{c['xs'].max()}] w={c['w']} y[{c['ytop']}..{c['ybot']}] h={c['h']} "
              f"frame_x[{frame_x(c['xs'].min()):.1f}..{frame_x(c['xs'].max()):.1f}] "
              f"belly_delta={d:.2f} (mid_mean={midm:.1f} tips_mean={tipm:.1f})")
        for c in short:
            P(f"  short comp x[{c['xs'].min()}..{c['xs'].max()}] w={c['w']} y[{c['ytop']}..{c['ybot']}] h={c['h']} "
              f"frame_x[{frame_x(c['xs'].min()):.1f}..{frame_x(c['xs'].max()):.1f}] frame_y[{frame_y(c['ytop']):.1f}..{frame_y(c['ybot']):.1f}]")
        if not comps:
            P("  (no dark components)")

    # F3: per-row parens inside matrix interior. Interior crop x~250..600.
    inter = components(g, 250, 600, min_h=4)
    shorts = [c for c in inter if c["h"] <= 40]
    P(f"[INTERIOR short strokes crop x250..600] count={len(shorts)}")
    for c in shorts[:24]:
        P(f"  x[{c['xs'].min()}..{c['xs'].max()}] y[{c['ytop']}..{c['ybot']}] h={c['h']} w={c['w']} "
          f"frame ({frame_x(c['xs'].min()):.1f},{frame_y(c['ytop']):.1f})")

    # F4: fills vs y-vector closing paren. Closing paren census frame x128 -> crop 79.2.
    # Fill colors in this slide: yellow band, pink band. Detect per-column fill pixels.
    r, gr, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    yellow = (r > 215) & (gr > 195) & (b < 190) & (r - b > 60)
    pink = (r > 215) & (b > 175) & (r - gr > 40)
    for tag, mask in (("yellow", yellow), ("pink", pink)):
        colcount = mask.sum(axis=0)
        cols = np.where(colcount > 5)[0]
        if len(cols):
            P(f"[FILL {tag}] columns crop x[{cols.min()}..{cols.max()}] "
              f"frame_x[{frame_x(cols.min()):.1f}..{frame_x(cols.max()):.1f}] peak_col_count={colcount.max()}")
        else:
            P(f"[FILL {tag}] none")
    # closing paren dark stroke columns near crop x60..100
    paren = components(g, 55, 110)
    for c in paren:
        if c["h"] >= 40:
            d, _ = belly(c["lab"], c["ys"], c["xs"])
            P(f"[CLOSE-PAREN zone] tall comp x[{c['xs'].min()}..{c['xs'].max()}] y[{c['ytop']}..{c['ybot']}] h={c['h']} "
              f"frame_x[{frame_x(c['xs'].min()):.1f}..{frame_x(c['xs'].max()):.1f}] belly={d:.2f}")
    P("")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("saved", OUT)
