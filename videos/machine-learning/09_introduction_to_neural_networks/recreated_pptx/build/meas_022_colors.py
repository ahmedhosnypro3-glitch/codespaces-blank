from PIL import Image
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_022.jpg").convert("RGB")
print("size", im.size)
from collections import Counter

def region(name, x0, y0, x1, y1, topn=6):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[im.getpixel((x, y))] += 1
    tot = sum(c.values())
    print(name, "total", tot)
    for col, n in c.most_common(topn):
        print("   #%02X%02X%02X" % col, n, round(100.0*n/tot,1), "%")

# left panel row1 interior (v2: x82-455, y122-180) sample band below text lines
region("L1 interior", 90, 165, 450, 178)
region("L1 upper", 90, 124, 450, 135)
# left panel row2 (y 210-268)
region("L2 interior", 90, 253, 450, 265)
# left panel row3 (y 297-360)
region("L3 interior", 90, 345, 450, 357)
# left panel row4 (y 400-452), panel x82-328
region("L4 interior", 90, 440, 320, 452)
# right panels row1 x598-825 y122-180
region("R1 interior", 605, 165, 820, 178)
region("R2 interior", 605, 253, 820, 265)
region("R3 interior", 605, 345, 820, 357)
region("R4 interior", 605, 440, 738, 452)
# container interior between panels (white?)
region("gap between L1 and R1", 470, 124, 590, 178)
# outside container (background)
region("outside left of container", 5, 200, 60, 480)
region("outside top band", 60, 12, 400, 45)
# frame colors
print("outer frame top edge px:", [im.getpixel((x, 41)) for x in (40, 100, 300)])
print("inner blue frame left edge:", [im.getpixel((68, y)) for y in (220, 300, 400)])
print("badge center:", im.getpixel((827, 70)), im.getpixel((827, 62)))
