"""Generate color-sharded 2D equation PNGs for slide 022 (mathtext -> 600dpi RGBA).

Shards are rendered one color at a time via scripts/render_eq.py, then composited on a
canvas using baseline metadata so stacked case rows stay baseline-aligned with a single
stretched red brace.
Usage: python3 gen_eq_022.py    (writes PNGs into equations_slide022/col_ and prints sizes)
"""
import json
import os
import subprocess

from PIL import Image, ImageDraw
import numpy as np

RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "equations_slide022")
DPI = 600
FONT = 13.0
RED = "C00000"
BLUE = "2B3FC4"
GREEN = "1E8B1E"
BLACK = "000000"
PAD = 8
CANVAS_W, CANVAS_H = 5000, 1400


class Shard:
    def __init__(self, name, latex, color):
        path = os.path.join(OUT, "col_%s.png" % name)
        info = json.loads(subprocess.run(
            ["python3", RENDER, latex, path, str(FONT), color],
            check=True, capture_output=True, text=True).stdout)
        self.path = path
        self.w = int(info["w_px"])
        self.h = int(info["h_px"])
        self.base = int(info["baseline_px"])

    def paste(self, canvas, x, base_y):
        im = Image.open(self.path).convert("RGBA")
        canvas.paste(im, (int(x), int(base_y - self.base)), im)
        return x + self.w

    def vcenter(self, top, bottom):
        im = Image.open(self.path).convert("RGBA")
        mid = (top + bottom) // 2
        canvas = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        return canvas


def brace():
    """Return (Shard for the cropped brace, pitch px between its two stacked rows)."""
    sh = Shard("brace", r"\left\{ \substack{0 \\ y} \right.", RED)
    im = Image.open(sh.path).convert("RGBA")
    a = np.asarray(im)[:, :, 3]
    cols = (a > 8).sum(axis=0)
    runs, s = [], None
    for x in range(len(cols)):
        if cols[x] > 0 and s is None:
            s = x
        elif cols[x] == 0 and s is not None:
            runs.append((s, x - 1))
            s = None
    if s is not None:
        runs.append((s, len(cols) - 1))
    x0, x1 = runs[0]
    right = (a > 8)[:, x1 + 1:].sum(axis=1)
    rows, s = [], None
    for y in range(len(right)):
        if right[y] > 0 and s is None:
            s = y
        elif right[y] == 0 and s is not None:
            rows.append((s, y - 1))
            s = None
    pitch = sh.base - rows[0][1]
    Image.fromarray(np.asarray(im)[:, x0:x1 + 1]).save(os.path.join(OUT, "col_brace_crop.png"))
    br = Shard.__new__(Shard)
    br.path = os.path.join(OUT, "col_brace_crop.png")
    br.w = x1 - x0 + 1
    br.h = sh.h
    br.base = sh.base
    return br, pitch


def finish(canvas, name):
    a = np.asarray(canvas)[:, :, 3]
    ys, xs = np.where(a > 8)
    y0, y1 = max(int(ys.min()) - PAD, 0), min(int(ys.max()) + PAD, canvas.height)
    x0, x1 = max(int(xs.min()) - PAD, 0), min(int(xs.max()) + PAD, canvas.width)
    path = os.path.join(OUT, name)
    canvas.crop((x0, y0, x1, y1)).save(path)
    return round((x1 - x0) / DPI, 4), round((y1 - y0) / DPI, 4)


BR, PITCH = brace()
LINE = PITCH
X0 = 600
Y0 = 430


def seq(canvas, shards, x, base_y, gap):
    end = x
    for sh in shards:
        end = sh.paste(canvas, end, base_y) + gap
    return end


def piecewise(name, pre, lines):
    c = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    y1 = Y0 + LINE
    mid = (Y0 + y1) // 2
    end = seq(c, pre, X0, mid, 0)
    xb = BR.paste(c, end + 60, y1)
    xval = xb + 80
    vmax = 0
    ends = []
    for i, (val, cond) in enumerate(lines):
        base = Y0 if i == 0 else y1
        e = seq(c, val, xval, base, 0)
        vmax = max(vmax, e - xval)
        ends.append(e)
    for i, (val, cond) in enumerate(lines):
        base = Y0 if i == 0 else y1
        seq(c, cond, xval + vmax + 80, base, 0)
    return finish(c, name)


def simple(name, parts, lines=1):
    c = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    seq(c, parts, X0, Y0, 0)
    return finish(c, name)


def fraction(name, pre, num, den, bar_color):
    c = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    end = seq(c, pre, X0, Y0 + 150, 0)
    xn = end + 60
    n = num[0]
    n.paste(c, xn, Y0)
    xmax = xn + n.w
    d = den[0]
    dn = Y0 + 300
    for sh in den:
        xmax = sh.paste(c, xmax, dn) + 20
    mid = (Y0 + dn) // 2 + 8
    ImageDraw.Draw(c).rectangle([xn, mid, xmax - 20, mid + 6], fill=bar_color)
    return finish(c, name)
