#!/usr/bin/env python3
"""w051_gen_eqs: generate all mathtext assets for slide 051 attempt 3.
600 dpi transparent PNGs + JSON sidecars via scripts/render_eq.py; fontsize
calibrated so each PNG's ink height matches the original's measured paren span
(frame px = pt). Assets -> build/assets/eq_051_*.png + sidecars."""
import subprocess
import json
import numpy as np
from PIL import Image
import os

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
ASSETS = f"{NS}/recreated_pptx/build/assets"
os.makedirs(ASSETS, exist_ok=True)
RENDER_EQ = f"{ROOT}/scripts/render_eq.py"

BLACK = "#000000"
BLUE = "#0F0087"    # measured blue text (15,0,135)
GREEN = "#659969"   # measured DEC interior green (101,153,105)
# core red for the step text: darkest-quartile mean of the red-mask px
im = Image.open(f"{NS}/unique_slides/slide_051.jpg").convert("RGB")
z = np.asarray(im).astype(int)
zone = z[66:81, 366:435]
redmask = (zone[:,:,0] > 110) & (zone[:,:,0]-zone[:,:,1] > 50) & (zone[:,:,0]-zone[:,:,2] > 40)
px = zone[redmask]
lum = px @ [0.299, 0.587, 0.114]
order = np.argsort(lum)
core = px[order[:max(1, len(order)//4)]].mean(axis=0)
RED = "#%02X%02X%02X" % tuple(int(round(c)) for c in core)
print("step red core:", RED, "n=", len(px))

def ink_h(path):
    a = np.asarray(Image.open(path).convert("RGBA"))[:, :, 3]
    rows = np.where((a > 8).any(axis=1))[0]
    return int(rows[-1] - rows[0] + 1)

PT600 = 600.0 / 72.0  # PNG px per slide pt

def gen(name, latex, target_h, color):
    out = f"{ASSETS}/{name}.png"
    target_px = target_h * PT600
    f = 12.0
    for it in range(5):
        r = subprocess.run(["python3", RENDER_EQ, latex, out, str(f), color],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"render_eq failed for {name}: {r.stderr}")
        side = json.loads(r.stdout)
        h = ink_h(out)
        if abs(h - target_px) <= 8:
            break
        f = round(f * target_px / h, 2)
    side["fontsize_pt"] = f
    side["mathtext"] = latex
    side["ink_h_px"] = h
    side["target_h_pt"] = target_h
    json.dump(side, open(out.replace(".png", ".json"), "w"), indent=1)
    print(f"{name}: F={f} ink_h={h} (target {target_px:.0f}px) w={side['w_px']} baseline_frac={side['baseline_frac']:.3f}")
    return side

G3 = r"\genfrac{(}{)}{0}{0}"
def col3(top, mid, bot, pad=""):
    return G3 + "{" + pad + top + pad + "}{\\genfrac{}{}{0}{}{" + pad + mid + pad + "}{" + pad + bot + pad + "}}"
def col2(top, bot):
    return G3 + "{" + top + "}{" + bot + "}"

S = {}
# top-band sample columns (2-entry, paren span y78..106 = 28pt)
for i, (t, b) in enumerate([("1","1"),("2","1"),("1","2"),("5","4"),("6","5"),("6","6")], 1):
    S[f"col_sample_{i}"] = gen(f"eq_051_col_sample_{i}", col2(t, b), 28, BLACK)
# Z columns (2-entry, y80..108 = 28pt)
for i, (t, b) in enumerate([("0","0"),("7","6"),("3","2")], 1):
    S[f"col_z_{i}"] = gen(f"eq_051_col_z_{i}", col2(t, b), 28, BLACK)
# augmented columns (3-entry, y181..224 = 43pt)
for i, (t, m, b) in enumerate([("1","1","1"),("1","2","1"),("1","1","2"),("1","5","4"),("1","6","5"),("1","6","6")], 1):
    S[f"col_aug_{i}"] = gen(f"eq_051_col_aug_{i}", col3(t, m, b), 43, BLACK)
# Initial W column (3-entry, y59..106 = 47pt, padded to ~25pt width)
S["col_initw"] = gen("eq_051_col_initw", col3("4", "-2", "-2", pad=r"\,"), 47, BLACK)
# green DEC column (3-entry, y147..191 = 44pt)
S["col_green"] = gen("eq_051_col_green", col3("5", "-1", "-1", pad=r"\,"), 44, GREEN)
# blue row vectors (paren band ~14pt)
for i, digits in enumerate(["1\\;\\;0\\;\\;0", "1\\;\\;7\\;\\;6", "1\\;\\;3\\;\\;2"], 1):
    S[f"rowvec_{i}"] = gen(f"eq_051_rowvec_{i}", "(" + digits + ")", 14, BLUE)
# d(Zi) = labels (black)
for i in (1, 2, 3):
    S[f"dzlabel_{i}"] = gen(f"eq_051_dzlabel_{i}", rf"d(Z_{i})\;=\;", 14, BLACK)
# Step eta = 1 (red)
S["step"] = gen("eq_051_step", r"Step\;\eta\;=\;1", 14, RED)

json.dump(S, open(f"{NS}/recreated_pptx/qa/slide051/w051_eq_assets.json", "w"), indent=1)
print("banked manifest -> qa/slide051/w051_eq_assets.json")
