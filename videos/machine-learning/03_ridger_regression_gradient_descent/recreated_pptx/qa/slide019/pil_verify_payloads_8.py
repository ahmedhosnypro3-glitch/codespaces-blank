#!/usr/bin/env python3
"""Byte-verify slide019 judgment payloads against the frozen protocol.

Extract the `-p "..."` payload strings from shared_patterns/judge_protocol_03.md
(Template A line, Template B line), apply the NNN/NAME/K substitutions, and
compare byte-for-byte with the banked attempt-8 payloads.
"""
import hashlib
import re
import sys

Q = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
     "recreated_pptx/qa/slide019")
PROTO = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
         "shared_patterns/judge_protocol_03.md")


def extract_payload(path, marker):
    """Return the literal text inside the `-p "..."` of the first -p line
    following `marker`."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for i, line in enumerate(lines):
        if marker in line:
            for j in range(i, min(i + 30, len(lines))):
                m = re.match(r'\s*-p\s+"(.*)"\s*$', lines[j])
                if m:
                    return m.group(1)
    raise SystemExit(f"payload marker {marker!r} not found")


def main():
    proto_a = extract_payload(PROTO, "Template A — full-slide comparison judge")
    proto_b = extract_payload(PROTO, "Template B — crop-pair judge")

    # Template A: no token substitution in the payload (chrome is baked in).
    derived_a = proto_a
    # Template B: slide NNN -> slide 019.
    derived_b = proto_b.replace("slide NNN", "slide 019")

    ok = True
    for name, derived, banked_path in (
        ("Template A", derived_a, f"{Q}/judgeA8_payload_20261024.txt"),
        ("Template B", derived_b, f"{Q}/judgeB8_payload_20261024.txt"),
    ):
        with open(banked_path, encoding="utf-8") as fh:
            banked = fh.read()
        # banked files are written with a trailing newline; strip exactly one.
        banked_cmp = banked[:-1] if banked.endswith("\n") else banked
        banked_md5 = hashlib.md5(banked_cmp.encode()).hexdigest()
        derived_md5 = hashlib.md5(derived.encode()).hexdigest()
        same = banked_cmp == derived
        ok = ok and same
        print(f"{name}: derived {len(derived)} chars md5={derived_md5} | "
              f"banked {len(banked_cmp)} chars md5={banked_md5} | "
              f"{'BYTE-EQUAL' if same else 'MISMATCH'}")
        if not same:
            for k, (x, y) in enumerate(zip(derived, banked_cmp)):
                if x != y:
                    print(f"  first diff at {k}: derived={x!r} "
                          f"banked={y!r}\n  derived: ...{derived[k-60:k+60]!r}\n"
                          f"  banked:  ...{banked_cmp[k-60:k+60]!r}")
                    break
            else:
                print(f"  length differs: derived={len(derived)} "
                      f"banked={len(banked_cmp)}")

    # corruption guards
    for p in (f"{Q}/judgeA8_payload_20261024.txt",
              f"{Q}/judgeB8_payload_20261024.txt"):
        with open(p, encoding="utf-8") as fh:
            txt = fh.read()
        for bad in ("BLOC7ER", "slide_NNN", "NNN"):
            if bad in txt:
                print(f"CORRUPTION: {bad!r} present in {p}")
                ok = False
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
