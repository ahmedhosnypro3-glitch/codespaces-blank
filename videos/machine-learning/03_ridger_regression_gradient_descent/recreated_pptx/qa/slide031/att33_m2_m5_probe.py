#!/usr/bin/env python3
"""M2/Bouncing/L2 adjudication probes for att33 MINORs (slide 031, render_33).

M2: does the ORIG dashed line at x=5 really stop at the x-axis, or do dim
    (JPEG-desaturated) dashes continue below it like the render's?
M5: 'Bouncing' tag colors — crop_33_topblock judge says orig = dark-red italic
    on pale yellow/pink fill; att33 full judge + build say lavender/purple.
L2: annotation box line 2 word anchors (is the line-1 drift present there too?)
"""
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide031"

gr = np.asarray(Image.open(f"{D}/crop_33_graph_render.png").convert("RGB")).astype(int)
go = np.asarray(Image.open(f"{D}/crop_33_graph_orig.png").convert("RGB")).astype(int)
tr = np.asarray(Image.open(f"{D}/crop_33_topblock_render.png").convert("RGB")).astype(int)
to = np.asarray(Image.open(f"{D}/crop_33_topblock_orig.png").convert("RGB")).astype(int)

# graph crop = frame [565,58]-[817,275]; topblock = frame [36,52]-[648,342]
GX, GY = 565.0, 58.0
SXg = gr.shape[1] / 252.0
SYg = gr.shape[0] / 217.0

print("graph crop size", gr.shape, "scale", round(SXg, 3), round(SYg, 3))
print("topblock crop size", tr.shape)

def classify(px):
    R, G, B = px
    if R > 55 and R - G > 25 and R - B > 25: return "R"   # red ink
    if R < 120 and G < 120 and B < 120: return "#"        # dark
    if abs(R - G) < 25 and abs(G - B) < 25 and R < 200: return "g"  # gray
    return "."

print()
print("### M2-A. x-axis locator: rows y360..451 with a horizontal dark/gray run > 300 crop px (plot width)")
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    hits = []
    for y in range(355, im.shape[0]):
        row = im[y, 40:480]
        dk = np.sum((row[:, 0] < 190) & (row[:, 1] < 190) & (row[:, 2] < 190))
        if dk > 300: hits.append((y, int(dk)))
    print(f"  {tag}: {hits[:12]}")

print()
print("### M2-B. 1px class map x246..272, y408..451 (dash band below axis)")
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    print(f"  --- {tag} ---")
    for y in range(408, min(452, im.shape[0])):
        line = "".join(classify(im[y, x]) for x in range(246, 273))
        print(f"    {y:3d} {line}")

print()
print("### M2-C. same class map for the clearly-dash region ABOVE (y330..370) for color comparison")
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    print(f"  --- {tag} ---")
    for y in range(330, 370, 2):
        line = "".join(classify(im[y, x]) for x in range(246, 273))
        print(f"    {y:3d} {line}")

print()
print("### M2-D. mean RGB of red-class px above axis (y100..380) vs below axis (y415..451)")
def redpx(im, y0, y1):
    R, G, B = im[y0:y1, 246:273, 0], im[y0:y1, 246:273, 1], im[y0:y1, 246:273, 2]
    m = (R > 55) & (R - G > 25) & (R - B > 25)
    return im[y0:y1, 246:273][m]
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    up, dn = redpx(im, 100, 380), redpx(im, 415, 452)
    f = lambda a: "n=0" if len(a) == 0 else f"n={len(a)} mean=({a[:,0].mean():.0f},{a[:,1].mean():.0f},{a[:,2].mean():.0f})"
    print(f"  {tag}: above[{f(up)}]  below[{f(dn)}]")

print()
print("### M5. Bouncing tag colors — frame region x300..400 y292..330 -> topblock crop")
TX, TY = 36.0, 52.0
SXt = tr.shape[1] / 612.0
SYt = tr.shape[0] / 290.0
for tag, im in (("RENDER", tr), ("ORIG  ", to)):
    x0, x1 = int((300 - TX) * SXt), int((400 - TX) * SXt)
    y0, y1 = int((292 - TY) * SYt), int((330 - TY) * SYt)
    reg = im[y0:y1, x0:x1]
    R, G, B = reg[..., 0], reg[..., 1], reg[..., 2]
    # fill = mode of light pixels (exclude dark/red/purple ink)
    light = reg[(R > 200) & (B > 180)]
    fill = light.mean(axis=0) if len(light) else None
    # ink = darkest quartile
    lum = R * 0.3 + G * 0.6 + B * 0.1
    thr = np.percentile(lum, 6)
    ink = reg[lum <= thr]
    print(f"  {tag}: fill mean RGB ({fill[0]:.0f},{fill[1]:.0f},{fill[2]:.0f}) n={len(light)}; "
          f"ink mean ({ink[:,0].mean():.0f},{ink[:,1].mean():.0f},{ink[:,2].mean():.0f}) "
          f"ink median ({np.median(ink[:,0]):.0f},{np.median(ink[:,1]):.0f},{np.median(ink[:,2]):.0f}) n={len(ink)}")

print()
print("### L2. annotation line 2 word clusters (frame coords) — drift check")
def redloose(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (R > 55) & (R - G > 22) & (R - B > 18)
def textink(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    red = redloose(im)
    blue = (B > R + 25) & (B > G + 10) & (B > 90)
    black = (R < 140) & (G < 140) & (B < 140) & (G < R + 30) & (G < B + 30) & ~((G > R + 20) & (G > B + 5))
    return red | blue | black
def clus(cols, x0, gap=4):
    runs, s = [], None
    for i, c in enumerate(cols):
        if c > 0 and s is None: s = i
        if c == 0 and s is not None: runs.append((x0 + s, x0 + i - 1)); s = None
    if s is not None: runs.append((x0 + s, x0 + len(cols) - 1))
    merged = []
    for a, b in runs:
        if merged and a - merged[-1][1] <= gap: merged[-1] = (merged[-1][0], b)
        else: merged.append((a, b))
    return merged
for tag, im in (("RENDER", tr), ("ORIG  ", to)):
    ti = textink(im)
    x0, x1 = 437, 1115
    prof = ti[455:520, x0:x1].sum(axis=1)
    ys = np.nonzero(prof > 2)[0]
    if len(ys) == 0:
        print(f"  {tag}: no L2 band found in crop y455..520"); continue
    ly0, ly1 = 455 + ys.min(), 455 + ys.max()
    c = clus(ti[ly0:ly1 + 1, x0:x1].sum(axis=0), x0)
    fc = [(round(TX + a / SXt, 1), round(TX + b / SXt, 1)) for a, b in c]
    g = [(c[i + 1][0] - c[i][1]) for i in range(len(c) - 1)]
    print(f"  {tag}: L2 band crop-y {ly0}..{ly1} frame-x clusters {fc}")
    print(f"        gaps(crop): {g}")
