#!/usr/bin/env python3
"""slide_031 original: find the four calculation-box borders by color (navy/green)."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
r, g, b = O[...,0], O[...,1], O[...,2]

# navy #000080-ish: r<60, g<60, b>80
navy = (r < 70) & (g < 70) & (b > 80) & (b < 200)
# green #008000-ish: g>60, g-r>30, g-b>30
green = (g > 50) & (g - r > 25) & (g - b > 25)
# exclude the green weight labels which are small: keep only long runs

def hgroups(y, mask, minlen=25):
    xs = np.where(mask[y])[0]
    if len(xs)==0: return []
    out=[]; s=xs[0]; p=xs[0]
    for v in xs[1:]:
        if v!=p+1: out.append((s,p)); s=v
        p=v
    out.append((s,p))
    return [o for o in out if o[1]-o[0]>=minlen]

def vgroups(x, mask, minlen=25):
    ys = np.where(mask[:,x])[0]
    if len(ys)==0: return []
    out=[]; s=ys[0]; p=ys[0]
    for v in ys[1:]:
        if v!=p+1: out.append((s,p)); s=v
        p=v
    out.append((s,p))
    return [o for o in out if o[1]-o[0]>=minlen]

for name, mask in [("NAVY", navy), ("GREEN", green)]:
    print(f"\n===== {name}: horizontal long runs (>=60) =====")
    for y in range(H):
        gg = hgroups(y, mask, 60)
        if gg: print(f" y={y}: {gg} rgb={tuple(O[y,(gg[0][0]+gg[0][1])//2])}")
    print(f"===== {name}: vertical long runs (>=60) =====")
    for x in range(W):
        gg = vgroups(x, mask, 60)
        if gg: print(f" x={x}: {gg} rgb={tuple(O[(gg[0][0]+gg[0][1])//2,x])}")
