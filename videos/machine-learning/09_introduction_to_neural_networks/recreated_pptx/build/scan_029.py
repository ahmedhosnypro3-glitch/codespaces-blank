from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{V}/unique_slides/slide_029.jpg"
REND = f"{V}/recreated_pptx/build/slide_029_rendered-1.png"

def is_darkred(c):
    r, g, b = c
    return r > 140 and r > g + 60 and r > b + 60 and g < 110

def is_beige(c):
    r, g, b = c
    return 200 < r < 245 and 185 < g < 230 and 150 < b < 200 and (r - b) > 20

def is_green(c):
    r, g, b = c
    return g > r + 25 and g > b + 25 and g > 100

def scan(path, label):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    print(f"=== {label} {im.size} ===")

    # dark red column profile on a mid-height band
    cols = []
    for x in range(w):
        cnt = 0
        for y in range(int(h * 0.30), int(h * 0.70)):
            if is_darkred(im.getpixel((x, y))):
                cnt += 1
        if cnt > (h * 0.15):
            cols.append(x)
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 2:
            groups[-1].append(x)
        else:
            groups.append([x])
    print(" dark-red vertical bands (x frac):",
          [(round(g[0]/w, 3), round(g[-1]/w, 3)) for g in groups])

    # beige column profile
    cols = []
    for x in range(w):
        cnt = sum(1 for y in range(int(h * 0.25), int(h * 0.72), 2) if is_beige(im.getpixel((x, y))))
        if cnt > 40:
            cols.append(x)
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 2:
            groups[-1].append(x)
        else:
            groups.append([x])
    print(" beige bands (x frac):", [(round(g[0]/w, 3), round(g[-1]/w, 3)) for g in groups])

    # green bands (class boxes + callout)
    cols = []
    for x in range(w):
        cnt = sum(1 for y in range(0, h, 3) if is_green(im.getpixel((x, y))))
        if cnt > 25:
            cols.append(x)
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
    print(" green bands (x frac):", [(round(g[0]/w, 3), round(g[-1]/w, 3)) for g in groups])

    # pale yellow (badge + formula boxes)
    cols = []
    for x in range(w):
        cnt = sum(1 for y in range(0, h, 3) if (lambda c: c[0] > 240 and c[1] > 240 and c[2] < 220 and c[2] > 150)(im.getpixel((x, y))))
        if cnt > 20:
            cols.append(x)
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
    print(" pale-yellow bands (x frac):", [(round(g[0]/w, 3), round(g[-1]/w, 3)) for g in groups])

    # magenta input/target boxes
    cols = []
    for x in range(w):
        cnt = sum(1 for y in range(0, int(h * 0.35), 2) if (lambda c: c[0] > 190 and c[0] < 245 and c[1] > 120 and c[1] < 200 and c[2] > 190 and c[2] < 245 and c[0] > c[1] + 25)(im.getpixel((x, y))))
        if cnt > 15:
            cols.append(x)
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
    print(" magenta bands (x frac):", [(round(g[0]/w, 3), round(g[-1]/w, 3)) for g in groups])
    print()

scan(ORIG, "ORIGINAL")
scan(REND, "PREV RENDER")
