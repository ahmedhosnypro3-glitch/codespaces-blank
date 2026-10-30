#!/usr/bin/env python3
"""Adjudicate the crop_2_column_of_columns FAIL findings against BOTH images:
box border geometry/colors, delimiter stack geometry, ink color classes,
label-block placement, and row structure of the vector-definition boxes.
All numbers in frame px (960x540, 1px = 1pt) for the original; render px
(= frame x 2.0833) for the 150dpi render, scaled back to frame space.
"""
import numpy as np
from PIL import Image

NS = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/")
QA = NS + "recreated_pptx/qa/slide014/"

S = 150 / 72.0
og = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)
rd = np.asarray(Image.open(QA + "render_2.png").convert("RGB")).astype(int)
Hog, Hog_w = og.shape[:2]
Hr = rd.shape[0]
sc = Hr / 540.0
print(f"original {og.shape[1]}x{Hog}  render {rd.shape[1]}x{Hr}  scale {sc:.4f}")


def inb(img, x, y):
    return 0 <= x < img.shape[1] and 0 <= y < img.shape[0]


def px(img, x, y):
    return tuple(img[y, x]) if inb(img, x, y) else None


def classify(R, G, B):
    if R > 242 and G > 242 and B > 242:
        return "WHITE"
    if abs(R - 233) < 14 and abs(G - 233) < 14 and abs(B - 231) < 14:
        return "PANEL"
    if R > 150 and G < 115 and B < 115:
        return "RED"
    if B > 145 and R < 95 and G < 95:
        return "BLUE"
    if G > 115 and R < 155 and B < 155:
        return "GREEN"
    if R > 195 and G > 195 and 145 < B < 232:
        return "YELLOW"
    if R > 228 and G < 232 and B < 232 and not (R - G > 45):
        return "PINK"
    if B > 218 and R < 245 and G > 228:
        return "PALEBLUE"
    if R < 135 and G < 135 and B < 135:
        return "BLACK"
    return "other"


# ---------- 1. vector-box border rows: find rows where a long horizontal
#            run of non-panel ink exists in the box band ----------
print("\n=== 1. VECTOR-BOX BORDER BANDS (original) ===")
for y in range(92, 118):
    row = og[y]
    nonwhite = [x for x in range(60, 910)
                if not (row[x][0] > 242 and row[x][1] > 242 and row[x][2] > 242)
                and classify(*row[x]) != "PANEL"]
    if not nonwhite:
        continue
    # longest contiguous run
    best, cur = [], [nonwhite[0]]
    for x in nonwhite[1:]:
        if x - cur[-1] <= 1:
            cur.append(x)
        else:
            if len(cur) > len(best):
                best = cur
            cur = [x]
    if len(cur) > len(best):
        best = cur
    if len(best) > 40:
        print(f"  y={y:3d} longest run x {best[0]}..{best[-1]} len={len(best)} "
              f"color@mid={classify(*row[(best[0]+best[-1])//2])} "
              f"rgb@left={tuple(row[best[0]])}")

# ---------- 2. vertical strokes inside the box band (tall parens?) ----------
print("\n=== 2. VERTICAL STROKE COLUMNS in y 105..235 (original) ===")
for x in range(70, 460, 2):
    col = [y for y in range(103, 236) if classify(*og[y, x]) not in ("WHITE", "PANEL")]
    if len(col) > 60:
        cols = {}
        for y in col:
            cc = classify(*og[y, x])
            cols[cc] = cols.get(cc, 0) + 1
        print(f"  x={x:3d} ink rows={len(col):3d} y {min(col)}..{max(col)} classes={cols}")

print("\n=== 2b. same for right box (x 455..815) ===")
for x in range(455, 815, 2):
    col = [y for y in range(103, 236) if classify(*og[y, x]) not in ("WHITE", "PANEL")]
    if len(col) > 60:
        cols = {}
        for y in col:
            cc = classify(*og[y, x])
            cols[cc] = cols.get(cc, 0) + 1
        print(f"  x={x:3d} ink rows={len(col):3d} y {min(col)}..{max(col)} classes={cols}")

# ---------- 3. ink row-profile: how many text lines per box ----------
print("\n=== 3. TEXT-LINE BANDS (row ink counts, left box x 84..430, original) ===")
for y in range(103, 236, 2):
    cnt = sum(1 for x in range(84, 430)
              if classify(*og[y, x]) not in ("WHITE", "PANEL"))
    bar = "#" * min(cnt // 8, 40)
    if cnt:
        print(f"  y={y:3d} ink={cnt:3d} {bar}")

print("\n=== 3b. TEXT-LINE BANDS (right box x 460..806, original) ===")
for y in range(103, 236, 2):
    cnt = sum(1 for x in range(460, 806)
              if classify(*og[y, x]) not in ("WHITE", "PANEL"))
    bar = "#" * min(cnt // 8, 40)
    if cnt:
        print(f"  y={y:3d} ink={cnt:3d} {bar}")

# ---------- 4. color census of ink inside each box ----------
print("\n=== 4. INK COLOR CENSUS (original, inside box borders) ===")
for label, x0, x1 in (("LEFT", 84, 430), ("RIGHT", 460, 806)):
    cc = {}
    for y in range(103, 236):
        for x in range(x0, x1):
            c = classify(*og[y, x])
            if c not in ("WHITE", "PANEL"):
                cc[c] = cc.get(c, 0) + 1
    print(f"  {label} box: {cc}")

print("\n=== 4b. INK COLOR CENSUS (render_2, same frame-space boxes) ===")
for label, x0, x1 in (("LEFT", 84, 430), ("RIGHT", 460, 806)):
    cc = {}
    for y in range(103, 236):
        for x in range(int(x0 * sc), int(x1 * sc)):
            c = classify(*rd[y, x])
            if c not in ("WHITE", "PANEL"):
                cc[c] = cc.get(c, 0) + 1
    print(f"  {label} box: {cc}")

# ---------- 5. exact box border x-extents on both sides ----------
print("\n=== 5. BOX EDGE x-EXTENTS ===")
for y in (101,):
    row = og[y]
    runs = []
    start = None
    for x in range(60, 910):
        nw = classify(*row[x]) not in ("WHITE", "PANEL")
        if nw and start is None:
            start = x
        elif not nw and start is not None:
            if x - start > 25:
                runs.append((start, x - 1, classify(*row[(start + x - 1) // 2])))
            start = None
    print(f"  original y={y} runs>25px: {runs}")
# vertical extent: scan a column well inside each box for border color
for label, xc in (("LEFT box interior", 250), ("RIGHT box interior", 630)):
    ys = [y for y in range(90, 260) if classify(*og[y, xc]) in ("RED", "PINK", "YELLOW")]
    if ys:
        print(f"  {label} x={xc}: border-class rows {min(ys)}..{max(ys)}")
