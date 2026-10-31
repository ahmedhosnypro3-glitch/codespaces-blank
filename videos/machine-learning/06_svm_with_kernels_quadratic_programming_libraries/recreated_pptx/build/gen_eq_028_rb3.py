#!/usr/bin/env python3
"""Render slide_028 (rb3) equation assets via render_math.py into eq_028/.

Column vectors are composed from individually rendered rows (nested \\overset
does NOT stack in matplotlib 3.11 mathtext), with tall paren PNGs rendered at
a matched font size. Writes rb3_<name>.png + manifest_rb3.json.
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

A = "\\alpha_{1}^{2},\\ \\alpha_{2}^{2},\\ \\sqrt{2}\\alpha_{1}\\alpha_{2},\\ \\sqrt{2}\\alpha_{1},\\ \\sqrt{2}\\alpha_{2},\\ 1"

ROWS = {
    "chip":   ([0.073, 0.256, 0.133, 0.300], [(R, "a^{T}b+1")], None),
    "sq":     ([0.139, 0.254, 0.154, 0.281], [(K, "^{2}\\;=")], None),
    "arow":   ([0.154, 0.178, 0.367, 0.207], [(R, "\\left(" + A + "\\right)")], None),
    "bcol":   ([0.371, 0.167, 0.429, 0.398], [(B, e) for e in
               ["\\beta_{1}^{2}", "\\beta_{2}^{2}", "\\sqrt{2}\\beta_{1}\\beta_{2}",
                "\\sqrt{2}\\beta_{1}", "\\sqrt{2}\\beta_{2}", "1"]], ("(", ")^{T}", B)),
    "eq":     ([0.443, 0.265, 0.518, 0.296], [(K, "=\\;\\phi(a)^{T}\\phi(b)")], None),
    "where":  ([0.550, 0.250, 0.651, 0.302],
               [(K, "Where:\\;\\phi(x)\\;=\\;"), (K, "\\left(\\overset{x_{1}}{x_{2}}\\right)^{T}")], None),
    "arrow":  ([0.690, 0.267, 0.704, 0.291], [(R, "\\Rightarrow")], None),
    "phicol": ([0.717, 0.167, 0.773, 0.398], [(K, e) for e in
               ["x_{1}^{2}", "x_{2}^{2}", "\\sqrt{2}x_{1}x_{2}",
                "\\sqrt{2}x_{1}", "\\sqrt{2}x_{2}", "1"]], ("(", ")", K)),
    "a":      ([0.073, 0.444, 0.125, 0.528], [(R, "\\mathbf{a}\\;=\\;"), (R, "\\left(\\overset{1}{2}\\right)^{T}")], None),
    "b":      ([0.146, 0.444, 0.200, 0.528], [(B, "\\mathbf{b}\\;=\\;"), (B, "\\left(\\overset{3}{4}\\right)^{T}")], None),
    "leq":    ([0.073, 0.615, 0.169, 0.652], [(K, "\\phi(a)^{T}\\phi(b)\\;=")], None),
    "row":    ([0.175, 0.541, 0.388, 0.574], [(R, "\\left(1^{2},\\ 2^{2},\\ \\sqrt{2}\\,1{\\cdot}2,\\ \\sqrt{2},\\ 2\\sqrt{2},\\ 1\\right)")], None),
    "bcol2":  ([0.394, 0.537, 0.460, 0.737], [(B, e) for e in
               ["3^{2}", "4^{2}", "\\sqrt{2}\\,3{\\cdot}4", "3\\sqrt{2}", "4\\sqrt{2}", "1"]], ("(", ")^{T}", B)),
    "prod":   ([0.479, 0.587, 0.627, 0.617], [(K, "=\\;"), (R, "\\left(1,\\ 4,\\ 2\\sqrt{2},\\ \\sqrt{2},\\ 2\\sqrt{2},\\ 1\\right)")], None),
    "numcol": ([0.654, 0.533, 0.710, 0.741], [(B, e) for e in
               ["9", "16", "12\\sqrt{2}", "3\\sqrt{2}", "4\\sqrt{2}", "1"]], ("(", ")", B)),
    "sum":    ([0.461, 0.746, 0.652, 0.778], [(K, "=\\;9+64+48+6+16+1\\;=\\;144")], None),
    "bot":    ([0.073, 0.787, 0.346, 0.824], [(K, "|\\;"), (R, "a^{T}"), (B, "b\\;+\\;1"),
               (K, "\\;|^{2}\\;=\\;(1+3+2{\\cdot}4+1)^{2}\\;=\\;12^{2}\\;=\\;144")], None),
}


def compose_row(segs, box):
    x0, y0, x1, y1 = box
    maxw, maxh = (x1 - x0) * W * 1.02, (y1 - y0) * H * 1.12
    row = "||".join(f"{c}:{latex}" for c, latex in segs)
    canvas, pt = rm.fit_row(row, 26.0, maxw, maxh)
    return canvas, pt


def compose_col(entries, paren, box):
    """Stack entry rows vertically; flank with tall paren PNGs."""
    x0, y0, x1, y1 = box
    maxw, maxh = (x1 - x0) * W, (y1 - y0) * H * 1.05
    n = len(entries)
    gap = 6
    line_h = (maxh * DPI - gap * (n - 1)) / n
    pt_h = line_h * 72.0 / DPI / 1.25
    ref = 40.0
    widths = [rm.measure_segment(latex, color, ref)[0] for color, latex in entries]
    paren_allow = 0.16  # inches reserved for the two squeezed paren glyphs
    pt_w = ref * max(0.2, (maxw - paren_allow)) / max(widths)
    pt = min(pt_h, pt_w, 26.0)
    parts = [rm.render_segment(latex, color, pt) for color, latex in entries]
    colw = max(p[0].shape[1] for p in parts)
    colh = sum(p[0].shape[0] for p in parts) + gap * (n - 1)
    col = np.zeros((colh, colw, 4), dtype=np.uint8)
    y = 0
    for arr, _ in parts:
        x = (colw - arr.shape[1]) // 2
        col[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        y += arr.shape[0] + gap
    if not paren:
        return col, pt
    lp, rp, pcolor = paren
    paren_pt = pt * 6.0
    for _ in range(4):
        la, _ = rm.render_segment("\\left" + lp + "\\vphantom{x}" if False else lp, pcolor, paren_pt)
        ra, _ = rm.render_segment(rp, pcolor, paren_pt)
        ph = max(la.shape[0], ra.shape[0])
        if abs(ph - colh) < 0.06 * colh:
            break
        paren_pt *= colh / max(ph, 1)
    la, _ = rm.render_segment(lp, pcolor, paren_pt)
    ra, _ = rm.render_segment(rp, pcolor, paren_pt)
    # squeeze parens horizontally to mimic stretchy PowerPoint delimiters
    target_w = max(12, int(0.07 * DPI))
    la = np.asarray(Image.fromarray(la).resize((target_w, la.shape[0]), Image.LANCZOS))
    ra = np.asarray(Image.fromarray(ra).resize((target_w, ra.shape[0]), Image.LANCZOS))
    w = la.shape[1] + colw + ra.shape[1] + 2 * gap
    h = max(colh, la.shape[0], ra.shape[0])
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    canvas[(h - la.shape[0]) // 2:(h - la.shape[0]) // 2 + la.shape[0], 0:la.shape[1]] = la
    canvas[(h - colh) // 2:(h - colh) // 2 + colh, la.shape[1] + gap:la.shape[1] + gap + colw] = col
    x0r = la.shape[1] + gap + colw + gap
    canvas[(h - ra.shape[0]) // 2:(h - ra.shape[0]) // 2 + ra.shape[0], x0r:x0r + ra.shape[1]] = ra
    return canvas, pt


man = {}
for name, (box, segs, paren) in ROWS.items():
    if paren:
        canvas, pt = compose_col(segs, paren, box)
    else:
        canvas, pt = compose_row(segs, box)
    fn = f"rb3_{name}.png"
    Image.fromarray(canvas).save(os.path.join(EQ, fn))
    ys, xs = np.where(canvas[..., 3] > 10)
    man[name] = {
        "file": fn,
        "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
        "w_in": round(canvas.shape[1] / DPI, 5), "h_in": round(canvas.shape[0] / DPI, 5),
        "pt": round(pt, 2), "box": box,
        "ink_bbox": [int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())],
    }
    print(name, man[name]["w_in"], man[name]["h_in"], man[name]["pt"], man[name]["ink_bbox"])

with open(os.path.join(EQ, "manifest_rb3.json"), "w") as fh:
    json.dump(man, fh, indent=2)
print("manifest_rb3.json written:", len(man), "assets")
