#!/usr/bin/env python3
"""scope_r4 slide 011 attempt-1 fix verification (measure only; judge decides)."""
import numpy as np
from PIL import Image

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
DPI = 150
A = np.asarray(Image.open(f"{VID}/qa/slide011/rejudge/_attempt1/render-1.png")
               .convert("RGB")).astype(int)
Ot = np.asarray(Image.open(f"{VID}/unique_slides/slide_011.jpg").convert("RGB")
                .resize((2001, 1125), Image.LANCZOS)).astype(int)


def box(a, x0, y0, x1, y1):
    return a[int(y0 * DPI):int(y1 * DPI), int(x0 * DPI):int(x1 * DPI)]


def near(a, rgb, tol):
    return np.abs(a - np.array(rgb)).max(axis=2) <= tol


def bb(m):
    ys, xs = np.nonzero(m)
    return None if len(xs) == 0 else (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


print("### A1: yellow highlight vs red title glyphs (attempt1) ###")
t = box(A, 0.30, 0.24, 12.20, 0.95)
red = near(t, (192, 0, 0), 90)
yel = near(t, (255, 215, 0), 70)
yb, rb = bb(yel), bb(red)
if yb:
    print(f"yellow block x {(0.30+yb[0]/DPI):.2f}-{(0.30+yb[2]/DPI):.2f}in "
          f"y {(0.24+yb[1]/DPI):.2f}-{(0.24+yb[3]/DPI):.2f}in "
          f"fill={int(yel.sum())/((yb[2]-yb[0]+1)*(yb[3]-yb[1]+1))*100:.0f}% (block, not glyphs)")
if rb:
    print(f"red title span x {(0.30+rb[0]/DPI):.2f}-{(0.30+rb[2]/DPI):.2f}in "
          f"(the word 'Output' sits at 7.24-8.33in)")
if yb and rb:
    print(f"red glyphs INSIDE highlight bbox: {int(red[yb[1]:yb[3]+1, yb[0]:yb[2]+1].sum())} "
          f"(red text on top of yellow = highlight, same as original)")

print("\n### A2: red overlay gone from the bottom strip; equation ink intact ###")
stripA = box(A, 0.3, 6.4, 13.0, 7.2)
redA = near(stripA, (192, 0, 0), 60)
print("attempt1 strip red px:", int(redA.sum()), "(v2 had a red 'Sigmoid' overlay here)")
cropA = box(A, 0.5, 6.65, 8.34167, 6.88333).mean(axis=2)
eq3 = Image.open(f"{VID}/recreated_pptx/build/eq_slide_011/eq3.png").convert("RGBA")
bgim = Image.new("RGBA", eq3.size, (253, 245, 230, 255))
eq3 = np.asarray(Image.alpha_composite(bgim, eq3).convert("L")
                 .resize((1176, 35), Image.LANCZOS)).astype(float)
asset_prof = (eq3 < 200).sum(axis=0)
render_prof = (cropA < 200).sum(axis=0)
for name, lo, hi in (("all", 0, len(asset_prof)),
                     ("under old overlay (x5.5-6.1in)", 751, 844),
                     ("left", 0, 751), ("right", 844, len(asset_prof))):
    a = asset_prof[lo:hi].sum(); r = render_prof[lo:hi].sum()
    print(f"  {name}: asset ink={int(a)} render ink={int(r)} retention={r/max(a,1)*100:.0f}%")
print(f"  column-profile Pearson r = {np.corrcoef(asset_prof, render_prof)[0,1]:.4f}")

print("\n### A3: wiring ink in the 3 clean inter-column bands ###")
bgc = np.array([253, 245, 230])
for tag, ob, thr in (("attempt1", A, 55), ("ORIGINAL", Ot, 45)):
    vals = []
    for x0, x1 in ((4.30, 5.45), (6.35, 7.15), (8.05, 8.95)):
        b = box(ob, x0, 2.6, x1, 5.8)
        m = (np.abs(b - bgc).max(axis=2) > thr) if tag == "attempt1" else (b.mean(axis=2) < 150)
        vals.append(int(m.sum()))
    print(f"{tag}: {vals}")
A2 = np.asarray(Image.open(f"{VID}/qa/slide011/rejudge/render-1.png").convert("RGB")).astype(int)
vals = []
for x0, x1 in ((4.30, 5.45), (6.35, 7.15), (8.05, 8.95)):
    b = box(A2, x0, 2.6, x1, 5.8)
    vals.append(int((np.abs(b - bgc).max(axis=2) > 55).sum()))
print(f"v2 (pre-fix): {vals}")
