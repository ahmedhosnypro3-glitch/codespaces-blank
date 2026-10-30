#!/usr/bin/env python3
"""Compact rebuild-geometry extraction for slide 014 from the ORIGINAL frame.
Answers: (1) vector-box x extents + border/fill colour, (2) ridge band line
count, (3) term-box extents/baselines, (4) final band extent+fill."""
import numpy as np
from PIL import Image

NS = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/")
OG = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)
H, W = OG.shape[:2]


def hexc(px):
    return "#%02X%02X%02X" % tuple(int(v) for v in px)


print("=== (1) VECTOR BOXES: column-scan for vertical borders in y150..225 ===")
# a vertical border column shows near-constant colour and many dark/coloured px
for x in range(52, 920, 2):
    col = OG[150:226, x]
    ink = (np.abs(col - 255).max(axis=1) > 30).sum()
    if ink > 60:
        c = col.mean(axis=0).astype(int)
        print(f"  x={x:4d} inkpx={ink:3d} avg={hexc(c)}")

print("\n=== (2) RIDGE BAND y246..284: text line count in x70..890 ===")
nz = (np.abs(OG - 255).max(axis=2) > 30)
prof = nz[246:285, 70:890].sum(axis=1)
runs=[];cur=None
for i, c in enumerate(prof):
    if c >= 6:
        if cur is None: cur=[246+i,246+i]
        else: cur[1]=246+i
    else:
        if cur: runs.append(tuple(cur)); cur=None
if cur: runs.append(tuple(cur))
print(f"  ridge-band text line runs: {runs}")
print(f"  => {len(runs)} text line(s)")

print("\n=== (3) TERM BOXES y455..525: row extents of non-panel ink ===")
panelish = (np.abs(OG[:, :, :] - np.array([233, 233, 231])).max(axis=2) < 14)
ink = ~panelish & (np.abs(OG - 255).max(axis=2) > 12)
for y in range(452, 528, 4):
    row = ink[y, 60:900]
    cols = np.where(row)[0]
    if len(cols) > 20:
        print(f"  y={y:3d} x {60+cols.min():3d}..{60+cols.max():3d} n={len(cols)}")

print("\n=== (4) FINAL BAND: fill colour at text-free x,y + extent ===")
print(f"  sample (700,516) = {hexc(OG[516,700])}, (300,518)={hexc(OG[518,300])}, (60,516)={hexc(OG[516,60])}")
print(f"  sample ridge (700,255) = {hexc(OG[255,700])}")
print(f"  sample objective (700,295) = {hexc(OG[295,700])}")
print(f"  sample define-loss (700,322) = {hexc(OG[322,700])}")
print(f"  sample loss-term box (400,470) = {hexc(OG[470,400])}")
print(f"  sample reg-term box (700,470) = {hexc(OG[470,700])}")
print(f"  sample left vecbox interior (200,150) = {hexc(OG[150,200])}")
print(f"  sample left vecbox border (433,150) = {hexc(OG[150,433])}")
print(f"  sample right vecbox interior (600,150) = {hexc(OG[150,600])}")
print(f"  sample right vecbox border (456,150) = {hexc(OG[150,456])}")
print(f"  left vecbox top-left corner (82,101) = {hexc(OG[101,82])}")
