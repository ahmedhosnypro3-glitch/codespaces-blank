#!/usr/bin/env python3
"""Render a multi-color LaTeX (mathtext) equation to one tight transparent PNG.

Usage:
  python3 render_eq_multi.py out.png <fontsize_pt> '<seg1>|<seg2>|...' [--gap N]

Each segment is '<color>:<latex>'; segments are rendered separately at the same
font size, aligned on a shared baseline, and concatenated horizontally.
Prints JSON metadata for pptxgenjs placement (w_in = w_px/600).
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
PAD_PX = 8
FIG_W, FIG_H = 12, 4


def render_segment(latex, color, fontsize):
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="center", va="baseline")
    probe = fig.text(0.15, 0.5, "x", fontsize=fontsize, color=color,
                     ha="center", va="baseline")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pb = probe.get_window_extent(renderer=renderer)
    buf = np.asarray(fig.canvas.buffer_rgba())
    px0, px1 = max(int(pb.x0) - 2, 0), int(pb.x1) + 2
    baseline_row = int(np.where(buf[:, :, 3][:, px0:px1].any(axis=1))[0][-1])
    ink = buf[:, :, 3] > 8
    ink[:, :px1 + 20] = False
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    plt.close(fig)
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    return buf[y0:y1, x0:x1], baseline_row - y0


def main():
    out = sys.argv[1]
    fontsize = float(sys.argv[2])
    spec = sys.argv[3]
    gap = 0
    if "--gap" in sys.argv:
        gap = int(sys.argv[sys.argv.index("--gap") + 1])

    segments = []
    for part in spec.split("@@"):
        color, latex = part.split(":", 1)
        segments.append((color, latex))

    rendered = [render_segment(latex, color, fontsize) for color, latex in segments]

    # common baseline: use the largest baseline offset as reference
    max_baseline = max(b for _, b in rendered)
    heights = [arr.shape[0] for arr, _ in rendered]
    total_h = max_baseline + max(h - b for (_, b), h in zip(rendered, heights)) + PAD_PX
    total_w = sum(arr.shape[1] for arr, _ in rendered) + gap * (len(rendered) - 1) + 2 * PAD_PX

    canvas = np.zeros((total_h, total_w, 4), dtype=np.uint8)
    x = PAD_PX
    for (arr, b), (color, latex) in zip(rendered, segments):
        y = max_baseline - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1] + gap

    Image.fromarray(canvas).save(out)
    info = {
        "path": out,
        "w_px": int(total_w), "h_px": int(total_h),
        "w_in": round(total_w / DPI, 5), "h_in": round(total_h / DPI, 5),
        "baseline_px": int(max_baseline), "baseline_frac": round(max_baseline / total_h, 5),
        "dpi": DPI, "fontsize_pt": fontsize,
        "segments": [{"color": c, "latex": l} for c, l in segments],
    }
    print(json.dumps(info))


if __name__ == "__main__":
    main()
