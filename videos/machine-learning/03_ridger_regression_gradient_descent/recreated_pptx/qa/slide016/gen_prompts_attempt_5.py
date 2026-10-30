#!/usr/bin/env python3
"""Attempt-5 payload regeneration (worker-016-finish-20261024).

Sources the Template A / Template B `-p` payloads byte-for-byte from
shared_patterns/judge_protocol_03.md and applies ONLY the protocol substitutions:
  NNN -> 016 (word-boundary safe), K -> 5 (word-boundary safe)
BLOCKER must stay intact (no BLOC1ER corruption).
"""
import re

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
PROTO = (f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent/"
         "shared_patterns/judge_protocol_03.md")
QA = (f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent/"
      "recreated_pptx/qa/slide016")

import re

md = open(PROTO, encoding="utf-8").read()

def payload_of(idx):
    """Extract the -p payload from the idx-th judge block (0=Template A, 1=Template B)."""
    blocks = [b for b in re.findall(r"```(.*?)```", md, re.S) if '-p "' in b]
    block = blocks[idx]
    p = block.index('-p "') + len('-p "')
    q = block.rindex('"')                      # payload contains no double quotes
    return block[p:q]

tplA = payload_of(0)
tplB = payload_of(1)

def subst(t, nnn="016", k="5"):
    t = re.sub(r"\bNNN\b", nnn, t)
    t = re.sub(r"\bK\b", k, t)
    return t

pA = subst(tplA)
pB = subst(tplB)

outA = f"{QA}/judge_prompt_5A.txt"
outB = f"{QA}/judge_prompt_5B.txt"
open(outA, "w", encoding="utf-8").write(pA)
open(outB, "w", encoding="utf-8").write(pB)

for tag, path, body in [("A", outA, pA), ("B", outB, pB)]:
    raw = open(path, "rb").read()
    print(f"Template {tag}: {path} {len(raw)} B | "
          f"BLOCKER x{body.count('BLOCKER')} | BLOC1ER x{body.count('BLOC1ER')} | "
          f"FINAL VERDICT x{body.count('FINAL VERDICT:')} | NNN left x{body.count('NNN')} | "
          f"bare-K left x{len(re.findall(chr(92)+'bK'+chr(92)+'b', body))}")

print("Template A payload head:", pA[:80])
print("Template B payload head:", pB[:80])
print("Template B contains 'slide 016':", "slide 016" in pB)
