#!/usr/bin/env python3
"""Wave-3 rebuild fix 1: eq_025/*_rb3b.png — larger, taller equation assets.

Fix for judge FAIL (equations at ~25-30% of original scale): re-rendered with
\substack column vectors, larger point sizes, and boxes fit to the original
ink extents measured in qa/rejudge2/orig_png/slide_025.png.
Rows: "color:latex" segments joined by "||". Colors per spec section 6.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_math as rm
import numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_025")
os.makedirs(OUT, exist_ok=True)

R, B, K = "#CC0000", "#0033CC", "#000000"

EQS = {
    # E1 [0.071,0.161,0.198,0.243]: a = (a1/a2)  b = (b1/b2), stacked columns, tight gap
    "e1": ("||".join([
        f"{R}:a", f"{K}:\\;=\\;", f"{R}:\\left(\\substack{{a_1\\\\a_2}}\\right)",
        f"{K}:\\;\\;", f"{B}:b", f"{K}:\\;=\\;",
        f"{B}:\\left(\\substack{{b_1\\\\b_2}}\\right)",
    ]), 16, 2.50, 0.62),
    # E2 [0.069,0.259,0.521,0.363]: a^T b = [a1 a2 | b1/b2]^{12} = (a1b1+a2b2)^2 = ...
    "e2": ("||".join([
        f"{R}:a^{{T}}", f"{B}:b", f"{K}:\\;=\\;",
        f"{R}:[\\;a_1\\;\\;a_2", f"{K}:\\;|\\;",
        f"{B}:\\substack{{b_1\\\\b_2}}\\;]^{{12}}",
        f"{K}:\\;=\\;(",
        f"{R}:a_1", f"{B}:b_1", f"{K}:\\;+\\;", f"{R}:a_2", f"{B}:b_2",
        f"{K}:)^{{2}}\\;=\\;",
        f"{R}:a_1^{{2}}", f"{B}:b_1^{{2}}", f"{K}:\\;+\\;",
        f"{R}:a_2^{{2}}", f"{B}:b_2^{{2}}", f"{K}:\\;+\\;2\\;",
        f"{R}:a_1", f"{B}:b_1", f"{R}:a_2", f"{B}:b_2",
    ]), 16, 6.00, 0.75),
    # E3 [0.069,0.380,0.458,0.541]: [a^T b]^2 = [a1^2 a2^2 sqrt2 a1a2 | 3-row b col] = phi(a)^T phi(b)
    "e3": ("||".join([
        f"{K}:[", f"{R}:a^{{T}}", f"{B}:b", f"{K}:]^{{2}}\\;=\\;",
        f"{K}:[\\;", f"{R}:a_1^{{2}}\\;\\;a_2^{{2}}\\;\\;\\sqrt{{2}}\\,a_1a_2",
        f"{K}:\\;|\\;",
        f"{B}:\\substack{{b_1^{{2}}\\\\b_2^{{2}}\\\\sqrt{{2}}\\,b_1b_2}}",
        f"{K}:\\;]\\;=\\;",
        f"{K}:\\varphi(a)^{{T}}", f"{B}:\\varphi(b)",
    ]), 16, 5.00, 1.10),
    # E4 [0.513,0.374,0.783,0.520]: Where: phi(x) =def (x1/x2) => (3-row col)^T
    "e4": ("||".join([
        f"{K}:Where:\\;\\varphi(x)\\;\\equiv\\;",
        f"{K}:\\left(\\substack{{x_1\\\\x_2}}\\right)",
        f"{R}:\\;\\Rightarrow\\;",
        f"{K}:\\left(\\substack{{x_1^{{2}}\\\\x_2^{{2}}\\\\sqrt{{2}}\\,x_1x_2}}\\right)^{{T}}",
    ]), 16, 3.20, 1.00),
    # E5 [0.644,0.520,0.732,0.550]: bold red "2D => 3D"
    "e5": (f"{R}:\\mathbf{{2D\\;\\Rightarrow\\;3D}}", 16, 1.00, 0.22),
}

def fit_tight(row, size, maxw, maxh, min_size=6.0):
    """Render at 600 dpi on a generously sized figure (no clipping), crop to
    ink, and shrink the point size until the ink fits maxw x maxh."""
    pt = size
    for _ in range(12):
        canvas = rm.render_row(row, pt)  # no need hints -> big figure
        alpha = canvas[:, :, 3] > 0
        rows = np.where(alpha.any(axis=1))[0]
        cols = np.where(alpha.any(axis=0))[0]
        pad = 6
        r0, r1 = max(rows.min() - pad, 0), min(rows.max() + pad + 1, canvas.shape[0])
        c0, c1 = max(cols.min() - pad, 0), min(cols.max() + pad + 1, canvas.shape[1])
        canvas = canvas[r0:r1, c0:c1]
        w_in, h_in = canvas.shape[1] / rm.DPI, canvas.shape[0] / rm.DPI
        if w_in <= maxw and h_in <= maxh:
            break
        pt = max(min_size, pt * 0.94)
    return canvas, pt

manifest = {}
for name, (row, size, maxw, maxh) in EQS.items():
    canvas, pt = fit_tight(row, size, maxw, maxh)
    fn = f"{name}_rb3b.png"
    Image.fromarray(canvas).save(os.path.join(OUT, fn))
    manifest[name] = {
        "file": fn, "path": os.path.join(OUT, fn),
        "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
        "w_in": round(canvas.shape[1] / rm.DPI, 5), "h_in": round(canvas.shape[0] / rm.DPI, 5),
        "pt": round(pt, 2),
    }
    print(name, manifest[name]["w_in"], manifest[name]["h_in"], manifest[name]["pt"])

with open(os.path.join(OUT, "manifest_rb3b.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
