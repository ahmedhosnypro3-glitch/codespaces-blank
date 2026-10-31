#!/usr/bin/env python3
"""Slide 34 asset generation v3: ROC right panel only (equations unchanged).
Changes vs v2 (driven by judge_verify_2 FAIL adjudication):
- badge "34" circle removed from the panel (house chrome already draws the
  slide badge; a second badge inside the ROC plot read as an extra content badge)
- point mapping inset from the plot frame so the (1,1) "0.0" marker no longer
  touches the top-right corner of the axes rectangle
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
ASSETS = os.path.join(NS, "recreated_pptx/build/assets")

PW, PH = 246, 342          # right panel size in frame px (origin 645,55)
DPI = 600
fig = plt.figure(figsize=(PW / 72.0, PH / 72.0), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW)
ax.set_ylim(0, PH)
ax.axis("off")
fig.patch.set_facecolor("white")

RED = "#C00000"
ARROW = "#FF0000"
ax.plot([0, 0], [0, PH], color="#888888", lw=1.2)
ax.plot([PW - 1, PW - 1], [0, PH], color="#888888", lw=1.2)

PX0, PX1, PY0, PY1 = 15, 243, 48, 318
ax.add_patch(plt.Rectangle((PX0, PY0), PX1 - PX0, PY1 - PY0, facecolor="#EEFEFB",
                           edgecolor=RED, lw=1.5))

INSET = 9                  # keep markers fully inside the plot rectangle
def X(fpr): return PX0 + INSET + (PX1 - PX0 - 2 * INSET) * fpr
def Y(tpr): return PY0 + INSET + (PY1 - PY0 - 2 * INSET) * tpr

for v in [0.2, 0.4, 0.6, 0.8]:
    ax.plot([X(v), X(v)], [PY0, PY1], color="#DDDDDD", lw=0.5)
    ax.plot([PX0, PX1], [Y(v), Y(v)], color="#DDDDDD", lw=0.5)

pts = [(1.0, 1.0, "0.0"), (0.66, 1.0, "0.1"), (0.33, 1.0, "0.3"),
       (0.0, 0.6, "0.7"), (0.16, 0.8, "0.4"), (0.16, 0.6, "0.6")]
for fpr, tpr, lab in pts:
    ax.plot([X(fpr)], [Y(tpr)], marker="o", ms=9, mfc="white", mec=ARROW, mew=1.6)

lbl_off = {"0.0": (-18, -13), "0.1": (0, -14), "0.3": (0, -14),
           "0.7": (15, -4), "0.4": (0, 11), "0.6": (13, -4)}
for fpr, tpr, lab in pts:
    dx, dy = lbl_off[lab]
    ax.text(X(fpr) + dx, Y(tpr) + dy, lab, ha="center", va="center", fontsize=8,
            color="black", bbox=dict(boxstyle="square,pad=0.15", fc="#FFF8E1", ec="#CCCCCC", lw=0.5))

ax.annotate("", xy=(PX0, PY1 + 7), xytext=(PX0, PY1 - 2),
            arrowprops=dict(arrowstyle="-|>", color=ARROW, lw=1.5, mutation_scale=14))
ax.annotate("", xy=(PX1 + 7, PY0), xytext=(PX1 - 2, PY0),
            arrowprops=dict(arrowstyle="-|>", color=ARROW, lw=1.5, mutation_scale=14))

ax.text(6, (PY0 + PY1) / 2, "TPR", rotation=90, ha="center", va="center",
        fontsize=11, fontweight="bold", color="black")
ax.text((PX0 + PX1) / 2, 30, "FPR", ha="center", va="center",
        fontsize=11, fontweight="bold", color="black")

roc_path = os.path.join(ASSETS, "slide034_roc_panel.png")
fig.savefig(roc_path, dpi=DPI, facecolor="white")
plt.close(fig)
with Image.open(roc_path) as im:
    w_px, h_px = im.size
man_path = os.path.join(ASSETS, "slide034_manifest.json")
man = json.load(open(man_path))
man["roc_panel"] = {"path": roc_path, "w_in": w_px / 600.0, "h_in": h_px / 600.0,
                    "w_px": w_px, "h_px": h_px}
json.dump(man, open(man_path, "w"), indent=1)
print("v3 roc panel:", w_px, h_px)
