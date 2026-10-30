#!/usr/bin/env python3
"""Slide 032 — fast decisive '?' vs '7' test on the right chord-endpoint label.

segments each label's ink into glyph column-groups, matches every group
INDEPENDENTLY (best of the two neighbour offsets) against character templates
rendered from serif/sans families, and ranks the resulting string.  A control
run on the original's known "(2, 10)" label proves the method before the
unknown is judged.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFont

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_032.jpg"
REND = DECK + "/recreated_pptx/qa/slide032/render_10.png"

FONTS = []
for p in ("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
    if os.path.exists(p):
        FONTS.append(p)

def load(path):
    return Image.open(path).convert("L")

def bmp(im, x0, y0, x1, y1, thr):
    px = im.load()
    return [[1 if px[x, y] < thr else 0 for x in range(x0, x1 + 1)] for y in range(y0, y1 + 1)]

def groups(bm, x0, gap=1):
    n = len(bm[0])
    ink = [any(bm[i][j] for i in range(len(bm))) for j in range(n)]
    out, run, empt = [], None, 0
    for j, v in enumerate(ink):
        if v:
            if run is None:
                run = [j, j]
            else:
                run[1] = j
            empt = 0
        elif run is not None:
            empt += 1
            if empt > gap:
                out.append((x0 + run[0], x0 + run[1]))
                run = None
    if run is not None:
        out.append((x0 + run[0], x0 + run[1]))
    return out

def trim(bm):
    rows = [r for r in bm if any(r)]
    if not rows:
        return None
    cols = [j for j in range(len(rows[0])) if any(r[j] for r in rows)]
    return [[r[j] for j in range(cols[0], cols[-1] + 1)] for r in rows]

def iou(a, b):
    a = trim(a)
    b = trim(b)
    if a is None or b is None:
        return 0.0
    H = max(len(a), len(b))
    W = max(len(a[0]), len(b[0]))
    A = [[0] * W for _ in range(H)]
    B = [[0] * W for _ in range(H)]
    for i, r in enumerate(a):
        for j, v in enumerate(r):
            A[i][j] = v
    for i, r in enumerate(b):
        for j, v in enumerate(r):
            B[i][j] = v
    inter = sum(A[i][j] and B[i][j] for i in range(H) for j in range(W))
    union = sum(A[i][j] or B[i][j] for i in range(H) for j in range(W))
    return inter / union if union else 0.0

def tmpl(ch, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    im = Image.new("L", (60, 60), 255)
    ImageDraw.Draw(im).text((10, 10), ch, fill=0, font=f)
    px = im.load()
    return trim([[1 if px[x, y] < 128 else 0 for x in range(60)] for y in range(60)])

def match(box, t, offs=((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1),
                          (1, -1), (1, 0), (1, 1))):
    """best IoU of template t over the group bitmap box"""
    H, W = len(box), len(box[0])
    h, w = len(t), len(t[0])
    best = 0.0
    for dy, dx in offs:
        for yi in range(0, H - h + 1):
            top = yi + dy
            if top < 0 or top + h > H:
                continue
            for xi in range(0, W - w + 1):
                left = xi + dx
                if left < 0 or left + w > W:
                    continue
                sub = [[box[top + yy][left + xx] for xx in range(w)] for yy in range(h)]
                v = iou(sub, t)
                if v > best:
                    best = v
    return best

def best_char(box, chars, fonts, sizes=range(8, 17)):
    best = (0.0, "")
    for fp in fonts:
        for s in sizes:
            for ch in chars:
                t = tmpl(ch, fp, s)
                if t is None:
                    continue
                v = match(box, t)
                if v > best[0]:
                    best = (v, ch)
    return best

def cmp_pair(box, a, b):
    ra = best_char(box, (a,), FONTS)
    rb = best_char(box, (b,), FONTS)
    return ra, rb

def show(bm, x0, y0, title):
    print(f"--- {title}: x{x0}..{x0+len(bm[0])-1} y{y0}..{y0+len(bm)-1} "
          f"({len(bm[0])}x{len(bm)})")
    print("     " + "".join(str((x0 + j) % 10) for j in range(len(bm[0]))))
    for i, r in enumerate(bm):
        print(f"{y0+i:4d} " + "".join("#" if v else "." for v in r))
    print()

def label_analysis(im, region, title, thr):
    x0, y0, x1, y1 = region
    bm = bmp(im, x0, y0, x1, y1, thr)
    show(bm, x0, y0, title)
    gs = groups(bm, x0, 1)
    print("  groups:", [(a, b) for a, b in gs])
    for gx0, gx1 in gs:
        if gx1 - gx0 + 1 < 2 or any(0 for _ in ()):
            pass
        sub = [[bm[i][j] for j in range(gx0 - x0, gx1 - x0 + 1)] for i in range(len(bm))]
        if not any(any(r) for r in sub):
            continue
        box = trim(sub)
        if box is None or len(box) < 3 or len(box[0]) < 2:
            continue
        cands = "?7,()"
        res = best_char(box, cands, FONTS)
        print(f"  glyph x{gx0}..{gx1} ({len(box[0])}x{len(box)}) -> "
              f"best '{res[1]}' IoU {res[0]:.4f}")
        if "?" in cands:
            for ch in cands:
                b = best_char(box, (ch,))
                print(f"      {ch!r}: {b:.4f}")
    print()
    return bm, gs

o = load(ORIG)
r = load(REND)
label_analysis(o, (726, 138, 754, 152), "ORIGINAL right-endpoint label", 190)
label_analysis(o, (617, 138, 662, 160), "ORIGINAL control '(2, 10)'", 190)
