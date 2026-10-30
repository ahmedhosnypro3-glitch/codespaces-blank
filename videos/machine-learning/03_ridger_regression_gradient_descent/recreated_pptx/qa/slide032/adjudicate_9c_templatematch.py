#!/usr/bin/env python3
"""Adjudicate_9c — objective glyph identification for the right-label finding #1.

Template-match candidate strings against the ORIGINAL frame's right-label window,
using the SAME serif family the build uses (Liberation Serif == Times New Roman
metrics), over a size range and full x/y alignment search.

The known RENDER text "(7, 7)" is used as a control: it must win on the render.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

o = np.asarray(Image.open((V + "/unique_slides/slide_032.jpg")).convert("L")).astype(float)
r = np.asarray(Image.open((V + "/recreated_pptx/qa/slide032/render_9.png")).convert("L")).astype(float)
oS = 1.0
rS = r.shape[0] / 540.0

CAND = ["(7, 7)", "(7,7)", "(?, ?)", "(?,?)", "(2, 2)", "(3, 3)", "(4, 4)", "(5, 5)",
        "(6, 6)", "(8, 8)", "(9, 9)", "(0, 0)", "(1, 1)", "(7, 5)", "(7, 6)", "(7, 8)",
        "(7, 9)", "(7, 0)", "(7, 3)", "(8, 7)", "(8, 10)", "(8,10)", "(7, 7?)", "(?, 7)"]


def render_string(text, size):
    """ink bitmap of `text` in Liberation Serif at px size; returns (bitmap, w, h)"""
    f = ImageFont.truetype(FONT, size)
    bb = f.getbbox(text)
    w, h = max(bb[2] - bb[0], 1) + 4, max(bb[3] - bb[1], 1) + 4
    im = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(im)
    d.text((2 - bb[0], 2 - bb[1]), text, font=f, fill=0)
    a = np.asarray(im).astype(float)
    return 255 - a, w, h


def score(win, text, size):
    """best ink-weighted correlation of `text` inside `win` over all alignments"""
    tmpl, tw, th = render_string(text, size)
    t = (255 - tmpl) / 255.0                      # 1 = ink
    wh, ww = win.shape
    best = -1e9; bestpos = None
    if tw + 2 > ww or th + 2 > wh:
        return -1e9, None
    if t.sum() < 1:
        return -1e9, None
    for dy in range(0, wh - th + 1):
        for dx in range(0, ww - tw + 1):
            w = win[dy:dy + th, dx:dx + tw]
            d = (255 - w) / 255.0
            # normalized ink-product: rewards matching ink, ignores white-white
            num = float((d * t).sum())
            den = float(np.sqrt((d * d).sum() * (t * t).sum())) or 1e-9
            s = num / den
            if s > best:
                best, bestpos = s, (dx, dy)
    return best, bestpos


# ORIG right-label window (frame px) — contains the dot at x716..726, chord at
# y145..148, and the two label glyphs at x~735..758.
WIN = (722, 140, 762, 156)
for tag, im, S in (("ORIG", o, oS), ("REND9", r, rS)):
    print("=" * 72)
    print(f"### {tag} — right-label window frame x{WIN[0]}..{WIN[2]} y{WIN[1]}..{WIN[3]}")
    x0, y0, x1, y1 = WIN
    win = im[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    rows = []
    for text in CAND:
        bestall, bestsz, bestpos = -1e9, None, None
        for size in range(8, 14):
            s, pos = score(win, text, size)
            if s > bestall:
                bestall, bestsz, bestpos = s, size, pos
        rows.append((bestall, text, bestsz, bestpos))
    rows.sort(reverse=True)
    for s, text, size, pos in rows:
        print(f"   {s:.4f}  size {size:>2}  dx{pos[0]} dy{pos[1]}  {text!r}")
    print()
