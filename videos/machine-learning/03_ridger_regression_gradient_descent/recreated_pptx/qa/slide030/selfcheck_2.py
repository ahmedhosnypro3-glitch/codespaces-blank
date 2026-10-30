"""Self-check 2 — slide 030: ink census + element geometry + parabola ripple + containment.
Render render_1.png (2001x1125 @150dpi) vs original unique_slides/slide_030.jpg (960x540)."""
import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540

def census(a, scale, label):
    R,G,B = a[:,:,0], a[:,:,1], a[:,:,2]
    fam = {
      'white': (R>235)&(G>235)&(B>235),
      'gray_panel': (np.abs(R-233)<16)&(np.abs(G-233)<16)&(np.abs(B-231)<18),
      'red_C00000ish': (R>90)&((R-G)>40)&((R-B)>10),
      'green_008000ish': (G>R+20)&(G>B+20)&(G>60)&(G<240),
      'blue_4F81BDish': (B>R+25)&(B>90),
      'magenta': (R>120)&(B>90)&(G<110),
      'purple_7030A0': (R>80)&(R<185)&(B>140)&(G<115),
      'dark': (R<110)&(G<110)&(B<110),
    }
    print(f"-- {label} ({'render' if scale else 'orig'}) --")
    for k, m in fam.items():
        n = int(m.sum())
        if scale: n = int(m.sum())  # report raw render px
        print(f"   {k:14s} {n:8d}")

census(orig, 0, "orig")
census(ren, 1, "render")

def bbox_render(fx0, fy0, fx1, fy1):
    return int(round(fx0*SX)), int(round(fy0*SY)), int(round(fx1*SX)), int(round(fy1*SY))

# ----- element ink bboxes in RENDER, mapped to frame px, vs original measured -----
def ink_bbox(img, mask_fn, x0, y0, x1, y1, scale_to_frame):
    sub = img[y0:y1, x0:x1]
    m = mask_fn(sub)
    ys, xs = np.nonzero(m)
    if not len(xs): return None
    if scale_to_frame:
        return ((x0+xs.min())/SX, (y0+ys.min())/SY, (x0+xs.max())/SX, (y0+ys.max())/SY)
    return (x0+xs.min(), y0+ys.min(), x0+xs.max(), y0+ys.max())

def notwhite(s): return ((s[:,:,0]<228)|(s[:,:,1]<228)|(s[:,:,2]<228))
def isred(s): return (s[:,:,0]>90)&((s[:,:,0]-s[:,:,1])>40)&((s[:,:,0]-s[:,:,2])>10)
def isgreen(s): return (s[:,:,1]>s[:,:,0]+20)&(s[:,:,1]>s[:,:,2]+20)&(s[:,:,1]>60)&(s[:,:,1]<240)

# plot frame red border (original: red frame x572..810 y65..311)
r = ink_bbox(ren, isred, bbox_render(560,55,825,320)[0], bbox_render(560,55,825,320)[1],
             bbox_render(560,55,825,320)[2], bbox_render(560,55,825,320)[3], True)
print(f"\nRENDER plot red-border bbox (frame px): {tuple(round(v,1) for v in r)}")
o = ink_bbox(orig, isred, 560, 55, 825, 320, False)
print(f"ORIG   plot red-border bbox (frame px): {o}")

# green dot + green box
r = ink_bbox(ren, isgreen, bbox_render(340,230,560,285)[0], bbox_render(340,230,560,285)[1],
             bbox_render(340,230,560,285)[2], bbox_render(340,230,560,285)[3], True)
print(f"RENDER green-box ink bbox (frame px): {tuple(round(v,1) for v in r) if r else None}")
o = ink_bbox(orig, isgreen, 340, 230, 560, 285, False)
print(f"ORIG   green-box ink bbox (frame px): {o}")

