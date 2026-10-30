#!/usr/bin/env python3
"""Render slide_026 equations as 2D PNGs (matplotlib mathtext, 600 dpi).

Original frame shows STACKED fractions for the sigmoid and tanh definitions
(1 over 1+e^-x, sinh x over cosh x) — professional 2D format per the house
math rule. Each asset is a tight transparent PNG; addImage uses w = px/600.
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 6
OUTDIR = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
          "09_introduction_to_neural_networks/recreated_pptx/build")


def render(mathtext, out, fontsize, color):
    fig = plt.figure(figsize=(14, 6), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${mathtext}$", fontsize=fontsize, color=color,
             ha="center", va="center")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {mathtext!r}")
    y0 = max(rows[0] - PAD_PX, 0); y1 = min(rows[-1] + PAD_PX, buf.shape[0])
    x0 = max(cols[0] - PAD_PX, 0); x1 = min(cols[-1] + PAD_PX, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    plt.close(fig)
    return {"path": out, "w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "w_in": round(float(x1 - x0) / DPI, 5),
            "h_in": round(float(y1 - y0) / DPI, 5),
            "dpi": DPI, "font_size_pt": fontsize, "color": color,
            "image": out.rsplit("/", 1)[-1], "mathtext": mathtext}


FS = 18
eqs = [
    ("eq_s026_row1",
     r"f(x) = \mathrm{Sigmoid}(x) = \frac{1}{1+e^{-x}} \;\Rightarrow\; f'(x) = f(x)(1-f(x))",
     "eq_s026_row1.png", "#333333"),
    ("eq_s026_row2",
     r"f(x) = \tanh(x) = \frac{\sinh x}{\cosh x} \;\Rightarrow\; f'(x) = 1-f(x)^{2}",
     "eq_s026_row2.png", "#333333"),
    ("eq_s026_box1",
     r"\mathrm{at}\ x=0\quad f(0)=0.5\quad f'(0)=0.25",
     "eq_s026_box1.png", "#333333"),
    ("eq_s026_box2",
     r"\mathrm{at}\ x=0\quad f(0)=0\quad f'(0)=1",
     "eq_s026_box2.png", "#333333"),
]

results = []
for name, mt, fn, color in eqs:
    info = render(mt, f"{OUTDIR}/{fn}", FS, color)
    info["name"] = name
    results.append(info)
    print(json.dumps({"name": name, "w_in": info["w_in"], "h_in": info["h_in"]}))

with open(f"{OUTDIR}/slide_026_equations.json", "w") as f:
    json.dump({"slide": "026", "equations": results}, f, indent=2)
print("wrote slide_026_equations.json")
