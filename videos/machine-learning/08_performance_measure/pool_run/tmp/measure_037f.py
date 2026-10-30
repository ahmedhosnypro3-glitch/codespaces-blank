"""Measure slide_037 plot interior: annotation text bands, arrows, curves, fill, axis labels."""
from PIL import Image
from collections import Counter
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
im = Image.open(f"{NS}/unique_slides/slide_037.jpg").convert("RGB")
W, H = im.size
px = im.load()

PL, PT, PR, PB = 259, 217, 632, 512
mag = lambda p: p[0] > 100 and p[2] > 100 and p[1] < p[0] - 50 and p[1] < p[2] - 50
blu = lambda p: p[2] > 120 and p[2] > p[0] + 60 and p[2] > p[1] + 50
grn = lambda p: p[1] > 100 and p[1] > p[0] + 50 and p[1] > p[2] + 40
pale_yel = lambda p: p[0] > 235 and p[1] > 225 and p[2] < 215 and p[2] > 140
red = lambda p: p[0] > 120 and p[0] > p[1] + 60 and p[0] > p[2] + 60
dark = lambda p: sum(p) < 330

def rows_of(pred, x0, x1, y0, y1, min_n=6):
    out = []
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1) if pred(px[x, y]))
        out.append((y, n))
    return out

def bands(pred, x0, x1, y0, y1, min_n=6, gap=3):
    rs = rows_of(pred, x0, x1, y0, y1, min_n)
    out = []
    s = None
    for y, n in rs:
        if n >= min_n:
            if s is None: s = y
        else:
            if s is not None: out.append((s, y - 1)); s = None
    if s is not None: out.append((s, y1 - 1))
    merged = []
    for b in out:
        if merged and b[0] - merged[-1][1] <= gap: merged[-1] = (merged[-1][0], b[1])
        else: merged.append(b)
    return merged

def xext(pred, y0, y1, x0, x1):
    xs = [x for y in range(y0, y1 + 1) for x in range(x0, x1) if pred(px[x, y])]
    return (min(xs), max(xs)) if xs else None

print("== magenta bands inside plot ==")
for (a, b) in bands(mag, PL, PR + 1, PT, PB + 1, 5):
    print("  y=%d..%d x=%s" % (a, b, xext(mag, a, b, PL, PR + 1)))
print("== blue bands inside plot ==")
for (a, b) in bands(blu, PL, PR + 1, PT, PB + 1, 5):
    print("  y=%d..%d x=%s" % (a, b, xext(blu, a, b, PL, PR + 1)))
print("== green bands inside plot ==")
for (a, b) in bands(grn, PL, PR + 1, PT, PB + 1, 5):
    print("  y=%d..%d x=%s" % (a, b, xext(grn, a, b, PL, PR + 1)))
print("== pale-yellow fill rows in plot (n>40) ==")
for y, n in rows_of(pale_yel, PL + 2, PR - 1, PT, PB):
    if n > 40: print("  y=%d n=%d" % (y, n))
print("== red ink in/around plot ==")
for (a, b) in bands(red, 150, 960, 200, 540, 4):
    print("  y=%d..%d x=%s" % (a, b, xext(red, a, b, 150, 960)))
print("== dark bands in plot (curves/diagonal/axes) ==")
for (a, b) in bands(dark, PL, PR + 1, PT, PB + 1, 4):
    print("  y=%d..%d x=%s" % (a, b, xext(dark, a, b, PL, PR + 1)))

# axis label TPR: red or dark, left of plot x 230..258
print("TPR label search x 225..258:")
for (a, b) in bands(dark, 225, 259, PT, PB + 1, 3):
    print("  dark y=%d..%d x=%s" % (a, b, xext(dark, a, b, 225, 259)))
for (a, b) in bands(red, 225, 259, PT, PB + 1, 3):
    print("  red y=%d..%d x=%s" % (a, b, xext(red, a, b, 225, 259)))
# FPR label: below plot y 513..516 too thin; maybe inside plot bottom or above strip. search y 513..518
print("FPR label search y 513..518 x 259..700:")
for (a, b) in bands(dark, 259, 700, 513, 519, 3):
    print("  dark y=%d..%d x=%s" % (a, b, xext(dark, a, b, 259, 700)))
for (a, b) in bands(red, 259, 700, 513, 519, 3):
    print("  red y=%d..%d x=%s" % (a, b, xext(red, a, b, 259, 700)))
# also search whole strip area y 513..540 for red text (FPR might be on the strip)
for (a, b) in bands(red, 259, 960, 513, 540, 3):
    print("  red(strip) y=%d..%d x=%s" % (a, b, xext(red, a, b, 259, 960)))

# sample the diagonal: dark pixels along line from (259,512) to (632,217)?
print("diagonal check: for x, min/max dark y in plot excluding horizontal axis rows:")
for x in range(PL + 5, PR - 4, 20):
    ys = [y for y in range(PT + 2, PB - 1) if dark(px[x, y])]
    if ys: print("  x=%d darkys=%s" % (x, ys[:12]))
