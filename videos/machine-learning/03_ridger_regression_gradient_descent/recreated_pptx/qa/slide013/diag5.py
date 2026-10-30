import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0
ra = np.asarray(R).astype(int)
ro = np.asarray(O).astype(int)

print("=== RENDER label-box white text extents ===")
wh = (ra[:, :, 0] > 235) & (ra[:, :, 1] > 235) & (ra[:, :, 2] > 235)
for (tag, x0, x1) in (("Train", 96, 161), ("Test", 801, 867)):
    m = wh[int(96 * s):int(126 * s), int(x0 * s):int(x1 * s)]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {tag}: ink x{x0 + xs.min()/s:.0f}..{x0 + xs.max()/s:.0f} y{96 + ys.min()/s:.0f}..{96 + ys.max()/s:.0f} n={m.sum()}")
print("=== ORIGINAL label-box white text extents ===")
who = (ro[:, :, 0] > 235) & (ro[:, :, 1] > 235) & (ro[:, :, 2] > 235)
for (tag, x0, x1) in (("Train", 96, 161), ("Test", 801, 867)):
    m = who[96:126, x0:x1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {tag}: ink x{x0 + xs.min()}..{x0 + xs.max()} y{96 + ys.min()}..{96 + ys.max()} n={m.sum()}")
print()
print("=== RENDER test table + train table row-band ink profile (frame px) ===")
nrb = ~(((np.abs(ra[:, :, 0] - 255) < 14) & (np.abs(ra[:, :, 1] - 255) < 14) & (np.abs(ra[:, :, 2] - 255) < 14)) |
        ((np.abs(ra[:, :, 0] - 233) < 16) & (np.abs(ra[:, :, 1] - 233) < 16) & (np.abs(ra[:, :, 2] - 231) < 18)))
for (tag, y0, y1, x0, x1) in (("trainB1", 126, 249, 92, 459), ("testB1", 126, 249, 719, 872),
                              ("trainB2", 265, 389, 92, 459), ("testB2", 265, 389, 719, 872),
                              ("trainB3", 402, 527, 92, 459), ("testB3", 402, 527, 719, 872)):
    a = nrb[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)].sum(axis=1) / (s * s)
    # print only rows with ink > 10
    rows = [(int(y0 + i / s), int(v)) for i, v in enumerate(a) if v > 10]
    # collapse into bands
    bands = []
    for y, v in rows:
        if bands and y - bands[-1][1] <= 1:
            bands[-1][1] = y
            bands[-1][2] += v
        else:
            bands.append([y, y, v])
    print(f"  {tag}: " + ", ".join(f"y{a}..{b}(n={c})" for a, b, c in bands))
