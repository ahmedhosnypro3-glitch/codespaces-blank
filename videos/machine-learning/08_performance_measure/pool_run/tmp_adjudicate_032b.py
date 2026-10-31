#!/usr/bin/env python3
"""Pass 2: precise measurements for slide-32 findings 2,4,5,6,7."""
from PIL import Image
import numpy as np
from collections import Counter

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/"
orig = np.array(Image.open(NS + "unique_slides/slide_032.jpg").convert("RGB")).astype(int)
ren = np.array(Image.open(NS + "recreated_pptx/qa/slide032/render.png").convert("RGB")).astype(int)
S = ren.shape[1] / 960.0

def is_red(p):    return p[0] > 110 and p[0] > p[1] * 1.6 and p[0] > p[2] * 1.6 and p[1] < 130
def is_dark(p):   return p[0] < 90 and p[1] < 90 and p[2] < 90
def is_blue(p):   return p[2] > 110 and p[2] > p[0] * 1.3 and p[2] > p[1] * 1.15
def is_cream(p):  return p[0] > 235 and p[1] > 225 and 185 < p[2] < 246
def any_ink(p):   return not (p[0] > 235 and p[1] > 235 and p[2] > 235)

def region(img, x0, y0, x1, y1, sc=1.0):
    return img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]

