#!/usr/bin/env python3
"""Slide 047 adjudication part 4: box3 label, paren extents, arrow glyph, class label x."""
import numpy as np
from PIL import Image

P = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_047.jpg"
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
LUM = a.mean(axis=2)
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
            res.append((i, j))
            i = j + 1
        else:
            i += 1
    return res


say("## M. BOX3 label 'd(Z?) =' 4x LANCZOS ASCII (claim: Z2)")
crop = im.crop((280, 286, 340, 310)).resize((60 * 4, 24 * 4), Image.LANCZOS)
ca = np.asarray(crop.convert("L"))
for yy in range(0, 96, 2):
    say(f"  y{286 + yy // 4:3d}|" + "".join("#" if ca[yy, xx] < 190 else "." for xx in range(0, 240, 2)) + "|")

say("\n## N. augmented matrix col-1 paren vertical extent (x91..99, y160..232)")
prof = (LUM[160:233, 91:100].min(axis=1) < 220)
say(f"  ink row runs: {[(160 + s, 160 + e) for s, e in runs(prof)]}")
say("## N2. top-left matrix col-1 paren vertical extent (x87..95, y60..112) [calibration]")
prof = (LUM[60:113, 87:96].min(axis=1) < 220)
say(f"  ink row runs: {[(60 + s, 60 + e) for s, e in runs(prof)]}")
say("## N3. calc box1 stack paren vertical extent (x386..394, y145..195)")
prof = (LUM[145:196, 386:395].min(axis=1) < 220)
say(f"  ink row runs: {[(145 + s, 145 + e) for s, e in runs(prof)]}")
say("## N4. W-vector paren vertical extent (x322..331, y56..108)")
prof = (LUM[56:109, 322:332].min(axis=1) < 220)
say(f"  ink row runs: {[(56 + s, 56 + e) for s, e in runs(prof)]}")

say("\n## O. sign statement start (claim: '=>' double-arrow then 'Positive > 0') 4x ASCII")
crop = im.crop((500, 154, 560, 178)).resize((60 * 4, 24 * 4), Image.LANCZOS)
ca = np.asarray(crop.convert("L"))
for yy in range(0, 96, 2):
    say(f"  y{154 + yy // 4:3d}|" + "".join("#" if ca[yy, xx] < 190 else "." for xx in range(0, 240, 2)) + "|")

say("\n## P. class outcome labels: column clusters in y158..176 (box1) x640..730")
prof = (LUM[158:177, 640:731].min(axis=0) < 220)
say(f"  ink col runs x640..730: {[(640 + s, 640 + e) for s, e in runs(prof)]}")
say("## P2. box2 class outcome in y225..243 x640..740")
prof = (LUM[225:244, 640:741].min(axis=0) < 220)
say(f"  ink col runs x640..740: {[(640 + s, 640 + e) for s, e in runs(prof)]}")

say("\n## Q. calc-box label+row-vector baseline band: box1 rows y150..175 x283..380 clusters")
prof = (LUM[150:176, 283:381].min(axis=1) < 220)
say(f"  ink row runs x283..380 y150..175: {[(150 + s, 150 + e) for s, e in runs(prof)]}")
say("## Q2. box1: label 'd(Z1) =' col clusters x283..330")
prof = (LUM[150:176, 283:331].min(axis=0) < 220)
say(f"  ink col runs: {[(283 + s, 283 + e) for s, e in runs(prof)]}")

open("videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047/adjudicate_w047_p4.txt", "w").write("\n".join(out))
print("\n".join(out))
