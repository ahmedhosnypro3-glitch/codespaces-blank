#!/usr/bin/env python3
"""PIL adjudication of slide017 render_2 selfcheck FAILs against BOTH images.

Every FAIL is re-measured against the original frame (960x540, 1px=1pt) and the
fresh 150dpi render (2001x1125, scale 2001/960=2.0833 render-px per frame px).
Bank: recreated_pptx/qa/slide017/adjudicate_fails.py
"""
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
print(f"render {ri.shape[1]}x{ri.shape[0]}  scale {S:.6f}")

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

def o_sl(mask, y0, y1, x0, x1):
    return mask[max(0, y0):y1 + 1, max(0, x0):x1 + 1]
def r_sl(mask, y0, y1, x0, x1):
    return mask[max(0, int(y0 * S)):int(y1 * S) + 1, max(0, int(x0 * S)):int(x1 * S) + 1]

def runs(row, minlen=1):
    out, i, n = [], 0, len(row)
    while i < n:
        if row[i]:
            j = i
            while j + 1 < n and row[j + 1]:
                j += 1
            if j - i + 1 >= minlen:
                out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out
def merge(rs, gap):
    m = []
    for x0, x1 in rs:
        if m and x0 - m[-1][1] <= gap:
            m[-1][1] = x1
        else:
            m.append([x0, x1])
    return m

# ── 1. TITLE: per-glyph colour mapping in both images ────────────────────────
print("\n== 1. TITLE glyph groups (y60..99, x170..890) ==")
def glyph_groups(mask_, img_is_render, gap):
    sub = r_sl(mask_, 60, 99, 170, 890) if img_is_render else o_sl(mask_, 60, 99, 170, 890)
    d = sub.sum(axis=0)
    rs = merge(runs(d > 0, 1), gap)
    if img_is_render:
        return [(round(p[0] / S + 170, 1), round(p[1] / S + 170, 1)) for p in rs]
    return [(p[0] + 170, p[1] + 170) for p in rs]

def dom_colors(m, y0, y1, x0, x1, ren):
    sub = None
    out = {}
    for key in ("red", "blue", "dark"):
        mk = r_sl(m[key], y0, y1, x0, x1) if ren else o_sl(m[key], y0, y1, x0, x1)
        out[key] = int(mk.sum())
    tot = sum(out.values()) or 1
    return out, tot

gr_o = glyph_groups(mo["red"] | mo["blue"] | mo["dark"], False, 5)
gr_r = glyph_groups(mr["red"] | mr["blue"] | mr["dark"], True, 10)
print("orig groups (gap5): ", gr_o)
print("rend groups (gap10):", gr_r)
# per-group dominant colour
def group_colors(groups, m, ren):
    res = []
    for (a, b) in groups:
        c, tot = dom_colors(m, 60, 99, int(a) + 1, int(b) - 1, ren)
        dom = max(c, key=c.get)
        res.append((a, b, dom, c))
    return res
print("\nper-group dominant colour (ORIG):")
for a, b, dom, c in group_colors(gr_o, mo, False):
    print(f"  x{a}..{b}  {dom:5s}  r{c['red']} b{c['blue']} d{c['dark']}")
print("per-group dominant colour (RENDER):")
for a, b, dom, c in group_colors(gr_r, mr, True):
    print(f"  x{a}..{b}  {dom:5s}  r{c['red']} b{c['blue']} d{c['dark']}")

# specific: the "=" glyph region between lambda and 3
print("\n'=' region probe (lambda..3 gap):")
for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
    seg = r_sl(m["red"] | m["blue"] | m["dark"], 60, 99, 750, 800) if ren else o_sl(m["red"] | m["blue"] | m["dark"], 60, 99, 750, 800)
    ys, xs = np.where(seg)
    if len(xs):
        print(f"  {nm}: ink x{750 + (xs.min() / S if ren else xs.min()):.1f}..{750 + (xs.max() / S if ren else xs.max()):.1f}")
    rr = int((r_sl(m["red"], 60, 99, 750, 800) if ren else o_sl(m["red"], 60, 99, 750, 800)).sum())
    bb = int((r_sl(m["blue"], 60, 99, 750, 800) if ren else o_sl(m["blue"], 60, 99, 750, 800)).sum())
    dd = int((r_sl(m["dark"], 60, 99, 750, 800) if ren else o_sl(m["dark"], 60, 99, 750, 800)).sum())
    print(f"    red={rr} blue={bb} dark={dd}")

