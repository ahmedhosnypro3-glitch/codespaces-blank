#!/usr/bin/env python3
"""Side-by-side dump of first read vs reanalysis read for the 27-37 sweep."""
import json
import os
import sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
ANA = os.path.join(NS, "analysis")
RE = os.path.join(ANA, "reanalysis")


def load_first(n):
    final = os.path.join(ANA, f"slide_{n:03d}_final.json")
    if os.path.exists(final):
        return json.load(open(final)), "final"
    raw = os.path.join(ANA, f"slide_{n:03d}_raw.json")
    if os.path.exists(raw):
        return json.load(open(raw)), "raw"
    return None, "NONE"


def load_re(n):
    p = os.path.join(RE, f"slide_{n:03d}_raw.json")
    return json.load(open(p)) if os.path.exists(p) else None


def block(d, tag):
    print(f"--- {tag} ---")
    if d is None:
        print("  (missing)")
        return
    print("TITLE:", json.dumps(d.get("slide_title"), ensure_ascii=False))
    vt = d.get("verbatim_text") or {}
    for k in ("bullets", "labels", "equations"):
        vals = vt.get(k) or []
        print(f"{k.upper()} ({len(vals)}):")
        for v in vals:
            print("   *", v)
    print("VISUAL_ELEMENTS:")
    for i, ve in enumerate(d.get("visual_elements") or []):
        print(f"  [{i}] type={ve.get('type')}")
        print(f"      desc: {ve.get('description')}")
        print(f"      pos: {ve.get('position')}")


for n in (int(a) for a in sys.argv[1:]):
    first, kind = load_first(n)
    re = load_re(n)
    print("=" * 100)
    print(f"SLIDE {n}   first_read={kind}   reanalysis={'present' if re else 'MISSING'}")
    print("=" * 100)
    block(first, f"FIRST READ ({kind})")
    print()
    block(re, "REANALYSIS")
    print()
