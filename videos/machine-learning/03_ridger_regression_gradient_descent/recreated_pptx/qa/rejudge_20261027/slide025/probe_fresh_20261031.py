#!/usr/bin/env python3
"""PIL probe for slide025 fresh FULL FAIL adjudication (read-only)."""
import hashlib, os, zipfile
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
S = f"{RJ}/slide025"

render = Image.open(f"{S}/render.png").convert("RGB")
orig = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
W, H = render.size
sx, sy = W / 960.0, H / 540.0
R = np.asarray(render).astype(int)
O = np.asarray(orig.resize((W, H), Image.LANCZOS)).astype(int)

def box(a, x0, y0, x1, y1):
    return a[int(y0*sy):int(y1*sy), int(x0*sx):int(x1*sx)]

def dark_ink(a):
    g = a.sum(axis=2)
    return int((g < 240).sum())

print("== 1. embedded plot PNGs vs build assets ==")
pptx = f"{NS}/recreated_pptx/slide_025_recreated.pptx"
with zipfile.ZipFile(pptx) as z:
    media = {n: hashlib.md5(z.read(n)).hexdigest() for n in z.namelist() if n.startswith("ppt/media/")}
for name in ["tl", "tr", "bl", "br"]:
    p = f"{NS}/recreated_pptx/build/assets/plot_025_{name}.png"
    m = hashlib.md5(open(p, "rb").read()).hexdigest()
    match = [k for k, v in media.items() if v == m]
    st = os.stat(p)
    import datetime
    print(f"  plot_025_{name}.png md5={m[:10]} mtime={datetime.datetime.utcfromtimestamp(st.st_mtime)} embedded={'YES ' + match[0] if match else 'NO MATCH'}")

print("== 2. BR panel (x615-880 y344-531): black path ink, surface stats ==")
for label, a in [("orig", O), ("render", R)]:
    b = box(a, 615, 344, 880, 531)
    g = b.sum(axis=2)
    sat = b.max(axis=2) - b.min(axis=2)
    print(f"  {label}: dark<80 ink={int((g<80).sum())} dark<240 ink={int((g<240).sum())} "
          f"colored(sat>60)={int((sat>60).sum())} colored%={100*(sat>60).mean():.1f} "
          f"meanRGB=({b[:,:,0].mean():.0f},{b[:,:,1].mean():.0f},{b[:,:,2].mean():.0f})")

print("== 3. BL label bands swap test (slide-space crops) ==")
# build-measured original bands: Global Minima x145..201 y439..465 (lower-left),
# Local Minima x286..311 y390..399 (right); judge claims orig LL=Local, LR=Global
bands = {"LL": (130, 430, 215, 475), "LR": (280, 385, 340, 470)}
def crop_slide(a, b):
    x0, y0, x1, y1 = b
    return a[int(y0*sy):int(y1*sy), int(x0*sx):int(x1*sx)]
def sim(a, b):
    if a.shape != b.shape:
        b = np.asarray(Image.fromarray(b.astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.LANCZOS)).astype(int)
    return float(np.abs(a - b).mean())
for k, b in bands.items():
    co, cr = crop_slide(O, b), crop_slide(R, b)
    print(f"  {k} box={b}: orig-vs-render meanAbsDiff={sim(co, cr):.2f} "
          f"orig dark ink={int((co.sum(axis=2)<240).sum())} render dark ink={int((cr.sum(axis=2)<240).sum())}")
# cross test: render LL vs orig LR and vice versa (swap detection)
coLL, coLR = crop_slide(O, bands["LL"]), crop_slide(O, bands["LR"])
crLL, crLR = crop_slide(R, bands["LL"]), crop_slide(R, bands["LR"])
print(f"  cross: renderLL-vs-origLL={sim(crLL, coLL):.2f} renderLL-vs-origLR={sim(crLL, coLR):.2f} "
      f"renderLR-vs-origLR={sim(crLR, coLR):.2f} renderLR-vs-origLL={sim(crLR, coLL):.2f}")

print("== 4. TR panel (x616-879 y115-317): geometry ==")
for label, a in [("orig", O), ("render", R)]:
    b = box(a, 616, 115, 879, 317)
    sat = b.max(axis=2) - b.min(axis=2)
    ys, xs = np.where(sat > 60)
    if len(ys):
        print(f"  {label}: colored extent x[{xs.min()/sx:.0f}..{xs.max()/sx:.0f}] y[{ys.min()/sy:.0f}..{ys.max()/sy:.0f}] "
              f"of box x616-879 y115-317, colored%={100*(sat>60).mean():.1f}")
    g = b.sum(axis=2)
    print(f"    dark<240 ink={int((g<240).sum())} red-ish ink={int(((b[:,:,0]>120)&(b[:,:,1]<90)&(b[:,:,2]<90)).sum())}")

print("== 5. TL panel (x85-265 y115-288) ==")
for label, a in [("orig", O), ("render", R)]:
    b = box(a, 85, 115, 265, 288)
    sat = b.max(axis=2) - b.min(axis=2)
    ys, xs = np.where(sat > 60)
    if len(ys):
        print(f"  {label}: colored extent x[{xs.min()/sx:.0f}..{xs.max()/sx:.0f}] y[{ys.min()/sy:.0f}..{ys.max()/sy:.0f}] colored%={100*(sat>60).mean():.1f}")

print("== 6. BR bottom-band flush test (rows y520-531 inside BR box) ==")
for label, a in [("orig", O), ("render", R)]:
    b = box(a, 618, 518, 877, 531)
    sat = b.max(axis=2) - b.min(axis=2)
    for i in range(b.shape[0]):
        row = b[i]
        print(f"  {label} y={518+i}: colored%={100*(sat[i]>60).mean():5.1f} meanRGB=({row[:,0].mean():.0f},{row[:,1].mean():.0f},{row[:,2].mean():.0f})")
