import numpy as np
from PIL import Image
ORIG = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_005.jpg"
REND = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/render_8.png"
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
SX, SY = 2001/960.0, 1125/540.0
print("ORIGINAL: column ink counts, x676..690, y464..498 (green box left edge is x688..690)")
for x in range(676, 692):
    col = o[464:499, x]
    print("  x=%d ink=%3d min=%3d %s" % (x, int((col.mean(axis=1) < 200).sum()), col.mean(axis=1).min(),
          "GREEN BORDER" if x in (688, 689, 690) else ""))
print()
print("RENDER x676..690 (col mean lum<200 count)")
for x in range(676, 692):
    X = int(x*SX)
    col = r[int(464*SY):int(499*SY), X:int(x*SX)+2].mean(axis=2)
    print("  x=%d ink=%3d min=%3d %s" % (x, int((col < 200).sum()), col.min(),
          "GREEN BORDER" if x in (688, 689, 690) else ""))
print()
print("=== original: is there ink at x682..683 across y464..498 (eq5 arrow tip)? ===")
print("  total ink px:", int((o[464:499, 682:684].mean(axis=2) < 200).sum()))
print("=== render: same ===")
print("  total ink px:", int((r[int(464*SY):int(499*SY), int(682*SX):int(684*SX)].mean(axis=2) < 200).sum()))
print()
print("=== finalw content ink in both, window x692..876 y467..496 ===")
def ink(arr, x0,x1,y0,y1, sx, sy):
    X0,X1,Y0,Y1 = int(x0*sx),int(x1*sx),int(y0*sy),int(y1*sy)
    sub = arr[Y0:Y1+1, X0:X1+1].mean(axis=2) < 200
    if not sub.any(): return None
    ys,xs = np.nonzero(sub)
    return (round((X0+xs.min())/sx,1), round((X0+xs.max())/sx,1), round((Y0+ys.min())/sy,1), round((Y0+ys.max())/sy,1))
print("  ORIG:", ink(o, 692, 876, 467, 496, 1, 1))
print("  REND:", ink(r, 692, 876, 467, 496, SX, SY))
