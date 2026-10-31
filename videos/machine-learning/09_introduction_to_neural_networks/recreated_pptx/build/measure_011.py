import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
B = V + "/recreated_pptx/build"

orig = Image.open(V + "/unique_slides/slide_011.jpg").convert("RGB")
O = np.asarray(orig).astype(int)
print("ORIG size", orig.size)

def bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

def ascii_map(a, x0, y0, x1, y1, dark=520, mid=650):
    for y in range(y0, y1):
        row = []
        for x in range(x0, x1):
            r, g, b = a[y, x]
            s = r + g + b
            if s < dark:
                row.append("#")
            elif s < mid:
                row.append("+")
            else:
                row.append(".")
        print(f"{y:4d} " + "".join(row))

# --- locate pale-yellow label boxes in the original diagram card (px 144..511 x 355..489) ---
reg = O[350:495, 140:520]
r, g, b = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
yel = (r > 225) & (g > 220) & ((r - b) > 12) & ((g - b) > 8)
ys, xs = np.where(yel)
print("ORIG pale-yellow pixels in diagram region:", len(xs))
if len(xs):
    print("  bbox(abs):", (xs.min() + 140, ys.min() + 350, xs.max() + 140, ys.max() + 350))

print("\n--- ORIG diagram card ASCII x330..430 y350..415 ---")
ascii_map(O, 330, 350, 430, 415)

print("\n--- ORIG badge numeral ASCII x896..940 y16..62 ---")
ascii_map(O, 896, 16, 940, 62)

# --- original equation region: dark ink bbox + column profile ---
eq = O[408:475, 590:825]
er, eg, eb = eq[:, :, 0], eq[:, :, 1], eq[:, :, 2]
dark = (er + eg + eb) < 500
print("\nORIG equation dark-ink bbox (abs):", bbox(dark))
cols = dark.sum(axis=0)
runs = []
inrun = False
for i, c in enumerate(cols):
    if c > 0 and not inrun:
        start = i; inrun = True
    elif c == 0 and inrun:
        runs.append((start + 590, i - 1 + 590, i - start)); inrun = False
if inrun:
    runs.append((start + 590, len(cols) - 1 + 590, len(cols) - start))
print("ORIG equation ink column runs (abs x):")
for s, e, w in runs:
    print(f"   x {s}..{e} width {w}")

# --- rendered build (judged render) ---
try:
    rend = Image.open(B + "/slide_011_rendered-1.png").convert("RGB")
    R = np.asarray(rend).astype(int)
    print("\nRENDER size", rend.size)
    sx = rend.size[0] / 960.0
    sy = rend.size[1] / 540.0
    # cream label box from v3 script: x 4.781in y 5.104in w 0.741 h 0.461  (150 dpi)
    px0, py0 = int(4.781 * 150), int(5.104 * 150)
    px1, py1 = int((4.781 + 0.741) * 150), int((5.104 + 0.461) * 150)
    sub = R[py0:py1, px0:px1]
    s = sub.sum(axis=2)
    print("RENDER cream-box region px", (px0, py0, px1, py1), "min sum", int(s.min()))
    dm = s < 560
    print("RENDER cream-box dark pixel count:", int(dm.sum()), "bbox(abs):", bbox(dm))
    print("--- RENDER cream box ASCII ---")
    for y in range(py0, py1):
        row = []
        for x in range(px0, px1):
            v = int(R[y, x].sum())
            row.append("#" if v < 560 else ("+" if v < 680 else "."))
        print(f"{y:4d} " + "".join(row))
except Exception as e:
    print("render read failed:", e)
