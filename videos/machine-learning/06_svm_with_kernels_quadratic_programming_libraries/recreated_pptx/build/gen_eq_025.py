#!/usr/bin/env python3
"""Generate eq_025/*.png math assets for slide_025 via render_math.fit_row (600 dpi).

Rows are "color:latex" segments joined by "||"; colors per spec section 6:
a-side #CC0000, b-side #0033CC, operators/brackets #000000, arrows #CC0000.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_math as rm
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_025")
os.makedirs(OUT, exist_ok=True)

R, B, K = "#CC0000", "#0033CC", "#000000"

# name -> (row, base_pt, maxw_in, maxh_in) — boxes are the spec's normalized
# regions converted to inches (x*13.33, y*7.5, w=(x1-x0)*13.33, h=(y1-y0)*7.5).
EQS = {
    # E1 [0.071,0.161,0.198,0.243]: a = (a1/a2)   b = (b1/b2), stacked columns
    "e1": ("||".join([
        f"{R}:a", f"{K}:\\;=\\;", f"{R}:\\left(\\overset{{a_1}}{{a_2}}\\right)",
        f"{K}:\\;\\;\\;\\;", f"{B}:b", f"{K}:\\;=\\;",
        f"{B}:\\left(\\overset{{b_1}}{{b_2}}\\right)",
    ]), 12, 1.69, 0.61),
    # E2 [0.069,0.259,0.521,0.363]: a^T b = [a1 a2 | b1/b2]^2 = (a1b1+a2b2)^2 = ...
    "e2": ("||".join([
        f"{R}:a^{{T}}", f"{B}:b", f"{K}:\\;=\\;",
        f"{R}:[\\;a_1\\;\\;a_2", f"{K}:\\;|\\;",
        f"{B}:\\overset{{b_1}}{{b_2}}\\;]^{{2}}",
        f"{K}:\\;=\\;(",
        f"{R}:a_1", f"{B}:b_1", f"{K}:\\;+\\;", f"{R}:a_2", f"{B}:b_2",
        f"{K}:)^{{2}}\\;=\\;",
        f"{R}:a_1^{{2}}", f"{B}:b_1^{{2}}", f"{K}:\\;+\\;",
        f"{R}:a_2^{{2}}", f"{B}:b_2^{{2}}", f"{K}:\\;+\\;2\\;",
        f"{R}:a_1", f"{B}:b_1", f"{R}:a_2", f"{B}:b_2",
    ]), 12, 6.00, 0.77),
    # E3 [0.069,0.380,0.458,0.541]: [a^T b]^2 = [a1^2 a2^2 sqrt2 a1a2 | b-col] = phi(a)^T phi(b)
    "e3": ("||".join([
        f"{K}:[", f"{R}:a^{{T}}", f"{B}:b", f"{K}:]^{{2}}\\;=\\;",
        f"{K}:[\\;", f"{R}:a_1^{{2}}\\;\\;a_2^{{2}}\\;\\;\\sqrt{{2}}\\,a_1a_2",
        f"{K}:\\;|\\;",
        f"{B}:\\overset{{b_1^{{2}}}}{{\\overset{{b_2^{{2}}}}{{\\sqrt{{2}}\\,b_1b_2}}}}",
        f"{K}:\\;]\\;=\\;",
        f"{K}:\\varphi(a)^{{T}}", f"{B}:\\varphi(b)",
    ]), 12, 5.15, 1.20),
    # E4 [0.513,0.374,0.783,0.520]: Where: phi(x) = (x1/x2)^T => (x1^2/x2^2/sqrt2 x1x2)^T
    "e4": ("||".join([
        f"{K}:Where:\\;\\varphi(x)\\;=\\;",
        f"{K}:\\left(\\overset{{x_1}}{{x_2}}\\right)^{{T}}",
        f"{R}:\\;\\Rightarrow\\;",
        f"{K}:\\left(\\overset{{x_1^{{2}}}}{{\\overset{{x_2^{{2}}}}{{\\sqrt{{2}}\\,x_1x_2}}}}\\right)^{{T}}",
    ]), 12, 3.58, 1.08),
    # E5 [0.644,0.520,0.732,0.550]: bare red caption "2D => 3D"
    "e5": (f"{R}:2D\\;\\Rightarrow\\;3D", 12, 1.17, 0.22),
}

manifest = {}
for name, (row, size, maxw, maxh) in EQS.items():
    canvas, pt = rm.fit_row(row, size, maxw, maxh)
    fn = f"{name}.png"
    Image.fromarray(canvas).save(os.path.join(OUT, fn))
    manifest[name] = {
        "file": fn, "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
        "w_in": round(canvas.shape[1] / rm.DPI, 5), "h_in": round(canvas.shape[0] / rm.DPI, 5),
        "pt": round(pt, 2),
    }
    print(name, manifest[name]["w_in"], manifest[name]["h_in"], manifest[name]["pt"])

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
