#!/usr/bin/env python3
"""Generate slide 008 graph: Multi-class classification with One-vs-All decision boundaries - FIXED VERSION."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

# Output directory
outdir = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
os.makedirs(outdir, exist_ok=True)

# Colors from validation analysis
BG_COLOR = "#e6e6e6"
PLOT_BG = "#ffffff"
PLOT_BORDER = "#c0392b"  # Red border
C1_COLOR = "#2ecc71"     # Green - UPPER cluster
C2_COLOR = "#2980b9"     # Blue - RIGHT cluster
C3_COLOR = "#c0392b"     # Red - LOWER-LEFT cluster
UNDEFINED_BG = "#d5f5e3" # Pale mint
UNDEFINED_BORDER = "#000000"
NEW_CLASS_BG = "#d7bde2" # Light purple
NEW_CLASS_BORDER = "#8e44ad"
YELLOW_LABEL = "#f1c40f"
ORANGE_Q = "#e67e22"
BLACK = "#000000"
AXIS_COLOR = BLACK

# Three decision boundary lines matching the original more closely:
# d1(x): red line from upper-left to lower-right (negative slope)
# d2(x): blue line from lower-left to upper-right (steeper positive slope) 
# d3(x): green line from lower-left to upper-right (shallower positive slope)

# Based on judge feedback, need lines that create three regions:
# C1 (green) = UPPER region (above d1 and above d3)
# C2 (blue) = RIGHT region (below d1, above d2)
# C3 (red) = LOWER-LEFT region (below d2, below d3)

# Original: red line upper-left to lower-right, blue steeper lower-left to upper-right, green shallower lower-left to upper-right
# Let's use lines that create the right regions:
# d1: y = -0.8*x + 4.2  (red, upper-left to lower-right, crosses y=4.2 at x=0)
# d2: y = 1.2*x - 1.5   (blue, lower-left to upper-right, steeper)
# d3: y = 0.4*x + 0.8   (green, lower-left to upper-right, shallower)

def classify_point(x, y):
    """Classify point based on decision boundaries matching original."""
    d1 = -0.8 * x + 4.2
    d2 = 1.2 * x - 1.5
    d3 = 0.4 * x + 0.8
    
    # C1 (green): UPPER - above both d1 and d3
    if y > d1 and y > d3:
        return 1
    # C2 (blue): RIGHT - below d1, above d2
    elif y < d1 and y > d2:
        return 2
    # C3 (red): LOWER-LEFT - below d2 and below d3
    elif y < d2 and y < d3:
        return 3
    else:
        return 0  # Ambiguous/Undefined region

# Generate points in tight clusters
np.random.seed(42)

n_per_class = 12
points = {1: [], 2: [], 3: []}

# Define cluster centers manually for tight clustering
# C1: upper region
c1_center = (2.5, 3.0)
# C2: right region  
c2_center = (4.0, 1.0)
# C3: lower-left region
c3_center = (1.0, 0.5)

centers = {1: c1_center, 2: c2_center, 3: c3_center}

for cls in [1, 2, 3]:
    cx, cy = centers[cls]
    while len(points[cls]) < n_per_class:
        # Gaussian around center, tight spread
        x = np.random.normal(cx, 0.35)
        y = np.random.normal(cy, 0.35)
        # Only accept if correctly classified
        if classify_point(x, y) == cls:
            points[cls].append((x, y))

# Create the classification plot (for embedding in PPTX)
fig, ax = plt.subplots(figsize=(5.5, 4.5), dpi=150)

# Plot decision boundaries
x_vals = np.linspace(-1, 6, 100)
ax.plot(x_vals, -0.8 * x_vals + 4.2, color=C3_COLOR, linewidth=2, label='d1(x)')
ax.plot(x_vals, 1.2 * x_vals - 1.5, color=C2_COLOR, linewidth=2)
ax.plot(x_vals, 0.4 * x_vals + 0.8, color=C1_COLOR, linewidth=2, label='d3(x)')

# Plot scatter points - tight clusters
c1_pts = np.array(points[1])
c2_pts = np.array(points[2])
c3_pts = np.array(points[3])

ax.scatter(c1_pts[:, 0], c1_pts[:, 1], c=C1_COLOR, s=40, alpha=0.9, edgecolors='white', linewidth=0.5)
ax.scatter(c2_pts[:, 0], c2_pts[:, 1], c=C2_COLOR, s=40, alpha=0.9, edgecolors='white', linewidth=0.5)
ax.scatter(c3_pts[:, 0], c3_pts[:, 1], c=C3_COLOR, s=40, alpha=0.9, edgecolors='white', linewidth=0.5)

# Add hatching for regions using contourf
xx, yy = np.meshgrid(np.linspace(-1, 6, 200),
                     np.linspace(-1, 6, 200))

# Region masks
d1_yy = -0.8 * xx + 4.2
d2_yy = 1.2 * xx - 1.5
d3_yy = 0.4 * xx + 0.8

mask_c1 = (yy > d1_yy) & (yy > d3_yy)
mask_c2 = (yy < d1_yy) & (yy > d2_yy)
mask_c3 = (yy < d2_yy) & (yy < d3_yy)

# Light hatching - use very light colors for fill with hatches
ax.contourf(xx, yy, mask_c1.astype(float), levels=[0.5, 1.5], hatches=['///'], 
            colors=[C1_COLOR], alpha=0.08)
ax.contourf(xx, yy, mask_c2.astype(float), levels=[0.5, 1.5], hatches=['\\\\\\'], 
            colors=[C2_COLOR], alpha=0.08)
ax.contourf(xx, yy, mask_c3.astype(float), levels=[0.5, 1.5], hatches=['+++'], 
            colors=[C3_COLOR], alpha=0.08)

# Set limits and aspect
ax.set_xlim(-1, 6)
ax.set_ylim(-1, 5)
ax.set_aspect('equal')

# Axes with arrowheads
ax.axhline(y=0, color=AXIS_COLOR, linewidth=1.2)
ax.axvline(x=0, color=AXIS_COLOR, linewidth=1.2)

# Arrowheads
ax.annotate('', xy=(6, 0), xytext=(5.5, 0),
            arrowprops=dict(arrowstyle='->', color=AXIS_COLOR, lw=1.5))
ax.annotate('', xy=(0, 5), xytext=(0, 4.5),
            arrowprops=dict(arrowstyle='->', color=AXIS_COLOR, lw=1.5))

# Remove ticks and labels
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel('')
ax.set_ylabel('')

# White background
ax.set_facecolor(PLOT_BG)
fig.patch.set_facecolor(PLOT_BG)

# Red border around plot
for spine in ax.spines.values():
    spine.set_color(PLOT_BORDER)
    spine.set_linewidth(2)

plt.tight_layout(pad=0.1)
plt.savefig(f"{outdir}/slide_008_classification.png", dpi=150, facecolor=PLOT_BG, edgecolor='none', bbox_inches='tight')
plt.close()

print("Generated slide_008_classification.png (FIXED)")

# Also create a full annotated version for visual reference
fig2, ax2 = plt.subplots(figsize=(10, 7.5), dpi=150)

# Plot area background
ax2.set_xlim(0, 13.33)
ax2.set_ylim(0, 7.5)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_facecolor(BG_COLOR)
fig2.patch.set_facecolor(BG_COLOR)

# Plot frame (white with red border)
plot_left, plot_bottom = 1.2, 1.0
plot_w, plot_h = 10.5, 5.5
plot_rect = plt.Rectangle((plot_left, plot_bottom), plot_w, plot_h,
                          facecolor=PLOT_BG, edgecolor=PLOT_BORDER, linewidth=2)
ax2.add_patch(plot_rect)

# Map data coordinates to plot coordinates
def map_x(x):
    return plot_left + (x - (-1)) / (6 - (-1)) * plot_w

def map_y(y):
    return plot_bottom + (y - (-1)) / (5 - (-1)) * plot_h

# Draw decision boundaries
x_d = np.linspace(-1, 6, 100)
ax2.plot(map_x(x_d), map_y(-0.8 * x_d + 4.2), color=C3_COLOR, linewidth=2, clip_on=False)
ax2.plot(map_x(x_d), map_y(1.2 * x_d - 1.5), color=C2_COLOR, linewidth=2, clip_on=False)
ax2.plot(map_x(x_d), map_y(0.4 * x_d + 0.8), color=C1_COLOR, linewidth=2, clip_on=False)

# Scatter points
for x, y in c1_pts:
    ax2.scatter(map_x(x), map_y(y), c=C1_COLOR, s=25, alpha=0.9, edgecolors='white', linewidth=0.3, clip_on=False)
for x, y in c2_pts:
    ax2.scatter(map_x(x), map_y(y), c=C2_COLOR, s=25, alpha=0.9, edgecolors='white', linewidth=0.3, clip_on=False)
for x, y in c3_pts:
    ax2.scatter(map_x(x), map_y(y), c=C3_COLOR, s=25, alpha=0.9, edgecolors='white', linewidth=0.3, clip_on=False)

# Axes inside plot
ax2.axhline(y=map_y(0), color=AXIS_COLOR, linewidth=1.2, clip_on=False)
ax2.axvline(x=map_x(0), color=AXIS_COLOR, linewidth=1.2, clip_on=False)
# Arrowheads
ax2.annotate('', xy=(map_x(6), map_y(0)), xytext=(map_x(5.5), map_y(0)),
            arrowprops=dict(arrowstyle='->', color=AXIS_COLOR, lw=1.5), clip_on=False)
ax2.annotate('', xy=(map_x(0), map_y(5)), xytext=(map_x(0), map_y(4.5)),
            arrowprops=dict(arrowstyle='->', color=AXIS_COLOR, lw=1.5), clip_on=False)

# Class labels (yellow boxes) - positioned near clusters
# C1: upper region
ax2.add_patch(plt.Rectangle((map_x(3.5), map_y(3.2)), 0.6, 0.4, facecolor=YELLOW_LABEL, edgecolor=BLACK, linewidth=1))
ax2.text(map_x(3.5) + 0.3, map_y(3.2) + 0.2, 'C1', ha='center', va='center', fontsize=10, fontweight='bold', color=BLACK)

# C2: right region
ax2.add_patch(plt.Rectangle((map_x(4.5), map_y(1.2)), 0.6, 0.4, facecolor=YELLOW_LABEL, edgecolor=BLACK, linewidth=1))
ax2.text(map_x(4.5) + 0.3, map_y(1.2) + 0.2, 'C2', ha='center', va='center', fontsize=10, fontweight='bold', color=BLACK)

# C3: lower-left region
ax2.add_patch(plt.Rectangle((map_x(1.2), map_y(0.8)), 0.6, 0.4, facecolor=YELLOW_LABEL, edgecolor=BLACK, linewidth=1))
ax2.text(map_x(1.2) + 0.3, map_y(0.8) + 0.2, 'C3', ha='center', va='center', fontsize=10, fontweight='bold', color=BLACK)

# Question marks (orange boxes)
q_positions = [
    (map_x(0.5), map_y(1.5)),   # left-middle
    (map_x(2.2), map_y(2.0)),   # center
    (map_x(4.5), map_y(3.0)),   # upper-right
    (map_x(2.0), map_y(0.2)),   # bottom-center
]
for qx, qy in q_positions:
    ax2.add_patch(plt.Rectangle((qx, qy), 0.35, 0.35, facecolor=ORANGE_Q, edgecolor=BLACK, linewidth=1))
    ax2.text(qx + 0.175, qy + 0.175, '?', ha='center', va='center', fontsize=14, fontweight='bold', color=BLACK)

# +ve labels
ax2.text(map_x(-0.5), map_y(2.5), '+ve', fontsize=10, color=BLACK, fontweight='bold')
ax2.text(map_x(4.0), map_y(3.8), '+ve', fontsize=10, color=BLACK, fontweight='bold')
ax2.text(map_x(3.5), map_y(-0.3), '+ve', fontsize=10, color=BLACK, fontweight='bold')

# Decision boundary labels
ax2.text(map_x(1.5), map_y(3.5), 'd1(x)', fontsize=12, fontweight='bold', color=C3_COLOR)
ax2.text(map_x(4.8), map_y(1.0), 'd3(x)', fontsize=12, fontweight='bold', color=C1_COLOR)

# Undefined box (top-left outside plot)
undef_x, undef_y = 0.3, 6.5
ax2.add_patch(plt.Rectangle((undef_x, undef_y), 2.0, 0.5, facecolor=UNDEFINED_BG, edgecolor=UNDEFINED_BORDER, linewidth=1))
ax2.text(undef_x + 1.0, undef_y + 0.25, 'Undefined', ha='center', va='center', fontsize=10, fontweight='bold', color=BLACK)
# Leader lines
ax2.plot([undef_x + 1.0, map_x(1.5)], [undef_y, map_y(2)], color=C3_COLOR, linewidth=1, linestyle='-')

# New Class box (middle-right outside plot)
newc_x, newc_y = 11.5, 3.5
ax2.add_patch(plt.Rectangle((newc_x, newc_y), 1.5, 0.5, facecolor=NEW_CLASS_BG, edgecolor=NEW_CLASS_BORDER, linewidth=1))
ax2.text(newc_x + 0.75, newc_y + 0.25, 'New Class', ha='center', va='center', fontsize=10, fontweight='bold', color=BLACK)

plt.tight_layout(pad=0)
plt.savefig(f"{outdir}/slide_008_full_annotated.png", dpi=150, facecolor=BG_COLOR, edgecolor='none')
plt.close()

print("Generated slide_008_full_annotated.png (FIXED)")