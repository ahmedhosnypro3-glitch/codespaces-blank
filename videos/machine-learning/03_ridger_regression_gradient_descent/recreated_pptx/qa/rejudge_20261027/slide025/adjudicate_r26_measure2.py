#!/usr/bin/env python3
"""Round-2 probes for adjudicate_full_fresh2_r26: D1, D2, D5, D6, D8 precise checks."""
import numpy as np
from PIL import Image
from collections import Counter

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025"
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

r = np.asarray(Image.open(f"{OUT}/render_cur.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB").resize((2001, 1125), Image.LANCZOS)).astype(int)
H, W = r.shape[:2]
sx, sy = W / 960.0, H / 540.0


def box(a, x0, y0, x1, y1):
    return a[int(y0 * sy):int(np.ceil(y1 * sy)), int(x0 * sx):int(np.ceil(x1 * sx))]


def is_red(px):
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    return (R > 140) & (G < 90) & (B < 90) & (R - G > 70)


def is_darkink(px):
    return px.sum(axis=2) < 330


def sbb(img, mask, x0, y0):
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return f"x{x0 + xs.min()/sx:.0f}-{x0 + xs.max()/sx:.0f} y{y0 + ys.min()/sy:.0f}-{y0 + ys.max()/sy:.0f} n={int(mask.sum())}"


print("== D1 precise: TR axes upper-left corner zone (x622-700, y122-165) dark ink per image ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 622, 122, 700, 165)
    ink = is_darkink(sub)
    print(f"  {label}: {sbb(img, ink, 622, 122)}")
# row-profile of ink in that zone to see tick rows
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 622, 122, 700, 165)
    ink = is_darkink(sub)
    rows = ink.sum(axis=1)
    nz = np.nonzero(rows > 2)[0]
    print(f"  {label} ink rows (slide y):", [round(122 + i / sy, 1) for i in nz][:40])

