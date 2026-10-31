#!/usr/bin/env python3
# Promoter/guard watch for slide 025 (agent-386 owns promotion; this guard never
# touches the DB and never deletes anything):
#  1. every 60s verify md5 of slide_025_recreated.pptx + build/assets/plot_025_{tl,tr,bl,br}.png
#     against the canonical k17g/c50e78bf signature; on any change append a timestamped
#     old/new line to CLOBBER_WATCH.log and restore from
#     slide025/slide_025_recreated.preK17n.bak.pptx and slide025/assets_k17g/, then re-verify
#  2. detect NEW clean verdict pairs (judge_full_*.txt + crop_dense_judge_*.txt sharing a tag,
#     both with a FINAL VERDICT ... PASS line and zero '429' lines) whose judged render maps to
#     a pptx md5 currently on disk -> record in PROMOTION_CANDIDATES.md
#  3. if the pptx md5 deviates from c50e78bf and the same deviant md5 has been observed for
#     >10 min while a matching clean PASS/PASS pair is recorded -> append PROMOTE-READY evidence
# Usage: promote_guard_20261031.py [--once] [--chunk SECONDS]   (default: loop until start+2h)
import glob
import hashlib
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
W = f"{RJ}/slide025"
BUILD = f"{NS}/recreated_pptx/build"
PPTX = f"{NS}/recreated_pptx/slide_025_recreated.pptx"
ASSETS = {k: f"{BUILD}/assets/plot_025_{k}.png" for k in ("tl", "tr", "bl", "br")}
CAN = {
    "pptx": "c50e78bf39531523dcf69d652254b647",
    "tl": "cd62022fbf0cfe30a351309c0230adb3",
    "tr": "b45c723af19e2cf11659109d63134cad",
    "bl": "7a8e7210f118b728245d268552a7d32d",
    "br": "f6af102ec110ff5113482659ff4f9d73",
}
BAK_PPTX = f"{W}/slide_025_recreated.preK17n.bak.pptx"
BAK_ASSETS = f"{W}/assets_k17g"
LOG = f"{W}/CLOBBER_WATCH.log"
CAND = f"{W}/PROMOTION_CANDIDATES.md"
STATE = f"{W}/.promote_guard_20261031_state.json"
STARTF = f"{W}/.promote_guard_20261031_start"
WATCH = 2 * 3600
POLL = 60
HEX = re.compile(r"\b[0-9a-f]{32}\b")


def now():
    return datetime.now(timezone.utc)


def ts():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def alog(path, line):
    with open(path, "a") as f:
        f.write(line + "\n")


def load_state():
    try:
        with open(STATE) as f:
            return json.load(f)
    except Exception:
        return {"md5cache": {}, "deviants": {}, "ready_fired": [], "recorded": [],
                "last_sig": None, "poll": 0}


def save_state(st):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(st, f)
    os.replace(tmp, STATE)


def cached_md5(st, p):
    try:
        s = os.stat(p)
    except OSError:
        return None
    key = p
    ent = st["md5cache"].get(key)
    if ent and ent[0] == s.st_mtime_ns and ent[1] == s.st_size:
        return ent[2]
    m = md5(p)
    st["md5cache"][key] = [s.st_mtime_ns, s.st_size, m]
    return m


def on_disk_pptx_md5s(st):
    out = {}
    for base in (f"{NS}/recreated_pptx", W):
        for dirpath, _dirs, files in os.walk(base):
            for fn in files:
                if fn.endswith(".pptx"):
                    p = os.path.join(dirpath, fn)
                    m = cached_md5(st, p)
                    if m:
                        out.setdefault(m, []).append(p)
    return out


def verdict(path):
    try:
        lines = open(path, errors="replace").read().splitlines()
    except OSError:
        return False, "", -1
    vlines = [l for l in lines if "FINAL VERDICT" in l]
    pass_lines = [l for l in vlines if "PASS" in l and "FAIL" not in l and "PASS or" not in l]
    n429 = sum(1 for l in lines if "429" in l)
    return bool(pass_lines), (pass_lines[-1].strip() if pass_lines else ""), n429


