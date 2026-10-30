"""att9 let-boxes crop FAIL adjudication: delimiter SHAPE (bars vs parens).
Measures per-row ink centroid of each delimiter column band in
(a) the ORIGINAL frame unique_slides/slide_004.jpg (1px=1pt) and
(b) the att9 render render_9.png (150dpi, sx=2001/960).
Paren '(' bows LEFT (toward the entries' left) at mid-span; ')' bows RIGHT."""
import numpy as np
from PIL import Image

o = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
                          "03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg").convert("RGB"), int)
r = np.asarray(Image.open("render_9.png").convert("RGB"), int)
SX, SY = 2001/960.0, 1125/540.0

def profile(img, x0, x1, y0, y1, sx=1.0, sy=1.0, thr=690):
    prof = {}
    for y in range(y0, y1):
        row = img[int(y*sy):int(y*sy)+1, int(x0*sx):int(x1*sx), :].reshape(-1, 3)
        ink = np.where(row.sum(axis=1) < thr)[0]
        if len(ink):
            prof[y] = x0 + ink.mean()/sx
    return prof

def bow(prof, name):
    ys = sorted(prof)
    if len(ys) < 30:
        print(f"{name}: too few rows ({len(ys)})"); return
    ymid = (ys[0]+ys[-1])/2
    mid = [prof[y] for y in ys if abs(y-ymid) < (ys[-1]-ys[0])*0.08]
    q = (ys[-1]-ys[0])*0.12
    ends = [prof[y] for y in ys if y < ys[0]+q or y > ys[-1]-q]
    b = (sum(ends)/len(ends)) - (sum(mid)/len(mid))
    shape = "'(' paren (bows left)" if b > 0.5 else ("')' paren (bows right)" if b < -0.5 else "STRAIGHT bar")
    print(f"{name}: rows y{ys[0]}..{ys[-1]}  mid-x {sum(mid)/len(mid):.2f}  ends-x {sum(ends)/len(ends):.2f}  bow {b:+.2f}px  -> {shape}")

print("== ORIGINAL (frame px) ==")
bow(profile(o, 152, 164, 104, 209), "L-box left delim  (orig)")
bow(profile(o, 181, 191, 104, 209), "L-box right delim (orig)")
bow(profile(o, 498, 510, 104, 212), "R-box left delim  (orig)")
bow(profile(o, 524, 537, 104, 212), "R-box right delim (orig)")
print("== RENDER_9 (150dpi px, reported in frame-px units) ==")
bow(profile(r, 152, 164, 104, 209, SX, SY), "L-box left delim  (rend)")
bow(profile(r, 181, 191, 104, 209, SX, SY), "L-box right delim (rend)")
bow(profile(r, 498, 510, 104, 212, SX, SY), "R-box left delim  (rend)")
bow(profile(r, 524, 537, 104, 212, SX, SY), "R-box right delim (rend)")
print("== ASCII map: orig L-box left delim (x152..164, step 6 rows) ==")
for y in range(104, 210, 6):
    row = "".join("#" if o[y, x].sum() < 690 else "." for x in range(152, 165))
    print(f"{y:3d} {row}")
print("== ASCII map: render_9 L-box left delim (frame x152..164, step 6 rows) ==")
for y in range(104, 210, 6):
    yy = int(y*SY)
    row = "".join("#" if r[yy, int(x*SX)].sum() < 690 else "." for x in range(152, 165))
    print(f"{y:3d} {row}")
