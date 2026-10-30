import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_1-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0
ra = np.asarray(R).astype(int)
ro = np.asarray(O).astype(int)


def census(a, mask, name, x0, x1, y0, y1):
    m = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if not len(ys):
        print(f"  {name}: none")
        return
    print(f"  {name}: x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={m.sum()}")


def yellow(a):
    return (a[:, :, 0] > 235) & (a[:, :, 1] > 200) & (a[:, :, 2] < 170) & (a[:, :, 0] - a[:, :, 2] > 90)


def blue(a):
    return (a[:, :, 2] > a[:, :, 0] + 60) & (a[:, :, 2] > 100) & (a[:, :, 1] < a[:, :, 0] + 30)


print("### RENDER: where is the extra yellow?")
census(ra, yellow(ra), "yellow all", 0, ra.shape[1], 0, ra.shape[0])
# per band in the train tables
for (tag, x0, x1, y0, y1) in (("trB1", 92, 459, 126, 249), ("trB2", 92, 459, 265, 389), ("trB3", 92, 459, 402, 527)):
    census(ra, yellow(ra), tag, int(x0*s), int(x1*s), int(y0*s), int(y1*s))
print()
print("### RENDER: label-box blue")
census(ra, blue(ra), "labels", int(90*s), int(870*s), int(90*s), int(132*s))
print("### RENDER: W box yellow extents per band")
for (tag, y0, y1) in (("wbB1", 126, 251), ("wbB2", 265, 389), ("wbB3", 402, 526)):
    census(ra, yellow(ra), tag, int(505*s), int(624*s), int(y0*s), int(y1*s))
print()
print("### ORIGINAL: same windows")
for (tag, x0, x1, y0, y1) in (("trB1", 92, 459, 126, 249), ("trB2", 92, 459, 265, 389), ("trB3", 92, 459, 402, 527)):
    census(ro, yellow(ro), tag, x0, x1, y0, y1)
census(ro, yellow(ro), "wbB1", 505, 624, 126, 251)
census(ro, yellow(ro), "wbB2", 505, 624, 265, 389)
census(ro, yellow(ro), "wbB3", 505, 624, 402, 526)
print()
print("### RENDER test-table ink vs original test-table ink, per row band")
# find where render test-table ink sits
nrb = ~(((np.abs(ra[:, :, 0] - 255) < 10) & (np.abs(ra[:, :, 1] - 255) < 10) & (np.abs(ra[:, :, 2] - 255) < 10)) |
        ((np.abs(ra[:, :, 0] - 233) < 10) & (np.abs(ra[:, :, 1] - 233) < 10) & (np.abs(ra[:, :, 2] - 231) < 12)))
nob = ~(((np.abs(ro[:, :, 0] - 255) < 10) & (np.abs(ro[:, :, 1] - 255) < 10) & (np.abs(ro[:, :, 2] - 255) < 10)) |
        ((np.abs(ro[:, :, 0] - 233) < 10) & (np.abs(ro[:, :, 1] - 233) < 10) & (np.abs(ro[:, :, 2] - 231) < 12)))
for (tag, y0, y1) in (("testB1", 126, 249), ("testB2", 265, 389), ("testB3", 402, 527)):
    print(f"  {tag} RENDER row-profile (ink px per row, x719..872):")
    cnt = nrb[int(y0 * s):int(y1 * s), int(719 * s):int(872 * s)].sum(axis=1)
    print("   ", [int(v) for v in cnt[::max(1, len(cnt) // 20)]])
    cnt2 = nob[y0:y1, 719:872].sum(axis=1)
    print("    ORIG:", [int(v) for v in cnt2[::max(1, len(cnt2) // 20)]])
