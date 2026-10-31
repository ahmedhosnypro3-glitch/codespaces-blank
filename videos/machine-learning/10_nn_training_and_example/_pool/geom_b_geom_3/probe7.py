import numpy as np
from PIL import Image
import importlib.util

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
spec = importlib.util.spec_from_file_location(
    "m2", f"{NS}/_pool/geom_b_geom_3/measure_v2.py")
m2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m2)
FX, FY = 960 / 2001.0, 540 / 1125.0

print("=== 014/016 ORIGINAL band1 row structure (frame y86..122) ===")
for n, lo, hi in [("014", 86, 122), ("016", 86, 122)]:
    om = m2.orig_ink(n, f"{NS}/unique_slides/slide_{n}.jpg")
    print(f"-- {n}")
    for y in range(lo, hi):
        xs = np.nonzero(om[y, :])[0]
        if len(xs):
            print(f"   y{y}: n={len(xs)} x{xs.min()}..{xs.max()}")
print("=== 014/017 RENDER band2 structure (render y180..250) ===")
for n in ["014", "017"]:
    rm = m2.render_ink(f"{NS}/_pool/lo_geom_b_geom_3/out/slide_{n}_150.png")
    print(f"-- {n}")
    for y in range(175, 255, 2):
        xs = np.nonzero(rm[y, :])[0]
        if len(xs):
            print(f"   ry{y} (frame y{y*FY:.0f}): n={len(xs)} "
                  f"x{xs.min()*FX:.0f}..{xs.max()*FX:.0f}")
