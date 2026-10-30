#!/usr/bin/env python3
"""Generate the function plot for slide 034: f(x) = (x^2 cos(x) - x)/10."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

# Function
def f(x):
    return (x**2 * np.cos(x) - x) / 10

# X range for the plot (matching original frame: -10 to 10)
x = np.linspace(-10, 10, 2000)
y = f(x)

# Figure size at 600 dpi to match equation rendering
# The build script expects: 1975 x 2116 px at 600 dpi = 237 x 253.92 pt
# The plot box is at x607..845 (238 pt wide), y60..312 (252 pt tall)
DPI = 600
W_IN = 1975 / DPI  # 3.29167 in
H_IN = 2116 / DPI  # 3.52667 in

fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_alpha(0.0)  # transparent background

# Plot the function (blue curve)
ax.plot(x, y, color="#0000FF", linewidth=1.5, zorder=1)

# Red markers on the curve (count [?] - let's add a few visible ones)
# From the frame analysis: red circular markers on the curve
# One marked local maximum area and the reached global minimum
marker_xs = [-6.5, -3.5, 0.5, 4.5, 7.8, 9.0]
marker_ys = [f(xi) for xi in marker_xs]
ax.scatter(marker_xs, marker_ys, color="#FF0000", s=40, zorder=3, edgecolors="none")

# Axes setup
ax.set_xlim(-10, 10)
ax.set_ylim(-12, 8)
ax.set_xlabel("x", fontsize=12, color="#000000")
ax.set_ylabel("y", fontsize=12, color="#000000")
ax.tick_params(axis="both", labelsize=10, colors="#000000")

# Grid
ax.grid(True, alpha=0.3, color="#CCCCCC", linewidth=0.5)

# Dark red border box (will be drawn on top in PPTX)
# No border here - the PPTX layer draws it

# Save
out_path = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
            "03_ridger_regression_gradient_descent/recreated_pptx/build/assets/"
            "slide_034_plot.png")
fig.savefig(out_path, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0)
plt.close(fig)

print(f"Saved plot to {out_path}: {W_IN:.4f}x{H_IN:.4f} in at {DPI} dpi")
print(f"Pixel dimensions: {W_IN*DPI:.0f} x {H_IN*DPI:.0f}")