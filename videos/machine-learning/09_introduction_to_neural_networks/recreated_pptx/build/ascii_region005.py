from PIL import Image
import numpy as np, sys

path = sys.argv[1]
cell = int(sys.argv[2])
xlo = int(sys.argv[3]); xhi = int(sys.argv[4])
ylo = int(sys.argv[5]); yhi = int(sys.argv[6])
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

white = (R > 244) & (G > 244) & (B > 244)
red = (R - G > 60) & (R - B > 60) & (R > 120)
blue = (B - R > 60) & (B - G > 50) & (B > 90)
dark = (R < 130) & (G < 130) & (B < 130)
other = (~white) & (~red) & (~blue) & (~dark)

print("legend: K=dark R=red B=blue o=mid-gray(other) (space)=white")
print("     +" + "-" * ((xhi - xlo) // cell) + "+")
for y0 in range(ylo, yhi, cell):
    line = []
    for x0 in range(xlo, xhi, cell):
        ys, xs = slice(y0, min(y0 + cell, H)), slice(x0, min(x0 + cell, W))
        n = (ys.stop - ys.start) * (xs.stop - xs.start)
        ch = " "
        bestn = 0
        for k, m in (("R", red), ("B", blue), ("K", dark), ("o", other)):
            v = int(m[ys, xs].sum())
            if v > bestn:
                bestn = v; ch = k
        if bestn < n * 0.25:
            ch = " " if int(white[ys, xs].sum()) >= n * 0.5 else "."
        line.append(ch)
    print(f"{y0:4d} |" + "".join(line) + "|")
