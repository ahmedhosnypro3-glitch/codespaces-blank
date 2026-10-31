#!/usr/bin/env python3
"""Sweeper #11 scan for 08_performance_measure.

Emits one line per actionable slide:
  DUAL\t<n>\t<attempt_path>\t<verify_path>   — both attempt and verify PASS,
      not yet certified in final_deck_ledger.json, slide_NNN_recreated.pptx exists.
  NEEDVERIFY\t<n>\t<attempt_path>\t<render_path> — latest attempt PASS, no verify
      PASS for any judge_verify_*, slide_NNN_recreated.pptx exists, and a render
      at least as new as the pptx exists.
Verdicts read with pool_run/verdict.py (strict FINAL VERDICT semantics).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

NS = Path(__file__).resolve().parent.parent
QA = NS / "recreated_pptx" / "qa"
LEDGER = NS / "final_deck_ledger.json"
PPTX_DIR = NS / "recreated_pptx"
VERDICT = NS / "pool_run" / "verdict.py"
PY = sys.executable or "python3"


def verdict(path):
    try:
        out = subprocess.run([PY, str(VERDICT), str(path)],
                             capture_output=True, text=True, timeout=30)
        return out.stdout.strip()
    except Exception:
        return "NONE"


def slide_nums():
    for d in sorted(QA.iterdir()):
        m = re.fullmatch(r"slide0*(\d+)", d.name)
        if m and d.is_dir():
            yield int(m.group(1)), d


def pass_files(d, pattern):
    out = []
    for f in sorted(d.glob(pattern), key=lambda p: p.name):
        if verdict(f) == "PASS":
            out.append(f)
    return out


def newest_render(d):
    renders = sorted(d.glob("render_*.png"),
                     key=lambda p: p.stat().st_mtime)
    return renders[-1] if renders else None


def main():
    ledger = json.load(open(LEDGER))
    certified = {int(p["page"]) for p in ledger["pages"]
                 if p.get("status") == "certified"}
    for n, d in slide_nums():
        pptx = PPTX_DIR / f"slide_{n:03d}_recreated.pptx"
        if not pptx.exists():
            continue
        attempts = pass_files(d, "judge_attempt_*.txt")
        verifies = pass_files(d, "judge_verify_*.txt")
        if n not in certified and attempts and verifies:
            print(f"DUAL\t{n}\t{attempts[-1]}\t{verifies[-1]}")
            continue
        if n in certified:
            continue
        if attempts and not verifies:
            r = newest_render(d)
            if r is None or r.stat().st_mtime < pptx.stat().st_mtime:
                continue
            print(f"NEEDVERIFY\t{n}\t{attempts[-1]}\t{r}")


if __name__ == "__main__":
    main()
