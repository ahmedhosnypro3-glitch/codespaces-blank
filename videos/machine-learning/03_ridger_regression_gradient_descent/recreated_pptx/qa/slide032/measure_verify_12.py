#!/usr/bin/env python3
"""Settle: black chord extent at y146; red vertical at x~687; column dumps."""
from PIL import Image

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORI = Image.open(f"{DECK}/unique_slides/slide_032.jpg").convert("RGB")
REN = Image.open(f"{DECK}/recreated_pptx/qa/slide032/render_11.png").convert("RGB")
S = REN.width / 960.0

def h(c):
    return "%02X%02X%02X" % c

print("== ORIG row y=146 across the plot (x 570..810, every 4) ==")
for x in range(570, 811, 4):
    print(f"  x{x}: {h(ORI.getpixel((x, 146)))}", end="")
    if (x - 570) // 4 % 6 == 5:
        print()
print()

print("\n== ORIG row y=145 vs 147 at x 576..660 ==")
for x in range(576, 661, 4):
    print(f"  x{x}: y145 {h(ORI.getpixel((x,145)))}  y146 {h(ORI.getpixel((x,146)))}  y147 {h(ORI.getpixel((x,147)))}")

print("\n== ORIG column x=688, y 66..310 (every 2) ==")
for y in range(66, 311, 2):
    c = ORI.getpixel((688, y))
    r, g, b = c
    tag = ""
    if r > g + 25 and r > b + 25:
        tag = " <-- RED-ish"
    print(f"  y{y}: {h(c)}{tag}")

print("\n== ORIG column x=687 and x=689 (red-ish count) ==")
for x in (686, 687, 688, 689, 690, 691):
    reds = [y for y in range(68, 308) if (lambda c: c[0] > c[1] + 18 and c[0] > c[2] + 18)(ORI.getpixel((x, y)))]
    print(f"  x={x}: {len(reds)} red-ish px", (f"y {reds[0]}..{reds[-1]}" if reds else ""))

print("\n== REND column x=687.5 (render px 1433), y 68..305 ==")
xr = int(687.5 * S)
reds = [y for y in range(int(68 * S), int(305 * S)) if (lambda c: c[0] > c[1] + 18 and c[0] > c[2] + 18)(REN.getpixel((xr, y)))]
print(f"  {len(reds)} red-ish px, y {reds[0]/S:.0f}..{reds[-1]/S:.0f}" if reds else "  none")

print("\n== ORIG: any reddish vertical line anywhere in plot? per-column red-ish count ==")
for x in range(574, 810):
    reds = [y for y in range(68, 308) if (lambda c: c[0] > c[1] + 15 and c[0] > c[2] + 15)(ORI.getpixel((x, y)))]
    if len(reds) > 20:
        print(f"  x={x}: {len(reds)} red-ish px, y {reds[0]}..{reds[-1]}, first gaps",
              [reds[i+1]-reds[i] for i in range(min(10, len(reds)-1))])

print("\n== ORIG row y=146: full light-inclusive census (sum<700) ==")
ink = [x for x in range(570, 811) if sum(ORI.getpixel((x, 146))) < 700]
print(f"  n={len(ink)}", (f"span {ink[0]}..{ink[-1]}" if ink else ""))
print("\n== ORIG row y=146: strict dark (sum<250) ==")
ink = [x for x in range(570, 811) if sum(ORI.getpixel((x, 146))) < 250]
print(f"  n={len(ink)}", (f"span {ink[0]}..{ink[-1]}" if ink else ""))
