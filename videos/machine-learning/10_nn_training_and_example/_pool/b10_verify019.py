from PIL import Image
import numpy as np

im = Image.open('qa/slide019/rejudge/render-attempt3.png').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print('size', W, 'x', H, 'dpi150 -> in', W/150.0, 'x', H/150.0)
lum = a.sum(axis=2) / 3.0
ink = lum < 200

def px_in(x_in, y_in):
    return int(round(x_in * 150)), int(round(y_in * 150))

# statement line 1 band (y 127-175 px, x 94-340 px): black subscript ink should be present
band = ink[127:175, 94:340]
print('statement-line1 black px:', int(band.sum()))
ys, xs = np.nonzero(band)
if len(xs):
    print('  bbox x', xs.min(), xs.max(), 'y', ys.min(), ys.max())

# region colors in the statement line 1 band
sub = a[127:175, 94:340]
dark = sub[sub.sum(axis=2) / 3.0 < 200]
if len(dark):
    cols, counts = np.unique(dark, axis=0, return_counts=True)
    order = np.argsort(-counts)[:6]
    for i in order:
        print('  color', cols[i], counts[i])

# eq4 containment: panel/bottom-right region beyond x=12.93in
x0, y0 = px_in(12.95, 6.35)
x1, y1 = px_in(13.33, 7.2)
reg = ink[y0:y1, x0:x1]
print('eq4 beyond-edge ink px (x>12.95in):', int(reg.sum()))

# overall right-edge strip beyond 13.0in (house slide edge)
x0, y0 = px_in(13.05, 0.15)
x1, y1 = px_in(13.33, 7.35)
print('right strip >13.05in ink px:', int(ink[y0:y1, x0:x1].sum()))

# eq1 (backprop chain) statement-1 line region: ink bbox
x0, y0 = px_in(0.4, 1.1)
x1, y1 = px_in(8.5, 2.0)
reg = ink[y0:y1, x0:x1]
ys, xs = np.nonzero(reg)
if len(xs):
    print('eq1 region bbox in:', round(xs.min()/150,3), round(xs.max()/150,3),
          round(ys.min()/150,3), round(ys.max()/150,3), 'px', int(reg.sum()))

# bottom-right panel (partials) legibility: 14pt text ink present
x0, y0 = px_in(9.2, 4.4)
x1, y1 = px_in(12.7, 6.9)
reg = ink[y0:y1, x0:x1]
print('bottom-right panel ink px:', int(reg.sum()))
ys, xs = np.nonzero(reg)
if len(xs):
    print('  bbox in:', round(0.4 + xs.min()/150,3), round(0.4 + xs.max()/150,3),
          round(4.4 + ys.min()/150,3), round(4.4 + ys.max()/150,3))

# cyan ji box text present (left diagram area)
x0, y0 = px_in(0.5, 3.2)
x1, y1 = px_in(9.0, 5.6)
print('diagram region ink px:', int(ink[y0:y1, x0:x1].sum()))
