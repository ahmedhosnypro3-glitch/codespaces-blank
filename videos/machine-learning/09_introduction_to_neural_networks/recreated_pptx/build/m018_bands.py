"""Per-band vertical border detection for slide 018 original."""
import numpy as np
from PIL import Image

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_018.jpg"
g = np.asarray(Image.open(IM).convert("L")).astype(int)
H, W = g.shape
gx = np.zeros_like(g)
gx[:, 1:] = np.abs(np.diff(g, axis=1))


def peaks(y0, y1, thr=40):
    v = (gx[y0:y1] > 60).sum(axis=0)
    out = []
    cur = None
    for x in range(W):
        if v[x] >= thr:
            if cur is None:
                cur = [x, x, v[x]]
            else:
                cur[1] = x
                cur[2] = max(cur[2], v[x])
        elif cur is not None:
            out.append((cur[0], cur[1], int(cur[2])))
            cur = None
    if cur:
        out.append((cur[0], cur[1], int(cur[2])))
    return out


print("eq-card band y100..150 :", peaks(100, 150, 30))
print("step pane band y175..270:", peaks(175, 270, 30))
print("callout band y185..235  :", peaks(185, 235, 15))
print("callout x330..470 only  :", peaks(185, 235, 10))
print("bottom charts y330..475 :", peaks(330, 475, 30))
print("caption band y485..512  :", peaks(485, 512, 10))
