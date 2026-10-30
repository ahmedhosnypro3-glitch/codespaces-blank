#!/usr/bin/env python3
"""Measure pass 2 for slide_024.jpg: panel-interior ink census, precise row
profiles of the 3 red text bands, bottom-icon shape analysis (zoomed ASCII +
saved crop), badge numeral ink, and a font-size advance fit with real
Arial-metric fonts (Liberation Sans Regular AND Bold).
Complements the predecessor's qa/slide024/measure_frame.py (kept verbatim)."""
import glob
import numpy as np
from PIL import Image, ImageFont

IM = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_024.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = im.shape[:2]
BG = np.array([231, 233, 230])  # panel E9E9E7 (measured at (300,300))

# --- 1. sensitive census INSIDE the panel only (margins off strokes+badge) ----
x0, x1 = 66, 894
y0, y1 = 52, 530
sub = im[y0:y1, x0:x1]
diff = np.abs(sub - BG).max(axis=2)
ink = diff > 18
print(f"panel-interior sensitive ink px = {ink.sum()}")
rows = np.where(ink.sum(axis=1) > 2)[0]
bands = []
if len(rows):
    s = rows[0]; p = rows[0]
    for y in rows[1:]:
        if y - p > 5:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
print("census bands (absolute coords):")
for (a, b) in bands:
    sel = ink[a:b + 1]
    xs_ = np.where(sel.any(axis=0))[0]
    print(f"  y {y0+a}..{y0+b}  x {x0+xs_.min()}..{x0+xs_.max()}  npx={sel.sum()}")

# --- 2. precise row profiles of the red bands (halo vs dense core) ------------
red = (im[:, :, 0] > 90) & ((im[:, :, 0] - im[:, :, 1]) > 40) & ((im[:, :, 0] - im[:, :, 2]) > 10)
for label, (ya, yb) in (("T(title)", (218, 275)), ("S1(and)", (288, 328)), ("S2(how)", (343, 388))):
    print(f"\n{label} row profile (red px per row, x 100..900):")
    for y in range(ya, yb):
        n = red[y, 100:900].sum()
        if n:
            xs_ = np.where(red[y, 100:900])[0]
            print(f"  y={y}: n={n:4d}  x {100+xs_.min()}..{100+xs_.max()}")

# --- 3. bottom icon: fine-grained mask analysis ---------------------------------
# dark non-red ink, whole bottom half of the panel interior
dark = (im.sum(axis=2) < 480) & ~((im[:, :, 0] > 90) & (im[:, :, 1] < 70))
icon_zone = dark[440:537, 380:580]
rr = np.where(icon_zone.sum(axis=1) > 0)[0]
cc = np.where(icon_zone.sum(axis=0) > 0)[0]
print("\nicon hunt (zone y 440..537, x 380..580):")
if len(rr):
    print(f"  dark ink rows {440+rr.min()}..{440+rr.max()}  cols {380+cc.min()}..{380+cc.max()}")
    # strict dark bbox too
    strict = (im.sum(axis=2) < 420)[440:537, 380:580]
    rr2 = np.where(strict.sum(axis=1) > 0)[0]
    cc2 = np.where(strict.sum(axis=0) > 0)[0]
    print(f"  strict(sum<420) rows {440+rr2.min()}..{440+rr2.max()}  cols {380+cc2.min()}..{380+cc2.max()}")
    looser = (im.sum(axis=2) < 600)[440:537, 380:580]
    rr3 = np.where(looser.sum(axis=1) > 0)[0]
    cc3 = np.where(looser.sum(axis=0) > 0)[0]
    print(f"  loose(sum<600)  rows {440+rr3.min()}..{440+rr3.max()}  cols {380+cc3.min()}..{380+cc3.max()}")

# full-resolution ASCII of the icon, 4 darkness levels
print("\nicon ASCII (x 458..484, y 500..528; '#' sum<330, '+' <450, '-' <570, '.' <690):")
for y in range(500, 528):
    line = ""
    for x in range(458, 484):
        c = im[y, x]
        s = c.sum()
        line += "#" if s < 330 else ("+" if s < 450 else ("-" if s < 570 else ("." if s < 690 else " ")))
    print(f"{y:3d} {line}")

# icon core color
ys, xs = np.where(strict)
if len(ys):
    pts = im[440 + ys, 380 + xs]
    print("icon strict-dark px color median:", np.median(pts, axis=0), "n=", len(pts))

# save a x8 LANCZOS upscale of the icon region for shape study
crop = Image.open(IM).convert("RGB").crop((452, 496, 486, 528))
crop = crop.resize((crop.width * 8, crop.height * 8), Image.LANCZOS)
outp = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide024/icon_x8.png"
crop.save(outp)
print("saved", outp)

# --- 4. badge numeral ink on THIS frame -----------------------------------------
print("\nbadge numeral ink (x 862..892, y 59..88, sum<330 px per row):")
for y in range(59, 89):
    row = im[y, 862:893]
    darkpx = (row.sum(axis=1) < 330).sum()
    if darkpx:
        xs_ = np.where(row.sum(axis=1) < 330)[0]
        print(f"  y={y}: darkpx={darkpx} x {862+xs_.min()}..{862+xs_.max()}")

# --- 5. font-size advance fit -----------------------------------------------------
T = "Gradient Descent (GD)"
S1 = "and"
S2 = "How to apply to minimize Loss function"
# inclusive ink bboxes from the red band scan (measure_frame.py + row profiles)
MEAS = {"T": (243, 717, 225, 267), "S1": (452, 507, 296, 320), "S2": (202, 757, 351, 379)}

for fname, pat in (("Bold", "/usr/share/fonts/**/LiberationSans-Bold.ttf"),
                   ("Regular", "/usr/share/fonts/**/LiberationSans-Regular.ttf")):
    cands = glob.glob(pat, recursive=True)
    if not cands:
        print(f"\nno font for {fname}"); continue
    fontpath = cands[0]
    print(f"\n=== advance fit with {fname} ({fontpath}) ===")
    for label, text in (("T", T), ("S1", S1), ("S2", S2)):
        mx = MEAS[label][1] - MEAS[label][0] + 1
        my = MEAS[label][3] - MEAS[label][2] + 1
        print(f"{label} '{text[:32]}' measured ink w={mx} h={my}")
        best = []
        for size in range(14, 60):
            f = ImageFont.truetype(fontpath, size)
            bbox = f.getbbox(text)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            best.append((abs(w - mx), size, w, h, bbox))
        best.sort()
        for d, size, w, h, bbox in best[:4]:
            print(f"   size {size}: ink w={w} (d={d}) h={h} bbox={bbox}")

# --- 6. band pitch (for placement) ----------------------------------------------
print("\nband centers/pitches (inclusive bboxes):")
c = [(225+267)/2, (296+320)/2, (351+379)/2]
print("centers y:", c, " pitches:", [round(c[1]-c[0],1), round(c[2]-c[1],1)])
print("x centers:", [(243+717)/2, (452+507)/2, (202+757)/2])