print("\n== D1b: whole TR interior dark-ink count (x625-870, y125-310), and 'x10' glyph zone (x625-665, y125-150) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 625, 125, 870, 310)
    print(f"  {label}: TR interior dark ink px {int(is_darkink(sub).sum())}")
    g = box(img, 625, 125, 665, 150)
    print(f"    x10-glyph zone ink px {int(is_darkink(g).sum())}")

print("\n== D2: TR surface color composition, inner plot area (x640-860, y140-300) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 640, 140, 860, 300).reshape(-1, 3)
    q = (sub // 48)
    c = Counter(map(tuple, q))
    tot = sub.shape[0]
    tops = c.most_common(6)
    print(f"  {label}:", "; ".join(f"bin{k}~RGB{k[0]*48+24},{k[1]*48+24},{k[2]*48+24} {100.0*v/tot:.1f}%" for k, v in tops))
    # red spike presence: strong red px count in upper half of plot (rear)
    rear = box(img, 640, 140, 860, 220)
    print(f"    rear-half strong-red px: {int(is_red(rear).sum())}")
    front = box(img, 640, 220, 860, 300)
    print(f"    front-half deep-blue px (B>120,R<80,G<80): {int(((front[...,2]>120)&(front[...,0]<80)&(front[...,1]<80)).sum())}")

print("\n== D5 precise: BL label text lines — wide probe boxes, per-line ink rows ==")
probes = {"GlobalMaxima": (180, 285, 340, 322), "LocalMaxima": (230, 328, 340, 360),
          "LocalMinima": (100, 438, 220, 470), "GlobalMinima": (230, 455, 340, 495)}
for name, (x0, y0, x1, y1) in probes.items():
    for label, img in [("render", r), ("orig", o)]:
        sub = box(img, x0, y0, x1, y1)
        ink = is_darkink(sub)
        ys, xs = np.nonzero(ink)
        if len(xs):
            # cluster rows into lines
            rows = sorted(set(int(y / sy) for y in ys))
            groups = []
            s = p = rows[0]
            for rr in rows[1:]:
                if rr - p > 2:
                    groups.append((s, p)); s = rr
                p = rr
            groups.append((s, p))
            print(f"  {name} {label}: bbox {sbb(img, ink, x0, y0)} text-line y-groups {[(y0+a, y0+b) for a, b in groups]}")
        else:
            print(f"  {name} {label}: NO ink")

print("\n== D6 precise: BR frame + raster edge contact ==")
for label, img in [("render", r), ("orig", o)]:
    # find BR frame: red pixels in BR quadrant; frame = 4 edges of rect
    q = box(img, 560, 340, 900, 535)
    m = is_red(q)
    colsum = m.sum(axis=0); rowsum = m.sum(axis=1)
    cols = np.nonzero(colsum > 0.6 * m.shape[0])[0]
    rows = np.nonzero(rowsum > 0.6 * m.shape[1])[0]
    if not len(cols) or not len(rows):
        # fallback: looser
        cols = np.nonzero(colsum > 0.3 * m.shape[0])[0]
        rows = np.nonzero(rowsum > 0.3 * m.shape[1])[0]
    fl, fr = 560 + cols.min() / sx, 560 + cols.max() / sx
    ft, fb = 340 + rows.min() / sy, 340 + rows.max() / sy
    inner = box(img, fl + 1.5, ft + 1.5, fr - 1.5, fb - 1.5)
    nonwhite = ~((inner > 235).all(axis=2))
    e = 3
    print(f"  {label}: BR frame x{fl:.0f}-{fr:.0f} y{ft:.0f}-{fb:.0f} (w{fr-fl:.0f} h{fb-ft:.0f}) inner {inner.shape[1]}x{inner.shape[0]} nonwhite% {100.0*nonwhite.mean():.1f}")
    print(f"    edge strips nonwhite px: top {int(nonwhite[:e].sum())}/{e*inner.shape[1]}  bottom {int(nonwhite[-e:].sum())}/{e*inner.shape[1]}  left {int(nonwhite[:,:e].sum())}/{e*inner.shape[0]}  right {int(nonwhite[:,-e:].sum())}/{e*inner.shape[0]}")

print("\n== D8 precise: TL left tick labels — ink columns x86-120, rows grouped, per image ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 84, 118, 122, 330)
    ink = is_darkink(sub)
    ys, xs = np.nonzero(ink)
    if len(xs):
        rows = sorted(set(int(y / sy) for y in ys))
        groups = []
        s = p = rows[0]
        for rr in rows[1:]:
            if rr - p > 2:
                groups.append((s, p)); s = rr
            p = rr
        groups.append((s, p))
        print(f"  {label}: tick-label text y-groups (slide): {[(118+a, 118+b) for a, b in groups]} total ink {int(ink.sum())}")
    else:
        print(f"  {label}: no ink x84-122")

print("\n== D7: TL interior — contour/gray-box presence: gray px + dark gridline px inside TL (x92-370, y122-292) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 92, 122, 370, 292)
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    gray = (np.abs(R - G) < 14) & (np.abs(G - B) < 14) & (R > 150) & (R < 235)
    dark = sub.sum(axis=2) < 330
    print(f"  {label}: gray px {int(gray.sum())} ({100.0*gray.mean():.1f}%)  dark ink px {int(dark.sum())} ({100.0*dark.mean():.1f}%)")

print("\n== D3 verify: TR frame vert extent via long vert cols; also TL/BL/BR frame rects both images ==")
for qname, (qx0, qy0, qx1, qy1) in {"TL": (60, 100, 560, 340), "TR": (560, 100, 900, 340), "BL": (60, 340, 560, 535), "BR": (560, 340, 900, 535)}.items():
    for label, img in [("render", r), ("orig", o)]:
        q = box(img, qx0, qy0, qx1, qy1)
        m = is_red(q)
        colsum = m.sum(axis=0); rowsum = m.sum(axis=1)
        cols = np.nonzero(colsum > 0.6 * m.shape[0])[0]
        rows = np.nonzero(rowsum > 0.6 * m.shape[1])[0]
        if len(cols) and len(rows):
            print(f"  {qname} {label}: frame x{qx0+cols.min()/sx:.0f}-{qx0+cols.max()/sx:.0f} y{qy0+rows.min()/sy:.0f}-{qy0+rows.max()/sy:.0f}  w{(cols.max()-cols.min())/sx:.0f} h{(rows.max()-rows.min())/sy:.0f}")
        else:
            print(f"  {qname} {label}: frame detect failed (cols {len(cols)} rows {len(rows)})")
