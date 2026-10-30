#!/usr/bin/env python3
"""STEP 3: re-cut both Procedure B crop pairs from the CURRENT render (render_5).

Regions (frame px): eq_stack x60..800 y328..425; delta_lines x60..880 y437..539.
Both sides use the SAME frame box, so the crops are geometrically identical by
construction (fixes the earlier 1px size mismatch) and remain matched-scale.
"""
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{V}/unique_slides/slide_036.jpg"
REND = f"{V}/recreated_pptx/qa/slide036/render_5.png"
OUT = f"{V}/recreated_pptx/qa/slide036"

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
sc = r.size[0] / 960.0
print(f"scale {sc:.4f}  orig {o.size}  rend {r.size}")

def cut(name, fx0, fy0, fx1, fy1):
    b = (int(round(fx0)), int(round(fy0)), int(round(fx1)), int(round(fy1)))
    co = o.crop(b)
    cr = r.crop((int(round(fx0*sc)), int(round(fy0*sc)),
                 int(round(fx1*sc)), int(round(fy1*sc))))
    if co.size != cr.size:
        cr = cr.resize(co.size, Image.LANCZOS)
        print(f"  !! resized render crop to match: {cr.size}")
    co.save(f"{OUT}/crop_5_{name}_orig.png")
    cr.save(f"{OUT}/crop_5_{name}_render.png")
    print(f"  {name}: frame box {b} -> both sides {co.size}")

cut("eq_stack", 60, 328, 800, 425)
cut("delta_lines", 60, 437, 880, 539)
