#!/usr/bin/env python3
"""Compact dump of first-read / reanalysis fields for slides 1-13 (drift prep)."""
import json, os, sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/analysis"

def summarize(path):
    with open(path) as f:
        d = json.load(f)
    vt = d.get("verbatim_text", {}) or {}
    out = {
        "title": d.get("slide_title"),
        "bullets": vt.get("bullets", []),
        "labels": vt.get("labels", []),
        "equations": vt.get("equations", []),
    }
    ve = d.get("visual_elements", []) or []
    out["visuals"] = [
        {"type": v.get("type"), "desc": (v.get("description") or "")[:400]} for v in ve
    ]
    return out

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "first"
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else 13
    for n in range(lo, hi + 1):
        if mode == "first":
            cand = [f"slide_{n:03d}_final.json", f"slide_{n:03d}_raw.json"]
        else:
            cand = [f"reanalysis/slide_{n:03d}_raw.json"]
        found = None
        for c in cand:
            p = os.path.join(BASE, c)
            if os.path.exists(p):
                found = (c, p)
                break
        print(f"\n########## SLIDE {n:03d} ({mode}) ##########")
        if not found:
            print("NO FILE FOUND")
            continue
        name, path = found
        try:
            s = summarize(path)
        except Exception as e:
            print(f"PARSE FAIL {name}: {e}")
            continue
        print(f"[file: {name}]")
        print("TITLE:", json.dumps(s["title"], ensure_ascii=False))
        print("BULLETS:", json.dumps(s["bullets"], ensure_ascii=False, indent=1))
        print("LABELS:", json.dumps(s["labels"], ensure_ascii=False, indent=1))
        print("EQUATIONS:", json.dumps(s["equations"], ensure_ascii=False, indent=1))
        for i, v in enumerate(s["visuals"], 1):
            print(f"  V{i} [{v['type']}] {v['desc']}")

main()
