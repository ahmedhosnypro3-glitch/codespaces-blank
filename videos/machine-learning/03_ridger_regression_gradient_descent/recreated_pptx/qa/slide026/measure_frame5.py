#!/usr/bin/env python3
"""Pass-5 (resume worker w4-s026): box border geometry+color, blue/red ink colors,
exact underline-bar extents per text row, title+body font-size fit by advance
width (real Arial metrics == the renderer's Arial), and greedy wrap simulation
for the wrapped lines (rows B/C and notes N1..N4).

Banked evidence for slide_026 (03_ridger_regression_gradient_descent).
Reuses the earlier passes' band census (measure_frame2/3/4) — adds colors, bars,
and wrap decisions.
"""
import numpy as np
from PIL import Image, ImageFont

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_026.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red_ink = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
blue_ink = (b > 90) & ((b - r) > 40) & ((b - g) > 40)
dark_ink = im.sum(axis=2) < 300

def runs(mask_row, minlen=1):
    idx = np.where(mask_row)[0]
    if not len(idx):
        return []
    out, s0, p0 = [], idx[0], idx[0]
    for i in idx[1:]:
        if i > p0 + 1:
            if p0 - s0 + 1 >= minlen:
                out.append((s0, p0))
            s0 = i
        p0 = i
    if p0 - s0 + 1 >= minlen:
        out.append((s0, p0))
    return out

print("== BOX BORDER: raw pixel values ==")
print(" top row y=91, x 300..310:", [tuple(im[91, x]) for x in range(300, 311)])
print(" top row y=90, x 300..310:", [tuple(im[90, x]) for x in range(300, 311)])
print(" left col x=82, y 300..310:", [tuple(im[y, 82]) for y in range(300, 311)])
print(" left col x=83, y 300..310:", [tuple(im[y, 83]) for y in range(300, 311)])
print(" right col x=862, y 300..310:", [tuple(im[y, 862]) for y in range(300, 311)])
print(" bottom row y=498, x 300..310:", [tuple(im[498, x]) for x in range(300, 311)])
print(" bottom row y=499, x 300..310:", [tuple(im[499, x]) for x in range(300, 311)])

# border extent: for each of the 4 edges, the contiguous strong-blue column/row profile
colblue = blue_ink[:, 100:900].sum(axis=0)
strong_cols = np.where(colblue > 300)[0] + 100
rowblue = blue_ink[:, 85:862].sum(axis=1)
strong_rows = np.where(rowblue > 300)[0]
print(" strong-blue cols (>300px):", strong_cols.tolist())
print(" strong-blue rows (>300px):", strong_rows.tolist())

# color histogram of the border (cols 81..85, rows 100..500)
win = im[100:500, 81:86].reshape(-1, 3)
print(" border col histogram top values:",
      sorted(map(tuple, win), key=lambda t: -b if False else 0)[:0])
uniq, cnt = np.unique(win, axis=0, return_counts=True)
order = np.argsort(-cnt)[:6]
for i in order:
    print("   ", tuple(uniq[i]), cnt[i])

print("\n== TEXT COLORS (glyph cores) ==")
# title: darkest red px in title band
tb = im[58:84, 290:645].reshape(-1, 3)
m = (tb[:, 0] > 90) & ((tb[:, 0] - tb[:, 1]) > 40)
print(" title red px count:", m.sum(), "darkest:", tb[m].min(axis=0) if m.sum() else None,
      "median:", np.median(tb[m], axis=0) if m.sum() else None)
# blue glyph core: row A x 302..434 (thick bold run), y 143..162
bb = im[143:163, 302:435].reshape(-1, 3)
m2 = (bb[:, 2] > 90) & ((bb[:, 2] - bb[:, 0]) > 40) & ((bb[:, 2] - bb[:, 1]) > 40)
print(" blue glyph px count:", m2.sum(), "darkest:", bb[m2].min(axis=0) if m2.sum() else None,
      "median:", np.median(bb[m2], axis=0) if m2.sum() else None)
# dark glyph core: N1 x 284..362
db = im[342:362, 284:363].reshape(-1, 3)
m3 = db.sum(axis=1) < 300
print(" dark glyph px count:", m3.sum(), "darkest:", db[m3].min(axis=0) if m3.sum() else None,
      "median:", np.median(db[m3], axis=0) if m3.sum() else None)

