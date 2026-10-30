#!/usr/bin/env python3
"""Slide 047 attempt 6: crop pairs + byte-for-byte judge payloads (worker w047-root).

- Extracts Template A / Template B payloads from shared_patterns/judge_protocol_03.md
  (substitutes only NNN/K).
- Cuts crop pairs from render_10.png + the original at matched effective scale
  (LANCZOS upscale of the original by render/540).
Run from repo root. Banks under recreated_pptx/qa/slide047/.
"""
import re

PROTO = "videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md"
Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047"
NNN, K = "047", "6"

text = open(PROTO, encoding="utf-8").read()

mA = re.search(r'Template A.*?-p "(.*?)"\n```', text, re.S)
assert mA, "template A payload not found"
payloadA = mA.group(1).replace("NNN", NNN)
open(f"{Q}/judge_prompt_attempt_{K}.txt", "w", encoding="utf-8").write(payloadA)

mB = re.search(r'Template B.*?-p "(.*?)"\n```', text, re.S)
assert mB, "template B payload not found"
payloadB = mB.group(1).replace("NNN", NNN)
for name in ("topband", "augmatrix", "calceq", "calcright", "button"):
    open(f"{Q}/crop_prompt_{K}_{name}.txt", "w", encoding="utf-8").write(payloadB)

banked = open(f"{Q}/crop_prompt_1_topband.txt", encoding="utf-8").read()
print("TemplateB == banked crop_prompt_1_topband.txt (K-invariant, NNN same):", payloadB == banked)
bankedA = open(f"{Q}/judge_prompt_1.txt", encoding="utf-8").read()
payloadA_k1 = mA.group(1).replace("NNN", NNN).replace("attempt_K", "attempt_1")
print("TemplateA == banked judge_prompt_1.txt (attempt_6 -> attempt_1):", payloadA == payloadA_k1,
      "| bankedA == payloadA_k1:", bankedA == payloadA_k1)

from PIL import Image

RENDER = f"{Q}/render_10.png"  # attempt-6 render (pixel-identical to banked render_9)
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_047.jpg"
regions = {
    "topband": (62, 50, 726, 132, "top band: left data matrix, Initial W vector, legend, Z matrix"),
    "augmatrix": (64, 134, 252, 261, "mid-left augmented-vectors matrix with spanning parens and class row"),
    "calceq": (268, 134, 605, 203, "box 1 equation: d(Z1) label, blue row vector, green stacked column, result"),
    "calcright": (490, 134, 865, 335, "right side of all three calc boxes: sign statements and class outcomes"),
    "button": (74, 273, 243, 309, "bottom-left red Check Classes button"),
}
rim = Image.open(RENDER).convert("RGB")
oim = Image.open(ORIG).convert("RGB")
sx = rim.width / 960.0
sy = rim.height / 540.0
print(f"scale render px per frame px: sx={sx:.5f} sy={sy:.5f}")

audit = [f"attempt {K} crop scale audit (worker w047-root-20261024)",
         f"render_10.png 2001x1125; frame 960x540; sx={sx:.6f} sy={sy:.6f}"]
for name, (x0, y0, x1, y1, desc) in regions.items():
    rx0, ry0, rx1, ry1 = round(x0 * sx), round(y0 * sy), round(x1 * sx), round(y1 * sy)
    rc = rim.crop((rx0, ry0, rx1, ry1))
    oc_up = oim.crop((x0, y0, x1, y1)).resize((round((x1 - x0) * sx), round((y1 - y0) * sy)), Image.LANCZOS)
    if rc.size != oc_up.size:
        rc = rc.resize(oc_up.size, Image.LANCZOS)
    rc.save(f"{Q}/crop_{K}_{name}_render.png")
    oc_up.save(f"{Q}/crop_{K}_{name}_orig.png")
    fr = rc.size[0] / (x1 - x0)
    fo = oc_up.size[0] / (x1 - x0)
    print(f"{name}: frame ({x0},{y0},{x1},{y1}) -> {rc.size} | eff scale render {fr:.4f} orig {fo:.4f}")
    audit.append(f"{name}: frame bbox ({x0},{y0},{x1},{y1}); orig upscaled LANCZOS x({sx:.4f},{sy:.4f}); "
                 f"render crop LANCZOS-resized to match; eff scale render {fr:.4f} vs orig {fo:.4f}")

open(f"{Q}/crop_{K}_scale_audit.txt", "w", encoding="utf-8").write("\n".join(audit) + "\n")
print("crops + payloads banked")
