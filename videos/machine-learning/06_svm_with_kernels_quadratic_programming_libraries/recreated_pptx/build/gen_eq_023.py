#!/usr/bin/env python3
"""Render slide 023 (RBF Kernel) math assets as stacked 2-D mathtext PNGs.

Matrices are composed cell-by-cell (mathtext here lacks \\begin{array} and
\\textcolor): each cell is a colored segment, rows are baseline-aligned,
paren/bracket delimiters are single glyphs stretched vertically to body height.
Output: recreated_pptx/build/eq_023/*.png at 600 dpi, JSON sizes printed.
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
    """rows: list of rows; each row is list of (latex, color) or (None, color)."""
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
    info = {"path": path, "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
            "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(size, 2)}
    print(json.dumps(info))
    return info


D = lambda s: (s, BLACK)


def main():
    fit("top_rbf", [[("e^{-\\gamma\\,\\|a-b\\|^{2}}", BLACK)]], 22, 1.70, 0.40,
        delim=("[", "]"))
    ab = [[("a_1", RED), ("b_1", BLUE)], [("a_2", RED), ("b_2", BLUE)]]
    fit("mat_ab", ab, 16, 0.95, 0.55, delim=("(", ")"))
    fit("eq_rbf", [[("e^{-\\gamma\\,\\|a-b\\|^{2}}", BLACK)]], 16, 1.30, 0.38)
    fit("mat_normal", [[("a_1", RED), ("a_2", RED)], [("b_1", BLUE), ("b_2", BLUE)]],
        15, 0.78, 0.50, delim=("(", ")"))
    fit("vec_map", [[("\\mathbf{a\\ ,\\ b\\ \\Rightarrow}", RED),
                     ("\\mathbf{u\\ ,\\ v}", BLUE2)]], 14, 1.35, 0.27)
    pink_rows = [[(f"u_{s}", RED), (f"v_{s}", BLUE2)]
                 for s in ("1", "2", "3", "\\dots", "\\dots", "\\infty")]
    fit("vec_pink", pink_rows, 14, 0.68, 1.50)
    vrest = ["2", "3", "\\dots", "\\dots", "\\infty"]
    kern = [[("u_1", RED), ("u_2", RED), ("u_3", RED), ("\\dots", RED),
             ("\\dots", RED), ("u_\\infty", RED), ("v_1", BLUE2)]]
    for s in vrest:
        kern.append([(None, RED)] * 6 + [(f"v_{s}", BLUE2)])
    fit("mat_kernel", kern, 14, 2.60, 1.00, delim=("(", ")"))
    fit("calc_atb", [[("\\mathit{Calculate}\\ ", BLACK),
                      ("\\mathbf{a^{T}\\,b}", RED)]], 14, 1.15, 0.25)
    fit("calc_utv", [[("\\mathit{Calculate}\\ ", BLACK),
                      ("\\mathbf{u^{T}\\,v}", RED)]], 14, 1.15, 0.25)


if __name__ == "__main__":
    main()
