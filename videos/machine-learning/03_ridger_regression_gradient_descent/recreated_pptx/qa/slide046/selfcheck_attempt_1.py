"""Pre-judge self-check for slide 046 attempt 1.

Two independent legs, both required GREEN before a judge dispatch:

  LEG 1 — chrome: shared_patterns/house_chrome_check.py must print PASS
           (its output is banked separately in house_chrome_check_attempt_1.txt).

  LEG 2 — geometry: for every element, the ink bbox measured on the RENDER is
           compared with the ink bbox measured on the ORIGINAL JPEG frame
           (unique_slides/slide_046.jpg) inside the SAME search window.
           Both images are 540 frame-px tall; the render is 2001 px tall so
           scale = H_render/540 render px per frame px (== 2.083 at 150 dpi).
           A divergence > TOL frame px on any element = BUILD DEFECT, fix before
           judging (PIL-first adjudication law).

Search windows are tight per element (no generic +TOL padding, because the
slide's text rows sit only 6-14 frame px apart and neighbours' ink would
otherwise bleed into the window and manufacture false spills).
"""
import json
import sys

import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide046"
RENDER = f"{QA}/render_1.png"
FRAME = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_046.jpg"
TOL = 8  # frame px

# element -> (x0, y0, x1, y1) search window in frame px, chosen tighter than the
# measured element so neighbouring rows cannot leak in
WINDOWS = {
    "top_rule":            (66, 52, 560, 60),
    "mid_rule":            (66, 125, 560, 134),
    "dashed_sep":          (66, 136, 250, 144),
    "subscript_header":    (84, 162, 242, 180),
    "data_row_1":          (84, 179, 242, 201),
    "data_row_2":          (84, 196, 242, 214),
    "data_row_3":          (84, 210, 242, 226),
    "class_label_row":     (84, 229, 242, 247),
    "initial_w":           (368, 62, 470, 92),
    "step_eta":            (330, 89, 424, 106),
    "check_classes":       (330, 108, 500, 127),
    "z_matrix":            (360, 168, 420, 205),
    "yellow_w_box":        (740, 54, 832, 111),
    "ugmented_header":     (66, 250, 250, 262),
    "iteration4_box":      (80, 275, 220, 308),
    "stop_box":            (60, 327, 247, 419),
    "plot_box":            (310, 170, 828, 486),
}


def frame_ink_bbox(path, x0, y0, x1, y1, thresh=200):
    """Ink bbox in FRAME px inside a frame-space window."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    H, W = a.shape[:2]
    s = H / 540.0
    sub = a[int(round(y0 * s)):int(round(y1 * s)) + 1,
            int(round(x0 * s)):int(round(x1 * s)) + 1]
    lum = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    mask = lum < thresh
    if not mask.any():
        return None
    ys, xs = np.where(mask)
    return (x0 + xs.min() / s, x0 + xs.max() / s,
            y0 + ys.min() / s, y0 + ys.max() / s)


def main():
    rows = []
    fails = []
    for name, (wx0, wy0, wx1, wy1) in WINDOWS.items():
        orig = frame_ink_bbox(FRAME, wx0, wy0, wx1, wy1)
        rend = frame_ink_bbox(RENDER, wx0, wy0, wx1, wy1)
        rows.append((name, orig, rend))
        if orig is None:
            fails.append(f"{name}: no ink in the ORIGINAL window {WINDOWS[name]}")
            continue
        if rend is None:
            fails.append(f"{name}: MISSING INK in the render (original has ink there)")
            continue
        d = [rend[i] - orig[i] for i in range(4)]
        worst = max(abs(v) for v in d)
        if worst > TOL:
            fails.append(f"{name}: render ink diverges from the original by {worst:.1f} frame px "
                         f"(dx0 {d[0]:.1f} dx1 {d[1]:.1f} dy0 {d[2]:.1f} dy1 {d[3]:.1f})")

    print("SELF-CHECK slide 046 attempt 1  (render vs original frame ink bboxes)")
    print(f"{'element':20s} {'orig x0..x1 / y0..y1':>34s}   {'render x0..x1 / y0..y1':>34s}   delta")
    for name, orig, rend in rows:
        if orig is None:
            print(f"{name:20s} {'(none)':>34s}   {'' if rend is None else '%.1f..%.1f / %.1f..%.1f' % rend:>34s}")
            continue
        o = "%.1f..%.1f / %.1f..%.1f" % orig
        if rend is None:
            print(f"{name:20s} {o:>34s}   {'MISSING':>34s}")
            continue
        r = "%.1f..%.1f / %.1f..%.1f" % rend
        d = max(abs(rend[i] - orig[i]) for i in range(4))
        print(f"{name:20s} {o:>34s}   {r:>34s}   {d:.1f}")

    # frame containment: no dark ink outside the panel x54..903 y45..540
    a = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
    H = a.shape[0]
    s = H / 540.0
    lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    dark = lum < 190
    outside = int(dark[int(45 * s):int(540 * s), :int(52 * s)].sum()
                  + dark[int(45 * s):int(540 * s), int(905 * s):].sum()
                  + dark[:int(44 * s), :].sum() + dark[int(541 * s):, :].sum())
    if outside:
        fails.append(f"frame containment: {outside} dark px outside the panel x54..903 y45..540")
    print(f"frame containment: {outside} dark px outside the panel")

    if fails:
        print("\nFAILURES:")
        for f in fails:
            print("  - " + f)
        with open(f"{QA}/selfcheck_attempt_1.txt", "w") as fh:
            fh.write("SELF-CHECK slide 046 attempt 1: FAIL\n")
            fh.write("\n".join("  - " + f for f in fails) + "\n")
        sys.exit(1)

    print("\nRESULT: PASS — all element ink bboxes match the original within "
          f"{TOL} frame px; frame containment clean.")
    with open(f"{QA}/selfcheck_attempt_1.txt", "w") as fh:
        fh.write("SELF-CHECK slide 046 attempt 1: PASS\n")
        fh.write(f"all {len(rows)} elements within {TOL} frame px of the original "
                 "frame ink bboxes; frame containment clean.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
