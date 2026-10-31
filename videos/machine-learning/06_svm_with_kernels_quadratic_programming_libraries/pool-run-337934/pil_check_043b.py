import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ren = np.asarray(Image.open(NS + "/recreated_pptx/renders/slide_043_recreated-1.png").convert("RGB")).astype(int)
orig = np.asarray(Image.open(NS + "/qa/rejudge2/orig_png/slide_043.png").convert("RGB")).astype(int)
# normalize orig 960x540 -> 2001x1125 by scaling coords
sx, sy = 2001/960, 1125/540

def mask(arr, hexc, tol=70):
    r, g, b = int(hexc[0:2],16), int(hexc[2:4],16), int(hexc[4:6],16)
    return (abs(arr[...,0]-r)<tol)&(abs(arr[...,1]-g)<tol)&(abs(arr[...,2]-b)<tol)

for name, c in [("blue","0000FF"),("green","00FF00"),("yellow","FFFF00"),("magenta","FF00FF"),
                ("red","FF0000"),("cyan","00FFFF"),("black","000000")]:
    mr = mask(ren, c); mo = mask(orig, c)
    if mr.sum() < 5 or mo.sum() < 5:
        print(name, "too few px", mr.sum(), mo.sum()); continue
    yr, xr = np.nonzero(mr); yo, xo = np.nonzero(mo)
    cr = (xr.mean()/2001, yr.mean()/1125); co = (xo.mean()*sx/2001, yo.mean()*sy/1125)
    # spread (std) normalized
    sr = (xr.std()/2001, yr.std()/1125); so = (xo.std()*sx/2001, yo.std()*sy/1125)
    print(f"{name:8s} centroid render {cr[0]:.3f},{cr[1]:.3f} orig {co[0]:.3f},{co[1]:.3f} | std render {sr[0]:.3f},{sr[1]:.3f} orig {so[0]:.3f},{so[1]:.3f} | n {mr.sum()}/{mo.sum()}")
