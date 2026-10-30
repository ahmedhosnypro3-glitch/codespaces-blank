#!/usr/bin/env python3
"""att9 measurement pass 4: z_zone per-element, vertical extent, 329 rule."""
from PIL import Image
import numpy as np

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
O48 = np.array(Image.open(f"{DECK}/unique_slides/slide_048.jpg").convert("RGB")).astype(int)
O49 = np.array(Image.open(f"{DECK}/unique_slides/slide_049.jpg").convert("RGB")).astype(int)

def runs(mask, start):
    out, s = [], None
    for i, v in enumerate(mask):
        if v and s is None: s = i
        elif not v and s is not None: out.append((start + s, start + i - 1)); s = None
    if s is not None: out.append((start + s, start + len(mask) - 1))
    return out

def bbox(a, x0, x1, y0, y1, thr=185):
    z = a[y0:y1, x0:x1]; m = z.sum(axis=2) < thr * 3
    if not m.any(): return None
    ys, xs = np.where(m)
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max(), int(m.sum()))

print("===== 1. z_zone per-element bboxes (y60..126) =====")
for nm, (x0, x1, y0, y1) in [
    ("label", (533, 632, 78, 102)), ("zheader", (630, 712, 66, 86)),
    ("zdigits_r1", (630, 712, 86, 103)), ("zdigits_r2", (630, 712, 103, 122)),
    ("zparens", (630, 712, 84, 122))]:
    b48 = bbox(O48, x0, x1, y0, y1); b49 = bbox(O49, x0, x1, y0, y1)
    print(f"  {nm}: 048={b48} 049={b49}")

print("===== 2. z_zone diff px by element =====")
d = np.abs(O48[60:126, 530:715] - O49[60:126, 530:715]).sum(axis=2)
ys, xs = np.where(d > 60)
pts = list(zip(xs + 530, ys + 60))
for nm, (x0, x1, y0, y1) in [("label", (533, 632, 78, 102)), ("zheader", (630, 712, 66, 86)),
                             ("zdigits", (630, 712, 86, 122)), ("other", (530, 715, 60, 126))]:
    n = sum(1 for x, y in pts if x0 <= x <= x1 and y0 <= y <= y1)
    print(f"  {nm}: {n}")

print("===== 3. x274 vertical y-extent (census c>=1, sum<640) =====")
for nm, O in [("048", O48), ("049", O49)]:
    z = O[136:535, 273:276]; m = z.sum(axis=2) < 640
    rr = m.sum(axis=1)
    ys = [136 + i for i, c in enumerate(rr) if c >= 1]
    gaps = [(a, b) for a, b in zip(ys, ys[1:]) if b - a > 1]
    print(f"  {nm}: rows {min(ys)}..{max(ys)} n={len(ys)} gaps={gaps}")

print("===== 4. rules y320..345 fine census (both, thr 640/660) =====")
for nm, O in [("048", O48), ("049", O49)]:
    for thr in (620, 660):
        z = O[320:346, 300:840]; m = z.sum(axis=2) < thr
        rc = m.sum(axis=1)
        top = [(320 + i, int(c)) for i, c in enumerate(rc) if c > 300]
        print(f"  {nm} thr{thr}: {top}")

print("===== 5. 048 row-1: right-side '=' bars + green parens bows =====")
z = O48[160:180, 726:738]; m = z.sum(axis=2) < 500
ys, xs = np.where(m) if m.any() else (np.array([]), np.array([]))
if len(xs): print(f"  '='2 ink x{726+xs.min()}..{726+xs.max()} y{160+ys.min()}..{160+ys.max()}")
# green paren columns' bows: subcolumns found earlier (739-741, 762-764)
z = O48[150:196, 737:743]; m = (z[:, :, 1] > z[:, :, 0] + 12) & (z.sum(axis=2) < 700)
ys, xs = np.where(m)
if len(xs): print(f"  green lp paren ink x{737+xs.min()}..{737+xs.max()} y{150+ys.min()}..{150+ys.max()} npx={len(xs)}")
z = O48[150:196, 760:767]; m = (z[:, :, 1] > z[:, :, 0] + 12) & (z.sum(axis=2) < 700)
ys, xs = np.where(m)
if len(xs): print(f"  green rp paren ink x{760+xs.min()}..{760+xs.max()} y{150+ys.min()}..{150+ys.max()} npx={len(xs)}")
# left green column paren bows
z = O48[150:196, 379:386]; m = (z[:, :, 1] > z[:, :, 0] + 12) & (z.sum(axis=2) < 700)
ys, xs = np.where(m)
if len(xs): print(f"  left green lp ink x{379+xs.min()}..{379+xs.max()} y{150+ys.min()}..{150+ys.max()} npx={len(xs)}")
z = O48[150:196, 402:409]; m = (z[:, :, 1] > z[:, :, 0] + 12) & (z.sum(axis=2) < 700)
ys, xs = np.where(m)
if len(xs): print(f"  left green rp ink x{402+xs.min()}..{402+xs.max()} y{150+ys.min()}..{150+ys.max()} npx={len(xs)}")

print("===== 6. 049 wcol left-column (x377..410, r2 zone) for left-col anchor =====")
z = O49[207:265, 375:412]; m = z.sum(axis=2) < 500
ys, xs = np.where(m) if m.any() else (np.array([]), np.array([]))
if len(xs):
    print(f"  049 r2 left-col ink x{375+xs.min()}..{375+xs.max()} y{207+ys.min()}..{207+ys.max()} npx={len(xs)}")
