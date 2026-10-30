#!/usr/bin/env python3
"""PIL arbitration of attempt-8 judge claims for slide 004.
Claims: (A) inline bold 'Required' duplicated in where-block L4;
        (B) missing red underlines under X/W in where-block line 1 (Yhat=XW);
        (C) matrix delimiter shape: orig=vertical bars vs render=parens.
Ground truth: unique_slides/slide_004.jpg (960x540) vs render_8.png (2001x1125, s=2.0833).
"""
from PIL import Image
import numpy as np

ORIG = Image.open("unique_slides/slide_004.jpg").convert("RGB")
REND = Image.open("recreated_pptx/qa/slide004/render_8.png").convert("RGB")
S = REND.height / 540.0
print(f"orig {ORIG.size} render {REND.size} scale {S:.4f}")

def ink(arr, x0, y0, x1, y1, thresh=200):
    """dark-ink mask in slide-space box (orig coords); returns bool array orig-res."""
    box = arr[y0:y1, x0:x1]
    return (box.max(axis=2) < thresh)

def runs(mask, min_len=2):
    """column runs (start,end) of True columns."""
    cols = mask.any(axis=0)
    out, start = [], None
    for i, v in enumerate(cols):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= min_len:
                out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(cols)))
    return out

# ---- (A) where-block L4 band: y 332..364, x 550..900 (orig space) ----
print("\n=== (A) L4 'W is Model Parameter ...' band, orig y332..364 ===")
ao = np.asarray(ORIG); ar = np.asarray(REND)
mo = ink(ao, 550, 332, 900, 364, 190)
print("ORIG dark word runs (x+550):", [(a+550, b+550) for a, b in runs(mo, 3)])
mr = ink(ar, int(550*S), int(332*S), int(900*S), int(364*S), 190)
print("REND dark word runs (x/2.0833):", [(round((a+550*S)/S,1), round((b+550*S)/S,1)) for a, b in runs(mr, 6)])
# red mask (for the red W + underline + tags)
def redmask(arr, x0, y0, x1, y1):
    box = arr[y0:y1, x0:x1].astype(int)
    return (box[:,:,0] > 140) & (box[:,:,1] < 110) & (box[:,:,2] < 110)
ro = redmask(ao, 550, 332, 900, 364)
print("ORIG red runs:", [(a+550, b+550) for a, b in runs(ro, 2)])
rr = redmask(ar, int(550*S), int(332*S), int(900*S), int(364*S))
print("REND red runs:", [(round((a+550*S)/S,1), round((b+550*S)/S,1)) for a, b in runs(rr, 4)])
# per-word row profile of the dark blob between x600..770 orig (inline region)
print("ORIG L4 band rows with ink (y, count) x550..770:")
for y in range(332, 364):
    n = int(ink(ao, 550, y, 770, y+1, 190).sum())
    if n: print(f"  y{y}: {n}")

# ---- (B) line-1 underline band: y 268..284, x 495..690 ----
print("\n=== (B) underline band under 'Yhat = XW' (orig y268..284 x495..690) ===")
uo = ink(ao, 495, 268, 690, 284, 190)
uro = redmask(ao, 495, 268, 690, 284)
print("ORIG dark runs:", [(a+495, b+495) for a, b in runs(uo, 2)])
print("ORIG red runs:", [(a+495, b+495) for a, b in runs(uro, 2)])
ur = ink(ar, int(495*S), int(268*S), int(690*S), int(284*S), 190)
urr = redmask(ar, int(495*S), int(268*S), int(690*S), int(284*S))
print("REND dark runs:", [(round((a+495*S)/S,1), round((b+495*S)/S,1)) for a, b in runs(ur, 4)])
print("REND red runs:", [(round((a+495*S)/S,1), round((b+495*S)/S,1)) for a, b in runs(urr, 4)])
# where are the underlines for lines 2/3 (known: Y black x508..526, W red x566..584 at y277..283)
print("ORIG line-2/3 underline check y274..284 x495..690 red/dark:")
print("  dark:", [(a+495, b+495) for a, b in runs(ink(ao, 495, 274, 690, 285, 190), 2)])
print("  red :", [(a+495, b+495) for a, b in runs(redmask(ao, 495, 274, 690, 285), 2)])

# ---- (C) delimiter shape: Yvec equation orig x87..224 y131..182 ----
print("\n=== (C) left matrix delimiter profiles (Yvec box) ===")
# left delim band x84..106, right delim band x205..228; rows y128..186
for name, arr, sc in (("ORIG", ao, 1.0), ("REND", ar, S)):
    y0, y1 = int(128*sc), int(186*sc)
    for side, xlo, xhi in (("left", 82, 110), ("right", 203, 230)):
        band = arr[y0:y1, int(xlo*sc):int(xhi*sc)]
        m = band.max(axis=2) < 200
        redm = (band[:,:,0].astype(int) > 140) & (band[:,:,1] < 110) & (band[:,:,2] < 110)
        xmin_per_row = []
        for r in range(m.shape[0]):
            xs = np.where(m[r] | redm[r])[0]
            if len(xs):
                # ink position in orig-space units
                xmin_per_row.append((r/sc + 128, (xs.min()+xlo*sc)/sc))
        if xmin_per_row:
            ys = [p[0] for p in xmin_per_row]
            xs = [p[1] for p in xmin_per_row]
            top = xs[: max(1, len(xs)//5)]
            mid = xs[len(xs)//3 : 2*len(xs)//3]
            bot = xs[-max(1, len(xs)//5):]
            print(f"{name} {side}: rows={len(xs)} y{ys[0]:.0f}..{ys[-1]:.0f} "
                  f"xmin top~{min(top):.1f} mid~{min(mid):.1f} bot~{min(bot):.1f} "
                  f"span={(max(xs)-min(xs)):.1f}px")
        # red pixel count in the delimiter band
        print(f"   {name} {side}: red_px={int(redm.sum())} dark_px={int(m.sum())}")
