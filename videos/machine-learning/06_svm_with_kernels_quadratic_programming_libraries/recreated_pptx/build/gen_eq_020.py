#!/usr/bin/env python3
"""Render slide_020 2D math assets (spec qa/reanalysis2/slide_020_analysis.txt section 8)
into build/eq_020/ at 600 dpi, plus eq_020/manifest.json with w_in/h_in."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
from render_math import render_segment, DPI

OUT = os.path.join(HERE, "eq_020")
RED, BLUE, GREEN, BLACK = "#C00000", "#0000CC", "#00B050", "#000000"


def seg(latex, color, size):
    return render_segment(latex, color, size)  # (arr, baseline)


def tall_delim(glyph, color, size, target_h_px):
    """Render a single delimiter glyph scaled (by font size) to ~target_h_px tall."""
    arr, _ = seg(glyph, color, size)
    scale = target_h_px / arr.shape[0]
    arr, _ = seg(glyph, color, size * scale)
    return arr


def compose(rows, rowgap=10, seggap=6):
    """rows: list of rows; each row = list of (arr, baseline, xoff). Baseline-aligned."""
    row_meta = []
    for row in rows:
        row = [(t[0], t[1], t[2]) if len(t) == 3 else (t[0], t[1], 0) for t in row]
        base = max(b for _, b, _ in row)
        h = max(a.shape[0] for a, _, _ in row)
        w = max(x + a.shape[1] for a, _, x in row)
        row_meta.append((row, base, h, w))
    W = max(w for _, _, _, w in row_meta)
    H = sum(h for _, _, h, _ in row_meta) + rowgap * (len(rows) - 1)
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    y = 0
    for row, base, h, _ in row_meta:
        for arr, b, x in row:
            yy = y + (base - b)
            canvas[yy:yy + arr.shape[0], x:x + arr.shape[1]] = arr
        y += h + rowgap
    return canvas


def fit(fn, max_w_in, max_h_in, size, min_size=6.0):
    pt = size
    while pt >= min_size:
        canvas = fn(pt)
        if canvas.shape[1] / DPI <= max_w_in and canvas.shape[0] / DPI <= max_h_in:
            return canvas, pt
        pt -= 0.5
    canvas = fn(min_size)
    return canvas, min_size


def blank(w_px):
    return (np.zeros((2, max(int(w_px), 1), 4), dtype=np.uint8), 1, 0)


def _hstack(items, gap=5):
    """items: list of (arr, vcenter) — vertically centered horizontal stack."""
    H = max(a.shape[0] for a, _ in items)
    W = sum(a.shape[1] for a, _ in items) + gap * (len(items) - 1)
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    x = 0
    for arr, _ in items:
        y0 = (H - arr.shape[0]) // 2
        canvas[y0:y0 + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1] + gap
    return canvas


def vec_matrix(pt):
    """( a1 , | b1 ; a2 , | b2 ) — one outer paren pair (green left, blue right), a
    full-height green separator bar between the alpha column and the b column,
    per-row commas — matches the original input box pixels."""
    a1, ab1 = seg(r"\alpha_{1}", RED, pt)
    a2, ab2 = seg(r"\alpha_{2}", RED, pt)
    b1, bb1 = seg(r"b_{1}", BLUE, pt)
    b2, bb2 = seg(r"b_{2}", BLUE, pt)
    c1, cb1 = seg(r",", BLACK, pt)
    c2, cb2 = seg(r",", BLACK, pt)
    acol = compose([[(a1, ab1, 0)], [(a2, ab2, 0)]], rowgap=280)
    bcol = compose([[(b1, bb1, 0)], [(b2, bb2, 0)]], rowgap=280)
    ccol = compose([[(c1, cb1, 0)], [(c2, cb2, 0)]], rowgap=280)
    h = max(acol.shape[0], bcol.shape[0])
    lp = tall_delim("(", GREEN, pt, int(h * 1.05))
    rp = tall_delim(")", BLUE, pt, int(h * 1.05))
    bar = tall_delim(r"\vert", "#00B050", pt, int(h * 1.02))
    return _hstack([(lp, 0), (acol, 0), (ccol, 0), (bar, 0), (bcol, 0), (rp, 0)], gap=6)


def _place(segs, gap=6):
    x = 0
    for a, b in segs:
        yield x, (a, b)
        x += a.shape[1] + gap


def calc_row(pt, sym2):
    """Calculate a^T b — the superscript T is drawn at full size, raised above the baseline."""
    c, cb = seg(r"\mathsf{Calculate}\quad", BLACK, pt)
    a, ab = seg(r"\boldsymbol{" + sym2[0] + r"}", RED, pt)
    T, tb = seg(r"\boldsymbol{\mathrm{T}}", RED, pt)
    b, bb = seg(r"\boldsymbol{" + sym2[1] + r"}", RED if sym2[2] == "r" else BLUE, pt)
    base = max(cb, ab, bb)
    raise_px = max(2, int(T.shape[0] * 0.35))
    H = max(c.shape[0], a.shape[0], b.shape[0]) + raise_px + 2
    W = c.shape[1] + 8 + a.shape[1] + 4 + T.shape[1] + 6 + b.shape[1]
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    yb = raise_px + max(cb, ab, bb)  # main baseline row
    canvas[yb - cb:yb - cb + c.shape[0], 0:c.shape[1]] = c
    x = c.shape[1] + 8
    canvas[yb - ab:yb - ab + a.shape[0], x:x + a.shape[1]] = a
    x += a.shape[1] + 4
    canvas[yb - raise_px - tb:yb - raise_px - tb + T.shape[0], x:x + T.shape[1]] = T
    x += T.shape[1] + 6
    canvas[yb - bb:yb - bb + b.shape[0], x:x + b.shape[1]] = b
    return canvas


def map_arrow(pt):
    return compose([[seg(r"\boldsymbol{a,\ b\ \Rightarrow\ u,\ v}", RED, pt)]], rowgap=0)


def norm_mtx(pt):
    """[ a1 a2 ] [ b1 ; b2 ] — row vector times column vector: green brackets on the
    alpha group, blue brackets on the b column."""
    row = compose([[ (a, b, x) for x, (a, b) in _place([seg(r"\alpha_{1}", RED, pt), seg(r"\alpha_{2}", RED, pt)], gap=8) ]], rowgap=0)
    b1, bb1 = seg(r"b_{1}", BLUE, pt)
    b2, bb2 = seg(r"b_{2}", BLUE, pt)
    bcol = compose([[(b1, bb1, 0)], [(b2, bb2, 0)]], rowgap=4)
    h = max(row.shape[0], bcol.shape[0])
    lb = tall_delim("[", GREEN, pt, int(h * 1.05))
    mid = tall_delim("][", GREEN, pt, int(h * 1.05))
    rb = tall_delim("]", BLUE, pt, int(h * 1.05))
    return _hstack([(lb, 0), (row, 0), (mid, 0), (bcol, 0), (rb, 0)], gap=5)


def uv_mtx(pt):
    """Tall [ u_i , v_i ] matrix — green left bracket, blue right bracket, blue entries."""
    labels = [(r"u_{1}", r"v_{1}"), (r"u_{2}", r"v_{2}"), (r"u_{3}", r"v_{3}"),
              (r"\vdots", r"\vdots"), (r"u_{n}", r"v_{n}")]
    rows = []
    for ul, vl in labels:
        u, ub = seg(ul, BLUE, pt)
        c, cb = seg(r",", BLACK, pt)
        v, vb = seg(vl, BLUE, pt)
        g = 5
        x_v = u.shape[1] + g + c.shape[1] + g
        rows.append([(u, ub, 0), (c, cb, u.shape[1] + g), (v, vb, x_v)])
    body = compose(rows, rowgap=8)
    h = body.shape[0]
    lb = tall_delim("[", GREEN, pt, int(h * 0.98))
    rb = tall_delim("]", BLUE, pt, int(h * 0.98))
    W = lb.shape[1] + 12 + body.shape[1] + 26 + rb.shape[1]
    H = max(h, lb.shape[0], rb.shape[0])
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    y0 = (H - lb.shape[0]) // 2
    canvas[y0:y0 + lb.shape[0], 0:lb.shape[1]] = lb
    x = lb.shape[1] + 12
    canvas[(H - h) // 2:(H - h) // 2 + h, x:x + body.shape[1]] = body
    x += body.shape[1] + 26
    y0 = (H - rb.shape[0]) // 2
    canvas[y0:y0 + rb.shape[0], x:x + rb.shape[1]] = rb
    return canvas


def kern_uv(pt):
    """Horizontal header row u1 u2 u3 ... ... un across the top, v1..vn as a right-hand
    column descending below it (blue) — matches the original green panel."""
    top, _ = seg(r"u_{1}\ u_{2}\ u_{3}\ \cdots\ \cdots\ u_{n}", BLUE, pt)
    vlabels = [r"v_{1}", r"v_{2}", r"v_{3}", r"\vdots", r"v_{n}"]
    vrows = []
    for vl in vlabels:
        v, vb = seg(vl, BLUE, pt)
        vrows.append([(v, vb, 0)])
    vcol = compose(vrows, rowgap=10)
    gap = 14
    W = top.shape[1]
    H = top.shape[0] + gap + vcol.shape[0]
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    canvas[0:top.shape[0], 0:top.shape[1]] = top
    x = W - vcol.shape[1]
    canvas[top.shape[0] + gap:H, x:x + vcol.shape[1]] = vcol
    return canvas


SPECS = {
    "eq20_vec":      (vec_matrix, 1.16, 0.84, 14),
    "eq20_calc_a":   (lambda pt: calc_row(pt, ("a", "b", "b")), 2.10, 0.34, 24),
    "eq20_calc_u":   (lambda pt: calc_row(pt, ("u", "v", "r")), 1.90, 0.36, 24),
    "eq20_map":      (map_arrow, 1.70, 0.30, 18),
    "eq20_norm_mtx": (norm_mtx, 1.35, 0.80, 18),
    "eq20_uv_mtx":   (uv_mtx, 1.18, 2.20, 18),
    "eq20_kern_uv":  (kern_uv, 2.70, 1.18, 20),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for name, (fn, maxw, maxh, size) in SPECS.items():
        canvas, pt = fit(fn, maxw, maxh, size)
        path = os.path.join(OUT, name + ".png")
        Image.fromarray(canvas).save(path)
        w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
        manifest[name] = {"path": path, "w_in": round(w_in, 5), "h_in": round(h_in, 5),
                          "fontsize_pt": pt}
        print(f"{name}: {w_in:.3f} x {h_in:.3f} in @ {pt}pt")
    with open(os.path.join(OUT, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    print("wrote eq_020/manifest.json")


if __name__ == "__main__":
    main()
