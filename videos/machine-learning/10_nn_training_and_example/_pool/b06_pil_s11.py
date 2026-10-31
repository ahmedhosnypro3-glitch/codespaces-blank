import sys
import numpy as np
from PIL import Image

R = sys.argv[1]  # render png
a = np.asarray(Image.open(R).convert("RGB")).astype(int)
H, W, _ = a.shape
print(f"render {W}x{H}")

r, g, b = a[..., 0], a[..., 1], a[..., 2]
yellow = (r > 200) & (g > 200) & (b < 120)
red = (r > 120) & (g < 90) & (b < 90)
dark = (r < 100) & (g < 100) & (b < 100)
ink = (a < 245).any(axis=2)

# FAIL finding 4: yellow highlighter block behind "Output" in title (x 7.24-8.33in, y 0.33-0.69in)
ty0, ty1 = int(0.33 * 150), int(0.69 * 150)
tx0, tx1 = int(7.24 * 150), int(8.33 * 150)
reg = a[ty0:ty1, tx0:tx1]
yr = yellow[ty0:ty1, tx0:tx1]
print(f"title highlight band x[{tx0},{tx1}] y[{ty0},{ty1}]: "
      f"yellow_frac={yr.mean():.3f} median_rgb={np.median(reg.reshape(-1,3),axis=0).astype(int)}")

# FAIL finding 2: inter-layer wiring in the neural diagram.
# Slide bg is cream (~FDF5E6), so "non-background" must use a strict threshold.
def nonbg(img):
    c = np.asarray(img.convert("RGB")).astype(int)
    return (np.abs(c - np.array([253, 245, 230])).max(axis=2) > 25)

nb = nonbg(Image.open(R))
print(f"render {W}x{H} nonbg_frac={nb.mean():.4f}")
if len(sys.argv) > 2:
    b2 = nonbg(Image.open(sys.argv[2]))
    if b2.shape == nb.shape:
        print(f"compare {sys.argv[2]}: nonbg_old={b2.mean():.4f} nonbg_new={nb.mean():.4f} "
              f"delta={(nb.mean()-b2.mean()):+.4f}")
    else:
        print(f"shape mismatch: {b2.shape} vs {nb.shape}")

# FAIL finding 3: red pixels inside the bottom equation strip (overlap indicator)
by0, by1 = int(6.55 * 150), int(7.10 * 150)
bex, bey = red[by0:by1, :], dark[by0:by1, :]
print(f"bottom strip y[{by0},{by1}]: red_frac={bex.mean():.4f} dark_frac={bey.mean():.4f}")

# diagram region ink (y 1.4-4.2in)
dy0, dy1 = int(1.4 * 150), int(4.2 * 150)
print(f"diagram band y[{dy0},{dy1}]: ink_frac={ink[dy0:dy1, :].mean():.4f}")

# vertical red "Error" bar right side (x ~11.9-12.7in)
ex0, ex1 = int(11.9 * 150), int(12.7 * 150)
print(f"error bar region x[{ex0},{ex1}]: red_frac={red[:, ex0:ex1].mean():.4f}")
