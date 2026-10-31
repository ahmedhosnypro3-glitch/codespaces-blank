"""Extract slide-008 decision-region polygons from the original frame by colour classification."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
A = np.asarray(Image.open(f"{V}/unique_slides/slide_008.jpg").convert("RGB")).astype(float)
R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]

green = (G - R > 6) & (G - B > 6) & (R > 200) & (G > 230)
lav = (B - R > 15) & (B - G > 15) & (B > 200) & (R > 140)
pink = (R - G > 6) & (R - B > 4) & (abs(G - B) < 25) & (R > 230)

BOX = (168, 796, 122, 504)
inner = np.zeros(A.shape[:2], bool)
inner[BOX[2]:BOX[3], BOX[0]:BOX[1]] = True


def region_poly(mask, k=21, minarea=2000):
    m = ndimage.binary_closing(mask & inner, np.ones((k, k)))
    m = ndimage.binary_opening(m, np.ones((5, 5)))
    m = ndimage.binary_closing(m, np.ones((k, k)))
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m)
    if n == 0:
        return None, 0
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    i = int(np.argmax(sizes)) + 1
    if sizes[i - 1] < minarea:
        return None, 0
    m = (lab == i)
    left, right = [], []
    for y in range(BOX[2], BOX[3]):
        xs = np.nonzero(m[y, BOX[0]:BOX[1]])[0]
        if len(xs) < 3:
            continue
        left.append((int(xs.min()) + BOX[0], y))
        right.append((int(xs.max()) + BOX[0], y))
    return left + right[::-1], int(sizes[i - 1])


out = {}
for name, mask in [("green", green), ("lavender", lav), ("pink", pink)]:
    poly, area = region_poly(mask)
    out[name] = poly
    if poly:
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        print(f"{name}: area={area} npts={len(poly)} bbox x={min(xs)}..{max(xs)} y={min(ys)}..{max(ys)}")
    else:
        print(f"{name}: NONE  (raw mask px={int((mask & inner).sum())})")

json.dump(out, open(f"{V}/recreated_pptx/build/slide_008_regions.json", "w"), indent=1)
print("wrote slide_008_regions.json")
