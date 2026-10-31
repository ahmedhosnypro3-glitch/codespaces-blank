#!/usr/bin/env python3
"""Render the 2D math assets for slide_022 (rebuild wave 3) into eq_022/.

Each asset is one render_math.py row of "color:latex||color:latex" segments,
fit into its spec box budget at 600 dpi. Manifest maps name -> natural size.
"""
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
    "eq_top": (r"#000000:[a||#FF0000:{}^{T}||#0000FF:b||#000000:+1]^{2}", 16, 1.40, 0.42),
    "eq_vec": (r"#000000:\left[\underset{a_{2}\ \ b_{2}}{a_{1}\ \ b_{1}}\right]", 14, 1.12, 0.82),
    "eq_calc_ab": (r"#000000:\mathsf{Calculate}\ \ a||#FF0000:{}^{T}||#000000:b", 13, 2.30, 0.32),
    "eq_mat": (r"#000000:\left[a_{1}\ \ a_{2}\right]\ \left[\underset{b_{2}}{b_{1}}\right]", 12, 0.88, 0.62),
    "eq_map": (r"#000000:a,\ b\ \Rightarrow\ u,\ v", 13, 1.55, 0.30),
    "eq_6x2": (r"#000000:\left[\underset{\underset{\underset{\underset{\underset{1\ \vert\ 1}{\sqrt{2}a_{2}\ \vert\ \sqrt{2}b_{2}}}{\sqrt{2}a_{1}\ \vert\ \sqrt{2}b_{1}}}{\sqrt{2}a_{1}a_{2}\ \vert\ \sqrt{2}b_{1}b_{2}}}{a_{2}^{2}\ \vert\ b_{2}^{2}}}{a_{1}^{2}\ \vert\ b_{1}^{2}}\right]", 16, 1.95, 2.05),
    "eq_calc_uv": (r"#000000:\mathsf{Calculate}\ \ u||#FF0000:{}^{T}||#000000:v", 13, 2.20, 0.32),
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
