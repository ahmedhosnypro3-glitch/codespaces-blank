from PIL import Image
import numpy as np, collections
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
def stats(name,x0,x1,y0,y1,mask=None):
    reg=O[y0:y1,x0:x1].reshape(-1,3)
    if mask is not None:
        m=mask[y0:y1,x0:x1].reshape(-1); reg=reg[m]
    c=collections.Counter(map(tuple,reg))
    print(f"-- {name} x{x0}..{x1} y{y0}..{y1} n={len(reg)} modal:", c.most_common(6))
V=O.max(axis=2)
# curve arm: x644..656, y79..135  (left branch away from other ink)
stats("curve left arm",644,656,79,135)
stats("curve right arm",706,720,177,235)
stats("chord row146",665,747,145,148)
stats("chord tick",658,666,144,161)
stats("dashed vert x687",686,690,68,120)
stats("dashed vert x745",744,747,68,120)
stats("green marker",676,702,246,258)
stats("(5,1) label",492,561,248,262)
stats("xtick band",578,806,268,291)
stats("plot bg clean",600,630,95,140)
