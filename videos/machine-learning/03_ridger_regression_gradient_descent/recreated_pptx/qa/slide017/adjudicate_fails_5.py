#!/usr/bin/env python3
"""Adjudication part 5: title tail glyphs (label-box excluded), W-box paren tips /
norm / digits per band, test-gridline colour per row, render bottom-line probe."""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
ri = np.asarray(Image.open(os.path.join(HERE, "render_2.png")).convert("RGB")).astype(int)
oi = np.asarray(Image.open(os.path.join(ROOT, "unique_slides", "slide_017.jpg")).convert("RGB")).astype(int)
S = ri.shape[0] / 540.0

def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    gray = (abs(r - 233) < 22) & (abs(g - 233) < 22) & (abs(b - 231) < 24)
    white = a.sum(axis=2) > 735
    bg = gray | white
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10) & ~bg
    blue = (b > 90) & ((b - r) > 40) & ((g - r) < 30) & ~bg
    dark = (a.sum(axis=2) < 330) & ~bg
    mint = (g > 200) & (b < 245) & (g - r > 15)
    rose = (abs(r - 215) < 35) & (abs(g - 190) < 35) & (abs(b - 194) < 37) & ((r - g) > 15)
    grayline = (abs(r - 206) < 14) & (abs(g - 208) < 14) & (abs(b - 205) < 14)
    return dict(red=red, blue=blue, dark=dark, white=white, mint=mint, rose=rose, grayline=grayline)
mo, mr = masks(oi), masks(ri)

def o_sl(m, y0, y1, x0, x1): return m[max(0, y0):y1 + 1, max(0, x0):x1 + 1]
def r_sl(m, y0, y1, x0, x1): return m[max(0, int(y0 * S)):int(y1 * S) + 1, max(0, int(x0 * S)):int(x1 * S) + 1]
def bbox(m, ren, y0, y1, x0, x1):
    sub = r_sl(m, y0, y1, x0, x1) if ren else o_sl(m, y0, y1, x0, x1)
    ys, xs = np.where(sub)
    if not len(xs): return None
    if ren:
        return (round(x0 + xs.min() / S, 1), round(x0 + xs.max() / S, 1), round(y0 + ys.min() / S, 1), round(y0 + ys.max() / S, 1), int(len(xs)))
    return (int(x0 + xs.min()), int(x0 + xs.max()), int(y0 + ys.min()), int(y0 + ys.max()), int(len(xs)))

print("== 1. TITLE tail glyphs, y58..95 (label box excluded) ==")
for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
    for label, key, x0, x1 in (("lambda", "blue", 730, 770), ("'='zone", "red", 750, 800), ("'3'", "blue", 780, 850)):
        print(f"  {nm} {label:8s}: {bbox(m[key], ren, 58, 95, x0, x1)}")
    # full tail ink bbox in the band above the label box
    print(f"  {nm} tail any  : {bbox(m['red'] | m['blue'], ren, 58, 95, 730, 850)}")

print("\n== 2. W-box paren tips per band (row-extent separated) ==")
WB = [(127, 251), (265, 389), (403, 527)]
for bi, (ya, yb) in enumerate(WB, 1):
    for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
        y0, y1 = ya + 15, yb - 15
        h = y1 - y0
        # left zone: exclude '=' bars (x<557) -> restrict x557..575
        sub_l = r_sl(m["dark"], y0, y1, 557, 575) if ren else o_sl(m["dark"], y0, y1, 557, 575)
        cl = sub_l.sum(axis=0)
        lt = [(557 + (i / S if ren else i), int(v)) for i, v in enumerate(cl) if v > 0]
        # right zone: x598..618
        sub_r = r_sl(m["dark"], y0, y1, 598, 618) if ren else o_sl(m["dark"], y0, y1, 598, 618)
        cr = sub_r.sum(axis=0)
        rt = [(598 + (i / S if ren else i), int(v)) for i, v in enumerate(cr) if v > 0]
        lstrong = [c for c in lt if c[1] > h * 0.3]
        rstrong = [c for c in rt if c[1] > h * 0.3]
        print(f"  B{bi} {nm}: L-tip {lt[0][0]:.1f}..{lt[-1][0]:.1f} (strong {lstrong[0][0] if lstrong else None}..{lstrong[-1][0] if lstrong else None})"
              f"  R-tip {rt[0][0]:.1f}..{rt[-1][0]:.1f} (strong {rstrong[0][0] if rstrong else None}..{rstrong[-1][0] if rstrong else None})")

print("\n== 3. W-box norm line (blue) + digit stack per band ==")
for bi, (ya, yb) in enumerate(WB, 1):
    for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
        nl = bbox(m["blue"], ren, yb - 42, yb - 4, 505, 624)
        dg = bbox(m["dark"], ren, ya + 30, yb - 45, 560, 602)
        print(f"  B{bi} {nm}: norm {nl}  digits {dg}")

print("\n== 4. TEST gridline colour per row (B1) — rose vs gray line px ==")
for y in (128, 160, 190, 221, 251):
    for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
        rose = int((r_sl(m["rose"], y - 1, y + 1, 672, 868) if ren else o_sl(m["rose"], y - 1, y + 1, 672, 868)).sum())
        gl = int((r_sl(m["grayline"], y - 1, y + 1, 672, 868) if ren else o_sl(m["grayline"], y - 1, y + 1, 672, 868)).sum())
        print(f"  y{y} {nm}: rose={rose} gray={gl}")

print("\n== 5. render test-bottom line probe: per-row class counts y246..258 (B1) ==")
for y in range(246, 259):
    rose = int(r_sl(mr["rose"], y, y, 672, 868).sum())
    gl = int(r_sl(mr["grayline"], y, y, 672, 868).sum())
    mint = int(r_sl(mr["mint"], y, y, 672, 868).sum())
    nw = int((~r_sl(mr["white"], y, y, 672, 868)).sum())
    print(f"  y{y}: rose={rose} gray={gl} mint={mint} nonwhite={nw}")
print("  ORIG same probe:")
for y in range(246, 259):
    rose = int(o_sl(mo["rose"], y, y, 672, 868).sum())
    gl = int(o_sl(mo["grayline"], y, y, 672, 868).sum())
    mint = int(o_sl(mo["mint"], y, y, 672, 868).sum())
    nw = int((~o_sl(mo["white"], y, y, 672, 868)).sum())
    print(f"  y{y}: rose={rose} gray={gl} mint={mint} nonwhite={nw}")
