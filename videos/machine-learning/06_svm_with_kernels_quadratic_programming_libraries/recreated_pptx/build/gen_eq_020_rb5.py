#!/usr/bin/env python3
"""slide_020 eq assets, rb5: fix judge MAJORs from slide_020_judge_manual_0.txt.
- tall delimiters are PIL-stretched (thin strokes) instead of font-scaled (solid bars)
- kern_uv = two parallel VERTICAL columns (u left, v right), per judge vs original
- calc rows slightly larger so the superscript T reads
Writes eq_020/*.png + manifest.json (same keys as rb4 so slide_020.js is unchanged).
"""
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
    return render_segment(latex, color, size)


def tall_delim(glyph, color, size, target_h_px):
    """Render the glyph at base size, then stretch vertically with PIL so the
    stroke stays thin (font-scaling made tall brackets a solid bar)."""
    arr, _ = seg(glyph, color, size)
    im = Image.fromarray(arr)
    w = max(int(arr.shape[1] * (target_h_px / arr.shape[0]) ** 0.5), 2)
    im = im.resize((w, int(target_h_px)), Image.LANCZOS)
    return np.asarray(im), 1


def compose(rows, rowgap=10):
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
    return fn(min_size), min_size


def vec_matrix(pt):
    """( a1 / a2 ) , ( b1 / b2 ) — green left paren, blue right paren, thin via stretch."""
    acol = compose([[(seg(r"\alpha_{1}", RED, pt)[0], seg(r"\alpha_{1}", RED, pt)[1], 0)],
                    [(seg(r"\alpha_{2}", RED, pt)[0], seg(r"\alpha_{2}", RED, pt)[1], 0)]], rowgap=4)
    bcol = compose([[(seg(r"b_{1}", BLUE, pt)[0], seg(r"b_{1}", BLUE, pt)[1], 0)],
                    [(seg(r"b_{2}", BLUE, pt)[0], seg(r"b_{2}", BLUE, pt)[1], 0)]], rowgap=4)
    cma, cmb = seg(r",", BLACK, pt)
    h = max(acol.shape[0], bcol.shape[0])
    lp, _ = tall_delim("(", GREEN, pt, int(h * 1.05))
    rp, _ = tall_delim(")", BLUE, pt, int(h * 1.05))
    g = 6
    W = lp.shape[1] + g + acol.shape[1] + g + cma.shape[1] + g + bcol.shape[1] + g + rp.shape[1]
    H = max(h, lp.shape[0], rp.shape[0])
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    y0 = (H - lp.shape[0]) // 2
    canvas[y0:y0 + lp.shape[0], 0:lp.shape[1]] = lp
    x = lp.shape[1] + g
    ya = (H - acol.shape[0]) // 2
    canvas[ya:ya + acol.shape[0], x:x + acol.shape[1]] = acol
    x += acol.shape[1] + g
    yc = (H - cma.shape[0]) // 2
    canvas[yc:yc + cma.shape[0], x:x + cma.shape[1]] = cma
    x += cma.shape[1] + g
    yb = (H - bcol.shape[0]) // 2
    canvas[yb:yb + bcol.shape[0], x:x + bcol.shape[1]] = bcol
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
         seg(r"\boldsymbol{" + sym2[0] + r"^{\mathrm{T}}}", RED, pt),
         seg(r"\boldsymbol{" + sym2[1] + "}", RED if sym2[2] == "r" else BLUE, pt)]
    return compose([[(a, b, x) for x, (a, b) in _place(r, gap=2)]], rowgap=0)


def map_arrow(pt):
    return compose([[seg(r"\boldsymbol{a,\ b\ \Rightarrow\ u,\ v}", RED, pt)]], rowgap=0)


