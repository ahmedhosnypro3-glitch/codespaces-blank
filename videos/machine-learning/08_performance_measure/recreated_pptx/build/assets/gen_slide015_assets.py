"""Generate slide_015 assets: y=1/x graph panel + stacked-fraction equation PNGs.

Graph geometry measured from unique_slides/slide_015.jpg (960x540 frame, 1px = 1pt):
  red-bordered panel x 660..859, y 96..274  (199 x 178 px)
  y-axis x=746.5, x-axis y=193, isotropic scale 15.2 px per data unit
  yellow highlight ellipse px x 740..775 / y 92..221 ; green y=1/x curve in QI+QIII
"""
import json
import os
import subprocess
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_GRAPH = os.path.join(HERE, "eq_015_graph.png")
OUT_MANIFEST = os.path.join(HERE, "eq_015_manifest.json")
ROOT = "/home/codespace/ai_llm_slides"

PANEL_W_PX, PANEL_H_PX = 199.0, 178.0   # measured panel size
PXS_PER_UNIT = 15.2                      # measured isotropic scale

XLIM = (-5.7, 7.4)                       # x=0 at 0.4347 of panel width (measured 746.5)
YLIM = (-5.3, 6.4)                       # y=0 at 0.5449 of panel height (measured 193)

fig = plt.figure(figsize=(PANEL_W_PX / 72, PANEL_H_PX / 72), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("white")
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis="both", direction="in", length=2, labelsize=5,
               colors="black", pad=1)

# graph-paper gridlines (integer ticks), light gray
ax.set_xticks(range(-5, 6))
ax.set_yticks(range(-5, 6))
ax.grid(True, color="#D3D3D3", linewidth=0.7, linestyle="-")

# axes: gray lines through y=0 / x=0
ax.axhline(0, color="#A9A9A9", linewidth=0.9)
ax.axvline(0, color="#A9A9A9", linewidth=0.9)

# y = 1/x hyperbola (quadrants I and III)
import numpy as np
xs = np.linspace(-6.8, 8.6, 1201)
ys = 1.0 / xs
ax.plot(xs, ys, color="#00A000", linewidth=1.3, solid_capstyle="round")

# yellow translucent highlight over the steep QI branch
ell = Ellipse((0.72, 2.4), width=2.30, height=8.50, facecolor="#FFFF00",
              alpha=0.45, edgecolor="none", zorder=3)
ax.add_patch(ell)

# small red square marker near (-1, 0)
ax.plot([-1], [0], marker="s", markersize=4.5, color="#FF0000",
        markerfacecolor="none", markeredgewidth=1.1, zorder=5)

# caption "y = 1/x" as a stacked fraction
ax.text(-0.45, 3.9, r"$y = \frac{1}{x}$", fontsize=12, color="black",
        ha="left", va="baseline", zorder=6)

# axis labels at the arrow ends
ax.text(7.25, -0.55, "x", fontsize=9, color="black", ha="left", va="center")
ax.text(0.45, 5.55, "y", fontsize=9, color="black", ha="left", va="top")

# red panel border (measured on the original frame)
ax.add_patch(plt.Rectangle((XLIM[0], YLIM[0]), XLIM[1] - XLIM[0],
                           YLIM[1] - YLIM[0], fill=False, edgecolor="#C00000",
                           linewidth=1.6, clip_on=False, zorder=10))

fig.savefig(OUT_GRAPH, dpi=600, facecolor="white")
plt.close(fig)


def render_eq(latex, out_png, fontsize, color):
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts/render_eq.py"), latex,
         out_png, str(fontsize), "#" + color],
        capture_output=True, text=True, check=True)
    for line in proc.stdout.splitlines():
        if line.strip().startswith("{"):
            return json.loads(line)
    raise RuntimeError("no json from render_eq for " + latex)


EQS = [
    ("frac1_prec", r"\frac{1}{Precision}", 26, "FF0000"),
    ("frac1_rec", r"\frac{1}{Recall}", 26, "FF0000"),
    ("paren_prec", r"\left(\frac{1}{Precision}\right)", 26, "FF0000"),
    ("paren_rec", r"\left(\frac{1}{Recall}\right)", 26, "FF0000"),
    ("paren_sum", r"\left(\frac{1}{Precision} + \frac{1}{Recall}\right)", 22, "FF0000"),
    ("frac1_f1", r"\frac{1}{F1}", 26, "0000FF"),
    ("frac1_f1_sm", r"\frac{1}{F1}", 22, "0000FF"),
]


def ink_box(png):
    from PIL import Image
    import numpy as np
    a = np.array(Image.open(png).convert("RGBA"))
    ink = a[:, :, 3] > 8
    rows = np.nonzero(ink.any(axis=1))[0]
    cols = np.nonzero(ink.any(axis=0))[0]
    h, w = ink.shape
    return {
        "ink_top_frac": float(rows.min()) / h,
        "ink_left_frac": float(cols.min()) / w,
        "ink_h_frac": float(rows.max() - rows.min() + 1) / h,
        "ink_w_frac": float(cols.max() - cols.min() + 1) / w,
    }


manifest = {}
for name, latex, size, color in EQS:
    png = os.path.join(HERE, "eq_015_%s.png" % name)
    meta = render_eq(latex, png, size, color)
    meta.update(ink_box(png))
    manifest[name] = meta

with open(OUT_MANIFEST, "w") as fh:
    json.dump(manifest, fh, indent=1)
print("OK", OUT_GRAPH, len(os.listdir(HERE)), "assets")
