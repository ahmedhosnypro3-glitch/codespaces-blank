#!/usr/bin/env python3
"""Generate professional 2D equations for slide 030 sigmoid formulas."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Sigmoid equations for O3-O7
# Professional 2D: stacked fraction with horizontal bar, e^{-x} superscript
equations = [
    # (filename, mathtext)
    ("eq_O3.png", r"$O_3 = \frac{1}{1 + e^{-2.3}} = 0.909$"),
    ("eq_O4.png", r"$O_4 = \frac{1}{1 + e^{-3.4}} = 0.968$"),
    ("eq_O5.png", r"$O_5 = \frac{1}{1 + e^{-4.5}} = 0.989$"),
    ("eq_O6.png", r"$O_6 = \frac{1}{1 + e^{-1.1544}} = 0.76$"),
    ("eq_O7.png", r"$O_7 = \frac{1}{1 + e^{-1.1544}} = 0.76$"),
]

# Also need Net equations with proper subscripts
net_equations = [
    ("eq_Net3.png", r"$Net_3 = 7 \times 0.1 + 4 \times 0.4 = 2.3$"),
    ("eq_Net4.png", r"$Net_4 = 7 \times 0.2 + 4 \times 0.5 = 3.4$"),
    ("eq_Net5.png", r"$Net_5 = 7 \times 0.3 + 4 \times 0.6 = 4.5$"),
    ("eq_Net6.png", r"$Net_6 = 0.909 \times 0.3 + 0.968 \times 0.4 + 0.989 \times 0.5 = 1.1544$"),
    ("eq_Net7.png", r"$Net_7 = 0.909 \times 0.3 + 0.968 \times 0.4 + 0.989 \times 0.5 = 1.1544$"),
]

def render_eq(filename, mathtext, fontsize=16, dpi=600):
    """Render a single mathtext equation to transparent PNG."""
    fig = plt.figure(figsize=(0.1, 0.1))
    fig.patch.set_alpha(0)
    plt.axis('off')
    # Render mathtext
    text = plt.text(0, 0, mathtext, fontsize=fontsize, color='black',
                    ha='left', va='bottom', fontfamily='DejaVu Sans',
                    math_fontfamily='cm')
    plt.draw()
    # Get tight bbox
    bbox = text.get_window_extent(renderer=fig.canvas.get_renderer())
    bbox_inches = bbox.transformed(fig.dpi_scale_trans.inverted())
    plt.close(fig)
    
    # Re-render with exact size
    w, h = bbox_inches.width, bbox_inches.height
    fig = plt.figure(figsize=(w, h), dpi=dpi)
    fig.patch.set_alpha(0)
    plt.axis('off')
    plt.text(0, 0, mathtext, fontsize=fontsize, color='black',
             ha='left', va='bottom', fontfamily='DejaVu Sans',
             math_fontfamily='cm')
    out_path = os.path.join(OUT_DIR, filename)
    fig.savefig(out_path, dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)
    print(f"Rendered {filename}: {w:.2f}x{h:.2f} in @ {dpi}dpi = {int(w*dpi)}x{int(h*dpi)} px")

for fname, mathtext in equations:
    render_eq(fname, mathtext, fontsize=16, dpi=600)

for fname, mathtext in net_equations:
    render_eq(fname, mathtext, fontsize=16, dpi=600)

print("Done generating equations.")