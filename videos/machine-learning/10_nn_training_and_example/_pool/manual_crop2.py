#!/usr/bin/env python3
"""Second targeted crop pass for doc-parse lane scope_d1.

For picture-only slides whose automated cascade stops at the root and whose
first band crop still missed diagram-internal labels. Crops at native
resolution (no upscaling); region boxes are approximate from the slide's
own analysis JSON layout regions.
"""
import os
import subprocess
import sys

from PIL import Image

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SKILL = "/home/codespace/.agents/skills/doc-parse/scripts/parse_document.py"

REGIONS = {
    # slide_008: diagram interior (beige box) — Recover Net/O/w, Output labels
    "008": [
        ("diag", 340, 55, 800, 220),
        ("nodes", 560, 60, 830, 200),
    ],
    # slide_018: bottom-left 'Input Data' + wider diagram + right column
    "018": [
        ("wide", 330, 50, 880, 235),
        ("lowleft", 330, 150, 620, 250),
    ],
}


def main():
    slide = sys.argv[1]
    src = os.path.join(VID, "unique_slides", f"slide_{slide}.jpg")
    outdir = os.path.join(VID, "_pool", f"cascade_{slide}", "pass2")
    os.makedirs(outdir, exist_ok=True)
    im = Image.open(src)
    for tag, l, t, r, b in REGIONS.get(slide, []):
        crop = im.crop((l, t, r, b))
        png = os.path.join(outdir, f"slide_{slide}_{tag}.png")
        crop.save(png)
        print(f"{slide}/{tag}: {crop.size} -> {png}", flush=True)
        p = subprocess.run(["python3", SKILL, png, "-o", outdir, "--timeout", "180"],
                           capture_output=True, text=True)
        print(f"  rc={p.returncode} out={p.stdout.strip()}", flush=True)


if __name__ == "__main__":
    main()
