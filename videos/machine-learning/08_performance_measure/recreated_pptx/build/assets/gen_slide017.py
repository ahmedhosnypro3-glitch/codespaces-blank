#!/usr/bin/env python3
"""Generate the F-Score vs Recall chart for slide 17 (F-Score for different Precision and Recall values).

F1 = 2*P*R/(P+R) for P = 0.1..1.0, sampled at recall = 0.0..1.0 step 0.1.
Ten colored series with hollow markers matching the original's palette.
Red dashed annotations + green solid guide lines overlaid per the original.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DPI = 150

recall = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

series = [
    (0.1, "#FF9999", "o"),
    (0.2, "#FFB366", "^"),
    (0.3, "#FFFF99", "v"),
    (0.4, "#99FF99", "<"),
    (0.5, "#99FFFF", ">"),
    (0.6, "#66CCCC", "D"),
    (0.7, "#99CCFF", "s"),
    (0.8, "#FF66FF", "+"),
    (0.9, "#CC99FF", "D"),
    (1.0, "#CC66FF", "x"),
]

fig, ax = plt.subplots(figsize=(6.5, 4.6), dpi=DPI)
fig.patch.set_facecolor("white")

for p, color, marker in series:
    f1 = np.where(recall > 0, 2 * p * recall / (p + recall), 0.0)
    f1[0] = 0.0  # F1=2p*0/(p+0) = 0 by convention in the original
    # hollow markers
    if marker == "+":
        ax.plot(recall, f1, color=color, marker=marker, linewidth=1.2, markersize=4.5, markerfacecolor=color, markeredgecolor=color, markeredgewidth=1.2)
    else:
        ax.plot(recall, f1, color=color, marker=marker, linewidth=1.2, markersize=4.5, markerfacecolor="none", markeredgecolor=color, markeredgewidth=1.2)

ax.set_xlabel("recall", fontsize=11, color="black")
ax.set_ylabel("F1", fontsize=11, color="black", rotation=0, labelpad=18, ha="right")
ax.set_xlim(-0.03, 1.03)
ax.set_ylim(-0.03, 1.03)
ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.tick_params(axis="both", labelsize=9, colors="black")
for spine in ax.spines.values():
    spine.set_color("black")
    spine.set_linewidth(0.8)

# Legend upper-left inside plot
legend_labels = [f"precision = {p}" for p, _, _ in series]
handles, labels = ax.get_legend_handles_labels()
ax.legend([plt.Line2D([], [], color=c, marker=m, linestyle="-", markerfacecolor="none" if m != "+" else c, markeredgecolor=c, markersize=4.5, linewidth=1.2) for _, c, m in series],
          legend_labels,
          loc="upper left", fontsize=8, frameon=True, facecolor="white", edgecolor="gray",
          framealpha=1.0, borderpad=0.4, labelspacing=0.35, handlelength=2.0)

# Red dashed annotations (per original)
ax.plot([0.0, 0.6], [0.65, 0.65], color="#FF0000", linestyle="--", linewidth=1.0)
ax.plot([0.6, 0.6], [0.65, 0.0], color="#FF0000", linestyle="--", linewidth=1.0)
ax.annotate("", xy=(0.0, 0.65), xytext=(0.05, 0.65), arrowprops=dict(arrowstyle="->", color="#FF0000", lw=1.0))
ax.plot([0.0, 0.98], [0.47, 0.47], color="#FF0000", linestyle="--", linewidth=1.0)
ax.plot([0.98, 0.98], [0.47, 0.0], color="#FF0000", linestyle="--", linewidth=1.0)
ax.annotate("", xy=(0.0, 0.47), xytext=(0.05, 0.47), arrowprops=dict(arrowstyle="->", color="#FF0000", lw=1.0))
ax.plot([0.0, 1.0], [0.18, 0.18], color="#FF0000", linestyle="-", linewidth=0.8)

# Green solid guide lines (per original)
ax.plot([0.0, 0.6], [0.60, 0.60], color="#00CC00", linewidth=1.0)
ax.plot([0.13, 0.13], [0.21, 0.0], color="#00CC00", linewidth=1.0)
ax.plot([0.0, 0.89], [0.21, 0.21], color="#00CC00", linewidth=1.0)
ax.plot([0.89, 0.89], [0.21, 0.0], color="#00CC00", linewidth=1.0)

# Small black '+' marker near (recall 0.28, F1 0.50)
ax.plot(0.28, 0.50, marker="+", color="black", markersize=8, markeredgewidth=1.5)

ax.margins(0.02)
plt.tight_layout(pad=1.0)

out = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/slide017_f1chart.png"
plt.savefig(out, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.15)
print(f"saved {out}")

# Also print the size for the build script
from PIL import Image
im = Image.open(out)
print(f"w_px={im.size[0]} h_px={im.size[1]}")
im600 = Image.open(out)
im600.save(out.replace(".png", "_600.png"), dpi=(600, 600)) if False else None
