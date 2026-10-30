#!/usr/bin/env python3
"""Slide 34 asset generation: ROC right panel (matplotlib, 600dpi, 1px=1pt) + 2D
equation PNGs (via scripts/render_eq.py mathtext contract). Writes manifest JSON."""
import json, os, subprocess, sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
REPO = "/home/codespace/ai_llm_slides"
PY = "/home/codespace/.pyenv/versions/3.15.2/bin/python3"
ASSETS = os.path.join(NS, "recreated_pptx/build/assets")
os.makedirs(ASSETS, exist_ok=True)

manifest = {}

# ---------------- ROC right panel ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# panel origin (645,55) px, size 246x342 px; y-up rel coords: ry = 397 - py
PW, PH = 246, 342
DPI = 600
fig = plt.figure(figsize=(PW / 72.0, PH / 72.0), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW)
ax.set_ylim(0, PH)
ax.axis("off")
fig.patch.set_facecolor("white")

DRED = "#8B0000"
# outer verticals of the right section
ax.plot([0, 0], [0, PH], color=DRED, lw=1.5)
ax.plot([PW - 1, PW - 1], [0, PH], color=DRED, lw=1.5)

# plot frame: px x 660..888, py 79..349 -> rel x 15..243, ry 48..318
PX0, PX1, PY0, PY1 = 15, 243, 48, 318
ax.add_patch(plt.Rectangle((PX0, PY0), PX1 - PX0, PY1 - PY0, facecolor="#EEFEFB",
                           edgecolor=DRED, lw=1.5))

def X(fpr): return PX0 + (PX1 - PX0) * fpr
def Y(tpr): return PY0 + (PY1 - PY0) * tpr

# grid + ticks
for v in [0.2, 0.4, 0.6, 0.8]:
    ax.plot([X(v), X(v)], [PY0, PY1], color="#CCCCCC", lw=0.5)
    ax.plot([PX0, PX1], [Y(v), Y(v)], color="#CCCCCC", lw=0.5)
for v in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    ax.text(X(v), PY0 - 7, f"{v:.1f}", ha="center", va="top", fontsize=7, color="black")
    ax.text(PX0 - 3, Y(v), f"{v:.1f}", ha="right", va="center", fontsize=7, color="black")

# dashed diagonal (0,0)-(1,1)
ax.plot([X(0), X(1)], [Y(0), Y(1)], ls=(0, (5, 4)), color="#999999", lw=1.0)

# data points from the six confusion matrices (validated spec)
pts = [(1.0, 1.0, "0.0"), (0.66, 1.0, "0.1"), (0.33, 1.0, "0.3"),
       (0.0, 0.6, "0.7"), (0.16, 0.8, "0.4"), (0.16, 0.6, "0.6")]
for fpr, tpr, lab in pts:
    ax.plot([X(fpr)], [Y(tpr)], marker="o", ms=9, mfc="#FF0000", mec="#FF0000")

lbl_off = {"0.0": (-4, 8), "0.1": (0, 8), "0.3": (0, 8), "0.7": (9, -3),
           "0.4": (0, 8), "0.6": (9, -10)}
for fpr, tpr, lab in pts:
    dx, dy = lbl_off[lab]
    ax.text(X(fpr) + dx, Y(tpr) + dy, lab, ha="center", va="center", fontsize=8,
            color="black", bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="#CCCCCC", lw=0.5))

ax.text(6, (PY0 + PY1) / 2, "TPR", rotation=90, ha="center", va="center",
        fontsize=11, fontweight="bold", color="black")
ax.text((PX0 + PX1) / 2, 30, "FPR", ha="center", va="center",
        fontsize=11, fontweight="bold", color="black")

# in-plot slide badge (original content): yellow circle at px (861..889, 58..77)
bx, by, br = 875 - 645, 397 - 67.5, 13
ax.add_patch(plt.Circle((bx, by), br, facecolor="#FBFF9E", edgecolor="#FBFF9E"))
ax.text(bx, by, "34", ha="center", va="center", fontsize=13, fontweight="bold", color="black")

roc_path = os.path.join(ASSETS, "slide034_roc_panel.png")
fig.savefig(roc_path, dpi=DPI, facecolor="white")
plt.close(fig)
from PIL import Image
with Image.open(roc_path) as im:
    w_px, h_px = im.size
manifest["roc_panel"] = {"path": roc_path, "w_in": w_px / 600.0, "h_in": h_px / 600.0,
                         "w_px": w_px, "h_px": h_px}

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

render_eq("eq_def_tpr", r"\mathrm{TPR}=\frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}", 16)
render_eq("eq_def_fpr", r"\mathrm{FPR}=\frac{\mathrm{FP}}{\mathrm{FP}+\mathrm{TN}}", 16)

comp = {
    "L1": ("5", "5+0", "1", "6", "6+0", "1"),
    "L2": ("5", "5+0", "1", "4", "4+2", "0.66"),
    "L3": ("5", "5+0", "1", "2", "2+4", "0.33"),
    "L4": ("4", "4+1", "\\frac{4}{5}", "1", "1+5", "0.16"),
    "M1": ("3", "3+1", "0.6", "1", "1+5", "0.16"),
    "M2": ("3", "3+2", "0.6", "0", "0+6", "0"),
}
for k, (tp, tpfn, tv, fp, fptn, fv) in comp.items():
    render_eq(f"eq_{k}_tpr", rf"\mathrm{{TPR}}=\frac{{{tp}}}{{{tpfn}}}={tv}", 12)
    render_eq(f"eq_{k}_fpr", rf"\mathrm{{FPR}}=\frac{{{fp}}}{{{fptn}}}={fv}", 12)

mpath = os.path.join(ASSETS, "slide034_manifest.json")
with open(mpath, "w") as f:
    json.dump(manifest, f, indent=1)
print("wrote", mpath)
for k, v in manifest.items():
    print(k, f"{v['w_in']:.3f}x{v['h_in']:.3f}in")
