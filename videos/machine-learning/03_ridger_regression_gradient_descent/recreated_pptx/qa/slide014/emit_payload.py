#!/usr/bin/env python3
"""Emit the Template A / Template B judge payloads byte-for-byte from
shared_patterns/judge_protocol_03.md, substituting NNN and K only.

Usage:
  python3 emit_payload.py A 014 2 > /tmp/pA.txt
  python3 emit_payload.py B 014 2 <NAME> "<region description>" > /tmp/pB.txt
"""
import sys

PROTO = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md")

lines = open(PROTO, encoding="utf-8").read().split("\n")
which, nnn, k = sys.argv[1], sys.argv[2], sys.argv[3]

# The payload is the single -p "..." line inside each fenced code block.
# Locate the fence that follows the template heading, then the -p line.
def find_payload(anchor):
    for i, ln in enumerate(lines):
        if anchor in ln:
            # scan forward for the line starting with '  -p "'
            for j in range(i, min(i + 40, len(lines))):
                if lines[j].lstrip().startswith('-p "'):
                    raw = lines[j].lstrip()
                    assert raw.endswith('"'), "unterminated -p line"
                    return raw[len('-p "'):-1]
    raise SystemExit(f"payload anchor not found: {anchor}")

if which == "A":
    p = find_payload("Comparison (the real judge")
    out = p.replace("NNN", nnn).replace("_K", "_" + k)
    sys.stdout.write(out)
elif which == "B":
    name = sys.argv[4]
    region = sys.argv[5]
    p = find_payload("Template B — crop-pair judge")
    out = p.replace("NNN", nnn).replace("_K", "_" + k)
    out = out.replace("crop_K_NAME_render", f"crop_{k}_{name}_render")
    out = out.replace("crop_K_NAME_orig", f"crop_{k}_{name}_orig")
    out = out.replace("crop_K_NAME_judge", f"crop_{k}_{name}_judge")
    out = out.replace("<one-line description of what the region contains>", region)
    out = out.replace("NAME", name)
    sys.stdout.write(out)
else:
    raise SystemExit("usage: emit_payload.py A|B NNN K [NAME] [REGION]")
