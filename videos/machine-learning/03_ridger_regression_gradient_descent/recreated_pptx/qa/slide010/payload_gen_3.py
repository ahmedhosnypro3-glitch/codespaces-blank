#!/usr/bin/env python3
"""Slide 010 — judge payload generator + byte-check (child lane, attempt K=3).
Extracts the Template A and Template B -p payloads VERBATIM from the frozen
shared_patterns/judge_protocol_03.md and applies ONLY the protocol-prescribed
substitutions (NNN->010; Template B NAME/region-desc live in the SHELL, not the
-p payload). Byte-checks that nothing else changed (NNN->010 is length-neutral,
3 chars -> 3 chars). BLOCKER text must never be altered.
"""
import os, sys

PROTO = ("../../../shared_patterns/judge_protocol_03.md")

def proto_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, PROTO))

def extract_payloads(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    pl = [ln for ln in lines if '-p "' in ln]
    if len(pl) != 2:
        sys.exit("expected exactly two `-p \"` lines (Template A, Template B), found %d" % len(pl))
    def extract(line):
        i = line.index('-p "') + 4
        j = line.rindex('"')
        return line[i:j]
    return extract(pl[0]), extract(pl[1])

def bytecheck(tmpl, out, subs):
    # apply substitutions, then verify the ONLY differences are the substitutions
    res = tmpl
    for a, b in subs:
        res = res.replace(a, b)
    # reverse check: reverting each substitution must reproduce the template exactly
    rev = res
    for a, b in reversed(subs):
        rev = rev.replace(b, a)
    assert rev == tmpl, "reverse-substitution did not reproduce template (substitution collision?)"
    # every 'NNN' must be gone
    assert "NNN" not in res or subs_dict_none(subs, "NNN"), ("residual NNN", res.count("NNN"))
    return res

def subs_dict_none(subs, k):
    return all(a != k for a, _ in subs)

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    A, B = extract_payloads(proto_path())
    print("Template A payload: %d bytes, NNN occurrences=%d, BLOCKER occurrences=%d"
          % (len(A), A.count("NNN"), A.count("BLOCKER")))
    print("Template B payload: %d bytes, NNN occurrences=%d, BLOCKER occurrences=%d"
          % (len(B), B.count("NNN"), B.count("BLOCKER")))
    # Template A: replace NNN->010 (payload may or may not contain NNN)
    A_out = A.replace("NNN", "010")
    # Template B: replace NNN->010
    B_out = B.replace("NNN", "010")
    # byte-checks
    assert len(A_out) == len(A), "A length changed"
    assert len(B_out) == len(B), "B length changed"
    assert "BLOCKER" in A_out and A_out.count("BLOCKER") == A.count("BLOCKER")
    assert "BLOCKER" in B_out and B_out.count("BLOCKER") == B.count("BLOCKER")
    assert A_out.replace("010", "NNN") == A
    assert B_out.replace("010", "NNN") == B
    assert "NNN" not in A_out and "NNN" not in B_out
    # anchors that must survive untouched
    for anc in ("GROUND RULES", "FINAL VERDICT:", "E9E9E7", "8,4" if False else "FDFD96"):
        assert anc in A_out and anc in B_out, ("missing anchor", anc)
    open(os.path.join(here, "payload_A_3.txt"), "w", encoding="utf-8").write(A_out)
    open(os.path.join(here, "payload_B_3.txt"), "w", encoding="utf-8").write(B_out)
    print("\nWROTE payload_A_3.txt (%d bytes), payload_B_3.txt (%d bytes)" % (len(A_out), len(B_out)))
    print("byte-check: NNN->010 length-neutral, BLOCKER intact, reverse substitution reproduces template. PASS")
    print("\n--- Template B payload written (used for ALL four crop regions; NAME/desc in shell) ---")
    print(B_out)

if __name__ == "__main__":
    main()
