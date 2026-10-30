#!/usr/bin/env python3
"""PIL adjudication of slide 049 judge_attempt_11 (render_10) vs original frame.
Measures the 2 MAJORs + key MINORs at pixel level. Frame coords: orig 960x540;
render_10 2001px wide -> scale 2001/960 = 2.084375."""
from PIL import Image
import numpy as np

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_049.jpg"
REND = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide049/render_10.png"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide049/pil_adjud_049a11_raw.txt"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r_im = Image.open(REND).convert("RGB")
rw, rh = r_im.size
s = rw / 960.0
r = np.asarray(r_im).astype(int)

def zone(img, x0, x1, y0, y1):
    return img[int(y0):int(y1), int(x0):int(x1)]

def lum(z):
    return 0.299*z[:,:,0] + 0.587*z[:,:,1] + 0.114*z[:,:,2]

def census(z):
    l = lum(z); ink = l < 200
    red = (z[:,:,0] > 140) & (z[:,:,0] - z[:,:,1] > 60) & (z[:,:,0] - z[:,:,2] > 60)
    blue = (z[:,:,2] > 120) & (z[:,:,2] - z[:,:,0] > 40) & (z[:,:,2] - z[:,:,1] > 20)
    green = (z[:,:,1] > 110) & (z[:,:,1] - z[:,:,0] > 25) & (z[:,:,1] - z[:,:,2] > 25)
    return ink, red, blue, green

lines = []
def P(*a):
    t = " ".join(str(x) for x in a)
    lines.append(t); print(t)

P("== render_10 size", rw, rh, "scale", round(s, 5))

# ---------- A) Initial W zone: frame x320..465 y50..115 ----------
P("\n## A) Initial-W zone (frame x320..465 y50..115)")
for name, img, sc in (("ORIG", o, 1.0), ("RENDER", r, s)):
    z = zone(img, 320*sc, 465*sc, 50*sc, 115*sc)
    ink, red, blue, green = census(z)
    P(f" {name}: ink={ink.sum()} red={red.sum()} blue={blue.sum()} green={green.sum()}")
    l = lum(z)
    # column profile of ink to find strokes/digits (1px = 1 frame px after /sc)
    prof = ink.sum(axis=0)
    cols = "".join("#" if c > (1.2*sc) else ("+" if c > 0 else ".") for c in prof)
    P(f" {name} colprofile x320..465:", cols)
    # ascii map, 1 char per frame px (downsample render by s)
    rows = []
    for yy in range(0, int(65*sc), int(sc)):
        band = zone(img, 320*sc, 465*sc, (50 + yy/sc)*sc, (50 + yy/sc + 1)*sc)
        inkb, _, _, _ = census(band)
        pr = inkb.sum(axis=0)
        rows.append("".join("#" if v > (0.4*sc) else "." for v in pr))
    P(f" {name} ascii (y50..115, x320..465):")
    for i, rr in enumerate(rows):
        P(f"   y{50+i:03d} {rr}")

# ---------- B) delimiter form: stroke straightness + tips ----------
P("\n## B) delimiter strokes: Initial-W pair + row-1 W column + aug col-1")
def stroke_scan(name, img, sc, x0, x1, y0, y1):
    z = zone(img, x0*sc, x1*sc, y0*sc, y1*sc)
    ink, _, _, _ = census(z)
    prof = ink.sum(axis=0)
    P(f" {name} x{x0}..{x1} y{y0}..{y1} colprofile:")
    P("   ", "".join("#" if c > (0.5*(y1-y0)*sc) else ("+" if c > (0.15*(y1-y0)*sc) else ("." if c > 0 else " ")) for c in prof))
    # vertical runs per ink column: straightness = long continuous run
    for ci, c in enumerate(prof):
        if c > (0.6*(y1-y0)*sc):
            colpx = ink[:, ci]
            # longest run
            best = cur = 0
            for v in colpx:
                cur = cur + 1 if v else 0
                best = max(best, cur)
            P(f"    col x{x0+ci/sc:.1f} h={c/sc:.0f} longest_run={best/sc:.0f} ({'STRAIGHT' if best > 0.7*c else 'BROKEN/curved'})")

