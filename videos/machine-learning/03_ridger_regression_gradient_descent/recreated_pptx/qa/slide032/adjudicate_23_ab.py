#!/usr/bin/env python3
"""Slide 032 — A/B proof of the right chord-endpoint label (original vs the two
banked builds).

render_9.png  = the inherited build, label "(7, 7)"  (crop_9_graph FAIL)
render_10.png = current build,      label "(?, ?)" (the applied fix)
Both were built by the SAME script with the SAME label box and font; only the
glyph text differs.  Comparing the ORIGINAL's label ink against both renders is
therefore a direct empirical test of which text the frame carries.
"""
import os
from PIL import Image

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide032"
ORIG = DECK + "/unique_slides/slide_032.jpg"
R9 = QA + "/render_9.png"
R10 = QA + "/render_10.png"
SC = 2001.0 / 960.0   # render-px per frame-px on the x axis
SCY = 1125.0 / 540.0  # render-px per frame-px on the y axis

def load(p):
    return Image.open(p).convert("L")

def trim(bm):
    rows = [r for r in bm if any(r)]
    if not rows:
        return None
    cols = [j for j in range(len(rows[0])) if any(r[j] for r in rows)]
    return [[r[j] for j in range(cols[0], cols[-1] + 1)] for r in rows]

def bmp_frame(im_l, fx0, fy0, fx1, fy1, thr):
    """crop a frame-coordinate bbox out of a render image and binarise"""
    im = im_l.crop((max(0, round(fx0 * SC)) - 2, max(0, round(fy0 * SCY)) - 2,
                    min(im_l.size[0], round(fx1 * SC)) + 3,
                    min(im_l.size[1], round(fy1 * SCY)) + 3))
    px = im.load()
    return [[1 if px[x, y] < thr else 0 for x in range(im.size[0])] for y in range(im.size[1])]

def bmp_box(im, x0, y0, x1, y1, thr):
    px = im.load()
    return [[1 if px[x, y] < thr else 0 for x in range(x0, x1 + 1)] for y in range(y0, y1 + 1)]

def iou(a, b, tol=2):
    if a is None or b is None:
        return 0.0
    H = max(len(a), len(b))
    W = max(len(a[0]), len(b[0]))
    def place(bm):
        A = [[0] * W for _ in range(H)]
        for i, r in enumerate(bm):
            for j, v in enumerate(r):
                A[i][j] = v
        return A
    A = place(a)
    best = 0.0
    for dy in range(-tol, tol + 1):
        for dx in range(-tol, tol + 1):
            B = [[0] * W for _ in range(H)]
            for i, r in enumerate(b):
                for j, v in enumerate(r):
                    yy, xx = i + dy, j + dx
                    if 0 <= yy < H and 0 <= xx < W:
                        B[yy][xx] = v
            inter = sum(A[i][j] and B[i][j] for i in range(H) for j in range(W))
            union = sum(A[i][j] or B[i][j] for i in range(H) for j in range(W))
            if union:
                best = max(best, inter / union)
    return best

o_l = load(ORIG)
r9_l = load(R9)
r10_l = load(R10)

# ---- 1. global ink bbox of the label (label is RIGHT of the chord end x726) ----
print("=== label ink bbox (region x727..756, y136..154; excludes chord/dot) ===")
for thr in (170, 190, 210):
    a = trim(bmp_box(o_l, 727, 136, 756, 154, thr))
    b9 = trim(bmp_frame(r9_l, 727, 136, 756, 154, thr))
    b10 = trim(bmp_frame(r10_l, 727, 136, 756, 154, thr))
    fa = f"orig {len(a[0])}w x {len(a)}h" if a else "orig none"
    f9 = f"r9 {len(b9[0])}w x {len(b9)}h" if b9 else "r9 none"
    f10 = f"r10 {len(b10[0])}w x {len(b10)}h" if b10 else "r10 none"
    print(f"  thr{thr}: {fa} | {f9} | {f10}")

# ---- 2. IoU of the original label against each render's label ----
print("\n=== IoU(original label ink vs render label ink), best of +-2px ===")
for thr in (170, 190, 210):
    a = trim(bmp_box(o_l, 727, 136, 756, 154, thr))
    b9 = trim(bmp_frame(r9_l, 727, 136, 756, 154, thr))
    b10 = trim(bmp_frame(r10_l, 727, 136, 756, 154, thr))
    print(f"  thr{thr}: vs render_9 '(7, 7)' = {iou(a, b9):.4f}   "
          f"vs render_10 '(?, ?)' = {iou(a, b10):.4f}")

# ---- 3. bitmaps side by side ----
for name, tag in (("ORIGINAL", o_l), ("render_9 '(7, 7)'", r9_l), ("render_10 '(?, ?)'", r10_l)):
    if tag is o_l:
        bm = bmp_box(o_l, 727, 138, 756, 154, 190)
        print(f"--- {name} thr190 x727..756 y138..154")
        print("     " + "".join(str(x % 10) for x in range(727, 757)))
        for i, r in enumerate(bm):
            print(f"{138+i:4d} " + "".join("#" if v else "." for v in r))
    else:
        bm = bmp_frame(tag, 727, 137, 756, 155, 190)
        print(f"--- {name} thr190 (render px, frame-equivalent crop)")
        for i, r in enumerate(bm):
            print(f"{137+i:4d} " + "".join("#" if v else "." for v in r))
    print()

# ---- 4. are render_9 and render_10 identical everywhere else? ----
from PIL import ImageChops
p9 = Image.open(R9).convert("RGB")
p10 = Image.open(R10).convert("RGB")
d = ImageChops.difference(p9, p10)
bb = d.getbbox()
print("render_9 vs render_10 diff bbox:", bb)
h = p9.histogram()
if bb:
    px = d.load()
    xs, ys = [], []
    for y in range(bb[1], bb[3] + 1):
        for x in range(bb[0], bb[2] + 1):
            if any(px[x, y]):
                xs.append(x); ys.append(y)
    print("changed render-px region:", min(xs), max(xs), min(ys), max(ys),
          "= frame x", round(min(xs) / SC, 1), "..", round(max(xs) / SC, 1),
          " y", round(min(ys) / SCY, 1), "..", round(max(ys) / SCY, 1))
