#!/usr/bin/env python3
"""Lane E health check for one crop-cascade run dir.

PASS requires all of:
  - manifest.json present, budgets honored (parse_calls_spent <= max_parse_calls,
    crops_spent <= max_crops, levels_processed <= max_depth)
  - every *.parse.json has finish_reason=stop and non-empty content
  - composed/<stem>_composed.md present and non-empty
Exit 0 = PASS, 1 = FAIL. Prints one line per check.
"""
import json
import sys
from pathlib import Path


def main() -> int:
    outdir = Path(sys.argv[1])
    problems = []

    manifest_path = outdir / "manifest.json"
    manifest = None
    if not manifest_path.exists():
        problems.append("manifest.json missing")
    else:
        try:
            manifest = json.loads(manifest_path.read_text())
        except Exception as e:
            problems.append(f"manifest.json unreadable: {e}")
    if manifest:
        caps = manifest.get("caps", {})
        checks = [
            ("parse_calls_spent", "max_parse_calls"),
            ("crops_spent", "max_crops"),
        ]
        for spent_key, cap_key in checks:
            spent = manifest.get(spent_key)
            cap = caps.get(cap_key)
            if spent is None or cap is None:
                problems.append(f"manifest missing {spent_key}/{cap_key}")
            elif spent > cap:
                problems.append(f"budget exceeded: {spent_key}={spent} > {cap_key}={cap}")
        levels = (manifest.get("recursion") or {}).get("levels_processed")
        max_depth = caps.get("max_depth")
        if levels is None or max_depth is None:
            problems.append("manifest missing recursion.levels_processed/max_depth")
        elif levels > max_depth:
            problems.append(f"depth exceeded: levels={levels} > max_depth={max_depth}")
        print(f"manifest: parse_calls={manifest.get('parse_calls_spent')}/{caps.get('max_parse_calls')} "
              f"crops={manifest.get('crops_spent')}/{caps.get('max_crops')} "
              f"levels={levels}/{max_depth} degraded={manifest.get('degraded')}")

    parse_jsons = sorted(outdir.rglob("*.parse.json"))
    if not parse_jsons:
        problems.append("no *.parse.json found")
    bad = 0
    for pj in parse_jsons:
        try:
            d = json.loads(pj.read_text())
        except Exception as e:
            problems.append(f"{pj.relative_to(outdir)} unreadable: {e}")
            bad += 1
            continue
        fr = d.get("finish_reason")
        clen = len((d.get("content") or "").strip())
        if fr != "stop" or clen == 0:
            problems.append(f"{pj.relative_to(outdir)} finish_reason={fr} content_len={clen}")
            bad += 1
    print(f"parse.json files: {len(parse_jsons)} total, {bad} bad (need finish_reason=stop, non-empty)")

    composed = sorted((outdir / "composed").glob("*_composed.md")) if (outdir / "composed").is_dir() else []
    if not composed:
        problems.append("composed transcript missing (composed/*_composed.md)")
    else:
        for c in composed:
            n = len(c.read_text(errors="replace").strip())
            print(f"composed: {c.name} {n} chars")
            if n == 0:
                problems.append(f"composed transcript empty: {c.name}")

    if problems:
        print("FAIL:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
