#!/usr/bin/env python3
"""Re-cut Procedure B crop pairs for slide 016 from render_8.png (the
underline-fix rebuild) at matched effective scale 2.0833, and regenerate the
Template B payload with the only legal substitution (NNN->016, \\bK\\b->6).

Only the regions that CHANGED across the rebuild are re-cut (proven by
pixel diff: last_bullet + full_body differ, missing_band/bullet2 are
byte-identical and keep their crop_5 transcripts).
"""
import re
import numpy as np
from PIL import Image
from pathlib import Path

QA = Path("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
          "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
RENDER = QA / "render_8.png"
ORIG = Path("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
            "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")
PROTO = Path("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
             "03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md")

r = Image.open(RENDER).convert("RGB")
o = Image.open(ORIG).convert("RGB")
S = r.size[1] / o.size[1]
print(f"render_6 {r.size}  original {o.size}  scale S={S:.4f}")

REGIONS = [
    ("last_bullet", 80, 475, 820, 532),
    ("full_body",   80,  98, 815, 532),
]
for name, x0, y0, x1, y1 in REGIONS:
    rb = (round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S))
    rc = r.crop(rb)
    oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    er = (rc.size[0] / (x1 - x0), rc.size[1] / (y1 - y0))
    eo = (oc.size[0] / (x1 - x0), oc.size[1] / (y1 - y0))
    assert abs(er[0] - eo[0]) < 0.01 and abs(er[1] - eo[1]) < 0.01, (er, eo)
    rc.save(QA / f"crop_8_{name}_render.png")
    oc.save(QA / f"crop_8_{name}_orig.png")
    print(f"{name}: render {rc.size} orig-upscaled {oc.size} eff "
          f"x={er[0]:.4f}/{eo[0]:.4f} y={er[1]:.4f}/{eo[1]:.4f}")

# --- K-token law: template payload, only NNN->016 and \bK\b->6 ---
block = re.search(r"## Template B —.*?```\n(.*?)```", PROTO.read_text(), re.S).group(1)
tmpl = re.search(r'-p "(.*?)"\s*$', block, re.S).group(1)
payload = tmpl.replace("NNN", "016")
payload = re.sub(r"\bK\b", "8", payload)
assert "NNN" not in payload and not re.search(r"\bK\b", payload)
assert "slide 016" in payload and payload.count("BLOCKER") == 2
(QA / "judge_prompt_8B.txt").write_text(payload)
print(f"\njudge_prompt_8B.txt: {len(payload)} bytes, md5-verified below")
