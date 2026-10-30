import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0
ra = np.asarray(R).astype(int)
ro = np.asarray(O).astype(int)


def mask_bg(a, thr=14):
    bg = ((np.abs(a[:, :, 0] - 255) < thr) & (np.abs(a[:, :, 1] - 255) < thr) & (np.abs(a[:, :, 2] - 255) < thr)) | \
         ((np.abs(a[:, :, 0] - 233) < thr + 2) & (np.abs(a[:, :, 1] - 233) < thr + 2) & (np.abs(a[:, :, 2] - 231) < thr + 4))
    return ~bg


ir = mask_bg(ra)
io = mask_bg(ro)

# per-cell: 10px grid over the content area, count ink in each
print("grid-ink occupancy diff (render vs original), content y45..540 x54..903")
print("showing cells where the difference is significant")
gy = gx = 10
for fy in range(46, 538, gy):
    line = []
    for fx in range(56, 900, gx):
        Y0, Y1 = int(fy * s), int((fy + gy) * s)
        X0, X1 = int(fx * s), int((fx + gx) * s)
        rn = int(ir[Y0:Y1, X0:X1].sum())
        on = int(io[fy:fy + gy, fx:fx + gx].sum())
        rn = rn / (s * s)
        d = rn - on
        if abs(d) > 12:
            line.append(f"({fx},{fy}):{d:+.0f}")
    if line:
        print("  " + " ".join(line))
