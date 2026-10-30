#!/usr/bin/env python3
"""Probe 8f: glyph correlation (Required vs Parameter) + restricted underline band
+ ASCII visualization of the Yvec equation region, orig vs render."""
from PIL import Image
import numpy as np

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB"))
REND = np.asarray(Image.open("recreated_pptx/qa/slide004/render_8.png").convert("RGB"))
S = REND.shape[0] / 540.0

def dark(arr, x0, y0, x1, y1, t=190):
    return (arr[y0:y1, x0:x1].max(axis=2) < t)

# ---- (A2) correlate last-inline-word patch vs tag patch in the ORIGINAL L4 ----
print("=== (A2) orig L4: last-inline (671..747) vs tag (803..878), y344..363 ===")
w1 = dark(ORIG, 668, 342, 750, 364)
w2 = dark(ORIG, 800, 342, 882, 364)
print(f"inline patch ink={w1.sum()} tag patch ink={w2.sum()}")
# slide tag patch horizontally to same width and XOR
h = 22
a = w1.astype(int); b = w2.astype(int)
# resize b to a's shape via PIL
bi = Image.fromarray((b*255).astype(np.uint8)).resize((a.shape[1], a.shape[0]))
bd = (np.asarray(bi) > 127).astype(int)
inter = (a & bd).sum(); union = (a | bd).sum()
print(f"IoU inline-vs-tag: {inter/union:.3f}  (same word expected >0.5)")
# also compare 'Parameter' hypothesis: patch from L4 597..664? no - use L3 tag 'Given'? insufficient.
# Better: render's own Parameter (689..728) vs its inline Required (733..752) vs orig patches
wr_p = dark(REND, int(689*S), int(342*S), int(728*S), int(364*S))
wr_r = dark(REND, int(733*S), int(342*S), int(752*S), int(364*S))
for name, wr in (("render_Parameter", wr_p), ("render_Required", wr_r)):
    wi = Image.fromarray((wr.astype(np.uint8)*255)).resize((a.shape[1], a.shape[0]))
    wd = (np.asarray(wi) > 127).astype(int)
    inter = (a & wd).sum(); union = (a | wd).sum()
    print(f"IoU orig-inline vs {name}: {inter/union:.3f}")
# ASCII of orig inline word and tag word
def ascii_patch(m, label):
    print(label)
    for r in m:
        print("  " + "".join("#" if v else "." for v in r))
ascii_patch(w1, "--- ORIG inline word x668..750 y342..364 ---")
ascii_patch(w2, "--- ORIG tag word x800..882 y342..364 ---")

# ---- (B2) restricted underline-only band y275..286 ----
print("\n=== (B2) underline band y275..286 (below L1 glyphs) x495..700 ===")
for name, arr, sc in (("ORIG", ORIG, 1.0), ("REND", REND, S)):
    m = dark(arr, int(495*sc), int(275*sc), int(700*sc), int(286*sc))
    b = arr[int(275*sc):int(286*sc), int(495*sc):int(700*sc)].astype(int)
    red = (b[:,:,0] > 140) & (b[:,:,1] < 110) & (b[:,:,2] < 110)
    blue = (b[:,:,2] > 120) & (b[:,:,0] < 100) & (b[:,:,1] < 110)
    def runs(mm, mn=2):
        cols = mm.any(axis=0); out, st = [], None
        for i, v in enumerate(cols):
            if v and st is None: st = i
            elif not v and st is not None:
                if i-st >= mn: out.append((round((st+495*sc)/sc,1), round((i+495*sc)/sc,1)))
                st = None
        if st is not None: out.append((round((st+495*sc)/sc,1), round((700*sc)/sc,1)))
        return out
    print(f"{name}: dark={runs(m)} red={runs(red)} blue={runs(blue)}")

# ---- (C2) ASCII visualization Yvec region orig x78..245 y124..190 (2x2 down) ----
print("\n=== (C2) ORIG Yvec region x78..245 y124..190 (2x2) ===")
reg = ORIG[124:190, 78:245].astype(int)
dk = reg.max(axis=2) < 190
red = (reg[:,:,0] > 140) & (reg[:,:,1] < 110) & (reg[:,:,2] < 110)
H, W = dk.shape
for yy in range(0, H-1, 2):
    row = ""
    for xx in range(0, W-1, 2):
        blk_d = dk[yy:yy+2, xx:xx+2].sum()
        blk_r = red[yy:yy+2, xx:xx+2].sum()
        row += ("R" if blk_r >= 2 else "#" if blk_d >= 2 else ("r" if blk_r else ("+" if blk_d else ".")))
    print(f"{124+yy:3d} {row}")
print("\n=== (C3) REND same region (frame x78..245 y124..190, eff. 2x2 down) ===")
x0, y0, x1, y1 = int(78*S), int(124*S), int(245*S), int(190*S)
reg = REND[y0:y1, x0:x1].astype(int)
dk = reg.max(axis=2) < 190
red = (reg[:,:,0] > 140) & (reg[:,:,1] < 110) & (reg[:,:,2] < 110)
# downsample so output px per frame px matches ORIG's (2 frame px per char)
fy = (y1-y0)/33.0; fx = (x1-x0)/83.0
for yy in range(33):
    row = ""
    for xx in range(83):
        ya, yb = int(y0+yy*fy), int(y0+(yy+1)*fy)
        xa, xb = int(x0+xx*fx), int(x0+(xx+1)*fx)
        bd = dk[ya:yb, xa:xb].sum(); br = red[ya:yb, xa:xb].sum()
        row += ("R" if br >= 2 else "#" if bd >= 2 else ("r" if br else ("+" if bd else ".")))
    print(f"{124+int(yy*fy/S):3d} {row}")
