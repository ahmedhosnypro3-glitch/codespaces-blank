#!/usr/bin/env python3
"""Generate eq_026/*.png math assets for slide_026 via render_math.fit_row (600 dpi)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_math as rm
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_026")
os.makedirs(OUT, exist_ok=True)

R, B, K = "#C00000", "#0026CC", "#1A1A1A"
# name -> (row segments joined by ||, size_pt, maxw_in, maxh_in)
EQS = {
    "eq1_a": (f"{R}:a||{K}:\\;=\\;||{R}:\\left[\\overset{{a_1}}{{a_2}}\\right]^{{T}}", 12, 0.66, 0.50),
    "eq2_b": (f"{B}:b||{K}:\\;=\\;||{B}:\\left[\\overset{{b_1}}{{b_2}}\\right]^{{T}}", 12, 0.66, 0.50),
    "eq3_chain": ("||".join([
        f"{R}:(a^{{T}}", f"{B}:b)^{{2}}", f"{K}:\\;=\\;",
        f"{R}:[a_1\\;\\;a_2", f"{K}:\\;|\\;",
        f"{B}:b_1\\;\\;b_2]^{{2}}", f"{K}:\\;=\\;(",
        f"{R}:a_1", f"{B}:b_1", f"{K}:\\;+\\;", f"{R}:a_2", f"{B}:b_2",
        f"{K}:)^{{2}}\\;=\\;", f"{R}:a_1^{{2}}", f"{B}:b_1^{{2}}",
        f"{K}:\\;+\\;", f"{R}:a_2^{{2}}", f"{B}:b_2^{{2}}", f"{K}:\\;+\\;2",
        f"{R}:a_1", f"{B}:b_1", f"{R}:a_2", f"{B}:b_2",
    ]), 12, 6.70, 0.55),
    "eq4_phi": ("||".join([
        f"{R}:[a^{{T}}", f"{B}:b]^{{2}}", f"{K}:\\;=\\;( ",
        f"{R}:\\left[\\overset{{a_1^{{2}}}}{{\\overset{{a_2^{{2}}}}{{\\sqrt{{2}}\\,a_1a_2}}}}\\right]",
        f"{K}:\\;|\\;",
        f"{B}:\\left[\\overset{{b_1^{{2}}}}{{\\overset{{b_2^{{2}}}}{{\\sqrt{{2}}\\,b_1b_2}}}}\\right]",
        f"{K}: )\\;=\\;\\varphi(a)^{{T}}\\varphi(b)",
    ]), 12, 4.70, 1.12),
    "eq5_where": ("||".join([
        f"{K}:Where:\\;\\varphi(x)\\;=\\;",
        f"{K}:\\left[\\overset{{x_1}}{{x_2}}\\right]^{{T}}",
        f"{R}:\\;\\Rightarrow\\;",
        f"{K}:\\left[\\overset{{x_1^{{2}}}}{{\\overset{{x_2^{{2}}}}{{\\sqrt{{2}}\\,x_1x_2}}}}\\right]^{{T}}",
    ]), 12, 3.60, 1.15),
    "eq6_cap": (f"{R}:2D\\;\\Rightarrow\\;3D", 12, 1.10, 0.22),
    "eq7_a": (f"{R}:a||{K}:\\;=\\;||{R}:\\left[\\overset{{1}}{{2}}\\right]^{{T}}", 12, 0.72, 0.58),
    "eq8_b": (f"{B}:b||{K}:\\;=\\;||{B}:\\left[\\overset{{3}}{{4}}\\right]", 12, 0.70, 0.58),
    "eq9_num": ("||".join([
        f"{K}:\\varphi(a)^{{T}}\\varphi(b)\\;=\\;( ",
        f"{R}:\\left[\\overset{{1^{{2}}}}{{\\overset{{2^{{2}}}}{{\\sqrt{{2}}\\,1*2}}}}\\right]",
        f"{K}:\\;|\\;",
        f"{B}:\\left[\\overset{{3^{{2}}}}{{\\overset{{4^{{2}}}}{{\\sqrt{{2}}\\,2*4}}}}\\right]",
        f"{K}: )\\;=\\;( ",
        f"{R}:\\left[\\overset{{1}}{{\\overset{{4}}{{\\sqrt{{2}}\\,2}}}}\\right]",
        f"{K}:\\;|\\;",
        f"{B}:\\left[\\overset{{9}}{{\\overset{{16}}{{\\sqrt{{2}}\\,12}}}}\\right]",
        f"{K}: )\\;=\\;9+64+48=121",
    ]), 12, 6.15, 0.80),
    "eq10_sq": (f"{R}:[a^{{T}}b]^{{2}}||{K}:\\;=\\;(1*3+2*4)^{{2}}\\;=\\;11^{{2}}\\;=\\;121",
                12, 3.15, 0.36),
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
