#!/usr/bin/env python3
"""Precise extents: (a) white table-body fill in orig; (b) peach bottom cells."""
from PIL import Image
import os

os.chdir("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent")
o = Image.open("unique_slides/slide_019.jpg").convert("RGB")
r = Image.open("recreated_pptx/qa/slide019/render_18.png").convert("RGB")
S = r.size[0] / o.size[0]
op, rp = o.load(), r.load()

def cls(p):
    R, G, B = p
    if R > 245 and G > 245 and B > 245: return "W"
    if R > 230 and G > 225 and B < 165: return "Y"
    if abs(R-233) < 12 and abs(G-233) < 12 and abs(B-231) < 12: return "G"
    if R > 240 and 200 < G < 240 and 170 < B < 215: return "p"  # peach FAE0C8
    if R > 240 and G > 245 and B > 215: return "c"
    if R > 215 and G > 245 and B > 215: return "m"
    return "?"

print("== white-zone vertical extent: classify x=340 (inside NO REG test grid) & x=100 (outlier col) & x=700 (RIDGE10), y150..535 ==")
for x in (100, 340, 700):
    line_o = "".join(cls(op[x, y]) for y in range(150, 536, 5))
    line_r = "".join(cls(rp[int(x*S), int(y*S)]) for y in range(150, 536, 5))
    print(f"x{x:3d} O {line_o}")
    print(f"     R {line_r}")
print("  (y runs 150..535 step5; first char y150)")

print("\n== white-zone horizontal extent at y=340 (group2, between bands) & y=210 ==")
for y in (210, 340):
    line_o = "".join(cls(op[x, y]) for x in range(56, 906, 5))
    line_r = "".join(cls(rp[int(x*S), int(y*S)]) for x in range(56, 906, 5))
    print(f"y{y:3d} O {line_o}")
    print(f"     R {line_r}")
print("  (x runs 56..905 step5)")

print("\n== bottom strip y500..535 fine map (x100..905 step5, y step3) ==")
for y in range(500, 536, 3):
    line_o = "".join(cls(op[x, y]) for x in range(100, 906, 5))
    print(f"y{y:3d} O {line_o}")
print("  (x runs 100..905 step5)")
