#!/usr/bin/env python3
"""Lane G diag: characterize original-frame chrome/artifact bands."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"

for s in ("008", "009", "013"):
    a = np.asarray(Image.open(f"{NS}/unique_slides/slide_{s}.jpg").convert("RGB")).astype(int)
    h, w = a.shape[:2]
    print("=" * 60, "SLIDE", s)
    print("  corner TL", a[0:4, 0:4].reshape(-1, 3).mean(0).round(1),
          " TR", a[0:4, -4:].reshape(-1, 3).mean(0).round(1),
          " BL", a[-4:, 0:4].reshape(-1, 3).mean(0).round(1),
          " BR", a[-4:, -4:].reshape(-1, 3).mean(0).round(1))
    for y in (0, 2, 5, 10, 20, 30, 40, 44, 45, 46, 50):
        print(f"  row{y:3d} mean={a[y].mean(0).round(1)} min={a[y].min(0)} max={a[y].max(0)}")
    for y in (500, 505, 508, 510, 512, 515, 518, 520, 522, 525, 528, 530, 535, 539):
        print(f"  row{y:3d} mean={a[y].mean(0).round(1)} min={a[y].min(0)} max={a[y].max(0)}")
    # yellow badge hunt
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    ym = (r > 220) & (g > 200) & (b < 190) & ((r - b) > 50)
    ys, xs = np.nonzero(ym)
    if len(xs):
        print("  yellow badge bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "n", len(xs))
    else:
        print("  no yellow badge found")
