#!/usr/bin/env python3
"""Glyph-metric + shadow analysis for slide_001.jpg title.
Goals: (1) cap height / x-height / stroke width of title glyphs -> font size;
(2) whether pink pixels form an offset SHADOW of the red glyphs (band-height
inflation); (3) per-line title bboxes; (4) subtitle/small-text cap heights."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

bg = np.minimum(np.abs(IM - np.array([231, 233, 230])).sum(axis=2),
                np.abs(IM - np.array([254, 255, 253])).sum(axis=2))

print("=== PINK layer analysis (title region y110..290, x260..700) ===")
pink = (r > 215) & (g > 120) & (g < 215) & (b > 120) & (b < 215) & (r - g > 40)
redcore = (r > 130) & (g < 90) & (b < 90) & (r - g > 70)
reg = (slice(110, 290), slice(260, 700))
pk = pink[reg]
rd = redcore[reg]
print(f"pink px: {pk.sum()}, redcore px: {rd.sum()}")
for label, m in [("pink", pk), ("redcore", rd)]:
    ys, xs = np.where(m)
    if len(ys):
        print(f"{label} bbox y {110+ys.min()}..{110+ys.max()}, x {260+xs.min()}..{260+xs.max()}")
# per-line pink bands
rows = np.where(pk.any(axis=1))[0]
if len(rows):
    bands = []
    s = p = rows[0]
    for y in rows[1:]:
        if y - p > 4:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
    print("pink bands (offset +110):", bands)

print("\n=== glyph metrics: 'R' of Ridge (L1) ===")
# word 'Ridge' occupies x281..~400 at y127..171. Column profile to split letters.
sub = IM[120:180, 275:410]
subink = (np.minimum(np.abs(sub - np.array([231, 233, 230])).sum(axis=2),
                     np.abs(sub - np.array([254, 255, 253])).sum(axis=2)) > 90)
colcount = subink.sum(axis=0)
print("col profile (x275+idx: count):")
ons = []
for i, c in enumerate(colcount):
    if c > 0:
        ons.append((275 + i, int(c)))
print(ons)

# 'R' glyph = x281..302: measure cap top/baseline
R = subink[:, 281 - 275:303 - 275]
ys, xs = np.where(R)
print(f"'R' ink rows y {120+ys.min()}..{120+ys.max()} (h={ys.max()-ys.min()+1}), cols x {275+xs.min()}..{275+xs.max()}")
# stroke width of 'i' stem: find narrow column runs; 'i' should be x~313-331 run? measure that run's width
print("\nruns in L1 slice y149 (from measure3): 281-302 R, 313-331 i?, 340-358 d?, 368-400 g+e?")
# measure 'i' stem width: vertical stem in x313..331
stem = subink[120:180, 313 - 275:332 - 275]
ys2, xs2 = np.where(stem)
if len(ys2):
    print(f"run@313: rows y {120+ys2.min()}..{120+ys2.max()}, cols x {275+xs2.min()}..{275+xs2.max()}")
    # mid-row width = stroke width
    midrow = stem[(ys2.min() + ys2.max()) // 2]
    print(f"mid-row stroke width: {int(midrow.sum())} px")

print("\n=== x-height vs cap-height: 'e' in Ridge (last run 368-400?) ===")
run = subink[:, 368 - 275:401 - 275]
ys3, xs3 = np.where(run)
if len(ys3):
    print(f"run@368-400: rows y {120+ys3.min()}..{120+ys3.max()}")

print("\n=== L2 'G' of Gradient ===")
sub2 = IM[172:225, 270:330]
ink2 = (np.minimum(np.abs(sub2 - np.array([231, 233, 230])).sum(axis=2),
                   np.abs(sub2 - np.array([254, 255, 253])).sum(axis=2)) > 90)
ys4, xs4 = np.where(ink2)
print(f"'G' ink rows y {172+ys4.min()}..{172+ys4.max()} (h={ys4.max()-ys4.min()+1})")

print("\n=== subtitle cap height: 'CS' of CSAI (y314..335) ===")
sub3 = IM[310:340, 340:470]
ink3 = (np.minimum(np.abs(sub3 - np.array([231, 233, 230])).sum(axis=2),
                   np.abs(sub3 - np.array([254, 255, 253])).sum(axis=2)) > 90)
cc = ink3.sum(axis=0)
print("subtitle col runs:")
on3 = np.where(cc > 0)[0]
runs3 = []
if len(on3):
    s = p = on3[0]
    for x in on3[1:]:
        if x - p > 2:
            runs3.append((s, p)); s = x
        p = x
    runs3.append((s, p))
print([(340 + a, 340 + z) for a, z in runs3])
# first run = 'C': measure its vertical extent
if runs3:
    a, z = runs3[0]
    rr = np.where(ink3[:, a:z + 1].any(axis=1))[0]
    print(f"'C' rows y {310+rr.min()}..{310+rr.max()} (h={rr.max()-rr.min()+1})")

print("\n=== name line cap: 'D' of Dr. (y378..400) ===")
sub4 = IM[374:405, 348:380]
ink4 = (np.minimum(np.abs(sub4 - np.array([231, 233, 230])).sum(axis=2),
                   np.abs(sub4 - np.array([254, 255, 253])).sum(axis=2)) > 90)
ys5 = np.where(ink4.any(axis=1))[0]
xs5 = np.where(ink4.any(axis=0))[0]
print(f"'Dr.' region rows y {374+ys5.min()}..{374+ys5.max()} (h={ys5.max()-ys5.min()+1}), cols {348+xs5.min()}..{348+xs5.max()}")

print("\n=== email line x-height (y404..417) ===")
print("band h=14 incl desc? 'kmelsayed@...' has 'y' descender; cap 'k' asc")
sub5 = IM[400:420, 380:600]
ink5 = (np.minimum(np.abs(sub5 - np.array([231, 233, 230])).sum(axis=2),
                   np.abs(sub5 - np.array([254, 255, 253])).sum(axis=2)) > 90)
ys6 = np.where(ink5.any(axis=1))[0]
print(f"email rows y {400+ys6.min()}..{400+ys6.max()} (h={ys6.max()-ys6.min()+1})")

print("\n=== instructors hdr 'I' cap (y449..468) ===")
sub6 = IM[445:472, 120:135]
ink6 = (np.minimum(np.abs(sub6 - np.array([231, 233, 230])).sum(axis=2),
                   np.abs(sub6 - np.array([254, 255, 253])).sum(axis=2)) > 90)
ys7 = np.where(ink6.any(axis=1))[0]
print(f"'I' col rows y {445+ys7.min()}..{445+ys7.max()} (h={ys7.max()-ys7.min()+1})")

print("\n=== red band @422..437 left: what is it? (x87..203) ===")
sub7 = IM[418:442, 80:210]
ink7 = (np.minimum(np.abs(sub7 - np.array([231, 233, 230])).sum(axis=2),
                   np.abs(sub7 - np.array([254, 255, 253])).sum(axis=2)) > 90)
rr7 = np.where(ink7.any(axis=1))[0]
cc7 = np.where(ink7.any(axis=0))[0]
print(f"rows y {418+rr7.min()}..{418+rr7.max()} (h={rr7.max()-rr7.min()+1}), cols x {80+cc7.min()}..{80+cc7.max()}")
# color census of this band
pxs = sub7[ink7]
print("colors:", Counter(map(tuple, pxs // 24 * 24)).most_common(4))
# glyph count via col runs
ccnt = ink7.sum(axis=0)
on7 = np.where(ccnt > 0)[0]
runs7 = []
if len(on7):
    s = p = on7[0]
    for x in on7[1:]:
        if x - p > 1:
            runs7.append((s, p)); s = x
        p = x
    runs7.append((s, p))
print(f"col runs ({len(runs7)}): {[(80+a, 80+z) for a, z in runs7]}")
