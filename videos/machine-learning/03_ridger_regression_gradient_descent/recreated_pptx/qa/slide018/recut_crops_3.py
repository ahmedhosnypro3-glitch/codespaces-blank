#!/usr/bin/env python3
"""Re-cut the crop_1_* pairs from render_4.png (attempt-3 render after the
attempt-2 FAIL fixes: y-row ink black, norm skeleton explicit primitives,
pencil-mark rect removed). Regions + descs are the banked attempt-1 set;
payloads are filename-free prose, so the banked crop prompts stay valid.
"""
import json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = os.path.join(HERE, "render_4.png")
ORIG = os.path.join(HERE, "..", "..", "..", "unique_slides", "slide_018.jpg")

REGIONS = [
    ("wbox",  (497, 119, 632, 259)),
    ("band1", (84, 118, 880, 258)),
    ("band2", (84, 255, 880, 395)),
    ("band3", (84, 392, 880, 532)),
    ("test",  (660, 88, 880, 258)),
    ("mark",  (660, 350, 880, 395)),
]
ri = Image.open(RENDER).convert("RGB")
oi = Image.open(ORIG).convert("RGB")
S = ri.height / 540.0
for name, (x0, y0, x1, y1) in REGIONS:
    rc = ri.crop((int(round(x0*S)), int(round(y0*S)), int(round(x1*S)), int(round(y1*S))))
    oc = oi.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(os.path.join(HERE, "crop_1_%s_render.png" % name))
    oc.save(os.path.join(HERE, "crop_1_%s_orig.png" % name))
    print("re-cut crop_1_%s from render_3  size=%s" % (name, rc.size))
print("done")