print("\n== UNDERLINE BARS: scan rows below each band for long solid runs ==")
# band definitions from the banked census
BANDS = {
    "rowA": (138, 168, "blue"),
    "rowB": (172, 202, "blue"),
    "rowC": (205, 236, "blue"),
    "rowD": (238, 268, "blue"),
    "gd_hdr": (105, 135, "red"),
    "notes_hdr": (300, 335, "red"),
    "N1": (338, 366, "dark"),
    "N2": (372, 400, "dark"),
    "N3": (437, 465, "dark"),
    "N4": (471, 502, "dark"),
}
for name, (y0, y1, col) in BANDS.items():
    print(f" -- {name} (y{y0}..{y1}, {col}) --")
    for yy in range(y0, y1):
        if col == "blue":
            mask = blue_ink[yy, 85:862]
        elif col == "red":
            mask = red_ink[yy, 85:862]
        else:
            mask = dark_ink[yy, 85:862]
        rr = runs(mask, minlen=25)
        long_rr = [(a + 85, c + 85) for a, c in rr if (c - a + 1) >= 40]
        if long_rr:
            print(f"    y{yy}: {long_rr}  (all>=25 runs: {[(a+85, c+85) for a, c in rr]})")

print("\n== FONT SIZE FIT (real Arial; frame px, 1px=1pt) ==")
AR = "/usr/share/fonts/TTF/Arial.TTF"
ARB = "/usr/share/fonts/TTF/Arialbd.TTF"

def adv(text, size, bold=False):
    f = ImageFont.truetype(ARB if bold else AR, int(round(size * 4)))  # 4x for precision
    return f.getlength(text) / 4.0

TITLE = "Gradient Descent Solution"
for s in (19, 20, 21, 22):
    print(f" title bold {s}pt adv={adv(TITLE, s, True):.1f}px (measured 346.0)")

BODY = {
    "rowA": "[1] Start with initial Random Weights (W)",
    "rowB": "[2] Update the weights by moving along the direction of negative gradient of Loss function",
    "rowC": "(w.r.t. W) (moving step is a hyper parameter, AKA Learning Rate)",
    "rowD": "[3] Stop when the gradient is almost zero (this is at the minimum value of the function)",
}
MEAS = {"rowA": 324, "rowB": 701, "rowC": 544, "rowD": 685}
for k, t in BODY.items():
    for s in (16, 17, 18):
        print(f" {k} reg {s}pt adv={adv(t, s):.1f}px (measured {MEAS[k]})")

print("\n== GREEDY WRAP SIMULATION at 17pt (box interior usable x 146..861 for alg rows, 109..861 for notes) ==")
def wrap(text, size, x_start, x_max, bold_words=()):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        # bold phrases widen the advance; approximate with a bold penalty per word
        ww = adv(trial, size)
        for bw in bold_words:
            if bw in trial:
                ww += 0.06 * adv(bw, size, True)
        if ww <= (x_max - x_start) or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines

for s in (16, 17):
    print(f" -- size {s} --")
    lb = wrap(BODY["rowB"] + " " + BODY["rowC"], s, 146, 861)
    print("   alg line2 wrap:", [(l, round(adv(l, s), 1)) for l in lb])
    n1 = "Least Squares Linear regression objective function is a convex function (even with regularizer). This means it has ONE Minimum (good news )."
    print("   note1 wrap:", [(l, round(adv(l, s), 1)) for l in wrap(n1, s, 109, 861)])
    n2 = "GD will approximately find this minimum value but at a variable number of steps depending on the used Learning Rate"
    print("   note2 wrap:", [(l, round(adv(n2, s), 1)) for l in wrap(n2, s, 109, 861)])

print("\n== MEASURED NOTE LINE WIDTHS (frame2 census) ==")
print("  N1 text x109..769 w=660 | N2 text x109..575 w=467 | N3 text x109..836 w=727 | N4 text x111..294 w=184")
print("  N4 extra band y498-503 x85..860 — check what that is:")
for yy in range(494, 506):
    print(f"    y{yy}: dark runs>=25: {[(a, c) for a, c in runs(dark_ink[yy, 85:862], 25)]}")
