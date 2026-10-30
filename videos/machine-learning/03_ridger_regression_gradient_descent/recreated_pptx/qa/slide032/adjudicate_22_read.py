#!/usr/bin/env python3
"""Slide 032 — size-matched glyph identification (no subset bias).

For every label ink group in the ORIGINAL, each candidate character template
must MATCH THE GROUP'S SIZE (trimmed w/h within 1px) before IoU is computed,
so a small template cannot score 1.0 by hiding inside a bigger blob.  A control
run on the original's own known "(2, 10)" label validates the method, then the
right chord-endpoint label is read.
"""
import os
from PIL import Image, ImageDraw, ImageFont

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_032.jpg"
REND = DECK + "/recreated_pptx/qa/slide032/render_10.png"

FONTS = [p for p in (
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
) if os.path.exists(p)]

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

def iou(a, b, tol=1):
    H = max(len(a) + tol, len(b))
    W = max(len(a[0]) + tol, len(b[0]))
    A = [[0] * W for _ in range(H)]
    B = [[0] * W for _ in range(H)]
    for i, r in enumerate(a):
        for j, v in enumerate(r):
            A[i][j] = v
    for i, r in enumerate(b):
        for j, v in enumerate(r):
            B[i + 0][j + 0] = v
    best = 0.0
    for dy in range(-tol, tol + 1):
        for dx in range(-tol, tol + 1):
            B2 = [[0] * W for _ in range(H)]
            for i, r in enumerate(b):
                for j, v in enumerate(r):
                    yy, xx = i + dy, j + dx
                    if 0 <= yy < H and 0 <= xx < W:
                        B2[yy][xx] = v
            inter = sum(A[i][j] and B2[i][j] for i in range(H) for j in range(W))
            union = sum(A[i][j] or B2[i][j] for i in range(H) for j in range(W))
            if union:
                best = max(best, inter / union)
    return best

CACHE = {}
def tmpl(ch, fontpath, size):
    key = (ch, fontpath, size)
    if key in CACHE:
        return CACHE[key]
    f = ImageFont.truetype(fontpath, size)
    im = Image.new("L", (60, 60), 255)
    ImageDraw.Draw(im).text((10, 10), ch, fill=0, font=f)
    px = im.load()
    t = trim([[1 if px[x, y] < 128 else 0 for x in range(60)] for y in range(60)])
    CACHE[key] = t
    return t

def identify(box, chars, tol=1):
    out = []
    for fp in FONTS:
        for s in range(7, 20):
            for ch in chars:
                t = tmpl(ch, fp, s)
                if t is None:
                    continue
                if abs(len(t) - len(box)) > tol or abs(len(t[0]) - len(box[0])) > tol:
                    continue
                out.append((iou(box, t, tol=tol), ch, os.path.basename(fp), s))
    out.sort(reverse=True)
    return out

def show(bm, x0, y0, title):
    print(f"--- {title}: x{x0}..{x0+len(bm[0])-1} y{y0}..{y0+len(bm)-1} "
          f"({len(bm[0])}w x {len(bm)}h)")
    print("     " + "".join(str((x0 + j) % 10) for j in range(len(bm[0]))))
    for i, r_ in enumerate(bm):
        print(f"{y0+i:4d} " + "".join("#" if v else "." for v in r_))
    print()

def analyse(im, region, title, thr, chars):
    x0, y0, x1, y1 = region
    bm = bmp(im, x0, y0, x1, y1, thr)
    show(bm, x0, y0, title)
    read = []
    for gx0, gx1 in groups(bm, x0, 1):
        sub = [[bm[i][j] for j in range(gx0 - x0, gx1 - x0 + 1)] for i in range(len(bm))]
        box = trim(sub)
        if box is None:
            continue
        w, h = len(box[0]), len(box)
        res = identify(box, chars)
        top = res[:3]
        print(f"  glyph x{gx0}..{gx1} ({w}w x {h}h): " +
              ", ".join(f"{ch!r} {v:.3f} ({fn} {s}pt)" for v, ch, fn, s in top))
        read.append(top[0][1] if top else "?")
    print(f"  => reading: {''.join(read)}\n")
    return "".join(read)

o = load(ORIG)
print("############ CONTROL: original's own '(2, 10)' ############")
analyse(o, (617, 136, 663, 161), "CONTROL", 190, "0123456789?,()-")
print("############ RIGHT chord-endpoint label ############")
analyse(o, (712, 130, 762, 158), "RIGHT label", 190, "0123456789?,()")
