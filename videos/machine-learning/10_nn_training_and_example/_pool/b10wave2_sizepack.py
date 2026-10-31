#!/usr/bin/env python3
"""Build ONE combined visual pack: original vs render for the where strip and
the cyan chain box, scaled to equal width for direct size comparison."""
from PIL import Image, ImageDraw

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
OUT = f"{NS}/_pool/tmp_b10wave2/s020_size_pack.png"
S = 960 / 13.3333
IN = 2001 / 13.3333

O = Image.open(f"{NS}/unique_slides/slide_020.jpg").convert("RGB")
R = Image.open(f"{NS}/qa/slide020/b10wave2/render-1.png").convert("RGB")


def cut(im, sc, x0, y0, x1, y1):
    X0, Y0, X1, Y1 = (int(v * sc) for v in (x0, y0, x1, y1))
    return im.crop((X0, Y0, X1, Y1))


W = 1500
parts = []
for label, region in (("WHERE STRIP", (0.60, 6.60, 9.05, 7.45)),
                      ("CYAN BOX", (0.60, 0.60, 5.45, 3.30))):
    for tag, im, sc in (("ORIGINAL", O, S), ("RECREATION", R, IN)):
        c = cut(im, sc, *region)
        h = max(1, int(c.size[1] * W / c.size[0]))
        parts.append((f"{label} — {tag}", c.resize((W, h), Image.LANCZOS)))

pad = 26
total_h = sum(p[1].size[1] + pad for p in parts) + pad
sheet = Image.new("RGB", (W, total_h), "white")
d = ImageDraw.Draw(sheet)
y = pad // 2
for label, img in parts:
    d.text((6, y + 4), label, fill="red")
    y += 18
    sheet.paste(img, (0, y))
    y += img.size[1] + pad
sheet.save(OUT)
print(sheet.size, OUT)
