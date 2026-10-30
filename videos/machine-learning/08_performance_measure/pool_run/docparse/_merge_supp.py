#!/usr/bin/env python3
"""Fold the supplemental anchor-targeted region leg into each run's manifest
and re-run the skill's frozen deterministic composer.

The crop-cascade script composes from the manifest alone, so the supplement
nodes are appended to manifest["crops"] with their own crop-to-frame
transform (frame = png_px / scale + origin_px) and the frozen
cascade_compose.compose_markdown() rebuilds the composed transcript.

Failed supplement calls are appended with an `error`, so the composed file
marks the gap instead of silently dropping it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_SCRIPTS = Path("/home/codespace/.agents/skills/doc-parse/scripts")
sys.path.insert(0, str(SKILL_SCRIPTS))

import cascade_compose as cc  # noqa: E402

ROOT = Path("/home/codespace/ai_llm_slides/videos/machine-learning/"
            "08_performance_measure/pool_run/docparse")

# source-frame boxes (960x540) of every supplemental crop, per run
REGIONS = {
    "ltop": (30, 35, 600, 205),
    "lmid": (30, 190, 600, 365),
    "lbot": (30, 345, 600, 520),
    "rcol": (555, 35, 945, 520),
    "band1": (30, 35, 940, 190),
    "band2": (30, 165, 940, 320),
    "band3": (30, 295, 940, 520),
    "mid_a": (30, 190, 340, 365),
    "mid_b": (300, 190, 600, 365),
}

DENSE = ["slide029", "slide031", "slide032", "slide033", "slide034",
         "slide035", "slide036", "slide037"]


def png_size(path: Path) -> tuple:
    from PIL import Image
    with Image.open(path) as im:
        return im.size


def supplement_nodes(run: Path) -> list:
    supp = run / "crops_supp"
    if not supp.is_dir():
        return []
    nodes = []
    for key_dir in sorted(p for p in supp.iterdir() if p.is_dir()):
        key = key_dir.name
        if key not in REGIONS:
            continue
        mds = sorted(key_dir.glob("*.parse.md"))
        jss = sorted(key_dir.glob("*.parse.json"))
        if not mds:
            continue
        md = mds[0]
        js = jss[0] if jss else None
        finish = None
        error = None
        if js is not None:
            data = json.loads(js.read_text())
            finish = data.get("finish_reason")
            content = data.get("content") or ""
            if finish != "stop":
                error = (f"finish_reason={finish} — repetition loop to the "
                         f"token ceiling ({data.get('usage', {}).get('output_tokens')} "
                         f"out tokens)")
        png = supp / f"{run.name}.{key}.png"
        x0, y0, x1, y1 = REGIONS[key]
        if png.is_file():
            pw, ph = png_size(png)
            scale = pw / float(x1 - x0)
            size_px = [pw, ph]
        else:
            scale = 3.0
            size_px = [int((x1 - x0) * scale), int((y1 - y0) * scale)]
        nodes.append({
            "id": f"supp.{key}",
            "level": 1,
            "class": "supplemental_region",
            "box_frame_px": [x0, y0, x1 - x0, y1 - y0],
            "estimated": False,
            "png": str(png) if png.is_file() else None,
            "parse_files": {
                "md": str(md.relative_to(run)),
                "json": str(js.relative_to(run)) if js else None,
            },
            "scale": scale,
            "size_px": size_px,
            "margin_applied": [0, 0],
            "stop_reason": "supplemental region leg" if not error else None,
            "stop_note": ("anchor-targeted re-cut outside the automated "
                          "cascade's frame-covering crop set"),
            "decision_source": "supplemental",
            "children": [],
            "transform": {
                "origin_px": [x0, y0],
                "scale": scale,
                "rule": ("frame = png_px / scale + origin_px "
                         "(scale cumulative png-per-source px; origin = png "
                         "top-left in source px)"),
            },
            "trigger": "supplemental region leg",
            "error": error,
        })
    return nodes


def main() -> None:
    for run_name in DENSE:
        run = ROOT / run_name
        manifest_path = run / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        existing = {c["id"] for c in manifest["crops"]}
        added = 0
        for node in supplement_nodes(run):
            if node["id"] in existing:
                continue
            manifest["crops"].append(node)
            added += 1
        if not added:
            print(f"{run_name}: no supplement nodes to add")
            continue
        composed_dir = run / "composed"
        composed_dir.mkdir(parents=True, exist_ok=True)
        text, patch = cc.compose_markdown(manifest, run)
        stem = manifest["slide"]
        (composed_dir / f"{stem}_composed.md").write_text(text)
        manifest["stats"].update(patch)
        manifest["stats"]["supplement_nodes"] = added
        manifest["supplement_leg"] = {
            "reason": ("anchor-targeted region re-cut outside the automated "
                       "cascade's frame-covering crop set"),
            "nodes_added": added,
        }
        cc.write_manifest(manifest, run)
        print(f"{run_name}: +{added} supplement nodes, "
              f"elements={patch['elements']}, collapsed={patch['dedup_collapsed']}")


if __name__ == "__main__":
    main()
