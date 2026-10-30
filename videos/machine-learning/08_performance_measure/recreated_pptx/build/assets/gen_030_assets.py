import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"

# ---- ROC plot panel: exact 254x306 px (frame px 641..895, 81..387) ----
PW, PH = 254, 306
DPI = 300
fig = plt.figure(figsize=(PW / DPI, PH / DPI), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW); ax.set_ylim(0, PH)
ax.axis("off")
ax.set_facecolor("#EAF6F6")
fig.patch.set_facecolor("#EAF6F6")
# blue border
for s in ax.spines.values():
    s.set_visible(True); s.set_color("#0000FF"); s.set_linewidth(1.2)
# gridlines (panel px coords measured): vlines x=62,104,147,191 ; hlines y=40,78,117,155,194,236
GRID = "#BFD9D9"
for gx in [19, 62, 104, 147, 191, 235]:
    ax.plot([gx, gx], [40, 248], color=GRID, lw=0.8, zorder=1)
for gy in [40, 78, 117, 155, 194, 236]:
    ax.plot([19, 235], [gy, gy], color=GRID, lw=0.8, zorder=1)
# red arrow axes: x-axis y=40 from x=19 to 249; y-axis x=19 from y=40 to 298
ax.annotate("", xy=(249, 40), xytext=(19, 40),
            arrowprops=dict(arrowstyle="-|>", color="#FF0000", lw=1.6), zorder=3)
ax.annotate("", xy=(19, 298), xytext=(19, 40),
            arrowprops=dict(arrowstyle="-|>", color="#FF0000", lw=1.6), zorder=3)
# two open red circles: (0.1) at data FPR=0.66 -> x=19+0.66*216=161.6 ; (0.0) at FPR=1.0 -> x=235 ; TPR=1 -> y=236
for cx, lbl, lx in [(162, "0.1", 168), (235, "0.0", 222)]:
    ax.add_patch(Circle((cx, 238), 4.2, fill=False, edgecolor="#FF0000", lw=1.6, zorder=4))
    ax.text(lx, 258, lbl, color="#000000", fontsize=7.5, ha="center", va="center", zorder=4)
# axis labels: TPR vertical at left (x=10, y=141), FPR below (x=138, y=23)
ax.text(10, 141, "TPR", color="#FF0000", fontsize=8, rotation=90, ha="center", va="center", zorder=4)
ax.text(138, 23, "FPR", color="#FF0000", fontsize=8, ha="center", va="center", zorder=4)
fig.savefig(f"{OUT}/roc_030.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)

# ---- fraction equations (drift items), 600 dpi transparent ----
EQDPI = 600
for name, tex in [
    ("eq_030_tpr", r"$\mathrm{TPR}\ =\ \dfrac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}$"),
    ("eq_030_fpr", r"$\mathrm{FPR}\ =\ \dfrac{\mathrm{FP}}{\mathrm{FP}+\mathrm{TN}}$"),
]:
    fig = plt.figure(dpi=EQDPI)
    fig.text(0, 0, tex, fontsize=11, color="#000000", va="baseline", ha="left")
    fig.savefig(f"{OUT}/{name}.png", dpi=EQDPI, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

from PIL import Image
for f in ["roc_030.png", "eq_030_tpr.png", "eq_030_fpr.png"]:
    im = Image.open(f"{OUT}/{f}")
    print(f, im.size, "w_in=%.5f h_in=%.5f" % (im.size[0] / (DPI if f.startswith("roc") else EQDPI), im.size[1] / (DPI if f.startswith("roc") else EQDPI)))
