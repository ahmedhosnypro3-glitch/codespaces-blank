#!/usr/bin/env python3
"""Pass 3: full gridline map of orig plot + threshold '=' detection + TPR/FPR label bboxes."""
from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/"
orig = np.array(Image.open(NS + "unique_slides/slide_032.jpg").convert("RGB")).astype(int)
ren = np.array(Image.open(NS + "recreated_pptx/qa/slide032/render.png").convert("RGB")).astype(int)
S = ren.shape[1] / 960.0

def is_red(p):    return p[0] > 110 and p[0] > p[1] * 1.6 and p[0] > p[2] * 1.6 and p[1] < 130
def any_ink(p):   return not (p[0] > 235 and p[1] > 235 and p[2] > 235)
def is_cream(p):  return p[0] > 235 and p[1] > 225 and 185 < p[2] < 246

print("=== orig plot gridlines (full) ===")
# vertical lines: columns in x[665,893] where many pixels differ from white, excluding red/cream
sub = orig[85:350, 665:893]
for j in range(sub.shape[1]):
    col = sub[:, j]
    n = sum(1 for p in col if any_ink(p) and not is_red(p) and not is_cream(p))
    if n > 120:
        px = [p for p in col if any_ink(p) and not is_red(p) and not is_cream(p)]
        print(f"  vline x={665+j} n={n} med={np.median(px,0).astype(int)}")
for i in range(sub.shape[0]):
    row = sub[i]
    n = sum(1 for p in row if any_ink(p) and not is_red(p) and not is_cream(p))
    if n > 120:
        px = [p for p in row if any_ink(p) and not is_red(p) and not is_cream(p)]
        print(f"  hline y={85+i} n={n} med={np.median(px,0).astype(int)}")

print("\n=== orig TPR/FPR label bboxes (red ink only) ===")
sub = orig[100:350, 640:662]
mask = np.array([[is_red(p) for p in row] for row in sub])
ys, xs = np.where(mask)
# exclude the y-axis line itself: find axis column (the col with most red)
colcounts = mask.sum(axis=0)
axis_j = int(np.argmax(colcounts))
print(f"y-axis col in region: x={640+axis_j} count={colcounts[axis_j]}")
mask2 = mask.copy(); mask2[:, max(0,axis_j-1):axis_j+2] = False
ys, xs = np.where(mask2)
if len(xs): print(f"orig TPR label red bbox: x[{640+xs.min()},{640+xs.max()}] y[{100+ys.min()},{100+ys.max()}] n={len(xs)}")
sub = orig[353:385, 740:830]
mask = np.array([[is_red(p) for p in row] for row in sub])
ys, xs = np.where(mask)
colcounts = mask.sum(axis=0)
axis_i = None
rowcounts = mask.sum(axis=1)
# x-axis line at y~351 is outside (region starts 353); red here = FPR label + maybe chip edge
if len(xs): print(f"orig FPR-region red bbox: x[{740+xs.min()},{740+xs.max()}] y[{353+ys.min()},{353+ys.max()}] n={len(xs)}")

print("\n=== threshold '=' detection: row-segment count per column, row-1 label box ===")
def eq_check(img, sc, label):
    sub = img[int(53*sc):int(75*sc), int(63*sc):int(158*sc)]
    mask = np.array([[any_ink(p) for p in row] for row in sub])
    hits = []
    for j in range(mask.shape[1]):
        rows = mask[:, j]
        segs = []
        cur = None
        for i, v in enumerate(rows):
            if v and cur is None: cur = i
            elif not v and cur is not None: segs.append((cur, i-1)); cur = None
        if cur is not None: segs.append((cur, len(rows)-1))
        # '=' column: exactly 2 segments with a gap >= 2, both 1-3 px tall, in middle of text height
        if len(segs) == 2 and (segs[1][0]-segs[0][1]) >= 2 and all(1 <= b-a+1 <= 3 for a, b in segs):
            hits.append((63 + j/sc, segs))
    # group consecutive hit columns
    groups = []
    for h in hits:
        if groups and h[0] - groups[-1][-1][0] <= 1.5:
            groups[-1].append(h)
        else:
            groups.append([h])
    print(f"{label}: '='-like column groups (x, segs):", [(round(g[0][0],1), round(g[-1][0],1), g[0][1]) for g in groups])
eq_check(orig, 1, "orig")
eq_check(ren, S, "render")

print("\n=== orig slide bg color top band + house frame check ===")
print("orig px (400,25):", orig[25,400], " (100,30):", orig[30,100], " (480,20):", orig[20,480])
print("orig red frame rows y[5,15]:", [(y, sum(1 for p in orig[y,100:900] if is_red(p))) for y in range(5,16)])
print("render px (400,25)/S:", ren[int(25*S), int(400*S)])
