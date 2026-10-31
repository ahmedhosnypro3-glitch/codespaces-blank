from PIL import Image
import glob, os

eqd = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/equations_slide022"
for f in sorted(glob.glob(eqd + "/*.png")):
    im = Image.open(f).convert("RGBA")
    px = im.load()
    cols = {}
    n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a > 128:
                n += 1
                cols[(r, g, b)] = cols.get((r, g, b), 0) + 1
    top = sorted(cols.items(), key=lambda kv: -kv[1])[:5]
    print(os.path.basename(f), im.size, "opaque", n)
    for c, k in top:
        print("    #%02X%02X%02X" % c, k, "transparent-px:", im.width*im.height - n)
