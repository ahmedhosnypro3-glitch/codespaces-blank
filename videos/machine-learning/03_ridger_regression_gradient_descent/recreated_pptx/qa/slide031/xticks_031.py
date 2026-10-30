from PIL import Image
import numpy as np
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
V=O.max(axis=2)
print("== dark(V<200) column profile, x 573..809, y 67..312 ==")
for x in range(573,810):
    c=(V[67:312,x]<200).sum()
    if c>60: print("  x",x,c)
print()
print("== dark(V<200) x-positions per row y 264..300 (x 573..809) ==")
for y in range(264,301):
    xs=np.nonzero(V[y,573:809]<200)[0]+573
    if len(xs): print("  y",y,list(xs))
print()
print("== dark(V<200) column profile for y 264..312 ==")
for x in range(573,810):
    c=(V[264:312,x]<200).sum()
    if c>3: print("  x",x,c)
