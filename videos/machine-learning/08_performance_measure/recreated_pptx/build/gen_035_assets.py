#!/usr/bin/env python3
"""Slide 35 asset generation: ROC right panel (matplotlib, 600dpi, 1px=1pt) + 2D
equation PNGs (via scripts/render_eq.py mathtext contract). Writes manifest JSON.

Frame-measured geometry (960x540 original, 1px = 1pt = 1/72 in):
  right section box x[637,904] y[42,399] (ROC), bottom-right box x[634,903] y[399,527].
  ROC plot frame x[660,890] y[84,352]; data mapping X(fpr)=660+216*fpr, Y(tpr)=352-201*tpr
  (gridlines measured at x=746,789,833,875 / y=151,194,233,272,311 -> 0.2 steps, 0@x660/y352).
"""
import json, os, subprocess, sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
REPO = "/home/codespace/ai_llm_slides"
PY = "/home/codespace/.pyenv/versions/3.15.2/bin/python3"
ASSETS = os.path.join(NS, "recreated_pptx/build/assets")
os.makedirs(ASSETS, exist_ok=True)

manifest = {}

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------- ROC right panel ----------------
# image box: x[637,904] y[42,399] -> 267 x 357 px
X0, Y0 = 637, 42          # top-left of image box (frame coords)
PW, PH = 267, 357         # px
DPI = 600
fig = plt.figure(figsize=(PW / 72.0, PH / 72.0), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW)
ax.set_ylim(0, PH)        # y-up rel: ry = (399 - py) - 42 = 357 - (py - 42)
ax.axis("off")
fig.patch.set_facecolor("white")

def rx(px): return px - X0
def ry(py): return (Y0 + PH) - py   # 399 - py

DRED = "#8B0000"
# outer section border
ax.add_patch(plt.Rectangle((rx(637), ry(399)), rx(904) - rx(637), ry(42) - ry(399),
                           facecolor="none", edgecolor=DRED, lw=1.5))

# plot frame x[660,890] y[84,352], light fill
PX0, PX1, PY0, PY1 = rx(660), rx(890), ry(352), ry(84)
ax.add_patch(plt.Rectangle((PX0, PY0), PX1 - PX0, PY1 - PY0, facecolor="#DAECF0",
                           edgecolor=DRED, lw=1.2))

def X(fpr): return rx(660 + 216.0 * fpr)
def Y(tpr): return ry(352 - 201.0 * tpr)

# grid at 0.2 steps
for v in [0.2, 0.4, 0.6, 0.8]:
    ax.plot([X(v), X(v)], [Y(0), Y(1)], color="#B9C4CC", lw=0.6, zorder=1)
    ax.plot([X(0), X(1)], [Y(v), Y(v)], color="#B9C4CC", lw=0.6, zorder=1)
ax.set_axisbelow(True)

# dashed diagonal (0,0)-(1,1)
ax.plot([X(0), X(1)], [Y(0), Y(1)], ls=(0, (5, 4)), color="#888888", lw=1.0, zorder=2)

# ROC points: threshold -> (fpr, tpr) from the 7 confusion matrices
pts = [("0.0", 1.0, 1.0), ("0.1", 0.66, 1.0), ("0.3", 0.33, 1.0), ("0.4", 0.16, 1.0),
       ("0.6", 0.16, 0.6), ("0.7", 0.0, 0.6), ("1.0", 0.0, 0.0)]
xs = [X(p[1]) for p in pts]
ys = [Y(p[2]) for p in pts]
ax.plot(xs, ys, color=DRED, lw=1.4, zorder=3)
for _, fpr, tpr in pts:
    ax.plot([X(fpr)], [Y(tpr)], marker="o", ms=8, mfc="#FF0000", mec="#FF0000", zorder=4)

# threshold labels near points (measured black comps in the frame)
lbl_off = {"0.0": (-14, 10), "0.1": (-2, 10), "0.3": (-10, 10), "0.4": (20, -58),
           "0.6": (20, 16), "0.7": (4, -22), "1.0": (26, 12)}
