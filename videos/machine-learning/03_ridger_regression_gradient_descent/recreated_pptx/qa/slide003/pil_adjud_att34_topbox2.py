#!/usr/bin/env python3
"""Probe 2: fine per-column run histograms around the ambiguous strokes,
curvature profiles for orig 409/451/475, render control profiles, ASCII maps."""
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg"
REND = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/render_34.png"
S = 2001 / 960.0

def load(p): return Image.open(p).convert("RGB")

def col_runs(im, x, y0, y1, thresh):
    px = im.load(); best = 0; bs = be = 0; run = 0; start = 0
    for y in range(y0, y1):
        r, g, b = px[x, y]
        if (r + g + b) / 3 < thresh:
            if run == 0: start = y
            run += 1
            if run > best: best, bs, be = run, start, y
        else: run = 0
    return best, bs, be

def prof(im, x, y0, y1, thresh=200, halfw=3, step=10):
    px = im.load(); out = []
    for y in range(y0, y1, step):
        num = 0.0; den = 0
        for xx in range(x - halfw, x + halfw + 1):
            r, g, b = px[xx, y]
            d = 255 - (r + g + b) / 3
            if d > (255 - thresh): num += xx * d; den += d
        out.append((y, round(num / den, 1) if den else None))
    return out

orig = load(ORIG); rend = load(REND)

print("### ORIG per-column max-run, x395..425 y150..265 (thresh 200 / 160)")
for x in range(395, 426):
    b2 = col_runs(orig, x, 150, 265, 200)[0]; b1 = col_runs(orig, x, 150, 265, 160)[0]
    if b2 >= 20: print(f"  x={x}: run200={b2} run160={b1}")
print("### ORIG per-column max-run, x440..485 y150..265")
for x in range(440, 486):
    b2 = col_runs(orig, x, 150, 265, 200)[0]; b1 = col_runs(orig, x, 150, 265, 160)[0]
    if b2 >= 20: print(f"  x={x}: run200={b2} run160={b1}")
print("### ORIG per-column max-run, x545..565 y145..265")
for x in range(545, 566):
    b2 = col_runs(orig, x, 145, 265, 200)[0]; b1 = col_runs(orig, x, 145, 265, 160)[0]
    if b2 >= 20: print(f"  x={x}: run200={b2} run160={b1}")
print("### ORIG per-column max-run, x290..303 y150..260 (yellowL zone)")
for x in range(290, 304):
    b2 = col_runs(orig, x, 150, 260, 200)[0]
    if b2 >= 20: print(f"  x={x}: run200={b2}")

print()
print("### ORIG curvature: cyanR@409, midcolL@451, midcolR@475")
for xc, y0, y1 in [(409, 162, 245), (451, 162, 245), (475, 163, 245)]:
    p = prof(orig, xc, y0, y1)
    print(f"  x~{xc}: " + " ".join(f"{y}:{c}" for y, c in p))

print()
print("### RENDER control: curvature of drawn straight lines (scaled coords)")
for xc, tag in [(296.5, "yL"), (331.5, "yR"), (373.5, "cL"), (414.5, "cR"), (517.5, "pL"), (556.5, "pR")]:
    xi = int(round(xc * S))
    p = prof(rend, xi, int(165 * S), int(245 * S))
    cs = [c for _, c in p if c is not None]
    spread = (max(cs) - min(cs)) if cs else None
    print(f"  {tag} x_slide={xc}: spread={spread}  " + " ".join(f"{y / S:.0f}:{c / S:.1f}" for y, c in p))

print()
print("### ASCII map ORIG x288..340 (yellow L+R delims), y152..262, thresh 210")
px = orig.load()
for y in range(152, 263, 2):
    row = ""
    for x in range(288, 341):
        r, g, b = px[x, y]
        v = (r + g + b) / 3
        row += "#" if v < 120 else ("+" if v < 200 else ".")
    print(f"  {y:3d} {row}")
print()
print("### ASCII map ORIG x443..482 (midcol delims), y152..262")
for y in range(152, 263, 2):
    row = ""
    for x in range(443, 483):
        r, g, b = px[x, y]
        v = (r + g + b) / 3
        row += "#" if v < 120 else ("+" if v < 200 else ".")
    print(f"  {y:3d} {row}")