stroke_scan("ORIG initialW-L", o, 1.0, 325, 340, 55, 110)
stroke_scan("REND initialW-L", r, s, 325, 340, 55, 110)
stroke_scan("ORIG initialW-R", o, 1.0, 345, 360, 55, 110)
stroke_scan("REND initialW-R", r, s, 345, 360, 55, 110)
stroke_scan("ORIG row1-Wcol", o, 1.0, 690, 755, 145, 195)
stroke_scan("REND row1-Wcol", r, s, 690, 755, 145, 195)
stroke_scan("ORIG aug-col1", o, 1.0, 88, 112, 175, 230)
stroke_scan("REND aug-col1", r, s, 88, 112, 175, 230)

# ---------- C) Z-grid delimiters (top band right) ----------
P("\n## C) Z-grid zone (frame x628..715 y58..130)")
for name, img, sc in (("ORIG", o, 1.0), ("RENDER", r, s)):
    z = zone(img, 628*sc, 715*sc, 58*sc, 130*sc)
    ink, _, _, _ = census(z)
    prof = ink.sum(axis=0)
    P(f" {name} colprofile:", "".join("#" if c > (0.5*72*sc) else ("+" if c > (0.15*72*sc) else ("." if c > 0 else " ")) for c in prof))

# ---------- D) colors ----------
P("\n## D) MINOR checks")
# D1 row-1 d-row digits color (orig x333..375 y147..160)
for name, img, sc in (("ORIG", o, 1.0), ("RENDER", r, s)):
    z = zone(img, 333*sc, 380*sc, 145*sc, 162*sc)
    ink, red, blue, green = census(z)
    P(f" D1 {name} row1 digits x333..380 y145..162: ink={ink.sum()} red={red.sum()} blue={blue.sum()} green={green.sum()}")
# D2 arrow color zone (row1 => x495..512 y158..175)
for name, img, sc in (("ORIG", o, 1.0), ("RENDER", r, s)):
    z = zone(img, 493*sc, 514*sc, 156*sc, 178*sc)
    ink, red, blue, green = census(z)
    l = lum(z)
    dark = ink & ~red & ~blue & ~green
    P(f" D2 {name} arrow zone x493..514 y156..178: ink={ink.sum()} red={red.sum()} blue={blue.sum()} green={green.sum()} darknoncolor={dark.sum()}")
# D3 header-box interior fill sample
for name, img, sc, pts in (("ORIG", o, 1.0, [(300, 90), (550, 90), (700, 90)]), ("RENDER", r, s, [(300, 90), (550, 90), (700, 90)])):
    samples = [tuple(img[int(y*sc), int(x*sc)]) for x, y in pts]
    P(f" D3 {name} top-box interior samples {pts}: {samples}")
# D4 row6 bottom containment (render vs bottom stroke y538.5)
z = zone(r, 260*s, 860*s, 505*s, 540*s)
ink, _, _, _ = census(z)
rowsink = ink.sum(axis=1)
P(" D4 RENDER rows y505..540 ink profile (x260..860):", " ".join(f"y{int(505+i/sc)}:{int(v/sc)}" for i, v in enumerate(rowsink) if v > 2))
# D5 W underline in rows (orig row1: W= zone x688..760 y70..90? use row1 W label x695..749 y150..170)
for name, img, sc in (("ORIG", o, 1.0), ("RENDER", r, s)):
    z = zone(img, 688*sc, 762*sc, 168*sc, 180*sc)
    ink, _, _, _ = census(z)
    P(f" D5 {name} row1 'W=' underline band y168..180: ink={ink.sum()}")

open(OUT, "w").write("\n".join(lines) + "\n")
print("\nbanked:", OUT)
