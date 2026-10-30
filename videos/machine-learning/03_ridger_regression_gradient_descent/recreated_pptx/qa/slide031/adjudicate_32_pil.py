#!/usr/bin/env python3
# Adjudicate judge_attempt_32's five findings, PIL-first (deck law).
# ORIG = unique_slides/slide_031.jpg (960x540, 1px=1pt)
# RENDER = qa/slide031/render_32.png (2001x1125, scale 2001/960)
from PIL import Image
import numpy as np

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_031.jpg"
REND = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide031/render_32.png"

oi = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
ri = np.asarray(Image.open(REND).convert("RGB")).astype(int)
S = ri.shape[1] / 960.0
print(f"orig {oi.shape} render {ri.shape} scale {S:.5f}")

def clusters(cols, gap=3, min_ink=2):
    """group ink column indices into clusters separated by >gap"""
    out = []
    cur = None
    for c in cols:
        if cur and c - cur[-1] <= gap:
            cur.append(c)
        else:
            if cur and len(cur) >= min_ink:
                out.append(cur)
            cur = [c]
    if cur and len(cur) >= min_ink:
        out.append(cur)
    return out

def blue_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (b > 120) & (b - r > 25) & (b - g > 20)

def gray_dark_mask(a, thr=150):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    return (mx < thr) & (mx - mn < 40)

