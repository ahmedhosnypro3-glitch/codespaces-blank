#!/usr/bin/env python3
"""Per-claim pixel adjudication of judge_full_fresh2.txt (slide 025) on render_cur.png.

render_cur.png is a fresh 150dpi render of the deliverable pinned at md5
736036754a8d6f2e4a582eefdf99effd (byte-identical to the backup bank copy) and is
pixel-identical to render.png, the IMG1 that judge_full_fresh2.txt judged.
All coordinates below are SLIDE-SPACE px (960x540 frame; 1px = 1pt).
"""
import numpy as np
from PIL import Image

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025"
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

r = np.asarray(Image.open(f"{OUT}/render_cur.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
H, W = r.shape[:2]
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB").resize((W, H), Image.LANCZOS)).astype(int)
sx, sy = W / 960.0, H / 540.0


def box(a, x0, y0, x1, y1):
    return a[int(y0 * sy):int(np.ceil(y1 * sy)), int(x0 * sx):int(np.ceil(x1 * sx))]


def is_red(px):
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    return (R > 140) & (G < 90) & (B < 90) & (R - G > 70)


def is_darkink(px):
    return px.sum(axis=2) < 330


def is_graybox(px):
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    return (np.abs(R - G) < 14) & (np.abs(G - B) < 14) & (R > 150) & (R < 235)


def bbox_of(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(mask.sum())


def slide_bbox(mask_full):
    ys, xs = np.nonzero(mask_full)
    if len(xs) == 0:
        return None
    return (round(xs.min() / sx, 1), round(ys.min() / sy, 1),
            round(xs.max() / sx, 1), round(ys.max() / sy, 1), int(mask_full.sum()))


def diff_stats(x0, y0, x1, y1):
    a, b = box(r, x0, y0, x1, y1), box(o, x0, y0, x1, y1)
    d = np.abs(a - b).sum(axis=2)
    n = d.size
    return int((d > 90).sum()), f"{100.0 * (d > 90).mean():.1f}%", n


print("== render_cur:", W, "x", H, "scale", round(sx, 4), round(sy, 4))
print("\n== A. red plot-frame rectangles (per quadrant), slide-space bbox of red frame ink ==")
for qname, (qx0, qy0, qx1, qy1) in {
    "TL": (60, 100, 560, 340), "TR": (560, 100, 900, 340),
    "BL": (60, 340, 560, 535), "BR": (560, 340, 900, 535),
}.items():
    for label, img in [("render", r), ("orig", o)]:
        sub = box(img, qx0, qy0, qx1, qy1)
        m = is_red(sub)
        bb = slide_bbox_full = None
        ys, xs = np.nonzero(m)
        if len(xs):
            bx0 = qx0 + xs.min() / sx; bx1 = qx0 + xs.max() / sx
            by0 = qy0 + ys.min() / sy; by1 = qy0 + ys.max() / sy
            # frame edges = rows/cols with many red px
            colsum = m.sum(axis=0); rowsum = m.sum(axis=1)
            cols = np.nonzero(colsum > (by1 - by0) * sy * 0.5)[0]
            rows = np.nonzero(rowsum > (bx1 - bx0) * sx * 0.5)[0]
            ce = (qx0 + (cols.min() / sx if len(cols) else -1), qx0 + (cols.max() / sx if len(cols) else -1))
            re_ = (qy0 + (rows.min() / sy if len(rows) else -1), qy0 + (rows.max() / sy if len(rows) else -1))
            print(f"  {qname} {label}: red bbox x{bx0:.0f}-{bx1:.0f} y{by0:.0f}-{by1:.0f}  long-vert-cols {ce[0]:.0f},{ce[1]:.0f}  long-horiz-rows {re_[0]:.0f},{re_[1]:.0f}")
        else:
            print(f"  {qname} {label}: NO red frame ink")

print("\n== B. per-quadrant diff stats render_cur vs orig (slide-space boxes) ==")
for qname, (x0, y0, x1, y1) in {
    "TL": (70, 110, 560, 330), "TR": (570, 110, 830, 330),
    "BL": (70, 345, 560, 530), "BR": (570, 345, 830, 530),
}.items():
    n, pct, tot = diff_stats(x0, y0, x1, y1)
    print(f"  {qname} box x{x0}-{x1} y{y0}-{y1}: diff>90 px {n} ({pct} of {tot})")

print("\n== C. D1: TR upper-left axes area — ink presence (x585-680, y120-190) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 585, 120, 680, 190)
    ink = is_darkink(sub)
    ys, xs = np.nonzero(ink)
    if len(xs):
        print(f"  {label}: dark-ink px {int(ink.sum())} bbox slide x{585+xs.min()/sx:.0f}-{585+xs.max()/sx:.0f} y{120+ys.min()/sy:.0f}-{120+ys.max()/sy:.0f}")
    else:
        print(f"  {label}: NO dark ink in TR upper-left axes area")

print("\n== D. D3: TR frame height — red horiz rows in TR (x575-825, y110-330) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 575, 110, 825, 330)
    m = is_red(sub)
    rowsum = m.sum(axis=1)
    rows = np.nonzero(rowsum > 0.5 * sub.shape[1])[0]
    if len(rows):
        # group contiguous
        groups = []
        start = rows[0]; prev = rows[0]
        for rr in rows[1:]:
            if rr - prev > 3:
                groups.append((start, prev)); start = rr
            prev = rr
        groups.append((start, prev))
        print(f"  {label}: horiz frame rows (slide y):", [(round(110+a/sy,1), round(110+b/sy,1)) for a, b in groups])

print("\n== E. D6: BR containment — ink touching inner frame edges (BR frame x~578-820 y~360-505) ==")
for label, img in [("render", r), ("orig", o)]:
    # detect BR red frame first
    sub = box(img, 570, 340, 900, 535)
    m = is_red(sub)
    ys, xs = np.nonzero(m)
    bx0 = 570 + xs.min() / sx; bx1 = 570 + xs.max() / sx
    by0 = 340 + ys.min() / sy; by1 = 340 + ys.max() / sy
    colsum = m.sum(axis=0); rowsum = m.sum(axis=1)
    cols = np.nonzero(colsum > 0.5 * m.shape[0])[0]
    rows = np.nonzero(rowsum > 0.5 * m.shape[1])[0]
    fl = 570 + cols.min() / sx; fr = 570 + cols.max() / sx
    ft = 340 + rows.min() / sy; fb = 340 + rows.max() / sy
    # non-red content ink within 3px inside each frame edge
    inner = box(img, fl + 1, ft + 1, fr - 1, fb - 1)
    redm = is_red(inner)
    content = (inner.sum(axis=2) < 720) & ~redm  # any non-white, non-red ink
    edge = 4
    top_strip = content[:edge, :]; bot_strip = content[-edge:, :]
    left_strip = content[:, :edge]; right_strip = content[:, -edge:]
    print(f"  {label}: BR frame x{fl:.0f}-{fr:.0f} y{ft:.0f}-{fb:.0f} | non-red ink in 4px strips: top {int(top_strip.sum())} bottom {int(bot_strip.sum())} left {int(left_strip.sum())} right {int(right_strip.sum())} of {edge*inner.shape[1]} / {edge*inner.shape[0]}")

print("\n== F. D4: BL gray 3D box/grid walls — gray px fraction inside BL frame ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 75, 350, 555, 525)
    g = is_graybox(sub)
    print(f"  {label}: graybox px {int(g.sum())} ({100.0*g.mean():.1f}% of BL box)")

print("\n== G. D5: BL callout label positions — dark-ink bbox near each claimed spot ==")
spots = {"GlobalMaxima": (200, 290, 270, 320), "LocalMaxima": (235, 325, 300, 355),
         "LocalMinima": (110, 435, 175, 465), "GlobalMinima": (200, 460, 300, 500)}
for sname, (x0, y0, x1, y1) in spots.items():
    for label, img in [("render", r), ("orig", o)]:
        sub = box(img, x0, y0, x1, y1)
        ink = is_darkink(sub)
        ys, xs = np.nonzero(ink)
        if len(xs):
            print(f"  {sname} {label}: ink px {int(ink.sum())} bbox slide x{x0+xs.min()/sx:.0f}-{x0+xs.max()/sx:.0f} y{y0+ys.min()/sy:.0f}-{y0+ys.max()/sy:.0f}")
        else:
            print(f"  {sname} {label}: no ink in probe box")

print("\n== H. D7/D8: TL region — gray box px, dark ink left tick strip (x70-110, y120-320) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 75, 115, 555, 330)
    print(f"  TL {label}: graybox px {int(is_graybox(sub).sum())} ({100.0*is_graybox(sub).mean():.1f}%)")
    strip = box(img, 70, 120, 112, 320)
    ink = is_darkink(strip)
    ys, xs = np.nonzero(ink)
    if len(xs):
        print(f"    left tick strip ink px {int(ink.sum())} bbox x{70+xs.min()/sx:.0f}-{70+xs.max()/sx:.0f} y{120+ys.min()/sy:.0f}-{120+ys.max()/sy:.0f}")
    else:
        print(f"    left tick strip: no ink")

print("\n== I. D9: title bbox — dark-red ink in top band (y40-105, x150-810) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 150, 40, 810, 105)
    m = is_red(sub) | is_darkink(sub)
    ys, xs = np.nonzero(m)
    if len(xs):
        print(f"  {label}: title ink px {int(m.sum())} bbox x{150+xs.min()/sx:.0f}-{150+xs.max()/sx:.0f} y{40+ys.min()/sy:.0f}-{40+ys.max()/sy:.0f}")

print("\n== J. D10: red strokes in TR upper area (x640-825, y115-200), excluding frame ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 640, 115, 825, 200)
    m = is_red(sub)
    # exclude frame borders: frame approx x578/820 y122/325 -> mask out x>810 or y>... keep interior
    ys, xs = np.nonzero(m)
    if len(xs):
        pts = [(round(640+x/sx), round(115+y/sy)) for x, y in zip(xs, ys)]
        # cluster summary: print bbox + a coarse 8x8 occupancy map
        occ = np.zeros((8, 8), int)
        for px_, py_ in pts:
            occ[min(7, (py_-115)*8//85), min(7, (px_-640)*8//185)] += 1
        print(f"  {label}: red px {len(pts)} bbox x{pts[0][0]}.. slide-x range {min(p[0] for p in pts)}-{max(p[0] for p in pts)} y {min(p[1] for p in pts)}-{max(p[1] for p in pts)}")
        for row in occ:
            print("     ", " ".join(f"{v:4d}" for v in row))
    else:
        print(f"  {label}: no red ink")

print("\n== K. color composition inside TR interior (x590-810, y130-300) — top color bins ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 590, 130, 810, 300).reshape(-1, 3)
    # quantize to 64-level bins
    q = (sub // 48)
    from collections import Counter
    c = Counter(map(tuple, q))
    tot = sub.shape[0]
    print(f"  {label} top bins (R,G,B //48):")
    for k, v in c.most_common(8):
        print(f"    bin{k}: {v} px ({100.0*v/tot:.1f}%)  approx RGB {k[0]*48+24},{k[1]*48+24},{k[2]*48+24}")

print("\n== L. color composition inside BL interior (x80-545, y355-520) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 80, 355, 545, 520).reshape(-1, 3)
    q = (sub // 48)
    from collections import Counter
    c = Counter(map(tuple, q))
    tot = sub.shape[0]
    print(f"  {label} top bins:")
    for k, v in c.most_common(8):
        print(f"    bin{k}: {v} px ({100.0*v/tot:.1f}%)  approx RGB {k[0]*48+24},{k[1]*48+24},{k[2]*48+24}")

print("\n== M. white padding inside BR frame (non-ink fraction) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 570, 340, 900, 535)
    m = is_red(sub)
    ys, xs = np.nonzero(m)
    fl = 570 + xs.min() / sx; fr = 570 + xs.max() / sx
    rowsum = m.sum(axis=1); colsum = m.sum(axis=0)
    rows = np.nonzero(rowsum > 0.5 * m.shape[1])[0]
    ft = 340 + rows.min() / sy; fb = 340 + rows.max() / sy
    inner = box(img, fl + 2, ft + 2, fr - 2, fb - 2)
    white = (inner > 235).all(axis=2)
    print(f"  {label}: BR frame x{fl:.0f}-{fr:.0f} y{ft:.0f}-{fb:.0f} inner {inner.shape[1]}x{inner.shape[0]} white frac {100.0*white.mean():.1f}%")
