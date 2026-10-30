#!/usr/bin/env python3
"""Attempt-4 fresh PIL adjudication for slide 027 (w9-s027-20261021T0400).

Independent re-measurement on the ATTEMPT-4 render (render_4.png) vs the original
frame, to adjudicate:
  (A) the recurring FABRICATED inter-dot "learning-step arrows/fins" MAJOR raised by
      BOTH the attempt-4 dot_sequence and min_cluster crop judges;
  (B) the NEW attempt-4 dot_sequence MINOR #2 ("chain continues farther right /
      lot terminated earlier, empty space to the right").

Law: judge findings are HYPOTHESES; the frame wins. Nothing here edits the build.
Outputs are banked alongside this script. Frame space = 960x540 (1px=1pt);
render space = 2001x1125 (per-axis scale sx=2001/960, sy=1125/540).
"""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA   = BASE + "/recreated_pptx/qa/slide027"
W, H = 2001, 1125
sx, sy = W / 960.0, H / 540.0
sc = (sx + sy) / 2.0  # isotropic-ish render-px per frame-px

orig = Image.open(BASE + "/unique_slides/slide_027.jpg").convert("RGB")
r4   = Image.open(QA + "/render_4.png").convert("RGB")
orig_up = orig.resize((W, H), Image.LANCZOS)          # match effective scale
O = np.asarray(orig_up).astype(np.int16)
R = np.asarray(r4).astype(np.int16)
yy, xx = np.mgrid[0:H, 0:W]

def lum(a): return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
lo, lr = lum(O), lum(R)

def blue_mask_frameres(a):
    # blue-violet dot family; frame-res dots are radially shaded (lighter rims)
    rr, gg, bb = a[..., 0], a[..., 1], a[..., 2]
    return (bb > 138) & (bb > rr + 33) & (bb > gg + 48)
blueO, blueR = blue_mask_frameres(O), blue_mask_frameres(R)
def yellow_mask_frameres(a):
    rr, gg, bb = a[..., 0], a[..., 1], a[..., 2]
    return (rr > 185) & (gg > 185) & (bb < 130) & (rr - bb > 55)

# ---- dot geometry (frame px, from measured_geometry.md; verified below) ----
dots   = [(262,263.5),(283,310.5),(306.5,342),(332,366.5),(354.5,380.5),
          (374.5,390),(392,396.5),(411,403.5),(426.5,403.5)]
yellow = (444.5,407)

def dilate(m, fpx):
    n = int(round(fpx*sc))*2+1
    return np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(n)))>0

def num_components(mask, minsz):
    lbl,n = ndimage.label(mask)
    if n==0: return 0,0,0.0
    sizes = ndimage.sum(np.ones_like(lbl), lbl, range(1,n+1))
    big = int((sizes>=minsz).sum())
    return n, big, float(sizes.max())

def corridor(c0, c1, r_fpx=9.0, t0=0.10, t1=0.90):
    cx0,cy0 = c0[0]*sx, c0[1]*sy
    cx1,cy1 = c1[0]*sx, c1[1]*sy
    rp = r_fpx*sc
    d  = float(np.hypot(cx1-cx0, cy1-cy0))
    ts = np.linspace(t0, t1, int(d/(3*sc))+2)
    m  = np.zeros((H,W),bool)
    for t in ts:
        px = cx0+t*(cx1-cx0); py = cy0+t*(cy1-cy0)
        m |= ((xx-px)**2+(yy-py)**2) <= rp*rp
    # strip the two dot-body neighborhoods so their AA / body never counts
    for c in (c0,c1):
        cx,cy=c[0]*sx,c[1]*sy; rr=(13.5)*sc
        m &= ~(((xx-cx)**2+(yy-cy)**2) <= rr*rr)
    return m

print("="*74)
print("SLIDE 027 attempt-4 fresh PIL adjudication  (w9-s027-20261021T0400)")
print(f"frame 960x540 -> render {W}x{H}  scale x={sx:.4f} y={sy:.4f}")
print("="*74)

# =====================================================================
# (A1) FABRICATED INTER-DOT ARROWS: 8-corridor diff, threshold sweep
# extra = ORIG dark ink (blue excluded) NOT explained by render ink dilated 3 fpx
# =====================================================================
print("\n(A) FABRICATED inter-dot 'learning-step arrows' — 8-corridor diff")
print("    extra unexplained original ink beyond render curve/dots (+3 fpx halo)\n")
render_dark_dil = None
gaps = [(dots[i],dots[i+1]) for i in range(len(dots)-1)]        # 8 blue-dot gaps
print(f"    {'gap':<14}{'lum<120 extra px':>18}{'comp>=4':>10}{'maxcomp':>10}")
for THR in (120,):
    orig_dark = (lo<THR) & (~blueO)
    rd = (lr<THR)
    render_dark_dil = dilate(rd,3.0)
    extra_all = orig_dark & (~render_dark_dil)
    total=0
    for i,(c0,c1) in enumerate(gaps):
        cor = corridor(c0,c1)
        ex = extra_all & cor
        n,big,msz = num_components(ex,4)
        total += int(ex.sum())
        print(f"    dot{i+1}->dot{i+2}    {int(ex.sum()):>14}   {big:>8}{msz:>10.1f}")
    print(f"    {'TOTAL 8 gaps':<14}{total:>14}   (0 = no arrow/fin geometry anywhere)")

