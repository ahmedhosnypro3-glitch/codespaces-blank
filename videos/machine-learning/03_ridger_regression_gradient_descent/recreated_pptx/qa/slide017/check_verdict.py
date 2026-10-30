#!/usr/bin/env python3
"""Extract the real verdict from a judge transcript (slide 017).

A transcript counts as a verdict ONLY if it carries a genuine
"FINAL VERDICT: PASS" / "FINAL VERDICT: FAIL" line. The frozen template's own
prose ends with "End with: FINAL VERDICT: PASS or FAIL ..." — an echo of that
instruction is NOT a verdict, so a match containing "or FAIL" / "PASS or" is
rejected. A file with no genuine verdict line is VOID (no evidence).

Usage: python3 check_verdict.py <transcript> [<transcript> ...]
Exit: 0 if every listed transcript is a real verdict, 1 otherwise.
"""
import re
import sys

GENUINE = re.compile(r"^\s*[#*\s]*FINAL VERDICT:\s*\**(PASS|FAIL)", re.M | re.I)
ECHO = re.compile(r"FINAL VERDICT:\s*PASS\s+or\s+FAIL", re.I)

rc = 0
for path in sys.argv[1:]:
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as e:
        print("%-58s MISSING (%s)" % (path, e))
        rc = 1
        continue
    lines = [ln for ln in text.splitlines() if GENUINE.search(ln)]
    echos = len(ECHO.findall(text))
    if not lines:
        print("%-58s VOID (no genuine FINAL VERDICT line; echo-of-template lines=%d)"
              % (path, echos))
        rc = 1
        continue
    verdicts = set(GENUINE.search(ln).group(1).upper() for ln in lines)
    print("%-58s VERDICT=%s (%d verdict line(s), echo-of-template lines=%d)"
          % (path, "/".join(sorted(verdicts)), len(lines), echos))
    if len(verdicts) > 1:
        print("    WARNING: conflicting verdict lines")
        rc = 1

sys.exit(rc)
