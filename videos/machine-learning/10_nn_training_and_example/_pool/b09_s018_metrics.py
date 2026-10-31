#!/usr/bin/env python3
"""b09 s018: panel rect + border colour + label glyph metrics, original side."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
o = np.asarray(Image.open(NS + "unique_slides/slide_018.jpg").convert("RGB")).astype(np.int16)

print("== panel edges: sample colours across x at y=62 and y=198 ==")
for y in (60, 62, 63, 64, 197, 198, 199, 200):
    row = [tuple(o[y, x]) for x in (368, 370, 372, 375, 378, 500, 700, 880, 888, 895, 898, 900, 902)]
    print(f" y={y}: " + " ".join(f"{x[0]},{x[1]},{x[2]}" for x in row))

print("\n== panel edges: sample colours down y at x=372 and x=902 ==")
for x in (370, 372, 374, 900, 902, 904):
    col = [tuple(o[y, x]) for y in (60, 63, 66, 100, 150, 195, 198, 201)]
    print(f" x={x}: " + " ".join(f"{p[0]},{p[1]},{p[2]}" for p in col))

print("\n== distinct saturated colours in the diagram panel (x368..902,y63..205) ==")
sub = o[63:205, 368:902].reshape(-1, 3)
cols, counts = np.unique(sub, axis=0, return_counts=True)
order = np.argsort(-counts)
for i in order[:22]:
    print(f"  {tuple(int(v) for v in cols[i])} x{int(counts[i])}")

print("\n== blue label glyph metrics (x690..760) ==")
blue = (o[:, :, 2] > 120) & (o[:, :, 0] < 120) & (o[:, :, 1] < 120)
for y0, y1, lbl in ((74, 106, "label1"), (106, 142, "label2"), (142, 182, "label3")):
    m = blue[y0:y1, 690:760]
    ys, xs = np.nonzero(m)
    print(f"  {lbl}: x {690+xs.min()}..{690+xs.max()} (w={xs.max()-xs.min()+1}) y {y0+ys.min()}..{y0+ys.max()} (h={ys.max()-ys.min()+1}) n={m.sum()}")

print("\n== class label glyph metrics (x780..850, dark) ==")
dark = o.sum(2) < 560
for y0, y1, lbl in ((50, 100, "c1"), (100, 140, "c2"), (140, 182, "cm")):
    m = dark[y0:y1, 780:850]
    ys, xs = np.nonzero(m)
    print(f"  {lbl}: x {780+xs.min()}..{780+xs.max()} (w={xs.max()-xs.min()+1}) y {y0+ys.min()}..{y0+ys.max()} (h={ys.max()-ys.min()+1})")

print("\n== magenta bottom label metrics (x360..420, y185..205) ==")
mg = (o[:, :, 0] > 120) & (o[:, :, 2] > 110) & (o[:, :, 1] < 95)
m = mg[185:205, 360:420]
ys, xs = np.nonzero(m)
print(f"  x {360+xs.min()}..{360+xs.max()} y {185+ys.min()}..{185+ys.max()} n={int(m.sum())}")
for y in range(186, 204):
    print(f"   {y}: " + "".join("#" if mg[y, x] else "." for x in range(360, 420)))
