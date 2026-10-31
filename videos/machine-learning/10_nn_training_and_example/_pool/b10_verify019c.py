from PIL import Image
import numpy as np

im = Image.open('qa/slide019/rejudge/render-attempt3.png').convert('RGB')
a = np.asarray(im).astype(int)
lum = a.sum(axis=2) / 3.0
ink = lum < 200
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 130) & (g < 110) & (b < 110)
nonred = ink & ~red

# row profile of nonred ink on the right half (x >= 9.0in = 1350px)
rh = nonred[:, 1350:]
rows = rh.sum(axis=1)
runs = []
inrun = False
for y, v in enumerate(rows):
    if v > 0 and not inrun:
        start = y; inrun = True
    elif v == 0 and inrun:
        runs.append((start, y - 1)); inrun = False
if inrun: runs.append((start, len(rows) - 1))
print('right-half nonred ink row bands (in):')
for s, e in runs:
    seg = rh[s:e+1]
    xs = np.nonzero(seg.any(axis=0))[0]
    print('  y %.3f-%.3f  x %.3f-%.3f in  px=%d' % (
        s / 150, (e + 1) / 150, 9.0 + xs.min() / 150, 9.0 + xs.max() / 150, int(seg.sum())))

# colors of the beyond-12.93in pixels
x0 = int(12.93 * 150)
reg = a[:, x0:]
m = nonred[:, x0:]
ys, xs = np.nonzero(m)
if len(xs):
    cols = reg[ys, xs]
    u, c = np.unique(cols, axis=0, return_counts=True)
    order = np.argsort(-c)[:8]
    for i in order:
        print('beyond-12.93 color', u[i], c[i])
