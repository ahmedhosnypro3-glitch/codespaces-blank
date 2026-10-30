#!/usr/bin/env python3
"""w051_fine_dump: colour-coded fine ASCII of the zones that decide the att2 fixes.
ORIG = slide_051.jpg (960x540); RENDER = render_2.png (2001x1125, 2.0835x frame).
Each px -> r (red) / b (blue) / g (green) / # (dark ink) / . (light)."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = f"{NS}/recreated_pptx/qa/slide051/w051_fine_dump_raw.txt"

IMGS = {}
for name, path in (("ORIG", f"{NS}/unique_slides/slide_051.jpg"),
                   ("RENDER", f"{NS}/recreated_pptx/qa/slide051/render_2.png")):
    im = Image.open(path).convert("RGB")
    IMGS[name] = (np.asarray(im).astype(int), im.size[0] / 960.0)

lines = []
def P(*a):
    t = " ".join(str(x) for x in a); lines.append(t); print(t)

def colorcode(name, x0, x1, y0, y1, step=1):
    img, s = IMGS[name]
    z = img[int(y0*s):int(y1*s), int(x0*s):int(x1*s)]
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = (R > 110) & (R-G > 50) & (R-B > 40)
    blue = (B > 90) & (B-R > 25) & (B-G > 10) & (G >= R)
    green = (G > 80) & (G-R > 15) & (G-B > 15)
    lum = 0.299*R + 0.587*G + 0.114*B
    dark = lum < 200
    P(f" {name} x{x0}..{x1} y{y0}..{y1} step {step} (col = x0 + k*{step}; row = y0 + j*{step}):")
    for yy in range(0, z.shape[0], step):
        row = []
        for xx in range(0, z.shape[1], step):
            if red[yy, xx:xx+step].any(): row.append("r")
            elif green[yy, xx:xx+step].any(): row.append("g")
            elif blue[yy, xx:xx+step].any(): row.append("b")
            elif dark[yy, xx:xx+step].any(): row.append("#")
            else: row.append(".")
        P(f"  {y0+yy//s if s==1 else round(y0+yy/s,1):>6} " + "".join(row))

P("== w051_fine_dump ==")
# d(Z1) row: card x274..853 top y140; original content per build comment:
# label x283..312, = x319..324, blue glyphs x335/351/369, green bars x381..382/x404..405,
# = x412..417, val x423, arrow x500..509, condition x522
P("\n## d-box1 left half")
colorcode("ORIG", 274, 430, 145, 197, 1)
P("")
colorcode("RENDER", 274, 430, 145, 197, 2)
P("\n## d-box1 right half (arrow + condition + class)")
colorcode("ORIG", 490, 700, 150, 185, 2)
P("")
colorcode("RENDER", 490, 700, 150, 185, 2)
P("\n## red Step zone")
colorcode("ORIG", 358, 448, 58, 92, 1)
P("")
colorcode("RENDER", 358, 448, 58, 92, 2)

open(OUT, "w").write("\n".join(lines) + "\n")
print("\nbanked:", OUT)
