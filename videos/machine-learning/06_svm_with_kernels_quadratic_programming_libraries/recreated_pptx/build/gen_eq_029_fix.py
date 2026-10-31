#!/usr/bin/env python3
"""Corrected math-asset generator for slide 029 -> eq_029b/ (600-dpi PNGs).

Fix vs render_math.py: text bbox y-coords are bottom-origin; the old crop used
them as top-origin rows and clipped glyphs to their tops. Here y is flipped.
Placement manifest: x/y in inches, centered in each spec region.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
PAD = 6
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_029b")
os.makedirs(OUT, exist_ok=True)
W, H = 13.33, 7.5


def draw(latex, color, pt, need_w, need_h, dpi):
    fig_w = max(3.0, (need_w or 4.0) * 1.25 + 1.0)
    fig_h = max(fig_w / 2.0, (need_h or 1.0) * 2.6, 2.0)
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
    fig.patch.set_alpha(0.0)
    txt = fig.text(0.02, 0.5, f"${latex}$", fontsize=pt, color=color,
                   ha="left", va="baseline")
    probe = fig.text(0.02, 0.95, "x", fontsize=pt, color=color,
                     ha="left", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    r = fig.canvas.get_renderer()
    bt = txt.get_window_extent(renderer=r)
    be = probe.get_window_extent(renderer=r)
    plt.close(fig)
    Hpx = buf.shape[0]
    y0 = max(Hpx - int(bt.y1) - PAD, 0)
    y1 = min(Hpx - int(bt.y0) + PAD + 1, Hpx)
    x0 = max(int(bt.x0) - PAD, 0)
    x1 = min(int(bt.x1) + PAD + 1, buf.shape[1])
    crop = buf[y0:y1, x0:x1]
    base = (Hpx - int(be.y0)) - y0
    return crop, base


def measure(latex, color, pt):
    _, _, bt = None, None, None
    fig = plt.figure(figsize=(30.0, 8.0), dpi=72)
    t = fig.text(0.05, 0.5, f"${latex}$", fontsize=pt, color=color, va="baseline")
    fig.canvas.draw()
    bt = t.get_window_extent(renderer=fig.canvas.get_renderer())
    plt.close(fig)
    return bt.width / 72.0, bt.height / 72.0


def parse(row):
    segs = []
    for part in row.split("||"):
        head = part.split("\\", 1)[0]
        if ":" in head:
            c, lt = part.split(":", 1)
        else:
            c, lt = "333333", part
        segs.append((c if c.startswith("#") else "#" + c, lt))
    return segs


def fit_row(row, size, maxw, maxh, min_size=6.0):
    segs = parse(row)
    ms = [measure(lt, c, size) for c, lt in segs]
    tw = sum(w for w, _ in ms)
    th = max(h for _, h in ms)
    scale = min(maxw / tw, maxh / th)
    pt = max(min_size, size * scale * 0.995)
    need = [(w * scale, h * scale) for w, h in ms]
    for _ in range(4):
        parts = [draw(lt, c, pt, nw, nh, DPI) for (c, lt), (nw, nh) in zip(segs, need)]
        base = max(b for _, b in parts)
        h = max(base + (a.shape[0] - b) for a, b in parts) + PAD
        w = sum(a.shape[1] for a, _ in parts) + 2 * PAD
        if w / DPI <= maxw and h / DPI <= maxh:
            break
        pt *= 0.94
        need = [(nw * 0.94, nh * 0.94) for nw, nh in need]
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    x = PAD
    for (arr, b), _ in zip(parts, segs):
        y = base - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1]
    return canvas, pt

EQS = {
    "e1": ("000000:e^{-\\frac{1}{2}(a-b)^{2}} = e^{-\\frac{1}{2}(a^{2}+b^{2}-2ab)} = "
           "||3333CC:e^{-\\frac{a^{2}}{2}}\\,"
           "||3333CC:e^{-\\frac{b^{2}}{2}}\\,||CC0000:e^{ab}",
           (0.086, 0.170, 0.505, 0.227), 14, 5.6, 0.44),
    "e2": ("CC0000:e^{ab} = "
           "||000000:1 + \\frac{ab}{1!} + \\frac{(ab)^{2}}{2!} + \\frac{(ab)^{3}}{3!} "
           "+ \\frac{(ab)^{4}}{4!} + \\frac{(ab)^{5}}{5!} + ......\\,"
           "||CC0000:\\infty",
           (0.086, 0.266, 0.505, 0.326), 14, 5.45, 0.44),
    "e3_eq": ("CC0000:e^{ab} =", (0.090, 0.393, 0.127, 0.426), 14, 0.5, 0.25),
    "e3_row": ("000000:\\left[\\ 1\\ \\frac{a}{\\sqrt{1!}}\\ \\frac{a^{2}}{\\sqrt{2!}}\\ "
               "\\frac{a^{3}}{\\sqrt{3!}}\\ \\frac{a^{4}}{\\sqrt{4!}}\\ ...\\ ...\\ \\infty\\ \\right]",
               (0.130, 0.389, 0.365, 0.444), 14, 3.14, 0.42),
    "e3_col": (None, (0.398, 0.395, 0.508, 0.785), 14, 1.45, 2.9),
    "e4": ("000000:e^{x} = 1 + \\frac{x}{1!} + \\frac{x^{2}}{2!} + \\frac{x^{3}}{3!} "
           "+ \\frac{x^{4}}{4!} + \\frac{x^{5}}{5!} + ......\\,||CC0000:\\infty",
           (0.533, 0.231, 0.859, 0.281), 13, 4.34, 0.37),
    "e5": ("000000:e^{3} = 1 + \\frac{3}{1!} + \\frac{3^{2}}{2!} + \\frac{3^{3}}{3!} "
           "+ \\frac{3^{4}}{4!} + \\frac{3^{5}}{5!} + ......\\,||CC0000:\\infty",
           (0.533, 0.311, 0.854, 0.365), 13, 4.27, 0.40),
    "phi_a": ("0000CC:\\phi(a)||CC0000:^{\\mathrm{T}}", (0.182, 0.467, 0.251, 0.520), 14, 0.92, 0.40),
    "phi_b": ("0000CC:\\phi(b)", (0.332, 0.594, 0.397, 0.650), 14, 0.87, 0.42),
}

COL_CELLS = [r"\frac{1}{b}", r"\frac{\sqrt{1!}}{b^{2}}", r"\frac{\sqrt{2!}}{b^{3}}",
             r"\frac{\sqrt{3!}}{b^{4}}", r"\frac{\sqrt{4!}}{...}", r"...", r"...\ \infty"]


def fit_col(cells, size, maxw, maxh, min_size=6.0):
    def build(pt):
        parts = [draw(c, "#000000", pt, None, None, DPI)[0] for c in cells]
        w = max(p.shape[1] for p in parts) + 2 * PAD
        h = sum(p.shape[0] for p in parts) + 2 * PAD + 2 * len(parts)
        cv = np.zeros((h, w, 4), dtype=np.uint8)
        y = PAD
        for p in parts:
            cv[y:y + p.shape[0], PAD:PAD + p.shape[1]] = p
            y += p.shape[0] + 2
        return cv
    lo, hi = min_size, size
    for _ in range(12):
        pt = (lo + hi) / 2
        cv = build(pt)
        if cv.shape[1] / DPI <= maxw and cv.shape[0] / DPI <= maxh:
            lo = pt
        else:
            hi = pt
    pt = lo
    cv = build(pt)
    dl = np.asarray(Image.fromarray(draw("[", "#000000", pt * 3, None, None, DPI)[0]).resize(
        (max(6, PAD // 2), cv.shape[0]), Image.BILINEAR))
    dr = np.asarray(Image.fromarray(draw("]", "#000000", pt * 3, None, None, DPI)[0]).resize(
        (max(6, PAD // 2), cv.shape[0]), Image.BILINEAR))
    w = cv.shape[1] + dl.shape[1] + dr.shape[1] + 2 * PAD
    out = np.zeros((cv.shape[0], w, 4), dtype=np.uint8)
    out[:, PAD:PAD + dl.shape[1]] = dl
    out[:, PAD + dl.shape[1]:PAD + dl.shape[1] + cv.shape[1]] = cv
    out[:, w - PAD - dr.shape[1]:w - PAD] = dr
    return out, pt


manifest = {}
for name, (row, (x0n, y0n, x1n, y1n), base_pt, maxw, maxh) in EQS.items():
    rx, ry = x0n * W, y0n * H
    rw, rh = (x1n - x0n) * W, (y1n - y0n) * H
    if row is None:
        canvas, pt = fit_col(COL_CELLS, base_pt, maxw, maxh)
    else:
        canvas, pt = fit_row(row, base_pt, maxw, maxh)
    Image.fromarray(canvas).save(os.path.join(OUT, name + ".png"))
    w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
    manifest[name] = {"file": name + ".png",
                      "x": round(rx + (rw - w_in) / 2, 4), "y": round(ry + (rh - h_in) / 2, 4),
                      "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(pt, 2)}
    print(name, "w_in=%.3f h_in=%.3f pt=%.1f" % (w_in, h_in, pt))

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
print("wrote", OUT)
