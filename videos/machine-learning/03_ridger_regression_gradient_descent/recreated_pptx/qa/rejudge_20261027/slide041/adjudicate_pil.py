#!/usr/bin/env python3
"""Read-only PIL adjudication of slide 041 rejudge FAIL claims, in slide space (960x540).

Claim 1 (MAJOR): render has a 6th table column (x3=(1;2)/C1) that the original lacks;
                original supposedly has 5 columns x1,x2,x4,x6 with a gap, classes C1 C1 C2 C2 C2.
Claim 2 (MINOR): W column-vector delimiters are '(' in render vs '[' in original.

Method: measure the ORIGINAL frame directly (headers, paren pairs, per-column digits,
class-label colors), then measure the RENDER downsampled to slide space in the same bands.
"""
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"

orig = Image.open(f"{NS}/unique_slides/slide_041.jpg").convert("RGB")
ren = Image.open(f"{RJ}/slide041/render.png").convert("RGB")
print(f"orig {orig.size}  render {ren.size}  scale {ren.size[0]/960:.4f}")
S = ren.size[0] / 960.0
ren_s = ren.resize((960, 540), Image.LANCZOS)

o = np.asarray(orig).astype(int)
r = np.asarray(ren_s).astype(int)


def dark(a):
    return a.sum(axis=2) < 420  # strong ink


def redish(a):
    return (a[:, :, 0] > 120) & (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 60)


def blueish(a):
    return (a[:, :, 2] > 110) & (a[:, :, 2] - a[:, :, 0] > 50) & (a[:, :, 2] - a[:, :, 1] > 40)


def clusters(mask_1d, min_gap=3):
    idx = np.where(mask_1d)[0]
    out = []
    if len(idx) == 0:
        return out
    start = prev = idx[0]
    for i in idx[1:]:
        if i - prev > min_gap:
            out.append((start, prev))
            start = i
        prev = i
    out.append((start, prev))
    return out


def band_report(name, a, y0, y1, x0=60, x1=240, mode="dark"):
    m = dark(a) if mode == "dark" else redish(a) if mode == "red" else blueish(a)
    col = m[y0:y1, x0:x1].sum(axis=0)
    cl = clusters(col > 0, min_gap=3)
    print(f"{name} y{y0}-{y1} x{x0}-{x1} [{mode}]: {len(cl)} clusters at x:",
          [f"{x0+c0}-{x0+c1}" for c0, c1 in cl])
    return cl


print("\n=== ORIGINAL slide_041.jpg ===")
# header row (x_i labels): band y58-73
band_report("ORIG headers", o, 58, 73)
# paren pairs / column ink: band y78-110 (vectors)
cl = band_report("ORIG vector band", o, 78, 110)
# class row y108-124: red and blue separately
band_report("ORIG class RED", o, 108, 124, mode="red")
band_report("ORIG class BLUE", o, 108, 124, mode="blue")
# per-column digit ink in vector band to detect column count independent of parens
col = dark(o)[76:112, 60:240].sum(axis=0)
print("ORIG per-x ink in y76-112 (nonzero runs):")
for c0, c1 in clusters(col > 0, min_gap=4):
    print(f"   x{60+c0}-{60+c1} ink={int(col[c0:c1+1].sum())}")

print("\n=== RENDER downsampled to 960x540 ===")
band_report("REN headers", r, 58, 73)
band_report("REN vector band", r, 78, 110)
band_report("REN class RED", r, 108, 124, mode="red")
band_report("REN class BLUE", r, 108, 124, mode="blue")

print("\n=== Claim 1 detailed: original header subscripts (digits after x) ===")
# header glyph band: for each expected header center, look at ink in y58-73
for cx in [96.5, 118, 140, 163, 185.5, 208]:
    band = dark(o)[58:73, int(cx) - 8:int(cx) + 8]
    print(f"  orig header near x={cx}: ink px = {int(band.sum())}")

print("\n=== Claim 1 detailed: original class label colors per column center ===")
for cx in [96.5, 118, 140, 163, 185.5, 208]:
    reg_r = redish(o)[108:124, int(cx) - 9:int(cx) + 9]
    reg_b = blueish(o)[108:124, int(cx) - 9:int(cx) + 9]
    reg_d = dark(o)[108:124, int(cx) - 9:int(cx) + 9]
    print(f"  orig class near x={cx}: red={int(reg_r.sum())} blue={int(reg_b.sum())} dark={int(reg_d.sum())}")

print("\n=== Claim 2: W-vector delimiter glyphs in ORIGINAL (x~328-356, y58-106) ===")
# left delimiter around x330.5, right around x352.5. Check bow vs serif:
# for each glyph column band, print per-row min/max ink x to see shape
def glyph_shape(a, x0, x1, y0, y1, label):
    m = dark(a)[y0:y1, x0:x1]
    print(f"  {label}: rows y{y0}-{y1}, ink x-range per 6-row slice (relative to x{x0}):")
    for yy in range(0, m.shape[0], 6):
        row = m[yy:yy + 6]
        xs = np.where(row.any(axis=0))[0]
        if len(xs):
            print(f"    y{y0+yy}-{y0+yy+5}: ink x {x0+xs.min()}..{x0+xs.max()} (w={xs.max()-xs.min()+1})")
        else:
            print(f"    y{y0+yy}-{y0+yy+5}: no ink")

glyph_shape(o, 326, 336, 56, 108, "ORIG left delim")
glyph_shape(o, 348, 358, 56, 108, "ORIG right delim")

print("\n=== Claim 2: same in RENDER ===")
glyph_shape(r, 326, 336, 56, 108, "REN left delim")
glyph_shape(r, 348, 358, 56, 108, "REN right delim")

# quantitative bow test: for a paren '(' the leftmost ink x at top/bottom rows is
# LARGER (indented) than at mid rows; for '[' top/bottom rows extend LEFT (serif).
def bow_test(a, x0, x1, y0, y1, label):
    m = dark(a)[y0:y1, x0:x1]
    H = m.shape[0]
    top = np.where(m[: H // 4].any(axis=0))[0]
    mid = np.where(m[H // 2 - 3: H // 2 + 4].any(axis=0))[0]
    bot = np.where(m[-H // 4:].any(axis=0))[0]
    if len(top) and len(mid) and len(bot):
        print(f"  {label}: leftmost-ink top={x0+top.min()} mid={x0+mid.min()} bottom={x0+bot.min()}"
              f"  (paren: top/bottom > mid-left; bracket '[': top/bottom <= mid-left, plus wide top/bottom rows)")
        tw = top.max() - top.min() + 1
        mw = mid.max() - mid.min() + 1
        bw = bot.max() - bot.min() + 1
        print(f"    row widths: top={tw} mid={mw} bottom={bw}  (bracket: top/bottom width >> mid)")

bow_test(o, 326, 336, 56, 108, "ORIG left delim")
bow_test(o, 348, 358, 56, 108, "ORIG right delim")
bow_test(r, 326, 336, 56, 108, "REN left delim")
bow_test(r, 348, 358, 56, 108, "REN right delim")

print("\n=== Table-region diff render-vs-orig (slide space) ===")
d = np.abs(r - o).sum(axis=2)
mask = d > 90
reg = mask[50:135, 60:730]
print(f"cream-box region y50-135 x60-730: diff px = {int(reg.sum())} of {reg.size} ({100*reg.sum()/reg.size:.2f}%)")
# where in the table band are diffs concentrated?
for x0 in range(60, 240, 20):
    sub = mask[54:130, x0:x0 + 20]
    print(f"  x{x0}-{x0+20} y54-130 diff px = {int(sub.sum())}")
