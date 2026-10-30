#!/usr/bin/env python3
"""Slide 047 adjudication part 3: augmented row split, calc-box glyph colour/identity."""
import numpy as np
from PIL import Image

P = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_047.jpg"
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
LUM = (R + G + B) / 3
out = []


def say(*ls):
    for ln in ls:
        out.append(ln)


def runs(mask):
    res, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j + 1 < n and mask[j + 1]:
                j += 1
            if j - i + 1 >= 1:
                res.append((i, j))
            i = j + 1
        else:
            i += 1
    return res


def split_rows(x0, x1, y0, y1, blank_min):
    """Row bands separated by >= blank_min fully-blank rows."""
    prof = LUM[y0 : y1 + 1, x0 : x1 + 1].min(axis=1) < 220
    bands, i, n = [], 0, len(prof)
    while i < n:
        if prof[i]:
            j = i
            gap = 0
            k = i
            while k < n:
                if prof[k]:
                    j = k
                    gap = 0
                else:
                    gap += 1
                    if gap >= blank_min:
                        break
                k += 1
            bands.append((y0 + i, y0 + j))
            i = k + 1
        else:
            i += 1
    return bands


say("## F. AUGMENTED matrix data band split (x92..222, y162..230), blank>=2 rows separates")
for s, e in split_rows(92, 222, 162, 230, 2):
    say(f"  y{s}..{e} (h{e - s + 1})")
say("  calibration — TOP-LEFT matrix (x90..218, y60..112), same splitter:")
for s, e in split_rows(90, 218, 60, 112, 2):
    say(f"  y{s}..{e} (h{e - s + 1})")

say("\n## G. BOX2 label 'd(Z?) =' 4x LANCZOS ASCII (claim: Z2)")
crop = im.crop((280, 156, 340, 180)).resize((60 * 4, 24 * 4), Image.LANCZOS)
ca = np.asarray(crop.convert("L"))
for yy in range(0, 96, 2):
    say(f"  y{156 + yy // 4:3d}|" + "".join("#" if ca[yy, xx] < 190 else "." for xx in range(0, 240, 2)) + "|")

say("\n## H. BOX3 label 'd(Z?) =' 4x LANCZOS ASCII (claim: Z2)")
crop = im.crop((280, 221, 340, 245)).resize((60 * 4, 24 * 4), Image.LANCZOS)
ca = np.asarray(crop.convert("L"))
for yy in range(0, 96, 2):
    say(f"  y{221 + yy // 4:3d}|" + "".join("#" if ca[yy, xx] < 190 else "." for xx in range(0, 240, 2)) + "|")

say("\n## I. BOX1 label 'd(Z?) =' 4x LANCZOS ASCII (claim: Z1)")
crop = im.crop((280, 156, 340, 180)).resize((60 * 4, 24 * 4), Image.LANCZOS)
ca = np.asarray(crop.convert("L"))
for yy in range(0, 20):
    say(f"  y{156 + yy // 4:3d}|" + "".join("#" if ca[yy, xx] < 190 else "." for xx in range(0, 240, 2)) + "|")


def core(x0, x1, y0, y1):
    band = a[y0 : y1 + 1, x0 : x1 + 1].reshape(-1, 3)
    lum = LUM[y0 : y1 + 1, x0 : x1 + 1].ravel()
    thr = np.percentile(lum, 10)
    sel = band[lum <= max(thr, 1)]
    if sel.size == 0:
        return None
    return tuple(int(v) for v in np.median(sel, axis=0))


say("\n## J. calc-box colour cores (claim: row vector BLUE, stack GREEN, result black)")
say(f"  box1 row vector (x335..378, y146..160) core -> {core(335, 378, 146, 160)}")
say(f"  box1 stack '14' (x392..404, y148..160) core -> {core(392, 404, 148, 160)}")
say(f"  box1 stack '-4' (x392..404, y162..174) core -> {core(392, 404, 162, 174)}")
say(f"  box1 stack '0' (x392..404, y178..190) core -> {core(392, 404, 178, 190)}")
say(f"  box1 result '= 14' (x414..440, y158..176) core -> {core(414, 440, 158, 176)}")

say("\n## K. legend colour cores (claim: C1 red, C2 blue, Zero green)")
say(f"  legend C1 (x239..248, y110..124) -> {core(239, 248, 110, 124)}")
say(f"  legend C2 (x312..326, y110..124) -> {core(312, 326, 110, 124)}")
say(f"  legend 'Zero' (x394..423, y110..124) -> {core(394, 423, 110, 124)}")

say("\n## L. box3 result glyph '= -2' (claim: verbatim arithmetic slip, minus sign)")
crop = im.crop((410, 258, 445, 278)).resize((35 * 6, 20 * 6), Image.LANCZOS)
ca = np.asarray(crop.convert("L"))
for yy in range(0, 120, 3):
    say(f"  y{258 + yy // 6:3d}|" + "".join("#" if ca[yy, xx] < 190 else "." for xx in range(0, 210, 2)) + "|")

open("videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047/adjudicate_w047_p3.txt", "w").write("\n".join(out))
print("\n".join(out))
