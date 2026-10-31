from PIL import Image
from collections import defaultdict

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
p = f"{V}/recreated_pptx/build/slide_029_diagram.png"
im = Image.open(p).convert("RGB")
w, h = im.size
print(f"diagram png {im.size} aspect={w/h:.4f}")

# panel is placed 6.61 x 3.43 in -> aspect 1.927
print(f"expected aspect for 6.61x3.43 = {6.61/3.43:.4f}")

# find dark-red vertical bars in the png
def isdk(c):
    r, g, b = c
    return r > 140 and r > g + 60 and r > b + 60 and g < 110

cnt = defaultdict(int)
for y in range(h):
    for x in range(w):
        if isdk(im.getpixel((x, y))):
            cnt[x] += 1
xs = sorted(x for x, n in cnt.items() if n > h * 0.3)
if xs:
    print(f"dark-red widespan columns x {xs[0]}-{xs[-1]} of {w} -> in-slide x = {0.94 + xs[0]/w*6.61:.2f}..{0.94 + xs[-1]/w*6.61:.2f} in")

# green-filled class boxes
cnt = defaultdict(int)
for y in range(h):
    for x in range(w):
        c = im.getpixel((x, y))
        if 200 < c[0] < 245 and 215 < c[1] < 250 and 180 < c[2] < 235 and c[1] - c[0] > 8 and c[1] - c[2] > 12:
            cnt[x] += 1
xs = sorted(x for x, n in cnt.items() if n > 8)
if xs:
    print(f"pale-green class boxes x {xs[0]}-{xs[-1]} of {w} -> in-slide x = {0.94 + xs[0]/w*6.61:.2f}..{0.94 + xs[-1]/w*6.61:.2f} in")

# beige panel extent
cnt = defaultdict(int)
for y in range(h):
    for x in range(w):
        c = im.getpixel((x, y))
        if 200 < c[0] < 250 and 190 < c[1] < 242 and 150 < c[2] < 218 and c[0] - c[2] > 16:
            cnt[x] += 1
xs = sorted(x for x, n in cnt.items() if n > h * 0.8)
if xs:
    print(f"beige panel x {xs[0]}-{xs[-1]} of {w}")
# y extent of beige
cnt2 = defaultdict(int)
for x in range(0, w, 2):
    for y in range(h):
        c = im.getpixel((x, y))
        if 200 < c[0] < 250 and 190 < c[1] < 242 and 150 < c[2] < 218 and c[0] - c[2] > 16:
            cnt2[y] += 1
ys = sorted(y for y, n in cnt2.items() if n > w * 0.3)
if ys:
    print(f"beige panel y {ys[0]}-{ys[-1]} of {h}")

# Where do white output boxes sit
cnt = defaultdict(int)
for y in range(h):
    for x in range(w):
        if min(im.getpixel((x, y))) > 240:
            cnt[x] += 1
xs = sorted(x for x, n in cnt.items() if n > 12)
if xs:
    print(f"white-content x {xs[0]}-{xs[-1]} of {w} -> in-slide {0.94 + xs[0]/w*6.61:.2f}..{0.94 + xs[-1]/w*6.61:.2f} in")