for lab, fpr, tpr in pts:
    dx, dy = lbl_off[lab]
    ax.text(X(fpr) + dx, Y(tpr) + dy, lab, ha="center", va="center", fontsize=7.5,
            color="black", zorder=5,
            bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none", alpha=0.85))

# "Best (FPR)" annotation, gutter left of plot near y~155 (frame px)
ax.text(rx(650), ry(162), "Best", ha="left", va="center", fontsize=9,
        fontweight="bold", color=DRED, zorder=5)
ax.text(rx(650), ry(174), "(FPR)", ha="left", va="center", fontsize=9,
        fontweight="bold", color=DRED, zorder=5)

# axis titles (maroon): TPR rotated at left, FPR below
ax.text(rx(648), ry(250), "TPR", rotation=90, ha="center", va="center",
        fontsize=11, fontweight="bold", color=DRED)
ax.text(rx(775), ry(372), "FPR", ha="center", va="center",
        fontsize=11, fontweight="bold", color=DRED)

roc_path = os.path.join(ASSETS, "slide035_roc_panel.png")
fig.savefig(roc_path, dpi=DPI, facecolor="white")
plt.close(fig)
from PIL import Image
with Image.open(roc_path) as im:
    w_px, h_px = im.size
manifest["roc_panel"] = {"path": roc_path, "w_in": w_px / 600.0, "h_in": h_px / 600.0,
                         "w_px": w_px, "h_px": h_px, "x_px": X0, "y_px": Y0}

# ---------------- equations (2D mathtext via render_eq.py) ----------------
def render_eq(name, latex, pt, color="000000"):
    out = os.path.join(ASSETS, name + ".png")
    r = subprocess.run([PY, os.path.join(REPO, "scripts/render_eq.py"), latex, out,
                        str(pt), color], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        sys.exit(1)
    meta = json.loads(r.stdout.strip().splitlines()[-1])
    manifest[name] = {"path": out, "w_in": meta["w_in"], "h_in": meta["h_in"],
                      "w_px": meta["w_px"], "h_px": meta["h_px"]}

BLUE = "#00008B"
# per-panel TPR/FPR computation lines (frame values; linear in original -> 2D upgrade)
comp = {
    "L1": ("5", "5+0", "1",   "6", "6+0", "1"),
    "L2": ("5", "5+0", "1",   "4", "4+2", "0.66"),
    "L3": ("5", "5+0", "1",   "2", "2+4", "0.33"),
    "L4": ("4", "4+1", "\\frac{4}{5}", "1", "1+5", "0.16"),
    "M1": ("3", "3+1", "0.6", "1", "1+5", "0.16"),
    "M2": ("3", "3+2", "0.6", "0", "0+6", "0"),
    "M3": ("0", "0+5", "0",   "0", "0+6", "0"),
}
for k, (tp, tpfn, tv, fp, fptn, fv) in comp.items():
    render_eq(f"eq_{k}_tpr", rf"\mathrm{{TPR}}=\frac{{{tp}}}{{{tpfn}}}={tv}", 12, BLUE)
    render_eq(f"eq_{k}_fpr", rf"\mathrm{{FPR}}=\frac{{{fp}}}{{{fptn}}}={fv}", 12, BLUE)

render_eq("eq_def_tpr", r"\mathrm{TPR}=\frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}", 16, "#800000")
render_eq("eq_def_fpr", r"\mathrm{FPR}=\frac{\mathrm{FP}}{\mathrm{FP}+\mathrm{TN}}", 16, "#800000")

mpath = os.path.join(ASSETS, "slide035_manifest.json")
with open(mpath, "w") as f:
    json.dump(manifest, f, indent=1)
print("wrote", mpath)
for k, v in manifest.items():
    print(k, f"{v['w_in']:.3f}x{v['h_in']:.3f}in")
