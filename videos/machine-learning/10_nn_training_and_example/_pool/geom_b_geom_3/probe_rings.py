import numpy as np
from PIL import Image
NS="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
def dark(a,l=150):
    lum=(a[:,:,0]*299+a[:,:,1]*587+a[:,:,2]*114)/1000.0
    return lum<l
for n in ["014","016","017","023","024"]:
    a=np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    m=dark(a)
    print(f"== {n}  size={a.shape[1]}x{a.shape[0]}")
    # column profile in content vertical span (exclude top/bottom 40 rows)
    col=m[60:500,:].sum(0)
    dk=[x for x in range(a.shape[1]) if col[x]>200]
    print("  dense cols(>200):",dk)
    row=m[:,100:800].sum(1)
    dkr=[y for y in range(a.shape[0]) if row[y]>250]
    print("  dense rows(>250):",dkr)
