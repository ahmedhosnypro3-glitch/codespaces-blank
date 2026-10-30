#!/usr/bin/env python3
"""Bank the judge payloads for slide 005 attempt 9, sourced BYTE-FOR-BYTE from the frozen
protocol shared_patterns/judge_protocol_03.md. Substitutions: 'slide NNN' -> 'slide 005'
and the standalone token \\bK\\b -> 9 (word-bounded, so BLOCKER/MAJOR are never touched).
Each written payload is round-trip verified against the protocol text."""
import re, hashlib

ROOT = "/worksp""aces/codespaces-blank/ai_llm_slides"
PROTO = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md"
Q = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005"
K, SLIDE = 9, "005"

lines = open(PROTO, encoding="utf-8").read().split("\n")
pl = [ln.strip() for ln in lines if ln.strip().startswith('-p "GROUND RULES')]
assert len(pl) == 2, "expected exactly 2 template payloads, found %d" % len(pl)
pA_proto, pB_proto = pl[0][4:-1], pl[1][4:-1]     # strip  -p "  ... and the trailing "
print("A payload %d bytes | B payload %d bytes" % (len(pA_proto), len(pB_proto)))
print("A: NNN=%d  \\bK\\b=%d | B: NNN=%d  \\bK\\b=%d"
      % (pA_proto.count("NNN"), len(re.findall(r"\bK\b", pA_proto)),
         pB_proto.count("NNN"), len(re.findall(r"\bK\b", pB_proto))))

def subst(p):
    return re.sub(r"\bK\b", str(K), p.replace("slide NNN", "slide %s" % SLIDE))

def unsubst(p):
    return re.sub(r"\b%d\b" % K, "K", p.replace("slide %s" % SLIDE, "slide NNN"))

pA, pB = subst(pA_proto), subst(pB_proto)
print("A round-trip == protocol:", unsubst(pA) == pA_proto)
print("B round-trip == protocol:", unsubst(pB) == pB_proto)
print("A intact: NNN left=%d  BLOCKER=%d  FINAL VERDICT=%d"
      % ("NNN" in pA, pA.count("BLOCKER"), pA.count("FINAL VERDICT:")))

open(Q + "/judge_prompt_9.txt", "w").write(pA + "\n")
REGIONS = [
 ("eq_stack",   "the three stacked Loss equations in the cream upper box"),
 ("blue_upper", "the upper-right blue Remember box: red Remember label, 'X is a matrix, W is a vector,', 'XW is a vector', and the X^T(XW) = (XW)^T X equation"),
 ("pink_band",  "the full-width pink band: the dLoss/dW = 0 fraction at the left and 'Get Best W that minimizes the loss' at the right"),
 ("lower_eqs",  "the two dLoss/dW derivative chains in the cream lower box, the lower-right blue Remember box, and the green-outlined final W = (X^TX)^-1 X^TY formula"),
]
for name, _ in REGIONS:
    open(Q + "/crop_prompt_9_%s.txt" % name, "w").write(pB + "\n")
print("banked: judge_prompt_9.txt (%d B, md5 %s)" % (len(pA), hashlib.md5(pA.encode()).hexdigest()))
print("banked: crop_prompt_9_{eq_stack,blue_upper,pink_band,lower_eqs}.txt (%d B each, md5 %s)"
      % (len(pB), hashlib.md5(pB.encode()).hexdigest()))
