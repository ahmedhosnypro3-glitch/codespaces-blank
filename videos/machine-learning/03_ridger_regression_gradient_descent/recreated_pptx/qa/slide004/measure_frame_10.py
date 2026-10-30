#!/usr/bin/env python3
"""Pass 10 — PredWhere token colors (clean windows) + Remember border core."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 100) & ((r - g) > 50) & ((r - b) > 30)
blue = (b > 90) & ((b - r) > 50) & ((b - g) > 30)
dark = (r + g + b) < 330


def dom(x0, x1, y0, y1):
    cr, cb, ck = int(red[y0:y1, x0:x1].sum()), int(blue[y0:y1, x0:x1].sum()), int(dark[y0:y1, x0:x1].sum())
    t = cr + cb + ck
    if t == 0:
        return "empty"
    return f"R{cr*100//t}%/B{cb*100//t}%/K{ck*100//t}% (tot{t})"


print("=== PredWhere VAR sub-region (x560..640) per line, tight windows ===")
for nm, (y0, y1) in {"L1 eq(508..560)": (250, 276), "L1 pred": (250, 276),
                     "L2 var(563..640)": (283, 304), "L3 var(560..640)": (311, 340),
                     "L4 var(563..640)": (344, 363)}.items():
    print(f"  {nm}: {dom(*({'L1 eq(508..560)': (505, 560, 250, 276), 'L1 pred': (560, 760, 250, 276), 'L2 var(563..640)': (560, 640, 283, 304), 'L3 var(560..640)': (560, 640, 311, 340), 'L4 var(563..640)': (560, 640, 344, 363)}[nm]))}")

print("\n=== PredWhere arrows (x768..795) per line ===")
for nm, (y0, y1) in {"L2 arrow": (283, 304), "L3 arrow": (311, 340), "L4 arrow": (344, 363)}.items():
    print(f"  {nm}: {dom(768, 795, y0, y1)}")

print("\n=== PredWhere 'Given/Required' tail (x795..884) per line ===")
for nm, (y0, y1) in {"L2 tail": (283, 304), "L3 tail": (311, 340), "L4 tail": (344, 363)}.items():
    print(f"  {nm}: {dom(795, 884, y0, y1)}")

print("\n=== PredWhere L1 detail (Y=XW region + Predicted) ===")
print("  x505..540 (Y=XW eq):", dom(505, 540, 250, 276))
print("  x540..560        :", dom(540, 560, 250, 276))
print("  x560..760 (Pred) :", dom(560, 760, 250, 276))

print("\n=== Remember border: most-blue single px over full perimeter ring ===")
# ring: top row, bottom row, left col, right col of box x784..878 y101..152
best = None
for (x0, x1, y0, y1) in [(786, 876, 101, 106), (786, 876, 148, 152), (783, 788, 104, 150), (873, 878, 104, 150)]:
    sub = im[y0:y1, x0:x1].reshape(-1, 3)
    sc = sub[:, 2] - np.maximum(sub[:, 0], sub[:, 1])
    k = sc > 12
    if k.any():
        idx = np.argmax(sc[k])
        px = sub[k][idx]
        print(f"  window {(x0,y0,x1,y1)}: most-blue px {tuple(int(px[i]) for i in range(3))}")
# also just histogram the border-ish blue
sub = im[103:150, 786:876].reshape(-1, 3)
bl = (sub[:, 2] - sub[:, 0] > 20)
if bl.any():
    print("  Remember border-ish median blue:", tuple(int(np.median(sub[bl][:, i])) for i in range(3)))

# fill samples at clean centers
print("\n=== fill centers ===")
for nm, (x, y) in {"Obj": (190, 249), "Err": (110, 315), "Formula": (400, 500), "Remember": (831, 142), "Define": (400, 420), "BOX1": (300, 200)}.items():
    print(f"  {nm}: RGB{tuple(int(im[y, x][i]) for i in range(3))}")
