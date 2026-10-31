from PIL import Image
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_022.jpg").convert("RGB")
px = im.load()

def cls(c):
    r, g, b = c
    if r - b > 20 and r > 235:
        return "PINK"
    if g - r > 3 and b - r < 20 and r > 245:
        return "YEL"
    if r - g < 12 and g - b < 15 and r > 245:
        return "WHT"
    if r - g > 25 and r - b > 25:
        return "RED"
    if b - r > 15 and b - g > 8:
        return "BLU"
    return "OTH"

for y, name in [(150, "row1"), (245, "row2"), (340, "row3"), (430, "row4")]:
    seq = [cls(px[x, y]) for x in range(70, 895)]
    out = []
    start = 0
    for i in range(1, len(seq)):
        if seq[i] != seq[start]:
            if i - start >= 3:
                out.append((70 + start, 70 + i - 1, seq[start]))
            start = i
    if len(seq) - start >= 3:
        out.append((70 + start, 70 + len(seq) - 1, seq[-1]))
    print("== y=%d %s ==" % (y, name))
    for a, b, c in out:
        print("   x %4d-%4d  n=%3d  %s" % (a, b, b - a + 1, c))
