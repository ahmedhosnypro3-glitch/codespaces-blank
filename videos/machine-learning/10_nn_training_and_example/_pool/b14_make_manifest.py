#!/usr/bin/env python3
"""Build OMML manifests for slides 027 and 028 by matching embedded pptx media
(md5) against the equation sidecars in recreated_pptx/build/assets/."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example")
BUILD = NS / "recreated_pptx" / "build"


def build_manifest(stem):
    pptx = NS / "recreated_pptx" / f"{stem}_recreated.pptx"
    z = zipfile.ZipFile(pptx)
    media = {n: hashlib.md5(z.read(n)).hexdigest()
             for n in z.namelist() if n.startswith("ppt/media/image")}
    assets = {}
    for side in sorted(BUILD.glob("assets/*.json")):
        png = side.with_suffix(".png")
        if not png.exists():
            continue
        info = json.loads(side.read_text())
        if "mathtext" not in info:
            continue
        assets[hashlib.md5(png.read_bytes()).hexdigest()] = {
            "image": png.name,
            "mathtext": info["mathtext"],
            "font_size_pt": info["fontsize_pt"],
            "color": info["color"],
        }
    equations = []
    for name in sorted(media, key=lambda n: int(n.rsplit("-", 1)[1].split(".")[0])):
        entry = assets.get(media[name])
        if entry is None:
            continue
        equations.append(entry)
    out = NS / "_pool" / "omml" / f"manifest_{stem}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"slides": [{"slide": 1, "equations": equations}]}, indent=1))
    print(f"{stem}: {len(equations)} equations -> {out}")
    for e in equations:
        print("   ", e["image"], e["mathtext"])


if __name__ == "__main__":
    for stem in sys.argv[1:] or ["slide_027", "slide_028"]:
        build_manifest(stem)
