#!/usr/bin/env python3
"""Pixel adjudication of judge_verify_v2 findings for slide 32.
Original: unique_slides/slide_032.jpg (960x540, 1px=1pt).
Render: recreated_pptx/qa/slide032/render.png (2001x1125 @150dpi; s=2001/960).
"""
from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/"
orig = np.array(Image.open(NS + "unique_slides/slide_032.jpg").convert("RGB")).astype(int)
ren = np.array(Image.open(NS + "recreated_pptx/qa/slide032/render.png").convert("RGB")).astype(int)
S = ren.shape[1] / 960.0
print("orig", orig.shape, "render", ren.shape, "S=%.4f" % S)

def classify(px):
    r, g, b = px
    if r > 180 and g > 180 and b > 180:
        return "white/light"
    if r > 120 and g < 90 and b < 90:
        return "red"
    if b > 120 and r < 110 and g < 140:
        return "blue"
    if r < 80 and g < 80 and b < 80:
        return "dark"
    if g > 150 and r > 150 and b < 160:
        return "green/yellow"
    if r > 230 and g > 230 and b > 200:
        return "cream/yellow"
    if b > 200 and g > 230 and r > 200:
        return "cyan"
    return f"other({r},{g},{b})"

def ink_bbox(img, x0, y0, x1, y1, pred, scale=1.0):
    """bounding box of pixels matching pred in region (coords in 960x540 frame px)."""
    X0, Y0, X1, Y1 = [int(round(v * scale)) for v in (x0, y0, x1, y1)]
    sub = img[Y0:Y1, X0:X1]
    mask = np.zeros(sub.shape[:2], bool)
    for i in range(sub.shape[0]):
        for j in range(sub.shape[1]):
            if pred(sub[i, j]):
                mask[i, j] = True
    if not mask.any():
        return None
    ys, xs = np.where(mask)
    return (X0 + xs.min(), Y0 + ys.min(), X0 + xs.max(), Y0 + ys.max()), int(mask.sum())

def is_red(p):    return p[0] > 110 and p[0] > p[1] * 1.6 and p[0] > p[2] * 1.6 and p[1] < 120
def is_dark(p):   return p[0] < 90 and p[1] < 90 and p[2] < 90
def is_blue(p):   return p[2] > 110 and p[2] > p[0] * 1.4 and p[2] > p[1] * 1.2
def is_cyan(p):   return p[2] > 200 and p[1] > 220 and p[0] > 190 and p[0] < 245
def is_cream(p):  return p[0] > 235 and p[1] > 225 and 190 < p[2] < 245
def any_ink(p):   return not (p[0] > 235 and p[1] > 235 and p[2] > 235)

print("\n=== 1. TOP BAND: original title? render title collision? ===")
# original: ink in top band y[10,60] excluding frame/badge region
for y0, y1 in [(10, 42), (42, 60)]:
    bb = ink_bbox(orig, 40, y0, 900, y1, any_ink)
    print(f"orig ink bbox y[{y0},{y1}] x[40,900]:", bb)
# original frame top line: find red rows near top
for y in range(5, 60):
    row = orig[y, 100:900]
    reds = sum(1 for p in row if is_red(p))
    if reds > 200:
        print(f"orig red horizontal line at y={y} (reds={reds})")
# render: title text = red ink in y[15,80] frame-px (=render y*S)
bb = ink_bbox(ren, 40, 12, 920, 80, is_red, S)
print("render red-ink bbox in top band (render px):", bb)
if bb:
    (x0, y0, x1, y1), n = bb
    print("  in frame px: x[%.0f,%.0f] y[%.1f,%.1f]" % (x0 / S, x1 / S, y0 / S, y1 / S))
# render: maroon/red border lines & blue divider in top band
for y in range(int(30 * S), int(85 * S)):
    row = ren[y, int(100 * S):int(900 * S)]
    reds = sum(1 for p in row if is_red(p))
    if reds > 300:
        print(f"render red horiz line y={y} frame-y={y/S:.1f} reds={reds}")
col = ren[:, int(342 * S)]
blues = [y for y in range(int(30 * S), int(520 * S)) if is_blue(col[y])]
if blues:
    print(f"render blue divider x=342: frame-y [{blues[0]/S:.1f},{blues[-1]/S:.1f}]")
# maroon right border of left panel x=635 in render: column scan
col = ren[:, int(635 * S)]
reds = [y for y in range(int(30 * S), int(520 * S)) if is_red(col[y])]
if reds:
    print(f"render left-panel right border x=635: frame-y [{reds[0]/S:.1f},{reds[-1]/S:.1f}]")
