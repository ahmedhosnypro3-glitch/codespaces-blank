#!/usr/bin/env python3
"""Fresh slide-023 math assets (rebuild wave 3) from qa/reanalysis2/slide_023_analysis.txt.

Matrices composed cell-by-cell with render_math.py segments (mathtext lacks
array envs); paren/bracket delimiters are glyphs stretched to body height.
Output: recreated_pptx/build/eq_023/*.png at 600 dpi + manifest.json.
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


def fit(manifest, name, rows, size0, maxw, maxh, delim=None):
    size = size0
    canvas = None
    for _ in range(14):
        canvas = compose(rows, size, delim)
        w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
        if w_in <= maxw and h_in <= maxh:
            break
        size *= 0.92
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(p)
    manifest[name] = {"image": name + ".png", "path": p,
                      "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
                      "w_in": round(canvas.shape[1] / DPI, 5),
                      "h_in": round(canvas.shape[0] / DPI, 5), "pt": round(size, 2)}


def main():
    m = {}
    fit(m, "top_rbf", [[("e^{-\\gamma\\,\\|a-b\\|^{2}}", BLACK)]], 22, 1.72, 0.40,
        delim=("[", "]"))
    ab = [[("a_1", RED), ("b_1", BLUE)], [("a_2", RED), ("b_2", BLUE)]]
    fit(m, "mat_ab", ab, 16, 0.95, 0.55, delim=("(", ")"))
    fit(m, "eq_rbf", [[("e^{-\\gamma\\,}", BLACK), ("\\|a-b\\|^{2}", BLUE)]],
        16, 1.35, 0.40)
    fit(m, "mat_normal", [[("a_1", RED), ("a_2", RED), ("b_1", BLUE)],
                          [(None, RED), (None, RED), ("b_2", BLUE)]],
        15, 0.78, 0.50, delim=("(", ")"))
    fit(m, "vec_map", [[("\\mathbf{a\\ ,\\ b\\ \\Rightarrow}", RED),
                        ("\\ \\mathbf{u\\ ,\\ v}", BLUE)]], 14, 1.38, 0.27)
    pink = [[(f"u_{s}", RED), (f"v_{s}", BLUE2)]
            for s in ("1", "2", "3", "\\dots", "\\dots", "\\infty")]
    fit(m, "vec_pink", pink, 14, 0.70, 1.55)
    kern = [[("u_1", RED), ("u_2", RED), ("u_3", RED), ("\\dots", RED),
             ("\\dots", RED), ("u_\\infty", RED), ("v_1", BLUE2)]]
    for s in ("2", "3", "\\dots", "\\dots", "\\infty"):
        kern.append([(None, RED)] * 6 + [(f"v_{s}", BLUE2)])
    fit(m, "mat_kernel", kern, 14, 2.42, 1.50, delim=("(", ")"))
    fit(m, "calc_atb", [[("\\mathit{Calculate}\\ ", BLACK),
                         ("\\mathbf{a^{T}\\,b}", RED)]], 14, 1.15, 0.25)
    fit(m, "calc_utv", [[("\\mathit{Calculate}\\ ", BLACK),
                         ("\\mathbf{u^{T}\\,v}", RED)]], 14, 1.15, 0.25)
    with open(os.path.join(OUT, "manifest.json"), "w") as fh:
        json.dump(m, fh, indent=2)
    print(json.dumps({k: {"w_in": v["w_in"], "h_in": v["h_in"]} for k, v in m.items()}))


if __name__ == "__main__":
    main()
