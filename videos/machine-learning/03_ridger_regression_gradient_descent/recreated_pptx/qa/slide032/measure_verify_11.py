#!/usr/bin/env python3
"""Focused probes: curve trace, red-dash vertical, band fills at clean y, chord gaps."""
from PIL import Image

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
REN = Image.open(f"{DECK}/recreated_pptx/qa/slide032/render_11.png").convert("RGB")
ORI = Image.open(f"{DECK}/unique_slides/slide_032.jpg").convert("RGB")
S = REN.width / 960.0

def is_curve(c):
    r, g, b = c
    return b > r + 14 and b > 95 and 70 < g < 200

def is_red(c):
    r, g, b = c
    return r > 110 and g < 105 and b < 105

print("== curve trace: for each frame x, curve-ink y (centroid) ==")
print(f"{'x':>5} {'ORIG y':>8} {'ORIG colour':>10} | {'REND y':>8} {'REND colour':>10} | {'analytic':>8} {'dREND':>7} {'dORIG':>7}")
XC, SX, YC, SY = 630.5, 11.5, 266, 12
maxd_o = maxd_r = 0.0
for fx in range(643, 734, 4):
    # ORIG
    yo = [(y, ORI.getpixel((fx, y))) for y in range(67, 308) if is_curve(ORI.getpixel((fx, y)))]
    # REND
    xr = int(fx * S)
    yr = [(y / S, REN.getpixel((xr, y))) for y in range(int(67 * S), int(308 * S)) if is_curve(REN.getpixel((xr, y)))]
    d = (fx - XC) / SX
    v = (d - 5) ** 2 + 1
    fy = YC - SY * v
    cyo = sum(y for y, _ in yo) / len(yo) if yo else float("nan")
    cyr = sum(y for y, _ in yr) / len(yr) if yr else float("nan")
    co = yo[len(yo) // 2][1] if yo else (0, 0, 0)
    cr = yr[len(yr) // 2][1] if yr else (0, 0, 0)
    do = cyo - fy if yo else float("nan")
    dr = cyr - fy if yr else float("nan")
    if yo: maxd_o = max(maxd_o, abs(do))
    if yr: maxd_r = max(maxd_r, abs(dr))
    print(f"{fx:>5} {cyo:8.1f} {co[0]:02X}{co[1]:02X}{co[2]:02X} | {cyr:8.1f} {cr[0]:02X}{cr[1]:02X}{cr[2]:02X} | {fy:8.1f} {dr:7.2f} {do:7.2f}")
print(f"max |curve y - analytic|: ORIG {maxd_o:.2f} px, REND {maxd_r:.2f} px")

print("\n== RED-ish vertical strokes inside the plot (ORIG) ==")
for fx in range(574, 810):
    n = sum(1 for y in range(68, 308) if is_red(ORI.getpixel((fx, y))))
    if n > 3:
        ys = [y for y in range(68, 308) if is_red(ORI.getpixel((fx, y)))]
        print(f"  x={fx}: {n} red px, y {ys[0]}..{ys[-1]}, gaps={[ys[i+1]-ys[i] for i in range(len(ys)-1) if ys[i+1]-ys[i] > 3][:8]}")

print("\n== RED-ish vertical strokes inside the plot (REND) ==")
for fx in range(int(574 * S), int(810 * S)):
    n = sum(1 for y in range(int(68 * S), int(308 * S)) if is_red(REN.getpixel((fx, y))))
    if n > 6:
        ys = [y for y in range(int(68 * S), int(308 * S)) if is_red(REN.getpixel((fx, y)))]
        print(f"  x={fx/S:.1f}: {n} red px, y {ys[0]/S:.0f}..{ys[-1]/S:.0f}, gaps={[round((ys[i+1]-ys[i])/S,1) for i in range(len(ys)-1) if ys[i+1]-ys[i] > 6][:8]}")

print("\n== band fills at clean y (avoid split lines) ==")
for nm, fx, y0, y1 in (("band1", 330, 344, 383), ("band2", 330, 387, 424),
                        ("band3", 330, 431, 468), ("band4", 400, 472, 494),
                        ("band5", 400, 497, 517)):
    fy = y0 + 7
    co = ORI.getpixel((fx, fy)); cr = REN.getpixel((int(fx * S), int(fy * S)))
    print(f"  {nm} ({fx},{fy}): ORIG {co[0]:02X}{co[1]:02X}{co[2]:02X}  REND {cr[0]:02X}{cr[1]:02X}{cr[2]:02X}")

print("\n== chord gaps at y146 ==")
for nm, img, s in (("ORIG", ORI, 1.0), ("REND", REN, S)):
    y = int(146 * s)
    dark = [x / s for x in range(int(648 * s), int(730 * s)) if sum(img.getpixel((x, y))) < 330]
    gaps = []
    for i in range(len(dark) - 1):
        if dark[i + 1] - dark[i] > 0.6:
            gaps.append((round(dark[i], 1), round(dark[i + 1], 1)))
    print(f"  {nm}: n={len(dark)} span {dark[0]:.1f}..{dark[-1]:.1f} gaps={gaps}")

print("\n== title ink bbox (y 70..95 only, x 70..600) ==")
for nm, img, s in (("ORIG", ORI, 1.0), ("REND", REN, S)):
    xs_all = []
    for y in range(int(70 * s), int(95 * s)):
        row = [x / s for x in range(int(70 * s), int(600 * s)) if sum(img.getpixel((x, y))) < 690]
        if row:
            xs_all.append((row[0], row[-1], y / s))
    x0 = min(a for a, _, _ in xs_all); x1 = max(b for _, b, _ in xs_all)
    y0 = min(y for *_, y in xs_all); y1 = max(y for *_, y in xs_all)
    print(f"  {nm}: ink x {x0:.1f}..{x1:.1f}  y {y0:.1f}..{y1:.1f}  rows={len(xs_all)}")
