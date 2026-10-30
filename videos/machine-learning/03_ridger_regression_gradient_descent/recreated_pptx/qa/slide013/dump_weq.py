import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
RED = (r > g + 40) & (r > b + 40)

# the red cluster x527..543 y163..179 is 'W=' probably; the digits to the right
# (x572..600) are a DIFFERENT colour. Identify them.
print("### colour of the digit glyphs at x570..600 y163..180 (B1)")
m = (lum[163:181, 570:601] < 210)
ys, xs = np.where(m)
if len(ys):
    vals = a[163:181, 570:601][m]
    import collections
    cc = collections.Counter((v[0] // 30, v[1] // 30, v[2] // 30) for v in vals)
    print("  dark-px colour histogram (R//30,G//30,B//30):", cc.most_common(6))
    print("  bbox x%d..%d y%d..%d" % (xs.min() + 570, xs.max() + 570, ys.min() + 163, ys.max() + 163))
print("  BLUE px in that window:", int(BLUE[163:181, 570:601].sum()))
print("  RED px in that window:", int(RED[163:181, 570:601].sum()))

print()
print("### the W=' red cluster x525..548 y160..182 zoomed")
Z = 6
sub = np.asarray(im.crop((524, 160, 548, 184)).resize((24 * Z, 24 * Z), Image.LANCZOS)).astype(float)
lu = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
for y in range(0, lu.shape[0], 3):
    print(f"{160 + y//Z:4d}| " + ''.join('#' if lu[y, x] < 205 else ('+' if lu[y, x] < 235 else '.') for x in range(0, lu.shape[1], 3)))
