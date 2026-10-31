#!/usr/bin/env python3
"""Wave-3 fix round 2 mathtext PNGs for slide_007 (rb4 assets; rb3 banked untouched).

Fixes judge MAJORs: true stacked 2-D column vectors/matrices (row PNGs stacked
in JS with drawn brackets), panel-3 block sized to fit its panel, en-dash in
equation 3. Content from qa/reanalysis2/slide_007_analysis.txt only.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_007")
RENDER = os.path.join(HERE, "render_math.py")
SIZE = 14.0

ASSETS = [
    ("rb4_sum1", [r"#0000FF:\sum_{i=1}^{3} a_i||#FF0000:x_i||#000000:\,=\,||#0000FF:a_1||#FF0000:x_1||#000000:\,+\,||#0000FF:a_2||#FF0000:x_2||#000000:\,+\,||#0000FF:a_3||#FF0000:x_3||#000000:\,=\,Z"], 3.55, 0.69, 10),
    ("rb4_arrow", [r"#FF0000:\Longrightarrow"], 0.30, 0.20, 10),
    ("rb4_eq", [r"#000000:="], 0.25, 0.35, 10),
    ("rb4_p1_rowA", [r"#0000FF:\left[a_1\ \ a_2\ \ a_3\right]"], 0.95, 0.30, 10),
    ("rb4_x1", [r"#FF0000:x_1"], 0.30, 0.22, 10),
    ("rb4_x2", [r"#FF0000:x_2"], 0.30, 0.22, 10),
    ("rb4_x3", [r"#FF0000:x_3"], 0.30, 0.22, 10),
    ("rb4_p1_rhs", [r"#000000:=\,\left(z\right)||#FF0000:\,_{1*1}"], 1.00, 0.34, 10),
    ("rb4_sum_a", [r"#0000FF:\sum_{i=1}^{3} a_i||#FF0000:x_i||#000000:\,=\,Z_1"], 0.95, 0.85, 10),
    ("rb4_sum_b", [r"#FF00FF:\sum_{i=1}^{3} b_i||#FF0000:x_i||#000000:\,=\,Z_2"], 0.95, 0.85, 10),
    ("rb4_sum_c", [r"#008000:\sum_{i=1}^{3} c_i||#FF0000:x_i||#000000:\,=\,Z_3"], 0.95, 0.85, 10),
    ("rb4_r_a", [r"#0000FF:a_1\ \ a_2\ \ a_3"], 0.80, 0.26, 10),
    ("rb4_r_b", [r"#FF00FF:b_1\ \ b_2\ \ b_3"], 0.80, 0.26, 10),
    ("rb4_r_c", [r"#008000:c_1\ \ c_2\ \ c_3"], 0.80, 0.26, 10),
    ("rb4_Z1", [r"#000000:Z_1"], 0.30, 0.22, 10),
    ("rb4_Z2", [r"#000000:Z_2"], 0.30, 0.22, 10),
    ("rb4_Z3", [r"#000000:Z_3"], 0.30, 0.22, 10),
    ("rb4_ann31", [r"#FF0000:{}^{3*1}"], 0.50, 0.30, 10),
    ("rb4_p3_left", [r"#FF0000:x_1 + 2 x_2 = 7", r"#FF0000:3 x_1 + 4 x_2 = 12",
                     "#FF0000:3 x_3 \u2013 5 x_1 = 10", r"#FF0000:x_1 + x_2 + x_3 = 24"], 1.30, 1.18, 36),
    ("rb4_n1", [r"#000000:1\ \ 2\ \ 0"], 0.85, 0.22, 10),
    ("rb4_n2", [r"#000000:3\ \ 4\ \ 0"], 0.85, 0.22, 10),
    ("rb4_n3", [r"#000000:-5\ \ 0\ \ 3"], 0.85, 0.22, 10),
    ("rb4_n4", [r"#000000:1\ \ 1\ \ 1"], 0.85, 0.22, 10),
    ("rb4_ann43", [r"#FF0000:{}^{4*3}"], 0.50, 0.30, 10),
    ("rb4_v7", [r"#000000:7"], 0.30, 0.22, 10),
    ("rb4_v12", [r"#000000:12"], 0.30, 0.22, 10),
    ("rb4_v10", [r"#000000:10"], 0.30, 0.22, 10),
    ("rb4_v24", [r"#000000:24"], 0.30, 0.22, 10),
    ("rb4_ann41", [r"#FF0000:{}^{4*1}"], 0.50, 0.30, 10),
]


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, rows, maxw, maxh, rowgap in ASSETS:
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".rb4.json")
        cmd = [sys.executable, RENDER, "--out", out, "--size", str(SIZE),
               "--maxw", str(maxw), "--maxh", str(maxh), "--rowgap", str(rowgap),
               "--out-json", js]
        for r in rows:
            cmd += ["--row", r]
        subprocess.run(cmd, check=True, cwd=HERE)
        with open(js) as fh:
            info = json.load(fh)
        manifest[name] = {"image": name + ".png", "w_in": info["w_in"], "h_in": info["h_in"]}
        print(name, info["w_in"], "x", info["h_in"], "in")
    with open(os.path.join(EQDIR, "rb4_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
