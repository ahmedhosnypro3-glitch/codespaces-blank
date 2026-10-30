#!/usr/bin/env python3
"""Fine adjudication part 2: title sub-glyphs, test-gridline colour, W paren tips."""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
RENDER = os.path.join(HERE, "render_2.png")
ORIG = os.path.join(ROOT, "unique_slides", "slide_017.jpg")

ri = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
oi = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
S = ri.shape[0] / 540.0

def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    gray = (abs(r - 233) < 22) & (abs(g - 233) < 22) & (abs(b - 231) < 24)
    white = a.sum(axis=2) > 735
    bg = gray | white
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10) & ~bg
    blue = (b > 90) & ((b - r) > 40) & ((g - r) < 30) & ~bg
    dark = (a.sum(axis=2) < 330) & ~bg
    return dict(red=red, blue=blue, dark=dark, white=white)

mo, mr = masks(oi), masks(ri)
def o_sl(m, y0, y1, x0, x1): return m[max(0, y0):y1 + 1, max(0, x0):x1 + 1]
def r_sl(m, y0, y1, x0, x1): return m[max(0, int(y0 * S)):int(y1 * S) + 1, max(0, int(x0 * S)):int(x1 * S) + 1]
def runs(row):
    out, i, n = [], 0, len(row)
    while i < n:
        if row[i]:
            j = i
            while j + 1 < n and row[j + 1]: j += 1
            out.append((i, j)); i = j + 1
        else: i += 1
    return out
def merge(rs, gap):
    m = []
    for x0, x1 in rs:
        if m and x0 - m[-1][1] <= gap: m[-1][1] = x1
        else: m.append([x0, x1])
    return m

# ── A. TITLE sub-glyphs: per-glyph colour + x range, both images ─────────────
print("== A. TITLE sub-glyph map (y60..99) ==")
def glyphs(m, ren):
    sub = r_sl(m["red"] | m["blue"] | m["dark"], 60, 99, 400, 890) if ren else o_sl(m["red"] | m["blue"] | m["dark"], 60, 99, 400, 890)
    d = sub.sum(axis=0)
    rs = merge(runs(d > 0), 2 if not ren else 4)
    out = []
    for a, b in rs:
        x0 = 400 + (a / S if ren else a); x1 = 400 + (b / S if ren else b)
        rr = int((r_sl(m["red"], 60, 99, int(x0), int(x1)) if ren else o_sl(m["red"], 60, 99, int(x0), int(x1))).sum())
        bb = int((r_sl(m["blue"], 60, 99, int(x0), int(x1)) if ren else o_sl(m["blue"], 60, 99, int(x0), int(x1))).sum())
        dd = int((r_sl(m["dark"], 60, 99, int(x0), int(x1)) if ren else o_sl(m["dark"], 60, 99, int(x0), int(x1))).sum())
        col = "RED" if rr > bb and rr > dd else ("BLUE" if bb > rr and bb > dd else "DARK")
        out.append((round(x0, 1), round(x1, 1), col))
    return out
go = glyphs(mo, False)
gr = glyphs(mr, True)
print(" orig (x400..890):")
for g in go: print("   ", g)
print(" rend (x400..890):")
for g in gr: print("   ", g)

# ── B. TEST gridlines: row profile of the bottom line + colour of gridlines ──
print("\n== B. TEST table bottom line row profile ==")
for bi, yb in enumerate([251, 389, 527], 1):
    for nm, img, ren in (("orig", oi, False), ("rend", ri, True)):
        rows = []
        for y in range(yb - 4, yb + 5):
            if ren:
                seg = img[int(y * S):int(y * S) + 2, int(670 * S):int(870 * S)]
            else:
                seg = img[y:y + 1, 670:870]
            nw = (seg.sum(axis=2) <= 735)
            rows.append((y, int(nw.sum())))
        print(f"  B{bi} {nm}: " + " ".join(f"y{y}:{n}" for y, n in rows))
print("\n== B2. test interior vertical gridline colour (orig x~770, render scaled) ==")
for nm, img, ren in (("orig", oi, False), ("rend", ri, True)):
    # sample the border colour: non-white pixel medians inside a gridline column band
    y0, y1 = (129, 159) if not ren else (129, 159)
    if ren:
        seg = img[int(y0 * S):int(y1 * S), int(769 * S):int(771 * S)].reshape(-1, 3)
    else:
        seg = img[y0:y1, 769:771].reshape(-1, 3)
    nz = seg[seg.sum(axis=1) <= 735]
    print(f"  {nm} x770@B1: n={len(nz)} median={np.median(nz,axis=0).astype(int).tolist() if len(nz) else None}")

# ── C. W-box right-zone: per-column row extent (separate paren tip vs border) ─
print("\n== C. W-box right zone per-column ink row-extent ==")
WB = [(127, 251), (265, 389), (403, 527)]
for bi, (ya, yb) in enumerate(WB, 1):
    for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
        y0, y1 = ya + 8, yb - 8
        sub = r_sl(m["dark"], y0, y1, 596, 624) if ren else o_sl(m["dark"], y0, y1, 596, 624)
        colsum = sub.sum(axis=0)
        # split: border columns = those with ink over >60% of the row span
        h = sub.shape[0]
        strong = [(596 + (i / S if ren else i), int(v)) for i, v in enumerate(colsum) if v > h * 0.6]
        tips = [(596 + (i / S if ren else i), int(v)) for i, v in enumerate(colsum) if 0 < v <= h * 0.6]
        sfirst = strong[0][0] if strong else None
        slast = strong[-1][0] if strong else None
        tfirst = tips[0][0] if tips else None
        tlast = tips[-1][0] if tips else None
        print(f"  B{bi} {nm}: border-cols {sfirst}..{slast} (n={len(strong)})  tip-cols {tfirst}..{tlast} (n={len(tips)})")
        if tlast: print(f"      rightmost tip col x{tlast:.1f} count {tips[-1][1]}/{h}")
