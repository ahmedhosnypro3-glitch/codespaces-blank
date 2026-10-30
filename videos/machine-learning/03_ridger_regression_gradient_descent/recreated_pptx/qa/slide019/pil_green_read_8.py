#!/usr/bin/env python3
"""Read the green predicted-y digits of the NO REG column, render_6 vs render_8.

Renders are 2001x1125 (150 dpi, 2.0833 px per pt); the original frame is 960x540
(1 px == 1 pt). Green ink is isolated as pixels where G dominates R and B, then
each value is cropped in native render resolution so the glyphs are legible.
"""
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019"
SCALE = 150 / 72.0


def is_green(c):
    r, g, b = c
    return g > 60 and g - r > 35 and g - b > 35


def show(path, label, frame_boxes):
    im = Image.open(path).convert("RGB")
    px = im.load()
    print(f"===== {label} ({path}) =====")
    for name, (fx0, fy0, fx1, fy1) in frame_boxes:
        x0, x1 = int(fx0 * SCALE), int(fx1 * SCALE)
        y0, y1 = int(fy0 * SCALE), int(fy1 * SCALE)
        print(f"--- {name}: frame x{fx0:.0f}..{fx1:.0f} y{fy0:.0f}..{fy1:.0f} "
              f"-> render x{x0}..{x1} y{y0}..{y1} ---")
        for y in range(y0, y1):
            line = "".join("#" if is_green(px[x, y]) else "." for x in range(x0, x1))
            if "#" in line:
                print(f"{y:5d} {line}")
        print()


# NO REG column: the three y-values per row group, in frame coordinates.
boxes = []
for row, (fy0, fy1) in enumerate([(246, 262), (351, 367), (461, 477)], start=1):
    for idx, (fx0, fx1) in enumerate([(203, 232), (261, 290), (319, 348)], start=1):
        boxes.append((f"rowgroup{row} value{idx}", (fx0, fy0, fx1, fy1)))

show(f"{QA}/render_6.png", "RENDER_6 (judged by attempt 6)", boxes)
show(f"{QA}/render_8.png", "RENDER_8 (current)", boxes)
