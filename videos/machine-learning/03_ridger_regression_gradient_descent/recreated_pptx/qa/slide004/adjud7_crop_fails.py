#!/usr/bin/env python3
"""PIL-first adjudication of the attempt-7 crop-judge findings for slide 004
(crop_7_let_boxes FAIL, crop_7_where_block FAIL, remember-MAJOR inside PASS).
Renders' side is already pinned by the build code + eq sidecars (black ink,
no underlines, lowercase n, flush-left where lines); this script measures the
ORIGINAL frame (unique_slides/slide_004.jpg, 960x540, 1px=1pt) to confirm or
refute each claimed defect, plus the eq_004_norm asset for the subscript-2 size.
"""
import numpy as np
from PIL import Image

D = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
ORIG = D + "/unique_slides/slide_004.jpg"
B = D + "/recreated_pptx/build/assets"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W, _ = o.shape
print("orig", o.shape)

def red_mask(a):
    R, G, Bl = a[..., 0], a[..., 1], a[..., 2]
    return (R > 110) & (R - G > 45) & (R - Bl > 35)

def blue_mask(a):
    R, G, Bl = a[..., 0], a[..., 1], a[..., 2]
    return (Bl > 110) & (Bl - R > 35) & (Bl - G > 25)

def dark_mask(a):
    return a.max(axis=-1) < 120

def components(mask):
    """8-connected components of a boolean mask -> list of (x0,y0,x1,y1,area)."""
    lab = np.zeros(mask.shape, dtype=int)
    out = []
    cur = 0
    idx = np.argwhere(mask)
    seen = np.zeros(mask.shape, dtype=bool)
    for (y, x) in idx:
        if seen[y, x]:
            continue
        cur += 1
        stack = [(y, x)]
        seen[y, x] = True
        pts = []
        while stack:
            cy, cx = stack.pop()
            pts.append((cy, cx))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] \
                       and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
        ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
        out.append((min(xs), min(ys), max(xs), max(ys), len(pts)))
    return out

print("\n=== S1: vector-entry ink colors (ORIGINAL) ===")
for name, (x0, x1, y0, y1) in {
    "box1 matrix": (158, 218, 105, 212),
    "box2 matrix": (500, 558, 105, 212),
}.items():
    reg = o[y0:y1, x0:x1]
    rm, dm = red_mask(reg), dark_mask(reg)
    print(f"{name} frame x{x0}..{x1} y{y0}..{y1}: red_px={rm.sum()} dark_px={dm.sum()}")
    if rm.sum() > 30:
        rr = reg[rm]
        print("   red median RGB:", np.median(rr, axis=0))

print("\n=== S2: 'N x 1' subscript case (ORIGINAL, red ink) ===")
# judge: orig crop ~x235 y215 (crop x0=75,y0=94, eff~2.09) -> frame ~(187,197)
win = o[185:215, 172:215]
rm = red_mask(win)
comps = components(rm)
comps.sort(key=lambda c: c[0])
print("window x172..215 y185..215, red components (x0,y0,x1,y1,area):")
for c in comps:
    if c[4] >= 4:
        print("  ", c, " h=", c[3] - c[1] + 1, " w=", c[2] - c[0] + 1)

print("\n=== S2b: same window in RENDER (frame-scaled) ===")
r = np.asarray(Image.open(D + "/recreated_pptx/qa/slide004/render_7.png").convert("RGB")).astype(int)
SX, SY = r.shape[1] / 960.0, r.shape[0] / 540.0
def rwin(x0, x1, y0, y1):
    return r[int(y0*SY):int(y1*SY), int(x0*SX):int(x1*SX)]
rreg = rwin(172, 215, 185, 215)
dm = dark_mask(rreg)
comps = components(dm)
comps.sort(key=lambda c: c[0])
print("render dark components in same frame window:")
for c in comps:
    if c[4] >= 4:
        print("  ", c, " h=", c[3] - c[1] + 1, " w=", c[2] - c[0] + 1)

print("\n=== S3: underline bars under 'from Model Yh=XW' (ORIGINAL) ===")
# band y163..183 per build comment; underline would sit ~y184..192
for (x0, x1, y0, y1, tag) in [
    (560, 745, 183, 193, "under-line1 full sweep"),
]:
    reg = o[y0:y1, x0:x1]
    dm = dark_mask(reg) | red_mask(reg)
    # horizontal runs >= 6 px
    for yy in range(reg.shape[0]):
        row = dm[yy]
        xs = np.flatnonzero(row)
        if xs.size == 0:
            continue
        splits = np.split(xs, np.flatnonzero(np.diff(xs) > 2) + 1)
        for s in splits:
            if s.size >= 6:
                print(f"  {tag}: y={y0+yy} run x{x0+s[0]}..{x0+s[-1]} len={s.size}")

