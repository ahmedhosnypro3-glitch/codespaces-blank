from PIL import Image
import numpy as np

im = Image.open('qa/slide019/rejudge/render-attempt3.png').convert('RGB')
a = np.asarray(im).astype(int)
lum = a.sum(axis=2) / 3.0
ink = lum < 200
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 130) & (g < 110) & (b < 110)
nonred_ink = ink & ~red

# eq4 line band: y 6.3-6.9in, x from 9.0 to slide edge
y0, y1 = int(6.3 * 150), int(6.9 * 150)
x0 = int(9.0 * 150)
reg = nonred_ink[y0:y1, x0:]
ys, xs = np.nonzero(reg)
if len(xs):
    print('eq4 band nonred bbox: x', round(x0/150 + xs.min()/150, 3),
          '->', round(x0/150 + xs.max()/150, 3), 'in; y',
          round(y0/150 + ys.min()/150, 3), '->', round(y0/150 + ys.max()/150, 3), 'in')

# any nonred ink beyond 12.93in anywhere?
x0 = int(12.93 * 150)
reg = nonred_ink[:, x0:]
ys, xs = np.nonzero(reg)
print('nonred ink px beyond 12.93in (whole slide):', len(xs))
if len(xs):
    yy = np.unique(ys // 15 * 15)
    print('  y bands (px):', yy[:20])

# eq4 exact panel region check (summary's coords): x 1940-1972 px, y 667-720
print('summary-region ink px [667:720,1940:1972]:', int(ink[667:720, 1940:1972].sum()))
print('summary-region red px:', int(red[667:720, 1940:1972].sum()))

# statement line1: confirm subscripts black (dark gray/black), not magenta
sub = a[127:175, 94:340]
mag = (sub[..., 0] > 140) & (sub[..., 1] < 100) & (sub[..., 2] > 100)
print('magenta px in statement line1 band:', int(mag.sum()))
