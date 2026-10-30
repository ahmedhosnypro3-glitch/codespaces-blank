"""Fine map with strict ink threshold + fill color census of slide_004 original boxes."""
from PIL import Image
import numpy as np
from collections import Counter

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
o = Image.open(ORIG).convert("RGB")
a = np.asarray(o).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

print("=" * 72)
print("BOX FILL COLORS (interior medians, text-free zones)")
print("=" * 72)
zones = {
    "Let Y box  (interior top-left corner)": (88, 120, 105, 112),
    "Let Y box  (bottom-right corner)":      (300, 380, 210, 216),
    "Let Yh box (TL corner)":               (433, 470, 105, 112),
    "Remember box":                          (790, 870, 104, 110),
    "Objective box":                         (82, 100, 246, 252),
    "Error box":                             (82, 120, 360, 362),
    "Where box":                             (700, 850, 236, 242),
    "Define box":                            (500, 640, 442, 445),
    "Formula box":                           (200, 400, 468, 471),
}
for name, (x0, x1, y0, y1) in zones.items():
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    med = tuple(int(v) for v in np.median(sub, axis=0))
    cnt = Counter(map(tuple, [tuple(v) for v in sub.tolist()]))
    top = cnt.most_common(3)
    print(f"  {name:42s} median={med}  top={top}")

print()
print("=" * 72)
print("STRICT INK MAP — left box equation region x155..262 y108..212")
print("=" * 72)
ink = (R < 150) | (G < 150) | (B < 150)
X0, X1, Y0, Y1 = 155, 263, 108, 212
print("     " + "".join(str((X0 + i) // 10 % 10) for i in range(X1 - X0)))
for yy in range(Y0, Y1):
    row = ""
    for xx in range(X0, X1):
        if not ink[yy, xx]:
            row += "."
            continue
        r_, g_, b_ = a[yy, xx]
        if r_ - g_ > 45 and r_ - b_ > 45:
            row += "R"
        elif b_ - r_ > 30:
            row += "B"
        else:
            row += "#"
    print(f"{yy:4d} {row}")
