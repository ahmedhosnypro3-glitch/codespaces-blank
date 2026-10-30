#!/usr/bin/env python3
"""scope_s1 read-only rejudge completeness scanner (no vision, no writes)."""
import json, os, re, hashlib, glob

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDES = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 17, 18, 21, 22, 23, 24, 26, 27]
VERD_RE = re.compile(r"FINAL VERDICT\s*:\s*(PASS|FAIL)", re.I)

ledger = json.load(open(os.path.join(NS, "final_deck_ledger.json")))
led = {p["slide_num"]: p for p in ledger["pages"]}


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def judge_state(d):
    """Return (verdict_or_None, n_attempts, files)."""
    files = sorted(glob.glob(os.path.join(d, "judge_attempt_*.txt")))
    files += sorted(glob.glob(os.path.join(d, "judge_attempt_*.stdout.txt")))
    verdicts = []
    for f in files:
        try:
            body = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        hits = VERD_RE.findall(body)
        if hits:
            verdicts.append((os.path.basename(f), hits[-1].upper()))
    last = verdicts[-1][1] if verdicts else "NONE"
    return last, len(files), verdicts


rows = []
for n in SLIDES:
    nnn = f"{n:03d}"
    qa = os.path.join(NS, "qa", f"slide{nnn}", "rejudge")
    rea = os.path.join(NS, "analysis", "reanalysis")
    raw = os.path.join(rea, f"slide_{nnn}_raw.json")
    fin = os.path.join(rea, f"slide_{nnn}_final.json")
    render = os.path.join(qa, "render-1.png")
    adj = os.path.join(qa, "adjudication.md")
    rep = os.path.join(qa, "REJUDGE_REPORT.md")
    build = os.path.join(NS, "recreated_pptx", "build", f"slide_{nnn}_recreated.pptx")
    verdict, natt, vlist = judge_state(qa)
    bmd5 = md5(build) if os.path.isfile(build) else None
    lmd5 = led.get(n, {}).get("source_md5")
    sync = "SYNC" if (bmd5 and lmd5 and bmd5 == lmd5) else (
        "MISMATCH" if (bmd5 and lmd5) else "NO-BUILD" if bmd5 is None else "NO-LEDGER")
    rows.append(dict(
        n=nnn, raw=os.path.isfile(raw), fin=os.path.isfile(final) if (final := fin) else False,
        render=os.path.isfile(render), verdict=verdict, natt=natt, vlist=vlist,
        adj=os.path.isfile(adj), rep=os.path.isfile(rep),
        sync=sync, bmd5=bmd5, lmd5=lmd5,
    ))

print(json.dumps(rows, indent=1))
print("=== SUMMARY ===")
for r in rows:
    miss = []
    if not r["raw"]: miss.append("raw")
    if not r["fin"]: miss.append("final")
    if not r["render"]: miss.append("render")
    if r["verdict"] == "NONE": miss.append("judge")
    if not r["adj"]: miss.append("adj")
    if not r["rep"]: miss.append("report")
    if r["sync"] != "SYNC": miss.append("ledger:" + r["sync"])
    print(f"slide_{r['n']} verdict={r['verdict']:<4} attempts={r['natt']} sync={r['sync']:<8} missing={','.join(miss) or 'NONE'}")
