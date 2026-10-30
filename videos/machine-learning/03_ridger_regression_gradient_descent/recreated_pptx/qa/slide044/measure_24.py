#!/usr/bin/env python3
"""Final decisive measurements before build."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
dark = LUM < 185
satred = (rf - gf > 45) & (rf - bf > 45) & (rf > 110)
satblue = (bf - rf > 40) & (bf - gf > 25) & (bf > 110)

print("=== 1. BOX INTERIOR fill (median of clean pixels y60..125, x76..712) ===")
sub = IM[60:126, 76:713].reshape(-1, 3)
pan = (sub[:, 0] - sub[:, 2])
cand = sub[(sub[:, 0] > 240) & (sub[:, 1] > 240)]
print(f"  near-white px: {len(cand)}  median #{int(np.median(cand[:,0])):02X}"
      f"{int(np.median(cand[:,1])):02X}{int(np.median(cand[:,2])):02X}")
cand2 = sub[(sub[:, 0] > 235) & (sub[:, 1] > 235) & (sub[:, 2] > 200)]
print(f"  cream-ish  px: {len(cand2)}  median #{int(np.median(cand2[:,0])):02X}"
      f"{int(np.median(cand2[:,1])):02X}{int(np.median(cand2[:,2])):02X}")

print("\n=== 2. Rule-text C glyphs (1px, x236..345, y105..127) ===")
print("     " + "".join(str((x // 10) % 10) for x in range(236, 345)))
print("     " + "".join(str(x % 10) for x in range(236, 345)))
for y in range(105, 128):
    line = ""
    for x in range(236, 345):
        if satblue[y, x]: line += "B"
        elif satred[y, x]: line += "R"
        elif dark[y, x]: line += "#"
        elif LUM[y, x] < 205: line += "+"
        else: line += " "
    print(f"{y:>4} {line}")

print("\n=== 3. Z-matrix box search (blue runs y58..126) ===")
sub_blue = satblue[58:127, 72:716]
cc = sub_blue.sum(axis=0)
xs = np.where(cc > 0)[0]
print("  blue column clusters:", end=" ")
if len(xs):
    runs = []; s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 5: runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
    print(" ".join(f"[x{72+a}..{72+b}]" for a, b in runs))
else:
    print("none")
rc = sub_blue.sum(axis=1)
ys = np.where(rc > 0)[0]
print("  blue row clusters:", end=" ")
if len(ys):
    runs = []; s = ys[0]
    for i in range(1, len(ys)):
        if ys[i] - ys[i - 1] > 5: runs.append((s, ys[i - 1])); s = ys[i]
    runs.append((s, ys[-1]))
    print(" ".join(f"[y{58+a}..{58+b}]" for a, b in runs))
else:
    print("none")

print("\n=== 4. LEFT-MIDDLE table: is there a box? (x60..250, y130..270) ===")
sl = dark[132:268, 60:251]
cc = sl.sum(axis=0)
xs = np.where(cc > 8)[0]
print("  long-ish grey/dark vertical candidates:", end=" ")
runs = []
if len(xs):
    s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 4: runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
for a, b in runs:
    ys = np.where(sl[:, a:b + 1].any(axis=1))[0]
    if len(ys) and (ys.max() - ys.min()) > 60:
        print(f"x{60+a}..{60+b} y{132+ys.min()}..{132+ys.max()} px={int(sl[:,a:b+1].sum())}", end="  ")
print()
print("  left-edge stroke colour probe (x60..75, y160):",
      [f"#{IM[160,x][0]:02X}{IM[160,x][1]:02X}{IM[160,x][2]:02X}" for x in range(60, 76)])
