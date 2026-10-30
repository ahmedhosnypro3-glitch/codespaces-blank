#!/usr/bin/env python3
"""render_26 PIL verification vs slide-019 forensic targets (pil_probe_a25 tables)."""
import sys
from PIL import Image

REND = sys.argv[1] if len(sys.argv) > 1 else "render_26.png"
SX = SY = 2000 / 960  # 2.0833

im = Image.open(REND).convert("RGB")
print(f"size={im.size}")


def to_r(v):
    return int(round(v * SX))


def ink_bbox(img, x0, y0, x1, y1, pred):
    """bbox of matching px in slide-space window (x0,y0,x1,y1), returns slide coords."""
    box = img.crop((to_r(x0), to_r(y0), to_r(x1), to_r(y1)))
    px = box.load()
    xs, ys = [], []
    for yy in range(box.size[1]):
        for xx in range(box.size[0]):
            if pred(px[xx, yy]):
                xs.append(xx)
                ys.append(yy)
    if not xs:
        return None
    return (
        x0 + min(xs) / SX, y0 + min(ys) / SY,
        x0 + max(xs) / SX, y0 + max(ys) / SY,
    )


def is_dark(p):
    return sum(p) < 300


def is_blue(p):
    r, g, b = p
    return b > 110 and b > r + 40 and g < b


def is_red(p):
    r, g, b = p
    return r > 120 and r > g + 50 and r > b + 50


def is_green(p):
    r, g, b = p
    return g > 90 and g > r + 30 and g > b + 20


def is_yellow(p):
    r, g, b = p
    return r > 200 and g > 190 and b < 140


fails = []


def check(name, got, want, tol):
    if got is None:
        print(f"FAIL {name}: no ink")
        fails.append(name)
        return
    d = max(abs(got[i] - want[i]) for i in range(4))
    ok = d <= tol
    print(f"{'ok  ' if ok else 'FAIL'} {name}: got ({got[0]:.1f},{got[1]:.1f})-({got[2]:.1f},{got[3]:.1f}) want {want} d={d:.1f} tol={tol}")
    if not ok:
        fails.append(name)


# digit rows: (color-pred, orig target bbox)
rows = [
    ("g1_11", is_blue, (91, 219, 108, 233)),
    ("g1_3", is_blue, (95, 244, 104, 259)),
    ("g1_22", is_green, (92, 269, 107, 284)),
    ("g2_30", is_red, (85, 326, 104, 341)),
    ("g2_3", is_blue, (90, 351, 99, 366)),
    ("g2_22", is_green, (85, 376, 104, 391)),
    ("g3_60", is_red, (85, 429, 104, 444)),
    ("g3_3", is_blue, (90, 455, 98, 470)),
    ("g3_22", is_green, (84, 480, 104, 495)),
]
for name, pred, want in rows:
    check(name, ink_bbox(im, 60, want[1] - 7, 130, want[3] + 7, pred), want, 4)

# subscript s
check("s_sub", ink_bbox(im, 92, 200, 103, 216, is_blue), (95, 205, 99, 211), 4)

# thin arcs: blue ink column extents around each delimiter (expect ~2-3px wide ink)
arcs = [
    ("g1_left", (80, 210, 90, 292)), ("g1_right", (110, 210, 120, 292)),
    ("g2_left", (74, 315, 84, 400)), ("g2_right", (105, 315, 115, 400)),
    ("g3_left", (74, 419, 84, 505)), ("g3_right", (104, 419, 114, 505)),
]
for name, w in arcs:
    got = ink_bbox(im, *w, is_blue)
    if got is None:
        print(f"FAIL {name}: no arc ink")
        fails.append(name)
    else:
        wid = got[2] - got[0]
        ok = wid <= 5.5
        print(f"{'ok  ' if ok else 'FAIL'} {name}: ink x{got[0]:.1f}..{got[2]:.1f} (w{wid:.1f}) y{got[1]:.1f}..{got[3]:.1f}")
        if not ok:
            fails.append(name)

# yellow patch extent per band (orig x76..116)
for name, y0, y1 in [("patch_g1", 264, 292), ("patch_g2", 371, 399), ("patch_g3", 475, 503)]:
    got = ink_bbox(im, 60, y0, 140, y1, is_yellow)
    check(name, got, (76, y0 + 2, 116, y1 - 2), 5)

print("RESULT:", "ALL PASS" if not fails else f"FAILS: {fails}")
