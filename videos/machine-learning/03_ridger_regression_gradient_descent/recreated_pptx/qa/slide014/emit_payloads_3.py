#!/usr/bin/env python3
"""Bank byte-for-byte payloads for slide014 judge legs, per the payload-hygiene law.

Frozen template = shared_patterns/judge_protocol_03.md ("substitute only NNN and K").
Substitutions applied:
  - bare token NNN        -> 014   (word-boundary regex; Template B only)
  - STANDALONE token K    -> 3     (\\bK\\b so BLOCKER is never corrupted)
No other edit. Each banked file is byte-checked against a fresh re-derivation.
"""
import hashlib
import re
import sys

import pathlib

PROTO = pathlib.Path(
    "videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md")
QA = pathlib.Path(
    "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014")

lines = PROTO.read_text(encoding="utf-8").split("\n")


def block(a, b):
    return "\n".join(lines[a - 1:b])


def payload_of(b):
    m = re.search(r'-p "(.*)"\s*$', b, re.S)
    assert m, "no -p payload in template"
    return m.group(1)


TPL = {"A": payload_of(block(62, 71)), "B": payload_of(block(108, 117))}
K = sys.argv[1] if len(sys.argv) > 1 else "3"


def substitute(t):
    t = re.sub(r"\bNNN\b", "014", t)   # slide number token
    t = re.sub(r"\bK\b", K, t)         # attempt token, word-boundary safe
    return t


for tag, tpl in TPL.items():
    sub = substitute(tpl)
    f = QA / f"payload_{tag}_{K}.txt"
    f.write_text(sub, encoding="utf-8")
    assert substitute(tpl) == f.read_text(encoding="utf-8"), f"byte-check failed {tag}"
    print(f"{f.name}: len={len(sub)} md5={hashlib.md5(sub.encode()).hexdigest()}")

    # corruption guards: BLOCKER intact, no leftover tokens
    assert "BLOCKER" in sub, "BLOCKER lost!"
    assert not re.search(r"BLOC[0-9]+ER", sub), "BLOCKER corrupted!"
    assert not re.search(r"\bNNN\b", sub), "leftover NNN"
    assert not re.search(r"\bK\b", sub), "leftover K"
    n_nnn = len(re.findall(r"\bNNN\b", tpl))
    n_k = len(re.findall(r"\bK\b", tpl))
    print(f"   template tokens substituted: NNN x{n_nnn}, K x{n_k}  "
          f"-> '014' x{sub.count('014')}, '{K}' x{len(re.findall(chr(92)+'b'+K+chr(92)+'b', sub))}")

print("payloads byte-checked, tokens fully substituted, BLOCKER intact")
