import re, hashlib
P = "videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{P}/recreated_pptx/qa/slide044"
proto = open(f"{P}/shared_patterns/judge_protocol_03.md").read()

def payload_after(heading):
    """Return the -p payload of the first ``` block after `heading` that carries one."""
    i = proto.index(heading)
    blocks = []
    while True:
        try:
            s = proto.index("```", i)
        except ValueError:
            break
        try:
            e = proto.index("```", s + 3)
        except ValueError:
            break
        blocks.append(proto[s + 3:e])
        i = e + 3
    for b in blocks:
        m = re.search(r'-p "(.*?)"\n', b, re.S)
        if m:
            return m.group(1)
    raise AssertionError(heading)

A = payload_after("## Template A — full-slide comparison judge")
A = A.replace("NNN", "44").replace("render_K", "render_2")
# legal substitutions only: \bK\b and NNN. No global K replacement (that corrupted BLOCKER once).
def subst_K(s):
    return re.sub(r"\bK\b", "2", s)
A_exp = subst_K(A)
B_exp = subst_K(payload_after("## Template B — crop-pair judge").replace("NNN", "44"))

def norm(s):
    return s.rstrip("\n")

def cmp(name, path, exp):
    banked = open(path).read()
    ok = norm(banked) == norm(exp)
    md5 = hashlib.md5(banked.encode()).hexdigest()[:12]
    if ok:
        print(f"[OK]   {name} md5 {md5} — byte-identical to protocol reconstruction")
    else:
        print(f"[DIFF] {name} md5 {md5} — differs; diff follows")
        ex, ba = exp.splitlines(), banked.splitlines()
        for k in range(max(len(ex), len(ba))):
            e = ex[k] if k < len(ex) else "<none>"
            b = ba[k] if k < len(ba) else "<none>"
            if e != b:
                print(f"  line {k+1}:")
                print(f"   exp: {e[:400]}")
                print(f"   ban: {b[:400]}")
    print(f"   BLOCKER={'BLOCKER' in banked} BLOC1ER={'BLOC1ER' in banked} "
          f"BLOC2ER={'BLOC2ER' in banked} B1OCKER={'B1OCKER' in banked} "
          f"zero_padded={'slide 044' in banked} K_leftover={bool(re.search(r'\bK\b', banked))}")
    return ok

okA = cmp("judgepayload_legs_A.txt", f"{Q}/judgepayload_legs_A.txt", A_exp)
okB = all(cmp(f"judgepayload_legs_B_{n}.txt", f"{Q}/judgepayload_legs_B_{n}.txt", B_exp)
           for n in ["centretext", "eqstack", "lefttables"])
print(f"\nOVERALL: A={'OK' if okA else 'FAIL'} B={'OK' if okB else 'FAIL'}")
