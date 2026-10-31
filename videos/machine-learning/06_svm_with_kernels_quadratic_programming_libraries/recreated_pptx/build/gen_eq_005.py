#!/usr/bin/env python3
"""Generate fresh 600-dpi mathtext PNGs for slide 005 rebuild (wave 3).

Content comes ONLY from qa/reanalysis2/slide_005_analysis.txt (sections 2/8).
Assets land in build/eq_005/ as rb3_*.png + rb3_*.json sidecars plus
rb3_manifest.json mapping name -> {image, box (inches), w_in, h_in}.
Matrices use nested \\overset levels; col vectors use
\\left[\\overset{\\overset{x_1}{x_2}}{x_3}\\right].
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_005")
RENDER = os.path.join(HERE, "render_math.py")

BLACK = "#000000"
RED = "#C00000"
GREEN = "#008000"

# name, box [x0,y0,x1,y1] normalized (spec sections 3/8), size, rowgap_px, rows
ASSETS = [
    ("rb3_e1", [0.030, 0.080, 0.972, 0.215], 18, 10, [
        BLACK + r":\left(x_1\ \ x_2\ \ x_3\right)||" + BLACK +
        r":\left|\overset{\overset{a_{11}\ \ a_{12}\ \ a_{13}}{a_{21}\ \ a_{22}\ \ a_{23}}}{a_{31}\ \ a_{32}\ \ a_{33}}\right|"
        + "||" + BLACK + r":\left(\overset{\overset{x_1}{x_2}}{x_3}\right)||" + BLACK + r":=||" + BLACK +
        r":\left(\overset{\overset{(a_{11}x_1+a_{21}x_2+a_{31}x_3)}{(a_{12}x_1+a_{22}x_2+a_{32}x_3)}}{(a_{13}x_1+a_{23}x_2+a_{33}x_3)}\right)"
        + "||" + BLACK + r":\left(\overset{\overset{x_1}{x_2}}{x_3}\right)",
    ]),
    ("rb3_e2", [0.030, 0.225, 0.972, 0.285], 16, 8, [
        BLACK + r":(a_{11}x_1+a_{21}x_2+a_{31}x_3)x_1 + (a_{12}x_1+a_{22}x_2+a_{32}x_3)x_2 + (a_{13}x_1+a_{23}x_2+a_{33}x_3)x_3 =",
        BLACK + r":a_{11}x_1^2 + a_{21}x_1x_2 + a_{31}x_1x_3 + a_{12}x_1x_2 + a_{22}x_2^2 + a_{32}x_2x_3 + a_{13}x_1x_3 + a_{23}x_2x_3 + a_{33}x_3^2",
    ]),
    ("rb3_e3", [0.030, 0.295, 0.972, 0.350], 16, 10, [
        RED + r":a_{11}x_1^2 + a_{22}x_2^2 + a_{33}x_3^2 + (a_{21}+a_{12})x_1x_2 + (a_{31}+a_{13})x_1x_3 + (a_{32}+a_{23})x_2x_3"
        + "||" + RED + r":\ \Rightarrow\ ||" + GREEN + r":\mathrm{Quadratic\ form}",
    ]),
    ("rb3_d1", [0.035, 0.365, 0.605, 0.420], 14, 10, [
        BLACK + r":a_{11}||" + RED + r":\ \Rightarrow\ ||" + RED + r":\mathrm{Coefficient\ of\ }x_1^2"]),
    ("rb3_d2", [0.035, 0.420, 0.605, 0.475], 14, 10, [
        BLACK + r":a_{22}||" + RED + r":\ \Rightarrow\ ||" + RED + r":\mathrm{Coefficient\ of\ }x_2^2"]),
    ("rb3_d3", [0.035, 0.475, 0.605, 0.530], 14, 10, [
        BLACK + r":a_{33}||" + RED + r":\ \Rightarrow\ ||" + RED + r":\mathrm{Coefficient\ of\ }x_3^2"]),
    ("rb3_d4", [0.035, 0.530, 0.605, 0.585], 14, 10, [
        BLACK + r":a_{21}+a_{12}||" + RED + r":\ \Rightarrow\ ||" + RED +
        r":a_{12}=a_{21}=\frac{1}{2}\ \mathrm{coefficient\ of\ }x_1x_2"]),
    ("rb3_d5", [0.035, 0.585, 0.605, 0.640], 14, 10, [
        BLACK + r":a_{31}+a_{13}||" + RED + r":\ \Rightarrow\ ||" + RED +
        r":a_{13}=a_{31}=\frac{1}{2}\ \mathrm{coefficient\ of\ }x_1x_3"]),
    ("rb3_d6", [0.035, 0.640, 0.605, 0.695], 14, 10, [
        BLACK + r":a_{32}+a_{23}||" + RED + r":\ \Rightarrow\ ||" + RED +
        r":a_{32}=a_{23}=\frac{1}{2}\ \mathrm{coefficient\ of\ }x_2x_3"]),
    ("rb3_hdr", [0.100, 0.700, 0.250, 0.730], 12, 10, [
        BLACK + r":x_1\ \ \ x_2\ \ \ x_3"]),
    ("rb3_m1", [0.080, 0.745, 0.230, 0.802], 13, 10, [
        BLACK + r":x_1\ \ \ a_{11}\ \ \ a_{12}"]),
    ("rb3_m2", [0.080, 0.802, 0.230, 0.858], 13, 10, [
        BLACK + r":x_2\ \ \ a_{21}\ \ \ a_{22}"]),
    ("rb3_m3", [0.080, 0.858, 0.230, 0.915], 13, 10, [
        BLACK + r":x_3\ \ \ a_{31}\ \ \ a_{32}"]),
]

# right 3x3 coefficient grid labels (verbatim from spec section 2)
GRID = [
    ("rb3_b1", r"\mathrm{coef\ of\ }x_1^2"),
    ("rb3_b2", r"0.5\ \mathrm{coef\ of\ }x_1x_3"),
    ("rb3_b3", r"0.5\ \mathrm{coef\ of\ }x_1x_2"),
    ("rb3_b4", r"0.5\ \mathrm{coef\ of\ }x_1x_2"),
    ("rb3_b5", r"\mathrm{coef\ of\ }x_2^2"),
    ("rb3_b6", r"0.5\ \mathrm{coef\ of\ }x_2x_3"),
    ("rb3_b7", r"0.5\ \mathrm{coef\ of\ }x_1x_3"),
    ("rb3_b8", r"0.5\ \mathrm{coef\ of\ }x_2x_3"),
    ("rb3_b9", r"\mathrm{coef\ of\ }x_3^2"),
]
COLS = [(0.500, 0.640), (0.640, 0.800), (0.800, 0.965)]
ROWS = [(0.745, 0.775), (0.805, 0.835), (0.865, 0.895)]
for i, (name, latex) in enumerate(GRID):
    r, c = divmod(i, 3)
    box = [COLS[c][0], ROWS[r][0], COLS[c][1], ROWS[r][1]]
    ASSETS.append((name, box, 10, 10, [BLACK + ":" + latex]))


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, box, size, rowgap, rows in ASSETS:
        x0, y0, x1, y1 = box
        nrows = len(rows)
        maxw = (x1 - x0) * 13.33
        maxh = (y1 - y0) * 7.5 / nrows
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".json")
        cmd = [sys.executable, RENDER, "--out", out, "--size", str(size),
               "--maxw", str(maxw), "--maxh", str(maxh * nrows),
               "--rowgap", str(rowgap), "--out-json", js]
        for r in rows:
            cmd += ["--row", r]
        subprocess.run(cmd, check=True, cwd=HERE)
        with open(js) as fh:
            info = json.load(fh)
        manifest[name] = {
            "image": name + ".png",
            "box": [round(x0 * 13.33, 4), round(y0 * 7.5, 4),
                    round((x1 - x0) * 13.33, 4), round((y1 - y0) * 7.5, 4)],
            "w_in": info["w_in"], "h_in": info["h_in"],
        }
        print(name, info["w_in"], "x", info["h_in"], "in")
    with open(os.path.join(EQDIR, "rb3_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