print("=== 2. Axis label colors (orig) ===")
# TPR vertical label: left of y-axis line x~661; region x[644,659] y[150,330]
sub = region(orig, 644, 150, 659, 330)
cnt = Counter()
for p in sub.reshape(-1, 3):
    if any_ink(p):
        cnt[(p[0]//40*40, p[1]//40*40, p[2]//40*40)] += 1
print("orig TPR-region ink color buckets:", cnt.most_common(6))
redp = [p for p in sub.reshape(-1,3) if is_red(p)]
darkp = [p for p in sub.reshape(-1,3) if is_dark(p)]
print(f"orig TPR region: red n={len(redp)} med={np.median(redp,0).astype(int) if redp else None}; dark n={len(darkp)} med={np.median(darkp,0).astype(int) if darkp else None}")
# FPR label: below x-axis y~351; region y[354,376] x[750,820]
sub = region(orig, 750, 354, 820, 376)
redp = [p for p in sub.reshape(-1,3) if is_red(p)]
darkp = [p for p in sub.reshape(-1,3) if is_dark(p)]
cnt = Counter()
for p in sub.reshape(-1, 3):
    if any_ink(p):
        cnt[(p[0]//40*40, p[1]//40*40, p[2]//40*40)] += 1
print("orig FPR-region ink buckets:", cnt.most_common(6))
print(f"orig FPR region: red n={len(redp)} med={np.median(redp,0).astype(int) if redp else None}; dark n={len(darkp)} med={np.median(darkp,0).astype(int) if darkp else None}")
# render counterparts
sub = region(ren, 644, 150, 659, 330, S)
redp = [p for p in sub.reshape(-1,3) if is_red(p)]
darkp = [p for p in sub.reshape(-1,3) if is_dark(p)]
print(f"render TPR region: red n={len(redp)}; dark n={len(darkp)} med={np.median(darkp,0).astype(int) if darkp else None}")
sub = region(ren, 750, 354, 820, 376, S)
redp = [p for p in sub.reshape(-1,3) if is_red(p)]
darkp = [p for p in sub.reshape(-1,3) if is_dark(p)]
print(f"render FPR region: red n={len(redp)}; dark n={len(darkp)} med={np.median(darkp,0).astype(int) if darkp else None}")
# where exactly is orig TPR text? ink bbox in x[640,662] y[100,350] excluding red axis line cols 660-663
sub = region(orig, 640, 100, 660, 350)
mask = np.array([[any_ink(p) and not is_red(p) for p in row] for row in sub])
ys, xs = np.where(mask)
if len(xs): print(f"orig non-red ink near y-axis: x[{640+xs.min()},{640+xs.max()}] y[{100+ys.min()},{100+ys.max()}] n={len(xs)}")

print("\n=== gridline colors in plot ===")
# orig: vertical gridline at x~708? find columns in y[100,340] x[665,895] with many nonwhite non-red pixels
sub = region(orig, 665, 100, 895, 340)
colcount = []
for j in range(sub.shape[1]):
    col = sub[:, j]
    n = sum(1 for p in col if any_ink(p) and not is_red(p) and not is_cream(p))
    colcount.append((665 + j, n))
top = sorted(colcount, key=lambda t: -t[1])[:8]
print("orig vertical gridline cols (x,count):", top)
for x, n in top[:4]:
    col = orig[100:340, x]
    px = [p for p in col if any_ink(p) and not is_red(p)]
    if px: print(f"  x={x} median rgb={np.median(px,0).astype(int)}")
rowcount = []
for i in range(sub.shape[0]):
    row = sub[i]
    n = sum(1 for p in row if any_ink(p) and not is_red(p) and not is_cream(p))
    rowcount.append((100 + i, n))
top = sorted(rowcount, key=lambda t: -t[1])[:8]
print("orig horizontal gridline rows (y,count):", top)
for y, n in top[:4]:
    row = orig[y, 665:895]
    px = [p for p in row if any_ink(p) and not is_red(p)]
    if px: print(f"  y={y} median rgb={np.median(px,0).astype(int)}")
# render gridline color
sub = region(ren, 665, 100, 895, 340, S)
cols = []
for j in range(0, sub.shape[1], 3):
    col = sub[:, j]
    n = sum(1 for p in col if any_ink(p) and not is_red(p) and not is_cream(p))
    cols.append((665 + j / S, n))
top = sorted(cols, key=lambda t: -t[1])[:6]
print("render vertical gridline cols (frame-x,count):", [(round(x,1), n) for x, n in top])
for x, n in top[:3]:
    j = int((x - 665) * S)
    col = ren[int(100*S):int(340*S), j]
    px = [p for p in col if any_ink(p) and not is_red(p)]
    if px: print(f"  x={x:.1f} median rgb={np.median(px,0).astype(int)}")

print("\n=== 4. marker + chip precise positions ===")
def red_clusters(img, x0, y0, x1, y1, sc, minn):
    sub = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]
    mask = np.array([[is_red(p) for p in row] for row in sub])
    ys, xs = np.where(mask)
    pts = list(zip(xs/sc + x0, ys/sc + y0))
    clusters = []
    for (x, y) in pts:
        for c in clusters:
            if abs(c[0]-x) < 25 and abs(c[1]-y) < 25:
                c[0] = (c[0]*c[2]+x)/(c[2]+1); c[1] = (c[1]*c[2]+y)/(c[2]+1); c[2] += 1
                break
        else:
            clusters.append([x, y, 1])
    return sorted([(round(c[0],1), round(c[1],1), c[2]) for c in clusters if c[2] > minn], key=lambda t: t[0])
print("orig red marker clusters:", red_clusters(orig, 665, 85, 895, 350, 1, 15))
print("render red marker clusters:", red_clusters(ren, 665, 85, 895, 350, S, 30))
def cream_chips(img, x0, y0, x1, y1, sc, minn):
    sub = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]
    mask = np.array([[is_cream(p) for p in row] for row in sub])
    ys, xs = np.where(mask)
    pts = list(zip(xs/sc + x0, ys/sc + y0))
    clusters = []
    for (x, y) in pts:
        for c in clusters:
            if abs(c[0]-x) < 35 and abs(c[1]-y) < 22:
                # bbox-style cluster
                c[0] = min(c[0], x); c[1] = min(c[1], y)
                c[2] = max(c[2], x); c[3] = max(c[3], y); c[4] += 1
                break
        else:
            clusters.append([x, y, x, y, 1])
    return sorted([(round((c[0]+c[2])/2,1), round((c[1]+c[3])/2,1), round(c[2]-c[0],1), round(c[3]-c[1],1), c[4]) for c in clusters if c[4] > minn], key=lambda t: (t[1], t[0]))
print("orig cream chips (cx,cy,w,h,n):", cream_chips(orig, 665, 85, 895, 350, 1, 60))
print("render cream chips (cx,cy,w,h,n):", cream_chips(ren, 665, 85, 895, 350, S, 120))

print("\n=== 5. caption text: bright red vs maroon (orig) ===")
sub = region(orig, 360, 432, 615, 468)
bright = [p for p in sub.reshape(-1,3) if p[0] > 200 and p[1] < 90 and p[2] < 90]
allred = [p for p in sub.reshape(-1,3) if is_red(p)]
print(f"orig caption inner: bright-red n={len(bright)}; all red n={len(allred)} med={np.median(allred,0).astype(int) if allred else None}")
print("orig caption red percentiles:", np.percentile(np.array(allred), [50, 90, 99], axis=0).astype(int) if allred else None)

print("\n=== 6. bottom-right matrix Actual vs P/N (orig vs render) ===")
for name, img, sc in [("orig", orig, 1), ("render", ren, S)]:
    sub = region(img, 762, 438, 820, 499, sc)
    # column ink profile excluding red border lines (x=771 border, x=800 border)
    prof = []
    for j in range(sub.shape[1]):
        col = sub[:, j]
        n = sum(1 for p in col if any_ink(p))
        prof.append((762 + j / sc, n))
    ink_cols = [(round(x,1), n) for x, n in prof if n > 2]
    print(f"{name} ink columns x[762,820]:", ink_cols)
    # red ink columns (Actual text if red)
    rprof = []
    for j in range(sub.shape[1]):
        col = sub[:, j]
        n = sum(1 for p in col if is_red(p))
        rprof.append((762 + j / sc, n))
    print(f"{name} red-ink columns:", [(round(x,1), n) for x, n in rprof if n > 2])

print("\n=== 7. threshold label '=' analysis, row1 box orig x[61,160] y[50,78] ===")
for name, img, sc in [("orig", orig, 1), ("render", ren, S)]:
    sub = region(img, 63, 53, 158, 75, sc)  # interior, avoid border
    mask = np.array([[any_ink(p) for p in row] for row in sub])
    # column profile
    colprof = mask.sum(axis=0)
    ink_cols = [j for j, v in enumerate(colprof) if v > 0]
    if not ink_cols:
        print(f"{name}: no ink"); continue
    # find gaps to segment glyphs
    glyphs = []
    cur = [ink_cols[0]]
    for j in ink_cols[1:]:
        if j - cur[-1] <= 1:
            cur.append(j)
        else:
            glyphs.append((cur[0], cur[-1])); cur = [j]
    glyphs.append((cur[0], cur[-1]))
    print(f"{name}: glyph col-groups (rel x): {[(a, b) for a, b in glyphs]}")
    # for the middle groups (the = sign), count row segments
    for (a, b) in glyphs:
        if 3 <= (b - a) <= 8:  # narrow glyph like = or -
            col = mask[:, a:b+1]
            rows = col.sum(axis=1)
            segs = []
            cur = None
            for i, v in enumerate(rows):
                if v > 0 and cur is None: cur = i
                elif v == 0 and cur is not None: segs.append((cur, i-1)); cur = None
            if cur is not None: segs.append((cur, len(rows)-1))
            print(f"  {name} narrow glyph x[{a},{b}] row-segments: {segs}")
