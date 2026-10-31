import json, os, re, sys, glob

ROOT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
os.chdir(ROOT)

PASS_RE = re.compile(r"FINAL VERDICT:?\s*\**\s*PASS\b")
FAIL_RE = re.compile(r"FINAL VERDICT:?\s*\**\s*FAIL\b")

def verdict(path):
    try:
        with open(path, "r", errors="replace") as f:
            txt = f.read()
    except OSError:
        return "unreadable"
    m = re.findall(r"FINAL VERDICT:?\s*\**\s*(PASS|FAIL)\b", txt)
    return m[-1] if m else "none"

def qa_dir(n):
    qa = os.path.join(ROOT, "recreated_pptx/qa")
    exact = "slide%03d" % n
    if os.path.isdir(os.path.join(qa, exact)):
        return os.path.join(qa, exact)
    rx = re.compile(r"^slide_?0*%d$" % n)
    cands = [d for d in os.listdir(qa) if rx.match(d) and os.path.isdir(os.path.join(qa, d))]
    if not cands:
        return None
    cands.sort(key=lambda d: (len(d), d))
    return os.path.join(qa, cands[0])

def scan():
    d = json.load(open("final_deck_ledger.json"))
    certified = set(p["slide_num"] for p in d["pages"] if p["status"] == "certified")
    out = []
    for n in range(1, 38):
        if n in certified:
            continue
        qd = qa_dir(n)
        if not qd:
            out.append((n, "no-qa-dir", None, None, None, None))
            continue
        renders = glob.glob(os.path.join(qd, "render*.png")) or glob.glob(os.path.join(qd, "*.png"))
        if not renders:
            pptx = "recreated_pptx/slide_%03d_recreated.pptx" % n
            out.append((n, "no-render", None, None, None, os.path.exists(pptx)))
            continue
        newest_render = max(renders, key=os.path.getmtime)
        R = os.path.getmtime(newest_render)
        attempts = sorted(glob.glob(os.path.join(qd, "judge_attempt_*.txt")), key=os.path.getmtime)
        verifies = sorted(glob.glob(os.path.join(qd, "judge_verify_*.txt")), key=os.path.getmtime)
        att_pass = [a for a in attempts if os.path.getmtime(a) > R and PASS_RE.search(open(a, errors="replace").read())]
        ver_all = [(v, os.path.getmtime(v), verdict(v)) for v in verifies]
        ver_pass = [v for v, m, vd in ver_all if m > R and vd == "PASS"]
        newest_ver = ver_all[-1] if ver_all else None
        if newest_ver and newest_ver[1] > R and newest_ver[2] == "FAIL" and not ver_pass:
            out.append((n, "verify-FAIL-newest", newest_render, att_pass[-1] if att_pass else None, newest_ver[0], None))
            continue
        if att_pass and ver_pass:
            out.append((n, "QUALIFIES", newest_render, att_pass[-1], ver_pass[-1], qd))
        else:
            out.append((n, "not-ready", newest_render,
                        att_pass[-1] if att_pass else None,
                        ver_pass[-1] if ver_pass else None, None))
    return out

if __name__ == "__main__":
    for row in scan():
        print(" | ".join(str(x) for x in row))