# does title red ink overlap those lines? check red ink presence at y=48 line region x 150-800
band = ren[int(46 * S):int(52 * S), int(100 * S):int(900 * S)]
print("render red ink count in y[46,52] band:", sum(1 for p in band.reshape(-1, 3) if is_red(p)))

print("\n=== 2. ROC panel: fill, gridlines, axis labels, markers ===")
# original plot interior samples (avoid gridlines/axes): sample a grid of points x[645,895] y[85,350]
from collections import Counter
cnt = Counter()
for x in range(645, 895, 6):
    for y in range(85, 350, 6):
        cnt[classify(orig[y, x])] += 1
print("orig plot interior classes:", cnt.most_common(6))
cnt = Counter()
for x in range(int(645 * S), int(895 * S), 12):
    for y in range(int(85 * S), int(350 * S), 12):
        cnt[classify(ren[y, x])] += 1
print("render plot interior classes:", cnt.most_common(6))
# gridline colors in original: find light-blue-ish rows/cols inside plot
def line_colors(img, scale):
    res = []
    for y in range(int(85 * scale), int(350 * scale)):
        row = img[y, int(665 * scale):int(890 * scale)]
        nonwhite = sum(1 for p in row if not (p[0] > 240 and p[1] > 240 and p[2] > 240))
        if nonwhite > 100:
            res.append((y / scale, nonwhite, tuple(np.median(row, axis=0).astype(int))))
    return res
print("orig horizontal gridlines (y, count, median rgb):", line_colors(orig, 1)[:12])
print("render horizontal gridlines:", line_colors(ren, S)[:12])
# axis label colors: TPR vertical label left of y-axis ~x[645,662] y[150,320]; FPR ~y[352,378] x[750,820]
for name, (x0, y0, x1, y1) in {"TPR label": (643, 150, 663, 330), "FPR label": (745, 352, 825, 380)}.items():
    sub = orig[y0:y1, x0:x1]
    cnt = Counter(classify(p) for p in sub.reshape(-1, 3))
    print(f"orig {name} classes:", cnt.most_common(4))
    bb = ink_bbox(orig, x0, y0, x1, y1, any_ink)
    print(f"  orig {name} ink bbox:", bb)
# marker centers: red ring pixels in plot interior x[665,895] y[85,350], cluster them
sub = orig[85:350, 665:895]
mask = np.zeros(sub.shape[:2], bool)
for i in range(sub.shape[0]):
    for j in range(sub.shape[1]):
        if is_red(sub[i, j]):
            mask[i, j] = True
# remove axis lines: y-axis at x~661 (outside), x-axis at y~351 (outside) - ok
ys, xs = np.where(mask)
pts = list(zip(xs + 665, ys + 85))
# simple clustering
clusters = []
for (x, y) in pts:
    for c in clusters:
        if abs(c[0] - x) < 25 and abs(c[1] - y) < 25:
            c[0] = (c[0] * c[2] + x) / (c[2] + 1); c[1] = (c[1] * c[2] + y) / (c[2] + 1); c[2] += 1
            break
    else:
        clusters.append([x, y, 1])
big = [c for c in clusters if c[2] > 15]
print("orig red clusters in plot (centers, n):", [(round(c[0], 1), round(c[1], 1), c[2]) for c in big])
# same for render
sub = ren[int(85 * S):int(350 * S), int(665 * S):int(895 * S)]
mask = np.zeros(sub.shape[:2], bool)
for i in range(sub.shape[0]):
    for j in range(sub.shape[1]):
        if is_red(sub[i, j]):
            mask[i, j] = True
ys, xs = np.where(mask)
pts = list(zip(xs / S + 665, ys / S + 85))
clusters = []
for (x, y) in pts:
    for c in clusters:
        if abs(c[0] - x) < 25 and abs(c[1] - y) < 25:
            c[0] = (c[0] * c[2] + x) / (c[2] + 1); c[1] = (c[1] * c[2] + y) / (c[2] + 1); c[2] += 1
            break
    else:
        clusters.append([x, y, 1])
big = [c for c in clusters if c[2] > 30]
print("render red clusters in plot (frame-px centers, n):", [(round(c[0], 1), round(c[1], 1), c[2]) for c in big])
# label chips (cream) in original plot
bb = ink_bbox(orig, 665, 85, 895, 350, is_cream)
print("orig cream bbox in plot:", bb)
sub = orig[85:350, 665:895]
mask = np.zeros(sub.shape[:2], bool)
for i in range(sub.shape[0]):
    for j in range(sub.shape[1]):
        if is_cream(sub[i, j]):
            mask[i, j] = True
