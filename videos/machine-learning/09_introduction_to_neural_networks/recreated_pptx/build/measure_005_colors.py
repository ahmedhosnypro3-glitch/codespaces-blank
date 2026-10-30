from PIL import Image
import numpy as np, sys

path = sys.argv[1] if len(sys.argv) > 1 else "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_005.jpg"
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def report(name, mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        print(f"{name}: none")
        return
    print(f"{name}: n={len(xs)} x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]")

red = (R > 120) & (R - G > 55) & (R - B > 55)
blue = (B > 100) & (B - R > 55) & (B - G > 55)
dark = (R < 110) & (G < 110) & (B < 110)
gray_bg = (abs(R - 232) < 12) & (abs(G - 232) < 12) & (abs(B - 232) < 12)
white = (R > 245) & (G > 245) & (B > 245)

print("size", W, H)
report("red", red)
report("blue", blue)
report("dark", dark)
report("gray_bg", gray_bg)
report("white", white)

# red row/column histogram to find the panel frames
print("\n-- red row counts (rows with >=30 red px) --")
rc = red.sum(axis=1)
for y in range(H):
    if rc[y] >= 30:
        xs = np.nonzero(red[y])[0]
        # summarize contiguous runs
        runs = []
        s = xs[0]; p = xs[0]
        for x in xs[1:]:
            if x != p + 1:
                runs.append((s, p)); s = x
            p = x
        runs.append((s, p))
        print(f"y={y} count={rc[y]} runs={runs[:6]}{'...' if len(runs)>6 else ''}")

print("\n-- red col counts (cols with >=30 red px) --")
cc = red.sum(axis=0)
for x in range(W):
    if cc[x] >= 30:
        ys = np.nonzero(red[:, x])[0]
        runs = []
        s = ys[0]; p = ys[0]
        for y in ys[1:]:
            if y != p + 1:
                runs.append((s, p)); s = y
            p = y
        runs.append((s, p))
        print(f"x={x} count={cc[x]} runs={runs[:6]}{'...' if len(runs)>6 else ''}")
