#!/usr/bin/env python3
"""PIL adjudication of the five attempt-2 findings against BOTH images.

Measures unique_slides/slide_012.jpg (960x540, 1px=1pt) against
qa/slide012/render_2.png (2001x1125, 150dpi) — regions are converted from frame
px to render px by SCALE = 2001/960 before every comparison.
"""
import sys
from PIL import Image
import numpy as np

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_012.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide012/render_2.png"

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
ow, oh = o.size
rw, rh = r.size
S = rw / ow
print(f"original {o.size}  render {r.size}  SCALE={S:.4f}")


def box(img, x0, y0, x1, y1, scale=1.0):
    a = np.asarray(img).astype(int)
    return a[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]


def med(a):
    return tuple(int(v) for v in np.median(a.reshape(-1, 3), axis=0))


def ink_frac(a, bg):
    """fraction of pixels whose distance from bg exceeds 60"""
    d = np.abs(a - np.array(bg)).sum(axis=2)
    return float((d > 60).mean())


print("\n" + "=" * 74)
print("FINDING 1 (MAJOR): outlier label text 'X5 is Outlier' verbatim")
print("=" * 74)
for name, (y0, y1) in (("is-Outlier #1", (323, 349)), ("is-Outlier #2", (445, 471))):
    ob = box(o, 69, y0, 196, y1)
    rb = box(r, 69, y0, 196, y1, S)
    # white text on a red box: count white-ish ink
    ow_w = (np.abs(ob - 255).sum(axis=2) < 60)
    rw_w = (np.asarray(r).astype(int)[int(y0*S):int(y1*S), int(69*S):int(196*S)])
    rw_white = (np.abs(rw_w - 255).sum(axis=2) < 60)
    ys, xs = np.nonzero(ow_w)
    ar = {"render": None}
    if len(xs):
        # text ink bbox in the ORIGINAL, in frame px
        print(f"{name}: ORIGINAL white-ink px={ow_w.sum():5d}  bbox x{69+xs.min()}..{69+xs.max()} "
              f"y{y0+ys.min()}..{y0+ys.max()}  (w={xs.max()-xs.min()+1}, h={ys.max()-ys.min()+1})")
    else:
        print(f"{name}: ORIGINAL no white ink found")
    print(f"{name}: RENDER   white-ink px={rw_white.sum():5d}  box fill median={med(rb)}")
print("-> render text is the literal string 'X5 is Outlier' (verified in ppt/slides/slide1.xml,")
print("   2 occurrences). The original's 960x540 glyphs are at the noise floor for a")
print("   per-character read; both judges (attempt 2 full-slide + crop judge) read 'X5'")
print("   with high confidence and gave a coherent semantic account.")

print("\n" + "=" * 74)
print("FINDING 2 (MINOR): 'Test Data' label — unfilled text vs solid box")
print("=" * 74)
ob = box(o, 767, 96, 866, 125)
rb = box(r, 767, 96, 866, 125, S)
print(f"ORIGINAL  region median RGB={med(ob)}   ink frac vs own median={ink_frac(ob, med(ob)):.3f}")
print(f"RENDER    region median RGB={med(rb)}   ink frac vs own median={ink_frac(rb, med(rb)):.3f}")
# per-column scan of the ORIGINAL: is there a solid rectangle (a constant fill)?
ocol = ob.reshape(ob.shape[0], -1, 3)
col_std = ocol.std(axis=(0, 2))
print(f"ORIGINAL  per-column std over rows: min={col_std.min():.1f} max={col_std.max():.1f} "
      f"mean={col_std.mean():.1f}")
print("-> low per-column std over rows = a uniform filled rect dominates;")
print("   a bare caption on the gray panel would show large std where glyphs sit.")
rcol = (np.asarray(r).astype(int)[int(96*S):int(125*S), int(767*S):int(866*S)])
print(f"RENDER    per-column std over rows: min={rcol.std(axis=(0,2)).min():.1f} "
      f"max={rcol.std(axis=(0,2)).max():.1f} mean={rcol.std(axis=(0,2)).mean():.1f}")

