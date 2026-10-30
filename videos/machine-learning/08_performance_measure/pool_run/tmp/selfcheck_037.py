"""Pre-judge PIL self-checks: render_1.png (150dpi, 2000x1125) vs original (960x540)."""
from PIL import Image
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
orig = Image.open(f"{NS}/unique_slides/slide_037.jpg").convert("RGB")
rend = Image.open(f"{NS}/recreated_pptx/qa/slide037/render_1.png").convert("RGB")
print("render size:", rend.size)
S = 150 / 72.0  # render px per original px
r = rend.resize((960, 540), Image.LANCZOS)
op, rp = orig.load(), r.load()
W = H = 960

def bbox(im_px, pred, x0=0, y0=0, x1=960, y1=540):
    bx0, by0, bx1, by1 = 960, 540, -1, -1
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(im_px[x, y]):
                n += 1
                bx0 = min(bx0, x); bx1 = max(bx1, x); by0 = min(by0, y); by1 = max(by1, y)
    return (bx0, by0, bx1, by1, n) if n else None

dark = lambda p: sum(p) < 330
print("ORIG dark bbox:", bbox(op, dark))
print("REND dark bbox:", bbox(rp, dark))

# house frame check on render: red-ish frame at 0.15in -> px 0.15*72=10.8 (in 960 space)
red = lambda p: p[0] > 130 and p[0] > p[1] + 70 and p[0] > p[2] + 70
print("REND red frame bbox:", bbox(rp, red))
# badge: yellow at house pos 12.48..12.98in -> 898..934 px, y 21.6..57.6
yel = lambda p: p[0] > 200 and p[1] > 185 and p[2] < 170
print("REND badge bbox:", bbox(rp, yel, 880, 10, 950, 70))
# plot box: light blue region
lb = lambda p: abs(p[0]-240) < 14 and abs(p[1]-248) < 12 and p[2] > 245
print("ORIG plot bbox:", bbox(op, lb, 200, 180, 700, 540))
print("REND plot bbox:", bbox(rp, lb, 200, 180, 700, 540))
# white text box
wh = lambda p: p[0] > 243 and p[1] > 246 and p[2] > 243
print("ORIG white box:", bbox(op, wh, 80, 85, 850, 220))
print("REND white box:", bbox(rp, wh, 80, 85, 850, 220))
# text bands dark rows in render, y 90..215
def bands(p, y0, y1, min_n=8):
    out = []
    s = None
    for y in range(y0, y1):
        n = sum(1 for x in range(70, 890) if dark(p[x, y]))
        if n >= min_n:
            if s is None: s = y
        else:
            if s is not None: out.append((s, y - 1)); s = None
    if s is not None: out.append((s, y1 - 1))
    m = []
    for b in out:
        if m and b[0] - m[-1][1] <= 4: m[-1] = (m[-1][0], b[1])
        else: m.append(b)
    return m
print("ORIG text bands 90..215:", bands(op, 90, 215))
print("REND text bands 90..215:", bands(rp, 90, 215))
# plot ink (colored) bbox render vs orig
mag = lambda p: p[0] > 100 and p[2] > 100 and p[1] < p[0] - 50 and p[1] < p[2] - 50
grn = lambda p: p[1] > 100 and p[1] > p[0] + 50 and p[1] > p[2] + 40
print("ORIG magenta:", bbox(op, mag, 250, 210, 650, 520))
print("REND magenta:", bbox(rp, mag, 250, 210, 650, 520))
print("ORIG green:", bbox(op, grn, 250, 210, 650, 520))
print("REND green:", bbox(rp, grn, 250, 210, 650, 520))
# containment: any non-bg ink outside house frame (frame at 10.8px..948.9px, y 10.8..530.8)?
bgish = lambda p: abs(p[0]-232) < 14 and abs(p[1]-232) < 14 and abs(p[2]-230) < 14
outside = []
for y in range(0, 540):
    for x in range(0, 960):
        if not (10.8 <= x <= 949 and 10.8 <= y <= 531):
            if not bgish(rp[x, y]) and sum(rp[x, y]) < 700:
                outside.append((x, y))
print("REND ink outside house frame:", len(outside), outside[:10])
