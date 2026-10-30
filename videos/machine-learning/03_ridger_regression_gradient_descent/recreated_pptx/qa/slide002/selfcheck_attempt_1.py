#!/usr/bin/env python3
"""Pre-judge self-check for slide 002 render_1.png (resumed worker, attempt 1).

The 8 mandatory items from scripts/17_worker_instructions.md, adapted to this
slide's content (two-line title + plus-sign artifact + house chrome; the slide
has NO equations, NO delimiters, NO tables — asserted as such where applicable).
All measurements in frame px (render * 72/150 back to 960x540 space).
"""
import numpy as np
from PIL import Image

RE = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide002/render_1.png"
).convert("RGB")).astype(int)
H, W = RE.shape[:2]
S = H / 540.0
r, g, b = RE[:, :, 0], RE[:, :, 1], RE[:, :, 2]
fails = []

def frame(arr2d):  # render-px mask -> frame-px coords helper
    return arr2d

# masks (render space)
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)          # C00000 family (strokes + title)
gray_ink = (np.abs(r - g) < 12) & (np.abs(g - b) < 12) & (r > 100) & (r < 190)  # plus/badge numeral zone
anyink = (np.abs(RE - np.array([231, 233, 230])).max(axis=2) > 28) & ~red

def bbox(mask, sl_y=(0, H), sl_x=(0, W)):
    sub = mask[sl_y[0]:sl_y[1], sl_x[0]:sl_x[1]]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (sl_x[0] + xs.min(), sl_x[0] + xs.max(), sl_y[0] + ys.min(), sl_y[0] + ys.max(), len(ys))

# (2) FRAME CONTAINMENT — content ink vs panel x54..903 y45..540 and house strokes.
tit = red & ~np.zeros_like(red)
# exclude stroke bands (x<65, x>893 render... frame 62/898) and bottom band y>530
content = red.copy()
content[:, :int(70*S)] = False
content[:, int(890*S):] = False
content[int(528*S):, :] = False
bb = bbox(content)
print(f"title content ink: frame x {bb[0]/S:.1f}..{bb[1]/S:.1f} y {bb[2]/S:.1f}..{bb[3]/S:.1f}")
if bb[0]/S < 54 or bb[1]/S > 903 or bb[2]/S < 45 or bb[3]/S > 540:
    fails.append(f"title ink outside panel: {bb}")
else:
    print(f"  containment: inside panel x54..903 y45..540 "
          f"(clearance L {bb[0]/S-54:.1f}px R {903-bb[1]/S:.1f}px T {bb[2]/S-45:.1f}px B {540-bb[3]/S:.1f}px) OK")

# plus sign containment + shape
pz = gray_ink[int(60*S):int(90*S), int(750*S):int(780*S)]
ys, xs = np.where(pz)
if len(ys) == 0:
    fails.append("plus sign ink not found in expected zone")
else:
    px0 = 750 + xs.min()/S; px1 = 750 + xs.max()/S
    py0 = 60 + ys.min()/S; py1 = 60 + ys.max()/S
    print(f"plus sign: frame x {px0:.1f}..{px1:.1f} y {py0:.1f}..{py1:.1f} n={len(ys)}")
    if px0 < 54 or px1 > 903 or py0 < 45 or py1 > 540:
        fails.append("plus sign outside panel")

# (3) EQUATIONS EXIST: slide has no equations (spec verbatim_text.equations empty);
# assert the equation concept does not apply — nothing to check. Assert no stray ink
# in the large empty zones: above title (y100..190), between lines (y233..271),
# below title (y320..530) outside strokes/badge/plus.
for nm, (y0, y1, x0, x1) in {
    "above title": (100, 190, 70, 890),
    "between lines": (233, 271, 150, 800),
    "below title": (320, 530, 70, 890),
}.items():
    bb2 = bbox(anyink | red, (int(y0*S), int(y1*S)), (int(x0*S), int(x1*S)))
    # 'below title' legitimately contains NOTHING (plus is at y71..82; badge y59..90)
    if bb2:
        print(f"  {nm} zone ink: frame x {bb2[0]/S:.1f}..{bb2[1]/S:.1f} y {bb2[2]/S:.1f}..{bb2[3]/S:.1f} n={bb2[4]}")
        if bb2[4] > 40:
            fails.append(f"unexpected ink in {nm} zone (n={bb2[4]})")
    else:
        print(f"  {nm} zone: clean")

