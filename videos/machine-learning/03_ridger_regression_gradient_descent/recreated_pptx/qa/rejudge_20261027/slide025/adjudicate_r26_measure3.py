#!/usr/bin/env python3
"""Round-3 probes: BR frame via bbox, TR z-tick column, TL tick band, D5 centroids, D10 strokes."""
import numpy as np
from PIL import Image

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


def line_groups(mask, axis, off, scale, gap=3, minpx=2):
    s = mask.sum(axis=1 - axis) if axis == 0 else mask.sum(axis=0)
    nz = np.nonzero(s > minpx)[0]
    if not len(nz):
        return []
    groups = []
    st = p = nz[0]
    for i in nz[1:]:
        if i - p > gap * scale:
            groups.append((off + st / scale, off + p / scale)); st = i
        p = i
    groups.append((off + st / scale, off + p / scale))
    return [(round(a, 1), round(b, 1)) for a, b in groups]


print("== D6 round3: BR frame via red bbox in quadrant (560,340)-(900,535) ==")
for label, img in [("render", r), ("orig", o)]:
    q = box(img, 560, 340, 900, 535)
    m = is_red(q)
    ys, xs = np.nonzero(m)
    fl, fr = 560 + xs.min() / sx, 560 + xs.max() / sx
    ft, fb = 340 + ys.min() / sy, 340 + ys.max() / sy
    print(f"  {label}: red bbox frame x{fl:.1f}-{fr:.1f} y{ft:.1f}-{fb:.1f} (w{fr-fl:.1f} h{fb-ft:.1f}) red px {int(m.sum())}")
    inner = box(img, fl + 2, ft + 2, fr - 2, fb - 2)
    if inner.size:
        nonwhite = ~((inner > 235).all(axis=2))
        e = 3
        print(f"    inner {inner.shape[1]}x{inner.shape[0]} nonwhite {100.0*nonwhite.mean():.1f}% | edge strips nonwhite: top {int(nonwhite[:e].sum())}/{e*inner.shape[1]} bottom {int(nonwhite[-e:].sum())}/{e*inner.shape[1]} left {int(nonwhite[:,:e].sum())}/{e*inner.shape[0]} right {int(nonwhite[:,-e:].sum())}/{e*inner.shape[0]}")
        # distance from raster edge to frame: first fully-white margin width on each side
        col_nw = nonwhite.mean(axis=0); row_nw = nonwhite.mean(axis=1)
        def margin(prof, from_start):
            n = len(prof)
            i = 0 if from_start else n - 1
            cnt = 0
            step = 1 if from_start else -1
            while 0 <= i < n and prof[i] < 0.02:
                cnt += 1; i += step
            return cnt / sx if axis_is_x else cnt / sy
        axis_is_x = True
        print(f"    white margin px: left {margin(col_nw, True):.1f} right {margin(col_nw, False):.1f}", end="")
        axis_is_x = False
        print(f" top {margin(row_nw, True):.1f} bottom {margin(row_nw, False):.1f}")

print("\n== D1 round3: TR z-tick column (x624-652) full plot height y124-310: text-line groups + ink ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 624, 124, 652, 310)
    ink = is_darkink(sub)
    print(f"  {label}: ink px {int(ink.sum())}, row text-line groups: {line_groups(ink, 0, 124, sy, gap=2, minpx=1)}")

print("\n== D1 round3b: above-box scale-annotation zone (x626-700, y122-140) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 626, 122, 700, 140)
    ink = is_darkink(sub)
    ys, xs = np.nonzero(ink)
    bb = f"x{626+xs.min()/sx:.0f}-{626+xs.max()/sx:.0f} y{122+ys.min()/sy:.0f}-{122+ys.max()/sy:.0f}" if len(xs) else "none"
    print(f"  {label}: ink px {int(ink.sum())} bbox {bb}")

print("\n== D8 round3: TL tick-label band x92-120 y125-290 (right of frame line): text-line groups ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 92, 125, 120, 290)
    ink = is_darkink(sub)
    print(f"  {label}: ink px {int(ink.sum())}, y-groups: {line_groups(ink, 0, 125, sy, gap=2, minpx=1)}")

print("\n== D5 round3: dark-ink centroid in +-22px windows around judge-claimed label centers ==")
claims = {"GlobalMaxima": ((215, 302), (240, 300)), "LocalMaxima": ((252, 338), (275, 340)),
          "LocalMinima": ((125, 446), (140, 455))}
for name, ((rx, ry), (ox, oy)) in claims.items():
    for label, img, (cx, cy) in [("render", r, (rx, ry)), ("orig", o, (ox, oy))]:
        sub = box(img, cx - 22, cy - 12, cx + 22, cy + 12)
        ink = is_darkink(sub)
        ys, xs = np.nonzero(ink)
        if len(xs):
            print(f"  {name} {label} @({cx},{cy}): ink {int(ink.sum())} centroid ({cx-22+xs.mean()/sx:.1f}, {cy-12+ys.mean()/sy:.1f}) bbox x{cx-22+xs.min()/sx:.0f}-{cx-22+xs.max()/sx:.0f} y{cy-12+ys.min()/sy:.0f}-{cy-12+ys.max()/sy:.0f}")
        else:
            print(f"  {name} {label} @({cx},{cy}): no ink in window")

print("\n== D10 round3: red stroke pixels inside TR interior excluding frame (x625-870 y124-310) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 625, 124, 870, 310)
    m = is_red(sub)
    # remove frame-adjacent pixels: frame at x~619/876, y~118/315; keep interior margin 6px
    mm = m.copy()
    mm[:int(8*sy), :] = False; mm[-int(8*sy):, :] = False
    mm[:, :int(8*sx)] = False; mm[:, -int(8*sx):] = False
    ys, xs = np.nonzero(mm)
    if len(xs):
        print(f"  {label}: interior red px {int(mm.sum())} centroid ({625+xs.mean()/sx:.1f}, {124+ys.mean()/sy:.1f}) bbox x{625+xs.min()/sx:.0f}-{625+xs.max()/sx:.0f} y{124+ys.min()/sy:.0f}-{124+ys.max()/sy:.0f}")
    else:
        print(f"  {label}: no interior red")

print("\n== D2 round3: TR rear spike: strong-red px in rear third (x640-860, y140-180) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 640, 140, 860, 180)
    print(f"  {label}: rear-strip strong-red px {int(is_red(sub).sum())}, area {sub.shape[0]*sub.shape[1]}")

print("\n== D4 round3: BL — gray grid-wall px in left+rear walls only (x95-380, y360-470) and surface fill ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 95, 360, 380, 470)
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    gray = (np.abs(R - G) < 14) & (np.abs(G - B) < 14) & (R > 150) & (R < 235)
    red = is_red(sub)
    blue = (B > 120) & (R < 80) & (G < 80)
    green = (G > 180) & (R < 170) & (B < 170)
    print(f"  {label}: gray {100.0*gray.mean():.1f}% red {100.0*red.mean():.1f}% blue {100.0*blue.mean():.1f}% green {100.0*green.mean():.1f}%")

print("\n== D7 round3: TL contour lines — dark ink inside dome area (x100-360, y130-280) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 100, 130, 360, 280)
    print(f"  {label}: dark ink px {int(is_darkink(sub).sum())} ({100.0*is_darkink(sub).mean():.1f}%)")
