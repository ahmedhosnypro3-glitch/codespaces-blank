#!/usr/bin/env python3
"""R2 render of slide_022 math assets into eq_022/ (single-segment mathtext so
superscripts/transposes stay attached; 6-D matrix as two aligned column PNGs)."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_022")
os.makedirs(OUT, exist_ok=True)
RENDER = os.path.join(HERE, "render_math.py")

ASSETS = {
    # name: (row, size_pt, maxw_in, maxh_in)
    "eq_top": (r"#000000:\left[a^{T}b+1\right]^{2}", 16, 1.40, 0.45),
    "eq_vec": (r"#000000:\left[\underset{a_{2}\ \ b_{2}}{a_{1}\ \ b_{1}}\right]", 14, 1.12, 0.82),
    "eq_calc_ab": (r"#000000:\mathrm{Calculate}\ a^{T}b", 13, 1.15, 0.32),
    "eq_mat": (r"#000000:\left[a_{1}\ \ a_{2}\right]\ \left[\underset{b_{2}}{b_{1}}\right]", 12, 0.88, 0.62),
    "eq_map": (r"#000000:a,\ b\ \Rightarrow\ u,\ v", 13, 1.55, 0.30),
    "eq_colL": (r"#000000:\left[\underset{\underset{\underset{\underset{\underset{1}{\sqrt{2}a_{2}}}{\sqrt{2}a_{1}}}{\sqrt{2}a_{1}a_{2}}}{a_{2}^{2}}}{a_{1}^{2}}\right]", 14, 0.95, 2.0),
    "eq_colR": (r"#000000:\left[\underset{\underset{\underset{\underset{\underset{1}{\sqrt{2}b_{2}}}{\sqrt{2}b_{1}}}{\sqrt{2}b_{1}b_{2}}}{b_{2}^{2}}}{b_{1}^{2}}\right]", 14, 0.95, 2.0),
    "eq_calc_uv": (r"#000000:\mathrm{Calculate}\ u^{T}v", 13, 1.15, 0.32),
    "eq_rowcol": (r"#000000:\left[a_{1}^{2}\ a_{2}^{2}\ \sqrt{2}a_{1}a_{2}\ \sqrt{2}a_{1}\ \sqrt{2}a_{2}\ 1\right]\ \vert\ \left[\underset{\underset{\underset{\underset{\underset{1}{\sqrt{2}b_{2}}}{\sqrt{2}b_{1}}}{\sqrt{2}b_{1}b_{2}}}{b_{2}^{2}}}{b_{1}^{2}}\right]", 18, 3.75, 2.05),
}

manifest = {}
for name, (row, size, maxw, maxh) in ASSETS.items():
    png = os.path.join(OUT, name + ".png")
    js = os.path.join(OUT, name + ".json")
    subprocess.run([sys.executable, RENDER, "--out", png, "--out-json", js,
                    "--size", str(size), "--maxw", str(maxw), "--maxh", str(maxh),
                    "--row", row], check=True, capture_output=True, text=True)
    with open(js) as fh:
        info = json.load(fh)
    manifest[name] = {"path": png, "w_in": info["w_in"], "h_in": info["h_in"],
                      "w_px": info["w_px"], "h_px": info["h_px"]}
    print(name, info["w_in"], "x", info["h_in"])

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
