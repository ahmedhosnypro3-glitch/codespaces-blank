#!/usr/bin/env python3
"""S5 carrier fine probe — 034 details that the geometry probe left open."""
from PIL import Image
import numpy as np

F = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)

# a. teal core: darkest decile of teal pixels
sub = im[59:313, 608:845].reshape(-1, 3)
r, g, b = sub[:, 0], sub[:, 1], sub[:, 2]
teal = (g > r + 30) & (b > r + 20) & (g > 120)
tv = sub[teal]
order = np.argsort(tv[:, 0])
core = tv[order[: len(order) // 10]]
print("teal core (darkest decile) median:", np.median(core, axis=0), "n=", len(core))
print("teal all median:", np.median(tv, axis=0))

# b/c. slope row: one cell c1 — scan row y=468 x140..190; col x=170 y456..482
print("--- slope c1 row y=468 x140..192")
prev = None
for x in range(140, 192):
    c = tuple(im[468, x]); k = tuple(v // 16 * 16 for v in c)
    if k != prev: print("  x=", x, c); prev = k
print("--- slope col x=170 y455..483")
prev = None
for y in range(455, 483):
    c = tuple(im[y, 170]); k = tuple(v // 16 * 16 for v in c)
    if k != prev: print("  y=", y, c); prev = k
# slope row bg (between inset boxes): x186..188
print("slope bg sample x185..189 y465..472:", np.median(im[465:472, 185:189].reshape(-1, 3), axis=0))
# slope label cell
print("slope label x90..130 y465..472:", np.median(im[465:472, 90:130].reshape(-1, 3), axis=0))
# slope row edges colors at x300
print("slope top edge x300 y456..462:", [tuple(im[y, 300]) for y in range(456, 463)])
print("slope bot edge x300 y475..481:", [tuple(im[y, 300]) for y in range(475, 481)])

# d. next-x red vertical centroids around each found column
found = [179, 219, 260, 301, 341, 382, 423, 463, 504, 544, 585, 626, 666, 707, 747, 788, 829, 869]
cent = []
for cx in found:
    w = im[486:500, cx - 3:cx + 4]
    redm = (w[:, :, 0] > 140) & (w[:, :, 1] < 90) & (w[:, :, 2] < 90).astype(object)
    redm = (w[:, :, 0] > 140) & (w[:, :, 1] < 90) & (w[:, :, 2] < 90)
    ys, xs = np.where(redm)
    c = xs.mean() + cx - 3 if len(xs) else None
    cent.append(round(c, 1) if c is not None else None)
print("next-x vertical centroids:", cent)
# label/c1 boundary + outer verticals of next-x row
w = im[486:500, 75:150]
redm = (w[:, :, 0] > 140) & (w[:, :, 1] < 90) & (w[:, :, 2] < 90)
print("next-x red cols x75..150:", sorted(set((np.where(redm)[1] + 75).tolist())))
w = im[486:500, 860:890]
redm = (w[:, :, 0] > 140) & (w[:, :, 1] < 90) & (w[:, :, 2] < 90)
print("next-x red cols x860..890:", sorted(set((np.where(redm)[1] + 860).tolist())))
# next-x row horizontal extent of red top rule
row = im[483, 60:900]
redm = (row[:, 0] > 140) & (row[:, 1] < 90) & (row[:, 2] < 90)
xs = np.where(redm)[0] + 60
print("next-x top rule extent:", xs.min() if len(xs) else None, xs.max() if len(xs) else None)

# e. expl box line-2 f(x) ink color (x265..315 y280..300) and line-1 X ink (x265..290 y256..276)
for (x0, x1, y0, y1, name) in [(265, 315, 280, 300, "f(x) line2"), (265, 292, 256, 276, "X line1")]:
    s = im[y0:y1, x0:x1].reshape(-1, 3)
    ink = s[s.max(axis=1) < 170]
    if len(ink):
        reds = ((ink[:, 0] > ink[:, 1] + 40) & (ink[:, 0] > ink[:, 2] + 40)).sum()
        blues = ((ink[:, 2] > ink[:, 0] + 40) & (ink[:, 2] > ink[:, 1] + 20)).sum()
        print(f"expl {name}: ink n={len(ink)} red-ish={reds} blue-ish={blues} median={np.median(ink,axis=0)}")
# line-1 values ink (9.6 / 9.8) — locate red bold runs y256..276 x292..600
s = im[256:276, 292:600]
redm = (s[:, :, 0] > 120) & (s[:, :, 1] < 80) & (s[:, :, 2] < 80)
ys, xs = np.where(redm)
if len(xs):
    print("line1 red-token bbox x", xs.min() + 292, "..", xs.max() + 292, " n=", len(xs))
# line-2 values blue
s = im[280:301, 292:600]
bm = (s[:, :, 2] > 120) & (s[:, :, 2] > s[:, :, 0] + 50) & (s[:, :, 1] < s[:, :, 2])
ys, xs = np.where(bm)
if len(xs):
    print("line2 blue-token bbox x", xs.min() + 292, "..", xs.max() + 292, " n=", len(xs))

# f. param border columns
print("--- param border scan y=260 x70..85:", [(x, tuple(im[260, x])) for x in range(70, 85)])
print("--- param border scan y=260 x168..180:", [(x, tuple(im[260, x])) for x in range(168, 180)])
print("--- param border top y240..258 x=100:", [(y, tuple(im[y, 100])) for y in range(242, 258, 2)])
print("--- param border bot y300..315 x=100:", [(y, tuple(im[y, 100])) for y in range(300, 315, 2)])

# g. band right edge + table right vertical
print("--- y345 x855..890:", [(x, tuple(im[345, x])) for x in range(855, 890, 2)])
print("--- y395 x855..890:", [(x, tuple(im[395, x])) for x in range(855, 890, 2)])
# left inner edge of band fills
print("--- y345 x78..90:", [(x, tuple(im[345, x])) for x in range(78, 90)])

# h. slope inset borders — red-ish census with looser threshold
sub = im[458:480, 143:872]
redm = (sub[:, :, 0] > 120) & (sub[:, :, 0] > sub[:, :, 1] + 50) & (sub[:, :, 0] > sub[:, :, 2] + 50)
colred = redm.sum(axis=0)
peaks = [x + 143 for x in range(len(colred)) if colred[x] >= 6]
print("slope red-ish vertical cols (loose):", peaks)
rowred = redm.sum(axis=1)
print("slope red-ish horizontal rows:", [(y + 458, int(rowred[y])) for y in range(len(rowred)) if rowred[y] > 30])

# i. eq box border probes
print("--- eq box border y=193 x460..470:", [(x, tuple(im[193, x])) for x in range(460, 470)])
print("--- eq box border y=193 x595..605:", [(x, tuple(im[193, x])) for x in range(595, 605)])
print("--- eq box border x=530 y164..175:", [(y, tuple(im[y, 530])) for y in range(164, 175)])
print("--- eq box border x=530 y214..224:", [(y, tuple(im[y, 530])) for y in range(214, 224)])

# j. plot border + box
print("--- plot border y=180 x603..613:", [(x, tuple(im[180, x])) for x in range(603, 613)])
print("--- plot border y=180 x840..850:", [(x, tuple(im[180, x])) for x in range(840, 850)])
print("--- plot border x=720 y54..64:", [(y, tuple(im[y, 720])) for y in range(54, 64)])
print("--- plot border x=720 y308..318:", [(y, tuple(im[y, 720])) for y in range(308, 318)])

# k. markers: red dot, orange arrow, green ellipse, pink box
print("--- red dot region y144..152 x778..790:", np.median(im[145:151, 780:787].reshape(-1, 3), axis=0))
print("--- orange arrow y116..135 x763..783 core:", np.median(
    im[118:133, 766:780].reshape(-1, 3)[
        (im[118:133, 766:780].reshape(-1, 3)[:, 0] > 180) & (im[118:133, 766:780].reshape(-1, 3)[:, 2] < 120)
    ], axis=0))
print("--- green ellipse y255..267 x799..817:", np.median(im[256:266, 800:816].reshape(-1, 3), axis=0))
print("--- pink box fill y272..300 x748..838:", np.median(im[274:298, 750:836].reshape(-1, 3), axis=0))
s = im[270:304, 742:845]
pk = (s[:, :, 0] > 200) & (s[:, :, 2] > 180) & (s[:, :, 1] < s[:, :, 0] - 20)
ys, xs = np.where(pk)
print("pink box fill bbox x", xs.min() + 742, "..", xs.max() + 742, " y", ys.min() + 270, "..", ys.max() + 270)
# pink box border color (magenta family)
s2 = im[266:308, 740:848].reshape(-1, 3)
mg = (s2[:, :, 0] > 130) & (s2[:, :, 2] > 100) & (s2[:, :, 1] < 90)
print("pink border-ish median:", np.median(s2[mg], axis=0) if mg.sum() else None, "n=", int(mg.sum()))
# red dashed guide
w = im[145:175, 775:795]
redm = (w[:, :, 0] > 130) & (w[:, :, 1] < 80) & (w[:, :, 2] < 80)
print("dashed guide red cols x775..795:", sorted(set((np.where(redm)[1] + 775).tolist())))
