#!/usr/bin/env python3
"""Probe 8i: mechanical extraction - vertical strokes, horizontal runs, components."""
from PIL import Image
import numpy as np
from scipy import ndimage

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)
REND = np.asarray(Image.open("recreated_pptx/qa/slide004/render_8.png").convert("RGB")).astype(int)
S = REND.shape[0] / 540.0

def masks(a, sc):
    dk = (a.max(axis=2) < 200)
    red = (a[:,:,0] > 140) & (a[:,:,1] < 120) & (a[:,:,2] < 120)
    blu = (a[:,:,2] > 120) & (a[:,:,0] < 110) & (a[:,:,1] < 120)
    return dk, red, blu

def vstrokes(dk, red, blu, sc, x0, y0, x1, y1, min_h=25):
    """columns with a contiguous ink run >= min_h frame-px; report per stroke."""
    out = []
    for xi in range(int(x0*sc), int(x1*sc)):
        col = (dk[:, xi] | red[:, xi] | blu[:, xi])
        col[:int(y0*sc)] = False; col[int(y1*sc):] = False
        # longest run
        best, cur, bs = 0, 0, 0
        for i, v in enumerate(col):
            if v: cur += 1
            else:
                if cur > best: best, bs = cur, i - cur
                cur = 0
        if cur > best: best, bs = cur, len(col) - cur
        if best >= min_h * sc:
            # color of the run
            seg_r = red[bs:bs+best, xi].sum(); seg_b = blu[bs:bs+best, xi].sum(); seg_d = dk[bs:bs+best, xi].sum()
            tot = seg_r + seg_b + seg_d
            c = "R" if seg_r > 0.5*tot else ("B" if seg_b > 0.35*tot else "D")
            out.append((round(xi/sc, 1), round(bs/sc, 1), round((bs+best)/sc, 1), round(best/sc, 1), c, int(seg_r), int(seg_b), int(seg_d)))
    # merge adjacent columns of same class
    merged = []
    for s in out:
        if merged and s[0] - merged[-1][0] <= 2.5 and s[4] == merged[-1][4] and abs(s[1]-merged[-1][1]) < 6:
            m = list(merged[-1]); m[1] = min(m[1], s[1]); m[2] = max(m[2], s[2]); merged[-1] = tuple(m)
        else:
            merged.append(s)
    return merged

def components(dk, red, blu, sc, x0, y0, x1, y1, min_px=40):
    lab, n = ndimage.label(dk | red | blu)
    out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(xs) < min_px * sc * sc / 4: continue
        mx, my = int(np.median(xs)), int(np.median(ys))
        sub = lambda m: m[ys, xs].sum()
        r, b, d = sub(red), sub(blu), sub(dk)
        tot = r + b + d
        c = "R" if r > 0.5*tot else ("B" if b > 0.35*tot else "D")
        out.append((round(xs.min()/sc,1), round(ys.min()/sc,1), round(xs.max()/sc,1), round(ys.max()/sc,1), c, int(tot)))
    return sorted(out, key=lambda t: (t[1], t[0]))

print("=== ORIG left box vertical strokes (x80..392 y100..218, h>=25) ===")
dk, red, blu = masks(ORIG, 1.0)
for s in vstrokes(dk, red, blu, 1.0, 80, 100, 392, 218):
    print(f"  x={s[0]} y{s[1]}..{s[2]} h={s[3]} color={s[4]} (r{s[5]} b{s[6]} d{s[7]})")
print("=== ORIG right box vertical strokes (x430..745) ===")
for s in vstrokes(dk, red, blu, 1.0, 430, 100, 745, 218):
    print(f"  x={s[0]} y{s[1]}..{s[2]} h={s[3]} color={s[4]} (r{s[5]} b{s[6]} d{s[7]})")
print("=== REND left box vertical strokes ===")
dk2, red2, blu2 = masks(REND, S)
for s in vstrokes(dk2, red2, blu2, S, 80, 100, 392, 218):
    print(f"  x={s[0]} y{s[1]}..{s[2]} h={s[3]} color={s[4]} (r{s[5]} b{s[6]} d{s[7]})")
print("=== REND right box vertical strokes ===")
for s in vstrokes(dk2, red2, blu2, S, 430, 100, 745, 218):
    print(f"  x={s[0]} y{s[1]}..{s[2]} h={s[3]} color={s[4]} (r{s[5]} b{s[6]} d{s[7]})")

print("\n=== ORIG left box components (min 40px, y100..218) ===")
for c in components(dk, red, blu, 1.0, 82, 100, 390, 218):
    print(f"  x{c[0]}..{c[2]} y{c[1]}..{c[3]} color={c[4]} ink={c[5]}")
print("=== REND left box components ===")
for c in components(dk2, red2, blu2, S, 82, 100, 390, 218):
    print(f"  x{c[0]}..{c[2]} y{c[1]}..{c[3]} color={c[4]} ink={c[5]}")

print("\n=== W glyph color, L1: ORIG x555..581 y250..273 (excl underline y274+) ===")
reg = ORIG[250:273, 555:581]
r = ((reg[:,:,0] > 140) & (reg[:,:,1] < 120) & (reg[:,:,2] < 120)).sum()
b = ((reg[:,:,2] > 120) & (reg[:,:,0] < 110)).sum()
d = ((reg.max(axis=2) < 200)).sum()
print(f"  red={r} blue={b} dark={d}")
print("=== X glyph color, L1: ORIG x539..559 y250..273 ===")
reg = ORIG[250:273, 539:559]
r = ((reg[:,:,0] > 140) & (reg[:,:,1] < 120) & (reg[:,:,2] < 120)).sum()
b = ((reg[:,:,2] > 120) & (reg[:,:,0] < 110)).sum()
print(f"  red={r} blue={b}")
print("=== REND W glyph x553..577 y248..272 ===")
reg = REND[int(248*S):int(272*S), int(553*S):int(577*S)]
r = ((reg[:,:,0] > 140) & (reg[:,:,1] < 120) & (reg[:,:,2] < 120)).sum()
b = ((reg[:,:,2] > 120) & (reg[:,:,0] < 110)).sum()
print(f"  red={r} blue={b}")
print("=== ORIG L1 y-hat underline + W underline rows (y266..280, x495..600) ===")
for y in range(266, 281):
    row_dk = dk[y, 495:600]; row_red = red[y, 495:600]
    druns = np.where(row_dk)[0]; rruns = np.where(row_red)[0]
    if len(druns) or len(rruns):
        print(f"  y{y}: dark {list(druns[:3])+['...']+[druns[-1]] if len(druns) else []} n={len(druns)} | red n={len(rruns)} {list(rruns[:3])+['...']+[rruns[-1]] if len(rruns) else []}")