ys, xs = np.where(mask)
if len(xs):
    # cluster cream into chips
    pts = list(zip(xs + 665, ys + 85))
    clusters = []
    for (x, y) in pts:
        for c in clusters:
            if abs(c[0] - x) < 30 and abs(c[1] - y) < 20:
                c[0] = (c[0] * c[2] + x) / (c[2] + 1); c[1] = (c[1] * c[2] + y) / (c[2] + 1); c[2] += 1
                break
        else:
            clusters.append([x, y, 1])
    print("orig cream chip clusters (cx,cy,n):", [(round(c[0]), round(c[1]), c[2]) for c in clusters if c[2] > 40])

print("\n=== 3. Caption box x[354,621] y[426,474]: border + text color ===")
for name, img, sc in [("orig", orig, 1), ("render", ren, S)]:
    X0, Y0, X1, Y1 = int(354 * sc), int(426 * sc), int(621 * sc), int(474 * sc)
    sub = img[Y0:Y1, X0:X1]
    # border: sample top edge row
    top = sub[0:3, :]
    bot = sub[-3:, :]
    left = sub[:, 0:3]
    right = sub[:, -3:]
    med = lambda a: tuple(np.median(a.reshape(-1, 3), axis=0).astype(int))
    # text ink: darkest & red pixels inside (exclude 6px border margin)
    inner = sub[6:-6, 6:-6]
    darkp = [p for p in inner.reshape(-1, 3) if is_dark(p)]
    redp = [p for p in inner.reshape(-1, 3) if is_red(p)]
    print(f"{name}: border top{med(top)} bot{med(bot)} left{med(left)} right{med(right)}; "
          f"inner dark n={len(darkp)} med={tuple(np.median(darkp, axis=0).astype(int)) if darkp else None}; "
          f"inner red n={len(redp)} med={tuple(np.median(redp, axis=0).astype(int)) if redp else None}")

print("\n=== 4. Bottom-right matrix x[771,886] y[438,499]: Actual label vs P/N ===")
for name, img, sc in [("orig", orig, 1), ("render", ren, S)]:
    X0, Y0, X1, Y1 = int(771 * sc), int(438 * sc), int(886 * sc), int(499 * sc)
    sub = img[Y0:Y1, X0:X1]
    # red ink (rotated Actual) bbox in left strip x[771,800]
    lx0, lx1 = int(771 * sc), int(800 * sc)
    lsub = img[Y0:Y1, lx0:lx1]
    mask = np.array([[is_red(p) for p in row] for row in lsub])
    if mask.any():
        ys, xs = np.where(mask)
        print(f"{name}: red 'Actual' ink bbox frame-px x[{ (lx0+xs.min())/sc:.1f},{(lx0+xs.max())/sc:.1f}] y[{(Y0+ys.min())/sc:.1f},{(Y0+ys.max())/sc:.1f}] n={mask.sum()}")
    else:
        print(f"{name}: no red ink in x[771,800]")
    # dark ink (P/N row labels) in x[800,815] strip
    px0, px1 = int(800 * sc), int(816 * sc)
    psub = img[Y0:Y1, px0:px1]
    mask = np.array([[any_ink(p) for p in row] for row in psub])
    if mask.any():
        ys, xs = np.where(mask)
        print(f"{name}: P/N-label ink bbox x[{(px0+xs.min())/sc:.1f},{(px0+xs.max())/sc:.1f}] y[{(Y0+ys.min())/sc:.1f},{(Y0+ys.max())/sc:.1f}]")

print("\n=== 5. Threshold label glyph: '=' vs '-' (row1 box x[61,160] y[50,78]) ===")
for name, img, sc in [("orig", orig, 1), ("render", ren, S)]:
    X0, Y0, X1, Y1 = int(61 * sc), int(50 * sc), int(160 * sc), int(78 * sc)
    sub = img[Y0:Y1, X0:X1]
    mask = np.array([[any_ink(p) and not is_cream(p) for p in row] for row in sub])
    # find the text row band, then count distinct horizontal ink rows in the right half (where = is)
    if mask.any():
        rows = mask.sum(axis=1)
        inkrows = [i for i, v in enumerate(rows) if v > 0]
        print(f"{name}: ink rows (frame-y rel): {[(Y0+i)/sc - 50 for i in inkrows]}")
        # column profile of ink to locate the = sign (right portion x rel 70-99)
        right = mask[:, int(70 * sc):int(99 * sc)]
        rrows = right.sum(axis=1)
        segs = []
        cur = None
        for i, v in enumerate(rrows):
            if v > 0 and cur is None:
                cur = i
            elif v == 0 and cur is not None:
                segs.append((cur, i - 1)); cur = None
        if cur is not None:
            segs.append((cur, len(rrows) - 1))
        print(f"{name}: right-half ink row segments (rel y): {[(round((Y0+a)/sc-50,1), round((Y0+b)/sc-50,1)) for a, b in segs]}")
