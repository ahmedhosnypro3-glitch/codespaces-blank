#!/usr/bin/env python3
"""Slide 032 — independent PIL adjudication of the crop_9_graph FAIL.

Question: the right chord-endpoint label in the ORIGINAL frame — does it read
"(?, ?)" (a blank/to-be-filled coordinate) or "(7, 7)"?

Method (numbers only, no vision):
  * locate the label ink in the original frame (960x540, 1px=1pt)
  * segment it into glyph column-groups
  * print each glyph as an ASCII bitmap
  * compare against font templates rendered locally for '?' and '7'
    (Liberation Serif / Times family — the frame's typeface, per the build's
    own measurement notes)
  * use the font-independent signature of '?' (bottom dot separated from the
    body by a blank row) vs '7' (top horizontal bar, continuous diagonal)
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/worksp""aces/codespaces-blank/ai_llm_slides"
DECK = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
ORIG = os.path.join(DECK, "unique_slides/slide_032.jpg")
REND = os.path.join(DECK, "recreated_pptx/qa/slide032/render_10.png")
HERE = os.path.dirname(os.path.abspath(__file__))

def load(p):
    return Image.open(p).convert("L")

def ascii_art(im, x0, y0, x1, y1, thr=170, invert=False, label=""):
    print(f"--- {label}  region x{x0}..{x1} y{y0}..{y1}  (thr<{thr}) ---")
    px = im.load()
    for y in range(y0, y1):
        row = ""
        for x in range(x0, x1):
            v = px[x, y]
            ink = v < thr
            if invert:
                ink = not ink
            row += "#" if ink else "."
        print(f"{y:4d} {row}")
    print()

def ink_cols(im, x0, y0, x1, y1, thr=170):
    px = im.load()
    cols = []
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if px[x, y] < thr)
        cols.append((x, n))
    return cols

def ink_rows(im, x0, y0, x1, y1, thr=170):
    px = im.load()
    rows = []
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1) if px[x, y] < thr)
        rows.append((y, n))
    return rows

def group_cols(cols, gap=1):
    groups, cur, prev = [], [], None
    for x, n in cols:
        if n > 0:
            if prev is not None and x - prev > gap:
                groups.append((cur[0], cur[-1]))
                cur = []
            cur.append(x)
        prev = x
    if cur:
        groups.append((cur[0], cur[-1]))
    return groups

def bitmap(im, x0, y0, x1, y1, thr=170):
    px = im.load()
    return [[1 if px[x, y] < thr else 0 for x in range(x0, x1 + 1)] for y in range(y0, y1 + 1)]

def print_bmp(bm, x0=0, y0=0, title=""):
    print(f"  [{title}] {len(bm[0])}x{len(bm)} at ({x0},{y0})")
    for r in bm:
        print("   " + "".join("#" if v else "." for v in r))
    print()

def shape_sig(bm):
    """font-independent signature: row ink counts + blank-row gaps + top/bottom row spans"""
    rows = [sum(r) for r in bm]
    if not rows or max(rows) == 0:
        return None
    top = next(i for i, v in enumerate(rows) if v > 0)
    bot = len(rows) - 1 - next(i for i, v in enumerate(reversed(rows)) if v > 0)
    gaps = [i for i, v in enumerate(rows) if v == 0]
    # internal blank rows (between first and last ink row)
    inner_gaps = [i for i in gaps if top < i < bot]
    def span(i):
        r = bm[i]
        idx = [j for j, v in enumerate(r) if v]
        return (idx[0], idx[-1], len(idx)) if idx else None
    return {
        "h": bot - top + 1,
        "top_row_span": span(top),
        "bot_row_span": span(bot),
        "inner_blank_rows": inner_gaps,
        "row_counts": rows[top:bot + 1],
    }

def find_font():
    cands = [
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    return None

def render_glyph(ch, size, fontpath):
    f = ImageFont.truetype(fontpath, size)
    im = Image.new("L", (40, 40), 255)
    d = ImageDraw.Draw(im)
    d.text((10, 5), ch, fill=0, font=f)
    bb = im.point(lambda v: 255 if v < 200 else 0).getbbox()
    if bb is None:
        return None
    return im.crop(bb)

def bmp_norm(bm):
    """crop to ink bbox, return binary bitmap"""
    rows = [r for r in bm if any(r)]
    if not rows:
        return None
    w = max(len(r) for r in rows)
    # trim empty columns
    cols = [j for j in range(w) if any(r[j] for r in rows)]
    j0, j1 = cols[0], cols[-1]
    return [[r[j] for j in range(j0, j1 + 1)] for r in rows]

def dist(a, b):
    """Jaccard distance between two binary bitmaps, aligned at bbox origin."""
    a = bmp_norm(a); b = bmp_norm(b)
    if a is None or b is None:
        return 1.0
    h = max(len(a), len(b)); w = max(len(a[0]), len(b[0]))
    A = [[0] * w for _ in range(h)]; B = [[0] * w for _ in range(h)]
    for i, r in enumerate(a):
        for j, v in enumerate(r):
            A[i][j] = v
    for i, r in enumerate(b):
        for j, v in enumerate(r):
            B[i][j] = v
    inter = sum(A[i][j] & B[i][j] for i in range(h) for j in range(w))
    union = sum(A[i][j] | B[i][j] for i in range(h) for j in range(w))
    return 1.0 - (inter / union if union else 0.0)

def main():
    orig = load(ORIG)
    rend = load(REND)
    print("original size", orig.size, "render size", rend.size)
    scale = rend.size[1] / 540.0
    print("render scale", round(scale, 4))

    # ---- locate the label region in the ORIGINAL by ink map -------------
    print("\n================= ORIGINAL: raw ink map near right chord endpoint =================")
    X0, X1, Y0, Y1 = 700, 790, 125, 165
    ascii_art(orig, X0, Y0, X1, Y1, thr=170, label="ORIG raw")
    print("column ink counts (ORIG x700..790):")
    for x, n in ink_cols(orig, X0, Y0, X1, Y1):
        print(f"  x={x} n={n}")
    print("\nrow ink counts (ORIG y125..165):")
    for y, n in ink_rows(orig, X0, Y0, X1, Y1):
        print(f"  y={y} n={n}")

if __name__ == "__main__":
    main()
