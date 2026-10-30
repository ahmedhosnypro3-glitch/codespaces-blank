# Slide 025 K=2-finding adjudication census (orig vs render_3, 960x540).
# Pure numpy (no scipy). Run: python3 measure_5_adjudicate.py
import numpy as np
from PIL import Image

DECK = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_025.jpg"
REND = DECK + "/recreated_pptx/qa/slide_025/render_3.png"

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
renF = np.asarray(Image.open(REND).convert("RGB")).astype(int)
ren = np.asarray(Image.fromarray(renF.astype(np.uint8)).resize((960, 540), Image.BOX)).astype(int)


def masks(img):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    white = (r > 235) & (g > 235) & (b > 235)
    ink = (r < 200) | (g < 200) | (b < 200)          # grid (#DDD=221) / halos excluded
    dark = (r < 100) & (g < 100) & (b < 100)
    redstroke = (r > 150) & (r < 235) & (g < 70) & (b < 70) & (r - g > 80)
    jetred = (r > 230) & (g < 95) & (b < 95)          # saturated jet red core
    sat = (img.max(axis=2) - img.min(axis=2)) > 45    # jet-chroma
    return dict(white=white, ink=ink, dark=dark, redstroke=redstroke,
                jetred=jetred, sat=sat)


def runs(v, minlen):
    xs = np.where(v)[0]
    if not len(xs):
        return []
    out, s = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] != xs[i - 1] + 1:
            out.append((s, xs[i - 1])); s = xs[i]
    out.append((s, xs[-1]))
    return [q for q in out if q[1] - q[0] + 1 >= minlen]


COMP = []


def label(mask, min_area=6):
    """8-connected components; returns [(id, area, x0, x1, y0, y1), ...]."""
    global COMP
    COMP = []
    H, W = mask.shape
    ys, xs = np.where(mask)
    seen = np.zeros((H, W), dtype=bool)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        stack = [(y0, x0)]
        seen[y0, x0] = True
        pix = []
        while stack:
            y, x = stack.pop()
            pix.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
        if len(pix) >= min_area:
            ys2 = [p[0] for p in pix]; xs2 = [p[1] for p in pix]
            COMP.append((len(COMP), len(pix), min(xs2), max(xs2), min(ys2), max(ys2)))
    return sorted(COMP, key=lambda t: -t[1])


QUADS = {"TL": (54, 45, 470, 292), "TR": (470, 45, 903, 320),
         "BL": (54, 292, 470, 539), "BR": (470, 320, 903, 539)}

mo, mr = masks(orig), masks(ren)


def redrect(m, x0, y0, x1, y1):
    sub = np.zeros_like(m["redstroke"]); sub[y0:y1 + 1, x0:x1 + 1] = True
    rs = m["redstroke"] & sub
    tops, bots, lefts, rights = [], [], [], []
    for y in range(y0, y1 + 1):
        for (s, e) in runs(rs[y], 60):
            (tops if y < (y0 + y1) // 2 else bots).append(y)
    for x in range(x0, x1 + 1):
        for (s, e) in runs(rs[:, x], 40):
            (lefts if x < (x0 + x1) // 2 else rights).append(x)

    def pick(lst):
        return int(np.median(lst)) if lst else None
    return pick(tops), pick(lefts), pick(rights), pick(bots)


print("=== RED RECT per quadrant (top/left/right/bottom; frame px) ===")
for name, (x0, y0, x1, y1) in QUADS.items():
    ro = redrect(mo, x0, y0, x1, y1)
    rr = redrect(mr, x0, y0, x1, y1)
    print("  %s orig %s | render %s" % (name, ro, rr))

print("\n=== SURFACE SILHOUETTE (ink<200 inside red rect, inset 6px) ===")
for name, (x0, y0, x1, y1) in QUADS.items():
    ro = redrect(mo, x0, y0, x1, y1); rr = redrect(mr, x0, y0, x1, y1)
    for tag, m, rc in (("orig", mo, ro), ("render", mr, rr)):
        if None in rc:
            print("  %s %-6s rect missing" % (tag, name)); continue
        t, l, rt, b = rc
        ix0, iy0, ix1, iy1 = l + 6, t + 6, rt - 6, b - 6
        sub = np.zeros_like(m["ink"]); sub[iy0:iy1 + 1, ix0:ix1 + 1] = True
        ink = m["ink"] & sub
        satc = m["sat"] & sub
        ys, xs = np.where(ink)
        bb = (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())) if len(xs) else None
        print("  %s %-6s ink bbox %s area %d (fill %.1f%%) | sat px %d"
              % (tag, name, bb, ink.sum(), 100.0 * ink.sum() / max(1, (ix1 - ix0 + 1) * (iy1 - iy0 + 1)), satc.sum()))

print("\n=== JET-RED CORE BLOBS (area>=40, inside rect) ===")
for name, (x0, y0, x1, y1) in QUADS.items():
    ro = redrect(mo, x0, y0, x1, y1); rr = redrect(mr, x0, y0, x1, y1)
    for tag, m, rc in (("orig", mo, ro), ("render", mr, rr)):
        if None in rc:
            continue
        t, l, rt, b = rc
        sub = np.zeros_like(m["jetred"]); sub[t + 5:b - 4, l + 5:rt - 4] = True
        blobs = label(m["jetred"] & sub, 40)
        print("  %s %-6s %d blobs (x0..x1,y0..y1,area): %s"
              % (tag, name, len(blobs), [(c[2], c[3], c[4], c[5], c[1]) for c in blobs[:8]]))

print("\n=== DARK BLOBS (area>=20) — annotation text / GD path, inside rect ===")
for name in ("BL", "BR"):
    x0, y0, x1, y1 = QUADS[name]
    ro = redrect(mo, x0, y0, x1, y1); rr = redrect(mr, x0, y0, x1, y1)
    for tag, m, rc in (("orig", mo, ro), ("render", mr, rr)):
        if None in rc:
            continue
        t, l, rt, b = rc
        sub = np.zeros_like(m["dark"]); sub[t + 5:b - 4, l + 5:rt - 4] = True
        blobs = label(m["dark"] & sub, 20)
        print("  %s %-4s %d blobs (x0..x1,y0..y1,area):" % (tag, name, len(blobs)))
        for c in blobs[:16]:
            print("      x%d..%d y%d..%d  a=%d" % (c[2], c[3], c[4], c[5], c[1]))

print("\n=== RED-STROKE BLOBS inside BL/BR rects (arrows?) — red, area>=15 ===")
for name in ("BL", "BR"):
    x0, y0, x1, y1 = QUADS[name]
    ro = redrect(mo, x0, y0, x1, y1)
    t, l, rt, b = ro
    sub = np.zeros_like(mo["redstroke"]); sub[t + 5:b - 4, l + 5:rt - 4] = True
    blobs = label(mo["redstroke"] & sub, 15)
    print("  orig %-4s %d red blobs (x0..x1,y0..y1,area):" % (name, len(blobs)))
    for c in blobs[:16]:
        print("      x%d..%d y%d..%d  a=%d" % (c[2], c[3], c[4], c[5], c[1]))

print("\n=== BL long red horizontals by row-scan (>=30px runs) ===")
x0, y0, x1, y1 = QUADS["BL"]
ro = redrect(mo, x0, y0, x1, y1)
t, l, rt, b = ro
sub = np.zeros_like(mo["redstroke"]); sub[t + 4:b - 3, l + 2:rt - 1] = True
rs = mo["redstroke"] & sub
for y in range(t + 4, b - 2):
    rr = runs(rs[y], 30)
    if rr:
        print("  orig row %d: %s" % (y, rr))
