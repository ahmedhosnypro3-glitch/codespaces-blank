#!/usr/bin/env python3
"""w051_att2_verify: PIL verification of all 8 judge_attempt_2 findings.
ORIG = slide_051.jpg (960x540, scale 1.0); RENDER = render_2.png (2001x1125)."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = f"{NS}/recreated_pptx/qa/slide051/w051_att2_verify_raw.txt"

IMGS = {}
for name, path in (("ORIG", f"{NS}/unique_slides/slide_051.jpg"),
                   ("RENDER", f"{NS}/recreated_pptx/qa/slide051/render_2.png")):
    im = Image.open(path).convert("RGB")
    IMGS[name] = (np.asarray(im).astype(int), im.size[0] / 960.0)

lines = []
def P(*a):
    t = " ".join(str(x) for x in a); lines.append(t); print(t)

def zone(name, x0, x1, y0, y1):
    img, s = IMGS[name]
    return img[int(y0*s):int(y1*s), int(x0*s):int(x1*s)], s

def masks(z):
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = (R > 110) & (R-G > 50) & (R-B > 40)
    blue = (B > 90) & (B-R > 25) & (B-G > 10) & (G >= R)
    green = (G > 110) & (G-R > 25) & (G-B > 25)
    lum = 0.299*R+0.587*G+0.114*B
    return lum < 200, red, blue, green

def ascii_zone(name, x0, x1, y0, y1, mname="ink", rowstep=2, colstep=2):
    z, s = zone(name, x0, x1, y0, y1)
    ink, red, blue, green = masks(z)
    m = dict(ink=ink, red=red, blue=blue, green=green)[mname]
    P(f" {name} {mname} x{x0}..{x1} y{y0}..{y1}:")
    for yy in range(0, m.shape[0], rowstep):
        P("   " + "".join("#" if m[yy, xx:xx+colstep].sum() > 0 else "." for xx in range(0, m.shape[1], colstep)))

P("== 051 att2 verification ==")

# --- #2: "Step eta" glyph (red) ---
P("\n## #2 Step-eta zone x360..440 y62..86 (red mask)")
for n in IMGS: ascii_zone(n, 360, 440, 62, 86, "red")

# --- #1: d-box 1: '=' + blue digits + delimiters (ink+blue) ---
P("\n## #1 d-box1 x312..412 y148..200 (ink)")
for n in IMGS: ascii_zone(n, 312, 412, 148, 200, "ink")
P("\n## #1b d-box1 blue mask x315..410 y150..198")
for n in IMGS: ascii_zone(n, 315, 410, 150, 198, "blue")

# --- #3: delimiter curvature, ORIGINAL decisive ---
P("\n## #3 stroke straightness (x-centroid per row; straight=bracket, bowed=paren)")
def stroke_profile(label, name, x0, x1, y0, y1, mname="ink"):
    z, s = zone(name, x0, x1, y0, y1)
    ink, red, blue, green = masks(z)
    m = dict(ink=ink, red=red, blue=blue, green=green)[mname]
    prof = []
    for yy in range(m.shape[0]):
        xs = np.where(m[yy])[0]
        if len(xs): prof.append((y0+yy/s, x0+xs.mean()/s))
    if prof:
        xs_all = [p[1] for p in prof]
        P(f" {name} {label} {mname} stroke x{x0}..{x1} y{y0}..{y1}: rows={len(prof)} x-range {min(xs_all):.1f}..{max(xs_all):.1f} (span {max(xs_all)-min(xs_all):.1f}px)")
        for yy in range(0, len(prof), max(1, len(prof)//12)):
            P(f"   y={prof[yy][0]:.0f} x_centroid={prof[yy][1]:.2f}")
for item in (
    ("sample col1 L", "ORIG", 87, 94, 78, 107, "ink"),
    ("sample col1 R", "ORIG", 99, 106, 78, 107, "ink"),
    ("Z1 L", "ORIG", 595, 601, 80, 109, "ink"),
    ("Z1 R", "ORIG", 609, 616, 80, 109, "ink"),
    ("InitialW L", "ORIG", 327, 336, 58, 107, "ink"),
    ("InitialW R", "ORIG", 349, 357, 58, 107, "ink"),
    ("aug col1 L", "ORIG", 91, 98, 181, 225, "ink"),
    ("aug col1 R", "ORIG", 104, 111, 181, 225, "ink"),
    ("green d1 L", "ORIG", 378, 385, 148, 196, "green"),
    ("green d1 R", "ORIG", 401, 409, 148, 196, "green"),
    ("sample col1 L", "RENDER", 87, 94, 78, 107, "ink"),
    ("Z1 L", "RENDER", 595, 601, 80, 109, "ink"),
    ("green d1 L", "RENDER", 378, 385, 148, 196, "green"),
):
    stroke_profile(*item)

# --- #4: "Check classes of" wrap ---
P("\n## #4 Check-classes-of x490..600 y72..112 (ink)")
for n in IMGS: ascii_zone(n, 490, 600, 72, 112, "ink")

# --- #5: third d-box condition wrap ---
P("\n## #5 d-box3 condition x505..640 y296..345 (ink)")
for n in IMGS: ascii_zone(n, 505, 640, 296, 345, "ink")

# --- #6: imply arrows ---
P("\n## #6 arrow1 x494..516 y158..180 (ink)")
for n in IMGS: ascii_zone(n, 494, 516, 158, 180, "ink", 1, 1)
P("\n## #6b arrow ink counts")
for n in IMGS:
    for label, x0, x1, y0, y1 in (("arrow1", 496, 512, 160, 175), ("arrow2", 506, 522, 229, 244), ("arrow3", 496, 512, 295, 310)):
        z, s = zone(n, x0, x1, y0, y1)
        ink, *_ = masks(z)
        P(f" {n} {label}: ink={int(ink.sum())}")

# --- #7: d(Z1) label ---
P("\n## #7 d(Z1) label x278..325 y152..182 (ink)")
for n in IMGS: ascii_zone(n, 278, 325, 152, 182, "ink")

# --- #8: Augmented heading italic? ---
P("\n## #8 heading x78..240 y143..163 (ink)")
for n in IMGS: ascii_zone(n, 78, 240, 143, 163, "ink")

open(OUT, "w").write("\n".join(lines) + "\n")
print("\nbanked:", OUT)
