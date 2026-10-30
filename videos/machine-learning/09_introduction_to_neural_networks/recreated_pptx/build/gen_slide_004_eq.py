#!/usr/bin/env python3
"""
Generate equation PNGs for slide 004 using matplotlib mathtext at 600 dpi.
Professional Format (2D) rendering for all equations.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 600
FONT_SIZE = 22  # Base font size for equations
COLOR = '#000000'
RED = '#c00000'
GREEN = '#00b050'
BLUE = '#0000ff'

# Equation definitions with their mathtext strings and colors
# Each equation will be rendered separately
equations = [
    {
        "name": "eq_delta_def_1",
        "mathtext": r"$\delta_i = -1$",
        "color": COLOR
    },
    {
        "name": "eq_delta_def_2",
        "mathtext": r"$\delta_i = +1$",
        "color": COLOR
    },
    {
        "name": "eq_dx_delta",
        "mathtext": r"$d(X)\delta_i > 0$",
        "color": COLOR
    },
    {
        "name": "eq_error",
        "mathtext": r"$\mathrm{Error} = \sum_{\mathrm{all\ misclassified\ vectors\ }(i)} \delta_i W^T X_i$",
        "color": COLOR
    },
    {
        "name": "eq_summation_positive",
        "mathtext": r"$\mathrm{Summation\ is\ always\ }positive$",
        "color": COLOR
    },
    {
        "name": "eq_gradient_descent",
        "mathtext": r"$W^{\mathrm{(updated)}} = W^{\mathrm{(old)}} - \eta \frac{\partial \mathrm{Error}}{\partial W}$",
        "color": COLOR
    },
    {
        "name": "eq_gradient",
        "mathtext": r"$\frac{\partial \mathrm{Error}}{\partial W} = \sum_{\mathrm{misclassified\ vectors}} \delta_i X_i$",
        "color": COLOR
    },
    {
        "name": "eq_update_batch",
        "mathtext": r"$W^{\mathrm{(updated)}} = W^{\mathrm{(old)}} - \eta \sum_{\mathrm{misclassified\ vectors\ ONLY\ }(i)} \delta_i X_i$",
        "color": COLOR
    },
    {
        "name": "eq_update_online",
        "mathtext": r"$W^{\mathrm{(updated)}} = W^{\mathrm{(old)}} - \eta \delta_i X_i$",
        "color": COLOR
    },
]

for eq in equations:
    fig, ax = plt.subplots(figsize=(1, 1), dpi=DPI)
    ax.text(0.5, 0.5, eq["mathtext"], 
            ha='center', va='center', 
            fontsize=FONT_SIZE, color=eq["color"],
            fontfamily='DejaVu Sans')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Tight bbox
    fig.tight_layout(pad=0)
    
    # Save with transparent background
    out_path = os.path.join(OUT_DIR, f"{eq['name']}.png")
    fig.savefig(out_path, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)
    
    # Get actual dimensions
    from PIL import Image
    img = Image.open(out_path)
    w_px, h_px = img.size
    w_in = w_px / DPI
    h_in = h_px / DPI
    print(f"{eq['name']}: {w_px}x{h_px} px = {w_in:.3f}x{h_in:.3f} in")

print("All equation PNGs generated.")