#!/usr/bin/env python3
"""Round-5 assets for slide 006: dejavusans mathtext, judge-noted ink colors
(x red, y green, z blue, arrows green, convert text red, -1 diagonals red).
rb5_ prefix; all prior asset sets untouched."""
import json
import os
import subprocess
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "dejavusans"
matplotlib.rcParams["mathtext.default"] = "it"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_006")
DPI = 600
BLACK, BLUE, GREEN, RED = "#000000", "#0000FF", "#008000", "#FF0000"
GRAY = "#404040"


def render_math(name, rows, size, maxw, maxh):
    out = os.path.join(OUT, f"rb5_{name}.png")
    jout = os.path.join(OUT, f"rb5_{name}.json")
    cmd = [sys.executable, os.path.join(HERE, "render_math.py"),
           "--out", out, "--size", str(size), "--maxw", str(maxw),
           "--maxh", str(maxh), "--out-json", jout]
    for r in rows:
        cmd += ["--row", r]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    info = json.load(open(jout))
    print(name, info["w_in"], "x", info["h_in"], "in")


def render_grid(name, rows, color_fn, fs=9, col_w=0.40, row_h=0.14):
    nr, nc = len(rows), len(rows[0])
    fw, fh = col_w * nc + 0.55, row_h * nr + 0.30
    fig = plt.figure(figsize=(fw, fh), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, fw)
    ax.set_ylim(0, fh)
    ax.axis("off")
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            ax.text(0.22 + c * col_w + col_w / 2, (nr - 1 - r) * row_h + row_h / 2,
                    f"${val}$", fontsize=fs, color=color_fn(r, c, val),
                    ha="center", va="center")
    x_l, x_r = 0.10, 0.22 + (nc - 1) * col_w + col_w + 0.03
    y_b, y_t = 0.05, row_h * nr + 0.03
    tick = 0.12
    for x, sgn in ((x_l, 1), (x_r, -1)):
        ax.plot([x, x], [y_b, y_t], color=BLACK, linewidth=1.6)
        ax.plot([x, x + sgn * tick], [y_b, y_b], color=BLACK, linewidth=1.6)
        ax.plot([x, x + sgn * tick], [y_t, y_t], color=BLACK, linewidth=1.6)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rr = np.where(ink.any(axis=1))[0]
    cc = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rr[0] - 6, 0), min(rr[-1] + 7, buf.shape[0])
    x0, x1 = max(cc[0] - 6, 0), min(cc[-1] + 7, buf.shape[1])
    out = os.path.join(OUT, f"rb5_{name}.png")
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    info = {"path": out, "w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "w_in": round((x1 - x0) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5)}
    with open(os.path.join(OUT, f"rb5_{name}.json"), "w") as fh:
        json.dump(info, fh, indent=2)
    plt.close(fig)
    print(name, info["w_in"], "x", info["h_in"], "in")


def main():
    os.makedirs(OUT, exist_ok=True)
    def ineq(a_col, op, b_col):
        segs = []
        for i in (1, 2, 3):
            if i > 1:
                segs += [f"{BLACK[1:]}: , "]
            segs += [f"{a_col}:x_{{{i}}}", f"{BLACK[1:]}:\\{op}", f"{b_col}:z_{{{i}}}"]
        return "||".join(segs)
    le = ineq("FF0000", "leq", "0000FF")
    ge = ineq("FF0000", "geq", "0000FF")
    chain = "||".join([
        f"{GREEN[1:]}:y_{{1}}", f"{BLACK[1:]}:\\leq", f"{RED[1:]}:x_{{1}}", f"{BLACK[1:]}:\\leq", f"{BLUE[1:]}:z_{{1}}", f"{BLACK[1:]}: ,  ",
        f"{GREEN[1:]}:y_{{2}}", f"{BLACK[1:]}:\\leq", f"{RED[1:]}:x_{{2}}", f"{BLACK[1:]}:\\leq", f"{BLUE[1:]}:z_{{2}}", f"{BLACK[1:]}: ,  ",
        f"{GREEN[1:]}:y_{{3}}", f"{BLACK[1:]}:\\leq", f"{RED[1:]}:x_{{3}}", f"{BLACK[1:]}:\\leq", f"{BLUE[1:]}:z_{{3}}", f"{BLACK[1:]}: ,"])
    def convrow(op, neg):
        segs = []
        for i in (1, 2, 3):
            if i > 1:
                segs.append(f"{RED[1:]}: , ")
            segs += [f"{RED[1:]}:{neg}x_{{{i}}}", f"{RED[1:]}:\\{op}", f"{RED[1:]}:{neg}z_{{{i}}}"]
        return "||".join(segs)
    render_math("le_str", [le], 16, 3.6, 0.30)
    render_math("ge_str", [ge], 16, 3.6, 0.30)
    render_math("chain_str", [chain], 16, 3.6, 0.30)
    render_math("conv1", [convrow("geq", "")], 14, 2.5, 0.24)
    render_math("conv2", [convrow("leq", "-")], 14, 2.5, 0.24)
    render_math("gxleh", [f"{RED[1:]}:G\\,x \\leq h"], 16, 1.45, 0.24)
    render_math("arrow", [f"{GREEN[1:]}:\\Rightarrow"], 18, 0.35, 0.30)
    render_math("leq", [f"{BLACK[1:]}:\\leq"], 16, 0.22, 0.22)
    render_grid("m3id", [["1", "0", "0"], ["0", "1", "0"], ["0", "0", "1"]],
                lambda r, c, v: BLACK)
    render_grid("m3neg", [["-1", "0", "0"], ["0", "-1", "0"], ["0", "0", "-1"]],
                lambda r, c, v: RED if v == "-1" else BLACK)
    render_grid("m6", [["-1", "0", "0"], ["0", "-1", "0"], ["0", "0", "-1"],
                       ["0", "0", "1"], ["0", "1", "0"], ["1", "0", "0"]],
                lambda r, c, v: (RED if v == "-1" else GREEN if v == "1" else GRAY),
                row_h=0.15)
    render_grid("vx3", [["x_{1}"], ["x_{2}"], ["x_{3}"]], lambda r, c, v: RED, col_w=0.5)
    render_grid("vz3", [["z_{1}"], ["z_{2}"], ["z_{3}"]], lambda r, c, v: BLUE, col_w=0.5)
    render_grid("vnegz3", [["-z_{1}"], ["-z_{2}"], ["-z_{3}"]], lambda r, c, v: BLUE, col_w=0.58)
    render_grid("vyz6", [["-y_{1}"], ["-y_{2}"], ["-y_{3}"],
                         ["z_{1}"], ["z_{2}"], ["z_{3}"]],
                lambda r, c, v: GREEN if v.startswith("-y") else BLUE, col_w=0.58, row_h=0.15)


if __name__ == "__main__":
    main()