print("\n" + "=" * 74)
print("FINDING 3 (MINOR): test-table colour scheme (y-row red, headers greenish)")
print("=" * 74)
# original test table v-grid 719,770,821,871 ; h-grid 128,160,190,221,252
TX = [719, 770, 821, 871]
TY = [128, 160, 190, 221, 252]
names = [["Test1", "Test2", "Test3"], ["30", "40", "50"], ["15", "20", "25"], ["60", "80", "100"]]
print("ORIGINAL cell ink (median colour of non-background pixels in each cell):")
for ri in range(4):
    row = []
    for ci in range(3):
        y0, y1 = TY[ri], TY[ri + 1]
        x0, x1 = TX[ci], TX[ci + 1]
        c = box(o, x0 + 3, y0 + 3, x1 - 3, y1 - 3)
        flat = c.reshape(-1, 3)
        bg = np.median(flat, axis=0)
        d = np.abs(flat - bg).sum(axis=1)
        inkp = flat[d > 90]
        row.append(f"{names[ri][ci]}={tuple(int(v) for v in inkp.mean(axis=0)) if len(inkp) else '-'}")
    print("   " + "  ".join(row))
print("RENDER cell ink (same cells, scaled by S):")
for ri in range(4):
    row = []
    for ci in range(3):
        y0, y1 = TY[ri], TY[ri + 1]
        x0, x1 = TX[ci], TX[ci + 1]
        c = box(r, x0 + 3, y0 + 3, x1 - 3, y1 - 3, S)
        flat = c.reshape(-1, 3)
        bg = np.median(flat, axis=0)
        d = np.abs(flat - bg).sum(axis=1)
        inkp = flat[d > 90]
        row.append(f"{names[ri][ci]}={tuple(int(v) for v in inkp.mean(axis=0)) if len(inkp) else '-'}")
    print("   " + "  ".join(row))

print("\n" + "=" * 74)
print("FINDING 4 (MINOR): cell fill tint (white vs faint green-grey)")
print("=" * 74)
for nm, (y0, y1) in (("orig cell (X1 row, col1)", (TY[1], TY[2])),):
    c = box(o, TX[1] + 4, y0 + 4, TX[2] - 4, y1 - 4)
    print(f"{nm}: ORIGINAL cell median RGB={med(c)}")
# training-table cell, x203..571 9 cols; row 1 of T1 (y158..189)
TC = [203, 244, 285, 326, 367, 407, 448, 489, 529, 571]
c = box(o, TC[1] + 4, 158 + 4, TC[2] - 4, 189 - 4)
print(f"orig train cell (T1 row1 col1): ORIGINAL median RGB={med(c)}")
c2 = box(r, TC[1] + 4, 158 + 4, TC[2] - 4, 189 - 4, S)
print(f"orig train cell (T1 row1 col1): RENDER   median RGB={med(c2)}")

print("\n" + "=" * 74)
print("FINDING 5 (MINOR): arrow anchor near the X6/X7 header area")
print("=" * 74)
for nm, img, sc in (("ORIGINAL", o, 1.0), ("RENDER", r, S)):
    a = np.asarray(img).astype(int)
    # red-ish mask: high R, low G/B
    m = (a[:, :, 0] > 150) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    y0, y1 = int(255 * sc), int(405 * sc)
    x0, x1 = int(575 * sc), int(710 * sc)
    sub = m[y0:y1, x0:x1]
    print(f"{nm}: red px in gap x575..710 y255..405 = {sub.sum()}")
    if sub.sum():
        ys, xs = np.nonzero(sub)
        print(f"    red bbox x{575 + xs.min()/sc:.0f}..{575 + xs.max()/sc:.0f} "
              f"y{255 + ys.min()/sc:.0f}..{255 + ys.max()/sc:.0f} (frame px)")
    # where is the second table's right edge & the callout's left edge?
    rm = (a[:, :, 0] > 150) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    band = rm[int(265 * sc):int(404 * sc), :]
    cols = np.nonzero(band.any(axis=0))[0]
    if len(cols):
        # leftmost/rightmost red column in the middle-table band (excludes the red label rail)
        print(f"    red cols present in band y265..404: x{cols.min()/sc:.0f}..{cols.max()/sc:.0f} (frame px)")
