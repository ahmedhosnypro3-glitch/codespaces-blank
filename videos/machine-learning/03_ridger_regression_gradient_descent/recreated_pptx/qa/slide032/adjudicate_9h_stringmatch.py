#!/usr/bin/env python3
"""Adjudicate_9h — decisive string match for the RIGHT point label.

Masks the black chord/dot out of BOTH search windows (x716..730: dot chord end),
then ranks candidate strings by best ink-cosine over an x/y/size search for each
image independently. The RENDER is the control: its text is known to be "(7, 7)"
(build/slide_032.js:200), so "(7, 7)" must win there. Whatever wins on the
ORIGINAL is what the original actually prints.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
GRAY = 102  # LABEL_GRAY 666666 lum

o = np.asarray(Image.open(V + "/unique_slides/slide_032.jpg").convert("L")).astype(float)
rim = Image.open(V + "/recreated_pptx/qa/slide032/render_9.png").convert("L")
rS = rim.size[1] / 540.0

CAND = ["(7, 7)", "(7,7)", "(?, ?)", "(?,?)", "(7, ?)", "(?, 7)", "(2, 2)", "(3, 3)",
        "(4, 4)", "(5, 5)", "(6, 6)", "(8, 8)", "(9, 9)", "(0, 0)", "(1, 1)",
        "(7, 10)", "(8, 10)", "(8,10)", "(7, 5)", "(7, 4)", "(7, 3)", "(7, 6)", "(7, 8)",
        "(7, 9)", "(7, 0)", "(8, 7)", "(8, 6)", "(8, 5)", "(8, 9)", "(?, 5)", "(8, ?)",
        "(3, 7)", "(6, 7)", "(5, 7)", "(4, 7)", "(2, 7)", "(9, 7)", "(0, 7)", "(1, 7)",
        "(7, 2)", "(7, 1)"]


def tmpl_ink(text, size):
    f = ImageFont.truetype(FONT, size)
    bb = f.getbbox(text)
    im = Image.new("L", (bb[2] - bb[0] + 6, bb[3] - bb[1] + 6), 255)
    ImageDraw.Draw(im).text((3 - bb[0], 3 - bb[1]), text, font=f, fill=GRAY)
    a = np.asarray(im).astype(float)
    return (255 - a) / 255.0


def scan(im, win, S, text, sizes):
    """im: full-array; win: frame bbox; S: px per frame px for that image"""
    x0, y0, x1, y1 = win
    W = np.asarray(Image.fromarray(im.astype(np.uint8)).crop(
        (int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))).astype(float) \
        if S != 1.0 else im[int(y0):int(y1), int(x0):int(x1)]
    wd = (255 - W) / 255.0
    best = -1
    bp = None
    for size in sizes:
        t = tmpl_ink(text, size)
        th, tw = t.shape
        if th > wd.shape[0] or tw > wd.shape[1]:
            continue
        for dy in range(wd.shape[0] - th + 1):
            for dx in range(wd.shape[1] - tw + 1):
                d = wd[dy:dy + th, dx:dx + tw]
                num = float((d * t).sum())
                den = float(np.sqrt((d * d).sum() * (t * t).sum())) or 1e-9
                s = num / den
                if s > best:
                    best, bp = s, (x0 + dx / S, y0 + dy / S, size)
    return best, bp


for tag, im, S, win, sizes in (
    ("ORIG", o, 1.0, (728, 138, 764, 158), range(8, 13)),
    ("REND9 (control)", np.asarray(rim).astype(float), rS, (712, 134, 768, 160),
     [round(10 * rS), round(9 * rS), round(11 * rS)]),
):
    print("=" * 76)
    print(f"### {tag}  window frame {win}")
    rows = []
    for text in CAND:
        s, bp = scan(im, win, S, text, sizes)
        rows.append((s, text, bp))
    rows.sort(reverse=True)
    for s, text, bp in rows[:12]:
        print(f"   {s:.4f}  at x{bp[0]:.0f} y{bp[1]:.0f} size{bp[2]}  {text!r}")
    print()
