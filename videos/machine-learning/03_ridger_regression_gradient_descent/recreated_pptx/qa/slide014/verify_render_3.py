#!/usr/bin/env python3
"""Verify render_2.png against the original: ink presence in every region,
band fill colors, and inset gaps from the C00000 strokes.

Frame space is 960x540 (1px = 1pt); render is 2001x1125 at 150dpi.
scale = 1125/540 ≈ 2.0833 render-px per frame-px.
"""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/"
NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"

rv = np.asarray(Image.open(QA + "render_2.png").convert("RGB")).astype(int)
og = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)
H, W = rv.shape[:2]
sc = W / 960.0
print(f"render {rv.shape}, original {og.shape}, scale {sc:.4f}")


def ink_rows(img, scale, x0, y0, x1, y1, thresh=30):
    """Count non-white pixels per row in a frame-space band -> list per row."""
    a = img[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    prof = (np.abs(a - 255).max(axis=2) > thresh)
    return prof.sum(axis=1)


def band_ink(name, x0, y0, x1, y1):
    rows = ink_rows(rv, sc, x0, y0, x1, y1)
    tot = int(rows.sum())
    nz = int((rows > 0).sum())
    print(f"  {name:26s} ({x0},{y0})-({x1},{y1}): ink px={tot:6d} rows-with-ink={nz}")
    return tot, nz


print("\n=== RENDER-2 ink presence per region (frame px space) ===")
regions = [
    ("title",              70,  60, 700,  95),
    ("vecbox_left_text",   60, 120, 440, 225),
    ("vecbox_right_text", 500, 120, 890, 225),
    ("ridge_band_text",    70, 252, 890, 275),
    ("objective_band",     70, 312, 890, 332),
    ("define_loss_band",   70, 398, 890, 418),
    ("loss_term_box",      60, 470, 440, 515),
    ("reg_term_box",      500, 470, 890, 515),
    ("final_band",         70, 512, 890, 522),
]
allpresent = True
for n, x0, y0, x1, y1 in regions:
    tot, nr = band_ink(n, x0, y0, x1, y1)
    if tot < 200:
        allpresent = False
print(f"ALL REGIONS HAVE INK: {allpresent}")

print("\n=== ORIGINAL ink presence per same regions ===")
for n, x0, y0, x1, y1 in regions:
    band_ink("[orig] " + n, x0, y0, x1, y1)

print("\n=== Band fills in render (dominant non-white color) ===")
def fillcolor(name, x0, y0, x1, y1):
    a = rv[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)].reshape(-1, 3)
    # most common quantized color
    q = (a // 8) * 8
    keys, counts = np.unique(q, axis=0, return_counts=True)
    top = keys[counts.argmax()] + 4
    print(f"  {name:26s} dominant #{top[0]:02X}{top[1]:02X}{top[2]:02X} "
          f"({counts.max()}/{len(a)} = {counts.max()/len(a)*100:.0f}%)")
    return top

print("render:")
f1 = fillcolor("ridge_band",   200, 254, 600, 270)
f2 = fillcolor("objective",    200, 314, 600, 330)
f3 = fillcolor("define_loss",  200, 400, 600, 416)
f4 = fillcolor("final_band",   200, 513, 600, 521)
print("original:")
fillcolor("[orig] ridge_band",   200, 254, 600, 270)
fillcolor("[orig] objective",    200, 314, 600, 330)
fillcolor("[orig] define_loss",  200, 400, 600, 416)
fillcolor("[orig] final_band",   200, 513, 600, 521)

print("\n=== Insets: band extents vs red strokes (frame px) ===")
red = (rv[:, :, 0] > 90) & ((rv[:, :, 0] - rv[:, :, 1]) > 30) & ((rv[:, :, 0] - rv[:, :, 2]) > 30)
def strokecols(y_frame):
    row = red[int(y_frame * sc), :]
    cols = np.where(row)[0]
    return (int(cols.min()/sc), int(cols.max()/sc)) if len(cols) else None
for yf in (260, 320, 405, 517):
    print(f"  red stroke cols at y={yf}: {strokecols(yf)} (expected L~58.5 R~901)")

# band left/right extents for the full-width bands
def fillcols(y_frame, name):
    a = rv[int(y_frame*sc), :]
    # non-white
    nz = np.where(np.abs(a - 255).max(axis=1) > 25)[0]
    if len(nz):
        print(f"  {name} band at y={yf if False else y_frame}: x {nz.min()/sc:.1f}..{nz.max()/sc:.1f}")
    else:
        print(f"  {name}: no fill")
for yfr, nm in ((260, "ridge"), (320, "objective"), (405, "define_loss"), (517, "final")):
    fillcols(yfr, nm)

print("\n=== Bottom stroke / band gap ===")
redrows = np.where(red.sum(axis=1) > 200)[0]
print(f"  bottom-most red row: {redrows.max()/sc:.1f} frame px")
fin = rv[int(517*sc):int(521*sc), :]
nzr = np.where(np.abs(fin - 255).max(axis=2) > 10)[0]
print(f"  final band rows {nzr.min()/sc:.1f}..{nzr.max()/sc:.1f}" if len(nzr) else "  no final band")
