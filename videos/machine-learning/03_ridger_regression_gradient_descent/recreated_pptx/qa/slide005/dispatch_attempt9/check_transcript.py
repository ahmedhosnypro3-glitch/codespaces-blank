#!/usr/bin/env python3
"""Validate a judge transcript: a real FINAL VERDICT body is required.

Certification law: a transcript counts only if it carries a genuine
`FINAL VERDICT` line. Template text echoed from the frozen prompt does NOT
count, and neither does a transcript that merely mentions the phrase.

Usage: check_transcript.py <transcript.txt> [...]
Exit 0 = every file given is a usable verdict; 1 = at least one is not.
"""
import os
import re
import sys

# A verdict line must actually assert PASS or FAIL, e.g.
#   FINAL VERDICT: PASS
#   ## FINAL VERDICT: **FAIL** - because ...
# The frozen template's instruction line reads "FINAL VERDICT: PASS or FAIL for
# ..." — that is a template echo, not an assertion, so "or" after the token is
# rejected.
VERDICT_RE = re.compile(
    r"FINAL VERDICT\s*[:\-]\s*\**\s*(PASS|FAIL)(?![A-Za-z])(?!\s+or\b)",
    re.IGNORECASE)
# Any occurrence, used to detect template-echo (mentions without an assertion).
MENTION_RE = re.compile(r"FINAL VERDICT", re.IGNORECASE)


def check(path):
    if not os.path.exists(path):
        return False, "MISSING", []
    data = open(path, "rb").read()
    if not data:
        return False, "EMPTY", []
    text = data.decode("utf-8", errors="replace")
    verdicts = VERDICT_RE.findall(text)
    mentions = MENTION_RE.findall(text)
    if not verdicts:
        return False, f"NO FINAL VERDICT ASSERTION ({len(mentions)} bare mention(s))", []
    if len(verdicts) > 1:
        # more than one assertion is ambiguous; report it rather than guess
        return False, f"AMBIGUOUS: {len(verdicts)} FINAL VERDICT assertions", verdicts
    body = text.strip()
    if len(body) < 400:
        return False, f"BODY TOO SHORT ({len(body)} chars)", verdicts
    # the verdict must be near the end of the body, not in a preamble
    tail = body[-1200:]
    if not VERDICT_RE.search(tail):
        return False, "FINAL VERDICT not in the final 1200 chars", verdicts
    return True, verdicts[0].upper(), verdicts


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    ok_all = True
    for p in sys.argv[1:]:
        ok, info, _ = check(p)
        ok_all = ok_all and ok
        print(f"{'OK  ' if ok else 'BAD '} {os.path.basename(p):45s} {info}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
