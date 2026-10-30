#!/usr/bin/env python3
"""Extract the curve centerline from the original frame and regenerate plot exactly."""
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
im = np.asarray(Image.open(ROOT + "/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
X0, X1, Y0, Y1 = 608, 847, 60, 312
box = im[Y0:Y1, X0:X1]
r, g, b = box[:, :, 0], box[:, :, 1], box[:, :, 2]

# cyan curve mask
cyan = (b - r > 55) & (g - r > 30) & (b > 140)

# per-frame-x, median curve y
curve_pts = []
for fx in range(X1 - X0):  # 0..239
    col = np.where(cyan[:, fx])[0]
    if len(col) >= 3:
        cy = np.median(col)
        curve_pts.append((fx, cy))
curve_pts = np.array(curve_pts)
print("curve points:", len(curve_pts), "x range", curve_pts[:,0].min(), "..", curve_pts[:,0].max())

# Now we have curve in frame coords. Let's convert to function domain.
# The x-axis is at frame y=172 (dark horizontal line found earlier).
# The y-axis is at frame x=724-608=116 (inside box, left of center).
x_axis_fy = 172 - Y0  # 112 in box coords
y_axis_fx = 724 - X0  # 116 in box coords

# Frame-to-domain scale
# From earlier: x-domain [-12,12] mapped to ~212px => ~8.83 px/unit
# Let's compute from the y-axis position: if y-axis (x=0) is at fx=116,
# and left edge (fx=0) is x=-12, right edge (fx=239) is x=12.
# x_domain = (fx - 116) * (24/239) = (fx - 116) * 0.1004
# y_domain = (fy - 112) * (-1) * scale_y

# Scale y: f=11 at fy=80 (box: 20), f=0 at fy=112, f=-11 at fy=254 (box: 194)
# scale_down = (112-20)/11 = 92/11 = 8.36 ; scale_up = (194-112)/11 = 82/11 = 7.45
# Use symmetric scale? (194-20)/22 = 174/22 = 7.91
# But let's see: the curve goes to ~fy=20 (f≈11) and ~fy=194 (f≈-11)

# Compute domain coords for each curve point
pts_dom = []
for fx, fy in curve_pts:
    xd = (fx - y_axis_fx) * (24 / (X1 - X0))  # 24 units over 239 px
    yd = (x_axis_fy - fy) / 7.91  # upward positive
    pts_dom.append((xd, yd))
pts_dom = np.array(pts_dom)

# Save the extracted curve
np.savez("/tmp/curve_034_extracted.npz", 
         frame_pts=curve_pts, domain_pts=pts_dom,
         x_axis_fy=x_axis_fy, y_axis_fx=y_axis_fx,
         x0=X0, y0=Y0, x1=X1, y1=Y1)

print("domain x range:", pts_dom[:,0].min(), "..", pts_dom[:,0].max())
print("domain y range:", pts_dom[:,1].min(), "..", pts_dom[:,1].max())
print("y-axis at fx:", y_axis_fx, "x-axis at fy:", x_axis_fy)

# Now regenerate with matplotlib using SAME coordinate system
# Plot box in PPTX: x607..845 (238pt = 238*600/72 = 1983px at 600dpi)
# But our asset is 1975x2116 at 600dpi = 3.29x3.53 in
# The plot box in PPTX is 238pt wide x 253pt tall
# 1pt = 1/72 in, so at 600dpi = 600/72 = 8.333 px/pt
# 238pt = 1983px, 253pt = 2108px (close to 1975x2116)
# Frame: 960x540 px. 1 frame px = 1pt = 1/72 in. At 600dpi = 8.333 render px/frame px.
# Plot box frame: x608..847 (240px), y60..312 (252px).
# Render: 240*8.333=2000px wide, 252*8.333=2100px tall. Asset is 1975x2116 (close enough).

# Let's generate at 600dpi matching the asset size exactly: 1975x2116
DPI = 600
W_PX, H_PX = 1975, 2116
W_IN, H_IN = W_PX/DPI, H_PX/DPI

fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_alpha(0.0)

# Use origin-crossing axes (like the original)
# x-axis at y=0, y-axis at x=0, with arrowheads
# Domain: x in [-12, 12], y in [-12, 12] (extend a bit)
ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)

# Hide default spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Draw origin-crossing axes manually
# x-axis line
ax.axhline(y=0, color='black', linewidth=1.2)
# y-axis line
ax.axvline(x=0, color='black', linewidth=1.2)

# Arrowheads
ax.annotate('', xy=(12, 0), xytext=(11.5, 0),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax.annotate('', xy=(-12, 0), xytext=(-11.5, 0),
            arrowprops=dict(arrowstyle='<-', color='black', lw=1.2))
ax.annotate('', xy=(0, 12), xytext=(0, 11.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax.annotate('', xy=(0, -12), xytext=(0, -11.5),
            arrowprops=dict(arrowstyle='<-', color='black', lw=1.2))

# Ticks: -10, -6, -2, 2, 6, 10 on x; -10..10 on y
xticks = [-10, -6, -2, 2, 6, 10]
yticks = list(range(-10, 11, 2))
ax.set_xticks(xticks)
ax.set_yticks(yticks)

# Labels: "y" at top of y-axis, "x" at right of x-axis
ax.text(0.3, 11.5, "y", fontsize=12, color="black", va="center", ha="left")
ax.text(11.5, -0.3, "x", fontsize=12, color="black", va="top", ha="center")

# Plot the CYAN curve (mean rgb 124, 200, 203)
curve_color = (124/255, 200/255, 203/255)
ax.plot(pts_dom[:,0], pts_dom[:,1], color=curve_color, linewidth=1.8, zorder=2)

# Red markers at the 3 cluster positions (from measurement)
# frame (741,150), (771,126), (783,148) -> convert to domain
for mk_fx, mk_fy in [(741, 150), (771, 126), (783, 148)]:
    fx_rel = mk_fx - X0
    fy_rel = mk_fy - Y0
    xd = (fx_rel - y_axis_fx) * (24 / (X1 - X0))
    yd = (x_axis_fy - fy_rel) / 7.91
    ax.scatter(xd, yd, color="red", s=30, zorder=3)

# Orange arrow pointing to the local max (frame 771,126) -> domain (3.80, 13.58)? 
# Wait, that's above y=12. Let me check: the arrow target should be on the curve.
# The marker at (771,126) is at frame y=126, x-axis at y=172, so it's ABOVE the x-axis (positive y).
# fx_rel=771-608=163. xd = (163-116)*0.1004 = 4.72. 
# fy_rel=126-60=66. yd = (112-66)/7.91 = 5.81.
# f(4.72) = (22.3*cos(4.72)-4.72)/10. cos(4.72)=-0.005. f≈-0.47. But the marker is above x-axis.
# Hmm, maybe the marker at (771,126) is the LOCAL MAX. f(x) near x=6 is positive.
# Let me just use the curve data to find the local maximum in the right region.

# The orange arrow from frame: x765..778, y116..135. Target around (771,126).
# This is a local maximum on the curve. In our domain data, find max y near x=4.7.
mask = (pts_dom[:,0] > 4) & (pts_dom[:,0] < 6)
if mask.any():
    max_idx = pts_dom[mask, 1].argmax()
    mx, my = pts_dom[mask][max_idx]
    print(f"local max near x=5: ({mx:.2f}, {my:.2f})")
    # Arrow from slightly left/above
    ax.annotate('', xy=(mx, my), xytext=(mx-0.8, my+1.5),
                arrowprops=dict(arrowstyle='->', color='orange', lw=2.5))

# Green marker on global minimum: frame 799..816 y255..266 -> domain
# fx=807, fy=260 -> fx_rel=199, fy_rel=200
# xd = (199-116)*0.1004 = 8.33
# yd = (112-200)/7.91 = -11.1 (very negative = global min)
ax.scatter(8.33, -11.1, color="lime", s=60, zorder=3, marker='o', edgecolors='none')

# Pink "Reach global Minima" callout: frame box x743..834, y270..306
# In box coords: fx_rel=743-608=135..834-608=226; fy_rel=270-60=210..306-60=246
# Domain: xd=(135-116)*0.1004=1.91..(226-116)*0.1004=11.0
# yd=(112-210)/7.91=-12.4..(112-246)/7.91=-16.9 (below plot)
# The callout sits at the BOTTOM of the chart frame, below x-axis (y=0).
# In PPTX build, it was placed at the bottom of the chart frame.
# Let's put it at the bottom-right of the chart.
ax.text(10, -10.5, "Reach\nglobal Minima", fontsize=9, color="#B0188C", 
        fontstyle='italic', fontweight='bold', va="top", ha="right",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#F9C7EF", edgecolor="#C040B0", linewidth=1.2))

# Red dashed drop guide from the marked local max down to the x-axis
# The local max is at frame (771,126) -> xd≈4.72. Drop to y=0.
# In the original, red dashed line from the local max down to x-axis at x≈783.
# Let's use the x from the drop guide: frame x783 -> fx_rel=175 -> xd=(175-116)*0.1004=5.92
ax.plot([5.92, 5.92], [0, 1.5], color="#C41E1E", linestyle="--", linewidth=1, zorder=1)

# Red initial-point dot: frame x779..787 y144..152 -> fx_rel=171..179, fy_rel=84..92
# xd=(175-116)*0.1004=5.92, yd=(112-88)/7.91=3.03
ax.scatter(5.92, 3.03, color="#C41E1E", s=25, zorder=3, edgecolors="none")

# Save
out_path = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
            "03_ridger_regression_gradient_descent/recreated_pptx/build/assets/"
            "slide_034_plot.png")
fig.savefig(out_path, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0)
plt.close(fig)
print(f"Saved to {out_path}: {W_IN:.4f}x{H_IN:.4f} in")

# Also generate the version used in PPTX (with border and white backing handled there)
# This is just the plot content.