#!/usr/bin/env python3
"""Independent per-region ink measurement for the ORIGINAL frame
(no shared variables with the render measurement)."""
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"

ORIG = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)
print("orig shape", ORIG.shape)

def ink(x0, y0, x1, y1, thresh=30):
    a = ORIG[y0:y1, x0:x1]
    prof = (np.abs(a - 255).max(axis=2) > thresh)
    return int(prof.sum()), int((prof.sum(axis=1) > 0).sum())

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
print("=== ORIGINAL ink per region ===")
for n, x0, y0, x1, y1 in regions:
    t, r = ink(x0, y0, x1, y1)
    print(f"  {n:26s} ink={t:6d} rows={r}")

print("\n=== ORIGINAL: row-profile of full width, find all bands (y 40..540) ===")
nz = (np.abs(ORIG - 255).max(axis=2) > 12)
rowcount = nz.sum(axis=1)
prev = 0
for y in range(40, 540):
    c = rowcount[y]
    state = "BAND" if c > 400 else ("text" if c > 20 else "empty")
    if (state == "BAND") != (prev == "BAND"):
        print(f"  y={y}: -> {state} (count {c})")
    prev = state

print("\n=== ORIGINAL: dominant fill color per band ===")
def dom(y0, y1, x0=200, x1=600):
    a = ORIG[y0:y1, x0:x1].reshape(-1, 3)
    q = (a // 8) * 8
    keys, counts = np.unique(q, axis=0, return_counts=True)
    top = keys[counts.argmax()] + 4
    print(f"  y {y0}..{y1}: #{top[0]:02X}{top[1]:02X}{top[2]:02X} ({counts.max()/len(a)*100:.0f}%)")
    return top
dom(254, 270)   # ridge
dom(314, 330)   # objective
dom(400, 416)   # define loss
dom(513, 521)   # final
dom(255, 268)   # ridge alt

print("\n=== ORIGINAL: exact band left/right extents ===")
for yf, nm in ((260, "ridge"), (320, "objective"), (405, "define_loss"), (517, "final")):
    row = nz[yf, :]
    cols = np.where(row)[0]
    print(f"  {nm:11s} y={yf}: x {cols.min()}..{cols.max()}" if len(cols) else f"  {nm}: none")

print("\n=== ORIGINAL: red stroke columns ===")
red = (ORIG[:, :, 0] > 90) & ((ORIG[:, :, 0] - ORIG[:, :, 1]) > 30) & ((ORIG[:, :, 0] - ORIG[:, :, 2]) > 30)
for yf in (60, 100, 260, 320, 405, 500, 517, 535):
    row = red[yf, :]
    cols = np.where(row)[0]
    print(f"  y={yf}: red cols {cols.min()}..{cols.max()}" if len(cols) else f"  y={yf}: no red")
redrows = np.where(red.sum(axis=1) > 100)[0]
print(f"  red rows {redrows.min()}..{redrows.max()}")

print("\n=== ORIGINAL: title ink rows/cols ===")
t = nz[55:100, 60:720]
rows = np.where(t.sum(axis=1) > 0)[0]
cols = np.where(t.sum(axis=0) > 0)[0]
print(f"  title rows 55+{rows.min()}..55+{rows.max()}; cols 60+{cols.min()}..60+{cols.max()}")
# title color split
tb = ORIG[55:100, 60:720]
blue = (tb[:, :, 2] > 100) & (tb[:, :, 2] - tb[:, :, 0] > 40)
print(f"  title blue px {blue.sum()}, black px {(tb.max(axis=2)<80).sum()}")
