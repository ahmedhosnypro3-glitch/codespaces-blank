#!/usr/bin/env python3
"""Sweeper #9 scan: find slides with BOTH a judge_attempt_* and judge_verify_*
whose LAST FINAL VERDICT line is PASS, not yet certified in final_deck_ledger.json,
no PASS row yet in verification_ledger.md, and whose slide_NNN_recreated.pptx exists.
Prints one line per candidate: slide<TAB>attempt_path<TAB>verify_path
"""
import json
import re
from pathlib import Path

NS = Path(__file__).resolve().parent.parent
QA = NS / "recreated_pptx" / "qa"
LEDGER = NS / "final_deck_ledger.json"
VLEDGER = NS / "pool_run" / "verification_ledger.md"
PPTX_DIR = NS / "recreated_pptx"


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
    m = re.search(rb"===\s*([^\n]*unique_slides[^\n]*)", data)
    if m:
        line = m.group(1)
        return line.find(b"unique_slides") < line.find(b"render_")
    return True


def key_num(p):
    nums = re.findall(r"(\d+)", p.stem)
    return int(nums[-1]) if nums else -1


def ledger_pass_slides():
    slides = set()
    for line in VLEDGER.read_text().splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|", line)
        if not m or "superseded" in line:
            continue
        cols = [c.strip() for c in line.split("|")]
        verdict = cols[4] if len(cols) > 4 else ""
        if "PASS" in verdict and "FAIL" not in verdict:
            slides.add(int(m.group(1)))
    return slides


def main():
    ledger = json.loads(LEDGER.read_text())
    certified = {p["slide_num"] for p in ledger["pages"] if p["status"] == "certified"}
    done = certified | ledger_pass_slides()
    for d in sorted(QA.iterdir()):
        if not d.is_dir() or not d.name.startswith("slide"):
            continue
        m = re.match(r"slide_?(\d+)$", d.name)
        if not m:
            continue
        n = int(m.group(1))
        if n in done:
            continue
        pptx = PPTX_DIR / f"slide_{n:03d}_recreated.pptx"
        if not pptx.exists():
            continue
        att = [f for f in sorted(d.glob("judge_attempt_*.txt")) if is_pass(f) and original_first(f)]
        ver = [f for f in sorted(d.glob("judge_verify_*.txt")) if is_pass(f) and original_first(f)]
        if att and ver:
            a = max(att, key=key_num)
            v = max(ver, key=key_num)
            print(f"{n}\t{a.relative_to(NS)}\t{v.relative_to(NS)}")


if __name__ == "__main__":
    main()
