#!/usr/bin/env python3
"""Probe 4: ASCII color maps — y-vector chips (#48), label positions/colors, ones column.
Maps ORIG vs RENDER for (a) y-vector column x82..168 y350..495, (b) bottom label zone x82..420 y438..515."""
import numpy as np
from PIL import Image

Q = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"
D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

r = np.asarray(Image.open(Q + "/render_33.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(D + "/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
SRX, SRY = 2001 / 960.0, 1125 / 540.0  # render px per slide px

def code(px):
    r, g, b = px
    mx, mn = max(r, g, b), min(r, g, b)
    if mx > 235 and mn > 225: return "."          # white
    if abs(r - 233) < 14 and abs(g - 233) < 14 and abs(b - 231) < 16: return ","  # panel gray
    if mx < 110: return "#"                        # dark ink
    sat = mx - mn
    if sat <= 40:
        return "+" if mx < 190 else "-"            # medium gray / light gray
    # saturated: classify hue
    if r > 200 and g > 200 and b < 190: return "Y"  # pale yellow
    if g > 200 and b > 200 and r < 190: return "C"  # pale cyan
    if r > 200 and b > 200 and g < 190: return "M"  # pale pink/orchid
    if r > 150 and g > 110 and b < 100: return "y"  # gold/orange
    if g > 110 and b > 110 and r < 110: return "c"  # teal
    if r > 140 and b > 140 and g < 120: return "m"  # magenta
    if b > 140 and r < 120: return "b"              # blue
    if r > 140 and g < 110 and b < 110: return "R"  # red
    return "s"                                      # other sat

def amap(img, x0, y0, x1, y1, isrender, step, tag):
    sx, sy = (SRX if isrender else 1.0), (SRY if isrender else 1.0)
    print(f"--- {tag} slide x{x0}..{x1} y{y0}..{y1} (step {step}x{step}) ---")
    hdr = "     " + "".join(str((x0 + i * step) // 100 % 10) if (x0 + i * step) % 50 < step else " " for i in range(int((x1 - x0) / step)))
    print(hdr)
    for yy in range(y0, y1, step):
        row = []
        for xx in range(x0, x1, step):
            cx, cy = int(xx * sx), int(yy * sy)
            blk = img[cy:cy + int(sy * step) - 1 or 1, cx:cx + int(sx * step) - 1 or 1]
            flat = blk.reshape(-1, 3)
            # most common code in block
            codes = {}
            for p in flat:
                c = code(p)
                codes[c] = codes.get(c, 0) + 1
            row.append(max(codes, key=codes.get) if codes else "?")
        print("%4d %s" % (yy, "".join(row)))

print("========== ORIGINAL (1px=1slide px) ==========")
amap(o, 82, 350, 168, 495, False, 2, "ORIG y-vector column")
amap(o, 82, 438, 420, 515, False, 3, "ORIG bottom label zone")
print("========== RENDER_33 (2.084 px/slide px) ==========")
amap(r, 82, 350, 168, 495, True, 2, "REND y-vector column")
amap(r, 82, 438, 420, 515, True, 3, "REND bottom label zone")
