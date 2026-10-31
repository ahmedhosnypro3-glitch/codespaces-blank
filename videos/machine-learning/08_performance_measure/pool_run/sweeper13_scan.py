#!/usr/bin/env python3
"""Scan recreated_pptx/qa/slide*/ for certification state.

Emits tab-separated rows:
  DUAL\t<n>\t<attempt_pass_path>\t<verify_pass_path>     — both PASS, candidate for merge
  NEEDVERIFY\t<n>\t<attempt_pass_path>\t<newest_render>  — attempt PASS, no verify PASS
Skips slides already certified in final_deck_ledger.json.
Verdict parsing reuses pool_run/verdict.py logic (never naive grep).
"""
import glob
import json
import os
import re
import sys

NS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(NS)

_TOKEN = r"(PASS|FAIL)"


def verdict(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    hits = [m.start() for m in re.finditer(r"FINAL\s+VERDICT", text, re.I)]
    for start in reversed(hits):
        tail = text[start:]
        m = re.match(r"FINAL\s+VERDICT[^A-Za-z]{0,8}?" + _TOKEN, tail, re.I)
        if not m:
            continue
        word = m.group(1).upper()
        rest = tail[m.end():]
        # prompt echo "FINAL VERDICT: PASS or FAIL" is not a verdict
        if re.match(r"\s*or\s+FAIL", rest, re.I):
            continue
        return word
    return None


def first_pass(files):
    for f in sorted(files):
        if verdict(f) == "PASS":
            return f
    return None


with open("final_deck_ledger.json") as fh:
    certified = {p["page"] for p in json.load(fh)["pages"] if p["status"] == "certified"}

qa = "recreated_pptx/qa"
for sd in sorted(os.listdir(qa)):
    m = re.match(r"slide0*(\d+)$", sd)
    if not m:
        continue
    n = int(m.group(1))
    if n in certified:
        continue
    dp = os.path.join(qa, sd)
    att = [f for f in glob.glob(os.path.join(dp, "judge_attempt_*.txt"))
           if not f.endswith((".log", ".tmp"))]
    ver = [f for f in glob.glob(os.path.join(dp, "judge_verify_*.txt"))
           if not f.endswith((".log", ".tmp"))]
    ap, vp = first_pass(att), first_pass(ver)
    renders = sorted(glob.glob(os.path.join(dp, "render_*.png")),
                     key=os.path.getmtime)
    newest = renders[-1] if renders else ""
    if ap and vp:
        print(f"DUAL\t{n}\t{ap}\t{vp}")
    elif ap and newest:
        print(f"NEEDVERIFY\t{n}\t{ap}\t{newest}")
