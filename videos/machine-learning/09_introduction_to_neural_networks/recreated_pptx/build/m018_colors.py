"""Color-based border detection for slide 018 original."""
import numpy as np
from PIL import Image

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_018.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

masks = {
    "yellow_callout": (R > 195) & (G > 165) & (B < 170),
    "coral_eqcard": (R > 170) & (R - G > 60) & (R - B > 60) & (G < 150),
    "blue_panels": (B > 130) & (B - R > 80) & (G < 160),
}
for name, m in masks.items():
    ys, xs = np.where(m)
    print(f"\n{name}: count {m.sum()}")
    # cluster bboxes via simple projection runs
    colsum = m.sum(axis=0)
    rowsum = m.sum(axis=1)
    cr = [(x, int(colsum[x])) for x in range(W) if colsum[x] > 20]
    rr = [(y, int(rowsum[y])) for y in range(H) if rowsum[y] > 20]
    print(" col peaks:", cr[:40])
    print(" row peaks:", rr[:40])
