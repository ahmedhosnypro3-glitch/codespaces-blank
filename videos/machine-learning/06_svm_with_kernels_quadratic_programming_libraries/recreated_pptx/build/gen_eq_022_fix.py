#!/usr/bin/env python3
"""Regenerate eq_022 math assets with attached superscripts and clean 6-row
column stacks (fix for garbled [a^T b+1]^2 and missing matrix rows)."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_022")
RENDER = os.path.join(HERE, "render_math.py")

COL_A = (r"\left[\underset{\underset{\underset{\underset{\underset{1}{\sqrt{2}a_{2}}}"
         r"{\sqrt{2}a_{1}}}{\sqrt{2}a_{1}a_{2}}}{a_{2}^{2}}}{a_{1}^{2}}\right]")
COL_B = (r"\left[\underset{\underset{\underset{\underset{\underset{1}{\sqrt{2}b_{2}}}"
         r"{\sqrt{2}b_{1}}}{\sqrt{2}b_{1}b_{2}}}{b_{2}^{2}}}{b_{1}^{2}}\right]")

ASSETS = {
    # name: (row, size_pt, maxw_in, maxh_in)
    "eq_top": (r"#FF0000:[a^{T}" + r"||#0000FF:b+1]^{2}", 16, 1.40, 0.42),
    "eq_vec": (r"#FF0000:\left[\underset{a_{2}}{a_{1}}\right]" + r"||#0000FF:\ \left[\underset{b_{2}}{b_{1}}\right]", 14, 1.12, 0.82),
    "eq_calc_ab": (r"#000000:\mathsf{Calculate}\ " + r"||#FF0000:a^{T}" + r"||#0000FF:b", 13, 2.30, 0.32),
    "eq_mat": (r"#FF0000:\left[a_{1}\ \ a_{2}\right]" + r"||#0000FF:\ \left[\underset{b_{2}}{b_{1}}\right]", 12, 0.88, 0.62),
    "eq_map": (r"#FF0000:a\ \Rightarrow\ u," + r"||#0000FF:\ b\ \Rightarrow\ v", 13, 1.55, 0.30),
    "eq_colL": (r"#FF0000:" + COL_A, 16, 0.95, 2.00),
    "eq_colR": (r"#0000FF:" + COL_B, 16, 0.95, 2.00),
    "eq_calc_uv": (r"#000000:\mathsf{Calculate}\ " + r"||#FF0000:u^{T}" + r"||#0000FF:v", 13, 2.20, 0.32),
    "eq_rowcol": (r"#FF0000:\left[a_{1}^{2}\ a_{2}^{2}\ \sqrt{2}a_{1}a_{2}\ \sqrt{2}a_{1}\ \sqrt{2}a_{2}\ 1\right]"
                  + r"||#000000:\ \vert\ "
                  + r"||#0000FF:" + COL_B, 18, 3.70, 1.00),
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
