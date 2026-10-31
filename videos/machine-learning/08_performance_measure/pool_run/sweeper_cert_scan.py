#!/usr/bin/env python3
"""Scan qa/slide* dirs for certification state. Prints JSON to stdout.

{
 "certified": [n...],
 "certifiable": [{"n","attempts","verifies"}...],          # dual PASS, not certified
 "needs_verify": [{"n","attempt","render","attempt_path"}...]  # fresh PASS attempt, no verify PASS
}
A PASS attempt is "fresh" when its judged render is newer than the slide pptx
(a pptx newer than the judged render = stale certification, worker must rebuild).
"""
import json, os, re

NS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QA = os.path.join(NS, "recreated_pptx", "qa")
LEDGER = os.path.join(NS, "final_deck_ledger.json")
PASS_RE = re.compile(r"FINAL VERDICT:\s*PASS", re.I)
RENDER_RE = re.compile(r"render[_a-zA-Z0-9-]*\.png")


def dirs_by_slide():
    out = {}
    for d in os.listdir(QA):
        m = re.fullmatch(r"slide_?(\d+)", d)
        if m and os.path.isdir(os.path.join(QA, d)):
            out.setdefault(int(m.group(1)), []).append(os.path.join(QA, d))
    return out


def verdict_pass(path):
    try:
        with open(path, "r", errors="replace") as fh:
            return bool(PASS_RE.search(fh.read()))
    except OSError:
        return False


def main():
    ledger = json.load(open(LEDGER))
    status = {p["slide_num"]: p["status"] for p in ledger["pages"]}
    out = {"certified": [], "certifiable": [], "needs_verify": []}
    for n in range(1, 38):
        padded = "%03d" % n
        pptx = os.path.join(NS, "recreated_pptx", "slide_%s_recreated.pptx" % padded)
        pptx_m = os.path.getmtime(pptx) if os.path.exists(pptx) else 0
        attempts, verifies = [], []
        for d in dirs_by_slide().get(n, []):
            for f in sorted(os.listdir(d)):
                p = os.path.join(d, f)
                if not f.endswith(".txt") or f.endswith(".tmp"):
                    continue
                rel = os.path.relpath(p, NS)
                if f.startswith("judge_attempt_") and verdict_pass(p):
                    attempts.append((f, p, rel))
                elif f.startswith("judge_verify_") and verdict_pass(p):
                    verifies.append((f, p, rel))
        if status.get(n) == "certified":
            out["certified"].append(n)
            continue
        if attempts and verifies:
            out["certifiable"].append({
                "n": n,
                "attempts": [a[2] for a in attempts],
                "verifies": [v[2] for v in verifies],
            })
            continue
        if attempts and not verifies:
            # newest PASS attempt whose judged render is not stale vs the pptx
            fresh = []
            for f, p, rel in attempts:
                with open(p, "r", errors="replace") as fh:
                    m = RENDER_RE.search(fh.read())
                render = m.group(0) if m else None
                rd = os.path.join(os.path.dirname(p), render) if render else None
                if rd and os.path.exists(rd) and os.path.getmtime(rd) >= pptx_m:
                    fresh.append({"attempt": f, "render": render,
                                  "attempt_path": rel,
                                  "render_path": os.path.relpath(rd, NS)})
            if fresh:
                fresh.sort(key=lambda x: x["attempt"])
                out["needs_verify"].append({"n": n, **fresh[-1]})
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
