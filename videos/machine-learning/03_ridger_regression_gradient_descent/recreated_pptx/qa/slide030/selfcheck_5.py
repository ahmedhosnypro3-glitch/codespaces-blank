"""Self-check 5 — slide 030: title ink extent, iter-table navy frame, x-row red
cells, secant+dots+3-labels. Render vs original."""
import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540
def bbox(fx0,fy0,fx1,fy1): return int(round(fx0*SX)), int(round(fy0*SY)), int(round(fx1*SX)), int(round(fy1*SY))

def inkbbox(img, box, sx, sy, mask=None):
    x0,y0,x1,y1 = box
    sub = img[y0:y1, x0:x1]
    if mask is None:
        m = (sub.sum(axis=2) < 640)
    else:
        m = mask(sub)
    ys, xs = np.nonzero(m)
    if not len(xs): return None
    return ((x0+xs.min())/sx, (y0+ys.min())/sy, (x0+xs.max())/sx, (y0+ys.max())/sy, int(m.sum()))

print("== 1. TITLE ink extent (frame px) ==")
print("   render:", tuple(round(v,1) for v in inkbbox(ren, bbox(40,50,600,100), SX, SY)))
print("   orig  :", inkbbox(orig, (40,50,600,100), 1, 1))

print("== 2. ITER TABLE navy outer frame (build x78..654 y325..530, 2pt) ==")
def isnavy(s): return (s[:,:,2]>s[:,:,0]+30)&(s[:,:,2]>90)&(s[:,:,0]<120)
print("   render:", tuple(round(v,1) for v in inkbbox(ren, bbox(40,300,700,545), SX, SY, isnavy)))
print("   orig  :", inkbbox(orig, (40,300,700,545), 1, 1, isnavy))

print("== 3. X-ROW red cells '3' and '5' (build: x-row cols 1 and 11 red text) ==")
def isred(s): return (s[:,:,0]>90)&((s[:,:,0]-s[:,:,1])>40)&((s[:,:,0]-s[:,:,2])>10)
for nm, img, sc in (("render", ren, (SX,SY)), ("orig", orig, (1,1))):
    x0,y0,x1,y1 = (bbox(150,334,175,356) if nm=="render" else (150,334,175,356))
    # col of first value '3' ~ x150..194; red-count there
    if nm == "render":
        b1 = bbox(148,334,196,356); b2 = bbox(588,334,636,356)
    else:
        b1 = (148,334,196,356); b2 = (588,334,636,356)
    n1 = int(isred(img[b1[1]:b1[3], b1[0]:b1[2]]).sum())
    n2 = int(isred(img[b2[1]:b2[3], b2[0]:b2[2]]).sum())
    print(f"   {nm}: red px in first-cell(3)={n1} last-cell(5)={n2}")

print("== 4. SECANT line + 3 dots + gray '3' labels (frame px) ==")
def dark(s): return (s.sum(axis=2) < 450)
for nm, img, sc in (("render", ren, (SX,SY)), ("orig", orig, (1,1))):
    if nm == "render":
        b = bbox(645,143,728,150)
    else:
        b = (645,143,728,150)
    r = inkbbox(img, b, sc[0], sc[1], dark)
    print(f"   {nm} secant y143..150 band ink bbox: " + (tuple(round(v,1) for v in r[:4]) + (r[4],)) if r else "none")
# dots tighter: y144..149 x-runs
for nm, img, sc in (("render", ren, (SX,SY)), ("orig", orig, (1,1))):
    if nm == "render":
        x0,y0,x1,y1 = bbox(645,144,728,149)
    else:
        x0,y0,x1,y1 = 645,144,728,149
    sub = img[y0:y1, x0:x1]
    m = (sub.sum(axis=2) < 450)
    colsum = m.sum(axis=0)
    runs = []; s=None
    for i,c in enumerate(colsum):
        if c>=4 and s is None: s=i
        if c<4 and s is not None: runs.append((s,i-1)); s=None
    if s is not None: runs.append((s,len(colsum)-1))
    print(f"   {nm} dot x-runs (frame): " + str([(round((x0+a)/sc[0],1), round((x0+b)/sc[0],1)) for a,b in runs]))
# gray 3-labels
def grayish(s): return (np.abs(s[:,:,0]-s[:,:,1])<25)&(np.abs(s[:,:,1]-s[:,:,2])<25)&(s.sum(axis=2)>280)&(s.sum(axis=2)<640)
for nm, img, sc in (("render", ren, (SX,SY)), ("orig", orig, (1,1))):
    if nm == "render":
        x0,y0,x1,y1 = bbox(660,128,715,145)
    else:
        x0,y0,x1,y1 = 660,128,715,145
    sub = img[y0:y1, x0:x1]
    m = grayish(sub)
    ys, xs = np.nonzero(m)
    if len(xs):
        print(f"   {nm} '3'-label ink: frame x{(x0+xs.min())/sc[0]:.0f}..{(x0+xs.max())/sc[0]:.0f} y{(y0+ys.min())/sc[1]:.0f}..{(y0+ys.max())/sc[1]:.0f} n={int(m.sum())}")
    else:
        print(f"   {nm} '3'-label ink: none")

print("== 5. red dashed vline at x=5 (draw x687..689; check both) ==")
def pinkish(s): return (s[:,:,0]>s[:,:,2]+20)&(s[:,:,0]>140)&(s[:,:,0]-s[:,:,1]>25)
for nm, img, sc in (("render", ren, (SX,SY)), ("orig", orig, (1,1))):
    if nm == "render":
        x0,y0,x1,y1 = bbox(680,80,695,260)
    else:
        x0,y0,x1,y1 = 680,80,695,260
    sub = img[y0:y1, x0:x1]
    m = pinkish(sub)
    cols = np.nonzero(m.sum(axis=0) > 3)[0]
    if len(cols):
        print(f"   {nm}: vline-like cols frame x{(x0+cols.min())/sc[0]:.0f}..{(x0+cols.max())/sc[0]:.0f} n={int(m.sum())}")
