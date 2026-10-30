import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0
print("render", R.size, "scale", s)

ra = np.asarray(R).astype(int)
ro = np.asarray(O).astype(int)

r_, g_, b_ = ra[:, :, 0], ra[:, :, 1], ra[:, :, 2]
o_, og, ob = ro[:, :, 0], ro[:, :, 1], ro[:, :, 2]

# rough ink masks (non background) to compare structure
def ink(a):
    bg = ((np.abs(a[:, :, 0] - 255) < 10) & (np.abs(a[:, :, 1] - 255) < 10) & (np.abs(a[:, :, 2] - 255) < 10)) | \
         ((np.abs(a[:, :, 0] - 233) < 10) & (np.abs(a[:, :, 1] - 233) < 10) & (np.abs(a[:, :, 2] - 231) < 12))
    return ~bg

ir = ink(ra)
io = ink(ro)
# simpler: use relative ink
ir = ~(((np.abs(ra[:, :, 0] - 255) < 10) & (np.abs(ra[:, :, 1] - 255) < 10) & (np.abs(ra[:, :, 2] - 255) < 10)) |
       ((np.abs(ra[:, :, 0] - 233) < 10) & (np.abs(ra[:, :, 1] - 233) < 10) & (np.abs(ra[:, :, 2] - 231) < 12)))
io = ~(((np.abs(ro[:, :, 0] - 255) < 10) & (np.abs(ro[:, :, 1] - 255) < 10) & (np.abs(ro[:, :, 2] - 255) < 10)) |
       ((np.abs(ro[:, :, 0] - 233) < 10) & (np.abs(ro[:, :, 1] - 233) < 10) & (np.abs(ro[:, :, 2] - 231) < 12)))

print("\n=== ink census (render vs original) in the key regions ===")
REGIONS = [
    ("train table B1", 92, 459, 126, 249),
    ("train table B2", 92, 459, 265, 389),
    ("train table B3", 92, 459, 402, 527),
    ("test table B1", 719, 872, 126, 249),
    ("test table B2", 719, 872, 265, 389),
    ("test table B3", 719, 872, 402, 527),
    ("W box B1", 505, 624, 126, 251),
    ("W box B2", 505, 624, 265, 389),
    ("W box B3", 505, 624, 402, 526),
    ("label boxes", 90, 870, 90, 132),
]
for (name, x0, x1, y0, y1) in REGIONS:
    X0, X1, Y0, Y1 = int(x0 * s), int(x1 * s), int(y0 * s), int(y1 * s)
    rn = int(ir[Y0:Y1, X0:X1].sum())
    on = int(io[y0:y1, x0:x1].sum())
    print(f"  {name:16s} render {rn:7d}  original {on:7d}  ratio {rn / max(on,1):.3f}")

# yellow census
def yellow(a):
    return (a[:, :, 0] > 235) & (a[:, :, 1] > 200) & (a[:, :, 2] < 170) & (a[:, :, 0] - a[:, :, 2] > 90)

ry_, oy = yellow(ra), yellow(ro)
print("\n=== yellow census ===")
for (name, x0, x1, y0, y1) in REGIONS:
    X0, X1, Y0, Y1 = int(x0 * s), int(x1 * s), int(y0 * s), int(y1 * s)
    print(f"  {name:16s} render {int(ry_[Y0:Y1, X0:X1].sum()):7d}  original {int(oy[y0:y1, x0:x1].sum()):7d}")

# blue census
def blue(a):
    return (a[:, :, 2] > a[:, :, 0] + 60) & (a[:, :, 2] > 100) & (a[:, :, 1] < a[:, :, 0] + 30)

rb_, ob_ = blue(ra), blue(ro)
print("\n=== blue census ===")
for (name, x0, x1, y0, y1) in REGIONS:
    X0, X1, Y0, Y1 = int(x0 * s), int(x1 * s), int(y0 * s), int(y1 * s)
    print(f"  {name:16s} render {int(rb_[Y0:Y1, X0:X1].sum()):7d}  original {int(ob_[y0:y1, x0:x1].sum()):7d}")

# red census
def red(a):
    return (a[:, :, 0] > a[:, :, 1] + 40) & (a[:, :, 0] > a[:, :, 2] + 40)

rr_, orr = red(ra), red(ro)
print("\n=== red census ===")
for (name, x0, x1, y0, y1) in REGIONS:
    X0, X1, Y0, Y1 = int(x0 * s), int(x1 * s), int(y0 * s), int(y1 * s)
    print(f"  {name:16s} render {int(rr_[Y0:Y1, X0:X1].sum()):7d}  original {int(orr[y0:y1, x0:x1].sum()):7d}")
