#!/usr/bin/env python3
"""
Generate 2D decision boundary diagram for slide 007 (Multi-Class Classification using ONE VS ALL).

Recreates the one-vs-all classification plot with:
- Three decision boundaries: red (descending), green (ascending), blue (steeper ascending)
- Three class regions with diagonal hatching: C1 (upper-left, light green), C2 (lower-right, light blue), C3 (bottom, light pink)
- Colored data points in each region
- '+ ve' annotations with BLACK text and thick colored arrows
- RED coordinate axes with arrowheads
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.path import Path as MplPath
from pathlib import Path

OUT_DIR = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Figure size in inches - will be embedded at exact size in PPTX
FIG_W, FIG_H = 8.66, 5.25
DPI = 600

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis('off')

# Colors
WHITE = '#ffffff'
RED = '#ff0000'
GREEN = '#008000'
BLUE = '#0000ff'
LIGHT_GREEN = '#90ee90'
LIGHT_BLUE = '#add8e6'
LIGHT_PINK = '#ffb6c1'
YELLOW = '#ffff00'
BLACK = '#000000'

# Line widths
LINE_W = 2.5
AXIS_W = 2.5
ARROW_W = 2.5

# ============================================================
# Define the three decision boundary lines
# Positioned to create THREE pure class wedges at the corners
# All lines pass near center but with slightly different intercepts
# to form a small central triangle (not a single intersection point)
# ============================================================

# Red line: descending from upper-left to lower-right
# Positive side (C1) = ABOVE the line (upper-left)
# From (0, 0.85) to (1, 0.15) -> y = -0.7x + 0.85
red_slope = -0.7
red_intercept = 0.85

# Green line: ascending from lower-left to upper-right
# Positive side (C2) = ABOVE the line (upper-right) 
# From (0, 0.25) to (1, 0.85) -> y = 0.6x + 0.25
green_slope = 0.6
green_intercept = 0.25

# Blue line: ascending steep from lower-left to upper-right
# Positive side (C3) = BELOW the line (lower-left/bottom)
# From (0.15, 0) to (0.75, 1) -> y = (1/0.6)(x - 0.15) = 1.667x - 0.25
blue_slope = 1.667
blue_intercept = -0.25

def y_red(x): return red_slope * x + red_intercept
def y_green(x): return green_slope * x + green_intercept
def y_blue(x): return blue_slope * x + blue_intercept

# Line endpoints (clamped to [0,1] x [0,1])
def clamp_line(m, b):
    pts = []
    y0 = m*0 + b
    if 0 <= y0 <= 1: pts.append([0, y0])
    y1 = m*1 + b
    if 0 <= y1 <= 1: pts.append([1, y1])
    if m != 0:
        x0 = -b/m
        if 0 <= x0 <= 1: pts.append([x0, 0])
        x1 = (1-b)/m
        if 0 <= x1 <= 1: pts.append([x1, 1])
    return np.array(pts)

red_pts = clamp_line(red_slope, red_intercept)
green_pts = clamp_line(green_slope, green_intercept)
blue_pts = clamp_line(blue_slope, blue_intercept)

red_p1, red_p2 = red_pts[0], red_pts[1]
green_p1, green_p2 = green_pts[0], green_pts[1]
blue_p1, blue_p2 = blue_pts[0], blue_pts[1]

print(f"Red: {red_p1} -> {red_p2}")
print(f"Green: {green_p1} -> {green_p2}")
print(f"Blue: {blue_p1} -> {blue_p2}")

# ============================================================
# Draw RED coordinate axes with ARROWHEADS (THICK)
# Vertical at left (x=0.05), Horizontal at bottom (y=0.05)
# ============================================================
ax.annotate('', xy=(0.05, 0.95), xytext=(0.05, 0.05),
            arrowprops=dict(arrowstyle='->', color=RED, lw=AXIS_W), zorder=3)
ax.annotate('', xy=(0.95, 0.05), xytext=(0.05, 0.05),
            arrowprops=dict(arrowstyle='->', color=RED, lw=AXIS_W), zorder=3)

# ============================================================
# Draw the three decision boundary lines WITH ARROWHEADS
# ============================================================
ax.annotate('', xy=red_p2, xytext=red_p1,
            arrowprops=dict(arrowstyle='->', color=RED, lw=LINE_W), zorder=5)
ax.annotate('', xy=green_p2, xytext=green_p1,
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=LINE_W), zorder=5)
ax.annotate('', xy=blue_p2, xytext=blue_p1,
            arrowprops=dict(arrowstyle='->', color=BLUE, lw=LINE_W), zorder=5)

# ============================================================
# Define the three CLASS REGIONS (the pure one-vs-all regions)
# Based on judge's description of original:
# C1 (green hatch): upper-left, ABOVE red line, bounded by red, green, top, left
# C2 (blue hatch): lower-right, BELOW red, ABOVE green, bounded by red, green, bottom, right
# C3 (pink hatch): bottom strip, BELOW red, BELOW green, BELOW blue, bounded by bottom, left, right, blue
# ============================================================

# Intersection points
# Intersection points
# Red-Green: -0.7x + 0.85 = 0.6x + 0.25 -> 1.3x = 0.6 -> x = 0.4615, y = 0.527
rg_x, rg_y = 0.4615, 0.527

# Red-Blue: -0.7x + 0.85 = 1.667x - 0.25 -> 2.367x = 1.1 -> x = 0.4647, y = 0.525
rb_x, rb_y = 0.4647, 0.525

# Green-Blue: 0.6x + 0.25 = 1.667x - 0.25 -> 1.067x = 0.5 -> x = 0.4686, y = 0.531
gb_x, gb_y = 0.4686, 0.531

# Blue at y=0
blue_x_at_0 = 0.25 / 1.667  # 0.15

# These are very close - small central triangle

# C1 region (upper-left): ABOVE red, ABOVE green, ABOVE blue
# Bounded by: top frame, left frame, red line (lower-right), green line (lower)
c1_poly = np.array([
    [0, 1],                    # top-left
    [0, y_green(0)],           # (0, 0.25) green at left edge
    [rg_x, rg_y],              # red-green intersection
    [0, y_red(0)],             # (0, 0.85) red at left edge
])
poly1 = Polygon(c1_poly, facecolor=LIGHT_GREEN, edgecolor='none', alpha=0.4, zorder=1)
ax.add_patch(poly1)

# C2 region (lower-right): BELOW red, ABOVE green, BELOW blue
# Bounded by: red line (upper-left), green line (upper-right), blue line (left), right frame, bottom frame
c2_poly = np.array([
    [1, 0.15],                 # red at right edge (y = -0.7*1 + 0.85 = 0.15)
    [1, 0],                    # bottom-right
    [blue_x_at_0, 0],          # blue at y=0: x = 0.15
    [gb_x, gb_y],              # green-blue intersection
    [rg_x, rg_y],              # red-green intersection
])
poly2 = Polygon(c2_poly, facecolor=LIGHT_BLUE, edgecolor='none', alpha=0.4, zorder=1)
ax.add_patch(poly2)

# C3 region (bottom): BELOW red, BELOW green, BELOW blue
# This is the large bottom region bounded by bottom frame, left frame, right frame, and the three lines from below
# At bottom (y=0): from x=0 to x=1, but above blue starts at x=0.15
# So C3 is: left of blue (x < blue_x), below green, below red
# Actually "below blue" for the bottom area means y < blue_y(x). Since blue goes from (0.15,0) up, below it is the area to the left of it at y=0.
# Let's define as: below red AND below green AND (left of blue OR below blue)
# At bottom edge y=0: below red (0 < 0.85-0.7x for x<1.21), below green (0 < 0.25+0.6x), below blue (0 < 1.667x-0.25 -> x > 0.15)
# So below blue is x > 0.15 at y=0. "Below blue" is the side toward the origin from the line.

# The region below all three lines at the bottom:
# From x=0 to x=1 at y=0, but bounded above by the lowest of the three lines
# The lowest line varies: at left, blue is lowest (at y=0, x=0.15); then green; then red.

c3_poly = np.array([
    [0, 0],                    # bottom-left
    [1, 0],                    # bottom-right
    [1, y_green(1)],           # green at right: 0.85... no, we want below green so y < green
    # Actually trace the lower envelope of the three lines
])
# Lower envelope: from left to right, which line is lowest?
# At x=0: red=0.85, green=0.25, blue=-0.25 (outside). So green is lowest in frame at x=0.
# Blue enters at x=0.15 (y=0). From x=0.15, blue is lower than green until they intersect.
# Green-blue intersection at x=0.4686, y=0.531.
# After that, green is lower than blue.
# Red is at y=0.85-0.7x. At x=0.15: red=0.745. At x=0.4686: red=0.522.
# So order from bottom: blue (from x=0.15), then green, then red.

# C3 = below the lowest of the three lines = below the lower envelope
# Lower envelope: blue from x=0.15 to x=0.4686, then green from x=0.4686 to x=1, and from x=0 to x=0.15 it's... green is at 0.25, but y=0 is below green.
# Actually at y=0, we're below all lines for x < 1. So the bottom strip is below all three.

# Let's trace: start bottom-left (0,0), go right along bottom to (1,0), up to green at right (1, 0.85), left along green to (0.4686, 0.531), left-down along blue to (0.15, 0), left along bottom to (0,0)? No.

# Simpler: C3 = below red AND below green AND below blue
# This is the region under all three lines.
# The upper boundary is the minimum of the three lines at each x.
c3_x = np.linspace(0, 1, 200)
c3_y = np.minimum.reduce([y_red(c3_x), y_green(c3_x), y_blue(c3_x)])
# But blue is negative for x < 0.15, so min will be negative. Clamp at 0.
c3_y = np.maximum(c3_y, 0)

# Build polygon for C3: bottom edge + lower envelope
c3_poly = np.array([[0, 0], [1, 0]] + list(zip(c3_x[::-1], c3_y[::-1])))
c3_poly = np.array(c3_poly)

poly3 = Polygon(c3_poly, facecolor=LIGHT_PINK, edgecolor='none', alpha=0.4, zorder=1)
ax.add_patch(poly3)

# ============================================================
# Add diagonal hatching
# ============================================================
def add_hatching(poly_verts, color, num_lines=30):
    if poly_verts is None or len(poly_verts) < 3:
        return
    min_x, max_x = poly_verts[:, 0].min(), poly_verts[:, 0].max()
    min_y, max_y = poly_verts[:, 1].min(), poly_verts[:, 1].max()
    path = MplPath(poly_verts)
    for offset in np.linspace(min_x + min_y - 0.5, max_x + max_y + 0.5, num_lines):
        x_vals = np.linspace(min_x - 0.5, max_x + 0.5, 200)
        y_vals = -x_vals + offset
        points = np.column_stack([x_vals, y_vals])
        inside = path.contains_points(points)
        if inside.any():
            segments = []
            current_seg = []
            for pt, inc in zip(points, inside):
                if inc:
                    current_seg.append(pt)
                elif current_seg:
                    segments.append(np.array(current_seg))
                    current_seg = []
            if current_seg:
                segments.append(np.array(current_seg))
            for seg in segments:
                if len(seg) > 1:
                    ax.plot(seg[:, 0], seg[:, 1], color=color, linewidth=0.5, alpha=0.7, zorder=2)

add_hatching(c1_poly, LIGHT_GREEN)
add_hatching(c2_poly, LIGHT_BLUE)
add_hatching(c3_poly, LIGHT_PINK)

# ============================================================
# Decision boundary labels - ROTATED along lines
# ============================================================
red_angle = np.degrees(np.arctan2(red_p2[1] - red_p1[1], red_p2[0] - red_p1[0]))
green_angle = np.degrees(np.arctan2(green_p2[1] - green_p1[1], green_p2[0] - green_p1[0]))
blue_angle = np.degrees(np.arctan2(blue_p2[1] - blue_p1[1], blue_p2[0] - blue_p1[0]))

# d₁(x) - on red line, upper-left portion
d1_x = 0.2
d1_y = y_red(d1_x)
ax.text(d1_x, d1_y + 0.04, 'd₁(x)', color=RED, fontsize=16, fontweight='bold', 
        ha='center', va='center', rotation=red_angle, zorder=10, family='sans-serif')

# d₂(x) - on green line, right portion
d2_x = 0.8
d2_y = y_green(d2_x)
ax.text(d2_x - 0.05, d2_y + 0.04, 'd₂(x)', color=GREEN, fontsize=16, fontweight='bold', 
        ha='center', va='center', rotation=green_angle, zorder=10, family='sans-serif')

# d₃(x) - on blue line, upper-right portion
d3_x = 0.65
d3_y = min(0.98, y_blue(d3_x))
ax.text(d3_x - 0.03, d3_y - 0.04, 'd₃(x)', color=BLUE, fontsize=16, fontweight='bold', 
        ha='center', va='center', rotation=blue_angle, zorder=10, family='sans-serif')

# ============================================================
# Class label boxes (yellow with C₁, C₂, C₃)
# ============================================================
# C1 in upper-left green region
ax.text(0.15, 0.7, 'C₁', color=BLACK, fontsize=16, fontweight='bold', ha='center', va='center', 
        bbox=dict(boxstyle='round,pad=0.3', facecolor=YELLOW, edgecolor='none'), zorder=10)

# C2 in lower-right blue region
ax.text(0.8, 0.25, 'C₂', color=BLACK, fontsize=16, fontweight='bold', ha='center', va='center', 
        bbox=dict(boxstyle='round,pad=0.3', facecolor=YELLOW, edgecolor='none'), zorder=10)

# C3 in bottom pink region
ax.text(0.5, 0.08, 'C₃', color=BLACK, fontsize=16, fontweight='bold', ha='center', va='center', 
        bbox=dict(boxstyle='round,pad=0.3', facecolor=YELLOW, edgecolor='none'), zorder=10)

# ============================================================
# Data points in each region
# ============================================================
np.random.seed(42)
n_dots = 12

# C1: above red, above green, above blue (upper-left)
c1_points = []
for _ in range(n_dots * 5):
    x = np.random.uniform(0.05, 0.45)
    y = np.random.uniform(0.6, 0.95)
    if y > y_red(x) and y > y_green(x) and y > y_blue(x):
        c1_points.append((x, y))
    if len(c1_points) >= n_dots:
        break

for x, y in c1_points:
    ax.plot(x, y, 'o', color=GREEN, markersize=8, markeredgecolor='none', zorder=6)

# C2: below red, above green, below blue (lower-right wedge)
c2_points = []
for _ in range(n_dots * 5):
    x = np.random.uniform(0.55, 0.95)
    y = np.random.uniform(0.05, 0.55)
    if y < y_red(x) and y > y_green(x) and y < y_blue(x):
        c2_points.append((x, y))
    if len(c2_points) >= n_dots:
        break

for x, y in c2_points:
    ax.plot(x, y, 'o', color=BLUE, markersize=8, markeredgecolor='none', zorder=6)

# C3: below red, below green, below blue (bottom region)
c3_points = []
for _ in range(n_dots * 5):
    x = np.random.uniform(0.05, 0.95)
    y = np.random.uniform(0.02, 0.35)
    if y < y_red(x) and y < y_green(x) and y < y_blue(x):
        c3_points.append((x, y))
    if len(c3_points) >= n_dots:
        break

for x, y in c3_points:
    ax.plot(x, y, 'o', color=RED, markersize=8, markeredgecolor='none', zorder=6)

# ============================================================
# '+ ve' annotations - BLACK text with THICK colored arrows
# Using ax.arrow for clean straight arrows (not curved annotate)
# ============================================================
# Red +ve: on positive side of red (above/upper-left) near lower-right of red line
# Red line goes from (0,0.85) to (1,0.15). Lower-right portion is near x=0.8, y=0.21.
# Positive side is above the line.
ax.arrow(0.82, 0.22, -0.08, 0.05, head_width=0.015, head_length=0.02,
         fc=RED, ec=RED, lw=ARROW_W, zorder=10, length_includes_head=True)
ax.text(0.88, 0.25, '+ ve', color=BLACK, fontsize=14, fontweight='bold', 
        ha='center', va='center', zorder=10)

# Green +ve: on positive side of green (above/upper-right) near left of green line
# Green line from (0,0.25) to (1,0.85). Left portion near x=0.2, y=0.37.
# Positive side is above the line.
ax.arrow(0.18, 0.42, 0.06, 0.04, head_width=0.015, head_length=0.02,
         fc=GREEN, ec=GREEN, lw=ARROW_W, zorder=10, length_includes_head=True)
ax.text(0.1, 0.45, '+ ve', color=BLACK, fontsize=14, fontweight='bold', 
        ha='center', va='center', zorder=10)

# Blue +ve: on positive side of blue (below/lower-left) near upper-right of blue line
# Blue line from (0.15,0) to (0.75,1). Upper-right portion near x=0.65, y=0.83.
# Positive side is BELOW the line (judge: "+ ve near blue line's upper-right" and positive side of blue is below).
ax.arrow(0.65, 0.78, 0.05, -0.05, head_width=0.015, head_length=0.02,
         fc=BLUE, ec=BLUE, lw=ARROW_W, zorder=10, length_includes_head=True)
ax.text(0.72, 0.72, '+ ve', color=BLACK, fontsize=14, fontweight='bold', 
        ha='center', va='center', zorder=10)

# ============================================================
# Save
# ============================================================
output_path = OUT_DIR / "slide_007_decision_boundary.png"
plt.savefig(output_path, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()

print(f"Generated: {output_path}")
print(f"Size: {FIG_W*DPI:.0f} x {FIG_H*DPI:.0f} px at {DPI} dpi")
print(f"Inches at 600dpi embed: {FIG_W:.2f} x {FIG_H:.2f} in")

# Sidecar JSON with metadata
import json
meta = {
    "image": "slide_007_decision_boundary.png",
    "width_in": FIG_W,
    "height_in": FIG_H,
    "dpi": DPI,
    "position": {
        "x": 2.4,
        "y": 1.65,
        "w": 8.66,
        "h": 5.25
    }
}
with open(OUT_DIR / "slide_007_decision_boundary.json", "w") as f:
    json.dump(meta, f, indent=2)
print(f"Metadata saved to {OUT_DIR}/slide_007_decision_boundary.json")