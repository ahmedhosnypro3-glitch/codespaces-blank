#!/usr/bin/env python3
"""scope_r2: compare certified analysis vs fresh reanalysis, field by field.

Usage: diff_analysis.py <slide_num> [certified_final.json] [fresh_final.json]
Prints a MATCH/DIVERGENT table ready for qa/slideNNN/rejudge/analysis_diff.md.
"""
import json
import sys
from pathlib import Path

VID = Path("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example")


def norm(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False)


def field_rows(cert, fresh):
    rows = []

    def add(name, a, b):
        rows.append((name, norm(a) == norm(b), a, b))

    add("slide_title", cert.get("slide_title"), fresh.get("slide_title"))
    add("subtitle_or_header", cert.get("subtitle_or_header"), fresh.get("subtitle_or_header"))
    for key in ("bullets", "labels", "equations"):
        add(f"verbatim_text.{key}", cert.get("verbatim_text", {}).get(key),
            fresh.get("verbatim_text", {}).get(key))
    add("layout.arrangement", cert.get("layout", {}).get("arrangement"),
        fresh.get("layout", {}).get("arrangement"))
    add("layout.regions", cert.get("layout", {}).get("regions"),
        fresh.get("layout", {}).get("regions"))
    add("layout.hierarchy", cert.get("layout", {}).get("hierarchy"),
        fresh.get("layout", {}).get("hierarchy"))
    add("visual_elements", cert.get("visual_elements"), fresh.get("visual_elements"))
    add("imagery", cert.get("imagery"), fresh.get("imagery"))
    add("colors", cert.get("colors"), fresh.get("colors"))
    add("typography_notes", cert.get("typography_notes"), fresh.get("typography_notes"))
    add("recreation_brief", cert.get("recreation_brief"), fresh.get("recreation_brief"))
    return rows


def main():
    n = int(sys.argv[1])
    pnn = f"{n:03d}"
    cert_path = Path(sys.argv[2]) if len(sys.argv) > 2 else VID / "analysis" / f"slide_{pnn}_final.json"
    fresh_path = Path(sys.argv[3]) if len(sys.argv) > 3 else VID / "analysis" / "reanalysis" / f"slide_{pnn}_final.json"
    cert = json.load(open(cert_path))
    fresh = json.load(open(fresh_path))
    rows = field_rows(cert, fresh)
    nd = sum(1 for _, ok, _, _ in rows if not ok)
    print(f"# Analysis diff slide {pnn}: certified vs fresh")
    print(f"certified: {cert_path.name}   fresh: {fresh_path.name}")
    print(f"fields compared: {len(rows)}   DIVERGENT: {nd}   MATCH: {len(rows)-nd}")
    print()
    for name, ok, a, b in rows:
        if ok:
            print(f"- {name}: MATCH")
            continue
        print(f"- {name}: DIVERGENT")
        if name.startswith("verbatim_text.") or name in ("visual_elements", "imagery", "colors",
                                                         "recreation_brief", "layout.regions"):
            av = a if isinstance(a, list) else [a]
            bv = b if isinstance(b, list) else [b]
            sa = {norm(x) for x in av}
            sb = {norm(x) for x in bv}
            only_c = [x for x in av if norm(x) not in sb]
            only_f = [x for x in bv if norm(x) not in sa]
            for x in only_c:
                print(f"    only in CERTIFIED: {x}")
            for x in only_f:
                print(f"    only in FRESH   : {x}")
        else:
            print(f"    CERTIFIED: {norm(a)[:400]}")
            print(f"    FRESH    : {norm(b)[:400]}")
    v = fresh.get("validation", {})
    print()
    print(f"fresh validation: verdict={v.get('verdict')} "
          f"score={v.get('recreatability_score_1_to_10')} "
          f"uncertain={len(v.get('uncertain_items', []) or [])}")


if __name__ == "__main__":
    main()
