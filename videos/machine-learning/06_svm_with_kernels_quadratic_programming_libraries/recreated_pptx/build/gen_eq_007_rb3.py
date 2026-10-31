#!/usr/bin/env python3
"""Fresh 600-dpi mathtext PNGs for the slide_007 wave-3 rebuild.

Content comes ONLY from qa/reanalysis2/slide_007_analysis.txt (sections 2/8).
Assets land in build/eq_007/rb3_*.png + rb3_manifest.json (old dump assets
left untouched).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_007")
RENDER = os.path.join(HERE, "render_math.py")
SIZE = 14.0

# name, rows, maxw_in, maxh_in, rowgap_px
ASSETS = [
    ("rb3_sum1", [r"#0000FF:\sum_{i=1}^{3} a_i||#FF0000:x_i||#000000:\,=\,||#0000FF:a_1||#FF0000:x_1||#000000:\,+\,||#0000FF:a_2||#FF0000:x_2||#000000:\,+\,||#0000FF:a_3||#FF0000:x_3||#000000:\,=\,Z"], 3.55, 0.69, 10),
    ("rb3_arrow", [r"#FF0000:\Rightarrow"], 0.26, 0.23, 10),
    ("rb3_p1_rowA", [r"#0000FF:\left[a_1\ \ a_2\ \ a_3\right]"], 1.05, 0.60, 10),
    ("rb3_p1_vecX", [r"#FF0000:\left[\overset{x_1}{\overset{x_2}{x_3}}\right]"], 0.78, 0.84, 10),
    ("rb3_p1_rhs", [r"#000000:=\left(z\right)||#FF0000:_{1*1}"], 1.20, 0.60, 10),
    ("rb3_sum_a", [r"#0000FF:\sum_{i=1}^{3} a_i||#FF0000:x_i||#000000:\,=\,Z_1"], 0.95, 0.44, 10),
    ("rb3_sum_b", [r"#FF00FF:\sum_{i=1}^{3} b_i||#FF0000:x_i||#000000:\,=\,Z_2"], 0.95, 0.48, 10),
    ("rb3_sum_c", [r"#008000:\sum_{i=1}^{3} c_i||#FF0000:x_i||#000000:\,=\,Z_3"], 0.95, 0.49, 10),
    ("rb3_r_a", [r"#0000FF:a_1\ \ a_2\ \ a_3"], 0.80, 0.30, 10),
    ("rb3_r_b", [r"#FF00FF:b_1\ \ b_2\ \ b_3"], 0.80, 0.30, 10),
    ("rb3_r_c", [r"#008000:c_1\ \ c_2\ \ c_3"], 0.80, 0.30, 10),
    ("rb3_eq", [r"#000000:="], 0.25, 0.35, 10),
    ("rb3_p2_vecX", [r"#FF0000:\left[\overset{x_1}{\overset{x_2}{x_3}}\right]"], 0.78, 0.93, 10),
    ("rb3_p2_rhs", [r"#000000:=\left[\overset{Z_1}{\overset{Z_2}{Z_3}}\right]||#FF0000:^{3*1}"], 1.30, 0.93, 10),
    ("rb3_p3_left", [r"#FF0000:x_1 + 2 x_2 = 7", r"#FF0000:3 x_1 + 4 x_2 = 12",
                      r"#FF0000:3 x_3 - 5 x_1 = 10", r"#FF0000:x_1 + x_2 + x_3 = 24"], 1.35, 1.20, 40),
    ("rb3_n1", [r"#000000:1\ \ 2\ \ 0"], 0.85, 0.27, 10),
    ("rb3_n2", [r"#000000:3\ \ 4\ \ 0"], 0.85, 0.27, 10),
    ("rb3_n3", [r"#000000:-5\ \ 0\ \ 3"], 0.85, 0.27, 10),
    ("rb3_n4", [r"#000000:1\ \ 1\ \ 1"], 0.85, 0.27, 10),
    ("rb3_ann43", [r"#FF0000:^{4*3}"], 0.55, 0.32, 10),
    ("rb3_p3_vecX", [r"#FF0000:\left[\overset{x_1}{\overset{x_2}{x_3}}\right]"], 0.78, 1.05, 10),
    ("rb3_p3_rhs", [r"#000000:=\left[\overset{7}{\overset{12}{\overset{10}{24}}}\right]||#FF0000:^{4*1}"], 1.30, 1.05, 10),
]


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, rows, maxw, maxh, rowgap in ASSETS:
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".rb3.json")
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
    with open(os.path.join(EQDIR, "rb3_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
