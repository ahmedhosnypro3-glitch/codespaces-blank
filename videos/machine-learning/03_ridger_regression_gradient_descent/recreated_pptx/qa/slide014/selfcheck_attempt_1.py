#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_014.jpg (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
H, W = im.shape[:2]
print("image", W, "x", H)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def mask_ink(tol=25):
    return (np.abs(im - 255).max(axis=2) > tol)

ink = mask_ink()
rows = np.where(ink.sum(axis=1) > 0)[0]
cols = np.where(ink.sum(axis=0) > 0)[0]
print("full ink bbox x", cols.min(), cols.max(), "y", rows.min(), rows.max())

# Per-row ink profile to find band boundaries
prof = ink.sum(axis=1)
print("\n--- row ink profile (every 4 rows) ---")
for y in range(0, 540, 4):
    if prof[y] > 0:
        print(f"y={y:3d} ink={prof[y]:4d}")
#!/usr/bin/env python3
"""PIL measurement of specific content regions in slide_014.jpg."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def mask_color(target_r, target_g, target_b, tol=30):
    return (np.abs(r - target_r) < tol) & (np.abs(g - target_g) < tol) & (np.abs(b - target_b) < tol)

def mask_ink(tol=30):
    return (np.abs(im - 255).max(axis=2) > tol)

ink = mask_ink()

# Measure yellow badge
yel = mask_color(255, 235, 59, tol=40)  # ~FFEB3B
ys = np.where(yel)
if len(ys[0]) > 0:
    print(f"Yellow badge: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}, center=({(ys[1].min()+ys[1].max())/2:.1f}, {(ys[0].min()+ys[0].max())/2:.1f})")

# Measure purple ring
pur = mask_color(106, 90, 205, tol=50)  # ~6A5ACD
ys = np.where(pur)
if len(ys[0]) > 0:
    print(f"Purple ring: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Red strokes
red = (r > 80) & ((r - g) > 30) & ((r - b) > 30)
ys = np.where(red)
print(f"Red strokes: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Panel gray E9E9E7 ~ (233,233,231)
gray = mask_color(233, 233, 231, tol=20)
ys = np.where(gray)
print(f"Panel gray: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Title region - look for blue text (0000FF)
blue = mask_color(0, 0, 255, tol=60)
ys = np.where(blue)
if len(ys[0]) > 0:
    print(f"Blue text: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Light yellow band (FFF9C4)
yel_band = mask_color(255, 249, 196, tol=40)
ys = np.where(yel_band)
if len(ys[0]) > 0:
    print(f"Light yellow band: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Light pink band (FFEBEE)
pink = mask_color(255, 235, 238, tol=40)
ys = np.where(pink)
if len(ys[0]) > 0:
    print(f"Light pink band: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Light blue band (E1F5FE)
lblue = mask_color(225, 245, 254, tol=40)
ys = np.where(lblue)
if len(ys[0]) > 0:
    print(f"Light blue band: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# Vertical ink profile for left/right columns
print("\n--- col ink profile (every 20 cols) ---")
prof = ink.sum(axis=0)
for x in range(0, 960, 20):
    if prof[x] > 0:
        print(f"x={x:3d} ink={prof[x]:4d}")#!/usr/bin/env python3
"""PIL measurement - tighter color detection for content bands."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

