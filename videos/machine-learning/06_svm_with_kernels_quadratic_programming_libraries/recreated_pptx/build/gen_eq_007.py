#!/usr/bin/env python3
"""Generate 600-dpi mathtext PNGs for slide 007 rebuild (wave 3).

Equations come ONLY from qa/reanalysis2/slide_007_analysis.txt section 8.
Assets land in build/eq_007/ as <name>.png + <name>.json sidecars + manifest.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_007")
RENDER = os.path.join(HERE, "render_math.py")
SIZE = 14.0

# name, render_math.py --row value, maxw_in, maxh_in
ASSETS = [
    ("sum1", r"#0000FF:\sum_{i=1}^{3} a_i x_i||#000000:= a_1 x_1 + a_2 x_2 + a_3 x_3 = Z", 3.56, 0.70),
    ("arrow", r"#FF0000:\Rightarrow", 0.30, 0.26),
    ("p1_row", r"#0000FF:\left[a_1\ \ a_2\ \ a_3\right]", 1.00, 0.55),
    ("vec_x", r"#FF0000:\left[\overset{x_1}{\overset{x_2}{x_3}}\right]", 0.60, 0.85),
    ("p1_rhs", r"#000000:= \left(z\right)", 0.90, 0.55),
    ("ann_1x1", r"#FF0000:1*1", 0.45, 0.30),
    ("sum_a", r"#0000FF:\sum_{i=1}^{3} a_i x_i||#000000:= Z_1", 0.95, 0.44),
    ("sum_b", r"#FF00FF:\sum_{i=1}^{3} b_i x_i||#000000:= Z_2", 0.95, 0.48),
    ("sum_c", r"#008000:\sum_{i=1}^{3} c_i x_i||#000000:= Z_3", 0.95, 0.49),
    ("r_a3", r"#0000FF:a_1\ \ a_2\ \ a_3", 0.85, 0.30),
    ("r_b3", r"#FF00FF:b_1\ \ b_2\ \ b_3", 0.85, 0.30),
    ("r_c3", r"#008000:c_1\ \ c_2\ \ c_3", 0.85, 0.30),
    ("eq_sign", r"#000000:=", 0.30, 0.40),
    ("z_vec3", r"#000000:\left[\overset{Z_1}{\overset{Z_2}{Z_3}}\right]", 0.55, 0.95),
    ("ann_3x1", r"#FF0000:3*1", 0.50, 0.30),
    ("e1", r"#FF0000:x_1 + 2 x_2 = 7", 1.22, 0.24),
    ("e2", r"#FF0000:3 x_1 + 4 x_2 = 12", 1.26, 0.24),
    ("e3", r"#FF0000:3 x_3 - 5 x_1 = 10", 1.26, 0.25),
    ("e4", r"#FF0000:x_1 + x_2 + x_3 = 24", 1.36, 0.33),
    ("n1", r"#000000:1\ \ 2\ \ 0", 0.90, 0.26),
    ("n2", r"#000000:3\ \ 4\ \ 0", 0.90, 0.26),
    ("n3", r"#000000:-5\ \ 0\ \ 3", 0.90, 0.26),
    ("n4", r"#000000:1\ \ 1\ \ 1", 0.90, 0.26),
    ("ann_4x3", r"#FF0000:4*3", 0.55, 0.30),
    ("rhs_vec4", r"#000000:\left[\overset{7}{\overset{12}{\overset{10}{24}}}\right]", 0.55, 1.10),
    ("ann_4x1", r"#FF0000:4*1", 0.55, 0.30),
]


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, row, maxw, maxh in ASSETS:
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".json")
        subprocess.run([
            sys.executable, RENDER,
            "--out", out, "--size", str(SIZE),
            "--maxw", str(maxw), "--maxh", str(maxh),
            "--row", row, "--out-json", js,
        ], check=True, cwd=HERE)
        with open(js) as fh:
            info = json.load(fh)
        manifest[name] = {
            "image": name + ".png",
            "w_in": info["w_in"], "h_in": info["h_in"],
            "pt": info["fontsize_pt"][0],
        }
        print(name, info["w_in"], "x", info["h_in"], "in @", info["fontsize_pt"][0], "pt")
    with open(os.path.join(EQDIR, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
