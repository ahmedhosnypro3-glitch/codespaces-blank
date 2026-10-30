#!/usr/bin/env python3
"""Slide 030: PIL adjudication of the two MAJOR findings in judge_attempt_6.txt
(worker w030-finish-20261024c).

MAJOR #1 "missing X column header": the judge says the main table's first header
cell is EMPTY in the recreation and contains an italic "X" in the original.
MAJOR #2 "title font family/size/left offset": the judge says the original's
title is bold serif at cap height ~22 px starting x~75, and the recreation's is
bold sans at cap ~17 px starting x~54.

Both are decided here by pixel evidence, not by opinion:
  - the house left stroke (a full-height red column) is removed before the
    title's text start is measured, otherwise it masquerades as the title's
    first glyph;
  - every region is printed as a one-character-per-frame-pixel ASCII map so the
    glyph itself (x vs X, serif vs sans) is visible.
"""
import numpy as np
from PIL import Image

V = "videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide030"

rend = np.asarray(Image.open(f"{Q}/render_6.png").convert("RGB")).astype(int)
orig = np.asarray(Image.open(f"{V}/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
SXR, SYR = 2001 / 960.0, 1125 / 540.0


def to_frames(im, sx, sy, box):
    x0, y0, x1, y1 = box
    X0, Y0, X1, Y1 = int(round(x0 * sx)), int(round(y0 * sy)), int(round(x1 * sx)), int(round(y1 * sy))
    sub = im[Y0:Y1, X0:X1].astype(float)
    h, w = sub.shape[:2]
    fh, fw = int(round(h / sy)), int(round(w / sx))
    out = np.zeros((fh, fw, 3))
    for i in range(fh):
        for j in range(fw):
            ys = slice(int(round(i * sy)), max(int(round((i + 1) * sy)), int(round(i * sy)) + 1))
            xs = slice(int(round(j * sx)), max(int(round((j + 1) * sx)), int(round(j * sx)) + 1))
            out[i, j] = sub[ys, xs].reshape(-1, 3).mean(axis=0)
    return out


def redish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r - g > 60) & (r - b > 40) & (r > 110)


def greenish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (g - r > 40) & (g - b > 40) & (g > 100)


def darkish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r < 120) & (g < 120) & (b < 120)


def ascii_map(a, mask, x0):
    rows = []
    for i in range(mask.shape[0]):
        rows.append("".join("#" if mask[i, j] else " " for j in range(mask.shape[1])))
    return rows


print("=" * 100)
print("MAJOR #1 — main table, first header cell (label column), frame px x89..152, y332..358")
print("=" * 100)
for label, im, sx, sy in (("render", rend, SXR, SYR), ("orig", orig, 1.0, 1.0)):
    sub = to_frames(im, sx, sy, (89, 332, 152, 358)).astype(int)
    dm = darkish(sub)
    print(f"-- {label}: dark ink px in the cell = {int(dm.sum())}")
    for i, row in enumerate(ascii_map(sub, dm, 89)):
        print(f"   y={332+i:3d} |{row}|")

print()
print("=" * 100)
print("MAJOR #2 — title band, frame px x52..620, y52..104 (house stroke removed)")
print("=" * 100)
for label, im, sx, sy in (("render", rend, SXR, SYR), ("orig", orig, 1.0, 1.0)):
    # full-height band to identify the house stroke columns
    tall = to_frames(im, sx, sy, (50, 45, 620, 300)).astype(int)
    tm = redish(tall) | greenish(tall)
    colcount = tm.sum(axis=0)
    stroke_cols = [50 + j for j, n in enumerate(colcount) if n > 0.5 * tall.shape[0]]
    band = to_frames(im, sx, sy, (50, 52, 620, 104)).astype(int)
    bm = redish(band) | greenish(band) | darkish(band)
    bm[:, [c - 50 for c in stroke_cols if 50 <= c < 620]] = False
    cols = bm.sum(axis=0)
    first = next((50 + j for j, n in enumerate(cols) if n >= 3), None)
    rows = bm.sum(axis=1)
    trows = [52 + i for i, n in enumerate(rows) if n >= 3]
    print(f"-- {label}: house stroke columns removed = {stroke_cols}")
    print(f"   title text ink start x = {first}   ink rows y = {trows[0] if trows else None}..{trows[-1] if trows else None}")
    if first is not None:
        # cap height of the first capital letter (first 22 px of the text run)
        cap = bm[:, first - 50:first - 50 + 22]
        cr = cap.sum(axis=1)
        caprows = [52 + i for i, n in enumerate(cr) if n >= 2]
        print(f"   first-letter ink rows (cap height) = {caprows[0] if caprows else None}..{caprows[-1] if caprows else None}"
              f"  -> cap height {caprows[-1]-caprows[0]+1 if caprows else 0} frame px")
        print("   first 24 px of the title, one char per frame px:")
        for i in range(bm.shape[0]):
            print(f"     y={52+i:3d} |{''.join('#' if bm[i,j] else ' ' for j in range(min(24, bm.shape[1])))}|")

print()
print("=" * 100)
print("Title: total text ink bbox (stroke removed) + per-column profile, first 140 px")
print("=" * 100)
for label, im, sx, sy in (("render", rend, SXR, SYR), ("orig", orig, 1.0, 1.0)):
    tall = to_frames(im, sx, sy, (50, 45, 620, 300)).astype(int)
    tm = redish(tall) | greenish(tall)
    colcount = tm.sum(axis=0)
    stroke_cols = [50 + j for j, n in enumerate(colcount) if n > 0.5 * tall.shape[0]]
    band = to_frames(im, sx, sy, (50, 52, 620, 104)).astype(int)
    bm = redish(band) | greenish(band) | darkish(band)
    bm[:, [c - 50 for c in stroke_cols if 50 <= c < 620]] = False
    ys, xs = np.where(bm)
    if len(xs):
        x0f, x1f = 50 + xs.min(), 50 + xs.max()
        y0f, y1f = 52 + ys.min(), 52 + ys.max()
        print(f"-- {label}: title text bbox frame px = ({x0f},{y0f})-({x1f},{y1f})  width={x1f-x0f+1} height={y1f-y0f+1}")
        prof = [(50 + j, int(n)) for j, n in enumerate(bm.sum(axis=0)) if n >= 3]
        print("   ink columns (x:count): " + " ".join(f"{x}:{n}" for x, n in prof[:40]))
print("\nTITLE/TABLE ADJUDICATION DATA DONE")
