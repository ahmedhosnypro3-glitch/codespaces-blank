#!/usr/bin/env python3
"""Sweeper scan: find slides with dual PASS (attempt+verify) postdating newest render."""
import json, os, re, sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
QA = os.path.join(NS, "recreated_pptx", "qa")
LEDGER = os.path.join(NS, "final_deck_ledger.json")
PASS_RE = re.compile(r"FINAL VERDICT:\s*PASS", re.I)
FAIL_RE = re.compile(r"FINAL VERDICT:\s*FAIL", re.I)
RENDER_RE = re.compile(r"^render[_a-zA-Z0-9-]*\.png$")


def verdict(path):
    try:
        with open(path, "r", errors="replace") as fh:
            t = fh.read()
        if PASS_RE.search(t):
            return "PASS"
        if FAIL_RE.search(t):
            return "FAIL"
    except OSError:
        pass
    return None


def dirs_by_slide():
    out = {}
    for d in os.listdir(QA):
        m = re.fullmatch(r"slide_?(\d+)", d)
        if m and os.path.isdir(os.path.join(QA, d)):
            out.setdefault(int(m.group(1)), []).append(os.path.join(QA, d))
    return out


def main():
    ledger = json.load(open(LEDGER))
    certified = {p["slide_num"] for p in ledger["pages"] if p["status"] == "certified"}
    dbs = dirs_by_slide()
    result = {"certified": sorted(certified), "qualifying": [], "skipped": []}
    for n in range(1, 38):
        if n in certified:
            continue
        padded = "%03d" % n
        pptx = os.path.join(NS, "recreated_pptx", "slide_%s_recreated.pptx" % padded)
        dirs = dbs.get(n, [])
        renders = []
        attempts, verifies = [], []
        for d in dirs:
            for f in os.listdir(d):
                p = os.path.join(d, f)
                if not os.path.isfile(p):
                    continue
                mt = os.path.getmtime(p)
                if RENDER_RE.match(f):
                    renders.append((mt, f, p))
                elif f.startswith("judge_attempt_") and f.endswith(".txt"):
                    v = verdict(p)
                    if v:
                        attempts.append((mt, f, p, v))
                elif f.startswith("judge_verify_") and f.endswith(".txt"):
                    v = verdict(p)
                    if v:
                        verifies.append((mt, f, p, v))
        if not renders:
            result["skipped"].append({"n": n, "reason": "no render (pptx exists: %s)" % os.path.exists(pptx)})
            continue
        renders.sort()
        R, _, rpath = renders[-1]
        att_pass = [a for a in attempts if a[3] == "PASS" and a[0] > R]
        ver_pass = [v for v in verifies if v[3] == "PASS" and v[0] > R]
        newest_verify = max(verifies, key=lambda x: x[0]) if verifies else None
        if newest_verify and newest_verify[3] == "FAIL":
            result["skipped"].append({"n": n, "reason": "newest verify FAIL, no later PASS verify",
                                      "newest_verify": newest_verify[2]})
            continue
        if att_pass and ver_pass:
            att_pass.sort(key=lambda x: x[0])
            ver_pass.sort(key=lambda x: x[0])
            result["qualifying"].append({
                "n": n,
                "render": os.path.relpath(rpath, NS),
                "attempt": os.path.relpath(att_pass[-1][2], NS),
                "verify": os.path.relpath(ver_pass[-1][2], NS),
                "pptx": "recreated_pptx/slide_%s_recreated.pptx" % padded,
            })
        else:
            result["skipped"].append({
                "n": n,
                "reason": "att_pass=%d ver_pass=%d after render %s" % (len(att_pass), len(ver_pass), os.path.basename(rpath)),
                "attempts": [(os.path.basename(a[2]), a[3]) for a in sorted(attempts)],
                "verifies": [(os.path.basename(v[2]), v[3]) for v in sorted(verifies)],
            })
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
