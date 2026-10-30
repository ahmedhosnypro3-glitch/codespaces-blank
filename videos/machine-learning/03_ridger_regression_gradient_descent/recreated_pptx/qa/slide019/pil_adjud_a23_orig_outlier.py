#!/usr/bin/env python3
"""High-fidelity outlier-column scan of the ORIGINAL frame: where is any
delimiter ink? Blue-ink census + 1px ASCII maps, all three groups."""
from PIL import Image
from collections import Counter

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = Image.open(f"{BASE}/unique_slides/slide_019.jpg").convert("RGB")

def census(x0, y0, x1, y1, thr=190):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = orig.getpixel((x, y))
            if r < thr and g < thr and b < thr:
                c[(r // 24 * 24, g // 24 * 24, b // 24 * 24)] += 1
    return c

print("== color census x56..125, y185..300 (group1 zone, thr190) ==")
for col, n in census(56, 185, 125, 300).most_common(10):
    print(f"  {col}: {n}")

def blue_map(x0, y0, x1, y1, step=2):
    print(f"  BLUE-ink map frame x{x0}..{x1} y{y0}..{y1} step {step}")
    hdr = "     " + "".join(str((x0 + i) % 10) for i in range(0, x1 - x0, step))
    print(hdr)
    for fy in range(y0, y1, step):
        row = []
        for fx in range(x0, x1, step):
            n = ink = 0
            for dy in range(step):
                for dx in range(step):
                    r, g, b = orig.getpixel((fx + dx, fy + dy))
                    n += 1
                    if b > r + 30 and b > g + 30 and b > 60:  # blue-dominant
                        ink += 1
            frac = ink / n
            row.append(" " if frac == 0 else ("░" if frac < 0.34 else ("▒" if frac < 0.67 else "█")))
        print(f"y{fy:3d} " + "".join(row))

print("\n== BLUE-ink (bracket candidates), group 1 ==")
blue_map(56, 185, 130, 300)
print("\n== BLUE-ink, groups 2+3 (y315..510) ==")
blue_map(56, 315, 130, 510)

# any ink at all between rule and entries? x67..83, y185..300, all colors, thr 200
print("\n== all-ink census x67..83 y185..300 thr200 ==")
print(census(67, 185, 83, 300, thr=200).most_common(8))
print("== all-ink census x67..83 y315..510 thr200 ==")
print(census(67, 315, 83, 510, thr=200).most_common(8))
# entries zone x84..120
print("== all-ink census x84..120 y185..300 thr200 ==")
print(census(84, 185, 120, 300, thr=200).most_common(8))
