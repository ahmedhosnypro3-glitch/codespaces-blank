#!/usr/bin/env python3
"""Pink-box border adjudication (crop_13 pinkbox F1 'missing thin border, MAJOR').
Measure the edge ring of the pink box in ORIG vs RENDER_13 (frame x735..836 y52..178)."""
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide050"

o = np.asarray(Image.open(NS + "/unique_slides/slide_050.jpg").convert("RGB"))
r = Image.open(QA + "/render_13.png").convert("RGB")
SC = r.size[1] / 540.0
r = np.asarray(r)

def ring_stats(img, x0, y0, x1, y1, tag, scale=1.0):
    box = img[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
    h, w, _ = box.shape
    ring = np.concatenate([box[0:2].reshape(-1,3), box[-2:].reshape(-1,3),
                           box[:,0:2].reshape(-1,3), box[:,-2:].reshape(-1,3)])
    fill = box[int(h*0.3):int(h*0.5), int(w*0.3):int(w*0.5)].reshape(-1,3)
    print("%s box(%d,%d,%d,%d) size %s" % (tag, x0, y0, x1, y1, (w, h)))
    print("  ring  px=%d mean=%s median=%s min_lum=%s dark_px(lum<200)=%d" % (
        len(ring), ring.mean(axis=0).round(1), np.median(ring, axis=0),
        round(float(ring.mean(axis=1).min()),1), int((ring.mean(axis=1) < 200).sum())))
    print("  fill  px=%d mean=%s median=%s" % (len(fill), fill.mean(axis=0).round(1), np.median(fill, axis=0)))
    # distinct darker-than-fill edge? show the 5 most common ring colors
    q = (ring // 16 * 16)
    uq, cnt = np.unique(q.reshape(-1,3), axis=0, return_counts=True)
    order = np.argsort(-cnt)[:6]
    print("  top ring colors:", [(list(uq[i]), int(cnt[i])) for i in order])

# locate the pink box precisely in the original: pink fill = high R, mid G/B
o_ = o.astype(int)
pink = (o_[:,:,0] > 200) & (o_[:,:,1] > 130) & (o_[:,:,1] < 210) & (o_[:,:,2] > 140) & (o_[:,:,2] < 215)
ys, xs = np.where(pink)
print("orig pink fill bbox: x%d..%d y%d..%d  n=%d" % (xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))
bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max(), ys.max()
ring_stats(o, bx0, by0, bx1, by1, "ORIG")

r_ = r.astype(int)
pinkr = (r_[:,:,0] > 200) & (r_[:,:,1] > 130) & (r_[:,:,1] < 210) & (r_[:,:,2] > 140) & (r_[:,:,2] < 215)
ys2, xs2 = np.where(pinkr)
print("\nrender pink fill bbox: x%d..%d y%d..%d  n=%d (frame %s)" % (
    xs2.min(), xs2.max(), ys2.min(), ys2.max(), len(xs2),
    (round(xs2.min()/SC), round(ys2.min()/SC), round(xs2.max()/SC), round(ys2.max()/SC))))
ring_stats(r, xs2.min(), ys2.min(), xs2.max(), ys2.max(), "RENDER13", scale=1.0)

# edge rows/cols detail in orig: scan the border band just inside/outside the fill
print("\nORIG row profiles at box top/bottom (mean RGB per row, x mid-band):")
mid = slice((bx0+bx1)//2 - 20, (bx0+bx1)//2 + 20)
for yy in range(by0-3, by0+5):
    print("  y%d %s" % (yy, o[yy, mid].mean(axis=0).round(0)))
for yy in range(by1-4, by1+4):
    print("  y%d %s" % (yy, o[yy, mid].mean(axis=0).round(0)))
print("ORIG col profiles at box left/right (mean RGB per col, y mid-band):")
midy = slice((by0+by1)//2 - 20, (by0+by1)//2 + 20)
for xx in range(bx0-3, bx0+5):
    print("  x%d %s" % (xx, o[midy, xx].mean(axis=0).round(0)))
for xx in range(bx1-4, bx1+4):
    print("  x%d %s" % (xx, o[midy, xx].mean(axis=0).round(0)))
