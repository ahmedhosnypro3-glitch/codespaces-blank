"""Self-check 3 — slide 030: parabola trace comparison orig vs render.
Axis map (from build + verified grid): X0=630.5, Y0=266.5, UX=11.45, UY=12.0 frame px.
Curve: f(x)=(x-5)^2+1 -> x(y) = 5 +- sqrt(y-1)."""
import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540
X0, Y0, UX, UY = 630.5, 266.5, 11.45, 12.0

def traces(img, sx, sy, name):
    # plot interior in this image's px
    x0,x1,y0,y1 = int(573*sx), int(809*sx), int(67*sy), int(310*sy)
    sub = img[y0:y1, x0:x1]
    B,R = sub[:,:,2], sub[:,:,0]
    # blue-ish: original is faded (B>R+15); render is 4F81BD (B>R+60)
    mask = (B > R + (15 if name=='orig' else 50)) & (B > 100)
    L, Rr = [], []   # frame-px x of left/right branch per row
    for i in range(mask.shape[0]):
        xs = np.nonzero(mask[i])[0]
        if len(xs) >= 2:
            # split runs: skip if the row has one run only (vertex neighborhood)
            runs = []
            s = xs[0]; p = xs[0]
            for v in xs[1:]:
                if v - p > 3: runs.append((s, p)); s = v
                p = v
            runs.append((s, p))
            if len(runs) >= 2:
                L.append((i+y0, (runs[0][0]+runs[0][1])/2 + x0))
                Rr.append((i+y0, (runs[-1][0]+runs[-1][1])/2 + x0))
    return L, Rr

for img, sx, sy, name in ((orig, 1, 1, 'orig'), (ren, SX, SY, 'render')):
    L, Rr = traces(img, sx, sy, name)
    print(f"== {name}: left-branch rows={len(L)} right-branch rows={len(Rr)} ==")
    # convert to data coords and compare with x = 5 -+ sqrt(f-1), f = (Y0-y)/UY
    devs = []
    for (y_px, x_px) in L + Rr:
        fx, fy = x_px/sx, y_px/sy
        f = (Y0 - fy)/UY
        if f < 1.05: continue
        exp = 5 - np.sqrt(f-1) if (y_px, x_px) in L else 5 + np.sqrt(f-1)
        got = X0 + (x_px/sx - X0)  # data x
        got_d = (x_px/sx - X0)/UX
        devs.append(abs(got_d - exp))
    if devs:
        devs = np.array(devs)
        print(f"   branch-vs-analytic deviation (data units): mean={devs.mean():.4f} max={devs.max():.4f} n={len(devs)}")
        print(f"   in frame px: mean={devs.mean()*UX:.2f} max={devs.max()*UX:.2f}")
    # vertex row extent (rows where the two branches merge): bottom of left branch
    if L:
        print(f"   left branch top y={L[0][0]/sy:.0f} bottom y={L[-1][0]/sy:.0f}; right top y={Rr[0][0]/sy:.0f} bottom y={Rr[-1][0]/sy:.0f}")

# vertex position comparison: lowest blue row in each image near x=688
for img, sx, sy, name in ((orig,1,1,'orig'),(ren,SX,SY,'render')):
    x0,x1,y0,y1 = int(660*sx), int(716*sx), int(200*sy), int(310*sy)
    sub = img[y0:y1, x0:x1]
    B,R = sub[:,:,2], sub[:,:,0]
    mask = (B > R + (15 if name=='orig' else 50)) & (B > 100)
    ys, xs = np.nonzero(mask)
    if len(ys):
        cxm = (xs.min()+xs.max())/2 + x0
        print(f"{name}: vertex blue bbox x{xs.min()+x0:.0f}..{xs.max()+x0:.0f} y{ys.min()+y0:.0f}..{ys.max()+y0:.0f} -> frame ({(xs.min()+x0)/sx:.1f}..{(xs.max()+x0)/sx:.1f}, {(ys.min()+y0)/sy:.1f}..{(ys.max()+y0)/sy:.1f}) center_x_frame={(cxm)/sx:.1f}")

# second-difference ripple along each branch (render, left branch): should be smooth (monotone curve)
ren_img, sx, sy = ren, SX, SY
L, Rr = traces(ren_img, sx, sy, 'render')
if L:
    xs_arr = np.array([v for _, v in L])
    d2 = np.diff(xs_arr, 2)
    print(f"render left-branch second-difference: mean={d2.mean():.4f} std={d2.std():.4f} max|d2|={np.abs(d2).max():.3f} render px (row-to-row)")
    # expected d2 for a parabola sampled per pixel row: x(y)=5-sqrt(y-1) has nonzero but smooth d2
    ys_arr = np.array([y for y, _ in L])
    f = (Y0 - ys_arr/sy)/UY
    exp_x = X0 - np.sqrt(np.maximum(f-1, 0))*UX
    d2e = np.diff(exp_x, 2)
    print(f"expected analytic second-difference: mean={d2e.mean():.4f} max|d2e|={np.abs(d2e).max():.3f}")
