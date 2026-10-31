#!/usr/bin/env python3
"""Sweeper #3 scan: find slides with BOTH a judge_attempt_* and judge_verify_*
whose last FINAL VERDICT is PASS (original-first), not yet certified in
final_deck_ledger.json. Prints one line per candidate:
  slide<TAB>attempt_path<TAB>verify_path
"""
import json
import re
import sys
from pathlib import Path

NS = Path(__file__).resolve().parent.parent
QA = NS / "recreated_pptx" / "qa"
SKIP = {1, 3, 9, 20, 27, 28, 29}


def last_verdict(path):
    last = None
    with open(path, "rb") as f:
        for line in f:
            if b"FINAL VERDICT" in line:
                last = line.decode("utf-8", "replace")
    return last


def is_pass(path):
    v = last_verdict(path)
    return v is not None and "PASS" in v and "FAIL" not in v


def original_first(path):
    with open(path, "rb") as f:
        data = f.read()
    if b"Image 1 = original" in data:
        return True
    # fallback: the === line lists the original frame before the render
    m = re.search(rb"===\s*([^\n]*unique_slides[^\n]*)", data)
    if m:
        line = m.group(1)
        ri = line.find(b"render")
        return ri == -1 or line.find(b"unique_slides") < ri
    return False


def key_num(p):
    nums = re.findall(r"(\d+)", p.stem)
    return int(nums[-1]) if nums else -1


def main():
    ledger = json.loads((NS / "final_deck_ledger.json").read_text())
    certified = {p["slide_num"] for p in ledger["pages"] if p["status"] == "certified"}
    for d in sorted(QA.iterdir()):
        if not d.is_dir() or not d.name.startswith("slide"):
            continue
        m = re.match(r"slide_?(\d+)$", d.name)
        if not m:
            continue
        n = int(m.group(1))
        if n in certified or n in SKIP:
            continue
        att = [f for f in sorted(d.glob("judge_attempt_*.txt")) if is_pass(f) and original_first(f)]
        ver = [f for f in sorted(d.glob("judge_verify_*.txt")) if is_pass(f) and original_first(f)]
        if att and ver:
            a = max(att, key=key_num)
            v = max(ver, key=key_num)
            print(f"{n}\t{a.relative_to(NS)}\t{v.relative_to(NS)}")


if __name__ == "__main__":
    main()
