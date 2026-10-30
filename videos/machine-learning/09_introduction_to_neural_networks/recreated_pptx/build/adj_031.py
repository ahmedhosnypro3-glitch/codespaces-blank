#!/usr/bin/env python3
"""PIL adjudication of slide_031 judge findings against the original frame."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
orig = Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")
rend = Image.open(f"{V}/recreated_pptx/build/slide_031_rendered-1.png").convert("RGB")
print("orig", orig.size, "render", rend.size)

# Diagram region in original: build places image at x=1.5,y=1.2,w=7.5,h=3.5 in
# 960x540 frame => 1px = 1pt at 960 wide? Slide is 13.33in wide = 960px -> 72 px/in
# so x=1.5in -> 108px, y=1.2in -> 86.4px, w=7.5in->540px, h=3.5in->252px
px_per_in = 960 / 13.33
def in2px(v): return v * px_per_in
print("px/in", px_per_in)
print("diagram bbox orig:", in2px(1.5), in2px(1.2), in2px(1.5+7.5), in2px(1.2+3.5))

# Crop the diagram area from original and render for visual check
dbox = (int(in2px(1.5)), int(in2px(1.2)), int(in2px(9.0)), int(in2px(4.7)))
orig.crop(dbox).resize((dbox[2]-dbox[0], dbox[3]-dbox[1])).save("/tmp/031_orig_diagram.png")

# The NN diagram PNG itself (generated) - 600dpi, 7.5x3.5in -> 4500x2100 px
d = Image.open(f"{V}/recreated_pptx/build/slide_031_nn_diagram.png")
print("diagram png size", d.size)
alpha = d.split()[-1] if d.mode == "RGBA" else None
if alpha is not None:
    a = np.array(alpha)
    ys, xs = np.where(a > 10)
    print("diagram ink bbox (px):", xs.min(), ys.min(), xs.max(), ys.max())
    print("diagram ink extent in inches:", xs.max()/600, ys.max()/600)
else:
    print("no alpha", d.mode)

# Save diagram at readable scale for vision later
d.convert("RGBA").save("/tmp/031_diagram_rgba.png")

# Find text-like ink in the ORIGINAL: look for the "O5=0.828" label and Target column.
# Scan the original's right part of diagram for dark ink columns
a = np.array(orig.convert("L"))
print("\n=== original column ink profile in diagram band y=86..338 ===")
band = a[86:338]
inkcols = (band < 128).sum(axis=0)
runs = []
inrun = False
for x, c in enumerate(inkcols):
    if c > 0 and not inrun:
        start = x; inrun = True
    elif c == 0 and inrun:
        runs.append((start, x-1, int(inkcols[start:x].sum()))); inrun = False
if inrun: runs.append((start, len(inkcols)-1, int(inkcols[start:].sum())))
print("ink column runs (x0,x1,ink):")
for r in runs: print(r)
