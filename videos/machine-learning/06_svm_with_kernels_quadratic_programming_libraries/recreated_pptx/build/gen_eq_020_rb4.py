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


def vec_matrix(pt):
    """Two column vectors ( a1 / a2 ) , ( b1 / b2 ) — green left paren around the
    alpha column, blue right paren around the b column, comma between."""
    acol = compose([[(seg(r"\alpha_{1}", RED, pt)[0], seg(r"\alpha_{1}", RED, pt)[1], 0)],
                    [(seg(r"\alpha_{2}", RED, pt)[0], seg(r"\alpha_{2}", RED, pt)[1], 0)]], rowgap=4)
    bcol = compose([[(seg(r"b_{1}", BLUE, pt)[0], seg(r"b_{1}", BLUE, pt)[1], 0)],
                    [(seg(r"b_{2}", BLUE, pt)[0], seg(r"b_{2}", BLUE, pt)[1], 0)]], rowgap=4)
    cma, cmb = seg(r",", BLACK, pt)
    h = max(acol.shape[0], bcol.shape[0], cma.shape[0])
    body_h = h
    lp = tall_delim("(", GREEN, pt, int(body_h * 1.05))
    rp = tall_delim(")", BLUE, pt, int(body_h * 1.05))
    g = 6
    W = lp.shape[1] + g + acol.shape[1] + g + cma.shape[1] + g + bcol.shape[1] + g + rp.shape[1]
    H = max(body_h, lp.shape[0], rp.shape[0])
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    y0 = (H - lp.shape[0]) // 2
    canvas[y0:y0 + lp.shape[0], 0:lp.shape[1]] = lp
    x = lp.shape[1] + g
    canvas[(H - acol.shape[0]) // 2:(H - acol.shape[0]) // 2 + acol.shape[0], x:x + acol.shape[1]] = acol
    x += acol.shape[1] + g
    yc = (H - cma.shape[0]) // 2
    canvas[yc:yc + cma.shape[0], x:x + cma.shape[1]] = cma
    x += cma.shape[1] + g
    canvas[(H - bcol.shape[0]) // 2:(H - bcol.shape[0]) // 2 + bcol.shape[0], x:x + bcol.shape[1]] = bcol
    x += bcol.shape[1] + g
    y0 = (H - rp.shape[0]) // 2
    canvas[y0:y0 + rp.shape[0], x:x + rp.shape[1]] = rp
    return canvas


def _place(segs, gap=6):
    x = 0
    for a, b in segs:
        yield x, (a, b)
        x += a.shape[1] + gap


def calc_row(pt, sym2):
    r = [seg(r"\mathsf{Calculate}\ ", BLACK, pt),
         seg(r"\boldsymbol{" + sym2[0] + r"^{T}}", RED, pt),
         seg(r"\boldsymbol{" + sym2[1] + "}", RED if sym2[2] == "r" else BLUE, pt)]
    return compose([[ (a, b, x) for x, (a, b) in _place(r, gap=2) ]], rowgap=0)


def map_arrow(pt):
    return compose([[seg(r"\boldsymbol{a,\ b\ \Rightarrow\ u,\ v}", RED, pt)]], rowgap=0)


def norm_mtx(pt):
    """[ a1 a2 | b1 ; b2 ] — tall dark brackets around the matrix (judge: missing
    multiplication brackets), green vertical separator, red a's, blue b's."""
    a1, a1b = seg(r"\alpha_{1}", RED, pt)
    a2, a2b = seg(r"\alpha_{2}", RED, pt)
    bar, barb = seg(r"\vert", GREEN, pt)
    b1, b1b = seg(r"b_{1}", BLUE, pt)
    b2, b2b = seg(r"b_{2}", BLUE, pt)
    g = 5
    x_a2 = a1.shape[1] + g
    x_bar = x_a2 + a2.shape[1] + g
    x_b = x_bar + bar.shape[1] + g
    r1 = [(a1, a1b, 0), (a2, a2b, x_a2), (bar, barb, x_bar), (b1, b1b, x_b)]
    r2 = [(b2, b2b, x_b)]
    body = compose([r1, r2], rowgap=6)
    h = body.shape[0]
    lb = tall_delim("[", BLACK, pt, int(h * 1.04))
    rb = tall_delim("]", BLACK, pt, int(h * 1.04))
    W = lb.shape[1] + 5 + body.shape[1] + 5 + rb.shape[1]
    H = max(h, lb.shape[0], rb.shape[0])
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    y0 = (H - lb.shape[0]) // 2
    canvas[y0:y0 + lb.shape[0], 0:lb.shape[1]] = lb
    x = lb.shape[1] + 5
    canvas[(H - h) // 2:(H - h) // 2 + h, x:x + body.shape[1]] = body
    x += body.shape[1] + 5
    y0 = (H - rb.shape[0]) // 2
    canvas[y0:y0 + rb.shape[0], x:x + rb.shape[1]] = rb
    return canvas


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
    lb = tall_delim("[", GREEN, pt, int(h * 1.04))
    rb = tall_delim("]", BLUE, pt, int(h * 1.04))
    W = lb.shape[1] + 5 + body.shape[1] + 5 + rb.shape[1]
    H = max(h, lb.shape[0], rb.shape[0])
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    y0 = (H - lb.shape[0]) // 2
    canvas[y0:y0 + lb.shape[0], 0:lb.shape[1]] = lb
    x = lb.shape[1] + 5
    canvas[(H - h) // 2:(H - h) // 2 + h, x:x + body.shape[1]] = body
    x += body.shape[1] + 5
    y0 = (H - rb.shape[0]) // 2
    canvas[y0:y0 + rb.shape[0], x:x + rb.shape[1]] = rb
    return canvas


def kern_uv(pt):
    """Top row u1 u2 u3 ... ... un plus right-hand column v1..vn (blue)."""
    top, tb = seg(r"u_{1}\ u_{2}\ u_{3}\ \cdots\ \cdots\ u_{n}", BLUE, pt)
    vlabels = [r"v_{1}", r"v_{2}", r"v_{3}", r"\vdots", r"v_{n}"]
    vrows = []
    for vl in vlabels:
        v, vb = seg(vl, BLUE, pt)
        vrows.append([(v, vb, 0)])
    vcol = compose(vrows, rowgap=8)
    gap = 12
    W = top.shape[1]
    H = top.shape[0] + gap + vcol.shape[0]
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    canvas[0:top.shape[0], (W - top.shape[1]) // 2:(W + top.shape[1]) // 2] = top
    x = W - vcol.shape[1]
    canvas[top.shape[0] + gap:H, x:x + vcol.shape[1]] = vcol
    return canvas


SPECS = {
    "eq20_vec":      (vec_matrix, 1.10, 0.80, 16),
    "eq20_calc_a":   (lambda pt: calc_row(pt, ("a", "b", "b")), 3.90, 0.42, 13),
    "eq20_calc_u":   (lambda pt: calc_row(pt, ("u", "v", "r")), 3.70, 0.42, 13),
    "eq20_map":      (map_arrow, 1.90, 0.38, 15),
    "eq20_norm_mtx": (norm_mtx, 0.98, 0.80, 13),
    "eq20_uv_mtx":   (uv_mtx, 1.05, 2.20, 13),
    "eq20_kern_uv":  (kern_uv, 2.60, 1.90, 13),
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
