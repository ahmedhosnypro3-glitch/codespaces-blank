#!/usr/bin/env python3
"""Extract the FINAL VERDICT from a judge transcript.

The vision model emits the verdict in several shapes; a naive
`grep "FINAL VERDICT: PASS"` both misses real PASSes
("### FINAL VERDICT" on its own line followed by "**PASS**") and matches
the instruction echo ("FINAL VERDICT: PASS or FAIL"). This emits exactly
PASS, FAIL, or NONE and never guesses.
"""

import re
import sys

_TOKEN = r"(PASS|FAIL)"


def verdict(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    hits = [m.start() for m in re.finditer(r"FINAL\s+VERDICT", text, re.I)]
    for start in reversed(hits):
        tail = text[start:]
        m = re.match(
            r"FINAL\s+VERDICT[^A-Za-z]{" + "0,8}?" + _TOKEN, tail, re.I
        )
        if not m:
            continue
        word = m.group(1).upper()
        rest = tail[m.end():]
        # "FINAL VERDICT: PASS or FAIL" is the prompt's instruction echoed by the
        # model, not a verdict.
        if word == "PASS" and re.match(r"\W*or\W*FAIL", rest, re.I):
            continue
        return word
    return "NONE"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: verdict.py <transcript>")
    try:
        print(verdict(sys.argv[1]))
    except OSError as e:
        print("[error] %s" % e, file=sys.stderr)
        sys.exit(2)
