"""Identify the two ambiguous glyphs in slide 030's right-endpoint label.

Method: template matching against digit glyphs taken from the SAME original frame
(point labels "(2, 10)" and "(5, 1)" — same italic gray font/size as the ambiguous
label). Each glyph is binarised at several thresholds, trimmed to its ink box,
resized to a common canvas, and compared by IoU + NCC.
"""
import numpy as np
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_030.jpg"
img = Image.open(ORIG).convert("RGB")
g = np.array(img).astype(float).sum(axis=2) / 3.0


def glyph(x0, x1, y0, y1, thr):
    sub = g[y0:y1, x0:x1]
    m = sub < thr
    ys, xs = np.nonzero(m)
    if len(xs) < 2:
        return None
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def norm(m, size=20):
    if m is None:
        return None
    im = Image.fromarray((m * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)
    return np.asarray(im) > 127


def iou(a, b):
    inter = np.logical_and(a, b).sum()
    union = np.logical_or(a, b).sum()
    return inter / union if union else 0.0


def ncc(a, b):
    x = a.ravel().astype(float) - a.mean()
    y = b.ravel().astype(float) - b.mean()
    d = np.linalg.norm(x) * np.linalg.norm(y)
    return float(x @ y / d) if d else 0.0


# (name, x0, x1, y0, y1) in original frame px
TEMPLATES = {
    "digit_2": (632, 642, 149, 159),
    "digit_1": (645, 651, 149, 159),
    "digit_0": (651, 659, 149, 159),
    "digit_5": (695, 704, 246, 258),
    "digit_1b": (709, 716, 246, 258),
    "digit_3span": (669, 675, 131, 140),
}
TARGETS = {
    "amb_A": (727, 737, 141, 152),
    "amb_B": (740, 750, 141, 152),
}

print("=== raw glyph bitmaps (threshold 178) ===")
for name, (x0, x1, y0, y1) in list(TEMPLATES.items()) + list(TARGETS.items()):
    m = glyph(x0, x1, y0, y1, 178)
    print(f"-- {name} (trim {m.shape[1]}x{m.shape[0]})")
    for row in m:
        print("   ", "".join("#" if v else "." for v in row))

print()
print("=== similarity matrix: target vs template (mean IoU / NCC over thresholds 160..200) ===")
for tname, tbox in TARGETS.items():
    print(f"-- {tname}")
    for tplname, tplbox in TEMPLATES.items():
        ious, nccs = [], []
        for thr in range(160, 201, 4):
            T = norm(glyph(*tbox, thr))
            P = norm(glyph(*tplbox, thr))
            if T is None or P is None:
                continue
            ious.append(iou(T, P))
            nccs.append(ncc(T.astype(float), P.astype(float)))
        print(f"   vs {tplname:12s} IoU={np.mean(ious):.3f}  NCC={np.mean(nccs):+.3f}")
