#!/usr/bin/env python3
"""Fix-wave assets for slide 038 (judge MAJORs): 2D displaystyle sums in the
dual equation, and an explicit [alpha_1..alpha_4] row vector multiplying the
4x4 Q matrix in the Minimize line. New rb3f_* PNGs; manifest keys are added,
never removed. Run from anywhere; paths are absolute inside the namespace.
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
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    MAN[name] = {"file": "eq_038/" + name + ".png",
                 "w_in": round(canvas.shape[1] / rm.DPI, 5),
                 "h_in": round(canvas.shape[0] / rm.DPI, 5),
                 "pt": round(pt, 2)}
    print(name, MAN[name]["w_in"], MAN[name]["h_in"], round(pt, 2))


def emit_qmat(name, color, fs=10, col_w=0.62, row_h=0.15):
    rows = [["4.5", "12.5", "-72", "-84.5"],
            ["12.5", "40.5", "-264.5", "-312.5"],
            ["-72", "-264.5", "2178", "2664.5"],
            ["-84.5", "-312.5", "2664.5", "3280.5"]]
    fig = plt.figure(figsize=(col_w * 4 + 0.5, row_h * 4 + 0.2), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, col_w * 4 + 1.2)
    ax.set_ylim(0, row_h * 4 + 0.5)
    ax.axis("off")
    ax.set_xlim(0, col_w * 4 + 0.5)
    ax.set_ylim(0, row_h * 4 + 0.2)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            ax.text(0.25 + c * col_w + col_w / 2,
                    (3 - r) * row_h + row_h / 2, f"${val}$",
                    fontsize=fs, color=color, ha="center", va="center")
    x_l, x_r = 0.08, 0.25 + 3 * col_w + col_w - 0.12
    y_b, y_t, tick = 0.04, row_h * 4 + 0.06, 0.12
    for x, sgn in ((x_l, 1), (x_r, -1)):
        ax.plot([x, x], [y_b, y_t], color=color, linewidth=1.6)
        ax.plot([x, x + sgn * tick], [y_b, y_b], color=color, linewidth=1.6)
        ax.plot([x, x + sgn * tick], [y_t, y_t], color=color, linewidth=1.6)
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
                 "pt": fs}
    print(name, MAN[name]["w_in"], MAN[name]["h_in"])


if __name__ == "__main__":
    # MAJOR 9: 2D professional dual formulation (displaystyle sums -> limits
    # stacked above/below the sigma; stacked 1/2 fraction)
    emit("rb3f_eq_dual", [
        "0000CC:\\mathrm{Minimize}\\ \\mathcal{L}_D(\\alpha) = \\frac{1}{2}"
        "\\overset{N}{\\underset{i=1}{\\sum}}\\overset{N}{\\underset{j=1}{\\sum}}"
        "\\alpha_i\\alpha_j y_i y_j \\left[x_i^{T} x_j + 1\\right]^2"
        " - \\overset{N}{\\underset{i=1}{\\sum}}\\alpha_i",
    ], 22, 10.6, 0.62)
    # MAJOR 10: explicit alpha row vector, Q matrix, alpha column vector
    emit("rb3f_alpha_row", [
        "CC0000:\\left[\\alpha_1\\ \\alpha_2\\ \\alpha_3\\ \\alpha_4\\right]",
    ], 16, 1.9, 0.34)
    emit("rb3f_alpha_colT", [
        "CC0000:\\left(\\overset{\\alpha_1}{\\overset{\\alpha_2}"
        "{\\overset{\\alpha_3}{\\alpha_4}}}\\right)^{T}",
    ], 14, 0.55, 0.78)
    emit_qmat("rb3f_qmat", "#CC0000")
    with open(MAN_PATH, "w") as fh:
        json.dump(MAN, fh, indent=1)
    print("manifest updated")
