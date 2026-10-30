from PIL import Image
import numpy as np, sys

path = sys.argv[1]
cell = int(sys.argv[2]) if len(sys.argv) > 2 else 4
xlo = int(sys.argv[3]) if len(sys.argv) > 3 else 40
xhi = int(sys.argv[4]) if len(sys.argv) > 4 else 920
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

white = (R > 245) & (G > 245) & (B > 245)
red = (R - G > 60) & (R - B > 60) & (R > 120)
blue = (B - R > 60) & (B - G > 50) & (B > 90)
beige = (~red) & (~blue) & (~white) & (R - B > 20) & (R > 175)
dark = (R < 130) & (G < 130) & (B < 130)
gray = (~white) & (~red) & (~blue) & (~beige) & (~dark) & (np.abs(R - G) < 20) & (np.abs(G - B) < 20)

order = ["R", "B", "Y", "K", ".", " "]
cntmap = {"R": red, "B": blue, "Y": beige, "K": dark, ".": gray, " ": white}
print("legend: K=dark R=red B=blue Y=beige(.)=gray (space)=white")
print("     +" + "-" * ((xhi - xlo) // cell) + "+")
for y0 in range(0, H, cell):
    line = []
    for x0 in range(xlo, xhi, cell):
        ys, xs = slice(y0, min(y0 + cell, H)), slice(x0, min(x0 + cell, W))
        n = (ys.stop - ys.start) * (xs.stop - xs.start)
        ch = " "
        bestn = 0
        for k in order:
            v = int(cntmap[k][ys, xs].sum())
            if v > bestn:
                bestn = v; ch = k
        if bestn < n * 0.18:
            ch = " " if int(white[ys, xs].sum()) >= n * 0.5 else "."
        line.append(ch)
    print(f"{y0:4d} |" + "".join(line) + "|")
