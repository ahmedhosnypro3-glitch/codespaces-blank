import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)


def colormap(y0, y1, x0, x1, label):
    sub = im[y0:y1, x0:x1]
    flat = sub.reshape(-1, 3)
    uniq, counts = np.unique(flat, axis=0, return_counts=True)
    order = np.argsort(-counts)
    print(f"### {label} y{y0}..{y1} x{x0}..{x1}")
    keys = []
    for i in order:
        c = uniq[i]
        if counts[i] >= 6:
            keys.append((tuple(int(v) for v in c), int(counts[i])))
    for i, (c, n) in enumerate(keys):
        print(f"  [{i}] {c}  n={n}")
    # legend: single char per color, index if >9
    legend = {}
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, (c, n) in enumerate(keys):
        legend[c] = chars[i]
    uc = {c: chars[i] for i, (c, n) in enumerate(keys)}
    print()
    for y in range(y0, y1):
        line = ''
        for x in range(x0, x1):
            c = tuple(int(v) for v in im[y, x])
            line += uc.get(c, '?')
        print(f"{y:4d} {line}")
    print()


colormap(182, 216, 456, 512, "LEFT BLUE SHAPE band1")
colormap(150, 195, 500, 632, "RED BOX INTERIOR band1 (top)")
