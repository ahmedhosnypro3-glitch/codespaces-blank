from PIL import Image
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_022.jpg").convert("RGB")
px = im.load()

def isink(c):
    r, g, b = c
    mx, mn = max(r, g, b), min(r, g, b)
    return mx - mn > 45 or mx < 165

def bbox(name, x0, y0, x1, y1):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if isink(px[x, y]):
                xs.append(x); ys.append(y)
    if not xs:
        print(name, "no ink"); return
    print("%-28s x %d-%d (w=%d)  y %d-%d (h=%d)" % (name, min(xs), max(xs), max(xs)-min(xs)+1,
                                                     min(ys), max(ys), max(ys)-min(ys)+1))

bbox("r1L prefix f(x)=Rectified", 90, 120, 240, 185)
bbox("r1L full content", 88, 118, 476, 186)
bbox("r1L val+cond line1", 330, 120, 476, 152)
bbox("r1L val+cond line2", 330, 150, 476, 186)
bbox("r1R content", 638, 118, 870, 186)
bbox("r2L content", 88, 212, 476, 275)
bbox("r3L content", 88, 312, 476, 380)
bbox("r4L content", 88, 418, 346, 480)
bbox("r4R content", 638, 418, 786, 480)
bbox("title", 150, 45, 730, 95)
bbox("derivative r1", 480, 118, 600, 152)
bbox("arrow r1", 495, 150, 600, 185)
bbox("badge", 800, 40, 900, 100)
# per-row vertical profile of ink in the left panel col x 90-476 (find line pitch)
for label, (y0, y1) in {"r1": (118, 190), "r2": (212, 280), "r3": (312, 380), "r4": (418, 485)}.items():
    prof = []
    for y in range(y0, y1):
        n = sum(1 for x in range(90, 476) if isink(px[x, y]))
        prof.append((y, n))
    rowsum = " ".join("%d:%d" % (y, n) for y, n in prof if n > 3)
    print("\nprofile %s: %s" % (label, rowsum))
