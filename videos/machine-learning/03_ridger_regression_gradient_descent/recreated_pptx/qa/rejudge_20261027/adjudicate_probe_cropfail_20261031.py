#!/usr/bin/env python3
"""Targeted PIL probes for the 2026-10-31 newest-clean CROP-FAIL adjudication.
Usage: adjudicate_probe_cropfail_20261031.py <NNN> <claim>
Read-only. Prints measurements used to confirm/refute each judge claim.
"""
import sys
import numpy as np
from PIL import Image

RJ = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027"
S = sys.argv[1]
CLAIM = sys.argv[2]
r = np.asarray(Image.open(f"{RJ}/slide{S}/crop_dense_render.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{RJ}/slide{S}/crop_dense_orig.png").convert("RGB")).astype(int)
if r.shape != o.shape:
    o = np.asarray(Image.fromarray(o.astype(np.uint8)).resize((r.shape[1], r.shape[0]), Image.LANCZOS)).astype(int)
H, W = r.shape[:2]
print(f"slide {S} claim={CLAIM} crop {W}x{H}")

def red(a):   return (a[:,:,0] > 110) & (a[:,:,0] - a[:,:,1] > 50) & (a[:,:,0] - a[:,:,2] > 50)
def blue(a):  return (a[:,:,2] > 110) & (a[:,:,2] - a[:,:,0] > 40) & (a[:,:,2] - a[:,:,1] > 30)
def dark(a):  return a.sum(axis=2) < 450
def grayish(a):
    m = (np.abs(a[:,:,0]-a[:,:,1]) < 22) & (np.abs(a[:,:,1]-a[:,:,2]) < 22)
    return m & (a.sum(axis=2) > 240) & (a.sum(axis=2) < 660)

def ascii_art(a, x0, y0, x1, y1, mask):
    for y in range(y0, y1, 2):
        line = "".join("#" if mask[y, x] else "." for x in range(x0, x1, 1))
        print(f"{y:4d} {line}")

if CLAIM == "003_xcolor":
    # claim: X glyphs red in render, dark in original, equation line upper-center
    for name, a in (("RENDER", r), ("ORIG", o)):
        rm, bm, dm = red(a), blue(a), dark(a)
        print(f"{name}: red px total={rm.sum()} (upper half={rm[:H//2].sum()}), blue={bm.sum()}, dark={dm.sum()}")
        rows = rm.sum(axis=1)
        top = np.argsort(rows)[-6:][::-1]
        print(f"  red rows with most ink: {[(int(t), int(rows[t])) for t in top]}")
    # where render is red, what is original?
    both_red_r = red(r)
    orig_at = o[both_red_r]
    if len(orig_at):
        print(f"orig color where render red: mean RGB = {orig_at.mean(axis=0).round(1)}")
    orig_red = red(o)
    rend_at = r[orig_red]
    if len(rend_at):
        print(f"render color where orig red: mean RGB = {rend_at.mean(axis=0).round(1)}")

