"""PIL measurements of unique_slides/slide_004.jpg (960x540 px -> 13.33x7.5 in, 1px=1pt)."""
from PIL import Image
import numpy as np

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_004.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = a.shape[:2]
P2I = 72.0


def in2px(v):
    return int(round(v * P2I))


def ink(x0, y0, x1, y1, bg=None, thr=45, gap=4):
    """Mask pixels differing from the local panel background; return ink runs in inches."""
    xs = slice(in2px(x0), in2px(x1))
    ys = slice(in2px(y0), in2px(y1))
    blk = a[ys, xs]
    if bg is None:
        # background = modal colour of the block
        vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
        bg = vals[cnts.argmax()]
    diff = np.abs(blk - np.array(bg)).max(axis=2)
    cols = np.where(diff.max(axis=0) > thr)[0] + in2px(x0)
    if len(cols) == 0:
        return [], bg
    runs, cur = [], [cols[0], cols[0]]
    for c in cols[1:]:
        if c - cur[1] <= gap + 1:
            cur[1] = c
        else:
            runs.append(tuple(cur))
            cur = [c, c]
    runs.append(tuple(cur))
    return runs, bg


def show(tag, y0, y1, x0, x1, minlen=3, **kw):
    runs, bg = ink(x0, y0, x1, y1, **kw)
    big = [r for r in runs if r[1] - r[0] >= minlen]
    span = (big[0][0] / P2I, big[-1][1] / P2I) if big else None
    print(f"{tag:<22} bg={tuple(bg)} first/last ink = {span[0]:.2f}-{span[1]:.2f} in"
          if span else
          f"{tag:<22} bg={tuple(bg)} NO INK")
    if len(big) > 12:
        print("      runs:", " ".join(f"{r[0]}-{r[1]}" for r in big[:40]))
    return big


print("== PANEL 1 (white) ==")
show("head", 1.55, 1.80, 0.9, 12.4)
show("line1", 1.90, 2.14, 0.9, 12.4)
show("line2", 2.25, 2.50, 0.9, 12.4)
print("== PANEL 2 (cream) ==")
show("head", 3.20, 3.46, 0.9, 12.4)
show("eqrow", 3.45, 4.08, 0.9, 12.4)
show("explanation", 3.55, 4.00, 3.4, 12.4)
show("positive", 4.12, 4.32, 0.9, 12.4)
print("== PANEL 3 (tan) ==")
show("head", 4.88, 5.12, 0.9, 12.4)
show("eqrow", 5.38, 6.02, 0.9, 12.4)
print("== BOTTOM ROW ==")
show("L box eq", 6.25, 6.56, 1.2, 6.7)
show("L box caption", 6.70, 6.95, 1.2, 6.7)
show("R box eq", 6.30, 6.68, 9.1, 12.25)
show("center caption", 6.28, 6.48, 6.8, 8.95)
show("arrow band", 6.49, 6.70, 6.8, 8.95)
show("rule band", 6.46, 6.52, 6.8, 9.4)

print("\n== colour samples ==")


def sample(tag, xin, yin):
    x, y = in2px(xin), in2px(yin)
    print(f"  {tag:<28} ({xin:.2f},{yin:.2f}) -> {tuple(a[y, x])}")


# trailing ">0" at the end of panel-1 conditional lines (last ink run ends ~11.29 in)
for x in [10.95, 11.05, 11.15, 11.25, 11.32]:
    sample("P1 line1 tail", x, 2.00)
for x in [10.90, 11.00, 11.10, 11.20, 11.30]:
    sample("P1 line2 tail", x, 2.36)
# panel 2 explanation: is "(W^T Xi)" underlined? probe below the text baseline
for y in [3.44, 3.46, 3.48, 3.50]:
    sample("P2 expl under-1", 6.10, y)
for y in [3.44, 3.46, 3.48]:
    sample("P2 expl under-2", 6.60, y)
# panel 2 sigma limit colour (below the sigma, around y 3.75-3.95)
for x in [1.60, 1.80, 2.00, 2.20, 2.40]:
    sample("P2 sigma limit", x, 3.86)
# panel 3 gradient equation sigma limit
for x in [7.30, 7.50, 7.70, 7.90]:
    sample("P3 sigma limit", x, 5.85)
# bottom left box sigma limit caption
for x in [3.70, 4.00, 4.30, 4.60]:
    sample("Lbox sigma limit", x, 6.82)

print("\n== bottom-row fills & borders ==")


def fill(tag, xin, yin):
    sample(tag, xin, yin)


fill("left box interior", 4.0, 6.60)
fill("left box interior2", 6.4, 6.28)
fill("gap tan", 7.90, 6.90)
fill("right box interior", 11.0, 6.60)
fill("panel3 tan", 7.90, 6.10)

