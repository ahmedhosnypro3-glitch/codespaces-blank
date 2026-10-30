#!/usr/bin/env python3
"""Render math (matplotlib mathtext) to tight transparent PNGs at 600 dpi.

An "equation" is one or more horizontal segments, each "color:latex"
(colon separator; color may be omitted). A segment may hold nested
\\overset stacks, so 2-D/3-D column vectors render as true 2-D math.

Usage:
  python3 render_math.py --out eq/x.png --size 22 --maxw 4.0 --maxh 1.0 \
      --row "#1A1A2E:Z = \\left(\\overset{x}{y}\\right)"
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
PAD_PX = 6


def _draw(latex, color, fontsize, fig_w, fig_h, dpi, x0):
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
    fig.patch.set_alpha(0.0)
    fig.patch.set_facecolor("none")
    txt = fig.text(x0, 0.5, f"${latex}$", fontsize=fontsize, color=color,
                   ha="left", va="baseline")
    probe = fig.text(x0, 0.95, "x", fontsize=fontsize, color=color,
                     ha="left", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    be = probe.get_window_extent(renderer=fig.canvas.get_renderer())
    bt = txt.get_window_extent(renderer=fig.canvas.get_renderer())
    plt.close(fig)
    if bt.width <= 0 or bt.height <= 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(int(bt.y0) - PAD_PX, 0), min(int(bt.y1) + PAD_PX + 1, buf.shape[0])
    x0c, x1c = max(int(bt.x0) - PAD_PX, 0), min(int(bt.x1) + PAD_PX + 1, buf.shape[1])
    if x1c <= x0c or y1 <= y0:
        raise SystemExit(f"degenerate ink for {latex!r}")
    return buf[y0:y1, x0c:x1c], int(be.y0) - y0, be, bt


def render_segment(latex, color, fontsize, need_w=None, need_h=None):
    fig_w = max(3.0, (need_w or 4.0) * 1.25 + 1.0)
    fig_h = max(fig_w / 2.0, (need_h or 1.0) * 2.6, 2.0)
    cropped, base, _, _ = _draw(latex, color, fontsize, fig_w, fig_h, DPI, x0=0.02)
    return cropped, base


def measure_segment(latex, color, fontsize):
    _, _, be, bt = _draw(latex, color, fontsize, 30.0, 8.0, 72, x0=0.05)
    return (bt.width / 72, bt.height / 72)


def parse_row(row):
    segs = []
    for part in row.split("||"):
        head = part.split("\\", 1)[0]
        if ":" in head:
            color, latex = part.split(":", 1)
        else:
            color, latex = "333333", part
        segs.append((color if color.startswith("#") else "#" + color, latex))
    return segs


def render_row(row, fontsize, sizes=None):
    segs = parse_row(row)
    parts = []
    for i, (color, latex) in enumerate(segs):
        sw, sh = (sizes[i] if sizes else (None, None))
        parts.append(render_segment(latex, color, fontsize, sw, sh))
    base = max(b for _, b in parts)
    h = max(base + (a.shape[0] - b) for (a, b) in parts) + PAD_PX
    w = sum(a.shape[1] for a, _ in parts) + 2 * PAD_PX
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    x = PAD_PX
    for (arr, b), _ in zip(parts, segs):
        y = base - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1]
    return canvas


def fit_row(row, size, max_w_in, max_h_in, min_size=6.0):
    """One probe render at 72 dpi, then exact-size render at 600 dpi."""
    segs = parse_row(row)
    measured = [measure_segment(latex, color, size) for color, latex in segs]
    total_w = sum(w for w, _ in measured)
    total_h = max(h for _, h in measured)
    if total_w <= 0 or total_h <= 0:
        raise SystemExit("measurement failed")
    scale = min(max_w_in / total_w, max_h_in / total_h)
    pt = max(min_size, size * scale * 0.995)
    need = [(w * scale, h * scale) for w, h in measured]
    for _ in range(3):
        canvas = render_row(row, pt, need)
        w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
        if w_in <= max_w_in and h_in <= max_h_in:
            break
        pt *= 0.94
        need = [(w * 0.94, h * 0.94) for w, h in need]
    else:
        canvas = render_row(row, min_size, [(w * 0.2, h * 0.2) for w, h in measured])
    return canvas, pt


def main():
    args = sys.argv[1:]
    out = args[args.index("--out") + 1]
    size = float(args[args.index("--size") + 1])
    rows = [args[i + 1] for i, a in enumerate(args) if a == "--row"]
    max_w = float(args[args.index("--maxw") + 1]) if "--maxw" in args else 40.0
    max_h = float(args[args.index("--maxh") + 1]) if "--maxh" in args else 20.0
    rowgap = int(args[args.index("--rowgap") + 1]) if "--rowgap" in args else 10
    canvases, sizes = [], []
    for r in rows:
        c, pt = fit_row(r, size, max_w, max_h)
        canvases.append(c)
        sizes.append(pt)
    w = max(c.shape[1] for c in canvases)
    h = sum(c.shape[0] for c in canvases) + rowgap * (len(canvases) - 1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = 0
    for c in canvases:
        x = (w - c.shape[1]) // 2
        canvas[y:y + c.shape[0], x:x + c.shape[1]] = c
        y += c.shape[0] + rowgap
    Image.fromarray(canvas).save(out)
    info = {"path": out, "w_px": int(w), "h_px": int(h),
            "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5),
            "dpi": DPI, "fontsize_pt": sizes, "rows": rows}
    if "--out-json" in args:
        with open(args[args.index("--out-json") + 1], "w") as fh:
            json.dump(info, fh, indent=2)
    print(json.dumps(info))


if __name__ == "__main__":
    main()
