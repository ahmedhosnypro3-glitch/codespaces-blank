import numpy as np
from PIL import Image
ORIG = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_005.jpg"
REND = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/render_7.png"
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
SX, SY = 2001/960.0, 1125/540.0

def ink(arr, x0, x1, y0, y1, thr=200, sx=1.0, sy=1.0):
    X0,X1,Y0,Y1 = int(x0*sx), int(x1*sx), int(y0*sy), int(y1*sy)
    sub = arr[Y0:Y1+1, X0:X1+1].mean(axis=2) < thr
    if not sub.any(): return None
    ys, xs = np.nonzero(sub)
    return (X0+xs.min())/sx, (Y0+ys.min())/sy, (X0+xs.max())/sx, (Y0+ys.max())/sy

# (name, x0, x1, y0, y1) — windows chosen to EXCLUDE box border strokes
REG = [
 ("title",      162, 810,  66,  92),
 ("rememberU",  679, 758, 136, 152),
 ("bodyX1",     679, 875, 156, 174),
 ("bodyX2",     679, 790, 176, 194),
 ("rem1eq",     682, 860, 212, 236),
 ("rememberL",  659, 730, 374, 392),
 ("rem2eq",     662, 862, 394, 421),
 ("pinkfrac",    77, 168, 292, 340),
 ("getbest",    190, 502, 300, 330),
 ("eq1",         96, 548, 107, 152),
 ("eq2",         95, 632, 171, 216),
 ("eq3",         96, 526, 228, 273),
 ("eq4",         95, 596, 373, 419),
 ("eq5",         94, 640, 458, 504),
 ("green",      692, 876, 463, 499),
]
print(f"{'region':11s} {'origCx':>7}{'rendCx':>8}{'dCx':>7} | {'origCy':>7}{'rendCy':>8}{'dCy':>8} | {'origH':>6}{'rendH':>7}{'dH':>7} | {'origW':>6}{'rendW':>7}")
print("-"*112)
rows = []
for name, x0,x1,y0,y1 in REG:
    ob = ink(o, x0,x1,y0,y1); rb = ink(r, x0,x1,y0,y1, sx=SX, sy=SY)
    if ob is None or rb is None:
        print(f"{name:11s} MISSING orig={ob is not None} rend={rb is not None}"); continue
    ocx, ocy = (ob[0]+ob[2])/2, (ob[1]+ob[3])/2
    rcx, rcy = (rb[0]+rb[2])/2, (rb[1]+rb[3])/2
    oh, ow = ob[3]-ob[1]+1, ob[2]-ob[0]+1
    rh, rw = rb[3]-rb[1]+1, rb[2]-rb[0]+1
    rows.append((name, ocx, rcx, ocy, rcy, oh, rh))
    print(f"{name:11s} {ocx:7.1f}{rcx:8.1f}{rcx-ocx:+7.2f} | {ocy:7.1f}{rcy:8.1f}{rcy-ocy:+8.2f} | {oh:6.1f}{rh:7.1f}{rh-oh:+7.1f} | {ow:6.1f}{rw:7.1f}")
print()
print("=== elements with |dCy| > 1.5 frame px (vertical misalignment worth fixing) ===")
for n,ocx,rcx,ocy,rcy,oh,rh in rows:
    if abs(rcy-ocy) > 1.5:
        print(f"  {n:11s} render ink centre is {rcy-ocy:+.2f} frame px vs original  (orig {ocy:.1f} rend {rcy:.1f})")
print("=== elements with |dCx| > 1.5 frame px ===")
for n,ocx,rcx,ocy,rcy,oh,rh in rows:
    if abs(rcx-ocx) > 1.5:
        print(f"  {n:11s} dx {rcx-ocx:+.2f}")
