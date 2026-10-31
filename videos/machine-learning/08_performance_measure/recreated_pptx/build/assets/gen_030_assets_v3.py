import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"

# ROC plot panel: exact 254x306 frame px at panel origin (641,81), PIL-measured from
# unique_slides/slide_030.jpg (local coords, y down; mpl y = 306 - local_y):
#   blue border rect (0,0)-(254,306); pale bg #EAF6F6; grid vlines local x 148,233,
#   hlines local y 112,229 (#BFD9D9)
#   red y-axis x=20 local, from y 283 up to y 6, small arrowhead at top
#   red x-axis y=283 local, from x 20 to x 249, small arrowhead at right
#   open red circles r~5 at local (169,68) [FPR=0.66] and (232,69) [FPR=1.0]
#   small red labels '0.1' at local (120,9), '0.0' at local (241,9), white-boxed
#   rotated red 'TPR' at local (10,169); red 'FPR' at local (135,294)
#   glyph heights ~11px at frame scale -> fontsize = px * 72/300
PW, PH = 254, 306
DPI = 300
PT = 72.0 / DPI  # points per frame px

fig = plt.figure(figsize=(PW / DPI, PH / DPI), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW); ax.set_ylim(0, PH)
ax.axis("off")
ax.set_facecolor("#EAF6F6")
fig.patch.set_facecolor("#EAF6F6")
for s in ax.spines.values():
    s.set_visible(True); s.set_color("#0000FF"); s.set_linewidth(2 * PT)
GRID = "#BFD9D9"
for gx in [148, 233]:
    ax.plot([gx, gx], [0, PH], color=GRID, lw=0.8 * PT, zorder=1)
for gy in [112, 229]:
    ax.plot([0, PW], [PH - gy, PH - gy], color=GRID, lw=0.8 * PT, zorder=1)
# red arrow axes (local y down -> mpl y up)
ax.annotate("", xy=(249, PH - 283), xytext=(20, PH - 283),
            arrowprops=dict(arrowstyle="-|>", color="#FF0000", lw=1.5 * PT,
                            mutation_scale=5), zorder=3)
ax.annotate("", xy=(20, PH - 6), xytext=(20, PH - 283),
            arrowprops=dict(arrowstyle="-|>", color="#FF0000", lw=1.5 * PT,
                            mutation_scale=5), zorder=3)
# two open red circles at measured positions
for cx, cy in [(169, 68), (232, 69)]:
    ax.add_patch(Circle((cx, PH - cy), 5, fill=True, facecolor="#EAF6F6",
                        edgecolor="#FF0000", lw=1.4 * PT, zorder=4))
# small white-boxed threshold labels above the circles
for lx, lbl in [(120, "0.1"), (241, "0.0")]:
    ax.text(lx, PH - 9, lbl, color="#FF0000", fontsize=11 * PT, ha="center",
            va="center", zorder=5,
            bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
ax.text(10, PH - 169, "TPR", color="#FF0000", fontsize=11 * PT, rotation=90,
        ha="center", va="center", zorder=5)
ax.text(135, PH - 294, "FPR", color="#FF0000", fontsize=11 * PT,
        ha="center", va="center", zorder=5)
fig.savefig(f"{OUT}/roc_030_v3.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)

from PIL import Image
im = Image.open(f"{OUT}/roc_030_v3.png")
print("roc_030_v3.png", im.size, "w_in=%.5f h_in=%.5f" % (im.size[0] / DPI, im.size[1] / DPI))
