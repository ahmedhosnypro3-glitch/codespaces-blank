#!/usr/bin/env python3
"""Generate eq_028/*.png math assets for slide_028 via render_math.fit_row (600 dpi).

Colors per spec section 6: accent red #FF0033, accent blue #0000FF, body #000000.
Feature-map component order is the slide's printed order:
[x1^2, x2^2, sqrt2 x1x2, sqrt2 x1, sqrt2 x2, 1] (web SOURCES: keep slide order).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_math as rm
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_028")
os.makedirs(OUT, exist_ok=True)

R, B, K = "#FF0033", "#0000FF", "#000000"


def col(rows):
    """Stacked column rows[0] over rows[1] over ... via nested \\overset."""
    out = rows[-1]
    for r in reversed(rows[:-1]):
        out = "\\overset{%s}{%s}" % (r, out)
    return out

# name -> (row, base_pt, maxw_in, maxh_in); boxes = spec normalized regions in inches.
EQS = {
    # chip text [0.073,0.256,0.133,0.300]: "a^T b + 1" red
    "c_chip": (f"{R}:a^{{T}}b\\;+\\;1", 12, 0.78, 0.32),
    # [0.139,0.254,0.154,0.281]: superscript 2 + "=" black
    "c_sq": (f"{K}:^{{2}}\\;=", 12, 0.28, 0.24),
    # alpha row [0.154,0.178,0.367,0.207]: red horizontal row vector
    "c_arow": (f"{R}:\\left(\\alpha_1^{{2}}\\;\\;\\alpha_2^{{2}}\\;\\;\\sqrt{{2}}\\alpha_1\\alpha_2"
               f"\\;\\;\\sqrt{{2}}\\alpha_1\\;\\;\\sqrt{{2}}\\alpha_2\\;\\;1\\right)",
               12, 2.82, 0.21),
    # beta column [0.371,0.167,0.429,0.398]: blue stacked 6-row column
    "c_bcol": (B + ":\\left(" + col(["\\beta_1^{2}", "\\beta_2^{2}", "\\sqrt{2}\\beta_1\\beta_2",
               "\\sqrt{2}\\beta_1", "\\sqrt{2}\\beta_2", "1"]) + "\\right)^{T}",
               12, 0.77, 1.72),
    # [0.443,0.265,0.518,0.296]: "= phi(a)^T phi(b)" black
    "c_eq": (f"{K}:=\\;\\varphi(a)^{{T}}\\varphi(b)", 12, 0.99, 0.23),
    # Where block [0.550,0.250,0.651,0.302]: "Where: phi(x) = (x1/x2)^T"
    "c_where": (f"{K}:Where:\\;\\varphi(x)\\;=\\;\\left(\\overset{{x_1}}{{x_2}}\\right)^{{T}}",
                12, 1.34, 0.39),
    # red double arrow [0.690,0.267,0.704,0.291]
    "c_arrow": (f"{R}:\\Rightarrow", 12, 0.18, 0.17),
    # phi(x) 6-column [0.717,0.167,0.773,0.398], slide order x1^2,x2^2,sqrt2 x1x2,...
    "c_phicol": (K + ":\\left(" + col(["x_1^{2}", "x_2^{2}", "\\sqrt{2}x_1x_2",
                 "\\sqrt{2}x_1", "\\sqrt{2}x_2", "1"]) + "\\right)",
                 12, 0.74, 1.72),
    # a = (1/2)^T red [0.073,0.444,0.125,0.528]
    "l_a": ("||".join([f"{R}:a", f"{K}:\\;=\\;",
                       f"{R}:\\left(\\overset{{1}}{{2}}\\right)^{{T}}"]), 12, 0.69, 0.62),
    # b = (3/4)^T blue [0.146,0.444,0.200,0.528]
    "l_b": ("||".join([f"{B}:b", f"{K}:\\;=\\;",
                       f"{B}:\\left(\\overset{{3}}{{4}}\\right)^{{T}}"]), 12, 0.71, 0.62),
    # "phi(a)^T phi(b) =" black [0.073,0.615,0.169,0.652]
    "l_eq": (f"{K}:\\varphi(a)^{{T}}\\varphi(b)\\;=", 12, 1.27, 0.27),
    # red row [0.175,0.541,0.388,0.574]: 1^2 2^2 sqrt2 1*2 sqrt2 2sqrt2 1
    "l_row": (f"{R}:\\left(1^{{2}}\\;\\;2^{{2}}\\;\\;\\sqrt{{2}}\\,1*2\\;\\;\\sqrt{{2}}"
              f"\\;\\;2\\sqrt{{2}}\\;\\;1\\right)", 12, 2.82, 0.24),
    # blue column [0.394,0.537,0.460,0.737]: 3^2 4^2 sqrt2 3*4 3sqrt2 4sqrt2 1
    "l_bcol": (B + ":\\left(" + col(["3^{2}", "4^{2}", "\\sqrt{2}\\,3*4",
               "3\\sqrt{2}", "4\\sqrt{2}", "1"]) + "\\right)",
               12, 0.87, 1.49),
    # "=" + red product row [0.479,0.587,0.627,0.617]: 1 4 2sqrt2 sqrt2 2sqrt2 1
    "l_prod": ("||".join([f"{K}:=\\;",
                          f"{R}:\\left(1\\;\\;4\\;\\;2\\sqrt{{2}}\\;\\;\\sqrt{{2}}"
                          f"\\;\\;2\\sqrt{{2}}\\;\\;1\\right)"]), 12, 1.96, 0.22),
    # blue numeric column [0.654,0.533,0.710,0.741]: 9 16 12sqrt2 3sqrt2 4sqrt2 1
    "l_numcol": (B + ":\\left(" + col(["9", "16", "12\\sqrt{2}", "3\\sqrt{2}",
                 "4\\sqrt{2}", "1"]) + "\\right)",
                 12, 0.74, 1.52),
    # sum line [0.461,0.746,0.652,0.778]: = 9+64+48+6+16+1 = 144
    "l_sum": (f"{K}:=\\;9+64+48+6+16+1\\;=\\;144", 12, 2.54, 0.23),
    # bottom line [0.073,0.787,0.346,0.824]: |a^Tb+1|^2 = (1+3+2*4+1)^2 = 12^2 = 144
    "l_bot": ("||".join([
        f"{K}:|\\;", f"{R}:a^{{T}}", f"{B}:b\\;+\\;1",
        f"{K}:\\;|^{{2}}\\;=\\;(1+3+2*4+1)^{{2}}\\;=\\;12^{{2}}\\;=\\;144",
    ]), 12, 3.62, 0.27),
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
