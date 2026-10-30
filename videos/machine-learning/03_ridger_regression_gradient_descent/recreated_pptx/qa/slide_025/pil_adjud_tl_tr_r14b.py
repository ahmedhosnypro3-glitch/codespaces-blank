#!/usr/bin/env python3
"""PIL adjudication of att14 TL/TR findings vs unique_slides/slide_025.jpg.

TL:
  A1 y186 red line right extent + figure redrect border position (overflow?)
  A2 third red line (y~200) extent
  A3 left tick label sign (2 vs -2) via bbox width + dash-gap detection
  A4 right tick label sign
  A5 bottom front-edge tick labels (0/0/-2/-2) cluster census
  A6 label-box yellow 'C' ink: first yellow x in render vs orig
  A7 surface ink coverage at domain corners (bell vs filled dome)
  A8 floor contour-ring ink in the flat base zone
TR:
  B1 slanted segment B (737..755, y210..225) red ink in orig?
  B2 front-left tick label order: label cluster y-centers top->bottom
  B3 back-pane dotted grid ink
  B4 floor contour ring ink density
"""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{V}/recreated_pptx/qa/slide_025"
S = 2001 / 960.0

orig = np.asarray(Image.open(f"{V}/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(f"{QA}/render_14.png").convert("RGB")).astype(int)


def zone(a, x0, y0, x1, y1, sc=1.0):
    return a[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]


def red_mask(z):
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    return (r > 120) & (r - g > 60) & (r - b > 60)


def dark_mask(z):
    return z.sum(axis=2) < 400


def runs_along_x(mask, min_run=2):
    cols = mask.any(axis=0)
    out, st = [], None
    for i, v in enumerate(cols):
        if v and st is None:
            st = i
        elif not v and st is not None:
            if i - st >= min_run:
                out.append((st, i - 1))
            st = None
    if st is not None:
        out.append((st, len(cols) - 1))
    return out


def label_clusters(mask, axis=0, gap=2, min_ink=2):
    """1-D ink clusters along axis with gaps."""
    proj = mask.sum(axis=1 - axis)
    idx = np.nonzero(proj >= min_ink)[0]
    if not len(idx):
        return []
    out, st, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i > prev + gap:
            out.append((st, prev))
            st = i
        prev = i
    out.append((st, prev))
    return out


print("=" * 72)
print("TL red lines")
print("=" * 72)
# A1/A2: red horizontal runs in rows y164..206, x95..295 (frame px)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    z = zone(a, 95, 160, 300, 210, sc)
    m = red_mask(z)
    print(f"--- {tag} rows y160..210 x95..300 ---")
    rowproj = m.sum(axis=1)
    for y in np.nonzero(rowproj > 8)[0]:
        xs = np.nonzero(m[y])[0]
        print(f"  row y={160 + y / sc:6.1f}  x {95 + xs.min() / sc:6.1f}..{95 + xs.max() / sc:6.1f}  n={int(rowproj[y])}")

print()
print("=" * 72)
print("TL figure redrect border: vertical red strokes x255..300, y110..295")
print("=" * 72)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    z = zone(a, 250, 110, 305, 295, sc)
    m = red_mask(z)
    colproj = m.sum(axis=0)
    peaks = [(250 + i / sc, int(colproj[i])) for i in np.nonzero(colproj > 30)[0]]
    print(f"{tag}: tall red columns: {peaks[:12]}")

print()
print("=" * 72)
print("TL tick labels")
print("=" * 72)
# A3: left tick zone — frame x88..112, y225..255 (judge: label at ~(100,238))
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    for (zx0, zy0, zx1, zy1, name) in [
        (88, 225, 114, 252, "left tick y~238"),
        (238, 232, 264, 256, "right tick y~244"),
        (118, 258, 230, 292, "bottom front edge"),
    ]:
        z = zone(a, zx0, zy0, zx1, zy1, sc)
        m = dark_mask(z)
        cl = label_clusters(m, axis=1, gap=3, min_ink=2)
        print(f"{tag:7s} {name}: {len(cl)} cluster(s)")
        for (cy0, cy1) in cl:
            sub = m[cy0:cy1 + 1]
            cols = np.nonzero(sub.any(axis=0))[0]
            # sub-clusters along x with gap>=2 (dash separated from digit)
            xr = [(cols[0], cols[-1])]
            gaps = np.nonzero(np.diff(cols) > 1)[0]
            segs, st = [], cols[0]
            prev = cols[0]
            for c in cols[1:]:
                if c > prev + 1:
                    segs.append((st, prev)); st = c
                prev = c
            segs.append((st, prev))
            print(f"    y {zy0 + cy0 / sc:6.1f}..{zy0 + cy1 / sc:6.1f}  "
                  f"w={(cols.max() - cols.min() + 1) / sc:5.1f}  "
                  f"xsegs={[(round(zx0 + s0 / sc, 1), round(zx0 + s1 / sc, 1)) for s0, s1 in segs]}")

print()
print("=" * 72)
print("A6 label-box yellow ink (box1 y130..180, x262..300)")
print("=" * 72)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    z = zone(a, 262, 130, 305, 182, sc)
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    yel = (r > 170) & (g > 150) & (b < 140)
    blu = (b > 120) & (b - r > 50)
    ys, xs = np.nonzero(yel)
    if len(xs):
        print(f"{tag}: yellow n={len(xs)}  x {262 + xs.min() / sc:.1f}..{262 + xs.max() / sc:.1f}  "
              f"y {130 + ys.min() / sc:.1f}..{130 + ys.max() / sc:.1f}")
    else:
        print(f"{tag}: yellow NONE; blue n={int(blu.sum())}")
    # blue box bbox
    ys, xs = np.nonzero(blu)
    if len(xs):
        print(f"        blue box x {262 + xs.min() / sc:.1f}..{262 + xs.max() / sc:.1f}  "
              f"y {130 + ys.min() / sc:.1f}..{130 + ys.max() / sc:.1f}")

print()
print("=" * 72)
print("A7 TL surface ink at domain corners (jet-colored pixels)")
print("=" * 72)
CORNERS = [("left corner", 96, 195, 130, 235), ("right corner", 225, 195, 258, 235),
           ("front corner", 150, 240, 210, 275)]
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    for nm, x0, y0, x1, y1 in CORNERS:
        z = zone(a, x0, y0, x1, y1, sc)
        r, g, b = z[..., 0], z[..., 1], z[..., 2]
        jet = ((b - r > 40) | (r - b > 40) | (g - b > 40)) & ~((r > 200) & (g > 200) & (b > 200))
        print(f"{tag:7s} {nm:13s} jet-ink {int(jet.sum()):5d} / {jet.size}")

print()
print("=" * 72)
print("A8 floor ring ink in flat base band (y245..285, x95..255)")
print("=" * 72)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    z = zone(a, 95, 245, 255, 285, sc)
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    cyan = (b > 110) & (b - r > 40) & (g - r > 20)
    yel = (r > 150) & (g > 120) & (r - b > 60)
    grn = (g > 110) & (g - r > 35) & (g - b > 35)
    print(f"{tag}: cyan {int(cyan.sum())}  yellow {int(yel.sum())}  green {int(grn.sum())}")

print()
print("=" * 72)
print("TR B1 slanted segment B zone x730..765 y205..232")
print("=" * 72)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    z = zone(a, 730, 205, 765, 232, sc)
    m = red_mask(z)
    print(f"{tag}: red px {int(m.sum())}")

print()
print("=" * 72)
print("TR B2 front-left edge tick labels (x608..650, y150..320)")
print("=" * 72)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    z = zone(a, 604, 150, 652, 322, sc)
    m = dark_mask(z)
    cl = label_clusters(m, axis=0, gap=4, min_ink=3)
    print(f"{tag}: {len(cl)} row clusters (top->bottom):")
    for (cy0, cy1) in cl:
        sub = m[cy0:cy1 + 1]
        cols = np.nonzero(sub.any(axis=0))[0]
        print(f"    y {150 + (cy0 + cy1) / 2 / sc:6.1f}  w={(cols.max() - cols.min() + 1) / sc:5.1f}  n={int(sub.sum())}")

print()
print("=" * 72)
print("B3 back-pane dotted grid ink (TR upper zone x660..870 y120..160)")
print("=" * 72)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    z = zone(a, 660, 120, 870, 160, sc)
    m = dark_mask(z)
    print(f"{tag}: dark px {int(m.sum())}")

print()
print("=" * 72)
print("B4 TR floor contour ring ink (x640..860 y285..315)")
print("=" * 72)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND14", rend, S)):
    z = zone(a, 640, 285, 860, 315, sc)
    m = dark_mask(z)
    gray = (abs(z[..., 0] - z[..., 1]) < 25) & (abs(z[..., 1] - z[..., 2]) < 25) & (z.sum(axis=2) < 600)
    print(f"{tag}: gray-ink {int(gray.sum())}  dark {int(m.sum())}")
