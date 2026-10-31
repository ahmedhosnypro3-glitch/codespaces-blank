#!/usr/bin/env python3
"""Slide 007 equation assets, iteration rb: 600-dpi mathtext PNGs, tight-cropped.

Fixes vs eq_007: displaystyle summations (limits stacked above/below the sigma),
en-dash in equation 3, direct matplotlib rendering (render_math.py clips wide ink).
Content ONLY from qa/reanalysis2/slide_007_analysis.txt section 8.
Writes eq_007/rb_*.png + rb.json sidecars + rb_manifest.json.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_007")
DPI = 600

BLACK, RED, BLUE, MAG, GREEN = "#000000", "#FF0000", "#0000FF", "#FF00FF", "#008000"

VEC_X = r"\left[\overset{x_1}{\overset{x_2}{x_3}}\right]"

# name, pt, rows (list of list of (color, latex))
ASSETS = [
    ("rb_sum1", 14, [[(BLUE, r"\overset{3}{\underset{i=1}{\sum}} a_i x_i"), (BLACK, r"= a_1 x_1 + a_2 x_2 + a_3 x_3 = Z")]]),
    ("rb_arrow", 16, [[(RED, r"\Rightarrow")]]),
    ("rb_p1row", 14, [[(BLUE, r"\left[a_1\ \ a_2\ \ a_3\right]")]]),
    ("rb_vecx", 14, [[(RED, VEC_X)]]),
    ("rb_p1rhs", 14, [[(BLACK, r"= \left(z\right)")]]),
    ("rb_ann1x1", 10, [[(RED, r"1*1")]]),
    ("rb_suma", 13, [[(BLUE, r"\overset{3}{\underset{i=1}{\sum}} a_i x_i"), (BLACK, r"= Z_1")]]),
    ("rb_sumb", 13, [[(MAG, r"\overset{3}{\underset{i=1}{\sum}} b_i x_i"), (BLACK, r"= Z_2")]]),
    ("rb_sumc", 13, [[(GREEN, r"\overset{3}{\underset{i=1}{\sum}} c_i x_i"), (BLACK, r"= Z_3")]]),
    ("rb_ra3", 14, [[(BLUE, r"a_1\ \ a_2\ \ a_3")]]),
    ("rb_rb3", 14, [[(MAG, r"b_1\ \ b_2\ \ b_3")]]),
    ("rb_rc3", 14, [[(GREEN, r"c_1\ \ c_2\ \ c_3")]]),
    ("rb_eq", 14, [[(BLACK, r"=")]]),
    ("rb_zvec3", 14, [[(BLACK, r"\left[\overset{Z_1}{\overset{Z_2}{Z_3}}\right]")]]),
    ("rb_ann3x1", 10, [[(RED, r"3*1")]]),
    ("rb_e1", 14, [[(RED, r"x_1 + 2 x_2 = 7")]]),
    ("rb_e2", 14, [[(RED, r"3 x_1 + 4 x_2 = 12")]]),
    ("rb_e3", 14, [[(RED, r"3 x_3 \text{–} 5 x_1 = 10")]]),
    ("rb_e4", 14, [[(RED, r"x_1 + x_2 + x_3 = 24")]]),
    ("rb_n1", 13, [[(BLACK, r"1\ \ 2\ \ 0")]]),
    ("rb_n2", 13, [[(BLACK, r"3\ \ 4\ \ 0")]]),
    ("rb_n3", 13, [[(BLACK, r"-5\ \ 0\ \ 3")]]),
    ("rb_n4", 13, [[(BLACK, r"1\ \ 1\ \ 1")]]),
    ("rb_ann4x3", 10, [[(RED, r"4*3")]]),
    ("rb_rhs4", 13, [[(BLACK, r"\left[\overset{7}{\overset{12}{\overset{10}{24}}}\right]")]]),
    ("rb_ann4x1", 10, [[(RED, r"4*1")]]),
]


def render(name, pt, rows):
    fig_w, fig_h = 24.0, 1.2 * len(rows) + 0.8
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    fig.patch.set_alpha(0.0)
    y = 1.0 - 0.4 / fig_h
    for row in rows:
        x = 0.01
        for color, latex in row:
            t = fig.text(x, y, f"${latex}$", fontsize=pt, color=color, ha="left", va="center")
            fig.canvas.draw()
            bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
            x += bb.width / (fig_w * DPI)
        y -= 1.0 / fig_h
    out = os.path.join(EQDIR, name + ".png")
    fig.savefig(out, transparent=True, bbox_inches="tight", pad_inches=0.02, dpi=DPI)
    plt.close(fig)
    from PIL import Image
    im = Image.open(out)
    w, h = im.size
    info = {"path": out, "w_px": w, "h_px": h, "w_in": round(w / DPI, 5),
            "h_in": round(h / DPI, 5), "dpi": DPI, "fontsize_pt": [pt] * len(rows)}
    json.dump(info, open(os.path.join(EQDIR, name + ".json"), "w"), indent=2)
    return {"image": name + ".png", "w_in": info["w_in"], "h_in": info["h_in"]}


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, pt, rows in ASSETS:
        manifest[name] = render(name, pt, rows)
        print(name, manifest[name]["w_in"], "x", manifest[name]["h_in"], "@", pt)
    with open(os.path.join(EQDIR, "rb_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
