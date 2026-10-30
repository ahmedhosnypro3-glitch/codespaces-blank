"""Measure pink formula-box fill color + extents, and per-text-band color classification."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
im = Image.open(V + "unique_slides/slide_021.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
P = lambda px: px / 72.0


def sample_region(y0, y1, x0, x1, name):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    # dominant light color
    from collections import Counter
    cnt = Counter(map(tuple, (sub // 8 * 8)))
    print(f"  {name} dominant colors: {cnt.most_common(4)}")


# Sample interiors of the 4 formula boxes
sample_region(62, 100, 130, 320, "TL interior")
sample_region(62, 100, 570, 720, "TR interior")
sample_region(290, 335, 110, 420, "BL interior")
sample_region(300, 330, 600, 800, "BR interior")

print("\n=== PINK BOX EXTENTS via light-red fill mask (adaptive) ===")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
# fill is light and reddish: r-g between 8 and 40, r-b between 8 and 40, g,b > 215
mask = (r > 240) & (r - g > 6) & (r - g < 45) & (r - b > 6) & (r - b < 45) & (g > 210) & (b > 210)
for name, y0, y1, x0, x1 in [("TL", 40, 115, 100, 460), ("TR", 40, 115, 540, 780),
                             ("BL", 270, 350, 80, 470), ("BR", 270, 350, 570, 860)]:
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print(f"  {name}: none"); continue
    print(f"  {name}: x {xs.min()+x0}-{xs.max()+x1-(x1-x0)+0} -> in {P(xs.min()+x0):.3f}-{P(xs.max()+x0):.3f} |"
          f" y {ys.min()+y0}-{ys.max()+y0} -> in {P(ys.min()+y0):.3f}-{P(ys.max()+y0):.3f}")

print("\n=== TEXT ROW BANDS + COLOR per band, for each formula box ===")
def classify(px):
    rr, gg, bb = px
    if rr > 150 and rr - gg > 40 and rr - bb > 40: return "RED"
    if bb > 130 and bb - rr > 40: return "BLUE"
    if gg > 90 and gg - rr > 25 and gg - bb > 25: return "GREEN"
    if rr < 110 and gg < 110 and bb < 110: return "BLACK"
    return "?"


def text_bands(x0, x1, y0, y1, name, bgpad=8):
    sub = a[y0:y1, x0:x1]
    # local bg = most common color in the region
    from collections import Counter
    bg = Counter(map(tuple, sub.reshape(-1, 3) // 6 * 6)).most_common(1)[0][0]
    ink = (np.abs(sub - bg).max(axis=2) > 45)
    rs = ink.sum(axis=1)
    out = []
    for y in range(y1 - y0):
        if rs[y] > 1:
            out.append(y + y0)
    seg = []
    for y in out:
        if not seg or y - seg[-1][1] > 3:
            seg.append([y, y])
        else:
            seg[-1][1] = y
    print(f"  {name} bg={bg}: {len(seg)} ink bands")
    for s in seg:
        rows = ink[s[0]-y0:s[1]-y0+1]
        cols = np.where(rows.any(axis=0))[0]
        # color census over ink pixels
        region = a[s[0]:s[1]+1, x0:x1]
        sel = rows
        px = region[sel]
        from collections import Counter
        cc = Counter(classify(p) for p in px)
        print(f"     band y {s[0]}-{s[1]} (in {P(s[0]):.3f}-{P(s[1]):.3f}) "
              f"x {cols.min()+x0}-{cols.max()+x0}: {cc.most_common(3)}")


text_bands(115, 340, 50, 110, "TL formula")
text_bands(552, 770, 50, 110, "TR formula")
text_bands(95, 435, 280, 345, "BL formula")
text_bands(590, 820, 280, 345, "BR formula")

print("\n=== GRAPH INTERNAL: axis span & tick label positions (TL) ===")
# inside TL graph x 124..396, y 112..272
sub = a[112:272, 124:396]
dark = (sub.max(axis=2) < 150)
rs = dark.sum(axis=1); cs = dark.sum(axis=0)
print("  rows >50% dark:", [(y+112, int(rs[y])) for y in range(160) if rs[y] > 80][:10])
print("  cols >50% dark:", [(x+124, int(cs[x])) for x in range(272) if cs[x] > 80][:10])
