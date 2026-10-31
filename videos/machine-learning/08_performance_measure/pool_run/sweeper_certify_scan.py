#!/usr/bin/env python3
"""Scan qa/slide* dirs: classify each slide 1..37 by newest attempt/verify verdicts."""
import json, os, re, glob

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
QA = os.path.join(NS, "recreated_pptx/qa")

def verdict_of(path):
    """Return 'PASS'/'FAIL'/None from the LAST FINAL VERDICT line of a transcript."""
    try:
        with open(path, "r", errors="replace") as f:
            txt = f.read()
    except OSError:
        return None
    lines = [l for l in txt.splitlines() if "FINAL VERDICT" in l.upper()]
    if not lines:
        return None
    last = lines[-1].upper()
    if "PASS" in last and "FAIL" not in last:
        return "PASS"
    if "FAIL" in last:
        return "FAIL"
    return "OTHER"

def newest(dirs, pat):
    files = []
    for d in dirs:
        files += glob.glob(os.path.join(QA, d, pat))
    files = [f for f in files if os.path.isfile(f)]
    files.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    return files

ledger = json.load(open(os.path.join(NS, "final_deck_ledger.json")))
certified = {p["page"] for p in ledger["pages"] if p.get("status") == "certified"}

# map slide number -> candidate qa dirs (zero-padded primary, legacy variants too)
for n in range(1, 38):
    dirs = []
    for name in (f"slide{n:03d}", f"slide{n}", f"slide_{n:03d}", f"slide_{n}"):
        d = os.path.join(QA, name)
        if os.path.isdir(d):
            dirs.append(name)
    att = newest(dirs, "judge_attempt_*.txt") if dirs else []
    ver = newest(dirs, "judge_verify_*.txt") if dirs else []
    att_pass = any(verdict_of(f) == "PASS" for f in att)
    ver_pass = any(verdict_of(f) == "PASS" for f in ver)
    newest_ver = verdict_of(ver[0]) if ver else None
    newest_att = verdict_of(att[0]) if att else None
    renders = newest(dirs, "render_*.png") if dirs else []
    newest_render = os.path.basename(renders[0]) if renders else None
    status = "CERTIFIED" if n in certified else "open"
    flag = ""
    if att_pass and ver_pass and n not in certified and newest_ver != "FAIL":
        flag = "CANDIDATE"
    elif att_pass and not ver_pass and newest_ver != "FAIL":
        flag = "NEEDS_VERIFY"
    elif newest_ver == "FAIL":
        flag = "REOPENED"
    print(f"slide{n:03d} dirs={dirs} attN={len(att)} attPASS={att_pass} newestATT={newest_att} "
          f"verN={len(ver)} verPASS={ver_pass} newestVER={newest_ver} render={newest_render} "
          f"ledger={status} {flag}")
    if flag == "CANDIDATE":
        print(f"CANDIDATE {n}")
    elif flag == "NEEDS_VERIFY" and n not in certified:
        print(f"NEEDS_VERIFY {n}")
print(f"CERTIFIED_COUNT {len(certified)}")
