import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)


def runs(vals):
    out = []
    s = 0
    for i in range(1, len(vals) + 1):
        if i == len(vals) or vals[i] != vals[s]:
            out.append((s, i - 1, vals[s]))
            s = i
    return out


print("### HORIZONTAL slice y=150, x495..645 — colour runs (panel=231,233,232 / white=254,255,253)")
row = [tuple(im[150, x]) for x in range(495, 646)]
for a, b, c in runs(row):
    if a == b:
        print(f"  x{495+a}: {c}")
    else:
        print(f"  x{495+a}..{495+b}: {c}")

print()
print("### VERTICAL slice x=506, y120..260")
col = [tuple(im[y, 506]) for y in range(120, 261)]
for a, b, c in runs(col):
    if a == b:
        print(f"  y{120+a}: {c}")
    else:
        print(f"  y{120+a}..{120+b}: {c}")

print()
print("### VERTICAL slice x=635, y120..260")
col = [tuple(im[y, 635]) for y in range(120, 261)]
for a, b, c in runs(col):
    if a == b:
        print(f"  y{120+a}: {c}")
    else:
        print(f"  y{120+a}..{120+b}: {c}")

print()
print("### HORIZONTAL slice y=170, x495..645")
row = [tuple(im[170, x]) for x in range(495, 646)]
for a, b, c in runs(row):
    if a == b:
        print(f"  x{495+a}: {c}")
    else:
        print(f"  x{495+a}..{495+b}: {c}")

print()
print("### HORIZONTAL slice y=165 (glyph row), x515..555 grayscale-ish")
for y in (162, 165, 168, 171, 177, 180):
    row = [tuple(im[y, x]) for x in range(515, 556)]
    print(f" y{y}: " + " ".join(f"{c[0]:3d}" for c in row))
