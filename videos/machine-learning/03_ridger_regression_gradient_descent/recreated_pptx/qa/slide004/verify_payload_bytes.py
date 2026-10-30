"""Strict payload byte-check for slide 004 attempt 7.

Extracts the `-p "..."` payload byte-for-byte from the frozen protocol
(shared_patterns/judge_protocol_03.md), applies only the substitutions the
protocol sanctions (NNN, K, NAME, region description), and compares bytes
against the staged prompt files used by the attempt-7 judge scripts.
"""

import hashlib
import re
from pathlib import Path

PROTOCOL = Path("shared_patterns/judge_protocol_03.md")
QA = Path("recreated_pptx/qa/slide004")


def payload_of(block: str) -> str:
    """Return the exact bytes of the -p payload inside a frozen command block."""
    start = block.index('-p "') + len('-p "')
    end = block.rindex('"')
    return block[start:end]


def sha(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


text = PROTOCOL.read_text(encoding="utf-8")
blocks = re.findall(r"```\n(.*?)\n```", text, re.S)
template_a = next(b for b in blocks if "-p \"" in b and "fidelity check vs original" in b)
template_b = next(b for b in blocks if "-p \"" in b and "ZOOMED CROP-PAIR" in b)

pa = payload_of(template_a)
pb = payload_of(template_b)

print("frozen Template A payload: %d bytes sha256=%s" % (len(pa.encode()), sha(pa)))
print("frozen Template B payload: %d bytes sha256=%s" % (len(pb.encode()), sha(pb)))
print()
print("Template A payload in-payload placeholder inventory:")
for token in ("NNN", "K", "NAME"):
    hits = len(re.findall(r"\b%s\b" % token, pa))
    print("  \\b%s\\b -> %d occurrence(s)" % (token, hits))
print("Template B payload in-payload placeholder inventory:")
for token in ("NNN", "K", "NAME"):
    hits = len(re.findall(r"\b%s\b" % token, pb))
    print("  \\b%s\\b -> %d occurrence(s)" % (token, hits))
print()

results = []

# Template A: NNN -> 004, K -> 7 (word-boundary substitutions only).
exp_a = re.sub(r"\bNNN\b", "004", pa)
exp_a = re.sub(r"\bK\b", "7", exp_a)
got_a = (QA / "judge_prompt_7.txt").read_text(encoding="utf-8")
results.append(("judge_prompt_7.txt vs Template A (NNN->004, K->7)", exp_a, got_a))

# Template B: NNN -> 004, K -> 7, NAME -> region slug, description -> region text.
for name, slug in (("remember", "remember"), ("let_boxes", "let_boxes")):
    desc = (QA / ("crop_7_%s_desc.txt" % name)).read_text(encoding="utf-8").strip()
    exp_b = re.sub(r"\bNNN\b", "004", pb)
    exp_b = re.sub(r"\bK\b", "7", exp_b)
    exp_b = re.sub(r"\bNAME\b", slug, exp_b)
    exp_b = exp_b.replace(
        "<one-line description of what the region contains>", desc
    )
    got_b = (QA / ("crop_prompt_6_%s.txt" % name)).read_text(encoding="utf-8")
    results.append(
        ("crop_prompt_6_%s.txt vs Template B (NNN->004, K->7, NAME->%s, desc)" % (name, slug),
         exp_b,
         got_b),
    )

ok = True
for label, expected, actual in results:
    same = expected == actual
    ok = ok and same
    print("[%s] %s" % ("PASS" if same else "FAIL", label))
    print("      expected %d bytes sha256=%s" % (len(expected.encode()), sha(expected)))
    print("      actual   %d bytes sha256=%s" % (len(actual.encode()), sha(actual)))
    if not same:
        for i, (e, a) in enumerate(zip(expected, actual)):
            if e != a:
                print("      first diff at char %d: expected %r got %r" % (i, e, a))
                break
        else:
            print("      length differs; common prefix identical")

print()
print("RESULT: %s" % ("ALL PASS" if ok else "FAIL"))
