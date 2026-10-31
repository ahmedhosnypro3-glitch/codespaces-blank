import numpy as np
from PIL import Image
NS="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
def dark(a,l=150):
    return (a[:,:,0]*299+a[:,:,1]*587+a[:,:,2]*114)/1000.0 < l
print("### 023 inner-ring vertical extent (cols 61,62,863) and row 523 span")
a=np.asarray(Image.open(f"{NS}/unique_slides/slide_023.jpg").convert("RGB")).astype(int); m=dark(a)
for x in (61,62,860,861,863,864):
    ys=np.nonzero(m[:,x])[0]; print(f"  col {x}: rows {ys.min() if len(ys) else '-'}..{ys.max() if len(ys) else '-'} n={len(ys)}")
for y in (58,523):
    xs=np.nonzero(m[y,:])[0]; print(f"  row {y}: cols {xs.min()}..{xs.max()} n={len(xs)}")
print("### 014: cols 65-72 rows where dark, and col 901/58 ring rows")
a=np.asarray(Image.open(f"{NS}/unique_slides/slide_014.jpg").convert("RGB")).astype(int); m=dark(a)
for x in (65,66,67,68,69,70,71,72):
    ys=np.nonzero(m[:,x])[0]
    print(f"  col {x}: rows {ys.min() if len(ys) else '-'}..{ys.max() if len(ys) else '-'} n={len(ys)}")
for y in (43,516):
    xs=np.nonzero(m[y,:])[0]; print(f"  row {y}: cols {xs.min()}..{xs.max()} n={len(xs)}")
print("### 023/024 outer ring row extents")
for n in ("023","024"):
    a=np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int); m=dark(a)
    for y in (43,538,539):
        xs=np.nonzero(m[y,:])[0]; print(f"  {n} row {y}: cols {xs.min()}..{xs.max()} n={len(xs)}")
    for x in (38,920):
        ys=np.nonzero(m[:,x])[0]; print(f"  {n} col {x}: rows {ys.min()}..{ys.max()} n={len(ys)}")
