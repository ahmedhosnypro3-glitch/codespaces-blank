# precise color + geometry probes on original slide_030
import numpy as np
from PIL import Image

a = np.asarray(Image.open("unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W = a.shape[:2]

def sample(x, y, label, rad=2):
    patch = a[max(0,y-rad):y+rad+1, max(0,x-rad):x+rad+1].reshape(-1,3)
    print(f"{label:38s} ({x:3d},{y:3d}) median={tuple(np.median(patch,axis=0).astype(int))}")

print("--- green weight-label components ---")
for (x0,x1,y0,y1) in [(276,287,144,153),(285,294,105,114),(276,284,173,182),(300,308,189,198)]:
    sub = a[y0:y1+1, x0:x1+1].reshape(-1,3)
    m = sub[(sub.sum(axis=1) < 700)]
    if len(m):
        print(f"  x{x0}-{x1} y{y0}-{y1}: darkest median={tuple(np.median(m,axis=0).astype(int))} n={len(m)}")

print("--- red title box region ---")
sample(75, 66, "title box left border")
sample(160, 60, "title box top-right")
sample(100, 77, "title box bottom")
sample(150, 70, "title text ink")

print("--- pink Bad Weights box: search ---")
pinkm = (a[:,:,0] > 235) & (a[:,:,1] > 190) & (a[:,:,1] < 220) & (a[:,:,2] > 150) & (a[:,:,2] < 200)
ys, xs = np.where(pinkm)
if len(xs):
    print("pink bbox", xs.min(), xs.max(), ys.min(), ys.max(), "n", len(xs))
    # restrict to left half
    sel = xs < 400
    print("left-half pink bbox", xs[sel].min(), xs[sel].max(), ys[sel].min(), ys[sel].max(), "n", sel.sum())
else:
    print("no pink found")

print("--- panel borders loose threshold ---")
loose = (a[:,:,0] > 120) & (a[:,:,0]-a[:,:,1] > 45) & (a[:,:,0]-a[:,:,2] > 45)
for y in range(56, 62):
    xs = np.where(loose[y])[0]
    print(f"row y={y}: n={len(xs)}", (xs.min(), xs.max()) if len(xs) else "")
for y in range(243, 251):
    xs = np.where(loose[y])[0]
    print(f"row y={y}: n={len(xs)}", (xs.min(), xs.max()) if len(xs) else "")
for x in range(186, 196):
    ys = np.where(loose[:, x])[0]
    print(f"col x={x}: n={len(ys)}", (ys.min(), ys.max()) if len(ys) else "")
