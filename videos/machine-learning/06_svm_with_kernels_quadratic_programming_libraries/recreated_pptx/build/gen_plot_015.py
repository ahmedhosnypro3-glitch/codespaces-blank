#!/usr/bin/env python3
# Slide 015 plot region, regenerated from pixel measurements of the original
# frame (qa/rejudge2/orig_png/slide_015.png, 960x540). Normalized coords
# [x,y] with y down; region maps to the figure exactly.
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

NS = os.path.dirname(os.path.abspath(__file__))  # build/
OUT = os.path.join(NS, "eq_015", "plot_015.png")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

RX0, RY0, RX1, RY1 = 0.111, 0.497, 0.857, 0.915
RW_IN = (RX1 - RX0) * 13.33
RH_IN = (RY1 - RY0) * 7.5

def u(X):
    return (np.asarray(X, float) - RX0) / (RX1 - RX0)

def v(Y):
    return (RY1 - np.asarray(Y, float)) / (RY1 - RY0)

DPI = 200
fig = plt.figure(figsize=(RW_IN, RH_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Orange U-shaped non-linear boundary: measured samples, smooth spline.
cx = [0.242, 0.26, 0.30, 0.34, 0.38, 0.42, 0.46, 0.48, 0.50, 0.54, 0.58, 0.61, 0.631]
cy = [0.511, 0.567, 0.679, 0.767, 0.832, 0.881, 0.904, 0.905, 0.900, 0.866, 0.794, 0.711, 0.645]
xs = np.linspace(cx[0], cx[-1], 300)
ys = make_interp_spline(cx, cy, k=3)(xs)
ax.plot(u(xs), v(ys), color="#FF8C00", lw=2.5, solid_capstyle="round", zorder=2)

# Blue near-vertical linear boundary, measured tilt: (0.408,0.517)->(0.362,0.915)
ax.plot([u(0.408), u(0.362)], [v(0.517), v(0.915)], color="#0000FF", lw=2.5,
        solid_capstyle="round", zorder=3)

# Red x-axis at measured y=0.828, x 0.111 -> 0.845 with right arrowhead
ax.annotate("", xy=(u(0.845), v(0.828)), xytext=(u(0.111), v(0.828)),
            arrowprops=dict(arrowstyle="-|>", color="#FF0000", lw=1.5,
                            mutation_scale=18, shrinkA=0, shrinkB=0), zorder=1)

# 12 markers on the axis, measured centers, y=0.826, r ~ 5.5 px of 960
cyan_x = [0.2964, 0.3277, 0.3593, 0.5858, 0.6235, 0.6580]
red_x = [0.3857, 0.4163, 0.4478, 0.4916, 0.5240, 0.5549]
r_pt = (5.5 / 960.0) * RW_IN * 72.0
ax.scatter(u(cyan_x), [v(0.826)] * 6, s=np.pi * r_pt ** 2, facecolor="#00FFFF",
           edgecolor="#00BFBF", linewidth=1.0, zorder=4)
ax.scatter(u(red_x), [v(0.826)] * 6, s=np.pi * r_pt ** 2, facecolor="#FF0000",
           edgecolor="#CC0000", linewidth=1.0, zorder=4)

# Red italic serif "x" label at measured (0.847, 0.851)
ax.text(u(0.847), v(0.851), "x", color="#FF0000", fontsize=13, style="italic",
        family="serif", ha="center", va="center", zorder=4)

fig.savefig(OUT, dpi=DPI, transparent=True)
plt.close(fig)
from PIL import Image
im = Image.open(OUT)
print("wrote", OUT, im.size, "expect", (round(RW_IN * DPI), round(RH_IN * DPI)))