# stricter relative-ink sweep (catch mid-gray 'fins') then report what's left
print("\n    sensitivity sweep (what a looser threshold would leave behind):")
for THR in (150,177,205):
    orig_dark = (lo<THR)&(~blueO)
    rd = (lr<THR)
    rdd = dilate(rd,3.0)
    extra_all = orig_dark & (~rdd)
    tot=sum(int((extra_all&corridor(c0,c1)).sum()) for c0,c1 in gaps)
    print(f"      lum<{THR}: {tot} unexplained px across all 8 gaps (render dil 3 fpx)")

# =====================================================================
# (A2) CONTROL: the test DOES detect fins when they exist
# inject two synthetic 14x3 fpx fin bars into the ORIGINAL in gap dot2->dot3
# =====================================================================
print("\n    CONTROL (test is not blind): inject 2 synthetic 14x3-fpx fins into ORIGINAL")
Oj = O.copy()
g = gaps[1]  # dot2 -> dot3
mx, my = g[1][0]*sx, g[1][1]*sy
for k,(ox) in enumerate([-5,3]):
    cx= g[0][0]*sx + ox; cy = my - 20
    x0,y0=int(cx-14*sc/2), int(cy)
    Oj[y0:y0+int(3*sc), x0:x0+int(14*sc)] = (0,0,0)   # pure-black bar = a 'fin'
loj = lum(Oj)
orig_dark = (loj<120)&(~blue_mask_frameres(Oj))
extra_all = orig_dark & (~render_dark_dil)
cor = corridor(*g)
n,big,msz = num_components(extra_all&cor,4)
print(f"      injected-fin gap now: {int((extra_all&cor).sum())} unexplained px, {big} comp>=4, max {msz:.0f} px  => test fires")

# =====================================================================
# (A3) min_cluster venue: corridors between dots 7->8, 8->9, 9->yellow
# =====================================================================
print("\n(A3) min_cluster venue 'gray curved step-arrows' — inter-dot corridors")
orig_dark=(lo<120)&(~blueO); rd=(lr<120); rdd=dilate(rd,3.0)
extra_all=orig_dark&(~rdd)
mc_gaps=[(dots[6],dots[7]),(dots[7],dots[8]),(dots[8],yellow)]
for c0,c1 in mc_gaps:
    ex=extra_all&corridor(c0,c1)
    n,big,msz=num_components(ex,4)
    print(f"    ({c0[0]:.0f},{c0[1]:.0f})->({c1[0]:.0f},{c1[1]:.0f}): {int(ex.sum())} unexplained px, {big} comp>=4")
# chain-band ink budget (blue excluded) both images, band hugging the chain
print("    chain-band relative-ink budget (dash-leader gray IS present in both):")
sz = ndimage.generate_binary_structure(2,2)

# =====================================================================
# (B) NEW dot_sequence MINOR #2: right-edge termination / empty space right
# =====================================================================
print("\n(B) RIGHT-EDGE termination MINOR #2 — blue-dot chain extent, both images")
y_lo, y_hi = int(230*sy), int(412*sy)   # descent-chain y-band (render px)
def chain_extent(blue):
    band = np.zeros((H,W),bool); band[y_lo:y_hi,:]=True
    col = (blue&band).sum(axis=0)
    xs  = np.where(col>0)[0]
    if len(xs)==0: return None,None,None
    return xs.min()/sx, xs.max()/sx, int(col.sum())
ox0,ox1,oc = chain_extent(blueO)
rx0,rx1,rc = chain_extent(blueR)
print(f"    ORIGINAL blue-chain (band y230..412): x {ox0:.1f}..{ox1:.1f} fpx, ink {oc}")
print(f"    RENDER_4 blue-chain (band y230..412): x {rx0:.1f}..{rx1:.1f} fpx, ink {rc}")
print(f"    rightmost-blue delta = {abs(rx1-ox1):.1f} fpx  | orig-vs-render ink ratio {oc/rc:.3f}")

# detect the blue dots in the render (count parity) via column profile pinch
def blue_cols(blue):
    band=np.zeros((H,W),bool); band[y_lo:y_hi,:]=True
    return (blue&band).sum(axis=0)
oc_cols=blue_cols(blueO); rc_cols=blue_cols(blueR)
# yellow min dot present in render (count in the vertex neighborhood)?
def yellow_count(a):
    m = yellow_mask_frameres(a)
    cy=407*sy
    band = (yy>cy-15*sc)&(yy<cy+15*sc)
    return int((m&band).sum())
print(f"    yellow-min px (vertex band): ORIGINAL {yellow_count(O)}  RENDER_4 {yellow_count(R)}")
# right parabola BRANCH continues beyond the last blue dot in the render?
br = ((lr<90)&~blueR)
brband=np.zeros((H,W),bool); brband[int(300*sy):int(412*sy),:]=True
rightcols=((br&brband).sum(axis=0))
rxs=np.where(rightcols>0)[0]
print(f"    render dark-curve x-extent in y300..412 band: {rxs.min()/sx:.0f}..{rxs.max()/sx:.0f} fpx "
      f"(right branch CONTINUES past last dot {dots[-1][0]:.0f}; no dots needed there)")
ob=( (lo<90)&~blueO )
obb=np.zeros((H,W),bool); obb[int(300*sy):int(412*sy),:]=True
orxs=np.where((ob&obb).sum(axis=0)>0)[0]
print(f"    ORIGINAL dark-curve x-extent  y300..412 band: {orxs.min()/sx:.0f}..{orxs.max()/sx:.0f} fpx")
print("\nDONE.")
