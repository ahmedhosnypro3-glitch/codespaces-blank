# b09: per-feature bbox comparison, original vs render (both 960x540).
# usage: python3 b09_v3_check.py <render.png>
import sys
from PIL import Image
import numpy as np

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example'
O = np.asarray(Image.open(NS + '/unique_slides/slide_018.jpg').convert('RGB')).astype(int)
R = np.asarray(Image.open(sys.argv[1]).convert('RGB').resize((960, 540), Image.LANCZOS)).astype(int)

def feat(img, x0, y0, x1, y1, pred):
    m = np.zeros(img.shape[:2], bool)
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(img[y, x]): m[y, x] = True
    if not m.any(): return None
    ys, xs = np.nonzero(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(m.sum()))

def cmps(name, a, b, tol=4):
    if a is None or b is None:
        print(f'{name:22s} orig={a} render={b}  <-- MISSING'); return
    d = [b[0]-a[0], b[2]-a[2], b[1]-a[1], b[3]-a[3]]
    ok = all(abs(v) <= tol for v in d)
    print(f'{name:22s} orig={a[:4]} render={b[:4]}  dx0={d[0]:+3d} dx1={d[1]:+3d} dy0={d[2]:+3d} dy1={d[3]:+3d}  npx {a[4]}->{b[4]}  {"OK" if ok else "<< OVER"}')

black = lambda c: c[0] < 110 and c[1] < 110 and c[2] < 110
red = lambda c: c[0] > 110 and c[0]-c[1] > 55 and c[0]-c[2] > 40
green = lambda c: c[1]-c[0] > 18 and c[1] > 120 and c[2] < c[1]-15
blue = lambda c: c[2] > 80 and c[2]-c[0] > 40 and c[2]-c[1] > 40 and c[0] < 160
mag = lambda c: c[0] > 90 and c[1] < 95 and c[2] > 75 and c[0]-c[1] > 40 and c[2]-c[1] > 35
cream = lambda c: abs(c[0]-218) < 14 and abs(c[1]-206) < 14 and abs(c[2]-194) < 14

print('--- features (960-space) ---')
cmps('equation black', feat(O, 820, 95, 876, 160, black), feat(R, 820, 95, 876, 160, black))
cmps('red question mark', feat(O, 868, 105, 895, 145, red), feat(R, 868, 105, 895, 145, red))
cmps('error column red', feat(O, 750, 60, 780, 195, red), feat(R, 750, 60, 780, 195, red))
cmps('class label col', feat(O, 774, 70, 828, 185, green), feat(R, 774, 70, 828, 185, green))
cmps('output label col', feat(O, 698, 70, 750, 185, blue), feat(R, 698, 70, 750, 185, blue))
cmps('cream panel', feat(O, 355, 45, 765, 212, cream), feat(R, 355, 45, 765, 212, cream))
cmps('bottom magenta', feat(O, 360, 180, 615, 210, mag), feat(R, 360, 180, 615, 210, mag))
cmps('input-data text', feat(O, 376, 188, 410, 202, mag), feat(R, 376, 188, 410, 202, mag))
cmps('network dark ink', feat(O, 365, 55, 702, 210, black), feat(R, 365, 55, 702, 210, black))
cmps('network green', feat(O, 365, 55, 702, 210, green), feat(R, 365, 55, 702, 210, green))
cmps('network red', feat(O, 365, 55, 702, 210, red), feat(R, 365, 55, 702, 210, red))

print()
print('--- ink coverage in diagram band x365..700 y55..210 ---')
for lbl, img in (('orig', O), ('render', R)):
    reg = img[55:210, 365:700].reshape(-1, 3)
    ink = ((reg.max(axis=1) - reg.min(axis=1)) > 22) | (reg.mean(axis=1) < 200)
    print(f'  {lbl}: coloured-or-dark px = {int(ink.sum())} of {len(reg)} ({100*ink.mean():.1f}%)')
