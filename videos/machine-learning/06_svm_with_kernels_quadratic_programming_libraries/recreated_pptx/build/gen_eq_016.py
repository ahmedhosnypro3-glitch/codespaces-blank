#!/usr/bin/env python3
"""Generate eq_016/*.png math assets for slide_016 via render_math.fit_row (600 dpi)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["MATHTEXT_FONTSET"] = "dejavusans"
import render_math as rm
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_016")
os.makedirs(OUT, exist_ok=True)

BLUE, RED = "#1F49C7", "#C00000"
# name -> (row segments joined by ||, size_pt, maxw_in, maxh_in)
EQS = {
    # x |-> phi(x) = [ x ; x^2 ] as a true 2-D column vector (brackets span both rows)
    "eq_map": (f"{BLUE}:x\\;\\Rightarrow\\;\\varphi(x)\\;=\\;"
               f"\\left[\\overset{{x}}{{x^{{2}}}}\\right]", 16, 1.95, 0.60),
    "eq_x2": (f"{RED}:x^{{2}}", 22, 0.55, 0.45),
    "eq_x": (f"{RED}:x", 22, 0.35, 0.45),
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
