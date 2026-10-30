#!/usr/bin/env python3
"""Shape probes for 003 structural adjudication: doubled right delimiter,
per-row mark glyphs, orig delimiter amplitude at soft threshold."""
import numpy as np
from PIL import Image
from scipy import ndimage

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/paren_sweep_20261026/s23_fresh/probe_003_shapes.txt"

def load(name):
    im = Image.open(f"{D}/crop_ps_eq_bottom_{name}.png").convert("RGB")
    return np.array(im)

ra = load("render")
oa = load("orig")
rg = np.array(Image.open(f"{D}/crop_ps_eq_bottom_render.png").convert("L")).astype(int)
og = np.array(Image.open(f"{D}/crop_ps_eq_bottom_orig.png").convert("L")).astype(int)

lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    lines.append(s)

def ascii_map(g, x0, x1, y0, y1, thr=170, xstep=1, ystep=2):
    P(f"  (ascii x{x0}..{x1} step{xstep}, y{y0}..{y1} step{ystep}, '#'=<{thr})")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1, xstep))
    hdr2 = "     " + "".join(str(x % 10) for x in range(x0, x1, xstep))
    P(hdr); P(hdr2)
    for y in range(y0, y1, ystep):
        row = "".join("#" if g[y, x] < thr else "." for x in range(x0, x1, xstep))
        P(f"{y:4d} {row}")

P("=== A. RENDER right-delimiter zone: what is the w=2 line at crop x633-634? ===")
P("RGB samples along the line (col 633) and neighbors:")
for y in (70, 130, 190, 250, 280):
    P(f"  y={y}: x628={tuple(ra[y,628])} x631={tuple(ra[y,631])} x632={tuple(ra[y,632])} "
      f"x633={tuple(ra[y,633])} x634={tuple(ra[y,634])} x635={tuple(ra[y,635])} x640={tuple(ra[y,640])}")
P("")
P("ASCII render crop x610..660, y40..310:")
ascii_map(rg, 610, 660, 40, 310, thr=170, xstep=1, ystep=6)
P("")
P("ASCII orig crop x595..645, y60..300:")
ascii_map(og, 595, 645, 60, 300, thr=170, xstep=1, ystep=6)
P("")

P("=== B. Per-row mark glyphs at crop x240..262 ===")
for name, g in (("RENDER", rg), ("ORIG", og)):
    P(f"--- {name}: rows y55..95 (row1) and y250..295 (row4) ---")
    ascii_map(g, 240, 262, 55, 95, thr=170, xstep=1, ystep=2)
    ascii_map(g, 240, 262, 250, 295, thr=170, xstep=1, ystep=2)
P("")

P("=== C. ORIG bottom-matrix delimiter amplitude at soft threshold (<210) ===")
for name, g in (("RENDER", rg), ("ORIG", og)):
    for tag, x0, x1 in (("LP", 200, 245), ("RP", 595, 645)):
        sub = (g[:, x0:x1] < 210)
        lab, n = ndimage.label(sub)
        best = None
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            h = ys.max() - ys.min() + 1
            if h > 150 and (best is None or h > best[0]):
                best = (h, ys, xs, i, lab == i)
        if best is None:
            P(f"  {name} {tag}: no tall comp at thr210")
            continue
        h, ys, xs, i, mask = best
        span = ys.max() - ys.min()
        mid = (ys >= ys.min() + 0.25 * span) & (ys <= ys.max() - 0.25 * span)
        tip = ~mid
        P(f"  {name} {tag}: comp h={h} x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] "
          f"belly(midX-tipX)={xs[mid].mean() - xs[tip].mean():+.2f} "
          f"(mid={xs[mid].mean():.1f} tips={xs[tip].mean():.1f})")
P("")

P("=== D. RENDER left delimiter close-up (is it a curve or bar?) crop x210..232, y40..310 ===")
ascii_map(rg, 210, 232, 40, 310, thr=170, xstep=1, ystep=8)
P("")
P("=== E. ORIG left delimiter close-up crop x205..235, y50..300 (thr 210) ===")
ascii_map(og, 205, 235, 50, 300, thr=210, xstep=1, ystep=8)

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("saved", OUT)
