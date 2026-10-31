import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
B = V + "/recreated_pptx/build"
O = np.asarray(Image.open(V + "/unique_slides/slide_011.jpg").convert("RGB")).astype(int)

def ascii_map(a, x0, y0, x1, y1, dark=520, mid=650, step=1, label=""):
    for y in range(y0, y1, step):
        row = []
        for x in range(x0, x1, step):
            s = int(a[y, x].sum())
            row.append("#" if s < dark else ("+" if s < mid else "."))
        print(f"{y:4d} " + "".join(row))

print("--- ORIG equation box ASCII x590..826 y408..474 ---")
ascii_map(O, 590, 408, 826, 474)

print("\n--- ORIG activation label zoom x360..416 y366..400 ---")
ascii_map(O, 360, 366, 416, 400)

R = np.asarray(Image.open(B + "/slide_011_rendered-1.png").convert("RGB")).astype(int)
print("\n--- RENDER scan: dark ink inside diagram card ---")
# card px: x 1.478..7.143 in, y 4.894..6.938 in at 150 dpi
x0, y0, x1, y1 = int(1.478 * 150), int(4.894 * 150), int(7.143 * 150), int(6.938 * 150)
sub = R[y0:y1, x0:x1]
s = sub.sum(axis=2)
dm = s < 500
ys, xs = np.where(dm)
print("card region", (x0, y0, x1, y1), "dark px", len(xs))
if len(xs):
    print("dark bbox abs:", (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0))
    cols = dm.sum(axis=0)
    runs, inrun = [], False
    for i, c in enumerate(cols):
        if c > 0 and not inrun:
            st = i; inrun = True
        elif c == 0 and inrun:
            runs.append((st + x0, i - 1 + x0, int(cols[st:i].max()))); inrun = False
    if inrun:
        runs.append((st + x0, len(cols) - 1 + x0, int(cols[st:].max())))
    print("ink column runs (max col density):")
    for a, b, m in runs:
        if b - a >= 1:
            print(f"   x {a}..{b} w={b-a+1} maxdensity={m}")

print("\n--- RENDER cream box area color samples ---")
for (x, y) in [(717, 766), (770, 800), (820, 830), (760, 790), (730, 795)]:
    print(f"  px({x},{y}) rgb={tuple(int(v) for v in R[y, x])}")

print("\n--- RENDER cream box ASCII x710..840 y760..840 ---")
ascii_map(R, 710, 760, 840, 840)
