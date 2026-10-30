#!/usr/bin/env python3
"""Slide 003 take-6 precise geometry probe (original frame only).

Measures the top matrix box regions the judges disputed:
- the three colored bands (yellow/cyan/pink): bbox, interior dark-ink counts
  (do bands contain row entries?), paren strokes around columns
- header glyphs X_1/X_2/X_n: bbox + color (X_2 red?)
- ellipsis separator column between cyan and pink
- y-labels: inside-band vs below-band
- bottom-left: X-matrix bracket strokes, N x d+1 dimension label position
- w-vector: entries present incl. 'b', bracket span
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
ORIG = f"{B}/unique_slides/slide_003.jpg"
a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W = a.shape[:2]
print(f"original {W}x{H}")


def mask_near(rgb, tol):
    return ((np.abs(a[:, :, 0] - rgb[0]) < tol) &
            (np.abs(a[:, :, 1] - rgb[1]) < tol) &
            (np.abs(a[:, :, 2] - rgb[2]) < tol))


def runs(cols, off, minpx=1):
    out, start = [], None
    for i, v in enumerate(cols):
        if v >= minpx and start is None:
            start = i
        elif v < minpx and start is not None:
            out.append((off + start, off + i - 1))
            start = None
    if start is not None:
        out.append((off + start, off + len(cols) - 1))
    return out


def bbox(m, label, y0, y1, x0=0, x1=W):
    sub = m[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        print(f"  {label}: none")
        return None
    b = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
    print(f"  {label}: x{b[0]}..{b[2]} y{b[1]}..{b[3]} "
          f"(cx {(b[0]+b[2])//2}, w {b[2]-b[0]+1}, h {b[3]-b[1]+1})")
    return b


def dark_frac(m_inner, label):
    sub = a[m_inner[1]:m_inner[3], m_inner[0]:m_inner[2]]
    dark = ((sub[:, :, 0] < 110) & (sub[:, :, 1] < 110) & (sub[:, :, 2] < 110)).sum()
    red = ((sub[:, :, 0] > 145) & (sub[:, :, 0] - sub[:, :, 1] > 45) &
           (sub[:, :, 0] - sub[:, :, 2] > 45)).sum()
    tot = sub.shape[0] * sub.shape[1]
    print(f"    inner dark={dark} red={red} of {tot} px -> "
          f"dark%={100*dark/tot:.1f} red%={100*red/tot:.1f}")


YEL = mask_near((255, 255, 153), 40)   # FFFF99 family (pale yellow)
CYA = mask_near((204, 255, 255), 30)   # CCFFFF cyan
PNK = mask_near((255, 192, 203), 30)   # FFC0CB pink

print("\n== TOP BOX bands ==")
yb = bbox(YEL, "yellow band", 130, 300)
cb = bbox(CYA, "cyan band", 130, 300)
pb = bbox(PNK, "pink band", 130, 300)

print("\n== interior ink of each band (exclude 8px edge, header y<140, y-label y>272) ==")
if yb:
    dark_frac((yb[0] + 8, 142, yb[2] - 8, 272), "yellow")
if cb:
    dark_frac((cb[0] + 8, 142, cb[2] - 8, 272), "cyan")
if pb:
    dark_frac((pb[0] + 8, 142, pb[2] - 8, 272), "pink")

print("\n== header glyphs row y115..140 (x265..600): dark/red ink columns ==")
sub = a[113:140, 265:600]
for name, m in (("dark", (sub[:, :, 0] < 110) & (sub[:, :, 1] < 110) & (sub[:, :, 2] < 110)),
                ("red", (sub[:, :, 0] > 145) & (sub[:, :, 0] - sub[:, :, 1] > 45) &
                 (sub[:, :, 0] - sub[:, :, 2] > 45)),
                ("blue", (sub[:, :, 2] > 145) & (sub[:, :, 2] - sub[:, :, 0] > 30))):
    cols = m.sum(axis=0)
    rl = ", ".join(f"x{s}..{e}" for s, e in runs(cols, 265) if True)
    print(f"  {name}: runs {rl}")

print("\n== ellipsis column between cyan and pink (x416..510, y141..296): dark px per col ==")
sub = a[141:296, 416:512]
dark = ((sub[:, :, 0] < 110) & (sub[:, :, 1] < 110) & (sub[:, :, 2] < 110))
cols = dark.sum(axis=0)
for s, e in runs(cols, 416):
    print(f"  dark column-run x{s}..{e} (px {cols[s-416:e-416+1].max()} max)")

print("\n== parens around bands? dark px in gaps left of yellow (x276..315, y141..296) ==")
for (gx0, gx1, lab) in ((276, 314, "left of yellow"), (345, 371, "yellow|cyan"),
                        (429, 470, "cyan|gap"), (471, 511, "gap|pink"), (559, 595, "right of pink")):
    sub = a[141:296, gx0:gx1]
    dark = ((sub[:, :, 0] < 110) & (sub[:, :, 1] < 110) & (sub[:, :, 2] < 110)).sum()
    print(f"  {lab} x{gx0}..{gx1}: dark px = {dark}")

print("\n== y-labels: red px bbox inside bottom of bands (y270..300) ==")
sub = a[268:302, 265:600]
redm = ((sub[:, :, 0] > 145) & (sub[:, :, 0] - sub[:, :, 1] > 45) &
        (sub[:, :, 0] - sub[:, :, 2] > 45))
cols = redm.sum(axis=0)
for s, e in runs(cols, 265):
    print(f"  red column-run x{s}..{e}")

print("\n== BOTTOM-LEFT box: bracket strokes + dim labels (frame x60..545 y320..520) ==")
dark = ((a[:, :, 0] < 110) & (a[:, :, 1] < 110) & (a[:, :, 2] < 110))
sub = dark[320:520, 60:545]
cols = sub.sum(axis=0)
print("  dark column-runs (brackets):")
for s, e in runs(cols, 60):
    print(f"    x{s}..{e} maxpx {cols[s-60:e-60+1].max()}")
sub2 = dark[470:505, 60:545]
cols2 = sub2.sum(axis=0)
print("  dim-label row band y470..505 dark column-runs:")
for s, e in runs(cols2, 60):
    print(f"    x{s}..{e} maxpx {cols2[s-60:e-60+1].max()}")
red = ((a[:, :, 0] > 145) & (a[:, :, 0] - a[:, :, 1] > 45) & (a[:, :, 0] - a[:, :, 2] > 45))
sub3 = red[465:510, 60:545]
cols3 = sub3.sum(axis=0)
print("  red column-runs in y465..510:")
for s, e in runs(cols3, 60):
    print(f"    x{s}..{e} maxpx {cols3[s-60:e-60+1].max()}")

print("\n== w-vector column (x350..420, y325..505): dark px per row ==")
sub = dark[325:505, 345:425]
rows = sub.sum(axis=1)
for s, e in runs(rows, 325):
    print(f"  row-run y{s}..{e} maxpx {rows[s-325:e-325+1].max()}")


def runs(cols, off, minpx=1):
    out, start = [], None
    for i, v in enumerate(cols):
        if v >= minpx and start is None:
            start = i
        elif v < minpx and start is not None:
            out.append((off + start, off + i - 1))
            start = None
    if start is not None:
        out.append((off + start, off + len(cols) - 1))
    return out
