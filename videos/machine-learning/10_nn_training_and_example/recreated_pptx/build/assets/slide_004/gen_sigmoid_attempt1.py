#!/usr/bin/env python3
"""Slide 4 attempt-1 sigmoid graph: red curve + visible tick labels.

Differs from assets/slide_004/gen_sigmoid.py in two evidence-backed ways:
  - curve colour: original's upper-right quadrant carries saturated RED ink
    (judge: "original red curve; recreation blue curve" — MINOR); the panel
    border stays blue in both.
  - tick labels: the certified spec lists axis labels -6..6 and 0.0..1.0, but
    the original generator blanked them (judge: "without axis numbers" — MINOR).
Writes a NEW asset file; the banked sigmoid_graph.png is left untouched.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = ("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
       "recreated_pptx/build/assets/slide_004/sigmoid_graph_attempt1.png")

REGION_PX = (700, 80, 920, 300)
BG = "#FFFFFF"
LINE_COLOR = "#FF0000"
GRID_COLOR = "#CCCCCC"
AXIS_COLOR = "#000000"
BORDER_COLOR = "#0000FF"
BORDER_WIDTH = 2

x = np.linspace(-6, 6, 400)
y = 1 / (1 + np.exp(-x))

w = REGION_PX[2] - REGION_PX[0]
h = REGION_PX[3] - REGION_PX[1]
fig = plt.figure(figsize=(w / 72, h / 72), dpi=72)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)
ax.plot(x, y, color=LINE_COLOR, linewidth=2)
ax.grid(True, color=GRID_COLOR, linewidth=0.5, linestyle="-")
ax.axhline(y=0, color=AXIS_COLOR, linewidth=0.8)
ax.axvline(x=0, color=AXIS_COLOR, linewidth=0.8)
ax.axhline(y=1, color=AXIS_COLOR, linewidth=0.8, linestyle="--")
ax.set_xticks(np.arange(-6, 7, 2))
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.tick_params(colors=AXIS_COLOR, labelsize=8)
ax.set_xlim(-6, 6)
ax.set_ylim(-0.1, 1.1)
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color(BORDER_COLOR)
    spine.set_linewidth(BORDER_WIDTH)

fig.savefig(OUT, dpi=72, facecolor=BG)
print(f"wrote {OUT}  region={w}x{h}px  curve={LINE_COLOR}  tick_labels=on")
