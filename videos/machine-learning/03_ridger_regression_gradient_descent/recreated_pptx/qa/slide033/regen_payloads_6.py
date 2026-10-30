#!/usr/bin/env python3
"""Regenerate slide 033's judge payloads byte-for-byte from the frozen protocol.

`shared_patterns/judge_protocol_03.md` states: "Every judge prompt for this deck
sources its `-p` payload byte-for-byte from the templates below (substitute only
NNN and K)". Verified this session:

  * judge_prompt_3.txt  (Template A)        4115 bytes -> VERBATIM in protocol  OK
  * judge_crop_prompt_*.txt (crop payloads) 8969 bytes -> NOT in the protocol  BAD

The bad crop payloads are a composite (Template A's long ground-rules block +
Template B's zoomed body). Template B's own `-p` is ONE self-contained payload on
protocol line 117 (1914 chars) whose clause (b) already carries a condensed
version of the chrome ground rules. Using the composite would violate the
byte-for-byte law. This script re-extracts both templates verbatim, substitutes
only NNN/K, and banks clean copies (old ones kept as evidence, per the law).
"""
PROTO = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md")
QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033")

NNN, K = "33", "6"
lines = open(PROTO).read().splitlines()


def payload_from_line(idx):
    """A template's -p value is the remainder of the line after '-p \"', with the
    trailing '\"' stripped."""
    l = lines[idx].strip()
    assert l.startswith('-p "'), f"line {idx} does not start with -p: {l[:40]}"
    body = l[len('-p "'):]
    assert body.endswith('"'), f"line {idx} does not end with a quote"
    return body[:-1]


# Template A / Template B payloads: find their `-p "` lines by content
idxA = [i for i, l in enumerate(lines)
        if l.strip().startswith('-p "') and "usable recreation'" in l]
idxB = [i for i, l in enumerate(lines)
        if l.strip().startswith('-p "') and 'ZOOMED CROP-PAIR' in l]
assert len(idxA) == 1, f"Template A -p lines found: {idxA}"
assert len(idxB) == 1, f"Template B -p lines found: {idxB}"


def payload_from_line(idx):
    """A template's -p value is the remainder of the line after '-p \"', with the
    trailing '\"' stripped."""
    l = lines[idx].strip()
    assert l.startswith('-p "'), f"line {idx} does not start with -p: {l[:40]}"
    body = l[len('-p "'):]
    assert body.endswith('"'), f"line {idx} does not end with a quote"
    return body[:-1]


tmplA = payload_from_line(idxA[0])
tmplB = payload_from_line(idxB[0])

outA = tmplA.replace("slide NNN", f"slide {NNN}")
outB = tmplB.replace("slide NNN", f"slide {NNN}")

open(f"{QA}/judge_payload_A_k{K}.txt", "w").write(outA)
open(f"{QA}/judge_payload_B_k{K}.txt", "w").write(outB)

# verify
oldA = open(f"{QA}/judge_prompt_3.txt").read().strip()
oldB = open(f"{QA}/judge_crop_prompt_plot.txt").read().strip()
print(f"Template A: protocol {len(tmplA)} -> banked {len(outA)}")
print(f"  old judge_prompt_3.txt identical to regenerated: {oldA == outA.strip()}")
print(f"Template B: protocol {len(tmplB)} -> banked {len(outB)}")
print(f"  old judge_crop_prompt_plot.txt identical to regenerated: {oldB == outB.strip()}")
print(f"  old composite payload length was {len(oldB)} (Template A rules + Template B body)")
print()
print("banked:")
print(f"  {QA}/judge_payload_A_k{K}.txt  (Template A, full-slide)")
print(f"  {QA}/judge_payload_B_k{K}.txt  (Template B, crop-pair)")
