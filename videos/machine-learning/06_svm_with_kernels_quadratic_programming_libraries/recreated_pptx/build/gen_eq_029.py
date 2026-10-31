#!/usr/bin/env python3
"""Fresh math assets for slide 029, rendered ONLY from
qa/reanalysis2/slide_029_analysis.txt section 8 (EQUATIONS).

Uses a local renderer: matplotlib mathtext at 600 dpi, tight transparent
PNG. NOTE: render_math._draw indexes buffer rows with bottom-origin text
extents (row 0 of buffer_rgba is the TOP), which clips glyphs to a sliver;
this script crops with the correct y-flip.

Bracketed row/column vectors of E3 are composed cell-by-cell (mathtext
lacks \\begin{array}); brackets are stretched delimiter glyphs.
Output: eq_029/*.png at 600 dpi + eq_029/manifest.json (file/w_in/h_in/pt).
"""
import json
import os
import sys

import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
PAD = 6
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_029")
RED = "#C00000"
BLUE = "#3333CC"
PHI = "#0000CC"
BLACK = "#000000"
COL_GAP = 14
ROW_GAP = 2


def seg(latex, color, size):
    """Render one latex segment -> (rgba array cropped to ink, baseline px
    from crop top)."""
    fig = plt.figure(figsize=(8.0, 4.0), dpi=DPI)
    fig.patch.set_alpha(0.0)
    txt = fig.text(0.02, 0.5, f"${latex}$", fontsize=size, color=color,
                   ha="left", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    H = buf.shape[0]
    bt = txt.get_window_extent(renderer=fig.canvas.get_renderer())
    plt.close(fig)
    y0 = max(H - int(bt.y1) - PAD, 0)          # top-origin crop rows
    y1 = min(H - int(bt.y0) + PAD + 1, H)
    x0 = max(int(bt.x0) - PAD, 0)
    x1 = min(int(bt.x1) + PAD + 1, buf.shape[1])
    crop = buf[y0:y1, x0:x1]
    if crop.shape[0] <= 0 or crop.shape[1] <= 0:
        raise SystemExit(f"no ink for {latex!r}")
    base = int(bt.y1) - int(0.5 * H) + PAD      # baseline px from crop top
    return crop, base


def parse_row(row):
    segs = []
    for part in row.split("||"):
        head = part.split("\\", 1)[0]
        if ":" in head:
            color, latex = part.split(":", 1)
        else:
            color, latex = "333333", part
        segs.append((color if color.startswith("#") else "#" + color, latex))
    return segs


def row_canvas(row, size):
    parts = [seg(lt, c, size) for c, lt in parse_row(row)]
    base = max(b for _, b in parts)
    h = max(base + (a.shape[0] - b) for a, b in parts) + PAD
    w = sum(a.shape[1] for a, _ in parts) + 2 * PAD
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    x = PAD
    for arr, b in parts:
        y = base - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1]
    return canvas


