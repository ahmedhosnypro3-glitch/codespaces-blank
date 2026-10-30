#!/usr/bin/env python3
"""Color-coded 2D equation PNGs for slide_021 attempt 1.

Renders each equation as ONE 600dpi transparent PNG with per-segment colors
(certified spec: Δ_ji = η black; O_i blue; O_j(1-O_j) green; bracketed term red),
matching the original frame's colour mapping measured in adjudication.md.
Emits <name>.png + <name>.json sidecar (render_eq.py-compatible fields).
"""
import json, os, subprocess, sys
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
DPI = 600
PT = 18

def segment_w_px(latex, pt=PT):
    """Advance width of a mathtext string at `pt` in points."""
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    tp = TextPath((0, 0), latex, size=pt,
                  prop=FontProperties(math_fontfamily="dejavusans", style="italic"))
    return tp.get_extents().width

def compose(segments, name, baseline_frac_note=""):
    """segments: list of (mathtext, hexcolor). Returns sidecar dict."""
    fs_pt = PT
    widths = [segment_w_px(l, fs_pt) for l, _ in segments]
    h_pt = fs_pt * 1.55
    w_pt = sum(widths)
    fig = plt.figure(figsize=(w_pt / 72.0, h_pt / 72.0), dpi=DPI)
    fig.patch.set_alpha(0.0)
    base_y = 0.30 / h_pt
    x_pt = 0.0
    for (latex, col), w in zip(segments, widths):
        fig.text(x_pt / w_pt, base_y, latex, fontsize=fs_pt, color=col,
                 style="italic", ha="left", va="baseline",
                 math_fontfamily="dejavusans")
        x_pt += w
    fig.canvas.draw()
    w_px, h_px = fig.canvas.get_width_height()
    buf = fig.canvas.buffer_rgba()
    im = Image.frombytes("RGBA", (w_px, h_px), bytes(buf))
    png = os.path.join(OUT, name + ".png")
    im.save(png)
    side = {"path": os.path.basename(png), "w_px": w_px, "h_px": h_px,
            "w_in": round(w_px / DPI, 5), "h_in": round(h_px / DPI, 5),
            "baseline_frac": 0.6959, "dpi": DPI, "fontsize_pt": fs_pt,
            "color": "#000000", "segments": [c for _, c in segments]}
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump(side, f, indent=1)
    print(f"{name}: {w_px}x{h_px}px  {side['w_in']}x{side['h_in']}in")
    plt.close(fig)
    return side

if __name__ == "__main__":
    # Colour map measured from unique_slides/slide_021.jpg (adjudication.md):
    # black 0F0F0F, blue 0000CC, green 007A00, red CC0000
    K, B, G, R = "#0F0F0F", "#0000CC", "#007A00", "#CC0000"
    OJ = r"O_j(1\,-\,O_j)"
    compose([(r"\Delta_{ji} = \eta", K), (r"O_i", B), (OJ, G),
             (r"[\,\sum_k(\delta_k w_{kj})\,]", R)], "eq1c")
    compose([(r"\Delta_{ji} = \eta", K), (r"O_i", B), (r"\delta_j", K)], "eq2c")
    compose([(r"\mathrm{Where:}", K), (r"\delta_j = ", R), (OJ, G),
             (r"[\,\sum_k(\delta_k w_{kj})\,]", R)], "eq3c")
