from PIL import Image
from collections import Counter
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_022.jpg").convert("RGB")
px = im.load()

def classify(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    if mx < 150 and mx - mn < 30:
        return "black"
    if r - g > 45 and r - b > 45:
        return "red"
    if g - r > 35 and g - b > 35:
        return "green"
    if b - r > 25 and b - g > 15:
        return "blue"
    return None

def ink(name, x0, y0, x1, y1):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            k = classify(*px[x, y])
            if k:
                c[k] += 1
    tot = sum(c.values())
    print(name, "ink px:", tot, {k: (v, str(round(100.0 * v / tot, 1)) + "%") for k, v in c.most_common()})

ink("row1 LEFT formula", 95, 122, 470, 180)
ink("row1 RIGHT formula", 605, 122, 825, 180)
ink("row2 LEFT formula", 95, 210, 470, 268)
ink("row2 RIGHT formula", 605, 210, 825, 268)
ink("row3 LEFT formula", 95, 297, 470, 360)
ink("row3 RIGHT formula", 605, 297, 825, 360)
ink("row4 LEFT formula", 95, 400, 330, 452)
ink("row4 RIGHT formula", 605, 400, 745, 452)
ink("TITLE", 185, 50, 700, 88)
ink("center arrows+labels", 480, 118, 560, 460)
