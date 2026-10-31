#!/usr/bin/env python3
"""Rebuild-wave-3 assets for slide 038 from qa/reanalysis2/slide_038_analysis.txt.

Renders mathtext rows (render_math.py) into tight transparent 600-dpi PNGs
named eq_038/rb3_*.png and writes eq_038/rb3_manifest.json with exact
w_in/h_in (w_in = px/600) for pptxgenjs addImage placement.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
import render_math as rm

OUT = os.path.join(BUILD, "eq_038")
os.makedirs(OUT, exist_ok=True)
MAN = {}


def emit(name, rows, size, maxw, maxh, left=False, rowgap=8):
    """Render rows at one common font size, stacked into one PNG."""
    segs = [rm.parse_row(r) for r in rows]
    meas = []
    for sg in segs:
        w = sum(rm.measure_segment(lt, c, size)[0] for c, lt in sg)
        h = max(rm.measure_segment(lt, c, size)[1] for c, lt in sg)
        meas.append((w, h))
    n = len(rows)
    scale = min(maxw / max(w for w, _ in meas),
                maxh / (sum(h for _, h in meas) + rowgap * (n - 1) / rm.DPI))
    pt = max(6.0, size * scale * 0.995)
    canvases = [rm.render_row(r, pt) for r in rows]
    w = max(c.shape[1] for c in canvases)
    h = sum(c.shape[0] for c in canvases) + rowgap * (n - 1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = 0
    for c in canvases:
        x = 0 if left else (w - c.shape[1]) // 2
        canvas[y:y + c.shape[0], x:x + c.shape[1]] = c
        y += c.shape[0] + rowgap
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    MAN[name] = {"file": "eq_038/" + name + ".png",
                 "w_in": round(canvas.shape[1] / rm.DPI, 5),
                 "h_in": round(canvas.shape[0] / rm.DPI, 5),
                 "pt": round(pt, 2)}
    print(name, MAN[name]["w_in"], MAN[name]["h_in"], round(pt, 2))


def vec(name, comps):
    a, b, c = comps
    row = ("CC0000:\\left(\\overset{%d}{\\overset{%d}{%d}}\\right)^{T}"
           % (a, b, c))
    emit(name, [row], 18, 1.0, 0.55)


if __name__ == "__main__":
    vec("rb3_vec_x1", (1, 2, 1))
    vec("rb3_vec_x2", (2, 2, 1))
    vec("rb3_vec_x3", (7, 4, 1))
    vec("rb3_vec_x4", (8, 4, 1))
    vec("rb3_vec_T1", (2, 3, 1))
    vec("rb3_vec_T2", (4, 5, 1))
    vec("rb3_vec_T3", (6, 2, 1))
    emit("rb3_eq_dual", [
        "0000CC:\\mathrm{Minimize}\\ \\mathcal{L}_D(\\alpha) = \\frac{1}{2}"
        "\\sum_{i=1}^{N}\\sum_{j=1}^{N}\\alpha_i\\alpha_j y_i y_j "
        "\\left[x_i^{T} x_j + 1\\right]^2 - \\sum_{i=1}^{N}\\alpha_i",
    ], 22, 10.6, 0.55)
    emit("rb3_blockA", [
        "000000:x_1^{T}\\ \\left(1\\ 1\\ 1\\right)",
        "000000:x_2^{T}\\ \\left(1\\ 2\\ 2\\right)",
        "000000:x_3^{T}\\ \\left(1\\ 2\\ 7\\right)",
        "000000:x_4^{T}\\ \\left(1\\ 4\\ 8\\right)",
    ], 16, 2.2, 1.55)
    emit("rb3_blockB", [
        "000000:x_1\\ x_2\\ x_3\\ x_4",
        "000000:\\left(1\\ 2\\ 7\\ 8\\right)",
        "000000:\\left(1\\ 2\\ 4\\ 4\\right)",
        "000000:\\left(1\\ 1\\ 1\\ 1\\right)",
    ], 16, 2.4, 1.55)
    emit("rb3_blockC", [
        "000000:x_1^{T}\\ \\left(2\\ 4\\ 11\\ 12\\right)",
        "000000:x_2^{T}\\ \\left(4\\ 8\\ 22\\ 24\\right)",
        "000000:x_3^{T}\\ \\left(11\\ 22\\ 65\\ 72\\right)",
        "000000:x_4^{T}\\ \\left(12\\ 24\\ 72\\ 80\\right)",
    ], 16, 2.3, 1.55)
    emit("rb3_blockD", [
        "000000:\\left[x_i^{T} x_j + 1\\right]^2",
        "000000:\\left(3^{2}\\ 5^{2}\\ 12^{2}\\ 13^{2}\\right)",
        "000000:\\left(5^{2}\\ 9^{2}\\ 23^{2}\\ 25^{2}\\right)",
        "000000:\\left(12^{2}\\ 23^{2}\\ 66^{2}\\ 73^{2}\\right)",
        "000000:\\left(13^{2}\\ 25^{2}\\ 73^{2}\\ 81^{2}\\right)",
    ], 16, 2.1, 1.6)
    with open(os.path.join(OUT, "rb3_manifest.json"), "w") as fh:
        json.dump(MAN, fh, indent=1)
    print("manifest written")

    emit("rb3_eq_qp", [
        "CC0000:\\mathrm{Minimize:}\\ \\left[+4.5\\alpha_1^{2} + 12.5\\alpha_1\\alpha_2"
        " - 72\\alpha_1\\alpha_3 - 84.5\\alpha_1\\alpha_4 + 12.5\\alpha_2\\alpha_1"
        " + 40.5\\alpha_2^{2} - 264.5\\alpha_2\\alpha_3 - 312.5\\alpha_2\\alpha_4"
        " - 72\\alpha_3\\alpha_1 - 264.5\\alpha_3\\alpha_2 + 2178\\alpha_3^{2}"
        " + 2664.5\\alpha_3\\alpha_4 - 84.5\\alpha_4\\alpha_1 - 312.5\\alpha_4\\alpha_2"
        " + 2664.5\\alpha_4\\alpha_3 + 3280.5\\alpha_4^{2}\\right]",
    ], 20, 10.6, 0.72)
    emit("rb3_eq_topcons", [
        "000000:\\alpha_1 y_1 + \\alpha_2 y_2 + \\alpha_3 y_3 + \\alpha_4 y_4 = 0",
        "000000:0 \\leq \\alpha_1 \\leq C,\\ 0 \\leq \\alpha_2 \\leq C,"
        "\\ 0 \\leq \\alpha_3 \\leq C,\\ 0 \\leq \\alpha_4 \\leq C",
    ], 14, 3.7, 0.95)
    emit("rb3_eq_cons", [
        "000000:-\\left[\\alpha_1 + \\alpha_2 + \\alpha_3 + \\alpha_4\\right]",
        "000000:\\sum\\alpha_i y_i = 0",
        "000000:\\alpha_1 + \\alpha_2 - \\alpha_3 - \\alpha_4 = 0",
        "000000:\\alpha_i \\leq C",
        "000000:\\alpha_1 \\leq 1,\\ \\alpha_2 \\leq 1,\\ \\alpha_3 \\leq 1,"
        "\\ \\alpha_4 \\leq 1",
        "000000:\\alpha_i \\geq 0",
        "000000:\\alpha_1 \\geq 0,\\ \\alpha_2 \\geq 0,\\ \\alpha_3 \\geq 0,"
        "\\ \\alpha_4 \\geq 0",
    ], 12, 4.6, 0.78, left=True, rowgap=4)
