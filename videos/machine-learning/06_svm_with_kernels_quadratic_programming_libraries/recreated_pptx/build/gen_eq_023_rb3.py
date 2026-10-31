#!/usr/bin/env python3
"""Fresh (wave-3 rebuild) math assets for slide 023, rendered ONLY from
qa/reanalysis2/slide_023_analysis.txt section 8 equations.

Matrices/vectors are composed cell-by-cell with render_math.py segments
(mathtext lacks \\begin{array} / \\textcolor); paren/bracket delimiters are
single glyphs stretched to body height. Output: eq_023/*.png at 600 dpi +
eq_023/manifest.json with w_in/h_in per asset.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_math import render_segment, DPI

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_023")
RED = "#C00000"
BLUE = "#0000CC"
BLUE2 = "#3300CC"
BLACK = "#000000"

PAD = 6
COL_GAP = 16
ROW_GAP = 4


def compose(rows, size, delim=None):
    cells = []
    for row in rows:
        cells.append([None if lt is None else render_segment(lt, c, size)
                      for lt, c in row])
    ncols = max(len(r) for r in cells)
    colw = [0] * ncols
    for r in cells:
        for c, cell in enumerate(r):
            if cell is not None:
                colw[c] = max(colw[c], cell[0].shape[1])
    rowh, rowbase = [], []
    for r in cells:
        h = 0
        b = 0
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
    dl = render_segment(delim[0], BLACK, size)[0]
    dr = render_segment(delim[1], BLACK, size)[0]
    dl = np.asarray(Image.fromarray(dl).resize((dl.shape[1], bh), Image.BILINEAR))
    dr = np.asarray(Image.fromarray(dr).resize((dr.shape[1], bh), Image.BILINEAR))
    w = bw + dl.shape[1] + dr.shape[1] + 2 * PAD
    canvas = np.zeros((bh, w, 4), dtype=np.uint8)
    canvas[:, PAD:PAD + dl.shape[1]] = dl
    canvas[:, PAD + dl.shape[1]:PAD + dl.shape[1] + bw] = body
    canvas[:, w - PAD - dr.shape[1]:w - PAD] = dr
    return canvas


def fit(name, rows, size0, maxw, maxh, delim=None):
    size = size0
    for _ in range(14):
        canvas = compose(rows, size, delim)
        w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
        if w_in <= maxw and h_in <= maxh:
            break
        size *= 0.92
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    return {"image": name + ".png", "path": path,
            "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
            "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(size, 2)}


def main():
    manifest = {}
    # spec eq 1: [ e^{-gamma ||a - b||^2} ] top band, black, bracketed
    manifest["top_rbf"] = fit("top_rbf",
                              [[("e^{-\\gamma\\,\\|a-b\\|^{2}}", BLACK)]],
                              22, 1.70, 0.42, delim=("[", "]"))
    # spec eq 7: (a1 b1 / a2 b2) input matrix, a red / b blue, both copies
    ab = [[("a_1", RED), ("b_1", BLUE)], [("a_2", RED), ("b_2", BLUE)]]
    manifest["mat_ab"] = fit("mat_ab", ab, 16, 0.95, 0.55, delim=("(", ")"))
    # spec eq 2: e^{-gamma ||a - b||^2} grey box, black, no delimiters
    manifest["eq_rbf"] = fit("eq_rbf",
                             [[("e^{-\\gamma\\,\\|a-b\\|^{2}}", BLACK)]],
                             16, 1.30, 0.38)
    # spec eq 8: (a1 a2 / b1 b2) cyan box in Normal Model panel [?]
    manifest["mat_normal"] = fit("mat_normal",
                                 [[("a_1", RED), ("a_2", RED)],
                                  [("b_1", BLUE), ("b_2", BLUE)]],
                                 15, 0.78, 0.50, delim=("(", ")"))
    # spec eq 5: a , b => u , v  (a,b red; u,v blue)
    manifest["vec_map"] = fit("vec_map",
                              [[("\\mathbf{a\\ ,\\ b\\ \\Rightarrow}", RED),
                                ("\\mathbf{u\\ ,\\ v}", BLUE2)]],
                              14, 1.35, 0.27)
    # spec eq 9: pink two-column list u1..u-inf | v1..v-inf
    pink = [[(f"u_{s}", RED), (f"v_{s}", BLUE2)]
            for s in ("1", "2", "3", "\\dots", "\\dots", "\\infty")]
    manifest["vec_pink"] = fit("vec_pink", pink, 14, 0.68, 1.50)
    # spec eq 10: kernel matrix, u-row across top, v-column down the right
    kern = [[("u_1", RED), ("u_2", RED), ("u_3", RED), ("\\dots", RED),
             ("\\dots", RED), ("u_\\infty", RED), ("v_1", BLUE2)]]
    for s in ("2", "3", "\\dots", "\\dots", "\\infty"):
        kern.append([(None, RED)] * 6 + [(f"v_{s}", BLUE2)])
    manifest["mat_kernel"] = fit("mat_kernel", kern, 14, 2.60, 1.00,
                                 delim=("(", ")"))
    # spec eq 3/4: Calculate a^T b / Calculate u^T v
    manifest["calc_atb"] = fit("calc_atb",
                               [[("\\mathit{Calculate}\\ ", BLACK),
                                 ("\\mathbf{a^{T}\\,b}", RED)]],
                               14, 1.15, 0.25)
    manifest["calc_utv"] = fit("calc_utv",
                               [[("\\mathit{Calculate}\\ ", BLACK),
                                 ("\\mathbf{u^{T}\\,v}", RED)]],
                               14, 1.15, 0.25)
    with open(os.path.join(OUT, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    for k, v in manifest.items():
        print(k, v["w_in"], "x", v["h_in"], "in")


if __name__ == "__main__":
    main()
