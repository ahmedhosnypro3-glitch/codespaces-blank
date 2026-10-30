from PIL import Image
import numpy as np, collections
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
mx=O.max(axis=2); mn=O.min(axis=2)
gray=(mx-mn)<20
dark=gray&(mx<212)          # curve + axes + text, excludes 224 gridlines and 240 bg
reg=dark[67:309,574:809]
ys,xs=np.nonzero(reg)
print("dark px in plot interior:",len(xs))
cnt=collections.Counter(map(tuple,(O[67:309,574:809][reg]//16*16)))
for c,n in cnt.most_common(12): print("  ",c,n)
print()
# column profile of dark pixels inside x 600..790, y 68..264 (above x-axis)
print("== per-column dark y positions (x 600..790) ==")
for x in range(600,792,4):
    idx=np.nonzero(dark[68:264,x])[0]+68
    if len(idx): print("  x",x, list(idx))