def tag_of(path, prefix):
    b = os.path.basename(path)
    return b[len(prefix):-len(".txt")]


def render_for(transcript, tag, kind):
    logf = transcript + ".log"
    if os.path.exists(logf):
        for line in open(logf, errors="replace"):
            m = re.match(r"\[info\]\s+(\S+?),\s*\S+?:\s*transcript written", line)
            if m:
                return m.group(1)
            m = re.match(r"===\s+(\S+?),\s*\S+?\s+===", line)
            if m:
                return m.group(1)
    guess = f"{W}/render_{tag}.png" if kind == "full" else f"{W}/crop_dense_render_{tag}.png"
    if tag and os.path.exists(guess):
        return guess
    return f"{W}/render.png" if kind == "full" else f"{W}/crop_dense_render.png"


def resolve_pptx_md5(render_path, transcript, ondisk):
    rb = os.path.basename(render_path)
    try:
        t_mtime = os.path.getmtime(transcript)
    except OSError:
        t_mtime = 0
    cands_pptx, cands_any, sigs = [], [], []
    scan_dirs = [W, RJ]
    for d in scan_dirs:
        for fn in os.listdir(d):
            p = os.path.join(d, fn)
            if not os.path.isfile(p) or not fn.endswith((".txt", ".log", ".out", ".md")):
                continue
            try:
                text = open(p, errors="replace").read()
            except OSError:
                continue
            for line in text.splitlines():
                if rb in line:
                    for h in HEX.findall(line):
                        (cands_pptx if "pptx" in line.lower() else cands_any).append(h)
                m = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z).*sig=([0-9a-f]{32})", line)
                if m:
                    sigs.append((m.group(1), m.group(2)))
    ordered = list(dict.fromkeys(cands_pptx + cands_any))
    if sigs:
        t_iso = datetime.fromtimestamp(t_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if t_mtime else ts()
        before = sorted(s for s in sigs if s[0] <= t_iso) or sorted(sigs)
        ordered.append(before[-1][1])
    ordered.append(CAN["pptx"])
    for c in ordered:
        if c in ondisk:
            return c, True, ordered
    return (ordered[0] if ordered else "UNRESOLVED"), False, ordered


def scan_pairs(st, ondisk):
    fulls = sorted(glob.glob(f"{W}/judge_full_*.txt"))
    crops = sorted(glob.glob(f"{W}/crop_dense_judge_*.txt"))
    crop_by_tag = {tag_of(c, "crop_dense_judge_"): c for c in crops}
    found = []
    for f in fulls:
        tag = tag_of(f, "judge_full_")
        c = crop_by_tag.get(tag)
        if not c:
            continue
        fok, fline, f429 = verdict(f)
        cok, cline, c429 = verdict(c)
        if not (fok and cok and f429 == 0 and c429 == 0):
            continue
        fkey = f"{tag}|{f}|{os.path.getmtime(f)}|{c}|{os.path.getmtime(c)}"
        if fkey in st["recorded"]:
            continue
        st["recorded"].append(fkey)
        fr = render_for(f, tag, "full")
        cr = render_for(c, tag, "crop")
        frm = cached_md5(st, fr) if os.path.exists(fr) else "missing"
        crm = cached_md5(st, cr) if os.path.exists(cr) else "missing"
        pmd5, match, cands = resolve_pptx_md5(fr, f, ondisk)
        literal = frm in ondisk
        block = [
            f"## [{ts()}] {'CANDIDATE' if (match or literal) else 'INFO-no-on-disk-pptx-match'} clean PASS/PASS pair — slide 25 tag=`{tag or '(base)'}`",
            f"- slide: 25",
            f"- full transcript: {f} (mtime {datetime.fromtimestamp(os.path.getmtime(f), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}) verdict: {fline!r} 429-lines={f429}",
            f"- crop transcript: {c} (mtime {datetime.fromtimestamp(os.path.getmtime(c), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}) verdict: {cline!r} 429-lines={c429}",
            f"- render file (full): {fr} md5={frm}",
            f"- render file (crop): {cr} md5={crm}",
            f"- pptx md5 (judged render source): {pmd5} candidate_order={cands[:6]}",
            f"- pptx-md5 match on disk: {'YES ' + '; '.join(ondisk[pmd5]) if match else 'NO'}; literal render-md5 in on-disk pptx set: {'YES' if literal else 'NO'}",
            f"- recorded by promote_guard_20261031.py (agent-386 owns promotion; no DB change made)",
            "",
        ]
        alog(CAND, "\n".join(block))
        alog(LOG, f"[{ts()}] GUARD NEW-CLEAN-PAIR slide=25 tag={tag or '(base)'} full={os.path.basename(f)} crop={os.path.basename(c)} render_full={fr} md5={frm} pptx_md5={pmd5} on_disk_match={match or literal}")
        found.append((tag, f, c, pmd5, match or literal))
    return found


def check_and_restore(st):
    st["poll"] += 1
    sig = {"pptx": cached_md5(st, PPTX)}
    for k, p in ASSETS.items():
        sig[k] = cached_md5(st, p)
    changed = [k for k in sig if sig[k] != CAN[k]]
    events = []
    if changed:
        prev = st.get("last_sig") or {}
        kind = "CLOBBER" if any(prev.get(k) != sig[k] for k in changed) else "STILL-DEVIANT"
        alog(LOG, f"[{ts()}] GUARD {kind} poll#{st['poll']} changed={','.join(changed)} "
                  f"observed_pptx={sig['pptx']} assets=[tl={sig['tl']} tr={sig['tr']} bl={sig['bl']} br={sig['br']}] "
                  f"canonical_pptx={CAN['pptx']} assets=[tl={CAN['tl']} tr={CAN['tr']} bl={CAN['bl']} br={CAN['br']}]")
        for k in changed:
            alog(LOG, f"[{ts()}] GUARD   {k}: old(canonical)={CAN[k]} new(observed)={sig[k]}")
        shutil.copyfile(BAK_PPTX, PPTX)
        shutil.copyfile(f"{BAK_ASSETS}/plot_025_tl.png", ASSETS["tl"])
        shutil.copyfile(f"{BAK_ASSETS}/plot_025_tr.png", ASSETS["tr"])
        shutil.copyfile(f"{BAK_ASSETS}/plot_025_bl.png", ASSETS["bl"])
        shutil.copyfile(f"{BAK_ASSETS}/plot_025_br.png", ASSETS["br"])
        np_ = cached_md5(st, PPTX)
        st["md5cache"][PPTX] = [os.stat(PPTX).st_mtime_ns, os.stat(PPTX).st_size, np_]
        ok_p = np_ == CAN["pptx"]
        oks = {}
        for k, p in ASSETS.items():
            m = cached_md5(st, p)
            st["md5cache"][p] = [os.stat(p).st_mtime_ns, os.stat(p).st_size, m]
            oks[k] = m == CAN[k]
        alog(LOG, f"[{ts()}] GUARD restored pptx<= {BAK_PPTX} verify_md5={np_} ok={ok_p}; "
                  f"assets<= {BAK_ASSETS}/ verify tl={oks['tl']} tr={oks['tr']} bl={oks['bl']} br={oks['br']}")
        events.append(f"{kind}:pptx {sig['pptx']}->restored ok={ok_p} assets ok={all(oks.values())}")
        d = sig["pptx"]
        if d != CAN["pptx"]:
            dv = st["deviants"].setdefault(d, {"first_seen": ts(), "first_epoch": time.time(), "count": 0})
            dv["count"] += 1
            dv["last_seen"] = ts()
    else:
        alog(LOG, f"[{ts()}] GUARD poll#{st['poll']} OK all-5-canonical pptx={sig['pptx']} "
                  f"assets=[{sig['tl']} {sig['tr']} {sig['bl']} {sig['br']}]")
        events.append("OK")
    st["last_sig"] = sig
    return sig, events


def promote_ready(st, ondisk):
    fired = []
    for d, info in list(st["deviants"].items()):
        if d == CAN["pptx"] or d in st["ready_fired"]:
            continue
        elapsed = time.time() - info["first_epoch"]
        if elapsed <= 600:
            continue
        matching = []
        for line in open(CAND, errors="replace"):
            if line.startswith("- pptx md5 (judged render source):") and line.split(":", 1)[1].split()[0] == d:
                matching.append(line.strip())
        if not matching:
            continue
        on_disk_now = ondisk.get(d, [])
        line = (f"[{ts()}] PROMOTE-READY slide=25 deviant_pptx_md5={d} first_seen={info['first_seen']} "
                f"elapsed={int(elapsed)}s count={info['count']} canonical={CAN['pptx']} "
                f"on_disk_pptx_now={';'.join(on_disk_now) or 'NOT-ON-DISK'} "
                f"matching_recorded_pairs={len(matching)} evidence={matching[0]} "
                f"— agent-386 owns promotion; guard made no DB change")
        alog(LOG, line)
        alog(CAND, f"\n## [{ts()}] PROMOTE-READY slide=25 deviant_pptx_md5={d} first_seen={info['first_seen']} elapsed={int(elapsed)}s on_disk_now={';'.join(on_disk_now) or 'NOT-ON-DISK'} matching={matching[0]}\n")
        st["ready_fired"].append(d)
        fired.append(d)
    return fired


def poll(st):
    sig, events = check_and_restore(st)
    ondisk = on_disk_pptx_md5s(st)
    pairs = scan_pairs(st, ondisk)
    ready = promote_ready(st, ondisk)
    return events, pairs, ready


def main():
    args = sys.argv[1:]
    once = "--once" in args
    chunk = 0
    if "--chunk" in args:
        chunk = int(args[args.index("--chunk") + 1])
    if not os.path.exists(STARTF):
        with open(STARTF, "w") as f:
            f.write(str(time.time()))
        alog(LOG, f"[{ts()}] GUARD promote_guard_20261031.py start pid={os.getpid()} window={WATCH}s poll={POLL}s "
                  f"canonical pptx={CAN['pptx']} assets tl={CAN['tl']} tr={CAN['tr']} bl={CAN['bl']} br={CAN['br']}")
        with open(CAND, "a") as f:
            f.write(f"# PROMOTION_CANDIDATES — slide 025 clean PASS/PASS verdict pairs\n"
                    f"Started {ts()} by promote_guard_20261031.py (promoter/guard; agent-386 owns promotion; no DB writes).\n"
                    f"A pair qualifies when judge_full_*.txt + crop_dense_judge_*.txt share a tag, both contain a\n"
                    f"FINAL VERDICT ... PASS line (not FAIL / not 'PASS or'), both have zero '429' lines, and the\n"
                    f"judged render maps to a pptx md5 currently on disk.\n\n")
    start = float(open(STARTF).read().strip())
    deadline = start + WATCH
    chunk_end = time.time() + chunk if chunk else deadline
    end = min(deadline, chunk_end)
    st = load_state()
    while True:
        events, pairs, ready = poll(st)
        save_state(st)
        for e in events:
            print(f"{ts()} {e}", flush=True)
        for tag, f, c, pmd5, match in pairs:
            print(f"{ts()} NEW-PAIR tag={tag} pptx_md5={pmd5} on_disk_match={match} full={os.path.basename(f)} crop={os.path.basename(c)}", flush=True)
        for d in ready:
            print(f"{ts()} PROMOTE-READY deviant_pptx_md5={d}", flush=True)
        nowt = time.time()
        if once or nowt >= end or nowt >= deadline:
            break
        time.sleep(min(POLL, max(1, end - nowt)))
    if time.time() >= deadline:
        alog(LOG, f"[{ts()}] GUARD promote_guard_20261031.py window elapsed ({WATCH}s) polls={st['poll']} — exiting")
        print(f"{ts()} GUARD window elapsed polls={st['poll']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