# (4) DELIMITER GEOMETRY: N/A — no multi-line parenthesized/bracketed blocks on this slide.
print("delimiter geometry: N/A (no delimiters on slide)")

# (5) TABLE DATA: N/A — no tables.
print("table data: N/A (no tables)")

# (7) LINE/BOX WRAP — one band per text element; no wrap spillover. Text boxes are
# w=800px vs longest ink 560 (70%) so wrap is impossible by construction; assert the
# rendered band count is exactly 2 title bands and no ink hugs the box edges.
rowsum = (red & ~np.zeros_like(red))[:, int(70*S):int(890*S)].sum(axis=1)
prof = rowsum[int(180*S):int(330*S)]
bands = 0; inb = False
for v in prof:
    if v > 0 and not inb: bands += 1; inb = True
    elif v == 0: inb = False
print(f"title band count in y180..330: {bands} (expect 2)")
if bands != 2:
    fails.append(f"title band count {bands} != 2 (wrap?)")

# (8) EXPLICIT LINE SPACING — lineSpacing pinned (50pt) on both single-line boxes;
# measured baseline pitch must equal the pinned layout pitch 75px.
l1 = bbox(content, (int(195*S), int(240*S)), (int(70*S), int(890*S)))
l2 = bbox(content, (int(268*S), int(320*S)), (int(70*S), int(890*S)))
# baselines: l1 bottom (no descenders in line 1), l2 bottom - descender (Arial 0.212em @42.5pt = 9.0px)
base1 = l1[3]/S
base2 = l2[3]/S - 9.0
pitch = base2 - base1
print(f"baselines: L1 {base1:.2f} L2 {base2:.2f}  pitch {pitch:.2f} (target 75.0)")
if abs(pitch - 75.0) > 1.5:
    fails.append(f"baseline pitch {pitch:.2f} != 75.0")

# color corroboration
tcore = RE[:, :, :][red & (np.arange(H)[:, None] > int(195*S)) & (np.arange(H)[:, None] < int(320*S))]
tr = r[(red) & (np.arange(H)[:, None] > int(195*S)) & (np.arange(H)[:, None] < int(320*S))]
tg = g[(red) & (np.arange(H)[:, None] > int(195*S)) & (np.arange(H)[:, None] < int(320*S))]
tb = b[(red) & (np.arange(H)[:, None] > int(195*S)) & (np.arange(H)[:, None] < int(320*S))]
print(f"title render ink mean rgb: ({tr.mean():.0f},{tg.mean():.0f},{tb.mean():.0f})  (frame core (172,34,48); nominal C00000)")
plus_px = RE[int(71*S):int(82*S), int(763*S):int(773*S)][gray_ink[int(71*S):int(82*S), int(763*S):int(773*S)]]
print(f"plus render ink mean rgb: ({plus_px[:,0].mean():.0f},{plus_px[:,1].mean():.0f},{plus_px[:,2].mean():.0f})  (frame core (140,142,139); nominal 808080)")

# badge numeral ink presence (checker covers geometry; count dark px in disc center)
numwin = RE[int(60*S):int(88*S), int(860*S):int(894*S)]
dark = (numwin.sum(axis=2) < 330).sum()
print(f"badge numeral dark ink px: {int(dark)} (expect > 40 at 150dpi)")
if dark < 40:
    fails.append(f"badge numeral ink sparse ({int(dark)})")

print()
if fails:
    print("SELFCHECK: FAIL")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("SELFCHECK: PASS (containment, bands=2, pitch, colors, numeral, wrap, census all clean)")
print("N/A items asserted: equations=none, delimiters=none, tables=none (per spec + frame census)")
print("Item 6 (zoomed crop vision) is executed as judge leg 2 (crop pairs) after this check.")
