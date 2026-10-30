#!/usr/bin/env python3
"""Structured drift diff: first read (final|raw) vs reanalysis raw, slides 1-13.

Emits normalized set differences for title/bullets/labels/equations plus a
numeric-token delta extracted from visual_elements descriptions, pairing
near-matches with difflib so cosmetic rewording is separated from material
missing/extra content.
"""
import difflib
import json
import os
import re
import sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/analysis"


def norm(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[\"“”'‘’`]", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip(" .,:;()[]{}")
    return s


def load(path):
    with open(path) as f:
        return json.load(f)


def fields(d):
    vt = d.get("verbatim_text") or {}
    return {
        "title": d.get("slide_title") or "",
        "bullets": list(vt.get("bullets") or []),
        "labels": list(vt.get("labels") or []),
        "equations": list(vt.get("equations") or []),
    }


def ve_text(d):
    out = []
    for v in d.get("visual_elements") or []:
        out.append(f"{v.get('type','')}: {v.get('description','')}")
    return " \n".join(out)


def nums(text):
    """Numeric tokens with optional %, preserving order-unique set."""
    found = re.findall(r"-?\d+(?:\.\d+)?\s?%?", text or "")
    return sorted(set(f.strip() for f in found if f.strip() and f.strip() != "%"))


def diff_list(field, first, second, sim=0.72):
    """Return (missing_in_second, extra_in_second, reworded_pairs)."""
    nf = [(x, norm(x)) for x in first]
    ns = [(x, norm(x)) for x in second]
    used = set()
    missing, reworded = [], []
    for raw_f, key_f in nf:
        if not key_f:
            continue
        best, best_i = 0.0, None
        for i, (raw_s, key_s) in enumerate(ns):
            if i in used or not key_s:
                continue
            r = difflib.SequenceMatcher(None, key_f, key_s).ratio()
            if r > best:
                best, best_i = r, i
        if best >= sim and best_i is not None:
            used.add(best_i)
            if norm(ns[best_i][0]) != key_f:
                reworded.append((raw_f, ns[best_i][0], round(best, 3)))
        else:
            missing.append(raw_f)
    extra = [raw_s for i, (raw_s, _) in enumerate(ns) if i not in used and norm(raw_s)]
    return missing, extra, reworded


def main():
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 13
    for n in range(lo, hi + 1):
        first_path = None
        for cand in (f"slide_{n:03d}_final.json", f"slide_{n:03d}_raw.json"):
            p = os.path.join(BASE, cand)
            if os.path.exists(p):
                first_path = p
                break
        re_path = os.path.join(BASE, "reanalysis", f"slide_{n:03d}_raw.json")
        print(f"\n===== SLIDE {n:03d} =====")
        if first_path is None:
            print("FIRST READ: NONE")
        else:
            print(f"FIRST READ FILE: {os.path.basename(first_path)}")
        if not os.path.exists(re_path):
            print("REANALYSIS: NOT YET PRESENT")
            continue
        fd = load(first_path)
        rd = load(re_path)
        ff, rf = fields(fd), fields(rd)
        print(f"TITLE first: {ff['title']!r}")
        print(f"TITLE re  : {rf['title']!r}")
        print(f"TITLE ratio: {difflib.SequenceMatcher(None, norm(ff['title']), norm(rf['title'])).ratio():.3f}")
        for field in ("bullets", "labels", "equations"):
            miss, extra, rew = diff_list(field, ff[field], rf[field])
            print(f"-- {field}: first={len(ff[field])} re={len(rf[field])}")
            if miss:
                print(f"   MISSING_IN_RE: {json.dumps(miss, ensure_ascii=False)}")
            if extra:
                print(f"   EXTRA_IN_RE  : {json.dumps(extra, ensure_ascii=False)}")
            if rew:
                print(f"   REWORDED     : {json.dumps(rew, ensure_ascii=False)}")
        fn, rn = nums(ve_text(fd)), nums(ve_text(rd))
        only_f = [x for x in fn if x not in rn]
        only_r = [x for x in rn if x not in fn]
        if only_f or only_r:
            print(f"-- NUMBERS only_in_first: {only_f}")
            print(f"-- NUMBERS only_in_re   : {only_r}")


main()
