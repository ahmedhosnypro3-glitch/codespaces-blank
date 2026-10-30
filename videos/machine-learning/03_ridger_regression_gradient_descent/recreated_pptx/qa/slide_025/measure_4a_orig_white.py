import sys
from PIL import Image
import numpy as np

FRAME = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg"

im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("frame", W, H)

R, G, B = a[..., 0], a[..., 1], a[..., 2]

# panel gray E9E9E7 mask
panel = (np.abs(R - 233) < 12) & (np.abs(G - 233) < 12) & (np.abs(B - 231) < 12)
# white figure background (very light, NOT panel gray)
white = (R > 245) & (G > 245) & (B > 245)

print("panel px %d  white px %d" % (panel.sum(), white.sum()))

# ---- white-figure connected-ish scan: group white runs per row into x-ranges,
# restricted to the body area below the title strip and inside the panel.
mask = white & ~panel
# ignore title band (y < 110) and badge
mask[:110, :] = False
mask[50:100, 840:910] = False

rows = mask.any(axis=1)
ys = np.where(rows)[0]
if len(ys):
    print("white ink rows %d..%d" % (ys.min(), ys.max()))

# per-row x extent, then compress into bands
def bands_from_mask(m):
    out = []
    inb = False
    for i, v in enumerate(m):
        if v and not inb:
            inb, s = True, i
        elif not v and inb:
            inb = False
            out.append((s, i - 1))
    if inb:
        out.append((s, len(m) - 1))
    return out

# dense vertical projection of white
colprof = mask.sum(axis=0)
rowprof = mask.sum(axis=1)
# find column bands with substantial white
cb = [b for b in bands_from_mask(colprof > 5)]
rb = [b for b in bands_from_mask(rowprof > 5)]
print("column bands (white>5):", cb)
print("row bands (white>5):", rb)
