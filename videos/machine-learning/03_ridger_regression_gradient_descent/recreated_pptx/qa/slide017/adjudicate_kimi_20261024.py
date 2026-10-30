#!/usr/bin/env python3
"""PIL adjudication of slide 017's banked selfcheck FAILs + the void judge's
claims (worker kimi-slide017, 2026-10-24). Every item measured against BOTH
images: render_3.png (2001x1125, S=2.083333 render-px per frame-px) and the
original unique_slides/slide_017.jpg (960x540, 1px=1pt). render_3.png is proven
current (md5-identical to a fresh soffice render of the current pptx).
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RENDER = os.path.join(HERE, "render_3.png")
ORIG = os.path.join(DECK, "unique_slides", "slide_017.jpg")

ri = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
oi = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
S = ri.shape[0] / 540.0
print("render %dx%d scale %.6f  orig %dx%d" % (ri.shape[1], ri.shape[0], S, oi.shape[1], oi.shape[0]))

def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    gray = (abs(r - 233) < 22) & (abs(g - 233) < 22) & (abs(b - 231) < 24)
    white = a.sum(axis=2) > 735
    bg = gray | white
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10) & ~bg
    blue = (b > 90) & ((b - r) > 40) & ((g - r) < 30) & ~bg
    dark = (a.sum(axis=2) < 330) & ~bg
    return dict(red=red, blue=blue, dark=dark, white=white, gray=gray,
                mint=((r > 150) & (g > 200) & (b < 240) & (g - r > 20)),
                yellow=((r > 225) & (g > 225) & (b < 200)))

mo, mr = masks(oi), masks(ri)

def o_sl(mask, y0, y1, x0, x1):
    return mask[max(0, y0):y1 + 1, max(0, x0):x1 + 1]
def r_sl(mask, y0, y1, x0, x1):
    return mask[max(0, int(y0 * S)):int(y1 * S) + 1, max(0, int(x0 * S)):int(x1 * S) + 1]

def runs(row, minlen=1):
    out, i, n = [], 0, len(row)
    while i < n:
        if row[i]:
            j = i
            while j + 1 < n and row[j + 1]:
                j += 1
            if j - i + 1 >= minlen:
                out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out

def merge(rs, gap):
    m = []
    for x0, x1 in rs:
        if m and x0 - m[-1][1] <= gap:
            m[-1][1] = x1
        else:
            m.append([x0, x1])
    return m

def colgroups(mask, y0, y1, x0, x1, ren, gap_frame=14):
    """Column-ink groups, gap tolerance in FRAME px on BOTH sides (the banked
    selfcheck applied 14 on the orig side but 14 RENDER px on the render side
    -- an asymmetric tolerance)."""
    sub = r_sl(mask, y0, y1, x0, x1) if ren else o_sl(mask, y0, y1, x0, x1)
    d = sub.sum(axis=0)
    gap_px = gap_frame * S if ren else gap_frame
    rs = merge(runs(d > 0, 1), gap_px)
    return ([(round(p[0] / S + x0, 1), round(p[1] / S + x0, 1)) for p in rs]
            if ren else [(p[0] + x0, p[1] + x0) for p in rs])

print("\n== ITEM 1/2: title red + blue groups (symmetric 14 frame-px gap, badge zone x>850 excluded) ==")
XW = (170, 850)  # badge ring starts ~x858; exclude it from both sides
ro, rr = colgroups(mo["red"], 60, 99, *XW, False), colgroups(mr["red"], 60, 99, *XW, True)
bo, br = colgroups(mo["blue"], 60, 99, *XW, False), colgroups(mr["blue"], 60, 99, *XW, True)
print("   RED  orig:", ro)
print("   RED  rend:", rr)
print("   BLUE orig:", bo)
print("   BLUE rend:", br)
ok_red = len(ro) == len(rr) and all(abs(a[0]-b[0]) <= 12 and abs(a[1]-b[1]) <= 12 for a, b in zip(ro, rr))
ok_blue = len(bo) == len(br) and all(abs(a[0]-b[0]) <= 12 and abs(a[1]-b[1]) <= 12 for a, b in zip(bo, br))
print("   VERDICT red groups:", "REFUTED (identical word runs)" if ok_red else "REAL DIFFERENCE")
print("   VERDICT blue groups:", "REFUTED (identical word runs)" if ok_blue else "REAL DIFFERENCE")

print("\n== ITEM 3: test-table bottom borders (y ~251/389/527, x 664..876) ==")
def hline_scan(img_white, y0, y1, x0, x1, ren):
    sub = (~r_sl(img_white, y0, y1, x0, x1)) if ren else (~o_sl(img_white, y0, y1, x0, x1))
    d = sub.sum(axis=1)
    frac = d / sub.shape[1]
    out = []
    for i, f in enumerate(frac):
        if f > 0.30:
            yy = y0 + (i / S if ren else i)
            out.append((round(yy, 1), round(float(f), 2)))
    return out
def line_color(img, y, x, ren):
    if ren:
        yy, xx = int(y * S), int(x * S)
        return np.round(np.median(img[yy-2:yy+3, xx-2:xx+3].reshape(-1, 3), axis=0)).astype(int)
    return np.round(np.median(img[y-1:y+2, x-1:x+2].reshape(-1, 3), axis=0)).astype(int)
for bi, (ya, yb, yexp) in enumerate([(231, 262, 251), (369, 400, 389), (507, 538, 527)], 1):
    o_lines = hline_scan(mo["white"], ya, yb, 664, 876, False)
    r_lines = hline_scan(mr["white"], ya, yb, 664, 876, True)
    o_bot = [l for l in o_lines if abs(l[0] - yexp) <= 6]
    r_bot = [l for l in r_lines if abs(l[0] - yexp) <= 6]
    print("   test B%d expected bottom y=%d:" % (bi, yexp))
    print("      orig first/last non-white rows: %s .. %s" % (o_lines[0] if o_lines else None, o_lines[-1] if o_lines else None))
    print("      rend first/last non-white rows: %s .. %s" % (r_lines[0] if r_lines else None, r_lines[-1] if r_lines else None))
    print("      orig bottom present:", bool(o_bot), " render bottom present:", bool(r_bot))
    for yy in range(yexp - 2, yexp + 2):
        print("      y=%d  orig px@690 %s  rend px@690 %s" % (yy, line_color(oi, yy, 690, False), line_color(ri, yy, 690, True)))

print("\n== ITEM 4: Train / Test label ink colour inside the blue boxes ==")
for nm, (x0, x1) in [("Train", (96, 160)), ("Test", (801, 866))]:
    def label_ink(img, ren):
        sub_img = (img[int(96*S):int(125*S), int(x0*S):int(x1*S)] if ren else img[96:126, x0:x1+1])
        fill = np.median(sub_img.reshape(-1, 3), axis=0)
        dist = np.abs(sub_img - fill).max(axis=2)
        ink = dist > 80
        r_, g_, b_ = sub_img[:, :, 0], sub_img[:, :, 1], sub_img[:, :, 2]
        whiteish = ink & (sub_img.sum(axis=2) > 735)
        reddish = ink & (r_ > 90) & ((r_ - g_) > 40)
        darkish = ink & (sub_img.sum(axis=2) < 330)
        inkmed = (np.round(np.median(sub_img[ink].reshape(-1, 3), axis=0)).astype(int).tolist()
                  if ink.sum() >= 8 else None)
        return fill, int(ink.sum()), int(whiteish.sum()), int(reddish.sum()), int(darkish.sum()), inkmed
    fo = label_ink(oi, False); fr = label_ink(ri, True)
    print("   %s label: orig fill=%s ink=%d white=%d red=%d dark=%d inkmed=%s" % (nm, np.round(fo[0]).astype(int), fo[1], fo[2], fo[3], fo[4], fo[5]))
    print("   %s label: rend fill=%s ink=%d white=%d red=%d dark=%d inkmed=%s" % (nm, np.round(fr[0]).astype(int), fr[1], fr[2], fr[3], fr[4], fr[5]))
    Image.fromarray(oi[96:126, x0:x1+1].astype(np.uint8)).resize(
        ((x1-x0+1)*4, 30*4), Image.LANCZOS).save(os.path.join(HERE, "label_%s_orig_x4.png" % nm.lower()))
    Image.fromarray(ri[int(96*S):int(125*S), int(x0*S):int(x1*S)].astype(np.uint8)).save(
        os.path.join(HERE, "label_%s_render.png" % nm.lower()))

print("\n== ITEM 5: mint y-row cells, all three test bands (fill medians) ==")
BANDS = [(1, (222, 247)), (2, (360, 385)), (3, (498, 523))]
for bi, (y0, y1) in BANDS:
    for ci, (x0, x1) in enumerate([(672, 716), (722, 767), (773, 818), (824, 869)], 1):
        def cell(img, ren):
            sub = (img[int(y0*S):int(y1*S), int(x0*S):int(x1*S)] if ren else img[y0:y1+1, x0:x1+1])
            return np.median(sub.reshape(-1, 3), axis=0), sub.reshape(-1, 3).shape[0]
        co, _ = cell(oi, False); cr, _ = cell(ri, True)
        print("   B%d cell%d: orig fill=%s rend fill=%s" % (bi, ci, np.round(co).astype(int), np.round(cr).astype(int)))
# also mint pixel counts per band (same windows as the banked selfcheck, all 3 bands)
for bi, (y0, y1) in enumerate([(222, 246), (359, 383), (497, 521)], 1):
    mo_m = int(o_sl(mo["mint"], y0, y1, 724, 868).sum())
    mr_m = int(r_sl(mr["mint"], y0, y1, 724, 868).sum())
    print("   B%d mint px: orig %d rend %d" % (bi, mo_m, mr_m))

print("\n== ITEM 6: frame containment x<56 (left of the left stroke) ==")
sub = ri[:, :int(56 * S)]
r_, g_, b_ = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
nonwhite = sub.sum(axis=2) <= 735
panelish = (abs(r_ - 232) <= 16) & (abs(g_ - 232) <= 16) & (abs(b_ - 230) <= 16)
other = nonwhite & ~panelish
print("   non-white px left of x56: %d ; of those panel-gray: %d ; OTHER ink: %d" % (int(nonwhite.sum()), int((nonwhite & panelish).sum()), int(other.sum())))
if other.sum():
    ys, xs = np.where(other)
    print("   OTHER ink bbox (render px): x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    # sample a few colors
    for k in range(0, len(xs), max(1, len(xs)//5)):
        print("      sample px:", sub[ys[k], xs[k]])

print("\n== ITEM 7: badge ring (void-judge claim 3) ==")
ob = o_sl(mo["red"] | mo["blue"] | mo["dark"], 40, 100, 845, 910)
rb = r_sl(mr["red"] | mr["blue"] | mr["dark"], 40, 100, 845, 910)
def bbox(sub, ren, x0, y0):
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return (round(xs.min()/S + x0, 1) if ren else xs.min()+x0, round(ys.min()/S + y0, 1) if ren else ys.min()+y0,
            round(xs.max()/S + x0, 1) if ren else xs.max()+x0, round(ys.max()/S + y0, 1) if ren else ys.max()+y0)
print("   orig badge ink bbox:", bbox(ob, False, 845, 40))
print("   rend badge ink bbox:", bbox(rb, True, 845, 40))
# ring colour sample: the ring is purple 6A5ACD; sample darkest ring px in each
def ring_color(img, ren):
    sub = (img[int(50*S):int(95*S), int(855*S):int(900*S)] if ren else img[50:96, 855:901])
    s = sub.reshape(-1, 3)
    # ring px = saturated non-yellow, non-white
    rr_, gg_, bb_ = s[:, 0], s[:, 1], s[:, 2]
    m = (bb_ - rr_ > 30) & (bb_ > 60)
    if m.sum() == 0:
        return None, 0
    return np.round(np.median(s[m], axis=0)).astype(int), int(m.sum())
print("   orig ring median:", ring_color(oi, False))
print("   rend ring median:", ring_color(ri, True))
