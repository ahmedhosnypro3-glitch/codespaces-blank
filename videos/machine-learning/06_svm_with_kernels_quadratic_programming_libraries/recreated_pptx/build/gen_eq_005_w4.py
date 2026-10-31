#!/usr/bin/env python3
"""Wave-4 math assets for slide 005, content from qa/reanalysis2/slide_005_analysis.txt only.
Color correction vs w3, verified by PIL sampling of unique_slides/slide_005.jpg:
E1/E2 black; E3 body red (#C00000) with red arrow and GREEN "Quadratic form";
definition lines: black LHS, red arrow, red RHS; matrix/grid labels black.
Assets: build/eq_005/w4_*.png + .json sidecars + w4_manifest.json (inches).
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
V3 = r"\left(\overset{\overset{x_1}{x_2}}{x_3}\right)"

A = []


def add(name, box, size, maxh, rows, rowgap=10):
    A.append((name, box, size, maxh, rows, rowgap))


add("w4_e1", [0.030, 0.080, 0.972, 0.215], 18, 1.0125, [
    BLACK + r":\left(x_1\ \ x_2\ \ x_3\right)\ \left\vert\overset{\overset{a_{11}\ \ a_{12}\ \ a_{13}}{a_{21}\ \ a_{22}\ \ a_{23}}}{a_{31}\ \ a_{32}\ \ a_{33}}\right\vert\ " + V3 +
    r"\ =\ \left(\overset{\overset{(a_{11}x_1{+}a_{21}x_2{+}a_{31}x_3)}{(a_{12}x_1{+}a_{22}x_2{+}a_{32}x_3)}}{(a_{13}x_1{+}a_{23}x_2{+}a_{33}x_3)}\right)\ " + V3,
])
add("w4_e2", [0.030, 0.222, 0.972, 0.288], 14, 0.22, [
    BLACK + r":(a_{11}x_1{+}a_{21}x_2{+}a_{31}x_3)x_1 + (a_{12}x_1{+}a_{22}x_2{+}a_{32}x_3)x_2 + (a_{13}x_1{+}a_{23}x_2{+}a_{33}x_3)x_3 =",
    BLACK + r":a_{11}x_1^2 + a_{21}x_1x_2 + a_{31}x_1x_3 + a_{12}x_1x_2 + a_{22}x_2^2 + a_{32}x_2x_3 + a_{13}x_1x_3 + a_{23}x_2x_3 + a_{33}x_3^2",
], rowgap=6)
# E3 rendered directly at 22pt via render_math.render_row (fit_row's height
# constraint caps a single row near 3.35in wide; the original line spans ~0.9
# of the slide width, so use the direct render and record its exact size).
E3_ROW = (RED + r":a_{11}x_1^2 + a_{22}x_2^2 + a_{33}x_3^2 + (a_{21}{+}a_{12})x_1x_2 + "
          r"(a_{31}{+}a_{13})x_1x_3 + (a_{32}{+}a_{23})x_2x_3||" +
          RED + r":\ \Rightarrow\ ||" + GREEN + r":\mathrm{Quadratic\ form}")


def add_e3():
    sys.path.insert(0, HERE)
    import render_math as rm
    from PIL import Image
    canvas = rm.render_row(E3_ROW, 22)
    out = os.path.join(EQDIR, "w4_e3.png")
    Image.fromarray(canvas).save(out)
    w_in, h_in = canvas.shape[1] / 600.0, canvas.shape[0] / 600.0
    info = {"path": out, "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
            "w_in": round(w_in, 5), "h_in": round(h_in, 5), "dpi": 600,
            "fontsize_pt": [22], "rows": [E3_ROW]}
    with open(os.path.join(EQDIR, "w4_e3.json"), "w") as fh:
        json.dump(info, fh, indent=2)
    x0, y0, x1, y1 = 0.030, 0.295, 0.972, 0.350
    man = {"image": "w4_e3.png", "x": round(x0 * 13.33, 4), "y": round(y0 * 7.5, 4),
           "w": round((x1 - x0) * 13.33, 4), "h": round((y1 - y0) * 7.5, 4),
           "w_in": info["w_in"], "h_in": info["h_in"]}
    return man
DEFS = [
    ("w4_d1", 0.365, r"a_{11}", r"\mathrm{Coefficient\ of\ }x_1^2"),
    ("w4_d2", 0.420, r"a_{22}", r"\mathrm{Coefficient\ of\ }x_2^2"),
    ("w4_d3", 0.475, r"a_{33}", r"\mathrm{Coefficient\ of\ }x_3^2"),
    ("w4_d4", 0.530, r"a_{21}{+}a_{12}", r"a_{12}{=}a_{21}{=}\frac{1}{2}\ \mathrm{coefficient\ of\ }x_1x_2"),
    ("w4_d5", 0.585, r"a_{31}{+}a_{13}", r"a_{13}{=}a_{31}{=}\frac{1}{2}\ \mathrm{coefficient\ of\ }x_1x_3"),
    ("w4_d6", 0.640, r"a_{32}{+}a_{23}", r"a_{32}{=}a_{23}{=}\frac{1}{2}\ \mathrm{coefficient\ of\ }x_2x_3"),
]
for name, y0, lhs, rhs in DEFS:
    add(name, [0.035, y0, 0.605, y0 + 0.055], 14, 0.4125,
        [BLACK + ":" + lhs + "||" + RED + r":\ \Rightarrow\ ||" + RED + ":" + rhs])

add("w4_hdr", [0.100, 0.700, 0.250, 0.730], 12, 0.225,
    [BLACK + r":x_1\ \ \ x_2\ \ \ x_3"])
MATS = [
    ("w4_m1", 0.745, r"x_1\ \ \ a_{11}\ \ \ a_{12}"),
    ("w4_m2", 0.802, r"x_2\ \ \ a_{21}\ \ \ a_{22}"),
    ("w4_m3", 0.858, r"x_3\ \ \ a_{31}\ \ \ a_{32}"),
]
for name, y0, latex in MATS:
    add(name, [0.080, y0, 0.230, y0 + 0.057], 13, 0.4275, [BLACK + ":" + latex])

GRID = [
    r"\mathrm{coef\ of\ }x_1^2", r"0.5\ \mathrm{coef\ of\ }x_1x_3", r"0.5\ \mathrm{coef\ of\ }x_1x_2",
    r"0.5\ \mathrm{coef\ of\ }x_1x_2", r"\mathrm{coef\ of\ }x_2^2", r"0.5\ \mathrm{coef\ of\ }x_2x_3",
    r"0.5\ \mathrm{coef\ of\ }x_1x_3", r"0.5\ \mathrm{coef\ of\ }x_2x_3", r"\mathrm{coef\ of\ }x_3^2",
]
COLS = [(0.500, 0.640), (0.640, 0.800), (0.800, 0.965)]
ROWS = [(0.745, 0.775), (0.805, 0.835), (0.865, 0.895)]
for i, latex in enumerate(GRID):
    r, c = divmod(i, 3)
    add("w4_b%d" % (i + 1), [COLS[c][0], ROWS[r][0], COLS[c][1], ROWS[r][1]], 10, 0.225,
        [BLACK + ":" + latex])


def main():
    os.makedirs(EQDIR, exist_ok=True)
    man = {"w4_e3": add_e3()}
    print("w4_e3", man["w4_e3"]["w_in"], "x", man["w4_e3"]["h_in"])
    bad = []
    for name, box, size, maxh, rows, rowgap in A:
        x0, y0, x1, y1 = box
        maxw = (x1 - x0) * 13.33
        boxh = (y1 - y0) * 7.5
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".json")
        cmd = [sys.executable, RENDER, "--out", out, "--size", str(size),
               "--maxw", str(maxw), "--maxh", str(maxh),
               "--rowgap", str(rowgap), "--out-json", js]
        for r in rows:
            cmd += ["--row", r]
        subprocess.run(cmd, check=True, cwd=HERE)
        with open(js) as fh:
            info = json.load(fh)
        ok = info["w_in"] <= maxw + 0.03 and info["h_in"] <= boxh + 0.03
        if not ok:
            bad.append(name)
        print(name, info["w_in"], "x", info["h_in"], "box", round(maxw, 3), "x", round(boxh, 3),
              "OK" if ok else "OVERFLOW")
        man[name] = {"image": name + ".png", "x": round(x0 * 13.33, 4), "y": round(y0 * 7.5, 4),
                     "w": round(maxw, 4), "h": round(boxh, 4),
                     "w_in": info["w_in"], "h_in": info["h_in"]}
    with open(os.path.join(EQDIR, "w4_manifest.json"), "w") as fh:
        json.dump(man, fh, indent=2)
    if bad:
        raise SystemExit("OVERFLOW: %s" % ", ".join(bad))


if __name__ == "__main__":
    main()
