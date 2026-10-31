#!/usr/bin/env python3
"""Render slide_028 (rb4) equation assets via render_math.py into eq_028/.

Fix vs rb3: column vectors now cap TOTAL width to the spec box (tall parens
are rendered narrow then vertically stretched, PowerPoint-style) instead of
letting huge paren glyphs balloon the canvas. Writes rb4_<name>.png +
manifest_rb4.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import render_math as rm
from render_math import DPI

EQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_028")
W, H = 13.33, 7.5
R, B, K = "#FF0033", "#0000FF", "#000000"
GAP = 10

A = ("\\alpha_{1}^{2},\\ \\alpha_{2}^{2},\\ \\sqrt{2}\\alpha_{1}\\alpha_{2},"
     "\\ \\sqrt{2}\\alpha_{1},\\ \\sqrt{2}\\alpha_{2},\\ 1")

ROWS = {
    "chip":   ([0.073, 0.256, 0.133, 0.300], [(R, "\\left(a^{T}b+1\\right)")], None),
    "sq":     ([0.139, 0.254, 0.154, 0.281], [(K, "^{2}\\;=")], None),
    "arow":   ([0.154, 0.178, 0.367, 0.207], [(R, "\\left(" + A + "\\right)")], None),
    "bcol":   ([0.371, 0.167, 0.429, 0.398], [(B, e) for e in
               ["\\beta_{1}^{2}", "\\beta_{2}^{2}", "\\sqrt{2}\\beta_{1}\\beta_{2}",
                "\\sqrt{2}\\beta_{1}", "\\sqrt{2}\\beta_{2}", "1"]], ("(", ")^{T}", B)),
    "eq":     ([0.443, 0.265, 0.518, 0.296], [(K, "=\\;\\phi(a)^{T}\\phi(b)")], None),
    "where":  ([0.550, 0.250, 0.651, 0.302],
               [(K, "Where:\\;\\phi(x)\\;=\\;"),
                (K, "\\left(\\overset{x_{1}}{x_{2}}\\right)^{T}")], None),
    "arrow":  ([0.690, 0.267, 0.704, 0.291], [(R, "\\Rightarrow")], None),
    "phicol": ([0.717, 0.167, 0.773, 0.398], [(K, e) for e in
               ["x_{1}^{2}", "x_{2}^{2}", "\\sqrt{2}x_{1}x_{2}",
                "\\sqrt{2}x_{1}", "\\sqrt{2}x_{2}", "1"]], ("(", ")", K)),
    "a":      ([0.073, 0.444, 0.125, 0.528], [(R, "\\mathbf{a}\\;=\\;"),
               (R, "\\left(\\overset{1}{2}\\right)^{T}")], None),
    "b":      ([0.146, 0.444, 0.200, 0.528], [(B, "\\mathbf{b}\\;=\\;"),
               (B, "\\left(\\overset{3}{4}\\right)^{T}")], None),
    "leq":    ([0.073, 0.615, 0.169, 0.652], [(K, "\\phi(a)^{T}\\phi(b)\\;=")], None),
    "row":    ([0.175, 0.541, 0.388, 0.574],
               [(R, "\\left(1^{2},\\ 2^{2},\\ \\sqrt{2}\\,1*2,\\ \\sqrt{2},\\ 2\\sqrt{2},\\ 1\\right)")], None),
    "bcol2":  ([0.394, 0.537, 0.460, 0.737], [(B, e) for e in
               ["3^{2}", "4^{2}", "\\sqrt{2}\\,3*4", "3\\sqrt{2}", "4\\sqrt{2}", "1"]], ("(", ")^{T}", B)),
    "prod":   ([0.479, 0.587, 0.627, 0.617], [(K, "=\\;"),
               (R, "\\left(1,\\ 4,\\ 2\\sqrt{2},\\ \\sqrt{2},\\ 2\\sqrt{2},\\ 1\\right)")], None),
    "numcol": ([0.654, 0.533, 0.710, 0.741], [(B, e) for e in
               ["9", "16", "12\\sqrt{2}", "3\\sqrt{2}", "4\\sqrt{2}", "1"]], ("(", ")", B)),
    "sum":    ([0.461, 0.746, 0.652, 0.778], [(K, "=\\;9+64+48+6+16+1\\;=\\;144")], None),
    "bot":    ([0.073, 0.787, 0.346, 0.824], [(K, "|\\;"), (R, "a^{T}"), (B, "b\\;+\\;1"),
               (K, "\\;|^{2}\\;=\\;(1+3+2*4+1)^{2}\\;=\\;12^{2}\\;=\\;144")], None),
}


def compose_row(segs, box):
    x0, y0, x1, y1 = box
    maxw, maxh = (x1 - x0) * W * 1.02, (y1 - y0) * H * 1.25
    row = "||".join(f"{c}:{latex}" for c, latex in segs)
    canvas, pt = rm.fit_row(row, 26.0, maxw, maxh)
    return canvas, pt


def vstretch(arr, target_h):
    idx = (np.arange(target_h) * arr.shape[0] / target_h).astype(int)
    return arr[idx]


def compose_col(entries, paren, box):
    """Stack entry rows; flank with parens rendered narrow then stretched tall."""
    x0, y0, x1, y1 = box
    maxw, maxh = (x1 - x0) * W, (y1 - y0) * H
    n = len(entries)
    ref = 40.0
    has_T = bool(paren) and paren[1].endswith("^{T}")
    paren_each = 0.085 if paren else 0.0
    t_allow = 0.12 if has_T else 0.0
    avail_w = max(0.05, maxw - 2 * paren_each - 3 * GAP / DPI - t_allow)
    widths = [rm.measure_segment(latex, color, ref)[0] for color, latex in entries]
    pt_w = ref * avail_w / max(widths)
    line_h = (maxh * DPI - GAP * (n - 1)) / n
    pt_h = line_h * 72.0 / DPI / 1.15
    pt = min(pt_h, pt_w, 24.0)
    parts = [rm.render_segment(latex, color, pt) for color, latex in entries]
    colw = max(p[0].shape[1] for p in parts)
    colh = sum(p[0].shape[0] for p in parts) + GAP * (n - 1)
    col = np.zeros((colh, colw, 4), dtype=np.uint8)
    y = 0
    for arr, _ in parts:
        x = (colw - arr.shape[1]) // 2
        col[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        y += arr.shape[0] + GAP
    if not paren:
        return col, pt
    lp, rp, pcolor = paren
    has_T = rp.endswith("^{T}")
    rp_glyph = ")" if has_T else rp
    allow_each = max(0.04, (maxw - colw / DPI - (0.09 if has_T else 0.04) - 2 * GAP / DPI) / 2)
    pt_p = 40.0
    la, _ = rm.render_segment(lp, pcolor, pt_p)
    while la.shape[1] / DPI > allow_each and pt_p > 4.0:
        pt_p *= 0.9
        la, _ = rm.render_segment(lp, pcolor, pt_p)
    ra, _ = rm.render_segment(rp_glyph, pcolor, pt_p)
    la, ra = vstretch(la, colh), vstretch(ra, colh)
    extra = 0
    if has_T:
        ta, _ = rm.render_segment("^{T}", pcolor, pt)
        extra = ta.shape[1]
    w = la.shape[1] + GAP + colw + GAP + ra.shape[1] + (GAP + extra if has_T else 0)
    assert w <= maxw * DPI * 1.05, f"column too wide: {w/DPI:.3f} > {maxw:.3f}"
    h = colh
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    canvas[0:la.shape[0], 0:la.shape[1]] = la
    canvas[0:colh, la.shape[1] + GAP:la.shape[1] + GAP + colw] = col
    xr = la.shape[1] + GAP + colw + GAP
    canvas[0:ra.shape[0], xr:xr + ra.shape[1]] = ra
    if has_T:
        canvas[0:ta.shape[0], xr + ra.shape[1] + GAP:xr + ra.shape[1] + GAP + ta.shape[1]] = ta
    return canvas, pt


man = {}
for name, (box, segs, paren) in ROWS.items():
    if paren:
        canvas, pt = compose_col(segs, paren, box)
    else:
        canvas, pt = compose_row(segs, box)
    fn = f"rb4_{name}.png"
    Image.fromarray(canvas).save(os.path.join(EQ, fn))
    ys, xs = np.where(canvas[..., 3] > 10)
    man[name] = {
        "file": fn,
        "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
        "w_in": round(canvas.shape[1] / DPI, 5), "h_in": round(canvas.shape[0] / DPI, 5),
        "pt": round(pt, 2), "box": box,
        "ink_bbox": [int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())],
    }
    print(name, man[name]["w_in"], man[name]["h_in"], man[name]["pt"])

with open(os.path.join(EQ, "manifest_rb4.json"), "w") as fh:
    json.dump(man, fh, indent=2)
print("manifest_rb4.json written:", len(man), "assets")
