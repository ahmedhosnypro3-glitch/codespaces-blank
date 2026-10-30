#!/usr/bin/env python3
"""scope_r4 step-2 helper: diff certified vs fresh slide analysis.

Prints a per-field MATCH/DIVERGENT report for slide_title, verbatim_text,
layout.regions, visual_elements, colors and recreation_brief items.
Usage: r4_diff.py <NNN>   (run from the video namespace)
"""
import json
import os
import re
import sys

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def flat_strings(obj):
    out = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("description", "content", "position", "arrangement",
                         "hierarchy", "type"):
                    if isinstance(v, str):
                        out.append(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            out.append(o)
    walk(obj)
    return out


def field_report(cert, fresh, label, getter):
    c = getter(cert)
    f = getter(fresh)
    cs, fs = set(norm(x) for x in flat_strings(c)), set(norm(x) for x in flat_strings(f))
    only_c = sorted(cs - fs)
    only_f = sorted(fs - cs)
    status = "MATCH" if not only_c and not only_f else "DIVERGENT"
    print(f"\n## {label}: {status}")
    if only_c:
        print(f"  only in CERTIFIED ({len(only_c)}):")
        for s in only_c:
            print(f"    - {s[:220]}")
    if only_f:
        print(f"  only in FRESH ({len(only_f)}):")
        for s in only_f:
            print(f"    + {s[:220]}")
    if not only_c and not only_f:
        print("  (identical string sets)")
    return status


def main():
    n = sys.argv[1]
    cert_path = f"{VID}/analysis/slide_{n}_final.json"
    if not os.path.exists(cert_path):
        cert_path = f"{VID}/analysis/slide_{n}_raw.json"
        print(f"# NOTE: no certified _final.json for slide_{n}; using certified _raw.json")
    fresh_path = f"{VID}/analysis/reanalysis/slide_{n}_final.json"
    if not os.path.exists(fresh_path):
        fresh_path = f"{VID}/analysis/reanalysis/slide_{n}_raw.json"
        print(f"# NOTE: no fresh _final.json for slide_{n}; using fresh _raw.json")
    cert = json.load(open(cert_path))
    fresh = json.load(open(fresh_path))
    print(f"# certified: {cert_path}")
    print(f"# fresh:    {fresh_path}")
    statuses = []
    statuses.append(field_report(cert, fresh, "slide_title",
                                 lambda d: [d.get("slide_title", "")]))
    statuses.append(field_report(cert, fresh, "verbatim_text",
                                 lambda d: d.get("verbatim_text", {})))
    statuses.append(field_report(cert, fresh, "layout.regions",
                                 lambda d: d.get("layout", {}).get("regions", [])))
    statuses.append(field_report(cert, fresh, "visual_elements",
                                 lambda d: d.get("visual_elements", [])))
    statuses.append(field_report(cert, fresh, "colors",
                                 lambda d: d.get("colors", [])))
    statuses.append(field_report(cert, fresh, "recreation_brief",
                                 lambda d: d.get("recreation_brief", [])))
    print("\n## SUMMARY")
    for s in statuses:
        print(f"  {s}")


if __name__ == "__main__":
    main()
