# Slide 025 BL final census: text bands, arrow blobs, y417 line true extent.
# Run: python3 measure_7_bl.py
import numpy as np
from PIL import Image

DECK = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
renF = np.asarray(Image.open(DECK + "/recreated_pptx/qa/slide_025/render_3.png").convert("RGB")).astype(int)
ren = np.asarray(Image.fromarray(renF.astype(np.uint8)).resize((960, 540), Image.BOX)).astype(int)

BL = (83, 290, 376, 527)   # measured figure box (inclusive)
x0, y0, x1, y1 = BL
ix0, iy0, ix1, iy1 = x0 + 8, y0 + 8, x1 - 8, y1 - 8


def m_dark_loose(img):     # catches antialiased dark text
    return (img.max(axis=2) < 135) & (img.min(axis=2) < 120)


def m_red_loose(img):      # catches maroon/C00000-family + jet red
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    return (r > 110) & (r - g > 45) & (r - b > 45) & (g < 140)


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


def label(mask, min_area=6):
    H, W = mask.shape
    seen = np.zeros((H, W), dtype=bool)
    out = []
    ys, xs = np.where(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        stack = [(y0, x0)]; seen[y0, x0] = True; pix = []
        while stack:
            y, x = stack.pop(); pix.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; stack.append((ny, nx))
        if len(pix) >= min_area:
            ys2 = [p[0] for p in pix]; xs2 = [p[1] for p in pix]
            out.append((len(pix), min(xs2), max(xs2), min(ys2), max(ys2)))
    return sorted(out, key=lambda t: -t[0])


print("=== BL dark-ink row bands (loose mask, px per row, rows >=8px) ===")
for tag, img in (("orig", orig), ("render", ren)):
    dk = m_dark_loose(img)[iy0:iy1 + 1, ix0:ix1 + 1]
    rows = dk.sum(axis=1)
    print("  %s total dark px %d" % (tag, dk.sum()))
    band, s = None, None
    for y in range(len(rows)):
        v = rows[y]
        if band is None and v >= 8:
            band, s = True, y
        elif band and v < 8:
            print("    y%d..%d  max %d px" % (s + iy0, y - 1 + iy0, rows[s:y].max())); band = None
    if band:
        print("    y%d..%d  max %d px" % (s + iy0, iy1, rows[s:].max()))

print("\n=== BL red-ink blobs (loose red, area>=10, inside figure) ===")
for tag, img in (("orig", orig), ("render", ren)):
    rd = m_red_loose(img)[iy0:iy1 + 1, ix0:ix1 + 1]
    blobs = label(rd, 10)
    print("  %s red px %d, %d blobs:" % (tag, rd.sum(), len(blobs)))
    for c in blobs[:20]:
        w = c[2] - c[1] + 1; h = c[4] - c[3] + 1
        print("    x%d..%d y%d..%d  a=%d  %dx%d %s" % (
            c[1] + ix0, c[2] + ix0, c[3] + iy0, c[4] + iy0, c[0], w, h,
            "LINE-ISH" if w >= 3 * h else ("ARROW-ISH" if w <= 2.5 * h and h >= 6 else "blob")))

print("\n=== BL rows 415..421: full loose-red extent per row (orig vs render) ===")
for tag, img in (("orig", orig), ("render", ren)):
    rd = m_red_loose(img)
    for y in range(414, 423):
        rr = runs(rd[y, x0:x1 + 1], 8)
        if rr:
            print("  %s y=%d: %s" % (tag, y, [(a + x0, b + x0) for a, b in rr]))