def compose(rows, size, delim=None):
    cells = [[None if lt is None else seg(lt, c, size) for lt, c in r]
             for r in rows]
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
    dl = np.asarray(Image.fromarray(seg(delim[0], BLACK, size)[0])
                    .resize((max(6, PAD // 2), bh), Image.BILINEAR))
    dr = np.asarray(Image.fromarray(seg(delim[1], BLACK, size)[0])
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
        canvas = row_canvas(row, size)
        if canvas.shape[1] / DPI <= maxw and canvas.shape[0] / DPI <= maxh:
            break
        size *= 0.93
    return save(name, canvas, size)


def fitgrid(name, rows, size0, maxw, maxh, delim=None):
    size = size0
    for _ in range(24):
        canvas = compose(rows, size, delim)
        if canvas.shape[1] / DPI <= maxw and canvas.shape[0] / DPI <= maxh:
            break
        size *= 0.92
    return save(name, canvas, size)


def main():
    m = {}
    # E1: RBF identity, inline superscript exponents; last two factors
    # blue-purple, final e^{ab} red. Region [0.090,0.185,0.477,0.222].
    m["e1"] = fitline("e1",
        "#000000:e^{-1/2(a-b)^{2}}=e^{-1/2(a^{2}+b^{2}-2ab)}="
        "||#3333CC:e^{-a^{2}/2}\\,e^{-b^{2}/2}\\ ||#CC0000:e^{ab}",
        30, 5.55, 0.42)
    # E2: Taylor series of e^{ab}, stacked fractions; e^{ab} and trailing
    # infinity red. Region [0.086,0.283,0.480,0.322].
    m["e2"] = fitline("e2",
        "#CC0000:e^{ab}||#000000: = 1+\\frac{ab}{1!}+\\frac{(ab)^{2}}{2!}"
        "+\\frac{(ab)^{3}}{3!}+\\frac{(ab)^{4}}{4!}+\\frac{(ab)^{5}}{5!}+\\dots\\dots"
        " ||#CC0000:\\infty",
        28, 5.60, 0.52)
    # E3 lead-in "e^{ab} =" at [0.090,0.393,0.127,0.426]
    m["e3_eq"] = fitline("e3_eq", "#CC0000:e^{ab}||#000000: =", 26, 0.50, 0.26)
    # E3 row vector [ a/sqrt1! a^2/sqrt2! a^3/sqrt3! a^4/sqrt4! ... ... inf ]
    m["e3_row"] = fitgrid("e3_row",
        [[(t, BLACK) for t in ("\\frac{a}{\\sqrt{1!}}", "\\frac{a^{2}}{\\sqrt{2!}}",
           "\\frac{a^{3}}{\\sqrt{3!}}", "\\frac{a^{4}}{\\sqrt{4!}}",
           "\\dots", "\\dots", "\\infty")]],
        28, 3.30, 0.55, delim=("[", "]"))
    # E3 column vector [ 1/b ; sqrt1!/b^2 ; ... ; ... inf ]
    m["e3_col"] = fitgrid("e3_col",
        [[(t, BLACK)] for t in ("\\frac{1}{b}", "\\frac{\\sqrt{1!}}{b^{2}}",
           "\\frac{\\sqrt{2!}}{b^{3}}", "\\frac{\\sqrt{3!}}{b^{4}}",
           "\\frac{\\sqrt{4!}}{\\dots}", "\\dots", "\\dots\\ \\infty")],
        20, 0.66, 2.80, delim=("[", "]"))
    # E4: e^x series, red trailing infinity, region [0.533,0.231,0.859,0.281]
    m["e4"] = fitline("e4",
        "#000000:e^{x} = 1+\\frac{x}{1!}+\\frac{x^{2}}{2!}+\\frac{x^{3}}{3!}"
        "+\\frac{x^{4}}{4!}+\\frac{x^{5}}{5!}+\\dots\\dots ||#CC0000:\\infty",
        26, 4.30, 0.37)
    # E5: e^3 series, red trailing infinity, region [0.533,0.311,0.854,0.365]
    m["e5"] = fitline("e5",
        "#000000:e^{3} = 1+\\frac{3}{1!}+\\frac{3^{2}}{2!}+\\frac{3^{3}}{3!}"
        "+\\frac{3^{4}}{4!}+\\frac{3^{5}}{5!}+\\dots\\dots ||#CC0000:\\infty",
        26, 4.25, 0.40)
    # phi labels: blue phi, red superscript T on phi(a)
    m["phi_a"] = fitline("phi_a", "#0000CC:\\phi(a)||#CC0000:^{\\mathrm{T}}",
                         30, 0.92, 0.40)
    m["phi_b"] = fitline("phi_b", "#0000CC:\\phi(b)", 30, 0.87, 0.42)
    with open(os.path.join(OUT, "manifest.json"), "w") as fh:
        json.dump(m, fh, indent=2)
    for k, v in m.items():
        print(k, v["w_in"], "x", v["h_in"], "in @", v["pt"], "pt")


if __name__ == "__main__":
    main()
