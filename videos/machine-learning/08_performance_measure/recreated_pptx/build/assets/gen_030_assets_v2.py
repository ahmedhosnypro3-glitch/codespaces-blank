import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"

# ---- ROC plot panel: exact 254x306 frame px at panel origin (641,81) ----
# PIL-measured from unique_slides/slide_030.jpg:
#   plot bg x[645,892] y[83,384], blue border x[643,895] y[80,388]
#   grid vert abs x = 660,703,745,788,832,876  (local 19,62,104,147,191,235)
#   grid horiz abs y = 347,309,270,232,193,151 (local 40,78,117,155,194,236; local y up)
#   red y-axis arrow x=660 from y=347 up; red x-axis arrow y=347 from x=660 right
#   circles abs (811,149) label 0.1, (875,149) label 0.0 -> local (170,238),(234,238)
PW, PH = 254, 306
DPI = 300
fig = plt.figure(figsize=(PW / DPI, PH / DPI), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW); ax.set_ylim(0, PH)
ax.axis("off")
ax.set_facecolor("#EAF6F6")
fig.patch.set_facecolor("#EAF6F6")
for s in ax.spines.values():
    s.set_visible(True); s.set_color("#0000FF"); s.set_linewidth(1.2)
GRID = "#BFD9D9"
for gx in [19, 62, 104, 147, 191, 235]:
    ax.plot([gx, gx], [40, 248], color=GRID, lw=0.8, zorder=1)
for gy in [40, 78, 117, 155, 194, 236]:
    ax.plot([19, 235], [gy, gy], color=GRID, lw=0.8, zorder=1)
# red connecting line between the two operating points (vision read: "a red line connects them")
ax.plot([170, 234], [238, 238], color="#FF0000", lw=1.4, zorder=3)
# red arrow axes: x-axis local y=40 x 19->249 ; y-axis local x=19 y 40->298
ax.annotate("", xy=(249, 40), xytext=(19, 40),
            arrowprops=dict(arrowstyle="-|>", color="#FF0000", lw=1.6), zorder=3)
ax.annotate("", xy=(19, 298), xytext=(19, 40),
            arrowprops=dict(arrowstyle="-|>", color="#FF0000", lw=1.6), zorder=3)
# two open red circles near the top: label 0.1 at FPR=0.66, label 0.0 at FPR=1.0, TPR=1
for cx, lbl, lx in [(170, "0.1", 170), (234, "0.0", 226)]:
    ax.add_patch(Circle((cx, 238), 4.2, fill=False, edgecolor="#FF0000", lw=1.6, zorder=4))
    ax.text(lx, 258, lbl, color="#000000", fontsize=7.5, ha="center", va="center", zorder=4)
ax.text(10, 141, "TPR", color="#FF0000", fontsize=8, rotation=90, ha="center", va="center", zorder=4)
ax.text(138, 23, "FPR", color="#FF0000", fontsize=8, ha="center", va="center", zorder=4)
fig.savefig(f"{OUT}/roc_030_v2.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)

# ---- definition fraction equations (drift items), 600 dpi transparent ----
# Source of truth pool_run/image_analysis/slide_030_analysis.txt: TPR def red #C00000,
# FPR def blue #1F497D, 9pt at (660,410)/(660,450).
EQDPI = 600
for name, tex, col in [
    ("eq_030_v2_tpr", r"$\mathrm{TPR}\ =\ \dfrac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}$", "#C00000"),
    ("eq_030_v2_fpr", r"$\mathrm{FPR}\ =\ \dfrac{\mathrm{FP}}{\mathrm{FP}+\mathrm{TN}}$", "#1F497D"),
]:
    fig = plt.figure(dpi=EQDPI)
    fig.text(0, 0, tex, fontsize=11, color=col, va="baseline", ha="left")
    fig.savefig(f"{OUT}/{name}.png", dpi=EQDPI, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

from PIL import Image
for f, dpi in [("roc_030_v2.png", DPI), ("eq_030_v2_tpr.png", EQDPI), ("eq_030_v2_fpr.png", EQDPI)]:
    im = Image.open(f"{OUT}/{f}")
    print(f, im.size, "w_in=%.5f h_in=%.5f" % (im.size[0] / dpi, im.size[1] / dpi))
