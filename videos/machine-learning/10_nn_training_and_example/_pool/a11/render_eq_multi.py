#!/usr/bin/env python3
"""render_eq_multi.py — 600dpi mathtext PNG from colored segments (a11).

matplotlib mathtext has no \\color, so a colored equation is rendered as
several single-color segments, each cropped to its ink box, then pasted onto
one transparent canvas with a COMMON baseline. All segments share figsize
(20x6in) and va='baseline' at figure y=0.5, so the baseline canvas row is a
constant (BASELINE). Output sidecar carries exact px size + baseline_frac for
the alignment law.

Usage:
  python3 render_eq_multi.py <segments.json> <out.png> <fontsize_pt>
segments.json: [{"mathtext": "...", "color": "RRGGBB", "gap_px": 0}, ...]
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 6
BASELINE = 1800  # 0.5 * 6in * 600dpi in a (20, 6) figure


def seg_box(latex, fontsize, color):
    fig = plt.figure(figsize=(20, 6), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color="#" + color,
             ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        plt.close(fig)
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    img = Image.fromarray(buf[y0:y1, x0:x1])
    plt.close(fig)
    return img, int(y0)


def main():
    segs = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    fontsize = float(sys.argv[3])

    rendered = []
    width = 0
    for i, s in enumerate(segs):
        img, y0 = seg_box(s["mathtext"], fontsize, s.get("color", "000000"))
        rendered.append((img, y0))
        width += img.width + int(s.get("gap_px", 0) or 0)
    if not rendered:
        raise SystemExit("no segments")

    loff = [BASELINE - y0 for _, y0 in rendered]     # baseline -> bottom of img
    above = max(loff)
    below = max(img.height - off for (img, _), off in zip(rendered, loff))
    height = above + max(0, below)

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = 0
    for (img, y0), seg in zip(rendered, segs):
        canvas.paste(img, (x, above - (BASELINE - y0)), img)
        x += img.width + int(seg.get("gap_px", 0) or 0)
    canvas.save(out)
    h = canvas.height
    print(json.dumps({"path": out, "w_px": int(width), "h_px": int(h),
                      "w_in": round(width / DPI, 5), "h_in": round(h / DPI, 5),
                      "baseline_px": int(above), "baseline_frac": round(above / h, 5),
                      "dpi": DPI, "fontsize_pt": fontsize}))


if __name__ == "__main__":
    main()
