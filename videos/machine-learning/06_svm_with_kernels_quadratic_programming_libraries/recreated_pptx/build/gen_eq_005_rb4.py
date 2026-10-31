#!/usr/bin/env python3
"""Slide 005 equation assets, iteration rb4: 600-dpi mathtext PNGs, tight-cropped.

Direct matplotlib mathtext rendering (render_math.py clips ink wider than its
probe figure and pads baselines); same mechanism: mathtext -> transparent PNG
at 600 dpi, placed at w = px/600 in. Content ONLY from
qa/reanalysis2/slide_005_analysis.txt. Writes eq_005/rb4_*.png + rb4_manifest.json.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_005")
DPI = 600

BLACK = "#000000"
RED = "#C00000"
GREEN = "#008000"

VEC3 = r"\left(\overset{\overset{x_1}{x_2}}{x_3}\right)"

# name, box [x0,y0,x1,y1] normalized, rowgap_in, pt, rows (each row = list of (color, latex))
ASSETS = [
    ("rb4_e1", [0.030, 0.080, 0.972, 0.215], 0.10, 24.0, [[
        (BLACK, r"\left(x_1\ \ x_2\ \ x_3\right)\ \left\vert\overset{\overset{a_{11}\ \ a_{12}\ \ a_{13}}{a_{21}\ \ a_{22}\ \ a_{23}}}{a_{31}\ \ a_{32}\ \ a_{33}}\right\vert\ " + VEC3 +
         r"\ =\ \left(\overset{\overset{(a_{11}x_1{+}a_{21}x_2{+}a_{31}x_3)}{(a_{12}x_1{+}a_{22}x_2{+}a_{32}x_3)}}{(a_{13}x_1{+}a_{23}x_2{+}a_{33}x_3)}\right)\ " + VEC3),
    ]]),
    ("rb4_e2", [0.030, 0.222, 0.972, 0.292], 0.06, 15.0, [
        [(BLACK, r"(a_{11}x_1{+}a_{21}x_2{+}a_{31}x_3)x_1 + (a_{12}x_1{+}a_{22}x_2{+}a_{32}x_3)x_2 + (a_{13}x_1{+}a_{23}x_2{+}a_{33}x_3)x_3 =")],
        [(BLACK, r"a_{11}x_1^2 + a_{21}x_1x_2 + a_{31}x_1x_3 + a_{12}x_1x_2 + a_{22}x_2^2 + a_{32}x_2x_3 + a_{13}x_1x_3 + a_{23}x_2x_3 + a_{33}x_3^2")],
    ]),
    ("rb4_e3", [0.030, 0.298, 0.972, 0.362], 0.10, 14.0, [[
        (RED, r"a_{11}x_1^2 + a_{22}x_2^2 + a_{33}x_3^2 + (a_{21}{+}a_{12})x_1x_2 + (a_{31}{+}a_{13})x_1x_3 + (a_{32}{+}a_{23})x_2x_3"),
        (RED, r"\ \Rightarrow\ "),
        (GREEN, r"\mathrm{Quadratic\ form}"),
    ]]),
    ("rb4_d1", [0.035, 0.365, 0.605, 0.420], 0.10, 14.0, [[(BLACK, r"a_{11}"), (RED, r"\ \Rightarrow\ "), (RED, r"\mathrm{Coefficient\ of\ }x_1^2")]]),
    ("rb4_d2", [0.035, 0.420, 0.605, 0.475], 0.10, 14.0, [[(BLACK, r"a_{22}"), (RED, r"\ \Rightarrow\ "), (RED, r"\mathrm{Coefficient\ of\ }x_2^2")]]),
    ("rb4_d3", [0.035, 0.475, 0.605, 0.530], 0.10, 14.0, [[(BLACK, r"a_{33}"), (RED, r"\ \Rightarrow\ "), (RED, r"\mathrm{Coefficient\ of\ }x_3^2")]]),
    ("rb4_d4", [0.035, 0.530, 0.605, 0.585], 0.10, 14.0, [[(BLACK, r"a_{21}{+}a_{12}"), (RED, r"\ \Rightarrow\ "), (RED, r"a_{12}{=}a_{21}{=}\frac{1}{2}\ \mathrm{coefficient\ of\ }x_1x_2")]]),
    ("rb4_d5", [0.035, 0.585, 0.605, 0.640], 0.10, 14.0, [[(BLACK, r"a_{31}{+}a_{13}"), (RED, r"\ \Rightarrow\ "), (RED, r"a_{13}{=}a_{31}{=}\frac{1}{2}\ \mathrm{coefficient\ of\ }x_1x_3")]]),
    ("rb4_d6", [0.035, 0.640, 0.605, 0.695], 0.10, 14.0, [[(BLACK, r"a_{32}{+}a_{23}"), (RED, r"\ \Rightarrow\ "), (RED, r"a_{32}{=}a_{23}{=}\frac{1}{2}\ \mathrm{coefficient\ of\ }x_2x_3")]]),
    ("rb4_hdr", [0.100, 0.700, 0.250, 0.730], 0.10, 12.0, [[(BLACK, r"x_1\ \ \ x_2\ \ \ x_3")]]),
    ("rb4_m1", [0.080, 0.745, 0.230, 0.802], 0.10, 13.0, [[(BLACK, r"x_1\ \ \ a_{11}\ \ \ a_{12}")]]),
    ("rb4_m2", [0.080, 0.802, 0.230, 0.858], 0.10, 13.0, [[(BLACK, r"x_2\ \ \ a_{21}\ \ \ a_{22}")]]),
    ("rb4_m3", [0.080, 0.858, 0.230, 0.915], 0.10, 13.0, [[(BLACK, r"x_3\ \ \ a_{31}\ \ \ a_{32}")]]),
]

GRID = [
    ("rb4_b1", r"\mathrm{coef\ of\ }x_1^2"),
    ("rb4_b2", r"0.5\ \mathrm{coef\ of\ }x_1x_3"),
    ("rb4_b3", r"0.5\ \mathrm{coef\ of\ }x_1x_2"),
    ("rb4_b4", r"0.5\ \mathrm{coef\ of\ }x_1x_2"),
    ("rb4_b5", r"\mathrm{coef\ of\ }x_2^2"),
    ("rb4_b6", r"0.5\ \mathrm{coef\ of\ }x_2x_3"),
    ("rb4_b7", r"0.5\ \mathrm{coef\ of\ }x_1x_3"),
    ("rb4_b8", r"0.5\ \mathrm{coef\ of\ }x_2x_3"),
    ("rb4_b9", r"\mathrm{coef\ of\ }x_3^2"),
]
COLS = [(0.500, 0.640), (0.640, 0.800), (0.800, 0.965)]
ROWS = [(0.745, 0.775), (0.805, 0.835), (0.865, 0.895)]
for i, (name, latex) in enumerate(GRID):
    r, c = divmod(i, 3)
    box = [COLS[c][0], ROWS[r][0], COLS[c][1], ROWS[r][1]]
    ASSETS.append((name, box, 0.10, 10.0, [[(BLACK, latex)]]))


def render(name, box, rowgap, pt, rows):
    fig_w, fig_h = 24.0, 4.0 * len(rows) + 1.0
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    fig.patch.set_alpha(0.0)
    y = 1.0 - 0.5 / fig_h
    for row in rows:
        fig.canvas.draw()
        x = 0.01
        for color, latex in row:
            t = fig.text(x, y, f"${latex}$", fontsize=pt, color=color, ha="left", va="center")
            fig.canvas.draw()
            bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
            x += bb.width / (fig_w * DPI)
            t.remove()
            fig.text(x - bb.width / (fig_w * DPI), y, f"${latex}$", fontsize=pt, color=color, ha="left", va="center")
        y -= (rowgap + 0.35) / fig_h
    out = os.path.join(EQDIR, name + ".png")
    fig.savefig(out, transparent=True, bbox_inches="tight", pad_inches=0.02, dpi=DPI)
    plt.close(fig)
    from PIL import Image
    im = Image.open(out)
    w, h = im.size
    js = os.path.join(EQDIR, name + ".json")
    x0, y0, x1, y1 = box
    info = {"path": out, "w_px": w, "h_px": h, "w_in": round(w / DPI, 5),
            "h_in": round(h / DPI, 5), "dpi": DPI, "fontsize_pt": [pt] * len(rows)}
    json.dump(info, open(js, "w"), indent=2)
    return {"image": name + ".png",
            "box": [round(x0 * 13.33, 4), round(y0 * 7.5, 4),
                    round((x1 - x0) * 13.33, 4), round((y1 - y0) * 7.5, 4)],
            "w_in": info["w_in"], "h_in": info["h_in"]}


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, box, rowgap, pt, rows in ASSETS:
        manifest[name] = render(name, box, rowgap, pt, rows)
        print(name, manifest[name]["w_in"], "x", manifest[name]["h_in"], "in @", pt, "pt")
    with open(os.path.join(EQDIR, "rb4_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
