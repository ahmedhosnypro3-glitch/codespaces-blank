#!/usr/bin/env python3
"""Regenerate slide 033's judge payloads byte-for-byte from the frozen protocol —
attempt 9 (render_9.png, == the current pptx byte-for-byte).

Protocol law: "Every judge prompt for this deck sources its `-p` payload
byte-for-byte from the templates below (substitute only NNN and K)."

Orchestrator directive (2026-10-24): any substitution inside a payload file is
\bK\b-only, byte-checked against source. Verified here: neither Template A nor
Template B's `-p` body contains a standalone `K` token or an `NNN` token after
the `slide NNN` -> `slide 33` substitution, so the payloads are attempt-static;
the attempt number appears ONLY in the file names, the transcript paths and the
--view strings. The digit runs '6'/'8' inside payload A are the protocol's own
dates (2026-10-10 / 2026-10-09), not a K substitution.

Output: judge_payload_A_k9.txt / judge_payload_B_k9.txt
"""
import re
import sys

PROTO = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md")
QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033")

NNN, K = "33", "9"
lines = open(PROTO).read().splitlines()


def payload_from_line(idx):
    l = lines[idx].strip()
    assert l.startswith('-p "'), f"line {idx + 1} does not start with -p: {l[:40]}"
    body = l[len('-p "'):]
    assert body.endswith('"'), f"line {idx + 1} does not end with a quote"
    return body[:-1]


idxA = [i for i, l in enumerate(lines)
        if l.strip().startswith('-p "') and "usable recreation'" in l]
idxB = [i for i, l in enumerate(lines)
        if l.strip().startswith('-p "') and 'ZOOMED CROP-PAIR' in l]
assert len(idxA) == 1, f"Template A -p lines found: {idxA}"
assert len(idxB) == 1, f"Template B -p lines found: {idxB}"

tmplA = payload_from_line(idxA[0])
tmplB = payload_from_line(idxB[0])

outA = tmplA.replace("slide NNN", f"slide {NNN}")
outB = tmplB.replace("slide NNN", f"slide {NNN}")

fail = False
for tag, tmpl, out in (("A", tmplA, outA), ("B", tmplB, outB)):
    if "NNN" in out:
        print(f"Template {tag}: FAIL — an NNN placeholder survived"); fail = True
    if re.search(r"\bK\b", out):
        print(f"Template {tag}: FAIL — a standalone K token is present"); fail = True
    # Template A's -p carries no slide reference (the NNN lives in the shared
    # prelude at protocol line 37, which is not part of the -p payload), so the
    # slide-33 assertion only applies to Template B.
    if tag == "B" and "slide 33" not in out:
        print(f"Template {tag}: FAIL — slide 33 not present"); fail = True
    if not (tmpl in open(PROTO).read()):
        print(f"Template {tag}: FAIL — template not a byte-substring of the protocol"); fail = True
    # the substitution is exactly the mandated one
    back = out.replace("slide 33", "slide NNN")
    if back != tmpl:
        print(f"Template {tag}: FAIL — substitution not reversible"); fail = True
if fail:
    sys.exit(1)

open(f"{QA}/judge_payload_A_k{K}.txt", "w").write(outA)
open(f"{QA}/judge_payload_B_k{K}.txt", "w").write(outB)

print(f"Template A: protocol {len(tmplA)} -> banked {len(outA)}  [protocol line {idxA[0] + 1}]")
print(f"Template B: protocol {len(tmplB)} -> banked {len(outB)}  [protocol line {idxB[0] + 1}]")
print("byte-for-byte + \\bK\\b-only + NNN-fully-substituted: PASS")
print(f"banked: {QA}/judge_payload_A_k{K}.txt , judge_payload_B_k{K}.txt")
