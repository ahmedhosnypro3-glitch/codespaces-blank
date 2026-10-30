#!/usr/bin/env python3
"""Side-by-side dump of first read (analysis/slide_NNN_final.json) vs
reanalysis read (analysis/reanalysis/slide_NNN_raw.json) for drift review.

Usage: compare_reads.py NNN [NNN ...]
"""
import json
import os
import re
import sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
ANALYSIS = os.path.join(NS, "analysis")
REANALYSIS = os.path.join(ANALYSIS, "reanalysis")

NUMBERS = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?%?")


def load(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def nums(text):
    return sorted(set(NUMBERS.findall(str(text))))


def show_list(label, a, b):
    print(f"\n### {label}")
    print(f"-- first ({len(a)}):")
    for i, x in enumerate(a):
        print(f"   [{i}] {x}")
    print(f"-- reanalysis ({len(b)}):")
    for i, x in enumerate(b):
        print(f"   [{i}] {x}")
    only_a = [x for x in a if x not in b]
    only_b = [x for x in b if x not in a]
    if only_a:
        print(f"   !! ONLY IN FIRST: {only_a}")
    if only_b:
        print(f"   !! ONLY IN REANALYSIS: {only_b}")
    na, nb = set(), set()
    for x in a:
        na.update(nums(x))
    for x in b:
        nb.update(nums(x))
    if na != nb:
        print(f"   !! NUMBER DIFF: first-only={sorted(na - nb)} re-only={sorted(nb - na)}")


def main():
    for n in sys.argv[1:]:
        n = str(int(n))
        fpath = os.path.join(ANALYSIS, f"slide_{n.zfill(3)}_final.json")
        rpath = os.path.join(REANALYSIS, f"slide_{n.zfill(3)}_raw.json")
        first = load(fpath)
        rean = load(rpath)
        print("=" * 100)
        print(f"SLIDE {n}   first={fpath if first else 'MISSING'}  reanalysis={'present' if rean else 'MISSING'}")
        if not rean:
            continue
        print(f"first title  : {first.get('slide_title') if first else None!r}")
        print(f"rean  title  : {rean.get('slide_title')!r}")
        print(f"first subtitle: {first.get('subtitle_or_header') if first else None!r}")
        print(f"rean  subtitle: {rean.get('subtitle_or_header')!r}")
        fv = (first or {}).get("verbatim_text", {}) or {}
        rv = rean.get("verbatim_text", {}) or {}
        for key in ("bullets", "labels", "equations"):
            show_list(key.upper(), fv.get(key) or [], rv.get(key) or [])
        fve = (first or {}).get("visual_elements") or []
        rve = rean.get("visual_elements") or []
        print(f"\n### VISUAL ELEMENTS  (first={len(fve)}, reanalysis={len(rve)})")
        for i, e in enumerate(fve):
            print(f"   F[{i}] ({e.get('type')}) {e.get('description')} | colors={e.get('colors')} | pos={e.get('position')}")
        for i, e in enumerate(rve):
            print(f"   R[{i}] ({e.get('type')}) {e.get('description')} | colors={e.get('colors')} | pos={e.get('position')}")
        fi = (first or {}).get("imagery") or []
        ri = rean.get("imagery") or []
        show_list("IMAGERY", fi, ri)
        print(f"\n### COLORS\n   first: {json.dumps((first or {}).get('colors'))}\n   rean : {json.dumps(rean.get('colors'))}")
        print(f"\n### TYPOGRAPHY\n   first: {(first or {}).get('typography_notes')}\n   rean : {rean.get('typography_notes')}")
        print(f"\n### ANIMATION\n   first: {(first or {}).get('animation_state')}\n   rean : {rean.get('animation_state')}")
        print(f"\n### REANALYSIS _meta: {rean.get('_meta')}")


if __name__ == "__main__":
    main()
