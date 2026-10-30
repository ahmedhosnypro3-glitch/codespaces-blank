#!/usr/bin/env python3
"""Curve + band census for slide 032 — render_8 vs unique_slides/slide_032.jpg.

Locates the parabola's actual ink in both images by column scans, then
compares its y-position at matched x. Also samples each iteration-table band
at text-free columns.
"""
from PIL import Image

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
REN = Image.open(f"{DECK}/recreated_pptx/qa/slide032/render_8.png").convert("RGB")
ORI = Image.open(f"{DECK}/unique_slides/slide_032.jpg").convert("RGB")
S = REN.width / 960.0
print(f"scale={S:.4f}")

def scan(img, fx, y0, y1, s=S, want="curve"):
    """Return list of (y, colour) for non-white, non-gridline ink in column fx."""
    out = []
    xs = int(round(fx * s))
    for yy in range(int(y0 * s), int(y1 * s)):
        c = img.getpixel((xs, yy))
        r, g, b = c
        # exclude near-white and the light gridlines
        if r > 235 and g > 235 and b > 235:
            continue
        if abs(r - 217) < 12 and abs(g - 217) < 12 and abs(b - 217) < 12:
            continue
        out.append((yy / s, c))
    return out

PROBE_X = [645, 655, 665, 675, 685, 695, 705, 715, 725, 732]
print("\n== column scans: curve ink y (frame px) ==")
print(f"{'x':>5} | {'ORIG curve y':>22} | {'REND curve y':>22}")
for fx in PROBE_X:
    o = scan(ORI, fx, 67, 307, s=1.0)
    r = scan(REN, fx, 67, 307, s=S)
    oy = [f"{y:.0f}:{c[0]:02X}{c[1]:02X}{c[2]:02X}" for y, c in o]
    ry = [f"{y:.1f}:{c[0]:02X}{c[1]:02X}{c[2]:02X}" for y, c in r]
    print(f"{fx:>5} | {' '.join(oy[:6]):>22} | {' '.join(ry[:6]):>22}")

# analytic prediction
XC, SX, YC, SY = 630.5, 11.5, 266, 12
print("\n== analytic parabola y at probe x (f(x)=(x-5)^2+1) ==")
for fx in PROBE_X:
    d = (fx - XC) / SX
    v = (d - 5) ** 2 + 1
    fy = YC - SY * v
    print(f"  x={fx} data={d:.3f} f={v:.3f} frame_y={fy:.1f}")

print("\n== iteration-table bands at text-free columns ==")
for nm, fx, fy0, fy1 in (("band1", 310, 344, 383), ("band2", 310, 387, 424),
                          ("band3", 310, 431, 468), ("band4", 380, 472, 494),
                          ("band5", 380, 497, 517)):
    # sample the middle of the band, avoid label column and any text
    co = ORI.getpixel((fx, (fy0 + fy1) // 2))
    cr = REN.getpixel((int(fx * S), int((fy0 + fy1) // 2 * S)))
    print(f"  {nm}: ORIG {co[0]:02X}{co[1]:02X}{co[2]:02X}  REND {cr[0]:02X}{cr[1]:02X}{cr[2]:02X}")

print("\n== chord presence: full row census at frame y=146 ==")
for nm, img, s in (("ORIG", ORI, 1.0), ("REND", REN, S)):
    y = int(146 * s)
    dark = [x / s for x in range(int(650 * s), int(730 * s)) if sum(img.getpixel((x, y))) < 330]
    if dark:
        print(f"  {nm}: dark x {dark[0]:.1f}..{dark[-1]:.1f}, n={len(dark)}")
    else:
        print(f"  {nm}: none at y146")

print("\n== dashed red vertical at data x=5 (frame x=688) ==")
for nm, img, s in (("ORIG", ORI, 1.0), ("REND", REN, S)):
    x = int(688 * s)
    reds = [y / s for y in range(int(67 * s), int(309 * s))
            if (lambda c: c[0] > 130 and c[1] < 110 and c[2] < 110)(img.getpixel((x, y)))]
    if reds:
        # gaps
        gaps, prev, cur = [], reds[0], [reds[0]]
        for y in reds[1:]:
            if y - prev > 3:
                gaps.append((cur[0], cur[-1])); cur = []
            cur.append(y); prev = y
        gaps.append((cur[0], cur[-1]))
        print(f"  {nm}: {len(gaps)} dash segments -> {[(round(a), round(b)) for a, b in gaps]}")
    else:
        print(f"  {nm}: none")

print("\n== title ink bbox (whole row census) ==")
for nm, img, s in (("ORIG", ORI, 1.0), ("REND", REN, S)):
    ys = [y for y in range(int(55 * s), int(95 * s))]
    xs_all = []
    for y in ys:
        row = [x for x in range(int(70 * s), int(600 * s))
               if sum(img.getpixel((x, y))) < 690]
        if row:
            xs_all.append((row[0] / s, row[-1] / s, y / s))
    if xs_all:
        x0 = min(a for a, _, _ in xs_all); x1 = max(b for _, b, _ in xs_all)
        y0 = min(y for *_, y in xs_all); y1 = max(y for *_, y in xs_all)
        print(f"  {nm}: ink x {x0:.1f}..{x1:.1f}  y {y0:.1f}..{y1:.1f}")
