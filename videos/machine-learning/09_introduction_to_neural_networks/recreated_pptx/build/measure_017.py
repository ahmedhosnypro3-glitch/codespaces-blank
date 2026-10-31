"""PIL measurements for slide 017 (unique_slides/slide_017.jpg, 960x540).
Locate: content frame, title ink, panel borders, callout boxes, step levels."""
from PIL import Image
import numpy as np

P = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
     "09_introduction_to_neural_networks/unique_slides/slide_017.jpg")
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
h, w, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# dark-red title ink (r high, g/b very low)
tmask = (r > 100) & (g < 60) & (b < 60)
ys, xs = np.where(tmask)
print("dark-red ink bbox:", xs.min(), ys.min(), xs.max(), ys.max(), "n=", len(xs))
# restrict to top band for title
t2 = tmask[:120, :]
ys, xs = np.where(t2)
print("title band bbox:", xs.min(), ys.min(), xs.max(), ys.max(), "n=", len(xs))

# panel border blue: b much larger than g, r low
blue = (b > 120) & (b - r > 40) & (b - g > 20)
# long vertical/horizontal runs of blue
colsum = blue.sum(axis=0)
print("blue cols >100px:", [(i, int(colsum[i])) for i in np.argsort(colsum)[-8:]])
rowsum = blue.sum(axis=1)
print("blue rows >100px:", [(i, int(rowsum[i])) for i in np.argsort(rowsum)[-8:]])

# pink frame: b>g, r>g moderately
pink = (r > g + 5) & (b > g + 5) & (r > 180)
prow = pink.sum(axis=1); pcol = pink.sum(axis=0)
print("pink rows >300:", [(i, int(prow[i])) for i in range(len(prow)) if prow[i] > 300])
print("pink cols >300:", [(i, int(pcol[i])) for i in range(len(pcol)) if pcol[i] > 300])

# near-black axes
blk = (r < 70) & (g < 70) & (b < 70)
brow = blk.sum(axis=1); bcol = blk.sum(axis=0)
print("black rows >150:", [(i, int(brow[i])) for i in range(len(brow)) if brow[i] > 150])
print("black cols >150:", [(i, int(bcol[i])) for i in range(len(bcol)) if bcol[i] > 150])

# black bottom band
print("bottom band rows:", [(i, int(blk[i].sum())) for i in range(510, 540) if blk[i].sum() > 200])
