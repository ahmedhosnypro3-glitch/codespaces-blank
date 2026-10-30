# PIL adjudication probes, slide 003 (frame space 960x540; crops are upscaled).
# 1) crop_32_topbox_orig.png: do per-column LEFT parens exist? right straight rules?
#    red ellipsis between y2 and yn?
# 2) crop_31_matrix_orig.png: per-row inner parentheses inside highlight bands?
from collections import defaultdict
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"

def cls(p):
    r, g, b = p[0], p[1], p[2]
    if r > 200 and g > 170 and b < 160: return 'y'
    if b > 170 and g > 150 and r < 170: return 'c'
    if r > 200 and b > 150 and g < 190 and r - g > 30: return 'm'
    if r > 150 and r - g > 60 and r - b > 60: return 'r'
    if max(r, g, b) < 120: return '#'
    return '.'

print("=== 1) topbox crop_32_topbox_orig.png ===")
im = Image.open(f"{R}/crop_32_topbox_orig.png").convert('RGB')
W, H = im.size
px = im.load()
print("size", W, H)

fillrows = {f: defaultdict(int) for f in 'ycm'}
fillcols = {f: defaultdict(int) for f in 'ycm'}
for y in range(0, H, 2):
    for x in range(0, W, 2):
        c = cls(px[x, y])
        if c in 'ycm':
            fillrows[c][y] += 1
            fillcols[c][x] += 1

fills = {}
for f in 'ycm':
    xs = sorted(x for x, n in fillcols[f].items() if n >= 3)
    ys = sorted(y for y, n in fillrows[f].items() if n >= 3)
    if xs:
        fills[f] = (min(xs), max(xs), min(ys), max(ys))
        print(f"fill {f}: x {min(xs)}..{max(xs)}  y {min(ys)}..{max(ys)}")

print("--- dark-ink column strips beside each fill (per-px dark counts) ---")
for f, (a, b, ya, yb) in fills.items():
    left = []; right = []
    for x in range(max(0, a - 34), a):
        n = sum(1 for y in range(ya, yb) if cls(px[x, y]) == '#')
        if n: left.append((x, n))
    for x in range(b + 1, min(W, b + 35)):
        n = sum(1 for y in range(ya, yb) if cls(px[x, y]) == '#')
        if n: right.append((x, n))
    print(f"fill {f} x{a}..{b}: LEFT dark cols {left}")
    print(f"            RIGHT dark cols {right}")

print("--- red clusters (whole crop) ---")
redpix = [(x, y) for y in range(H) for x in range(W) if cls(px[x, y]) == 'r']
print("red px total:", len(redpix))
if redpix:
    xs = sorted(set(p[0] for p in redpix))
    cl = []; cur = [xs[0], xs[0]]
    for x in xs[1:]:
        if x - cur[1] <= 8:
            cur[1] = x
        else:
            cl.append(tuple(cur)); cur = [x, x]
    cl.append(tuple(cur))
    for a, b in cl:
        pts = [(x, y) for x, y in redpix if a <= x <= b]
        ys = [p[1] for p in pts]
        print(f"  red cluster x{a}..{b}: n={len(pts)} y{min(ys)}..{max(ys)}")

fx, fy = max(1, W // 200), max(1, H // 56)
print(f"--- ASCII {W}x{H} step {fx}x{fy} ---")
for y in range(0, H, fy):
    row = ''
    for x in range(0, W, fx):
        cnt = defaultdict(int)
        for dy in range(0, fy, 2):
            for dx in range(0, fx, 2):
                if x + dx < W and y + dy < H:
                    cnt[cls(px[x + dx, y + dy])] += 1
        best = max(cnt.items(), key=lambda kv: kv[1])
        row += best[0] if best[1] >= 2 else '.'
    print(row)

print("=== 2) matrix crop_31_matrix_orig.png: per-row inner parens? ===")
im = Image.open(f"{R}/crop_31_matrix_orig.png").convert('RGB')
W, H = im.size
px = im.load()
print("size", W, H)
rowy = {f: defaultdict(int) for f in 'ycm'}
for y in range(0, H, 2):
    for x in range(0, W, 2):
        c = cls(px[x, y])
        if c in 'ycm':
            rowy[c][y] += 1
bands = {}
for f in 'ycm':
    ys = sorted(y for y, n in rowy[f].items() if n >= 5)
    if ys:
        bands[f] = (min(ys), max(ys))
        print(f"band {f}: y {min(ys)}..{max(ys)}")
for f, (ya, yb) in bands.items():
    print(f"--- {f} band y{ya}..{yb}: dark cols (8-col bins) ---")
    bins = defaultdict(int)
    for y in range(ya, yb + 1):
        for x in range(W):
            if cls(px[x, y]) == '#':
                bins[x // 8 * 8] += 1
    print(sorted(bins.items()))
