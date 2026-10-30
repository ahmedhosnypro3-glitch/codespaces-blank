#!/usr/bin/env python3
"""Slide 047 PIL adjudication (worker w047-root-20261024, attempt 6).

Re-verifies EVERY defect claimed by prior lanes' FAIL verdicts against the ORIGINAL
frame (960x540, 1px=1pt) before accepting or refuting it. Run from the repo root
(ai_llm_slides/). Banked output: recreated_pptx/qa/slide047/adjudicate_w047.txt
"""
import numpy as np
from PIL import Image

P = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_047.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
LUM = (R + G + B) / 3
INK = LUM < 228
out = []


def say(*lines):
    for ln in lines:
        out.append(ln)


def classify(px):
    r, g, b = px
    if r - g > 40 and r - b > 40:
        return "RED"
    if b - r > 30 and b - g > 10:
        return "BLUE"
    if g - r > 20 and g - b > 20:
        return "GREEN"
    return "BLACK"


def core_color(x0, x1, y0, y1):
    """Median colour of the darkest 15% ink pixels in a box (JPEG-noise robust)."""
    band = a[y0 : y1 + 1, x0 : x1 + 1].reshape(-1, 3)
    lum = LUM[y0 : y1 + 1, x0 : x1 + 1].ravel()
    thr = np.percentile(lum, 12)
    sel = band[lum <= max(thr, 1)]
    if sel.size == 0:
        return None, None
    med = tuple(int(v) for v in np.median(sel, axis=0))
    return med, classify(med)


def col_profile(x0, x1, y0, y1, thresh=228):
    return INK[y0 : y1 + 1, x0 : x1 + 1].sum(axis=0)


def row_profile(x0, x1, y0, y1, thresh=228):
    return INK[y0 : y1 + 1, x0 : x1 + 1].sum(axis=1)


def runs(mask, min_len=1):
    """Yield (start, end) inclusive runs of True."""
    res = []
    i = 0
    n = len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j + 1 < n and mask[j + 1]:
                j += 1
            if j - i + 1 >= min_len:
                res.append((i, j))
            i = j + 1
        else:
            i += 1
    return res


say(f"### image {W}x{H}")

# ---------------------------------------------------------------- top band fill
say("\n## 1. TOP BAND fill + border (claim: cream FFFFE8 fill, dark-blue hairline)")
band_int = [
    ("clear interior (706,62)", 706, 62),
    ("clear interior (712,120)", 712, 120),
    ("clear interior (600,122)", 600, 122),
    ("clear interior (450,58)", 450, 58),
]
for name, x, y in band_int:
    say(f"  {name}: RGB={tuple(a[y, x])}")
say(f"  band border row y=55 x300..700: median RGB={tuple(np.median(a[55, 300:700], axis=0).astype(int))}")
say(f"  band border row y=129 x300..700: median RGB={tuple(np.median(a[129, 300:700], axis=0).astype(int))}")
say(f"  above band y=52 x300..700: median RGB={tuple(np.median(a[52, 300:700], axis=0).astype(int))} (panel gray?)")

# ---------------------------------------------------- top-left matrix class row
say("\n## 2. TOP-LEFT matrix class row: claim C1 C1 C1 (red) C2 C2 C2 (blue)")
# whole matrix band x84..220; find digit columns
cp = col_profile(84, 220, 78, 108)
cruns = runs(cp > 0)
say(f"  digit/paren column clusters in y78..108 (x84..220): {[(84+s, 84+e) for s, e in cruns]}")
# each cluster = one matrix column (parens + digits). class label band below:
say("  class-label band y113..123, per column cluster, core colour:")
for s, e in cruns:
    cx0, cx1 = 84 + s, 84 + e
    med, cls = core_color(cx0, cx1, 112, 124)
    say(f"    x{cx0}..{cx1}: core={med} -> {cls}")

# --------------------------------------------------------- augmented matrix rows
say("\n## 3. AUGMENTED matrix (claim: 3 data rows + header + class row)")
rp = row_profile(80, 246, 140, 258)
rruns = runs(rp > 1)  # >1 ink px per row to skip noise
say(f"  ink row runs in x80..246, y140..258: {[(140+s, 140+e) for s, e in rruns]}")
# and column clusters within the data band only (skip title/class)
say("  (compare with the 4-row reading in MEASUREMENT_NOTES.md attempt-1 era)")

