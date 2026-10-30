#!/usr/bin/env python3
"""Measure 051 original ink extents for row-level elements + column bows,
then try mathtext spacing variants for dzlabel/rowvec/step widths."""
import json, os, sys
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
sys.path.insert(0, f"/home/ahmed/Projects/ai_llm_slides/scripts")
os.environ.setdefault("TMPDIR", "/home/ahmed/Projects/ai_llm_slides/scratch/tmp")

orig = np.array(Image.open(f"{BASE}/unique_slides/slide_051.jpg").convert("L")).astype(float)
ink = orig < 200

def bbox(name, y0, y1, x0, x1):
    sub = ink[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(ys) == 0:
        print(f"{name}: EMPTY")
        return None
    r = (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())
    print(f"{name}: ink x{r[0]}..{r[1]} (w={r[1]-r[0]+1}pt) y{r[2]}..{r[3]} (h={r[3]-r[2]+1}pt)")
    return r

print("== ORIGINAL row-level ink extents ==")
bbox("dzlabel row1 (d(Z1)=)", 155, 178, 278, 332)
bbox("dzlabel row2", 224, 247, 278, 332)
bbox("dzlabel row3", 290, 313, 278, 332)
bbox("rowvec row1 (blue (1 0 0))", 147, 170, 324, 379)
bbox("rowvec row2", 216, 239, 324, 379)
bbox("rowvec row3", 282, 305, 324, 379)
bbox("step (red Step eta = 1)", 60, 86, 358, 470)
bbox("initialW col", 55, 110, 322, 360)
bbox("green col row1 (5;-1;-1)", 143, 196, 372, 412)
bbox("green col row2", 213, 264, 372, 412)
bbox("green col row3", 279, 330, 372, 412)
bbox("'Initial W =' text", 70, 90, 258, 322)

print("== ORIGINAL bows: sample cols (y74..110) ==")
for i, (lx, rx) in enumerate([(90, 102), (111, 124), (134, 147), (156, 170), (179, 192), (202, 214)]):
    lsub = ink[74:110, lx - 4:lx + 3]
    ys, xs = np.nonzero(lsub)
    apex = lx - 4 + xs.min() if len(xs) else None
    print(f" col{i+1} lp window x{lx-4}..{lx+2}: apex x={apex}, ink y {74+ys.min()}..{74+ys.max()}" if len(xs) else f" col{i+1} lp: -")
print("== ORIGINAL bows: Z cols (y76..112) ==")
for i, (lx, rx) in enumerate([(598, 612), (621, 634), (643, 656)]):
    lsub = ink[76:112, lx - 4:lx + 3]
    ys, xs = np.nonzero(lsub)
    if len(xs):
        print(f" Z{i+1} lp apex x={lx-4+xs.min()}, ink y {76+ys.min()}..{76+ys.max()}")
print("== ORIGINAL bows: aug cols (y177..228) ==")
for i, (lx, rx) in enumerate([(94, 107), (115, 128), (137, 151), (160, 173), (182, 195), (205, 218)]):
    lsub = ink[177:228, lx - 4:lx + 3]
    ys, xs = np.nonzero(lsub)
    if len(xs):
        print(f" aug{i+1} lp apex x={lx-4+xs.min()}, ink y {177+ys.min()}..{177+ys.max()}")

print("== MATHTEXT WIDTH EXPERIMENTS ==")
import importlib.util
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
rq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rq)

EXP = f"{BASE}/recreated_pptx/qa/slide051/eq_experiments"
os.makedirs(EXP, exist_ok=True)

def try_eq(tag, latex, fs, color):
    out = f"{EXP}/exp_{tag}.png"
    try:
        info = rq.render(latex, out, fs, color)
        print(f" {tag:34s} fs{fs:6.2f} ink-> w {info['w_in']*72:6.1f}pt h {info['h_in']*72:5.1f}pt  latex={latex}")
    except Exception as e:
        print(f" {tag}: FAIL {e}")

for tag, latex, fs, col in [
    ("dz_nospace", "d(Z_1)=", 15.38, "#000000"),
    ("dz_thin", "d(Z_1)\\;=\\;", 15.38, "#000000"),
    ("dz_nospace_stixsans", "d(Z_1)=", 15.38, "#000000"),
    ("dz_neg", "d(Z_1)\\!=\\!", 15.38, "#000000"),
    ("rv_semi", "(1\\;0\\;0)", 15.56, "#0F0087"),
    ("rv_thin", "(1\\,\\,0\\,\\,0)", 15.56, "#0F0087"),
    ("rv_thin2", "(1\\,0\\,0)", 15.56, "#0F0087"),
    ("rv_semi2", "(1\\;\\,0\\;\\,0)", 15.56, "#0F0087"),
    ("step_tight", "Step\\,\\eta\\,=\\,1", 14.43, "#A1232A"),
    ("step_semi", "Step\\;\\eta\\;=\\;1", 14.43, "#A1232A"),
    ("step_rm", "\\mathrm{Step}\\;\\eta\\;=\\;1", 14.43, "#A1232A"),
]:
    try_eq(tag, latex, fs, col)
