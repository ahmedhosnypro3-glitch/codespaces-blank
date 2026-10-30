#!/usr/bin/env python3
"""Cut targeted region crops from original frames for the doc-parse lane.

Region boxes come from the independent analysis read (analysis/slide_NNN_raw.json
layout regions), converted from % to frame pixels. Each crop is upscaled with
Lanczos so it clears the ~480 px floor and stays inside the 1664x2048 input
ceiling. The crop-to-frame transform is recorded per region so frame positions
are never read from crop-local coordinate tokens.

Writes only under videos/machine-learning/08_performance_measure/.
"""

import json
from pathlib import Path

from PIL import Image

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
FRAMES = NS / "unique_slides"
DOCPARSE = NS / "pool_run" / "docparse"

# slide -> list of (region_name, x0%, y0%, x1%, y1%, upscale)
REGIONS = {
    "002": [
        ("right_column", 49, 12, 97, 92, 3),
    ],
    "003": [
        ("right_flowcharts", 49, 36, 97, 90, 3),
    ],
    "004": [
        ("left_diagram", 3, 12, 67, 96, 2),
        ("right_matrices", 66, 26, 99, 97, 3),
    ],
    "005": [
        ("bottom_left_matrix", 5, 40, 50, 90, 3),
        ("bottom_right_matrix", 47, 55, 95, 90, 3),
    ],
    "007": [
        ("right_class_tree", 53, 50, 99, 93, 3),
        ("left_formula", 3, 40, 52, 66, 3),
    ],
    "009": [
        ("left_bubbles", 3, 36, 55, 80, 3),
    ],
    "013": [
        ("right_formulas_calc", 48, 28, 97, 98, 3),
    ],
}

MAX_W, MAX_H = 1664, 2048

manifest = []
for slide, specs in REGIONS.items():
    src = FRAMES / f"slide_{slide}.jpg"
    with Image.open(src) as im:
        W, H = im.size
    out_root = DOCPARSE / f"slide{slide}" / "regions"
    for name, x0p, y0p, x1p, y1p, scale in specs:
        box = (
            max(0, round(W * x0p / 100)),
            max(0, round(H * y0p / 100)),
            min(W, round(W * x1p / 100)),
            min(H, round(H * y1p / 100)),
        )
        bw, bh = box[2] - box[0], box[3] - box[1]
        s = scale
        while (bw * s > MAX_W or bh * s > MAX_H) and s > 1:
            s -= 0.25
        with Image.open(src) as im:
            region = im.crop(box).resize(
                (round(bw * s), round(bh * s)), Image.LANCZOS)
        rdir = out_root / name
        rdir.mkdir(parents=True, exist_ok=True)
        png = rdir / f"slide_{slide}_{name}.png"
        region.save(png, "PNG")
        entry = {
            "slide": f"slide_{slide}",
            "region": name,
            "source_frame": src.name,
            "frame_dims": [W, H],
            "box_frame_px": [box[0], box[1], bw, bh],
            "scale": round(s, 4),
            "crop_dims": [region.width, region.height],
            "png": str(png.relative_to(NS)),
            "transform_rule": (
                "frame_x = crop_px / scale + box.x0 ; "
                "frame_y = crop_px / scale + box.y0"
            ),
            "targeting_source": "analysis/slide_%s_raw.json layout regions" % slide,
        }
        manifest.append(entry)
        print(f"slide_{slide} {name}: box={box} scale={s} "
              f"crop={region.width}x{region.height}")

mfile = DOCPARSE / "_driver" / "region_manifest.json"
mfile.parent.mkdir(parents=True, exist_ok=True)
mfile.write_text(json.dumps(manifest, indent=1))
print(f"\nregion manifest -> {mfile}")
