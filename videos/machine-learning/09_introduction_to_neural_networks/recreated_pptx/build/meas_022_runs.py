from PIL import Image
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_022.jpg").convert("RGB")
W, H = im.size
px = im.load()

def runs(seq, tol=12):
    out = []
    start = 0
    base = seq[0]
    for i in range(1, len(seq)):
        if max(abs(seq[i][k] - base[k]) for k in range(3)) > tol:
            out.append((start, i - 1, base, i - start))
            start = i; base = seq[i]
    out.append((start, len(seq) - 1, base, len(seq) - start))
    return [r for r in out if r[3] >= 2]

def hscan(y, x0, x1):
    seq = [px[x, y] for x in range(x0, x1)]
    print("--- horizontal y=%d, x %d..%d ---" % (y, x0, x1))
    for a, b, c, n in runs(seq):
        print("  x %4d-%4d  #%02X%02X%02X  n=%d" % (x0 + a, x0 + b, c[0], c[1], c[2], n))

def vscan(x, y0, y1):
    seq = [px[x, y] for y in range(y0, y1)]
    print("--- vertical x=%d, y %d..%d ---" % (x, y0, y1))
    for a, b, c, n in runs(seq):
        print("  y %4d-%4d  #%02X%02X%02X  n=%d" % (y0 + a, y0 + b, c[0], c[1], c[2], n))

hscan(176, 55, 900)          # row1, just below text baseline
vscan(200, 95, 520)          # through left panels rows 1-4
vscan(700, 95, 520)          # through right panels rows 1-4
hscan(455, 55, 900)          # row 4 band
