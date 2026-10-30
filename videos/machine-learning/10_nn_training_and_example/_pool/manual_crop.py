#!/usr/bin/env python3
"""Targeted region crop + re-parse for doc-parse lane scope_d1.

Used where the automated cascade stops at the root (full-frame parse yields
no text lines) but the slide visibly carries diagram labels. Crops at native
resolution (no upscaling), then parses each crop with the frozen skill script.
"""
import os
import subprocess
import sys

from PIL import Image

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SKILL = "/home/codespace/.agents/skills/doc-parse/scripts/parse_document.py"

# slide -> list of (tag, left, top, right, bottom) in source pixels
REGIONS = {
    "008": [("band", 320, 40, 935, 240)],
    "018": [("band", 320, 40, 935, 235)],
}


def main():
    slide = sys.argv[1]
    src = os.path.join(VID, "unique_slides", f"slide_{slide}.jpg")
    outdir = os.path.join(VID, "_pool", f"cascade_{slide}", "manual")
    os.makedirs(outdir, exist_ok=True)
    im = Image.open(src)
    for tag, l, t, r, b in REGIONS.get(slide, []):
        crop = im.crop((l, t, r, b))
        png = os.path.join(outdir, f"slide_{slide}_{tag}.png")
        crop.save(png)
        print(f"{slide}/{tag}: {crop.size} -> {png}", flush=True)
        cmd = ["python3", SKILL, png, "-o", outdir, "--timeout", "180"]
        p = subprocess.run(cmd, capture_output=True, text=True)
        print(f"  rc={p.returncode} out={p.stdout.strip()} err={p.stderr.strip()[:300]}",
              flush=True)


if __name__ == "__main__":
    main()