# parabola blue in render vs orig
def isblue(s): return (s[:,:,2]>s[:,:,0]+25)&(s[:,:,2]>90)
r = ink_bbox(ren, isblue, bbox_render(570,60,815,312)[0], bbox_render(570,60,815,312)[1],
             bbox_render(570,60,815,312)[2], bbox_render(570,60,815,312)[3], True)
print(f"RENDER blue ink bbox (frame px): {tuple(round(v,1) for v in r) if r else None}")
o = ink_bbox(orig, isblue, 570, 60, 815, 312, False)
print(f"ORIG   blue ink bbox (frame px): {o}")

# ----- parabola ripple check on the RENDER: trace blue ink center per row, fit f=(x-5)^2+1 -----
print("\n== parabola ripple check (render) ==")
x0,x1 = bbox_render(570,60,815,312)[0], bbox_render(570,60,815,312)[2]
y0,y1 = bbox_render(570,60,815,312)[1], bbox_render(570,60,815,312)[3]
sub = ren[y0:y1, x0:x1]
blue = (sub[:,:,2]>sub[:,:,0]+25)&(sub[:,:,2]>90)
X0r, Y0r, UXr, UYr = 630.5*SX, 266.5*SY, 11.45*SX, 12.0*SY
pts = []
for i in range(blue.shape[0]):
    xs = np.nonzero(blue[i])[0]
    if len(xs):
        cx = (xs.min()+xs.max())/2 + x0
        pts.append((i+y0, cx))
# expected: cx = X0r + 5*UXr (vertex) for all rows -> the curve is symmetric about x=5
if pts:
    dev = [abs(cx - (X0r + 5*UXr)) for _, cx in pts]
    print(f"   blue rows={len(pts)}; max |cx-(vertex)| in frame px = {max(dev)/SX:.2f}")
    # second-difference ripple along the traced curve
    cxs = np.array([cx for _, cx in pts])
    d2 = np.diff(cxs, 2)
    print(f"   second-diff of x-center: mean={d2.mean():.3f} max|d2|={np.abs(d2).max():.3f} render px")
    # expected monotone widening away from vertex except near clip
    ys_arr = np.array([y for y, _ in pts])
    yy = (Y0r - ys_arr)/UYr  # data y
    exp_halfw = np.sqrt(np.maximum(yy-1, 0))
    # measured half width in data x
    halfw = []
    for i in range(blue.shape[0]):
        xs = np.nonzero(blue[i])[0]
        if len(xs): halfw.append(((xs.max()-xs.min())/2)/UXr)
        else: halfw.append(np.nan)
    err = [abs(h-e) for h, e in zip(halfw, exp_halfw) if not np.isnan(h)]
    print(f"   parabola half-width vs expected sqrt(y-1): max err = {max(err):.3f} data-units over {len(err)} rows")

# ----- frame containment: no ink beyond inner frames -----
print("\n== frame containment ==")
# param table navy frame x103..237 y199..281: content ink must be inside
def darkish(s): return (s[:,:,0]<170)&(s[:,:,1]<170)&(s[:,:,2]<170)
for name, (fx0,fy0,fx1,fy1) in {
  'param-table': (104,200,236,280),
  'iter-table-frame': (79,326,653,529),
  'plot-frame': (573,66,809,310),
  'eq-box-A': (400,186,529,211),
  'green-box': (349,235,553,280),
  'callout': (336,293,568,319),
}.items():
    x0,y0,x1,y1 = bbox_render(fx0,fy0,fx1,fy1)
    sub = ren[y0:y1, x0:x1]
    m = darkish(sub)|isred(sub)|isgreen(sub)|isblue(sub)
    ys, xs = np.nonzero(m)
    if len(xs):
        print(f"   {name:16s} ink frame px x{(x0+xs.min())/SX:.1f}..{(x0+xs.max())/SX:.1f} y{(y0+ys.min())/SY:.1f}..{(y0+ys.max())/SY:.1f}  (box {fx0}..{fx1} {fy0}..{fy1})")
    else:
        print(f"   {name:16s} NO INK")
