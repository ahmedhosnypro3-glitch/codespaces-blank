"""PIL region measurement for slide 018 original frame (960x540)."""
import numpy as np
from PIL import Image

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_018.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = a.shape[:2]
print("frame", W, H)


def near(rgb, tol):
    return (np.abs(a - np.array(rgb)).sum(axis=2) < tol)


def bbox_rows_cols(mask, minlen, axis):
    runs = []
    cur = None
    for i in range(mask.shape[axis]):
        cnt = int(mask[:, i].sum() if axis == 1 else mask[i, :].sum())
        if cnt >= minlen:
            if cur is None:
                cur = [i, i]
            else:
                cur[1] = i
        elif cur is not None:
            runs.append(tuple(cur))
            cur = None
    if cur is not None:
        runs.append(tuple(cur))
    return runs


# coral-ish red borders (#FF4D4D) -> loose: r>200, g<130, b<130
coral = (a[:, :, 0] > 190) & (a[:, :, 0] - a[:, :, 1] > 90) & (a[:, :, 0] - a[:, :, 2] > 90)
# pure blue borders (#0000FF)
blue = (a[:, :, 2] > 150) & (a[:, :, 2] - a[:, :, 0] > 90) & (a[:, :, 1] < 130)

for name, m in (("CORAL", coral), ("BLUE", blue)):
    ys, xs = np.where(m)
    print(f"{name}: total {m.sum()} bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
    print(f"  row runs (>40px): {bbox_rows_cols(m, 40, 1)}")
    print(f"  col runs (>25px): {bbox_rows_cols(m, 25, 0)}")

# dark red title strip (#C00000)
darkred = (np.abs(a - np.array([192, 0, 0])).sum(axis=2) < 120)
ys, xs = np.where(darkred)
print("DARKRED bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "count", darkred.sum())
# title band: rows with many darkred px
rr = darkred.sum(axis=1)
print("  title rows:", [y for y in range(H) if rr[y] > 40][:12])
