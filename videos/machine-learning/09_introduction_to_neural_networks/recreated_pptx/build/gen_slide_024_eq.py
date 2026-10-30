#!/usr/bin/env python3
"""Generate equation PNGs for slide 024 at 600 dpi with per-glyph color compositing.

The original slide colors the three 'x' argument glyphs (in f(x), Sigmoid(x),
and the e^{-x} exponent) red. Mathtext has no \color, so we render the black
equation and overlay separately-rendered red glyphs at measured positions.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np

OUT_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 600
FONT_SIZE = 22
BLACK = '#000000'
RED = '#c00000'
BLUE = '#0000ff'


def render(spec, name, color):
    fig, ax = plt.subplots(figsize=(1, 1), dpi=DPI)
    ax.text(0.5, 0.5, spec, ha='center', va='center',
            fontsize=FONT_SIZE, color=color, fontfamily='DejaVu Sans')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.tight_layout(pad=0)
    out = os.path.join(OUT_DIR, name)
    fig.savefig(out, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)
    img = Image.open(out)
    w, h = img.size
    print(f"{name}: {w}x{h} px = {w/DPI:.3f}x{h/DPI:.3f} in")
    return img


def dims(name):
    img = Image.open(os.path.join(OUT_DIR, name))
    return img.size


def overlay(base_img, layer_name, x_frac, y_frac):
    """Paste layer (transparent PNG) onto base at fractional position
    measured against base's ink bbox."""
    base = base_img.convert('RGBA')
    layer = Image.open(os.path.join(OUT_DIR, layer_name)).convert('RGBA')

    def ink_bbox(img):
        a = np.array(img)
        alpha = a[:, :, 3]
        ys, xs = np.where(alpha > 8)
        return (xs.min(), ys.min(), xs.max(), ys.max())

    bx0, by0, bx1, by1 = ink_bbox(base)
    bw = bx1 - bx0 + 1
    bh = by1 - by0 + 1
    lx0, ly0, lx1, ly1 = ink_bbox(layer)
    lw, lh = lx1 - lx0 + 1, ly1 - ly0 + 1

    px = int(bx0 + x_frac * bw - lx0 - lw / 2)
    py = int(by0 + y_frac * bh - ly0 - lh / 2)
    base.alpha_composite(layer, (px, py))
    return base


def report(img, name, save=True):
    w, h = img.size
    if save:
        img.save(os.path.join(OUT_DIR, name))
    print(f"{name}: {w}x{h} px = {w/DPI:.3f}x{h/DPI:.3f} in")
    return w / DPI, h / DPI


# ---- 1. Sigmoid definition: f(x) = Sigmoid(x) = 1/(1+e^{-x}) ----
# base black
base = render(r"$f(x)=\mathrm{Sigmoid}(x)=\frac{1}{1+e^{-x}}$", "_s024_sig_base.png", BLACK)
report(base, "eq_s024_sigmoid.png")

print("done black sigmoid")
