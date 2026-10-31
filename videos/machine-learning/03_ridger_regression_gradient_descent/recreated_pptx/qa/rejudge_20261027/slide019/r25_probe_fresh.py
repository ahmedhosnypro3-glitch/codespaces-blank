#!/usr/bin/env python3
"""Fresh r25 pixel probes for slide 019 r16-FAIL adjudication.
render.png (2001x1125, 2026-10-31 06:15:53) vs unique_slides/slide_019.jpg (960x540).
All coords in slide-space px unless noted. Read-only."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide019"
rp = Image.open(f"{RJ}/render.png").convert("RGB")
op = Image.open(f"{NS}/unique_slides/slide_019.jpg").convert("RGB")
R = np.asarray(rp).astype(int); O = np.asarray(op).astype(int)
H, W = R.shape[:2]
SX, SY = W / 960.0, H / 540.0

def rs(x): return int(round(x * SX))
def ry(y): return int(round(y * SY))

def region(img, x0, y0, x1, y1):
    if img is R:
        return img[ry(y0):ry(y1), rs(x0):rs(x1)]
    return img[y0:y1, x0:x1]

def ink_stats(img, x0, y0, x1, y1):
    """count ink px by class in slide-space box: red, dark, blue, green; plus mean bg"""
    a = region(img, x0, y0, x1, y1)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (r + g + b) / 3.0
    red = ((r > 100) & (r > g * 1.5) & (r > b * 1.5)).sum()
    dark = (lum < 90).sum()
    blue = ((b > 100) & (b > r * 1.4) & (b > g * 1.2)).sum()
    green = ((g > 90) & (g > r * 1.3) & (g > b * 1.3)).sum()
    ink = (lum < 200).sum()
    bg = a[(lum >= 200)]
    mean = bg.mean(axis=0).round(1).tolist() if len(bg) else None
    return dict(px=int(a.shape[0] * a.shape[1]), ink=int(ink), red=int(red),
                dark=int(dark), blue=int(blue), green=int(green), bg_mean=mean)

print("== D1: column fills (mean bg RGB, ink-class counts) ==")
# header band y~174..198 (above body), body cell interiors away from text
for name, x0, x1 in [("NO-REG col", 124, 383), ("RIDGE3 col", 390, 643), ("RIDGE10 col", 644, 894)]:
    for img, tag in ((O, "ORIG"), (R, "RENDER")):
        h = ink_stats(img, x0 + 8, 176, x1 - 8, 196)   # header strip
        b = ink_stats(img, x0 + 8, 300, x1 - 8, 320)   # body row-gap (row1/row2 gap)
        print(f"{name:11s} {tag:6s} header y176-196 bg={h['bg_mean']} ink={h['ink']} red={h['red']} green={h['green']} | body y300-320 bg={b['bg_mean']} ink={b['ink']}")
# bottom tint strip y515..523
for img, tag in ((O, "ORIG"), (R, "RENDER")):
    for name, x0, x1 in [("NO-REG", 130, 247), ("RIDGE3", 390, 390 + 253), ("RIDGE10", 644, 644 + 250)]:
        s = ink_stats(img, x0 + 6, 516, x1 - 6, 522)
        print(f"strip {name:8s} {tag:6s} y516-522 bg={s['bg_mean']}")

print()
print("== D2: RIDGE10 (col2) W-vector digits — XML source of truth + cell pixel diff ==")
import zipfile, re
z = zipfile.ZipFile(NS + "/recreated_pptx/slide_019_recreated.pptx")
xmls = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml", n)]
txt = ""
for n in sorted(xmls):
    x = z.read(n).decode("utf8", "ignore")
    if "Ridge" in x or "0.13" in x:
        txt += x
runs = re.findall(r"<a:t>([^<]*)</a:t>", txt)
w10 = [t for t in runs if re.fullmatch(r"0\.\d+|1\.\d+|\d+", t.strip())]
print("numeric runs in deck slide xml:", w10)
# pixel diff of the three col2 W-cell entry regions (rows y~200-297 / 305-402 / 415-512), entries right of 'W =' ~ x700-890
for i, (y0, y1) in enumerate([(200, 297), (305, 402), (415, 512)]):
    a = region(R, 700, y0 + 20, 890, y1 - 6); b = region(O, 700, y0 + 20, 890, y1 - 6)
    if a.shape != b.shape:
        from PIL import Image as I
        b = np.asarray(I.fromarray(b.astype('uint8')).resize((a.shape[1], a.shape[0]), I.LANCZOS)).astype(int)
    d = np.abs(a - b).sum(axis=2)
    print(f"col2 row{i} W-cell x700-890 y{y0+20}-{y1-6}: diff>90 px = {int((d > 90).sum())} / {d.size} ({100*(d>90).mean():.2f}%)")

print()
print("== D3: W-entry ink color in all 9 W boxes (entries only, x0+8..x0+80) ==")
COLX = [124, 384, 644]
ROWS = [(200, 297), (305, 402), (415, 512)]
for ci, cx in enumerate(COLX):
    for ri, (y0, y1) in enumerate(ROWS):
        o = ink_stats(O, cx + 8, y0 + 25, cx + 80, y1 - 10)
        r = ink_stats(R, cx + 8, y0 + 25, cx + 80, y1 - 10)
        print(f"col{ci} row{ri}: ORIG ink={o['ink']} red={o['red']} dark={o['dark']} | RENDER ink={r['ink']} red={r['red']} dark={r['dark']}")

print()
print("== D4: delimiters — straight red bars vs curved dark parens, 9 cells ==")
def bars(img, x0, y0, x1, y1):
    a = region(img, x0, y0, x1, y1)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (r + g + b) / 3.0
    red = ((r > 100) & (r > g * 1.5) & (r > b * 1.5) & (lum < 220)).sum()
    dark = (lum < 90).sum()
    return int(red), int(dark)
for ci, cx in enumerate(COLX):
    for ri, (y0, y1) in enumerate(ROWS):
        o = bars(O, cx + 3, y0 + 2, cx + 6, y1 - 2)      # left edge strip
        rr = bars(R, cx + 3, y0 + 2, cx + 6, y1 - 2)
        oR = bars(O, cx + 80, y0 + 2, cx + 84, y1 - 2)    # right edge strip
        rR = bars(R, cx + 80, y0 + 2, cx + 84, y1 - 2)
        print(f"col{ci} row{ri}: ORIG L red/dark={o} R red/dark={oR} | RENDER L={rr} R={rR}")

print()
print("== D5: 'Test Data' blue box right edge (max x of blue border, y40..160) ==")
for img, tag in ((O, "ORIG"), (R, "RENDER")):
    a = region(img, 60, 40, 500, 160)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    blue = (b > 110) & (b > r * 1.4) & (b > g * 1.2)
    ys, xs = np.where(blue)
    if len(xs):
        x0 = 60 if img is O else rs(60)
        print(f"{tag}: blue-border max slide-x = {(x0 + xs.max()) / (1 if img is O else SX):.1f}, count={len(xs)}")

print()
print("== D6: z1 label ink color (top ref line, x160..230 y88..116) ==")
for img, tag in ((O, "ORIG"), (R, "RENDER")):
    s = ink_stats(img, 160, 88, 235, 116)
    print(f"{tag}: ink={s['ink']} red={s['red']} dark={s['dark']} blue={s['blue']}")
# also z2 for contrast
for img, tag in ((O, "ORIG"), (R, "RENDER")):
    s = ink_stats(img, 300, 88, 375, 116)
    print(f"z2 {tag}: ink={s['ink']} red={s['red']} dark={s['dark']} blue={s['blue']}")
