#!/usr/bin/env python3
"""Render the 2D (professional-format) math assets for slides 018-022.

Writes PNGs into build/assets/eq/ plus build/assets/eq/manifest.json
mapping asset name -> {w_in, h_in} for pptxgenjs addImage placement.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from render_math import render_row, PAD_PX

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "assets", "eq")
DPI = 600
MIN_SIZE = 7.0

# name -> (latex string, color, requested pt size, max width in, max height in)
# Multi-segment rows use "color:latex||color:latex"; color None = already inline.
EQS = {
    "eq18_z":   (r"Z = \left(\underset{y}{x}\right)", "1A1A2E", 20, 1.85, 1.5),
    "eq18_phi": (r"\left(\underset{\sqrt{2}xy}{\underset{y^{2}}{x^{2}}}\right)", "1A1A2E", 16, 1.65, 2.0),
    "eq19_main": (r"#E74C3C:a^{T}b||#1ABC9C:\ \Rightarrow\ ||#27AE60:\mathsf{map\ to}\ \phi(a)\ \mathsf{and}\ \phi(b)||#1ABC9C:\ \Rightarrow\ ||#27AE60:\phi(a)^{T}\phi(b)||#2C3E50:\ \equiv\ ||#E74C3C:\mathbf{K}(a,b)", None, 22, 11.3, 0.8),
    "eq20_mtx_t": (r"\left[\underset{b_{1}\ \ b_{2}}{a_{1}\ \ a_{2}}\right]", "2C3E50", 13, 1.36, 0.95),
    "eq20_mtx_b": (r"\left[\underset{b_{1}\ \ b_{2}}{a_{1}\ \ a_{2}}\right]", "2C3E50", 13, 1.36, 0.95),
    "eq20_mtx2":  (r"\left[\underset{b_{1}\ \ b_{2}}{a_{1}\ \ a_{2}}\right]", "2C3E50", 12, 2.1, 0.75),
    "eq20_calc_a": (r"\mathsf{Calculate}\ a^{T}b", "2C3E50", 14, 4.7, 0.4),
    "eq20_calc_u": (r"\mathsf{Calculate}\ u^{T}v", "2C3E50", 13, 5.0, 0.35),
    "eq20_map":  (r"a, b \rightarrow u, v", "2C3E50", 11, 1.55, 0.32),
    "eq20_uv_map": (r"\left[\underset{a_{2}\ \ b_{2}}{a_{1}\ \ b_{1}}\right]", "8E44AD", 10, 1.5, 0.55),
    "eq20_uv_mtx": (r"\left(\underset{u_{m}\ \ v_{m}}{\underset{\vdots\ \ \vdots}{\underset{u_{2}\ \ v_{2}}{u_{1}\ \ v_{1}}}}\right)", "8E44AD", 11, 1.6, 1.4),
    "eq20_u_row": (r"u_{1}\ u_{2}\ \cdots\ u_{m}", "2C3E50", 12, 4.8, 0.3),
    "eq20_v_row": (r"v_{1}\ v_{2}\ \cdots\ v_{m}", "2C3E50", 12, 4.8, 0.3),
    "eq21_title": (r"\left[a^{T}b\right]^{2}", "FFFFFF", 22, 7.0, 0.5),
    "eq21_lab1": (r"a_{1}, b_{1}", "FFFFFF", 13, 1.3, 0.45),
    "eq21_lab2": (r"a_{2}, b_{2}", "FFFFFF", 13, 1.3, 0.45),
    "eq21_mtx":  (r"\left[\underset{b_{2}}{a_{1}\ \ a_{2}\ \ b_{1}}\right]", "2C3E50", 13, 2.8, 0.9),
    "eq21_sq":   (r"\left[a^{T}b\right]^{2}", "E74C3C", 16, 2.8, 0.45),
    "eq21_uv":   (r"\left[\underset{a_{2}^{2}\ \ b_{2}^{2}}{\sqrt{2}a_{1}a_{2}\ \ \sqrt{2}b_{1}b_{2}}\right]", "8E44AD", 12, 2.8, 1.4),
    "eq21_6d":   (r"\left[a_{1}^{2}, a_{2}^{2}, \sqrt{2}a_{1}a_{2}, \sqrt{2}a_{1}, \sqrt{2}a_{2}, b_{1}^{2}, b_{2}^{2}\right]", "2C3E50", 11, 4.6, 1.6),
    "eq22_title": (r"\left[a^{T}b + 1\right]^{2}", "E74C3C", 22, 7.0, 0.5),
    "eq22_lab1": (r"a_{1}, b_{1}", "2C3E50", 13, 1.5, 0.4),
    "eq22_lab2": (r"a_{2}, b_{2}", "2C3E50", 13, 1.5, 0.4),
    "eq22_mtx":  (r"\left[\underset{b_{1}\ \ b_{2}}{a_{1}\ \ a_{2}}\right]", "2C3E50", 14, 1.6, 1.3),
    "eq22_col_a": (r"\left(\underset{1}{\underset{\ldots}{a_{1}^{2}}}\right)", "8E44AD", 12, 1.2, 1.3),
    "eq22_col_b": (r"\left(\underset{1}{\underset{\ldots}{b_{1}^{2}}}\right)", "8E44AD", 12, 1.2, 1.3),
    "eq22_6d":   (r"\left[a_{1}^{2}, a_{2}^{2}, \sqrt{2}a_{1}a_{2}, \sqrt{2}a_{1}, \sqrt{2}a_{2}, 1\right]", "2C3E50", 11, 5.0, 1.3),
    "eq22_b6":   (r"\left(\underset{1}{\underset{\sqrt{2}b_{2}}{\underset{\sqrt{2}b_{1}}{\underset{\sqrt{2}b_{1}b_{2}}{\underset{b_{2}^{2}}{b_{1}^{2}}}}}}\right)", "2C3E50", 11, 1.0, 3.3),
    "eq22_norm_a": (r"\mathbf{\mathsf{Normal\ Model}}\ \mathsf{—}\ \mathbf{\mathsf{Calculate}}\ a^{T}b", "E74C3C", 13, 2.6, 0.4),
    "eq22_kern_u": (r"\mathbf{\mathsf{Kernelized\ Model}}\ \mathsf{—}\ \mathbf{\mathsf{Calculate}}\ u^{T}v", "E74C3C", 13, 5.8, 0.4),
    "eq21_norm_a": (r"\mathbf{\mathsf{Normal\ Model}}\ \mathsf{—}\ \mathbf{\mathsf{Calculate}}\ a^{T}b", "E74C3C", 14, 5.6, 0.4),
    "eq21_kern_u": (r"\mathbf{\mathsf{Kernelized\ Model}}\ \mathsf{—}\ \mathbf{\mathsf{Calculate}}\ u^{T}v", "E74C3C", 14, 5.6, 0.4),
    "eq21_map":   (r"\mathsf{Vectors\ Mapping}\ a, b \rightarrow u, v", "FFFFFF", 11, 2.8, 0.45),
}


def fit(name, spec):
    latex, color, size, max_w, max_h = spec
    row = latex if color is None else f"#{color}:{latex}"
    pt = size
    while pt >= MIN_SIZE:
        canvas = render_row(row, pt)
        w_in = canvas.shape[1] / DPI
        h_in = canvas.shape[0] / DPI
        if w_in <= max_w and h_in <= max_h:
            return canvas, pt, w_in, h_in
        pt -= 0.5
    canvas = render_row(row, MIN_SIZE)
    return canvas, MIN_SIZE, canvas.shape[1] / DPI, canvas.shape[0] / DPI


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = {}
    for name, spec in EQS.items():
        canvas, pt, w_in, h_in = fit(name, spec)
        path = os.path.join(OUT_DIR, f"{name}.png")
        Image.fromarray(canvas).save(path)
        manifest[name] = {"path": path, "w_in": round(w_in, 4),
                          "h_in": round(h_in, 4), "fontsize_pt": pt}
        print(f"{name}: {w_in:.2f} x {h_in:.2f} in @ {pt}pt")
    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    print("wrote manifest.json")


if __name__ == "__main__":
    main()
