import numpy as np
from PIL import Image

im = Image.open('unique_slides/slide_031.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

# column gray profile inside the plot, excluding the parabola rows
grayish = (abs(a[:, :, 0] - a[:, :, 1]) < 14) & (abs(a[:, :, 1] - a[:, :, 2]) < 14) \
          & (a[:, :, 0] > 165) & (a[:, :, 0] < 228)
sub = grayish[70:262, 574:808]
prof = sub.sum(axis=0)
print('=== x-grid profile (col: count), peaks ===')
peaks = [(574 + i, c) for i, c in enumerate(prof) if c > 120]
for x, c in peaks:
    print('  x=%d count=%d' % (x, c))

print('=== full profile sampled ===')
for i in range(0, 234, 2):
    print('   x=%d count=%d' % (574 + i, prof[i]))
