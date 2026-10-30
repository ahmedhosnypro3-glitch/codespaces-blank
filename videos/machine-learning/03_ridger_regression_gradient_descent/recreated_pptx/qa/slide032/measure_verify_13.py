#!/usr/bin/env python3
"""Settle the red vertical at data x=5 (dash vs solid) and the chord end dots."""
from PIL import Image

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORI = Image.open(f"{DECK}/unique_slides/slide_032.jpg").convert("RGB")
REN = Image.open(f"{DECK}/recreated_pptx/qa/slide032/render_11.png").convert("RGB")
S = REN.width / 960.0

def redness(c):
    return c[0] - max(c[1], c[2])

print("== ORIG column x=689: redness profile, runs with redness > 20 ==")
prof = [(y, redness(ORI.getpixel((689, y)))) for y in range(68, 308)]
runs, cur_start = [], None
for y, r in prof:
    if r > 20:
        if cur_start is None:
            cur_start = y
    else:
        if cur_start is not None:
            runs.append((cur_start, y - 1)); cur_start = None
if cur_start is not None:
    runs.append((cur_start, 307))
print(f"  {len(runs)} runs:")
for a, b in runs:
    print(f"    y{a}..{b} (h={b-a+1})")

print("\n== ORIG column x=688: same ==")
prof = [(y, redness(ORI.getpixel((688, y)))) for y in range(68, 308)]
runs, cur_start = [], None
for y, r in prof:
    if r > 20:
        if cur_start is None:
            cur_start = y
    else:
        if cur_start is not None:
            runs.append((cur_start, y - 1)); cur_start = None
if cur_start is not None:
    runs.append((cur_start, 307))
print(f"  {len(runs)} runs: " + ", ".join(f"y{a}..{b}" for a, b in runs))

print("\n== ORIG chord end dots: dark-in-column census near x=651..655 and x=722..726 ==")
for xr in (650, 651, 652, 653, 654, 655, 720, 722, 724, 726, 727):
    column = [y for y in range(60, 230) if sum(ORI.getpixel((xr, y))) < 400]
    if column:
        print(f"  x={xr}: dark y {column[0]}..{column[-1]} n={len(column)}")
    else:
        print(f"  x={xr}: none")

print("\n== REND chord end dots: render columns ==")
for xr in (653.5, 687.5, 722.5):
    x = int(xr * S)
    column = [y for y in range(int(60 * S), int(230 * S)) if sum(REN.getpixel((x, y))) < 400]
    if column:
        print(f"  x={xr}: dark y {column[0]/S:.0f}..{column[-1]/S:.0f} n={len(column)}")
    else:
        print(f"  x={xr}: none")

print("\n== ORIG dark ink bbox in x648..658, y130..165 (left dot) ==")
pts = [(x, y) for x in range(646, 660) for y in range(128, 168) if sum(ORI.getpixel((x, y))) < 500]
if pts:
    print(f"  x {min(p[0] for p in pts)}..{max(p[0] for p in pts)}  y {min(p[1] for p in pts)}..{max(p[1] for p in pts)}  n={len(pts)}")
pts = [(x, y) for x in range(716, 732) for y in range(128, 168) if sum(ORI.getpixel((x, y))) < 500]
if pts:
    print(f"  RIGHT: x {min(p[0] for p in pts)}..{max(p[0] for p in pts)}  y {min(p[1] for p in pts)}..{max(p[1] for p in pts)}  n={len(pts)}")
