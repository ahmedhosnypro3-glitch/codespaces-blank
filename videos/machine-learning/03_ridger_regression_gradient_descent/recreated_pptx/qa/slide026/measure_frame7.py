#!/usr/bin/env python3
"""Pass-7 (resume worker w4-s026): (a) title font pin (Calibri vs Carlito vs Arial),
(b) notes line assignment by SUFFIX/position match at 18pt with word-level x check
against measured runs, (c) raw pixel probe of the y493..502 mystery bar, (d) N4/N3
word-position check for the underline bars."""
import numpy as np
from PIL import Image, ImageFont, ImageDraw

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_026.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)

def word_boxes(text, fontpath, size):
    """Return [(word, ink_x0, ink_x1)] laid out from x=0 with single spaces (advance-based)."""
    S = 4
    f = ImageFont.truetype(fontpath, int(round(size * S)))
    words = text.split(" ")
    out, pen = [], 0.0
    for i, w in enumerate(words):
        if i:
            pen += f.getlength(" ")
        # ink extent of the word relative to its origin
        img = Image.new("L", (int(size * S * len(w) * 2) + 200, size * S * 3), 0)
        d = ImageDraw.Draw(img)
        d.text((100, 100), w, font=f, fill=255)
        a = np.asarray(img)
        ys, xs = np.where(a > 40)
        if len(xs):
            li = (xs.min() - 100) / S
            ri = (xs.max() - 100) / S
        else:
            li = ri = 0.0
        out.append((w, pen + li, pen + ri))
        pen += f.getlength(w)
    return out

print("== (a) TITLE: real Calibri / Carlito / Arial bold, sizes 29..34 ==")
TITLE = "Gradient Descent Solution"
for name, p in [("Calibri", "/usr/share/fonts/TTF/calibrib.ttf"),
                ("Carlito", None), ("Arial", "/usr/share/fonts/TTF/Arialbd.TTF")]:
    import glob
    if p is None:
        p = glob.glob("/usr/share/fonts/**/Carlito-Bold.ttf", recursive=True)[0]
    for s in (29, 30, 31, 31.5, 32, 33, 34):
        f = ImageFont.truetype(p, int(round(s * 4)))
        img = Image.new("L", (2400, 400), 0)
        d = ImageDraw.Draw(img)
        d.text((100, 100), TITLE, font=f, fill=255)
        a = np.asarray(img)
        ys, xs = np.where(a > 40)
        w = (xs.max() - xs.min() + 1) / 4
        h = (ys.max() - ys.min() + 1) / 4
        mark = "  <<<" if abs(w - 346) < 4 and abs(h - 23) < 2 else ""
        print(f"  {name:8s} s={s:5} ink_w={w:6.1f} ink_h={h:5.1f}{mark}")

AR = "/usr/share/fonts/TTF/Arial.TTF"
ARB = "/usr/share/fonts/TTF/Arialbd.Tf".replace("Tf", "TF")

print("\n== (b) NOTES at 18pt: word x-positions vs measured runs ==")
# N3 hypothesis: line ends "...depending on"; N4 = "the used Learning Rate"
N3TXT = "GD will approximately find this minimum value but at a variable number of steps depending on"
N3_MEAS_RUNS = [(109, 136), (141, 170), (176, 278), (283, 313), (319, 345), (351, 425),
                (430, 471), (477, 501), (507, 520), (525, 533), (538, 728), (733, 812), (818, 836)]
wb = word_boxes(N3TXT, AR, 18)
print("  N3 predicted word ink extents (+109):")
for w, a, b in wb:
    print(f"    {w:16s} x {109+a:6.1f} .. {109+b:6.1f}")
print("  N3 measured runs:", N3_MEAS_RUNS)

N4TXT = "the used Learning Rate"
wb4 = word_boxes(N4TXT, AR, 18)
print("  N4 predicted word ink extents (+109):")
for w, a, b in wb4:
    print(f"    {w:16s} x {109+a:6.1f} .. {109+b:6.1f}")
print("  N4 measured ink x 111..294 (w 184)")

N1TXT = "Least Squares Linear regression objective function is a convex function (even with"
N1_MEAS_RUNS = [(109, 154), (159, 224), (229, 279), (284, 362), (373, 442), (448, 511),
                (522, 534), (539, 548), (554, 610), (615, 682), (688, 730), (736, 769)]
wb1 = word_boxes(N1TXT, AR, 18)
print("  N1 predicted word ink extents (+109):")
for w, a, b in wb1:
    print(f"    {w:16s} x {109+a:6.1f} .. {109+b:6.1f}")
print("  N1 measured runs:", N1_MEAS_RUNS)

N2TXT = "regularizer). This means it has ONE Minimum (good news )."
N2_MEAS_RUNS = [(109, 202), (208, 241), (247, 295), (301, 311), (316, 341), (347, 385),
                (391, 466), (473, 516), (522, 560), (566, 575)]
wb2 = word_boxes(N2TXT, AR, 18)
print("  N2 predicted word ink extents (+109):")
for w, a, b in wb2:
    print(f"    {w:16s} x {109+a:6.1f} .. {109+b:6.1f}")
print("  N2 measured runs:", N2_MEAS_RUNS)

print("\n== (c) raw pixels rows 492..503, cols 95..330 (mystery bar) ==")
for yy in range(492, 504):
    row = im[yy, 95:330]
    dark = np.where(row.sum(axis=1) < 420)[0]
    blue = np.where((row[:, 2] - row[:, 0] > 40) & (row[:, 2] > 90))[0]
    print(f"  y{yy}: dark runs: {[(int(a+95), int(c+95)) for a, c in [()]] if False else ''}"
          f"dark[{dark.min()+95 if len(dark) else '-'}..{dark.max()+95 if len(dark) else '-'}] n={len(dark)} "
          f"blue[{blue.min()+95 if len(blue) else '-'}..{blue.max()+95 if len(blue) else '-'}] n={len(blue)}")
print("  raw samples y499 x100..130:", [tuple(im[499, x]) for x in range(100, 131, 5)])
print("  raw samples y497 x100..130:", [tuple(im[497, x]) for x in range(100, 131, 5)])
print("  raw samples y496 x100..130:", [tuple(im[496, x]) for x in range(100, 131, 5)])
print("  raw samples y495 x100..130:", [tuple(im[495, x]) for x in range(100, 131, 5)])

print("\n== (d) N3 bar check: bar x190..276 vs 'approximately' predicted; bar x540..727 ==")
for w, a, b in wb:
    if w in ("approximately", "variable", "number", "of", "steps"):
        print(f"    {w:16s} x {109+a:6.1f} .. {109+b:6.1f}")

print("\n== (e) GD header + Notes header + rowA/rowB/rowD word positions at 18pt ==")
for txt, x0 in [("[1] Start with initial Random Weights (W)", 146),
                ("[2] Update the weights by moving along the direction of negative gradient of Loss function", 146),
                ("[3] Stop when the gradient is almost zero (this is at the minimum value of the function)", 146)]:
    print(f"  -- {txt[:40]}... (x0={x0})")
    for w, a, b in word_boxes(txt, AR, 18):
        print(f"     {w:16s} x {x0+a:6.1f} .. {x0+b:6.1f}")