# ---------------------------------------------------------------- legend spacing
say("\n## 4. LEGEND 'C1 positive C2negative Zero is unaccepted' (claim: NO space after C2)")
lp = col_profile(236, 514, 108, 126)
lruns = runs(lp > 0)
say(f"  ink column runs in legend band y108..126 (x236..514): {[(236+s, 236+e) for s, e in lruns]}")
say("  gaps between consecutive runs (px):")
gaps = []
for i in range(1, len(lruns)):
    g = lruns[i][0] - lruns[i - 1][1] - 1
    gaps.append((236 + lruns[i - 1][1] + 1, 236 + lruns[i][0] - 1, g))
say("   " + ", ".join(f"gap x{s}..{e} = {g}px" for s, e, g in gaps))

# ------------------------------------------------------------ calc box interiors
say("\n## 5. CALC BOX interiors (claim: WHITE fill + A6ACB8 hairline, not tinted)")
for name, (x0, y0, x1, y1) in {
    "box1 interior left (x275..300,y142..152)": (275, 142, 300, 152),
    "box1 interior right (x830..852,y142..152)": (830, 142, 852, 152),
    "box2 interior right (x830..852,y209..219)": (830, 209, 852, 219),
    "box3 interior right (x830..852,y274..284)": (830, 274, 852, 284),
}.items():
    sel = a[y0 : y1 + 1, x0 : x1 + 1].reshape(-1, 3)
    med = tuple(int(v) for v in np.median(sel, axis=0))
    say(f"  {name}: median RGB={med}")
say(f"  box1 top border y=139 x400..600: median RGB={tuple(np.median(a[139, 400:600], axis=0).astype(int))}")
say(f"  box1 bottom border y=198 x400..600: median RGB={tuple(np.median(a[198, 400:600], axis=0).astype(int))}")

# --------------------------------------------------------- sign statement colour
say("\n## 6. BOX1 sign statement '=> Positive > 0' (claim: BLACK bold)")
med, cls = core_color(508, 592, 158, 176)
say(f"  core={med} -> {cls}")
say(f"  for reference, 'Class I' box1 (x663..700,y158..176) core -> {core_color(663, 700, 158, 176)}")
say(f"  for reference, 'd(Z1) =' box1 (x283..325,y158..176) core -> {core_color(283, 325, 158, 176)}")

# ------------------------------------------------------------------ button fill
say("\n## 7. BUTTON (claim: red C00000 fill, white bold text)")
sel = a[284:297, 110:220].reshape(-1, 3)
say(f"  button interior median RGB={tuple(int(v) for v in np.median(sel, axis=0))}")
say(f"  text-core (white) in button: darkest->brightest sample y282..300 x130..150 median of top lum: "
    f"{tuple(int(v) for v in np.median(a[282:301, 130:151].reshape(-1,3), axis=0))}")

# ----------------------------------------------------------- W vector entries
say("\n## 8. INITIAL W vector (claim: THREE entries 4 / -2 / -2)")
rpw = row_profile(300, 360, 56, 108)
say(f"  ink row runs in x300..360, y56..108 (label '=' is at y75..84, x340..354): "
    f"{[(56+s, 56+e) for s, e in runs(rpw > 0)]}")
# digits column of W vector
cpw = col_profile(332, 352, 58, 106)
say(f"  ink col runs in W-digits band x332..352, y58..106: {[(332+s, 332+e) for s, e in runs(cpw > 0)]}")

# ------------------------------------------------- calcs column delimiter shape
say("\n## 9. CALC box column-vector delimiter shape (claim: spanning ROUND parens)")
d = a[148:190, 380:407].min(axis=2)
for yy in range(0, 42, 2):
    say(f"    y{148+yy:3d}|" + "".join("#" if d[yy, xx] < 200 else "." for xx in range(0, 27)) + "|")

say("\n## 10. augmented title glyph row (claim: 'Ugmented' = source typo, no leading 'A')")
t = LUM[146:162, 78:190]
for yy in range(0, 16):
    say(f"    y{146+yy:3d}|" + "".join("#" if t[yy, xx] < 200 else "." for xx in range(0, 112)) + "|")

say("\n## 11. Z-matrix header glyphs (claim: Z1 Z1 Z1)")
z = LUM[62:80, 594:660]
for yy in range(0, 18):
    say(f"    y{62+yy:3d}|" + "".join("#" if z[yy, xx] < 200 else "." for xx in range(0, 66)) + "|")

open("videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047/adjudicate_w047.txt", "w").write("\n".join(out))
print("\n".join(out))
