#!/usr/bin/env python3
"""graphgen for slide 007: 2D One-vs-All classification plot with three linear
decision boundaries, hatched regions, class labels, and data points.
Matches the original slide's measured colors and layout.

Usage: python3 graphgen/slide_007_ovr.py <out.png>
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys

# Output dimensions (inches at 150 DPI to match render pipeline)
# Plot frame from analysis: 18%-83% of slide width (13.33in), 22%-92% of slide height (7.5in)
# = x: 2.4in to 11.06in (w=8.66in), y: 1.65in to 6.9in (h=5.25in)
DPI = 150
W_IN = 8.66
H_IN = 5.25

# Colors from analysis (hex, no # prefix for matplotlib)
BG = "#FFFFFF"           # plot background (white)
FRAME_COLOR = "#FF0000"  # red frame border
# Decision boundary colors
RED = "#FF0000"
GREEN = "#008000"
BLUE = "#0000FF"
# Region hatching colors
HATCH_C1 = "#90EE90"    # light green
HATCH_C2 = "#ADD8E6"    # light blue
HATCH_C3 = "#FFB6C1"    # light pink
# Class label box
LABEL_BOX = "#FFFF00"   # yellow
LABEL_TEXT = "#000000"  # black
# Data point colors
DOT_C1 = "#008000"
DOT_C2 = "#0000FF"
DOT_C3 = "#FF0000"
# +ve annotation colors
PLUSVE_C1 = "#FF0000"
PLUSVE_C2 = "#008000"
PLUSVE_C3 = "#0000FF"

# Decision boundary lines in normalized [0,1] x [0,1] (0,0 = bottom-left)
# d1: descending from upper-left to lower-right, separates C1 (above) from C3 (below)
# d2: ascending moderate, separates C2 (above) from C3 (below)
# d3: ascending steep, separates C1 (above) from C2 (below)

def d1(x): return -0.7 * x + 0.85
def d2(x): return 0.5 * x + 0.15
def d3(x): return 1.3 * x - 0.15

def region(x, y):
    """Return region number: 1=C1(top), 2=C2(right), 3=C3(bottom-left)"""
    above_d1 = y > d1(x)
    above_d2 = y > d2(x)
    above_d3 = y > d3(x)
    if above_d1 and above_d3:
        return 1
    elif above_d2 and not above_d3:
        return 2
    else:
        return 3

def generate_plot(output_path):
    fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    
    # Set up coordinate system: normalized [0,1] x [0,1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    x_vals = np.linspace(0, 1, 400)
    
    # Fill hatched regions
    # C1: y from max(d1, d3) to 1 (top region)
    y_upper_c1 = np.maximum(d1(x_vals), d3(x_vals))
    ax.fill_between(x_vals, y_upper_c1, 1, color=HATCH_C1, hatch='/////', alpha=0.6, edgecolor='none')
    
    # C2: y from d2 to d3 where d2 < d3 (right region, x > 0.375)
    x_c2 = x_vals[x_vals >= 0.375]
    ax.fill_between(x_c2, d2(x_c2), d3(x_c2), color=HATCH_C2, hatch='/////', alpha=0.6, edgecolor='none')
    
    # C3: y from 0 to min(d1, d2) (bottom-left region)
    y_lower_c3 = np.minimum(d1(x_vals), d2(x_vals))
    ax.fill_between(x_vals, 0, y_lower_c3, color=HATCH_C3, hatch='/////', alpha=0.6, edgecolor='none')
    
    # Draw decision boundary lines
    ax.plot(x_vals, d1(x_vals), color=RED, linewidth=1.5, zorder=10)
    ax.plot(x_vals, d2(x_vals), color=GREEN, linewidth=1.5, zorder=10)
    ax.plot(x_vals, d3(x_vals), color=BLUE, linewidth=1.5, zorder=10)
    
    # Add SMALL red axis arrows (thin, subtle - matching original's small origin arrows)
    # Vertical arrow at left edge (x=0), pointing UP
    ax.annotate('', xy=(0, 0.75), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.0), zorder=9)
    # Horizontal arrow at bottom edge (y=0), pointing RIGHT
    ax.annotate('', xy=(0.75, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.0), zorder=9)
    
    # Add labels for decision boundaries - POSITIONED PER ORIGINAL
    # d1 label: upper-left, NEAR red line but LEFT of C1 badge, not clipped
    # Red line at x=0.05: y=0.815; place label to the right of that, above line
    ax.text(0.06, d1(0.06) + 0.04, 'd\u2081(x)', color=RED, fontsize=13, fontweight='bold',
            ha='left', va='bottom', family='sans-serif', zorder=18)
    
    # d2 label: far right, near green line
    ax.text(0.95, d2(0.95) - 0.04, 'd\u2082(x)', color=GREEN, fontsize=13, fontweight='bold',
            ha='right', va='top', family='sans-serif', zorder=18)
    
    # d3 label: top-right, near blue line
    ax.text(0.80, d3(0.80) + 0.04, 'd\u2083(x)', color=BLUE, fontsize=13, fontweight='bold',
            ha='center', va='bottom', family='sans-serif', zorder=18)
    
    # Generate data points for each region - DETERMINISTIC (fixed positions)
    # Hand-picked positions inside each region matching original's sparse distribution
    c1_dots = [(0.30, 0.95), (0.45, 0.92), (0.55, 0.88), (0.65, 0.93), (0.72, 0.87),
               (0.25, 0.88), (0.38, 0.85), (0.60, 0.80)]
    c2_dots = [(0.72, 0.55), (0.80, 0.50), (0.88, 0.58), (0.92, 0.45), (0.78, 0.42),
               (0.85, 0.35), (0.93, 0.30), (0.70, 0.45)]
    c3_dots = [(0.15, 0.15), (0.25, 0.22), (0.35, 0.12), (0.45, 0.25), (0.55, 0.18),
               (0.20, 0.05), (0.40, 0.30), (0.50, 0.10)]
    
    for (x, y) in c1_dots:
        ax.plot(x, y, 'o', color=DOT_C1, markersize=7, markeredgewidth=0, zorder=15)
    for (x, y) in c2_dots:
        ax.plot(x, y, 'o', color=DOT_C2, markersize=7, markeredgewidth=0, zorder=15)
    for (x, y) in c3_dots:
        ax.plot(x, y, 'o', color=DOT_C3, markersize=7, markeredgewidth=0, zorder=15)
    
    # Add class labels in yellow boxes - POSITIONED PER ORIGINAL
    # C1 label: upper-left area (near green dots), clearly above red line
    ax.text(0.18, 0.78, 'C\u2081', color=LABEL_TEXT, fontsize=11, fontweight='bold',
            ha='center', va='center', family='sans-serif', zorder=20,
            bbox=dict(boxstyle='square,pad=0.25', facecolor=LABEL_BOX, edgecolor='none'))
    
    # C2 label: middle-right area
    ax.text(0.80, 0.65, 'C\u2082', color=LABEL_TEXT, fontsize=11, fontweight='bold',
            ha='center', va='center', family='sans-serif', zorder=20,
            bbox=dict(boxstyle='square,pad=0.25', facecolor=LABEL_BOX, edgecolor='none'))
    
    # C3 label: bottom-left area
    ax.text(0.28, 0.38, 'C\u2083', color=LABEL_TEXT, fontsize=11, fontweight='bold',
            ha='center', va='center', family='sans-serif', zorder=20,
            bbox=dict(boxstyle='square,pad=0.25', facecolor=LABEL_BOX, edgecolor='none'))
    
    # Add "+ve" annotations (NO SPACE, color-coded per original) with arrows
    # Red +ve: near bottom-right end of red line
    x_plus1 = 0.88
    y_plus1 = d1(x_plus1) - 0.06
    ax.annotate('+ve', xy=(0.82, d1(0.82)), xytext=(x_plus1, y_plus1),
                color=PLUSVE_C1, fontsize=10, fontweight='bold', ha='center', va='top',
                arrowprops=dict(arrowstyle='->', color=PLUSVE_C1, lw=1.0), zorder=20)
    
    # Green +ve: left side, mid-height, pointing toward green line
    x_plus2 = 0.06
    y_plus2 = 0.42
    ax.annotate('+ve', xy=(0.16, d2(0.16)), xytext=(x_plus2, y_plus2),
                color=PLUSVE_C2, fontsize=10, fontweight='bold', ha='center', va='center',
                arrowprops=dict(arrowstyle='->', color=PLUSVE_C2, lw=1.0), zorder=20)
    
    # Blue +ve: top-right next to blue line, near d3 label
    x_plus3 = 0.93
    y_plus3 = 0.93
    ax.annotate('+ve', xy=(0.88, d3(0.88)), xytext=(x_plus3, y_plus3),
                color=PLUSVE_C3, fontsize=10, fontweight='bold', ha='center', va='center',
                arrowprops=dict(arrowstyle='->', color=PLUSVE_C3, lw=1.0), zorder=20)
    
    # Draw red frame around plot
    rect = plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor=FRAME_COLOR, linewidth=1.5, zorder=20)
    ax.add_patch(rect)
    
    plt.tight_layout(pad=0)
    fig.savefig(output_path, dpi=DPI, facecolor=BG, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    print(f"Generated {output_path} ({W_IN}x{H_IN}in at {DPI} DPI)")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "scratch/slide_007_ovr.png"
    generate_plot(out)