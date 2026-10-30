#!/usr/bin/env python3
"""graphgen for slide 013: XOR scatter plot with two diagonal decision boundaries,
six data points (2 red X, 2 green circles, 2 cyan circles), axes with arrowheads,
and a small handwritten annotation mark.

Usage: python3 graphgen/slide_013_xor_scatter.py <out.png>
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys

# Output dimensions (inches at 150 DPI to match render pipeline)
# Plot frame from analysis: middle right, roughly x=6.0-12.0, y=1.5-4.5
# = w=6.0in, h=3.0in
DPI = 150
W_IN = 6.0
H_IN = 3.0

# Colors from analysis (hex)
BG = "#FFFFFF"           # plot background (white)
FRAME_COLOR = "#B22222"  # red frame border
DARK_BLUE = "#191970"    # dark blue for diagonal lines
RED = "#B22222"          # red for X markers
GREEN = "#008000"        # green for circles
CYAN = "#00CED1"         # cyan for circles
BLACK = "#000000"        # black for axes
GRAY = "#808080"         # gray for annotation

def generate_plot(output_path):
    fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    
    # Set up coordinate system: [0,1] x [0,1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Draw red frame around plot
    rect = plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor=FRAME_COLOR, linewidth=1.5, zorder=20)
    ax.add_patch(rect)
    
    # Axes with arrowheads
    # x1 axis (horizontal, bottom)
    ax.annotate('', xy=(0.95, 0.05), xytext=(0.05, 0.05),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=1.5), zorder=10)
    # x2 axis (vertical, left)
    ax.annotate('', xy=(0.05, 0.95), xytext=(0.05, 0.05),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=1.5), zorder=10)
    
    # Axis labels
    ax.text(0.98, 0.02, 'x\u2081', color=BLACK, fontsize=14, fontweight='normal',
            ha='right', va='bottom', family='sans-serif', zorder=15)
    ax.text(0.02, 0.98, 'x\u2082', color=BLACK, fontsize=14, fontweight='normal',
            ha='left', va='top', family='sans-serif', zorder=15)
    
    # Two thick dark-blue diagonal lines (downward sloping left-to-right)
    x_vals = np.linspace(0, 1, 200)
    # Line 1: from upper-left to lower-right
    y1 = -0.9 * x_vals + 0.95
    # Line 2: parallel, slightly lower
    y2 = -0.9 * x_vals + 0.75
    ax.plot(x_vals, y1, color=DARK_BLUE, linewidth=3, zorder=10)
    ax.plot(x_vals, y2, color=DARK_BLUE, linewidth=3, zorder=10)
    
    # Six markers:
    # 2 red X markers (upper-left and mid-left)
    ax.plot(0.15, 0.85, 'X', color=RED, markersize=14, markeredgewidth=2.5, zorder=15)
    ax.plot(0.15, 0.55, 'X', color=RED, markersize=14, markeredgewidth=2.5, zorder=15)
    
    # 2 green circles (center-left and lower-right)
    ax.plot(0.45, 0.65, 'o', color=GREEN, markersize=10, markeredgewidth=0, zorder=15)
    ax.plot(0.85, 0.35, 'o', color=GREEN, markersize=10, markeredgewidth=0, zorder=15)
    
    # 2 cyan circles (lower-left and mid-right)
    ax.plot(0.25, 0.25, 'o', color=CYAN, markersize=10, markeredgewidth=0, zorder=15)
    ax.plot(0.75, 0.55, 'o', color=CYAN, markersize=10, markeredgewidth=0, zorder=15)
    
    # Small handwritten annotation near center [content unreadable, ?]
    # Small rectangle with ?
    ax.add_patch(plt.Rectangle((0.55, 0.55), 0.12, 0.05, facecolor='#F5F5F5', edgecolor=GRAY, linewidth=0.5, zorder=15))
    ax.text(0.61, 0.575, '?', color=GRAY, fontsize=10, ha='center', va='center', family='sans-serif', zorder=16)
    
    plt.tight_layout(pad=0)
    fig.savefig(output_path, dpi=DPI, facecolor=BG, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    print(f"Generated {output_path} ({W_IN}x{H_IN}in at {DPI} DPI)")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "scratch/slide_013_xor_scatter.png"
    generate_plot(out)