def norm_mtx(pt):
    """[ a1 a2 | b1 ; b2 ] — thin stretched brackets, green separator."""
    a1, a1b = seg(r"\alpha_{1}", RED, pt)
    a2, a2b = seg(r"\alpha_{2}", RED, pt)
    bar, barb = seg(r"\vert", GREEN, pt)
    b1, b1b = seg(r"b_{1}", BLUE, pt)
    b2, b2b = seg(r"b_{2}", BLUE, pt)
    g = 5
    x_a2 = a1.shape[1] + g
    x_bar = x_a2 + a2.shape[1] + g
    x_b = x_bar + bar.shape[1] + g
    body = compose([[(a1, a1b, 0), (a2, a2b, x_a2), (bar, barb, x_bar), (b1, b1b, x_b)],
                    [(b2, b2b, x_b)]], rowgap=6)
    h = body.shape[0]
    lb, _ = tall_delim("[", BLACK, pt, int(h * 1.04))
    rb, _ = tall_delim("]", BLACK, pt, int(h * 1.04))
    W = lb.shape[1] + 5 + body.shape[1] + 5 + rb.shape[1]
    H = max(h, lb.shape[0], rb.shape[0])
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    y0 = (H - lb.shape[0]) // 2
    canvas[y0:y0 + lb.shape[0], 0:lb.shape[1]] = lb
    x = lb.shape[1] + 5
    yh = (H - h) // 2
    canvas[yh:yh + h, x:x + body.shape[1]] = body
    x += body.shape[1] + 5
    y0 = (H - rb.shape[0]) // 2
    canvas[y0:y0 + rb.shape[0], x:x + rb.shape[1]] = rb
    return canvas


def uv_mtx(pt):
    """Tall [ u_i | v_i ] matrix — thin stretched brackets, full-height blue separator."""
    labels = [(r"u_{1}", r"v_{1}"), (r"u_{2}", r"v_{2}"), (r"u_{3}", r"v_{3}"),
              (r"\vdots", r"\vdots"), (r"u_{n}", r"v_{n}")]
    rows = []
    for ul, vl in labels:
        u, ub = seg(ul, BLUE, pt)
        v, vb = seg(vl, BLUE, pt)
        rows.append([(u, ub, 0), (v, vb, u.shape[1])])
    u_w = max(seg(ul, BLUE, pt)[0].shape[1] for ul, _ in labels)
    body = compose(rows, rowgap=10)
    h = body.shape[0]
    g = 8
    bar, _ = tall_delim(r"\vert", BLUE, pt, int(h * 1.0))
    lb, _ = tall_delim("[", GREEN, pt, int(h * 1.04))
    rb, _ = tall_delim("]", BLUE, pt, int(h * 1.04))
    x_bar = lb.shape[1] + g + u_w + 3
    W = lb.shape[1] + g + body.shape[1] + g + bar.shape[1] + g + rb.shape[1]
    W = max(W, x_bar + bar.shape[1] + g + rb.shape[1])
    H = max(h, lb.shape[0], rb.shape[0], bar.shape[0])
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    y0 = (H - lb.shape[0]) // 2
    canvas[y0:y0 + lb.shape[0], 0:lb.shape[1]] = lb
    x = lb.shape[1] + g
    yh = (H - h) // 2
    canvas[yh:yh + h, x:x + body.shape[1]] = body
    yb = (H - bar.shape[0]) // 2
    canvas[yb:yb + bar.shape[0], x_bar:x_bar + bar.shape[1]] = bar
    xr = W - rb.shape[1]
    y0 = (H - rb.shape[0]) // 2
    canvas[y0:y0 + rb.shape[0], xr:xr + rb.shape[1]] = rb
    return canvas


def kern_uv(pt):
    """Spec layout: horizontal u header row across the top, v column down the right."""
    top, tb = seg(r"u_{1}\ u_{2}\ u_{3}\ \cdots\ \cdots\ u_{n}", BLUE, pt)
    vcol = compose([[(seg(l, BLUE, pt)[0], seg(l, BLUE, pt)[1], 0)]
                    for l in (r"v_{1}", r"v_{2}", r"v_{3}", r"\vdots", r"v_{n}")], rowgap=10)
    gap = 14
    W = top.shape[1]
    H = top.shape[0] + gap + vcol.shape[0]
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    canvas[0:top.shape[0], (W - top.shape[1]) // 2:(W + top.shape[1]) // 2] = top
    x = W - vcol.shape[1]
    canvas[top.shape[0] + gap:H, x:x + vcol.shape[1]] = vcol
    return canvas


SPECS = {
    "eq20_vec":      (vec_matrix, 1.10, 0.80, 16),
    "eq20_calc_a":   (lambda pt: calc_row(pt, ("a", "b", "b")), 1.30, 0.28, 14),
    "eq20_calc_u":   (lambda pt: calc_row(pt, ("u", "v", "r")), 1.20, 0.27, 14),
    "eq20_map":      (map_arrow, 1.60, 0.26, 13),
    "eq20_norm_mtx": (norm_mtx, 0.95, 0.72, 12),
    "eq20_uv_mtx":   (uv_mtx, 1.10, 2.20, 12),
    "eq20_kern_uv":  (kern_uv, 2.30, 1.45, 12),
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
