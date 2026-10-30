#!/usr/bin/env python3
"""ASCII ink maps of the outlier-column delimiter zone, orig vs render_23.
Window: frame x56..90, y188..300 (group 1) — delimiter + entries left edge."""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = Image.open(f"{BASE}/unique_slides/slide_019.jpg").convert("RGB")
rend = Image.open(f"{BASE}/recreated_pptx/qa/slide019/render_23.png").convert("RGB")
SX = rend.size[0] / orig.size[0]
SY = rend.size[1] / orig.size[1]

def ascii_map(img, x0, y0, x1, y1, sx=1.0, sy=1.0, step=2):
    print(f"  window frame x{x0}..{x1} y{y0}..{y1}  (1 char = {step}px wide, {step}px tall)")
    hdr = "     " + "".join(str((x0 + i) % 10) for i in range(0, x1 - x0, step))
    print(hdr)
    for fy in range(y0, y1, step):
        row = []
        for fx in range(x0, x1, step):
            ink = 0
            n = 0
            for dy in range(step):
                for dx in range(step):
                    px_x, px_y = int((fx + dx) * sx), int((fy + dy) * sy)
                    if px_x >= img.size[0] or px_y >= img.size[1]:
                        continue
                    r, g, b = img.getpixel((px_x, px_y))
                    n += 1
                    if r < 150 and g < 150 and b < 150:
                        ink += 1
            frac = ink / max(n, 1)
            row.append(" " if frac == 0 else ("░" if frac < 0.34 else ("▒" if frac < 0.67 else "█")))
        print(f"y{fy:3d} " + "".join(row))

print("== ORIGINAL ==")
ascii_map(orig, 56, 188, 92, 300)
print()
print("== RENDER_23 (scaled to frame) ==")
ascii_map(rend, 56, 188, 92, 300, sx=SX, sy=SY)
