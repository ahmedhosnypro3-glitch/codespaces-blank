import numpy as np
from PIL import Image
import importlib.util

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
spec = importlib.util.spec_from_file_location(
    "m2", f"{NS}/_pool/geom_b_geom_3/measure_v2.py")
m2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m2)
FX, FY = 960 / 2001.0, 540 / 1125.0
for n in ["014", "017", "016"]:
    om = m2.orig_ink(n, f"{NS}/unique_slides/slide_{n}.jpg")
    rm = m2.render_ink(f"{NS}/_pool/lo_geom_b_geom_3/out/slide_{n}_150.png")
    print(f"########## {n}")
    for j, (y0, y1) in enumerate(m2.bands_of(om)):
        b, k = m2.bbox_in(om, y0, y1)
        print(f"  ORIG band{j} y{y0}..{y1}  x{b[0]}..{b[2]} ink={k}")
    print("  --- render (normalized to frame px) ---")
    for j, (y0, y1) in enumerate(m2.bands_of(rm)):
        b, k = m2.bbox_in(rm, y0, y1)
        print(f"  RENDER band{j} y{y0}..{y1} -> frame y{y0*FY:.0f}..{y1*FY:.0f}"
              f"  x{b[0]*FX:.0f}..{b[2]*FX:.0f} ink={k}")