elif CLAIM == "008_trunc":
    # claim: blue 2nd line in render stops at 'regular', orig continues 'iz...'
    for name, a in (("RENDER", r), ("ORIG", o)):
        bm = blue(a)
        ys, xs = np.where(bm)
        print(f"{name}: blue px={bm.sum()}", end=" ")
        if len(xs):
            print(f"x range {xs.min()}-{xs.max()}, y range {ys.min()}-{ys.max()}")
        else:
            print()
        # restrict to lower half (the blue line)
        low = bm[H//2:, :]
        ys2, xs2 = np.where(low)
        if len(xs2):
            print(f"  lower-half blue: x {xs2.min()}-{xs2.max()} px={low.sum()} rows {ys2.min()+H//2}-{ys2.max()+H//2}")

elif CLAIM == "015_jglyph":
    # claim1: first glyph 'I' vs 'J' at top-left (x8-105,y12-95); claim2: whole expr blue in render
    for name, a in (("RENDER", r), ("ORIG", o)):
        bm, dm = blue(a), dark(a)
        print(f"{name}: blue px={bm.sum()} dark px={dm.sum()} blue/(blue+dark)={bm.sum()/max(1,bm.sum()+dm.sum()):.3f}")
    print("--- RENDER top-left glyph region ink (x4-60,y8-100) ---")
    ascii_art(r, 4, 8, 60, 100, dark(r) | blue(r))
    print("--- ORIG top-left glyph region ---")
    ascii_art(o, 4, 8, 60, 100, dark(o) | blue(o))

elif CLAIM == "017_edge":
    # claim: right-edge X8 column digits differ (row1 1 vs 1+fragment, row3 22 vs 2)
    for name, a in (("RENDER", r), ("ORIG", o)):
        dm = dark(a)
        colsum = dm.sum(axis=0)
        print(f"{name}: dark px in last 60 cols={colsum[-60:].sum()}, per-col last 30: {colsum[-30:].tolist()}")
    # rows of interest: find dark-ink row bands in right 60 cols
    for name, a in (("RENDER", r), ("ORIG", o)):
        dm = dark(a)[:, -60:]
        rows = dm.sum(axis=1)
        bands = [y for y in range(H) if rows[y] >= 3]
        # group
        groups = []
        for y in bands:
            if groups and y - groups[-1][-1] <= 3: groups[-1].append(y)
            else: groups.append([y])
        print(f"{name} ink row-bands in right 60 cols: {[(g[0], g[-1], int(rows[g].sum())) for g in groups]}")

elif CLAIM == "018_missing3":
    # claim: highlighted (yellow) X8 cell row1 has red '3' in orig, empty in render
    for name, a in (("RENDER", r), ("ORIG", o)):
        yel = (a[:,:,0] > 220) & (a[:,:,1] > 210) & (a[:,:,2] < 190) & (a[:,:,2] > 100)
        ys, xs = np.where(yel)
        if len(xs):
            print(f"{name}: yellow px={yel.sum()} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}")
            rm = red(a) & yel.__class__(np.broadcast_to(yel[:,:,None], a.shape))[:,:,0] if False else red(a)
            # red ink inside yellow bbox
            x0,x1,y0,y1 = xs.min(), xs.max(), ys.min(), ys.max()
            sub_r = red(a[y0:y1+1, x0:x1+1]); sub_y = yel[y0:y1+1, x0:x1+1]
            print(f"   red px inside yellow bbox: {(sub_r & sub_y).sum()}, red total in bbox: {sub_r.sum()}")
        else:
            print(f"{name}: no yellow found")

elif CLAIM == "022_redrule":
    # claim: continuous red horizontal rule in render at y~0.27-0.30 of crop, absent in orig
    for name, a in (("RENDER", r), ("ORIG", o)):
        rm = red(a)
        rows = rm.sum(axis=1)
        cand = [(y, int(rows[y])) for y in range(H) if rows[y] > W * 0.3]
        print(f"{name}: rows with >30% width red ink: {cand[:20]}")

elif CLAIM == "031_grid":
    # claim: vertical separators at crop x~78,155,235,313,395,475,555 and row rules missing in render
    xs = [78, 155, 235, 313, 395, 475, 555]
    for name, a in (("RENDER", r), ("ORIG", o)):
        dm = dark(a) | grayish(a)
        print(f"{name}: vertical-separator ink at boundaries (y30-410, x+-3):")
        for x in xs:
            seg = dm[30:410, max(0,x-3):x+4]
            print(f"   x={x}: {int(seg.sum())}", end="")
        print()
        rows = dm[:, 60:580].sum(axis=1)
        hrules = [(y, int(rows[y])) for y in range(30, 410) if rows[y] > 300]
        print(f"   horiz rules (rows y30-410 with >300 ink px in x60-580): {hrules[:20]}")

elif CLAIM == "041_gridleft":
    # claim: gridlines start far left (x~25) in render vs at axis (x~120) in orig; vertical rule too high
    for name, a in (("RENDER", r), ("ORIG", o)):
        gm = grayish(a) & ~dark(a)
        rows = gm.sum(axis=1)
        glines = [y for y in range(H) if rows[y] > 150]
        groups = []
        for y in glines:
            if groups and y - groups[-1][-1] <= 3: groups[-1].append(y)
            else: groups.append([y])
        print(f"{name} gray gridline row-groups: {[(g[0], g[-1]) for g in groups]}")
        for g in groups:
            y = g[len(g)//2]
            xs = np.where(gm[y])[0]
            if len(xs): print(f"   y={y}: gray x {xs.min()}-{xs.max()}")
        # vertical gray line near x~118 above first gridline
        col = gm[:, 110:130].sum(axis=1)
        seg = [(y, int(col[y])) for y in range(0, min(H, 300)) if col[y] >= 5]
        print(f"   vert gray ink x110-130, y0-300: {seg[:25]}")

elif CLAIM == "048_digit":
    # claim: bottom entry of x5 column (crop x~200-230, y~195-215) is (6) in render vs (5) in orig
    print("--- RENDER cell region (x185-245, y185-225) ---")
    ascii_art(r, 185, 185, 245, 225, dark(r))
    print("--- ORIG same region ---")
    ascii_art(o, 185, 185, 245, 225, dark(o))
    for name, a in (("RENDER", r), ("ORIG", o)):
        dm = dark(a)
        print(f"{name} ink px in x185-245 y185-225: {int(dm[185:225, 185:245].sum())}")

elif CLAIM == "036_text":
    # claim: case/spelling differences; verbatim record says 'Class II' / 'misclassified'
    for name, a in (("RENDER", r), ("ORIG", o)):
        dm = dark(a)
        rows = dm.sum(axis=1)
        bands = []
        inb = False
        for y in range(H):
            if rows[y] > 4 and not inb: start = y; inb = True
            elif rows[y] <= 4 and inb: bands.append((start, y)); inb = False
        print(f"{name} text row-bands: {bands[:25]}")
