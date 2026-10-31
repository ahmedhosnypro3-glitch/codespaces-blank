#!/usr/bin/env python3
"""Fix-cycle-2 assets for slide 038 (fresh judge MAJORs from slide_038_judge_a1_1.txt):
bigger stacked vectors + y-labels, legible top-right constraints, larger QP
expansion and constraints block. New rb3f2_* PNGs; manifest keys only added.
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
MAN_PATH = os.path.join(OUT, "rb3_manifest.json")
with open(MAN_PATH) as fh:
    MAN = json.load(fh)


def emit(name, rows, size, maxw, maxh, left=False, rowgap=8):
    segs = [rm.parse_row(r) for r in rows]
    meas = []
    for sg in segs:
        w = sum(rm.measure_segment(lt, c, size)[0] for c, lt in sg)
        h = max(rm.measure_segment(lt, c, size)[1] for c, lt in sg)
        meas.append((w, h))
    n = len(rows)
    scale = min(maxw / max(w for w, _ in meas),
                maxh / (sum(h for _, h in meas) + rowgap * (n - 1) / rm.DPI))
    pt = max(7.0, size * scale * 0.995)
    canvases = [rm.render_row(r, pt) for r in rows]
    w = max(c.shape[1] for c in canvases)
    h = sum(c.shape[0] for c in canvases) + rowgap * (n - 1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = 0
    for c in canvases:
        x = 0 if left else (w - c.shape[1]) // 2
        canvas[y:y + c.shape[0], x:x + c.shape[1]] = c
        y += c.shape[0] + rowgap
    Image.fromarray(canvas).save(os.path.join(OUT, name + ".png"))
    MAN[name] = {"file": "eq_038/" + name + ".png",
                 "w_in": round(canvas.shape[1] / rm.DPI, 5),
                 "h_in": round(canvas.shape[0] / rm.DPI, 5),
                 "pt": round(pt, 2)}
    print(name, MAN[name]["w_in"], MAN[name]["h_in"], round(pt, 2))


def vec(name, comps):
    a, b, c = comps
    emit(name, ["CC0000:\\left(\\overset{%d}{\\overset{%d}{%d}}\\right)^{T}"
                % (a, b, c)], 24, 0.95, 0.78)


def ylab(name, i, v):
    emit(name, ["000000:y_{%d} = %d" % (i, v)], 18, 0.9, 0.34)


if __name__ == "__main__":
    vec("rb3f2_vec_x1", (1, 2, 1))
    vec("rb3f2_vec_x2", (2, 2, 1))
    vec("rb3f2_vec_x3", (7, 4, 1))
    vec("rb3f2_vec_x4", (8, 4, 1))
    vec("rb3f2_vec_T1", (2, 3, 1))
    vec("rb3f2_vec_T2", (4, 5, 1))
    vec("rb3f2_vec_T3", (6, 2, 1))
    ylab("rb3f2_y1", 1, 1)
    ylab("rb3f2_y2", 2, 1)
    ylab("rb3f2_y3", 3, -1)
    ylab("rb3f2_y4", 4, -1)
    emit("rb3f2_topcons", [
        "000000:\\alpha_1 y_1 + \\alpha_2 y_2 + \\alpha_3 y_3 + \\alpha_4 y_4 = 0",
        "000000:0 \\leq \\alpha_1 \\leq C,\\ 0 \\leq \\alpha_2 \\leq C,"
        "\\ 0 \\leq \\alpha_3 \\leq C,\\ 0 \\leq \\alpha_4 \\leq C",
    ], 16, 3.8, 1.55, rowgap=6)
    emit("rb3f2_qp", [
        "CC0000:\\mathrm{Minimize:}\\ \\left[+4.5\\alpha_1^{2} + 12.5\\alpha_1\\alpha_2"
        " - 72\\alpha_1\\alpha_3 - 84.5\\alpha_1\\alpha_4 + 12.5\\alpha_2\\alpha_1"
        " + 40.5\\alpha_2^{2} - 264.5\\alpha_2\\alpha_3 - 312.5\\alpha_2\\alpha_4"
        " - 72\\alpha_3\\alpha_1 - 264.5\\alpha_3\\alpha_2 + 2178\\alpha_3^{2}"
        " + 2664.5\\alpha_3\\alpha_4 - 84.5\\alpha_4\\alpha_1 - 312.5\\alpha_4\\alpha_2"
        " + 2664.5\\alpha_4\\alpha_3 + 3280.5\\alpha_4^{2}\\right]",
    ], 20, 10.4, 0.72)
    emit("rb3f2_cons_l", [
        "000000:-\\left[\\alpha_1 + \\alpha_2 + \\alpha_3 + \\alpha_4\\right]",
        "000000:\\sum\\alpha_i y_i = 0",
        "000000:\\alpha_1 + \\alpha_2 - \\alpha_3 - \\alpha_4 = 0",
        "000000:\\alpha_i \\leq C",
    ], 15, 3.4, 0.62, left=True, rowgap=3)
    emit("rb3f2_cons_r", [
        "000000:\\alpha_1 \\leq 1,\\ \\alpha_2 \\leq 1,\\ \\alpha_3 \\leq 1,"
        "\\ \\alpha_4 \\leq 1",
        "000000:\\alpha_i \\geq 0",
        "000000:\\alpha_1 \\geq 0,\\ \\alpha_2 \\geq 0,\\ \\alpha_3 \\geq 0,"
        "\\ \\alpha_4 \\geq 0",
    ], 15, 3.4, 0.62, left=True, rowgap=3)
    with open(MAN_PATH, "w") as fh:
        json.dump(MAN, fh, indent=1)
    print("manifest updated")
