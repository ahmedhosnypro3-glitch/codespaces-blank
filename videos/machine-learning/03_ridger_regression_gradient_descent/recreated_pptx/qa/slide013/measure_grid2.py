import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# relative-ink: anything not near-white and not near panel gray
nonwhite = (r < 245) | (g < 245) | (b < 245)

print("=== relative-ink column profile, y126..253 (row 1 band) ===")
seg = nonwhite[126:254, :]
cnt = seg.sum(axis=0)
xs = np.where(cnt > 60)[0]
# group
groups = []
s = p = xs[0]
for x in xs[1:]:
    if x - p <= 6:
        p = x
    else:
        groups.append((s, p))
        s = p = x
groups.append((s, p))
for a, c in groups:
    print(f"  x{a}..{c}  (max ink {cnt[a:c+1].max()})")

print("\n=== relative-ink row profile, x100..460 (left train table) ===")
seg2 = nonwhite[:, 100:461]
cnt2 = seg2.sum(axis=1)
ys = np.where(cnt2 > 100)[0]
groups = []
s = p = ys[0]
for y in ys[1:]:
    if y - p <= 6:
        p = y
    else:
        groups.append((s, p))
        s = p = y
groups.append((s, p))
for a, c in groups:
    print(f"  y{a}..{c} (max {cnt2[a:c+1].max()})")

print("\n=== full-slide ink column groups (y60..530, x>=55) ===")
seg3 = nonwhite[60:531, 55:]
cnt3 = seg3.sum(axis=0)
xs = np.where(cnt3 > 40)[0]
groups = []
s = p = xs[0]
for x in xs[1:]:
    if x - p <= 8:
        p = x
    else:
        groups.append((s, p))
        s = p = x
groups.append((s, p))
for a, c in groups:
    print(f"  x{a+55}..{c+55}  (max ink {cnt3[a:c+1].max()})")

print("\n=== full-slide ink row groups (x55..905) ===")
seg4 = nonwhite[:, 55:906]
cnt4 = seg4.sum(axis=1)
ys = np.where(cnt4 > 40)[0]
groups = []
s = p = ys[0]
for y in ys[1:]:
    if y - p <= 8:
        p = y
    else:
        groups.append((s, p))
        s = p = y
groups.append((s, p))
for a, c in groups:
    print(f"  y{a}..{c} (max {cnt4[a:c+1].max()})")
