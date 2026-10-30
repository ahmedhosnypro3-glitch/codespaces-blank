"""Title shift via cross-correlation + x-row red cells with loose (JPEG-red) mask."""
import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540

# ---- title bands as ink bitmaps (frame scale) ----
def band(img, scx, scy, y0, y1, x0, x1, thr):
    X0, X1 = int(round(x0*scx)), int(round(x1*scx))
    Y0, Y1 = int(round(y0*scy)), int(round(y1*scy))
    sub = img[Y0:Y1, X0:X1]
    return (sub.sum(axis=2) < thr)

# render band downscaled to frame px: use rendering at native then compare via resampling
R = band(ren, SX, SY, 55, 105, 60, 570, 700)
O = band(orig, 1, 1, 55, 105, 60, 570, 700)
# resize render band to frame size
Rimg = Image.fromarray((R*255).astype(np.uint8)).resize((R.shape[1]//2, R.shape[0]//2), Image.LANCZOS)
Rb = np.asarray(Rimg) > 60
print("render band shape (frame px):", Rb.shape, " orig:", O.shape)
best = None
for dy in range(-12, 13):
    for dx in range(-30, 11):
        # shift Rb by (dy,dx) against O
        h, w = O.shape
        ys0, xs0 = max(0, dy), max(0, dx)
        ys1, xs1 = min(h, h+dy), min(w, w+dx)
        if ys1-ys0 < 10 or xs1-xs0 < 10: continue
        A = O[ys0:ys1, xs0:xs1]
        B = Rb[ys0-dy:ys1-dy, xs0-dx:xs1-dx]
        score = (A ^ B).sum() - abs(A.sum()-B.sum())*2
        if best is None or score < best[0]:
            best = (score, dx, dy)
print(f"TITLE best alignment shift: dx={best[1]} dy={best[2]} (render must move by -dx,-dy: move {best[1]} left, {best[2]} up)")
print(f"  -> title box x should be 57 + {-best[1]} = {57 - best[1]}; box y should be 62 + {-best[2]} = {62 - best[2]}")

# ---- x-row red cells, loose mask ----
print("\n== X-ROW red ink (loose JPEG-red mask), original -=")
Rr, Gg, Bb = orig[:,:,0], orig[:,:,1], orig[:,:,2]
m = (Rr > 90) & ((Rr-Gg) > 40) & ((Rr-Bb) > 10)
sub = m[330:380, 80:660]
cols = np.nonzero(sub.any(axis=0))[0]
runs = []
if len(cols):
    s = cols[0]; p = cols[0]
    for v in cols[1:]:
        if v-p > 3: runs.append((s,p)); s = v
        p = v
    runs.append((s,p))
print("   red col-runs (frame x):", [(80+a, 80+b) for a, b in runs])
# cell centers: 150+22+44k for k=0..10 -> 172..612
print("   expected value-cell centers: 172,216,260,304,348,392,436,480,524,568,612")

print("\n== X-ROW red ink, render -=")
Rr2, Gg2, Bb2 = ren[:,:,0], ren[:,:,1], ren[:,:,2]
m2 = (Rr2 > 90) & ((Rr2-Gg2) > 40) & ((Rr2-Bb2) > 10)
x0,y0,x1,y1 = int(80*SX), int(330*SY), int(660*SX), int(380*SY)
sub2 = m2[y0:y1, x0:x1]
cols = np.nonzero(sub2.any(axis=0))[0]
runs = []
if len(cols):
    s = cols[0]; p = cols[0]
    for v in cols[1:]:
        if v-p > 3: runs.append((s,p)); s = v
        p = v
    runs.append((s,p))
print("   red col-runs (frame x):", [(round((x0+a)/SX), round((x0+b)/SX)) for a, b in runs])
