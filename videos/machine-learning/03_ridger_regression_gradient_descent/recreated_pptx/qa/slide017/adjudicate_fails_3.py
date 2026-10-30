#!/usr/bin/env python3
"""Fine adjudication part 3: title-tail column profiles, bottom-border colour
classes, per-band W-box element extents (render vs original)."""
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

# ── 1. TITLE tail profiles x740..900 (bin 2 frame px) ────────────────────────
print("== 1. TITLE tail column profiles (bin 2 frame px; letters = any/red/blue) ==")
for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
    sub_any = r_sl(m["red"] | m["blue"] | m["dark"], 58, 100, 740, 900) if ren else o_sl(m["red"] | m["blue"] | m["dark"], 58, 100, 740, 900)
    sub_r = r_sl(m["red"], 58, 100, 740, 900) if ren else o_sl(m["red"], 58, 100, 740, 900)
    sub_b = r_sl(m["blue"], 58, 100, 740, 900) if ren else o_sl(m["blue"], 58, 100, 740, 900)
    da, dr, db = sub_any.sum(axis=0), sub_r.sum(axis=0), sub_b.sum(axis=0)
    bins = []
    for i in range(0, len(da), int(2 * S) if ren else 2):
        a = int(da[i:i + (int(2 * S) if ren else 2)].sum())
        rr = int(dr[i:i + (int(2 * S) if ren else 2)].sum())
        bb = int(db[i:i + (int(2 * S) if ren else 2)].sum())
        x = 740 + (i / S if ren else i)
        bins.append(f"{x:.0f}:{a}/{rr}/{bb}")
    print(f" {nm}: " + " ".join(bins))

# ── 2. bottom border colour classes ──────────────────────────────────────────
print("\n== 2. bottom-border colour-class probe ==")
def classify(img, y0, y1, x0, x1, ren):
    if ren:
        seg = img[int(y0 * S):int(y1 * S) + 1, int(x0 * S):int(x1 * S) + 1]
    else:
        seg = img[int(y0):int(y1) + 1, int(x0):int(x1) + 1]
    px = seg.reshape(-1, 3)
    r, g, b = px[:, 0], px[:, 1], px[:, 2]
    rose = (abs(r - 215) < 30) & (abs(g - 190) < 30) & (abs(b - 194) < 32) & ((r - g) > 8) & ((b - g) > 4)
    gray = (abs(r - 206) < 15) & (abs(g - 208) < 15) & (abs(b - 205) < 15)
    mint = (g > 200) & (b < 245) & (g - r > 15)
    panel = (abs(r - 232) < 10) & (abs(g - 232) < 10) & (abs(b - 230) < 10)
    white = px.sum(axis=1) > 735
    other = ~(rose | gray | mint | panel | white)
    return dict(rose=int(rose.sum()), gray=int(gray.sum()), mint=int(mint.sum()),
                panel=int(panel.sum()), white=int(white.sum()), other=int(other.sum()))
print(" TEST bottoms (expect rose line in both):")
for bi, yb in enumerate([251, 389, 527], 1):
    o = classify(oi, yb - 1, yb + 1, 670, 870, False)
    r = classify(ri, yb - 1, yb + 1, 670, 870, True)
    print(f"  T-B{bi} y{yb} orig {o}")
    print(f"  T-B{bi} y{yb} rend {r}")
print(" TRAIN bottoms (reference, expect gray line in both):")
for bi, yb in enumerate([249, 389, 526], 1):
    o = classify(oi, yb - 1, yb + 1, 94, 457, False)
    r = classify(ri, yb - 1, yb + 1, 94, 457, True)
    print(f"  R-B{bi} y{yb} orig {o}")
    print(f"  R-B{bi} y{yb} rend {r}")
print(" TEST interior h-line (reference y221 B1):")
o = classify(oi, 220, 222, 670, 870, False); r = classify(ri, 220, 222, 670, 870, True)
print(f"  orig {o}"); print(f"  rend {r}")

# ── 3. per-band W-box element extents ────────────────────────────────────────
print("\n== 3. W-box per-band element extents (frame px) ==")
WB = [(127, 251), (265, 389), (403, 527)]
def ext(m, ren, y0, y1, x0, x1):
    sub = r_sl(m, y0, y1, x0, x1) if ren else o_sl(m, y0, y1, x0, x1)
    ys, xs = np.where(sub)
    if not len(xs): return None
    return (round(x0 + (xs.min() / S if ren else xs.min()), 1),
            round(x0 + (xs.max() / S if ren else xs.max()), 1),
            int(len(xs)))
for bi, (ya, yb) in enumerate(WB, 1):
    print(f" band {bi}:")
    for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
        w = ext(m["red"], ren, ya + 4, ya + 60, 505, 560)
        lp = ext(m["dark"], ren, ya + 15, yb - 15, 545, 566)
        rp = ext(m["dark"], ren, ya + 15, yb - 15, 600, 621)
        dg = ext(m["dark"], ren, ya + 4, yb - 4, 566, 600)
        nl = ext(m["blue"], ren, yb - 40, yb - 4, 505, 624)
        print(f"   {nm}: W(red) {w}  Lparen {lp}  Rparen {rp}  digits {dg}  norm(blue) {nl}")
