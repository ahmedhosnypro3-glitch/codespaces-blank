from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
w, h = im.size
SW, SH = 13.33, 7.5
px = im.load()

def tin(xf):
    return round(xf * SW, 2)

def xprofile(yf, pred, label, thresh=1):
    y = int(yf * h)
    xs = [x for x in range(w) if pred(px[(x, y)])]
    if not xs:
        print(f"  {label}: none")
        return
    runs = []
    for x in xs:
        if runs and x - runs[-1][-1] <= 4:
            runs[-1].append(x)
        else:
            runs.append([x])
    print(f"  {label} @y={yf*h/SH:.2f}in: " + ", ".join(
        f"{tin(r[0]/w)}-{tin(r[-1]/w)}in (len {(r[-1]-r[0])/w*SW:.2f})" for r in runs if len(r) > thresh))

def yprofile(xf, pred, label):
    x = int(xf * w)
    ys = [y for y in range(h) if pred(px[(x, y)])]
    if not ys:
        print(f"  {label}: none")
        return
    runs = []
    for y in ys:
        if runs and y - runs[-1][-1] <= 4:
            runs[-1].append(y)
        else:
            runs.append([y])
    print(f"  {label} @x={tin(xf)}in: " + ", ".join(
        f"{r[0]/h*SH:.2f}-{r[-1]/h*SH:.2f}in (len {(r[-1]-r[0])/h*SH:.2f})" for r in runs if len(r) > 1))

lb = lambda c: 200 < c[0] < 245 and 220 < c[1] < 250 and 240 < c[2] < 256 and c[1] - c[0] > 8
lg = lambda c: 215 < c[0] < 250 and 230 < c[1] < 252 and 205 < c[2] < 245 and c[1] - c[0] > 8
mag = lambda c: c[0] > 180 and c[1] > 115 and c[2] > 180 and c[0] - c[1] > 30 and c[2] - c[1] > 30
white = lambda c: min(c) > 245
graybd = lambda c: abs(c[0] - c[1]) < 6 and abs(c[1] - c[2]) < 6 and 100 < c[0] < 170
py = lambda c: c[0] > 245 and c[1] > 245 and 200 < c[2] < 235

print("== LAYER CALLOUT boxes (light-blue / light-green) ==")
for xf in [0.24, 0.26, 0.28, 0.42, 0.44, 0.46]:
    yprofile(xf, lb, f"lightblue x={tin(xf)}")
for xf in [0.42, 0.44, 0.46, 0.48]:
    yprofile(xf, lg, f"lightgreen x={tin(xf)}")

print("\n== callout box x extents ==")
for yf in [0.735, 0.75, 0.77, 0.79]:
    xprofile(yf, lb, "lightblue")
for yf in [0.735, 0.75, 0.77]:
    xprofile(yf, lg, "lightgreen")

print("\n== ARROWS (blue/green outlines above callouts) ==")
blue = lambda c: c[2] > c[0] + 40 and c[2] > 140 and c[0] < 120
green = lambda c: c[1] > c[0] + 40 and c[1] > c[2] + 40 and c[1] > 110
for yf in [0.66, 0.68, 0.70, 0.71, 0.72]:
    xprofile(yf, blue, "blue-arrow")
for yf in [0.66, 0.68, 0.70, 0.71, 0.72]:
    xprofile(yf, green, "green-arrow")

print("\n== MAGENTA boxes + dashed arrow (row y=1.55) ==")
xprofile(0.207, mag, "magenta@y0.207")
xprofile(0.20, mag, "magenta@y0.20")
xprofile(0.22, mag, "magenta@y0.22")
for xf in [0.08, 0.10, 0.67, 0.69]:
    yprofile(xf, mag, f"magenta x={tin(xf)}")

print("\n== BOTTOM ROW box borders (gray #808080) ==")
for yf in [0.865, 0.88, 0.91, 0.94]:
    xprofile(yf, graybd, "gray-border")
for yf in [0.845, 0.86]:
    xprofile(yf, py, "pale-yellow")

print("\n== NOTE BOX (white, red border) ==")
for yf in [0.49, 0.51, 0.53, 0.55, 0.57]:
    xprofile(yf, white, "white")
print("  red borders:")
for yf in [0.485, 0.49, 0.58]:
    xprofile(yf, lambda c: c[0] > 120 and c[0] - c[1] > 45 and c[0] - c[2] > 45, "red")

print("\n== LEGEND BOX (light beige, red border) ==")
for yf in [0.24, 0.30, 0.42]:
    xprofile(yf, lambda c: 235 < c[0] < 252 and 220 < c[1] < 240 and 200 < c[2] < 228, "lbeige")
for yf in [0.24, 0.42]:
    xprofile(yf, lambda c: c[0] > 120 and c[0] - c[1] > 45 and c[0] - c[2] > 45, "red")
