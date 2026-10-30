#!/usr/bin/env python3
"""Pre-judge self-check for slide 015 (attempt 1).
PIL-only verification of measured frame geometry against the 150dpi render.
Scale: render_px / frame_px = 1125/540 = 2.0833 (1px = 1pt in both).
"""
import numpy as np
from PIL import Image

RENDER = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/render_1.png"
ORIG   = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg"

def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)

def ink_mask(a):
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    lum = a.sum(axis=2)/3
    red = (r>90)&((r-g)>40)&((r-b)>10)     # house strokes + red title/border
    return (lum<130)&(~red)

def band(a, y0, y1, x0, x1, label):
    sc = a.shape[0]/540.0
    m = ink_mask(a)[int(y0*sc):int((y1+1)*sc), int(x0*sc):int((x1+1)*sc)]
    if not m.any():
        print(f"  {label:20s} EMPTY  <-- DEFECT")
        return None
    ys,xs = np.where(m)
    return (ys.min()/sc+y0, ys.max()/sc+y0, xs.min()/sc+x0, xs.max()/sc+x0)

# measured frame targets (from measure_015*.py on the original)
TARGETS = [
    ("TITLE",        (68, 84,  124, 901),  (60, 95, 74, 902)),
    ("EQ1",          (110,152,  97,  901),  (105,160, 74, 902)),
    ("REDBOX_TEXT",  (285,325,  80,  700),  (276,333, 80, 700)),
    ("PEACH_TEXT",   (279,329,  790, 896),  (276,333, 790, 896)),
    ("DERIVATIVES",  (356,400,  79,  901),  (342,412, 74, 902)),
    ("NORMALEQ",     (420,450,   79,  900),  (412,470, 74, 902)),
    ("GREENBOX",     (478,508,  316,  884),  (474,516, 316, 884)),
]
# separate colored boxes (must be present as fills/borders, not text ink)
COLOR = [
    ("red box border",   "red",  (276,333, 80, 700)),
    ("peach fill",       "peach",(276,333, 788,896)),
    ("green box border", "green",(473,516, 314,884)),
    ("yellow badge",     "yellow",(56, 92, 856,895)),
]

rend = load(RENDER)
print(f"render {rend.shape[1]}x{rend.shape[0]}")
fails = []

print("TEXT REGIONS (render vs frame-measured target):")
for name,(y0,y1,tx0,tx1),(wy0,wy1,wx0,wx1) in TARGETS:
    got = band(rend, wy0, wy1, wx0, wx1, name)
    if got is None:
        fails.append(f"{name}: no ink"); continue
    gy0,gy1,gx0,gx1 = got
    # vertical band must overlap the target window
    ok_y = (gy1 >= y0) and (gy0 <= y1)
    ok_x = (gx1 >= tx0-30) and (gx0 <= tx1+30)
    print(f"  {name:16s} render y{gy0:.0f}-{gy1:.0f} x{gx0:.0f}-{gx1:.0f}"
          f"   target y{y0}-{y1} x{tx0}-{tx1}   y:{'OK' if ok_y else 'FAIL'} x:{'OK' if ok_x else 'FAIL'}")
    if not (ok_y and ok_x):
        fails.append(f"{name}: y{'OK' if ok_y else 'FAIL'} x{'OK' if ok_x else 'FAIL'}")

print("COLORED ELEMENTS:")
sc = rend.shape[0]/540.0
r,g,b = rend[:,:,0],rend[:,:,1],rend[:,:,2]
for name,kind,(y0,y1,x0,x1) in COLOR:
    sub = rend[int(y0*sc):int((y1+1)*sc), int(x0*sc):int((x1+1)*sc)]
    rr,gg,bb = sub[:,:,0],sub[:,:,1],sub[:,:,2]
    if kind=="red":
        m = (rr>120)&((rr-gg)>40)&((rr-bb)>10)
    elif kind=="peach":
        m = (rr>235)&(gg>195)&(gg<240)&(bb>180)&(bb<235)
    elif kind=="green":
        m = (gg>120)&(gg<220)&(rr<100)&(bb<150)
    elif kind=="yellow":
        m = (rr>200)&(gg>200)&(bb<190)   # FDFD96: (253,253,150)
    n = m.sum()
    print(f"  {name:16s} {n:6d} px   {'OK' if n>300 else 'FAIL (<300px)'}")
    if n <= 300:
        fails.append(f"{name}: only {n} px")

print()
if fails:
    print("SELF-CHECK: FAIL")
    for f in fails: print("  -", f)
    raise SystemExit(1)
print("SELF-CHECK: PASS (all regions present, all boxes/fills present, no empty region)")
