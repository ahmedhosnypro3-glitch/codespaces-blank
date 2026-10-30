#!/usr/bin/env python3
"""Precise row-profile scan to find each node's vertical extent on slide 23."""
from PIL import Image
import numpy as np

img = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_023.jpg").convert("RGB")
arr = np.asarray(img).astype(int)
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

# x-column bands to probe (each node's x-range)
bands = {
    "INIT":      (402, 787),
    "PICK":      (592, 790),
    "FORWARD":   (597, 793),
    "BACKWARD":  (597, 793),
    "LASTSAMPLE":(514, 671),
    "STOPCRIT":  (502, 693),
    "MAXITER":   (339, 453),
    "STOP":      (729, 847),
    "STOPFAIL":  (262, 535),
    "PICKFIRST": (117, 275),
}
for name, (x0, x1) in bands.items():
    print(f"\n{name} band x={x0}-{x1}:")
    runs = []
    cur = None
    for y in range(0, 540):
        col = arr[y, x0:x1+1]
        # "filled" = pastel non-white
        filled = ((col[:,0] > 225) & (col[:,1] > 200) & (col[:,2] > 150) &
                  (np.abs(col[:,0]-col[:,2]) < 60)).mean()
        if filled > 0.55:
            if cur is None:
                cur = y
        else:
            if cur is not None:
                runs.append((cur, y-1))
                cur = None
    if cur is not None:
        runs.append((cur, 539))
    for (a, bb) in runs:
        if bb - a >= 4:
            print(f"  y={a}-{bb} (h={bb-a+1})")