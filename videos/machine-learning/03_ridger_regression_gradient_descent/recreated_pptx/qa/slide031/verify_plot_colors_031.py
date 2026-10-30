from PIL import Image
import numpy as np, collections
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
reg=O[68:308,576:807].reshape(-1,3)
# quantize
q=(reg//16*16)
cnt=collections.Counter(map(tuple,q))
print("top colors in plot interior:")
for c,n in cnt.most_common(25): print(" ",c,n)
print()
# find non-gray chromatic pixels
mx=reg.max(axis=1); mn=reg.min(axis=1)
chrom=reg[(mx-mn)>40]
print("chromatic px:",len(chrom))
cnt2=collections.Counter(map(tuple,(chrom//16*16)))
for c,n in cnt2.most_common(20): print(" ",c,n)
