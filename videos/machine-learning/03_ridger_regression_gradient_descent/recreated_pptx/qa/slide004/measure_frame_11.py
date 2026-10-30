import numpy as np
from PIL import Image
FR = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]; lum=a.mean(axis=2)
red=(R-G>30)&(R-B>30); dark=lum<90
def bbox(mask,label,x0,x1,y0,y1):
    sub=mask[y0:y1,x0:x1]
    if not sub.any(): print(f"  {label}: NONE"); return None
    ys,xs=np.where(sub)
    print(f"  {label}: x {x0+xs.min()}..{x0+xs.max()} (w{1+xs.max()-xs.min()})  y {y0+ys.min()}..{y0+ys.max()} (h{1+ys.max()-ys.min()})")
    return (x0+xs.min(),x0+xs.max(),y0+ys.min(),y0+ys.max())
# BOX1 equation 'Let Y = (vec)_{n x 1}' LEFT of caption 'Original Labels'(x245+)
print("BOX1 eq region (x80..235,y108..206):")
r1=bbox(red,"RED parens",80,235,108,206)
d1=bbox(dark,"dark(LetY+=vec+sub)",80,235,108,206)
# right-most red = right paren edge; subscript sits right of it (still <235)
rx=r1[1]
sub=dark[108:206, rx+1:235]
if sub.any():
    ys,xs=np.where(sub); print(f"  subscript(right of x{rx}): x {rx+1+xs.min()}..{rx+1+xs.max()}  y {108+ys.min()}..{108+ys.max()}")
else: print("  subscript: none")
# left-most red=left paren; dark strictly left of left paren = 'Let Y ='
lx=r1[0]
subL=dark[108:206,80:lx]
if subL.any():
    ys,xs=np.where(subL); print(f"  LetY (left of x{lx}): x {80+xs.min()}..{80+xs.max()}  y {108+ys.min()}..{108+ys.max()}")

print("BOX2 eq region (x420..583,y100..220):")
r2=bbox(red,"RED parens",420,583,100,220)
d2=bbox(dark,"dark(LetYhat+vec+sub)",420,583,100,220)
rx2=r2[1]
sub2=dark[100:220, rx2+1:583]
if sub2.any():
    ys,xs=np.where(sub2); print(f"  subscript(right of x{rx2}): x {rx2+1+xs.min()}..{rx2+1+xs.max()}  y {100+ys.min()}..{100+ys.max()}")
else: print("  subscript: none")
lx2=r2[0]
subL2=dark[100:220,420:lx2]
if subL2.any():
    ys,xs=np.where(subL2); print(f"  LetYhat (left of x{lx2}): x {420+xs.min()}..{420+xs.max()}  y {100+ys.min()}..{100+ys.max()}")
