import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0

ra = np.asarray(R).astype(float)
ro = np.asarray(O).astype(float)


def rlum(x, y):
    return 0.299 * ra[int(y * s), int(x * s), 0] + 0.587 * ra[int(y * s), int(x * s), 1] + 0.114 * ra[int(y * s), int(x * s), 2]


def olum(x, y):
    return 0.299 * ro[y, x, 0] + 0.587 * ro[y, x, 1] + 0.114 * ro[y, x, 2]


def dump(name, lumfn, x0, x1, y0, y1, thr=215):
    print(f"### {name} x{x0}..{x1} y{y0}..{y1}")
    for y in range(y0, y1):
        row = "".join("#" if lumfn(x, y) < thr * 0.75 else ("+" if lumfn(x, y) < thr else ".") for x in range(x0, x1))
        print(f"{y:4d}| {row}")
    print()


# B2 value stack: original vs render (frame-space bbox)
dump("ORIG B2 values x560..590 y276..350", olum, 560, 590, 276, 350)
dump("RENDER B2 values x560..590 y276..350", rlum, 560, 590, 276, 350)

# B1 value stack (digit height reference)
dump("ORIG B1 values x560..590 y138..210", olum, 560, 590, 138, 210)
dump("RENDER B1 values x560..590 y138..210", rlum, 560, 590, 138, 210)

# Train label box: original (full box) then render
dump("ORIG Train box x94..164 y94..128", olum, 94, 164, 94, 128)
dump("RENDER Train box x94..164 y94..128", rlum, 94, 164, 94, 128)

# Test label box: original vs render
dump("ORIG Test box x799..869 y94..128", olum, 799, 869, 94, 128)
dump("RENDER Test box x799..869 y94..128", rlum, 799, 869, 94, 128)
