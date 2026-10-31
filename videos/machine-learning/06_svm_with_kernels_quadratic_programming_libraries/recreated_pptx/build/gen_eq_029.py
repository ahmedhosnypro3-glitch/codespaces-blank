#!/usr/bin/env python3
"""Fresh math assets for slide 029, rendered ONLY from
qa/reanalysis2/slide_029_analysis.txt section 8 (EQUATIONS).

Single-line multi-color equations use render_math.fit_row (|| segments).
The bracketed row/column vectors of E3 are composed cell-by-cell
(mathtext lacks \\begin{array}); brackets are stretched delimiter glyphs.
Output: eq_029/*.png at 600 dpi + eq_029/manifest.json (file/w_in/h_in/pt).
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_math import render_segment, render_row, DPI

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_029")
RED = "#CC0000"
BLUE = "#3333CC"
PHI = "#0000CC"
BLACK = "#000000"
PAD = 6
COL_GAP = 14
ROW_GAP = 2


def compose(rows, size, delim=None):
    cells = [[None if lt is None else render_segment(lt, c, size)
              for lt, c in row] for row in rows]
    ncols = max(len(r) for r in cells)
    colw = [0] * ncols
    for r in cells:
        for c, cell in enumerate(r):
            if cell is not None:
                colw[c] = max(colw[c], cell[0].shape[1])
    rowh, rowbase = [], []
    for r in cells:
        h = b = 0
        for cell in r:
            if cell is not None:
                h = max(h, cell[0].shape[0])
                b = max(b, cell[1])
        rowh.append(h)
        rowbase.append(b)
    bw = sum(colw) + COL_GAP * (ncols - 1) + 2 * PAD
    bh = sum(rowh) + ROW_GAP * (len(cells) - 1) + 2 * PAD
    body = np.zeros((bh, bw, 4), dtype=np.uint8)
    y = PAD
    for r, row in enumerate(cells):
        x = PAD
        for c, cell in enumerate(row):
            if cell is not None:
                arr, base = cell
                ytop = y + rowbase[r] - base
                body[ytop:ytop + arr.shape[0], x:x + arr.shape[1]] = arr
            x += colw[c] + COL_GAP
        y += rowh[r] + ROW_GAP
    if not delim:
        return body
    dl = np.asarray(Image.fromarray(render_segment(delim[0], BLACK, size)[0])
                    .resize((max(6, PAD // 2), bh), Image.BILINEAR))
    dr = np.asarray(Image.fromarray(render_segment(delim[1], BLACK, size)[0])
                    .resize((max(6, PAD // 2), bh), Image.BILINEAR))
    w = bw + dl.shape[1] + dr.shape[1] + 2 * PAD
    canvas = np.zeros((bh, w, 4), dtype=np.uint8)
    canvas[:, PAD:PAD + dl.shape[1]] = dl
    canvas[:, PAD + dl.shape[1]:PAD + dl.shape[1] + bw] = body
    canvas[:, w - PAD - dr.shape[1]:w - PAD] = dr
    return canvas


def save(name, canvas, pt):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    return {"file": name + ".png", "w_px": int(canvas.shape[1]),
            "h_px": int(canvas.shape[0]),
            "w_in": round(canvas.shape[1] / DPI, 5),
            "h_in": round(canvas.shape[0] / DPI, 5), "pt": round(pt, 2)}


def fitline(name, row, size0, maxw, maxh):
    size = size0
    for _ in range(24):
        canvas = render_row(row, size)
        if canvas.shape[1] / DPI <= maxw and canvas.shape[0] / DPI <= maxh:
            break
        size *= 0.93
    return save(name, canvas, size)


def fitgrid(name, rows, size0, maxw, maxh, delim=None):
    size = size0
    for _ in range(16):
        canvas = compose(rows, size, delim)
        if canvas.shape[1] / DPI <= maxw and canvas.shape[0] / DPI <= maxh:
            break
        size *= 0.92
    return save(name, canvas, size)


def main():
    m = {}
    # E1: RBF identity; last two factors blue-purple, final e^{ab} red
    m["e1"] = fitline("e1",
        "#000000:e^{-1/2(a-b)^{2}}=e^{-1/2(a^{2}+b^{2}-2ab)}="
        "||#3333CC:e^{-a^{2}/2}\\,e^{-b^{2}/2}\\ ||#CC0000:e^{ab}",
        22, 5.10, 0.26)
    # E2: Taylor series of e^{ab}; e^{ab} and trailing infinity red
    m["e2"] = fitline("e2",
        "#CC0000:e^{ab}||#000000: = 1+\\frac{ab}{1!}+\\frac{(ab)^{2}}{2!}"
        "+\\frac{(ab)^{3}}{3!}+\\frac{(ab)^{4}}{4!}+\\frac{(ab)^{5}}{5!}+\\dots\\dots"
        " ||#CC0000:\\infty",
        20, 5.20, 0.50)
    # E3 lead-in "e^{ab} ="
    m["e3_eq"] = fitline("e3_eq", "#CC0000:e^{ab}||#000000: =", 16, 0.50, 0.26)
    # E3 row vector [ a/sqrt1! a^2/sqrt2! a^3/sqrt3! a^4/sqrt4! ... ... inf ]
    m["e3_row"] = fitgrid("e3_row",
        [[(t, BLACK) for t in ("\\frac{a}{\\sqrt{1!}}", "\\frac{a^{2}}{\\sqrt{2!}}",
           "\\frac{a^{3}}{\\sqrt{3!}}", "\\frac{a^{4}}{\\sqrt{4!}}",
           "\\dots", "\\dots", "\\infty")]],
        18, 3.10, 0.42, delim=("[", "]"))
    # E3 column vector [ 1/b ; sqrt1!/b^2 ; sqrt2!/b^3 ; sqrt3!/b^4 ; sqrt4!/... ; ... ; ... inf ]
    m["e3_col"] = fitgrid("e3_col",
        [[(t, BLACK)] for t in ("\\frac{1}{b}", "\\frac{\\sqrt{1!}}{b^{2}}",
           "\\frac{\\sqrt{2!}}{b^{3}}", "\\frac{\\sqrt{3!}}{b^{4}}",
           "\\frac{\\sqrt{4!}}{\\dots}", "\\dots", "\\dots\\ \\infty")],
        14, 0.62, 2.80, delim=("[", "]"))
    # E4: e^x series, red trailing infinity
    m["e4"] = fitline("e4",
        "#000000:e^{x} = 1+\\frac{x}{1!}+\\frac{x^{2}}{2!}+\\frac{x^{3}}{3!}"
        "+\\frac{x^{4}}{4!}+\\frac{x^{5}}{5!}+\\dots\\dots ||#CC0000:\\infty",
        18, 4.30, 0.36)
    # E5: e^3 series, red trailing infinity
    m["e5"] = fitline("e5",
        "#000000:e^{3} = 1+\\frac{3}{1!}+\\frac{3^{2}}{2!}+\\frac{3^{3}}{3!}"
        "+\\frac{3^{4}}{4!}+\\frac{3^{5}}{5!}+\\dots\\dots ||#CC0000:\\infty",
        18, 4.25, 0.40)
    # phi labels: blue phi, red superscript T on phi(a)
    m["phi_a"] = fitline("phi_a", "#0000CC:\\phi(a)||#CC0000:^{\\mathrm{T}}",
                         22, 0.92, 0.40)
    m["phi_b"] = fitline("phi_b", "#0000CC:\\phi(b)", 22, 0.87, 0.42)
    with open(os.path.join(OUT, "manifest.json"), "w") as fh:
        json.dump(m, fh, indent=2)
    for k, v in m.items():
        print(k, v["w_in"], "x", v["h_in"], "in @", v["pt"], "pt")


if __name__ == "__main__":
    main()