print("\n=== S3b: 'Let Y =' lead-in underline check (ORIGINAL) ===")
reg = o[155:168, 85:160]
dm = dark_mask(reg) | red_mask(reg)
for yy in range(reg.shape[0]):
    xs = np.flatnonzero(dm[yy])
    if xs.size == 0:
        continue
    splits = np.split(xs, np.flatnonzero(np.diff(xs) > 2) + 1)
    for s in splits:
        if s.size >= 6:
            print(f"  y={155+yy} run x{85+s[0]}..{85+s[-1]} len={s.size}")

print("\n=== S4: where-block line left edges ===")
for i, (y0, y1) in enumerate([(284, 306), (312, 336), (343, 367)]):
    for img, tag, sc in ((o, "orig", 1.0), (r, "render", 1.0)):
        if tag == "render":
            reg = rwin(497, 884, y0, y1)
        else:
            reg = o[y0:y1, 497:884]
        dm = dark_mask(reg) | red_mask(reg) | blue_mask(reg)
        cols = np.flatnonzero(dm.any(axis=0))
        left = 497 + cols[0] if cols.size else -1
        right = 497 + cols[-1] if cols.size else -1
        print(f"  line{i+1} y{y0}..{y1} [{tag}]: ink x{left}..{right}")

print("\n=== S5: word segmentation + ink fraction, where line 1 (ORIGINAL) ===")
def words(a, y0, y1, x0=497, x1=884, gap=5):
    reg = a[y0:y1, x0:x1]
    dm = dark_mask(reg) | red_mask(reg) | blue_mask(reg)
    colhas = dm.any(axis=0)
    xs = np.flatnonzero(colhas)
    if xs.size == 0:
        return []
    splits = np.split(xs, np.flatnonzero(np.diff(xs) > gap) + 1)
    out = []
    for s in splits:
        sub = dm[:, s[0]:s[-1] + 1]
        frac = sub.mean()
        out.append((x0 + s[0], x0 + s[-1], round(float(frac), 3)))
    return out
print("  orig line1 words (x0,x1,ink-frac):", words(o, 284, 306))
print("  orig line2 words:", words(o, 312, 336))
print("  orig line3 words:", words(o, 343, 367))
print("  render line1 words:", words(rwin(497, 884, 284, 306), 0, 306-284))
print("  render line2 words:", words(rwin(497, 884, 312, 336), 0, 336-312))
print("  render line3 words:", words(rwin(497, 884, 343, 367), 0, 367-343))

print("\n=== S6: where-block ink colors per line (ORIGINAL vs RENDER) ===")
for i, (y0, y1) in enumerate([(284, 306), (312, 336), (343, 367)]):
    for a, tag in ((o[y0:y1, 497:884], "orig"), (rwin(497, 884, y0, y1), "rend")):
        rm, bm, dm = red_mask(a), blue_mask(a), dark_mask(a)
        msg = f"  line{i+1} [{tag}]: red={rm.sum()} blue={bm.sum()} dark={dm.sum()}"
        if rm.sum() > 20:
            rr = a[rm]
            msg += f" red_med={np.median(rr,axis=0).astype(int)} x[{np.flatnonzero(rm.any(axis=0))[0]}..{np.flatnonzero(rm.any(axis=0))[-1]}]"
        if bm.sum() > 20:
            bb = a[bm]
            msg += f" blue_med={np.median(bb,axis=0).astype(int)} x[{np.flatnonzero(bm.any(axis=0))[0]}..{np.flatnonzero(bm.any(axis=0))[-1]}]"
        print(msg)

print("\n=== S7: remember eq '||a||2 = a^T a' component heights ===")
# ORIGINAL frame x786..884 y118..155
reg = o[116:156, 786:886]
dm = dark_mask(reg)
comps = components(dm)
comps = [c for c in comps if c[4] >= 6]
comps.sort(key=lambda c: c[0])
print("orig components (x0,y0,x1,y1,area) rel to (786,116):")
for c in comps:
    print("   x%d..%d y%d..%d area=%d h=%d w=%d" % (786+c[0], 786+c[2], 116+c[1], 116+c[3], c[4], c[3]-c[1]+1, c[2]-c[0]+1))
# ASSET eq_004_norm.png at 600dpi: scale 600/72 = 8.333 px per frame pt
asset = np.asarray(Image.open(B + "/eq_004_norm.png").convert("RGB")).astype(int)
adm = asset.max(axis=-1) < 160
comps = components(adm)
comps = [c for c in comps if c[4] >= 40]
comps.sort(key=lambda c: c[0])
print("asset eq_004_norm components (600dpi; 8.333 px = 1 frame pt):")
for c in comps:
    print("   x%d..%d y%d..%d area=%d h=%d(=%.1fpt) w=%d" % (c[0], c[2], c[1], c[3], c[4], c[3]-c[1]+1, (c[3]-c[1]+1)/8.333, c[2]-c[0]+1))