mask_yel = (r >= 250) & (g >= 240) & (b >= 180) & (b <= 210) & (r - b > 30)
ys = np.where(mask_yel)
if len(ys[0]) > 0:
    print(f"Light yellow: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

mask_pink = (r >= 250) & (g >= 225) & (g <= 245) & (b >= 228) & (b <= 248)
ys = np.where(mask_pink)
if len(ys[0]) > 0:
    print(f"Light pink: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

mask_lblue = (r >= 215) & (r <= 240) & (g >= 235) & (g <= 255) & (b >= 245) & (b <= 255)
ys = np.where(mask_lblue)
if len(ys[0]) > 0:
    print(f"Light blue: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

panel_mask = (np.abs(r[54:904, :] - 233) < 15) & (np.abs(g[54:904, :] - 233) < 15) & (np.abs(b[54:904, :] - 231) < 15)
ys = np.where(panel_mask)
if len(ys[0]) > 0:
    print(f"Panel gray: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# badge
br = im[55:90, 850:900]
rb, gb, bb = br[:, :, 0], br[:, :, 1], br[:, :, 2]
yel_mask = (rb > 220) & (gb > 220) & (bb < 120)
ys = np.where(yel_mask)
if len(ys[0]) > 0:
    print(f"Badge yellow center: ({ys[1].mean()+850:.1f}, {ys[0].mean()+55:.1f})")
pur_mask = (bb > 140) & (rb > 80) & (rb < 180) & (gb < 130)
ys = np.where(pur_mask)
if len(ys[0]) > 0:
    print(f"Badge purple center: ({ys[1].mean()+850:.1f}, {ys[0].mean()+55:.1f})")

print("\n--- Row transitions (ink density) ---")
prof = (np.abs(im - 255).max(axis=2) > 30).sum(axis=1)
prev = 0
for y in range(540):
    if abs(prof[y] - prev) > 150:
        print(f"  y={y}: {prev} -> {prof[y]}")
    prev = prof[y]

print("\n--- Upper middle (y=90-180) col profile ---")
sub = im[90:180, 60:900]
inkm = (np.abs(sub - 255).max(axis=2) > 30).sum(axis=0)
for x in range(0, 840, 40):
    if inkm[x] > 10:
        print(f"  x={x+60}: ink={inkm[x]}")

print("\n--- Lower middle (y=400-500) col profile ---")
sub = im[400:500, 60:900]
inkm = (np.abs(sub - 255).max(axis=2) > 30).sum(axis=0)
for x in range(0, 840, 40):
    if inkm[x] > 10:
        print(f"  x={x+60}: ink={inkm[x]}")

# blue text rows (title + accents)
blue = (b > 180) & (r < 120) & (g < 100)
ys = np.where(blue)
if len(ys[0]) > 0:
    print(f"\nBlue ink: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")
    rows_b = np.where(blue.sum(axis=1) > 2)[0]
    print(f"Blue ink rows: {rows_b.min()}-{rows_b.max()}")

# Black text ink in content bands (exclude panel gray FFFFFF)
blackish = (r < 120) & (g < 120) & (b < 120)
ys = np.where(blackish)
if len(ys[0]) > 0:
    print(f"Black ink: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")
#!/usr/bin/env python3
"""Sample exact colors along vertical and horizontal centerlines."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)

# Vertical scan down x=480 (center)
print("=== Vertical scan at x=480 ===")
for y in range(40, 545, 5):
    px = im[y, 480]
    print(f"y={y:3d}  rgb={tuple(int(v) for v in px)}")

# Horizontal scan at y=470 (loss/reg term boxes)
print("\n=== Horizontal scan at y=250 ===")
for x in range(50, 960, 20):
    px = im[250, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

print("\n=== Horizontal scan at y=470 ===")
for x in range(50, 960, 20):
    px = im[470, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")
#!/usr/bin/env python3
"""Sample exact colors along horizontal centerlines."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)

# y=250 (Ridge band + Objective band)
print("=== Horizontal scan at y=250 (Ridge/Objective bands) ===")
for x in range(50, 960, 20):
    px = im[250, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

# y=270 (Define Loss band)
print("\n=== Horizontal scan at y=270 (Define Loss band) ===")
for x in range(50, 960, 20):
    px = im[270, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

# y=470 (Loss Term / Reg Term boxes)
print("\n=== Horizontal scan at y=470 (Loss Term / Reg Term boxes) ===")
for x in range(50, 960, 20):
    px = im[470, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

# y=515 (Final objective band)
print("\n=== Horizontal scan at y=515 (Final objective band) ===")
for x in range(50, 960, 20):
    px = im[515, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")

# y=80 (vector boxes)
print("\n=== Horizontal scan at y=80 (vector boxes) ===")
for x in range(50, 960, 20):
    px = im[80, x]
    print(f"x={x:3d}  rgb={tuple(int(v) for v in px)}")#!/usr/bin/env python3
"""Measure precise fill-color band extents with tight masks."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]


def extent(mask, name):
    # require a solid run horizontally so we exclude text pixels
    rowc = mask.sum(axis=1)
    ys = np.where(rowc > 200)[0]
    if not len(ys):
        print(f"{name}: none")
        return
    y0, y1 = ys.min(), ys.max()
    colc = mask[y0:y1 + 1].sum(axis=0)
    xs = np.where(colc > 20)[0]
    x0, x1 = xs.min(), xs.max()
    # dominant color
    region = im[y0:y1 + 1, x0:x1 + 1]
    print(f"{name}: x {x0}-{x1}, y {y0}-{y1}, w={x1-x0+1}, h={y1-y0+1}, "
          f"rgb={tuple(int(v) for v in np.median(region.reshape(-1,3), axis=0))}")


# yellow band FFF9C4 -> JPEG reads ~(249,253,218)
extent((r >= 240) & (r <= 253) & (g >= 245) & (b >= 205) & (b <= 235) & (r - b > 20), "Yellow band")
# pink band FFEBEE -> ~(255,250,255)? sample at y=470 showed purple-ish (119,117,201)
# purple-pink boxes -> sample (119,117,201) which is a PURPLE fill (6A5ACD-ish?) not pink
extent((r > 100) & (r < 135) & (g > 85) & (g < 130) & (b > 185) & (b < 215), "Purple fill (y470)")
# final band E1F5FE -> (237,253,250)
extent((r >= 225) & (r <= 242) & (g >= 245) & (b >= 240) & (b <= 255), "Blue band E1F5FE")
# vector box white region (y 110..185)
extent((r >= 250) & (g >= 250) & (b >= 250), "White interior")

# Vector box black border (upper-middle left) - find black border rows
print("\n--- looking for box borders ---")
sub = im[95:200, 100:900]
bsub = (sub.max(axis=2) < 100)
rowc = bsub.sum(axis=1)
for i, c in enumerate(rowc):
    if c > 100:
        print(f"  y={95+i}: {c} px")

print("\n--- x=480 col profile y=100..200 ---")
for y in range(100, 200, 4):
    print(f"  y={y:3d} rgb={tuple(int(v) for v in im[y,480])}")
#!/usr/bin/env python3
"""Measure each content band's extent precisely."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# Yellow band (FFF9C4 approx ~249,253,218). Scan at columns that are text-free
print("=== YELLOW band: vertical scan at x=150 (text-free left area) ===")
for y in range(230, 460, 4):
    print(f"  y={y:3d} rgb={tuple(int(v) for v in im[y,150])}")

# Determine the yellow band y-extent by counting matching pixels per row
yel = (r > 240) & (g > 240) & (b > 200) & (b < 240) & (r - b > 15)
rowc = yel.sum(axis=1)
print("\nYellow matching px per row:")
for y in range(230, 460, 4):
    print(f"  y={y:3d}: {rowc[y]}")
#!/usr/bin/env python3
"""Find pink band (Define Loss) and light blue bands."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# Pink band (FFEBEE) - light pink #FFEBEE = (255, 235, 238)
pink = (r > 240) & (r < 255) & (g > 220) & (g < 250) & (b > 225) & (b < 255) & (r - g > 5) & (g - b > -30)
rowc = pink.sum(axis=1)
print("Pink band matching px per row:")
for y in range(280, 400, 2):
    if rowc[y] > 50:
        print(f"  y={y:3d}: {rowc[y]}")

# Light blue band (E1F5FE) - (225, 245, 254)
lblue = (r > 215) & (r < 240) & (g > 235) & (g < 255) & (b > 240) & (b < 255)
rowc = lblue.sum(axis=1)
print("\nLight blue band matching px per row:")
for y in range(400, 540, 2):
    if rowc[y] > 50:
        print(f"  y={y:3d}: {rowc[y]}")

# Vector boxes top area
print("\n=== Vector boxes y-range ===")
for y in range(60, 240, 4):
    # look for white background with black text
    pix = im[y, 200]
    if pix[0] > 245 and pix[1] > 245 and pix[2] > 245:
        print(f"  y={y:3d} white at x=200")

# Right vector box x-range at y=100
print("\n=== Right vector box x at y=100 ===")
for x in range(500, 960, 20):
    pix = im[100, x]
    print(f"  x={x:3d} rgb={tuple(int(v) for v in pix)}")