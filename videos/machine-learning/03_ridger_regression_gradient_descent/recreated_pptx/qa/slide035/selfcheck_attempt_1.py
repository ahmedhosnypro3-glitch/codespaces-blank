import numpy as np
from PIL import Image

rend = np.asarray(Image.open("videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide035/render_1.png").convert("RGB")).astype(int)
H, W = rend.shape[:2]
S = H / 540.0  # render px per frame px
print(f"render {W}x{H}, scale {S:.4f}")
r, g, b = rend[:,:,0], rend[:,:,1], rend[:,:,2]
red = (r > 110) & ((r - g) > 50) & ((r - b) > 20)
blue = (b > 110) & ((b - g) > 50) & ((b - r) > 50)
inner = np.zeros_like(red); inner[:, int(70*S):int(895*S)] = True

def band(mask, y0f, y1f, label, targets):
    m = mask & inner
    m[:int(y0f*S), :] = False; m[int(y1f*S)+1:, :] = False
    ys, xs = np.where(m)
    x0, x1 = xs.min()/S, xs.max()/S
    # row profile for band structure
    rows = m.sum(axis=1); nz = np.where(rows > 0)[0]
    y0r, y1r = nz.min()/S, nz.max()/S
    # x-height top: first row where count > 0.35*max
    mx = rows[nz].max()
    xh = nz[rows[nz] > 0.35*mx][0]/S
    # baseline: last row with count > 0.35*max
    bl = nz[rows[nz] > 0.35*mx][-1]/S
    print(f"{label}: ink x {x0:.1f}..{x1:.1f} (center {(x0+x1)/2:.1f}), top {y0r:.1f}, x-height-top {xh:.1f}, baseline {bl:.1f}, bottom {y1r:.1f}")
    print(f"   targets: {targets}")
    print(f"   deltas: x0 {x0-targets[0]:+.1f} x1 {x1-targets[1]:+.1f} xh {xh-targets[2]:+.1f} bl {bl-targets[3]:+.1f}")

band(red, 160, 240, "L1", (147, 813, 185, 211))
band(red, 245, 310, "L2", (217, 743, 263, 288.5))
band(blue, 315, 370, "SUB", (271, 678, 335, 357))

# pitch check
m = red & inner
rows = m.sum(axis=1)
nz = np.where(rows > 3)[0]
# find contiguous bands
bnds=[]; s=nz[0]; p=nz[0]
for y in nz[1:]:
    if y > p+4: bnds.append((s,p)); s=y
    p=y
bnds.append((s,p))
print("red bands (frame px):", [(round(a/S,1), round(bb/S,1)) for a,bb in bnds])
# containment: no ink outside panel x54..903, y45..540
full = red | blue
full[:, :int(54*S)-2] = False; full[:, int(903*S)+2:] = False  # clip to panel window for content check
ys, xs = np.where(full)
print("content ink bbox inside panel window (frame px):", round(xs.min()/S,1), round(xs.max()/S,1), round(ys.min()/S,1), round(ys.max()/S,1))
