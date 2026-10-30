#!/usr/bin/env python3
"""w013 final measurement pass on unique_slides/slide_013.jpg (960x540, 1px=1pt).
Prints numbers only; no rendering, no vision."""
from PIL import Image
import numpy as np

im = Image.open('unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print('frame', W, H)

def ink_bbox(x0, y0, x1, y1, pred, label):
    sub = a[y0:y1, x0:x1]
    m = pred(sub)
    ys, xs = np.where(m)
    if len(xs) == 0:
        print(f'{label}: EMPTY')
        return None
    bx0, bx1, by0, by1 = x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max()
    print(f'{label}: ink x{bx0}..{bx1} y{by0}..{by1} (w{bx1-bx0+1} h{by1-by0+1}) n={len(xs)}')
    return bx0, by0, bx1, by1

def core_color(x0, y0, x1, y1, pred, label, n=5):
    sub = a[y0:y1, x0:x1]
    m = pred(sub)
    if m.sum() == 0:
        print(f'{label}: no core px')
        return
    px = sub[m]
    # darkest / most saturated median of the mask
    med = np.median(px, axis=0).astype(int)
    print(f'{label}: core median rgb={tuple(med)} hex={med[0]:02X}{med[1]:02X}{med[2]:02X} n={m.sum()}')

R = lambda s: s[:, :, 0]
G = lambda s: s[:, :, 1]
B = lambda s: s[:, :, 2]
def redmask(s):   return (R(s) > 110) & (G(s) < 90) & (B(s) < 90) & (R(s) - G(s) > 70)
def bluemask(s):  return (B(s) > 110) & (R(s) < 100) & (B(s) - R(s) > 70)
def darkmask(s):  return (R(s) < 110) & (G(s) < 110) & (B(s) < 110)
def yellowmask(s): return (R(s) > 170) & (G(s) > 140) & (B(s) < 190) & (R(s) - B(s) > 40)

print('\n== TITLE ==')
ink_bbox(100, 55, 900, 110, redmask, 'title red ink')
core_color(100, 55, 900, 110, redmask, 'title core')

print('\n== TRAIN TABLE band 1 ==')
# vertical gridlines: scan for columns where many light-gray/colored px exist
sub = a[127:249, 60:480]
# gridline detector: columns with >60% non-white-ish pixels
for x in range(80, 480):
    col = a[130:247, x]
    nonwhite = ((col[:, 0] < 235) | (col[:, 1] < 235) | (col[:, 2] < 235)).sum()
    if nonwhite > 90:
        print(f'  gridline col x={x} nonwhite={nonwhite}')
print('  --- horizontal ---')
for y in range(120, 260):
    row = a[y, 95:455]
    nonwhite = ((row[:, 0] < 235) | (row[:, 1] < 235) | (row[:, 2] < 235)).sum()
    if nonwhite > 250:
        print(f'  gridline row y={y} nonwhite={nonwhite}')

# gridline core colour sample
print('  gridline colour samples:', [tuple(a[127+i, x]) for x in (133, 174) for i in (0, 5, 10)])
print('  gridline h samples:', [tuple(a[y, 300]) for y in (126, 157)])

print('\n== TRAIN band1 cell inks ==')
ink_bbox(134, 127, 214, 157, bluemask, 'header X1 (blue)')
ink_bbox(214, 127, 255, 157, redmask, 'header X2 (red)')
ink_bbox(92, 158, 133, 188, bluemask, 'rowlabel X1 (blue)')
ink_bbox(134, 158, 174, 188, bluemask, 'cell 1 (blue)')
ink_bbox(174, 158, 214, 188, redmask, 'cell 2 (red)')

print('\n== TEST table band1 ==')
for y in range(120, 260):
    row = a[y, 719:873]
    nonwhite = ((row[:, 0] < 235) | (row[:, 1] < 235) | (row[:, 2] < 235)).sum()
    if nonwhite > 120:
        print(f'  gridline row y={y} nonwhite={nonwhite}')
for x in range(715, 880):
    col = a[130:246, x]
    nonwhite = ((col[:, 0] < 235) | (col[:, 1] < 235) | (col[:, 2] < 235)).sum()
    if nonwhite > 80:
        print(f'  gridline col x={x} nonwhite={nonwhite}')
print('  fill samples y row band1:', [tuple(a[238, x]) for x in (740, 790, 840)])
print('  fill samples y row band2:', [tuple(a[378, x]) for x in (740, 790, 840)])
print('  fill samples y row band3:', [tuple(a[515, x]) for x in (740, 790, 840)])
print('  white body sample band1:', tuple(a[200, 745]))
ink_bbox(719, 160, 770, 188, redmask, 'test c1 30 (red)')
ink_bbox(770, 160, 821, 188, bluemask, 'test c2 40 (blue)')
ink_bbox(821, 160, 872, 188, redmask, 'test c3 50 (red)')
ink_bbox(719, 127, 770, 157, redmask, 'test header Test1')

print('\n== LABEL BOXES ==')
# fill bbox: blue mask
ink_bbox(80, 85, 200, 135, bluemask, 'Train box blue fill')
core_color(80, 85, 200, 135, bluemask, 'Train box core')
ink_bbox(780, 85, 890, 135, bluemask, 'Test box blue fill')
core_color(780, 85, 890, 135, bluemask, 'Test box core')
# white text inside blue: pixels near-white inside box
subT = a[95:127, 95:165]
wm = (subT[:, :, 0] > 200) & (subT[:, :, 1] > 200) & (subT[:, :, 2] > 200)
ys, xs = np.where(wm)
print(f'Train white text ink x{95+xs.min()}..{95+xs.max()} y{95+ys.min()}..{95+ys.max()} n={wm.sum()}')

print('\n== W BOX band1 ==')
ink_bbox(495, 120, 640, 260, redmask, 'W box red border')
core_color(495, 120, 640, 260, redmask, 'W box border core')
# W glyph (italic serif red) region left of bracket
ink_bbox(515, 155, 570, 210, redmask, 'W glyph + = (red)')
core_color(515, 155, 570, 210, redmask, 'W glyph core')
# bracket strokes: thin dark vertical curves between x560..600
sub = a[130:230, 555:610]
dm = darkmask(sub)
for x in range(555, 610):
    col = dm[:, x - 555]
    if col.sum() > 20:
        ys = np.where(col)[0]
        print(f'  dark col x={x} n={col.sum()} y{130+ys.min()}..{130+ys.max()}')
# digits region
ink_bbox(565, 130, 600, 215, darkmask, 'vector digits (dark)')

print('\n== ELLIPSE band1 ==')
ink_bbox(495, 205, 640, 255, yellowmask, 'ellipse yellow fill')
core_color(495, 205, 640, 255, yellowmask, 'ellipse fill core')
# text on ellipse: darker than fill
sub = a[215:250, 505:625]
tm = (sub[:, :, 0] < 150) & (sub[:, :, 1] < 150) & (sub[:, :, 2] < 150)
ys, xs = np.where(tm)
print(f'ellipse text ink x{505+xs.min()}..{505+xs.max()} y{215+ys.min()}..{215+ys.max()} n={tm.sum()}')
if tm.sum():
    med = np.median(sub[tm], axis=0).astype(int)
    print('ellipse text core rgb=', tuple(med), f'hex={med[0]:02X}{med[1]:02X}{med[2]:02X}')

print('\n== ARROWS band1 ==')
ink_bbox(455, 175, 515, 220, bluemask, 'left arrow blue')
ink_bbox(620, 175, 680, 220, bluemask, 'right arrow blue')
# shaft/head profile of left arrow: row extents per column
for x in range(460, 508, 2):
    col = a[180:215, x]
    m = bluemask(col[None, :, :])[0]
    ys = np.where(m)[0]
    if len(ys):
        print(f'  left arrow x={x} blue y{180+ys.min()}..{180+ys.max()} n={len(ys)}')

print('\n== band 2 / 3 W box + ellipse ==')
for bi, (y0, y1) in enumerate([(260, 395), (398, 530)]):
    ink_bbox(495, y0, 640, y1, redmask, f'W box band{bi+2} border')
    ink_bbox(495, y0, 640, y1, yellowmask, f'ellipse band{bi+2} fill')
print('\n== band 2 label band (expect none) ==')
ink_bbox(80, 250, 200, 290, bluemask, 'blue label band2')
ink_bbox(780, 250, 890, 290, bluemask, 'blue label band2 right')
