#!/usr/bin/env python3
"""ASCII ink map of the chord region in the ORIG, to settle dots vs plain chord."""
from PIL import Image

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORI = Image.open(f"{DECK}/unique_slides/slide_032.jpg").convert("RGB")
REN = Image.open(f"{DECK}/recreated_pptx/qa/slide032/render_11.png").convert("RGB")
S = REN.width / 960.0

def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

def amap(img, x0, x1, y0, y1, s=1.0, thr=140, step=2, lo=None, hi=None):
    print(f"  {img.size} x0={x0}..{x1} y0={y0}..{y1} thr={thr}")
    hdr = "     " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1, step))
    print("     " + "".join(str(x % 10) if x % 10 == 0 else "." for x in range(x0, x1, step)))
    for y in range(y0, y1, step):
        row = ""
        for x in range(x0, x1, step):
            c = img.getpixel((int(x * s), int(y * s)))
            row += "#" if lum(c) < thr else ("+" if lum(c) < 200 else ".")
        print(f"  {y:>4} {row}")

print("== ORIG chord+dot region x640..740 y128..170 ==")
amap(ORI, 640, 740, 128, 170, s=1.0)

print("\n== REND same region ==")
amap(REN, 640, 740, 128, 170, s=S)
