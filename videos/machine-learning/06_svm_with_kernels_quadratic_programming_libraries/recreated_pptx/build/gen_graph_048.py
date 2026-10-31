import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
pts = json.load(open(BASE + "/eq_048/points_raw.json"))

# Original 960x540 frame; plot panel measured at x 207..757, y 64..501 (y down).
PX0, PY0, PX1, PY1 = 207, 64, 757, 501
PW, PH = PX1 - PX0, PY1 - PY0   # 550 x 437

fig_w, fig_h = PW / 100.0, PH / 100.0   # 5.5 x 4.37 in @100dpi -> 550x437 px
fig = plt.figure(figsize=(fig_w, fig_h), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW)
ax.set_ylim(0, PH)
ax.axis("off")
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

colors = {"red": "#FF0000", "blue": "#0000FF", "black": "#000000"}
for name in ("red", "blue", "black"):
    xy = pts[name]
    xs = [p[0] - PX0 for p in xy]
    ys = [PY1 - p[1] for p in xy]   # flip y
    ax.scatter(xs, ys, s=12, c=colors[name], marker="o", edgecolors="none", linewidths=0)

# red border matching the original panel frame (~2.5 px at 960-scale -> 0.025 fig-frac)
import matplotlib.patches as mpatches
ax.add_patch(mpatches.Rectangle((0, 0), PW, PH, fill=False, edgecolor="#FF0000", linewidth=3.5, zorder=10))

out = BASE + "/slide_048_graph.png"
fig.savefig(out, dpi=200, facecolor="white", pad_inches=0)
print("wrote", out)