# ── 2. TEST TABLE bottom gridlines ───────────────────────────────────────────
print("\n== 2. TEST TABLE bottom gridlines (both images) ==")
TT_BOTTOMS = [251, 389, 527]
for bi, yb in enumerate(TT_BOTTOMS, 1):
    for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
        seg = (r_sl(~m["white"], yb - 2, yb + 2, 670, 870) if ren
               else o_sl(~m["white"], yb - 2, yb + 2, 670, 870))
        n = int(seg.sum())
        # colour of the line pixels
        px = (ri[int((yb - 1) * S):int((yb + 1) * S) + 1, int(670 * S):int(870 * S)] if ren
              else oi[yb - 1:yb + 2, 670:871]).reshape(-1, 3)
        nz = px[px.sum(axis=1) <= 735]
        med = np.median(nz, axis=0).astype(int) if len(nz) else None
        # is there anything on the row just below (would indicate a double line)
        below = int((r_sl(~m["white"], yb + 4, yb + 9, 670, 870) if ren
                     else o_sl(~m["white"], yb + 4, yb + 9, 670, 870)).sum())
        print(f"  B{bi} bottom y{yb} {nm}: nonwhite n={n} linemedian={med.tolist() if med is not None else None} below(y+4..9)={below}")
    # also the row ABOVE bottom to make sure interior is as expected
print("\n  (reference) TRAIN table bottoms:")
TB_BOTTOMS = [249, 389, 526]
for bi, yb in enumerate(TB_BOTTOMS, 1):
    for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
        seg = (r_sl(~m["white"], yb - 2, yb + 2, 94, 457) if ren
               else o_sl(~m["white"], yb - 2, yb + 2, 94, 457))
        print(f"  T-B{bi} bottom y{yb} {nm}: nonwhite n={int(seg.sum())}")

# ── 3. W-BOX right paren extents (per band, both images) ─────────────────────
print("\n== 3. W-BOX interior right edge (dark ink) per band ==")
WB = [(127, 251, 505, 624), (265, 389, 505, 624), (403, 527, 505, 624)]
for bi, (ya, yb, xa, xb) in enumerate(WB, 1):
    for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
        sub = r_sl(m["dark"], ya + 4, yb - 4, 554, 624) if ren else o_sl(m["dark"], ya + 4, yb - 4, 554, 624)
        ys, xs = np.where(sub)
        if len(xs):
            if ren:
                print(f"  Wbox B{bi} {nm}: dark x{554 + xs.min() / S:.1f}..{554 + xs.max() / S:.1f}  y{ya + 4 + ys.min() / S:.1f}..{ya + 4 + ys.max() / S:.1f}  n={len(xs)}")
            else:
                print(f"  Wbox B{bi} {nm}: dark x{554 + xs.min()}..{554 + xs.max()}  y{ya + 4 + ys.min()}..{ya + 4 + ys.max()}  n={len(xs)}")
        else:
            print(f"  Wbox B{bi} {nm}: no dark ink")
    # column profile of the right edge zone (frame x 595..625) for the original
    for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
        prof = (r_sl(m["dark"], ya + 20, yb - 20, 595, 624).sum(axis=0) if ren
                else o_sl(m["dark"], ya + 20, yb - 20, 595, 624).sum(axis=0))
        cols = [(595 + (i / S if ren else i), int(v)) for i, v in enumerate(prof) if v > 0]
        if cols:
            print(f"    right-zone cols {nm}: first x{cols[0][0]:.1f} last x{cols[-1][0]:.1f} (n cols {len(cols)})")
        else:
            print(f"    right-zone cols {nm}: empty x595..624")

# ── 4. FRAME CONTAINMENT left of stroke ──────────────────────────────────────
print("\n== 4. non-white ink left of x56 (render) ==")
anyink = ~mr["white"]
left = anyink[:, :int(56 * S)]
print("  count:", int(left.sum()))
ys, xs = np.where(left)
if len(xs):
    print(f"  y range {ys.min() / S:.1f}..{ys.max() / S:.1f}  x range {xs.min() / S:.1f}..{xs.max() / S:.1f} (frame px)")
    px = ri[ys, xs]
    # classify panel gray vs other
    ispanel = (np.abs(px[:, 0] - 233) < 22) & (np.abs(px[:, 1] - 233) < 22) & (np.abs(px[:, 2] - 231) < 24)
    print(f"  panel-gray-like: {int(ispanel.sum())}   other: {int((~ispanel).sum())}")
    otherpx = px[~ispanel]
    if len(otherpx):
        print("  other px sample:", otherpx[:10].tolist())
        print("  other px mean:", otherpx.mean(axis=0).round(1).tolist())
right = anyink[:, int(904 * S):]
print("  right of x904 count:", int(right.sum()))