print("\n=== FINDING 1+3: bounce arrows ===")
# orig region x390..545 y300..360; render scaled
for tag, img, (x0, x1, y0, y1) in [
    ("ORIG", oi, (390, 545, 300, 360)),
    ("REND", ri, (int(390 * S), int(545 * S), int(300 * S), int(360 * S))),
]:
    reg = img[y0:y1, x0:x1]
    bm = blue_mask(reg)
    colink = bm.sum(axis=0)
    cols = np.where(colink > 0)[0]
    cls = clusters(list(cols), gap=4, min_ink=2)
    print(f"\n{tag} region x{x0}..{x1} y{y0}..{y1}: blue px={bm.sum()}, col-clusters={len(cls)}")
    for cl in cls:
        c0, c1 = cl[0], cl[-1]
        sub = bm[:, c0:c1 + 1]
        rows = np.where(sub.sum(axis=1) > 0)[0]
        # interior sample: center of bbox
        cy = (rows[0] + rows[-1]) // 2
        cx = (c0 + c1) // 2
        # interior = pixels inside bbox that are NOT blue-ink
        inner = reg[rows[0]:rows[-1] + 1, c0:c1 + 1]
        innerm = bm[rows[0]:rows[-1] + 1, c0:c1 + 1]
        n_inner = innerm.size - innerm.sum()
        # modal non-blue interior colour
        px = inner[~innerm]
        if len(px):
            modal = {}
            for p in px[:: max(1, len(px) // 400)]:
                modal[tuple(p)] = modal.get(tuple(p), 0) + 1
            top = sorted(modal.items(), key=lambda kv: -kv[1])[:3]
        else:
            top = []
        print(f"  blob x{x0+c0}..{x0+c1} (w{c1-c0+1}) y{y0+rows[0]}..{y0+rows[-1]} (h{rows[-1]-rows[0]+1}) "
              f"ink={int(sub.sum())} nonblue_inner={n_inner} modal_inner={top}")

print("\n=== FINDING 2: x-row column count ===")
# olive band: orig y344..364 (x row), text ink y~346..362; label col ends x131
for tag, img, sc in [("ORIG", oi, 1.0), ("REND", ri, S)]:
    y0, y1 = int(346 * sc), int(363 * sc)
    x0, x1 = int(131 * sc), int(884 * sc)
    reg = img[y0:y1, x0:x1]
    dm = gray_dark_mask(reg, thr=140)
    colink = dm.sum(axis=0)
    cols = np.where(colink >= 1)[0]
    cls = clusters(list(cols), gap=6, min_ink=1)
    centers = [x0 / sc + (c[0] + c[-1]) / 2 / sc for c in cls]
    print(f"{tag}: {len(cls)} text clusters in x-row")
    print("  centers(frame px):", [f"{c:.1f}" for c in centers])
    if len(cls) > 2:
        d = [centers[i + 1] - centers[i] for i in range(len(centers) - 1)]
        print("  gaps:", [f"{g:.1f}" for g in d])
    # f(x) row too (y364..381 band, text ~y366..380)
    y0b, y1b = int(366 * sc), int(381 * sc)
    regb = img[y0b:y1b, x0:x1]
    dmb = gray_dark_mask(regb, thr=140)
    colsb = np.where(dmb.sum(axis=0) >= 1)[0]
    clsb = clusters(list(colsb), gap=6, min_ink=1)
    print(f"{tag}: {len(clsb)} text clusters in f(x)-row")

print("\n=== FINDING 2b: terminal-cell identity (orig) ===")
# orig x-row cells: pitch 41.67 from x131. Compare last cell ink vs earlier cells.
pitch = 41.67
y0, y1 = 346, 363
cells = {}
for c in range(18):
    cx0 = int(131 + c * pitch)
    cell = oi[y0:y1, cx0:cx0 + int(pitch)]
    m = gray_dark_mask(cell, thr=140)
    cells[c] = m
# find first cell whose ink pattern equals the last (allow 1px shift)
last = cells[17]
def sim(a, b):
    if a.sum() == 0 or b.sum() == 0:
        return -1
    inter = (a & b).sum()
    return inter / max(a.sum(), b.sum())
print("orig last-cell (c17) ink px:", int(last.sum()))
best = []
for c in range(17):
    for dy in (-1, 0, 1):
        shifted = np.roll(cells[c], dy, axis=1)
        best.append((sim(last, shifted), c, dy))
best.sort(reverse=True)
print("best matches for last cell (score, col, dy):", [(f"{s:.2f}", c, dy) for s, c, dy in best[:5]])
# also check c16 vs c6 (4.8) and c7 (5.1)
print("sim(c16, c6):", f"{sim(cells[16], cells[6]):.2f}", " sim(c16, c7):", f"{sim(cells[16], cells[7]):.2f}")
print("sim(c17, c6):", f"{sim(cells[17], cells[6]):.2f}", " sim(c17, c7):", f"{sim(cells[17], cells[7]):.2f}")

print("\n=== FINDING 4: '(?, ?)' label vs curve ===")
for tag, img, sc in [("ORIG", oi, 1.0), ("REND", ri, S)]:
    x0, x1 = int(705 * sc), int(795 * sc)
    y0, y1 = int(125 * sc), int(165 * sc)
    reg = img[y0:y1, x0:x1]
    dm = gray_dark_mask(reg, thr=160)
    colink = dm.sum(axis=0)
    cols = np.where(colink >= 1)[0]
    cls = clusters(list(cols), gap=8, min_ink=2)
    print(f"{tag} region x{705}..{795} y{125}..{165}:")
    for cl in cls:
        rows = np.where(dm[:, cl[0]:cl[-1] + 1].sum(axis=1) > 0)[0]
        print(f"  dark-ink cluster x{705+cl[0]/sc:.1f}..{705+cl[-1]/sc:.1f} y{125+rows[0]/sc:.1f}..{125+rows[-1]/sc:.1f}")
    # curve stroke: steel-blue family (b>r, b>110, not too dark)
    r_, g_, b_ = reg[..., 0], reg[..., 1], reg[..., 2]
    cm = (b_ > 110) & (b_ - r_ > 15) & (b_ - g_ > 10) & (r_ < 200)
    colc = np.where(cm.sum(axis=0) >= 1)[0]
    clc = clusters(list(colc), gap=4, min_ink=1)
    for cl in clc:
        rows = np.where(cm[:, cl[0]:cl[-1] + 1].sum(axis=1) > 0)[0]
        print(f"  curve-stroke cols x{705+cl[0]/sc:.1f}..{705+cl[-1]/sc:.1f} y{125+rows[0]/sc:.1f}..{125+rows[-1]/sc:.1f} n={int(cm[:, cl[0]:cl[-1]+1].sum())}")

print("\n=== FINDING 5: slope-row green border thickness ===")
for tag, img, sc in [("ORIG", oi, 1.0), ("REND", ri, S)]:
    x = int(200 * sc)
    col = img[int(470 * sc):int(500 * sc), x]
    print(f"{tag} col x={x} y470..500:")
    for i, p in enumerate(col):
        y = 470 + i / sc
        r, g, b = p
        if g > r + 20 and g > b + 20:
            print(f"  y{y:.1f} green ({r},{g},{b})")

print("\n=== EXTRA: orig x-row terminal-value cross-check via f(x) row ===")
# f(x) row orig cells, pitch 41.67 from x131, y366..381
y0, y1 = 366, 381
fcells = {}
for c in range(18):
    cx0 = int(131 + c * pitch)
    fcells[c] = gray_dark_mask(oi[y0:y1, cx0:cx0 + int(pitch)], thr=140)
lastf = fcells[17]
print("orig f(x) last-cell ink px:", int(lastf.sum()))
bestf = []
for c in range(17):
    for dy in (-1, 0, 1):
        bestf.append((sim(lastf, np.roll(fcells[c], dy, axis=1)), c, dy))
bestf.sort(reverse=True)
print("best matches (score, col, dy):", [(f"{s:.2f}", c, dy) for s, c, dy in bestf[:5]])
