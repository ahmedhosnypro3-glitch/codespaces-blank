#!/usr/bin/env python3
"""Round-4 assets for slide 038: fix judge BLOCKERs/MAJORs from the fresh
transcript (slide_038_judge_a1_1.txt).

- Column vectors rendered by hand (bracket lines + one mathtext row per
  component + ^T), because nested \\overset stacks render only the top glyph.
- Vectors are 2-D per the original frame: x1=(1,1), x2=(2,2), x3=(7,4),
  x4=(8,4); T1=(2,3), T2=(4,5), T3=(6,2).
- Bigger top-right constraints, two-row Minimize expansion, bigger Subject-to
  columns, bigger matrix blocks. Manifest keys are overwritten in place,
  never removed. Run from anywhere; paths absolute inside the namespace.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
import render_math as rm

OUT = os.path.join(BUILD, "eq_038")
MAN_PATH = os.path.join(OUT, "rb3_manifest.json")
with open(MAN_PATH) as fh:
    MAN = json.load(fh)

DPI = 600
matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"


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
    Image.fromarray(canvas).save(os.path.join(OUT, name + ".png"))
    MAN[name] = {"file": "eq_038/" + name + ".png",
                 "w_in": round(canvas.shape[1] / DPI, 5),
                 "h_in": round(canvas.shape[0] / DPI, 5),
                 "pt": round(pt, 2)}
    print(name, MAN[name]["w_in"], MAN[name]["h_in"], round(pt, 2))


def colvec(name, comps, color, fs, sup="T", w_in=0.36, row_h=0.24, pad=0.06):
    """Hand-drawn column vector: bracket lines + one mathtext row per component."""
    n = len(comps)
    h_in = n * row_h + 2 * pad
    fig = plt.figure(figsize=(w_in, h_in), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w_in)
    ax.set_ylim(0, h_in)
    ax.axis("off")
    col = "#" + color
    for i, c in enumerate(comps):
        ax.text(w_in / 2 + 0.05, h_in - pad - (i + 0.5) * row_h, f"${c}$",
                fontsize=fs, color=col, ha="center", va="center")
    x_l, x_r = 0.07, w_in - 0.11
    y_b, y_t, tick = 0.03, h_in - 0.03, 0.07
    for x, sgn in ((x_l, 1), (x_r, -1)):
        ax.plot([x, x], [y_b, y_t], color=col, linewidth=2.2)
        ax.plot([x, x + sgn * tick], [y_b, y_b], color=col, linewidth=2.2)
        ax.plot([x, x + sgn * tick], [y_t, y_t], color=col, linewidth=2.2)
    if sup:
        ax.text(w_in - 0.01, h_in - pad - 0.01, f"${{}}^{{{sup}}}$",
                fontsize=fs * 0.75, color=col, ha="right", va="top")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rr = np.where(ink.any(axis=1))[0]
    cc = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rr[0] - 8, 0), min(rr[-1] + 8, buf.shape[0])
    x0, x1 = max(cc[0] - 8, 0), min(cc[-1] + 8, buf.shape[1])
    plt.close(fig)
    Image.fromarray(buf[y0:y1, x0:x1]).save(os.path.join(OUT, name + ".png"))
    MAN[name] = {"file": "eq_038/" + name + ".png",
                 "w_in": round((x1 - x0) / DPI, 5),
                 "h_in": round((y1 - y0) / DPI, 5),
                 "pt": round(fs, 2)}
    print(name, MAN[name]["w_in"], MAN[name]["h_in"], fs)


if __name__ == "__main__":
    colvec("rb4_vec_x1", ["1", "1"], "C00000", 15)
    colvec("rb4_vec_x2", ["2", "2"], "C00000", 15)
    colvec("rb4_vec_x3", ["7", "4"], "C00000", 15)
    colvec("rb4_vec_x4", ["8", "4"], "C00000", 15)
    colvec("rb4_vec_T1", ["2", "3"], "C00000", 15)
    colvec("rb4_vec_T2", ["4", "5"], "C00000", 15)
    colvec("rb4_vec_T3", ["6", "2"], "C00000", 15)
    colvec("rb4_alpha_colT",
           ["\\alpha_1", "\\alpha_2", "\\alpha_3", "\\alpha_4"],
           "CC0000", 11, w_in=0.42, row_h=0.15, pad=0.06)
    for i, v in enumerate(["1", "1", "-1", "-1"], 1):
        emit(f"rb4_ylab_{i}", [f"000000:y_{i} = {v}"], 18, 1.0, 0.32)
    emit("rb4_eq_topcons", [
        "000000:\\alpha_1 y_1 + \\alpha_2 y_2 + \\alpha_3 y_3 + \\alpha_4 y_4 = 0",
        "000000:0 \\leq \\alpha_1 \\leq C,\\ 0 \\leq \\alpha_2 \\leq C,"
        "\\ 0 \\leq \\alpha_3 \\leq C,\\ 0 \\leq \\alpha_4 \\leq C",
    ], 22, 3.86, 1.0)
    emit("rb4f_eq_dual", [
        "0000CC:\\mathrm{Minimize}\\ \\mathcal{L}_D(\\alpha) = \\frac{1}{2}"
        "\\overset{N}{\\underset{i=1}{\\sum}}\\overset{N}{\\underset{j=1}{\\sum}}"
        "\\alpha_i\\alpha_j y_i y_j \\left[x_i^{T} x_j + 1\\right]^2"
        " - \\overset{N}{\\underset{i=1}{\\sum}}\\alpha_i",
    ], 24, 10.6, 0.58)
    emit("rb4_blockA", [
        "000000:x_1^{T}\\ \\left(1\\ 1\\ 1\\right)",
        "000000:x_2^{T}\\ \\left(1\\ 2\\ 2\\right)",
        "000000:x_3^{T}\\ \\left(1\\ 2\\ 7\\right)",
        "000000:x_4^{T}\\ \\left(1\\ 4\\ 8\\right)",
    ], 20, 2.2, 1.62)
    emit("rb4_blockB", [
        "000000:x_1\\ x_2\\ x_3\\ x_4",
        "000000:\\left(1\\ 2\\ 7\\ 8\\right)",
        "000000:\\left(1\\ 2\\ 4\\ 4\\right)",
        "000000:\\left(1\\ 1\\ 1\\ 1\\right)",
    ], 20, 2.4, 1.62)
    emit("rb4_blockC", [
        "000000:x_1^{T}\\ \\left(2\\ 4\\ 11\\ 12\\right)",
        "000000:x_2^{T}\\ \\left(4\\ 8\\ 22\\ 24\\right)",
        "000000:x_3^{T}\\ \\left(11\\ 22\\ 65\\ 72\\right)",
        "000000:x_4^{T}\\ \\left(12\\ 24\\ 72\\ 80\\right)",
    ], 20, 2.3, 1.62)
    emit("rb4_blockD", [
        "000000:\\left[x_i^{T} x_j + 1\\right]^2",
        "000000:\\left(3^{2}\\ 5^{2}\\ 12^{2}\\ 13^{2}\\right)",
        "000000:\\left(5^{2}\\ 9^{2}\\ 23^{2}\\ 25^{2}\\right)",
        "000000:\\left(12^{2}\\ 23^{2}\\ 66^{2}\\ 73^{2}\\right)",
        "000000:\\left(13^{2}\\ 25^{2}\\ 73^{2}\\ 81^{2}\\right)",
    ], 20, 2.15, 1.68)
    emit("rb4_eq_qp", [
        "CC0000:\\mathrm{Minimize:}\\ \\left[+4.5\\alpha_1^{2} + 12.5\\alpha_1\\alpha_2"
        " - 72\\alpha_1\\alpha_3 - 84.5\\alpha_1\\alpha_4 + 12.5\\alpha_2\\alpha_1"
        " + 40.5\\alpha_2^{2} - 264.5\\alpha_2\\alpha_3 - 312.5\\alpha_2\\alpha_4\\right.",
        "CC0000:\\left.- 72\\alpha_3\\alpha_1 - 264.5\\alpha_3\\alpha_2"
        " + 2178\\alpha_3^{2} + 2664.5\\alpha_3\\alpha_4 - 84.5\\alpha_4\\alpha_1"
        " - 312.5\\alpha_4\\alpha_2 + 2664.5\\alpha_4\\alpha_3 + 3280.5\\alpha_4^{2}\\right]",
    ], 20, 10.6, 0.9)
    emit("rb4_cons_l", [
        "000000:-\\left[\\alpha_1 + \\alpha_2 + \\alpha_3 + \\alpha_4\\right]",
        "000000:\\sum\\alpha_i y_i = 0",
        "000000:\\alpha_1 + \\alpha_2 - \\alpha_3 - \\alpha_4 = 0",
    ], 16, 1.9, 0.66, left=True, rowgap=5)
    emit("rb4_cons_r", [
        "000000:\\alpha_i \\leq C",
        "000000:\\alpha_1 \\leq 1,\\ \\alpha_2 \\leq 1,\\ \\alpha_3 \\leq 1,"
        "\\ \\alpha_4 \\leq 1",
        "000000:\\alpha_i \\geq 0",
        "000000:\\alpha_1 \\geq 0,\\ \\alpha_2 \\geq 0,\\ \\alpha_3 \\geq 0,"
        "\\ \\alpha_4 \\geq 0",
    ], 16, 2.6, 0.66, left=True, rowgap=5)
    with open(MAN_PATH, "w") as fh:
        json.dump(MAN, fh, indent=1)
    print("manifest updated")
