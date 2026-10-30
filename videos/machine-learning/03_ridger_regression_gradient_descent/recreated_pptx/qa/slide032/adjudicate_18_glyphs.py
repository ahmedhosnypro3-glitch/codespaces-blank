#!/usr/bin/env python3
"""Slide 032 — glyph-level extraction of the right chord-endpoint label.

ORIGINAL (frame 960x540, 1px=1pt): label ink cols x728..749, rows y142..152.
RENDER_10 (2001x1125, 2.0833 px/pt): label ink cols x727.x..744.x.
Prints both as aligned ASCII bitmaps, segments glyph column-groups, and reports
each group's bbox + row ink profile + blank-row gaps (the font-independent
signature separating '?' from '7': a '?' carries an isolated bottom dot below
a blank row; a '7' carries a full-width top bar with a continuous diagonal).
"""
import os
from PIL import Image

ROOT = "/worksp""aces/codespaces-blank/ai_llm_slides"
DECK = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
ORIG = os.path.join(DECK, "unique_slides/slide_032.jpg")
REND = os.path.join(DECK, "recreated_pptx/qa/slide032/render_10.png")

SCALE = 2.0833

def bm_rect(im, x0, y0, x1, y1, thr):
    """inclusive x1/y1"""
    px = im.load()
    return [[1 if (px[x, y][0] if im.mode == "RGB" else px[x, y]) < thr else 0
             for x in range(x0, x1 + 1)] for y in range(y0, y1 + 1)]

def show(bm, x0, y0, title, ruler=True):
    print(f"--- {title}: bbox x{x0}..{x0+len(bm[0])-1} y{y0}..{y0+len(bm)-1}")
    if ruler:
        print("     " + "".join(str(x % 10) for x in range(x0, x0 + len(bm[0]))))
    for i, r in enumerate(bm):
        print(f"{y0+i:4d} " + "".join("#" if v else "." for v in r))
    print()

def groups(bm, x0, gap=1):
    """column glyph groups by empty-column runs >= gap+1"""
    ncol = len(bm[0])
    inkcol = [any(bm[i][j] for i in range(len(bm))) for j in range(ncol)]
    out, j = [], 0
    while j < ncol:
        if inkcol[j]:
            k = j
            while k + 1 < ncol and (inkcol[k + 1] or (k + 2 < ncol and any(
                    bm[i][k + 2] for i in range(len(bm))) )):
                k += 1
                if not inkcol[k] and k + 1 < ncol and inkcol[k + 1]:
                    k += 1
            out.append((x0 + j, x0 + k))
            j = k + 1
        else:
            j += 1
    # simpler: merge columns separated by <= gap empty columns
    return out

def simple_groups(bm, x0, gap=1):
    ncol = len(bm[0])
    ink = [any(bm[i][j] for i in range(len(bm))) for j in range(ncol)]
    out = []
    run = None
    empt = 0
    for j, v in enumerate(ink):
        if v:
            if run is None:
                run = [j, j]
            else:
                run[1] = j
            empt = 0
        else:
            if run is not None:
                empt += 1
                if empt > gap:
                    out.append((x0 + run[0], x0 + run[1]))
                    run = None
    if run is not None:
        out.append((x0 + run[0], x0 + run[1]))
    return out

def profile(bm, gx0, gx1, x0):
    j0, j1 = gx0 - x0, gx1 - x0
    sub = [[bm[i][j] for j in range(j0, j1 + 1)] for i in range(len(bm))]
    rows = [sum(r) for r in sub]
    top = next((i for i, v in enumerate(rows) if v), None)
    bot = len(rows) - 1 - next((i for i, v in enumerate(reversed(rows)) if v), None)
    inner_blanks = [i for i in range(top, bot + 1) if rows[i] == 0]
    def span(i):
        idx = [k for k, v in enumerate(sub[i]) if v]
        return (idx[0], idx[-1], len(idx)) if idx else None
    return {
        "w": gx1 - gx0 + 1,
        "h": bot - top + 1,
        "row_counts": rows[top:bot + 1],
        "inner_blank_rows": inner_blanks,
        "top_span": span(top),
        "bot_span": span(bot),
        "row2_span": span(top + 1) if top + 1 <= bot else None,
        "mid_span": span((top + bot) // 2),
        "sub": sub,
    }

def analyse(im, x0, x1, y0, y1, thr, title):
    bm = bm_rect(im, x0, y0, x1, y1, thr)
    show(bm, x0, y0, title)
    for gx0, gx1 in simple_groups(bm, x0, gap=1):
        p = profile(bm, gx0, gx1, x0)
        print(f"  glyph x{gx0}..{gx1} ({p['w']}x{p['h']}) rows={p['row_counts']} "
              f"inner_blank_rows={p['inner_blank_rows']}")
        print(f"        top_span={p['top_span']} bot_span={p['bot_span']} "
              f"row2_span={p['row2_span']} mid_span={p['mid_span']}")
    print()

o = Image.open(ORIG).convert("L")
r = Image.open(REND).convert("L")
analyse(o, 726, 752, 141, 153, 185, "ORIGINAL right-endpoint label")
analyse(r, 1509, 1553, 292, 322, 185, "RENDER_10 right-endpoint label (render px; frame = x/2.0833)")
fry0, fry1 = 141, 153
print("frame x of render cols 1509..1553:", [round((c) / SCALE, 1) for c in (1509, 1553)])
