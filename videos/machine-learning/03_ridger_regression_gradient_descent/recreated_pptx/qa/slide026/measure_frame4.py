#!/usr/bin/env python3
"""Pass-4: raw underline bar extents + sensitive title band + row C color boundary.
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_026.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red_ink = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
blue_ink = (b > 90) & ((b - r) > 40) & ((b - g) > 40)
# sensitive blue: any strong-blue-ish (b-r>25)
blue_soft = (b > 80) & ((b - r) > 25) & ((b - g) > 25)
red_soft = (r > 80) & ((r - g) > 25) & ((r - b) > 5)
dark_soft = im.sum(axis=2) < 420

print("== ROW B bar zone: rows 189..198, x 340..580 — soft-blue runs ==")
for yy in range(189, 199):
    row = blue_soft[yy, 340:580]
    idx = np.where(row)[0]
    if not len(idx):
        continue
    rr = []
    s0 = p0 = idx[0]
    for i in idx[1:]:
        if i > p0 + 1:
            rr.append((s0, p0)); s0 = i
        p0 = i
    rr.append((s0, p0))
    desc = ", ".join(f"{a+340}-{c+340}({row[a:c+1].mean():.2f})" for a, c in rr)
    print(f"  y{yy}: {desc}")

print("\n== ROW B bar zone: same rows x 560..860 (check any bar extension right) ==")
for yy in range(189, 199):
    row = blue_soft[yy, 560:860]
    idx = np.where(row)[0]
    if not len(idx):
        continue
    rr = []
    s0 = p0 = idx[0]
    for i in idx[1:]:
        if i > p0 + 1:
            rr.append((s0, p0)); s0 = i
        p0 = i
    rr.append((s0, p0))
    desc = ", ".join(f"{a+560}-{c+560}({row[a:c+1].mean():.2f})" for a, c in rr if (c-a+1) >= 8)
    print(f"  y{yy}: {desc}")

print("\n== ROW D bar zone: rows 254..264, x 280..480 — soft-blue runs ==")
for yy in range(254, 265):
    row = blue_soft[yy, 280:480]
    idx = np.where(row)[0]
    if not len(idx):
        continue
    rr = []
    s0 = p0 = idx[0]
    for i in idx[1:]:
        if i > p0 + 1:
            rr.append((s0, p0)); s0 = i
        p0 = i
    rr.append((s0, p0))
    desc = ", ".join(f"{a+280}-{c+280}({row[a:c+1].mean():.2f})" for a, c in rr)
    print(f"  y{yy}: {desc}")

print("\n== N3 bar zone: rows 452..466, x 100..840 — soft-dark runs (w>=20) ==")
for yy in range(452, 467):
    row = dark_soft[yy, 100:840]
    idx = np.where(row)[0]
    if not len(idx):
        continue
    rr = []
    s0 = p0 = idx[0]
    for i in idx[1:]:
        if i > p0 + 1:
            rr.append((s0, p0)); s0 = i
        p0 = i
    rr.append((s0, p0))
    desc = ", ".join(f"{a+100}-{c+100}({row[a:c+1].mean():.2f})" for a, c in rr if (c-a+1) >= 20)
    print(f"  y{yy}: {desc}")

print("\n== TITLE sensitive band (ink = dist from gray(233,233,231) > 20), x 280..650 ==")
bg = np.array([233, 233, 231])
ink = np.abs(im - bg).max(axis=2) > 20
for yy in range(50, 95):
    cnt = ink[yy, 280:650].sum()
    if cnt > 0:
        print(f"  y{yy}: {cnt} ink px")

# title: check color under ink — confirm all-red (no black parts)
print("\n== TITLE color composition per word run ==")
for (a, c) in [(294, 407), (415, 522), (531, 639)]:
    win = (slice(55, 90), slice(a, c + 1))
    rc = red_ink[win].sum(); bc = blue_ink[win].sum(); dc = dark_soft[win].sum()
    print(f"  word x {a}-{c}: red={rc} blue={bc} dark={dc}")

print("\n== ROW C red boundary: first/last red-classified columns (strict) ==")
win = (slice(205, 236), slice(400, 700))
prof = red_soft[win].sum(axis=0)
cols = np.where(prof > 0)[0]
if len(cols):
    print(f"  red cols x {cols.min()+400}..{cols.max()+400}")
    # find transition: print columns 500..530 profile
    for x in range(505, 530):
        print(f"    x{x}: red={red_soft[205:236, x].sum()} blue={blue_soft[205:236, x].sum()}")

print("\n== check for ink between rows (any missed lines) — box interior full census, threshold 20 ==")
prof = ink[:, 85:861].sum(axis=1)
prev = False
for y in range(93, 497):
    cur = prof[y] > 2
    if cur and not prev:
        y0 = y
    if prev and not cur:
        print(f"  ink band y {y0}-{y-1} (h={y-y0})")
    prev = cur
if prev:
    print(f"  ink band y {y0}-496")
