#!/usr/bin/env python3
"""Measure colors in the main-diagram panel: weight label colors, node circle fills."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
LX, LY, HX, HY = 85, 102, 551, 302
sub = a[LY:HY, LX:HX]


def census(y0, y1, x0, x1, label):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    # drop near-gray (panel bg)
    r, g, b = reg[:, 0], reg[:, 1], reg[:, 2]
    sat = reg.max(axis=1) - reg.min(axis=1)
    colored = reg[sat > 30]
    print(f"\n-- {label}  x[{x0}..{x1}] y[{y0}..{y1}]  px={len(reg)} colored={len(colored)}")
    if len(colored) == 0:
        print("   (no saturated color)")
        return
    # classify
    cls = {
        "red": (colored[:, 0] > colored[:, 1] + 40) & (colored[:, 0] > colored[:, 2] + 40),
        "green": (colored[:, 1] > colored[:, 0] + 25) & (colored[:, 1] > colored[:, 2] + 25),
        "blue": (colored[:, 2] > colored[:, 0] + 25) & (colored[:, 2] > colored[:, 1] + 20),
        "purple": (colored[:, 0] > colored[:, 1] + 12) & (colored[:, 2] > colored[:, 1] + 12),
    }
    for k, m in cls.items():
        if m.sum() > 20:
            mcol = colored[m].mean(axis=0).astype(int)
            print(f"   {k}: n={int(m.sum())} mean=#{mcol[0]:02X}{mcol[1]:02X}{mcol[2]:02X} "
                  f"range=({colored[m].min(axis=0)}..{colored[m].max(axis=0)})")
    dark = (reg.sum(axis=1) < 250)
    if dark.sum() > 20:
        print(f"   dark-ink: n={int(dark.sum())}")


print("=== weight-label strip: labels sit between inputs and nodes (x 120..300) ===")
census(140, 280, 120, 300, "left input->node weight strip")
census(140, 170, 120, 300, "row 1 weights (x1->n1, x2->n1)")
census(170, 230, 120, 300, "row 2 weights (x1->n2, x2->n2)")
census(230, 290, 120, 300, "row 3 weights")

print("\n=== node circles region (x 300..420) ===")
census(140, 290, 300, 420, "nodes region")
print("\n=== step box (purple) x[415..470] y[194..226] ===")
census(194, 226, 415, 471, "step box")
print("\n=== green blob x[280..352] y[202..274] ===")
census(202, 275, 280, 353, "green blob")
print("\n=== right of step box (O/P area) x[470..551] ===")
census(200, 240, 470, 551, "O/P area")

# Teal test: is there any cyan/teal fill anywhere in the panel?
print("\n=== teal test in whole panel ===")
r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
teal = (g > 120) & (b > 120) & (abs(g - b) < 60) & (r < g - 20)
print(f"teal-ish px in panel: {int(teal.sum())}")
lbl = (r > 150) & (g > 150) & (b < 160) & (abs(r - g) < 50)
print(f"light-yellow px in panel: {int(lbl.sum())}")
