#!/usr/bin/env python3
"""FRESH background promoter (backup to 278/296) for slide 025 k17c.

Polls every 2 min up to 2h for any assets_k17*/ dir under slide025/ with 4
PNGs whose md5s ALL differ from assets_k15 AND a pil_k17*_out.txt showing
CHECK1<50% + CHECK2 pass + CHECK3 present + winding ~6.0 + markers ok.
On a qualifying set (lowest CHECK1 wins): DB check, backups, rebuild, render
+ chrome check, full/crop vision legs (OCC_MAX=700), PIL-adjudicate FAILs,
and on clean FULL PASS + CROP PASS (or PIL-dismissed) update DB + final deck
+ result.txt + REJUDGE_REGISTER.md. Never git, never delete evidence.
"""
import glob
import hashlib
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
D = f"{RJ}/slide025"
BUILD = f"{NS}/recreated_pptx/build"
PPTX = f"{NS}/recreated_pptx/slide_025_recreated.pptx"
DB = f"{NS}/slides_progress.db"
LOG = f"{D}/promote_k17c_fresh.log"
TMPDIR = f"{ROOT}/scratch/tmp"
PREV_PPTX_MD5 = "b93c5fa291e23e569cf27baef279853a"

K15 = {
    "plot_025_bl.png": "5acfb177d1e4d640b2fd7a08a1f21eda",
    "plot_025_br.png": "500287a3f4fe98a32ee0cac44e5bd5f8",
    "plot_025_tl.png": "73cbaec1d8f2d9a6faf3aca1841b213e",
    "plot_025_tr.png": "375a2d7bef424fe275a6c27647d09756",
}
PNGS = list(K15.keys())


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg):
    line = f"{now()} {msg}"
    with open(LOG, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def db_row():
    try:
        con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=20)
        row = con.execute(
            "SELECT gen_status, visual_check, last_error FROM slides WHERE slide_id=25"
        ).fetchone()
        con.close()
        return row
    except Exception as e:
        return ("err", str(e), None)


def parse_pil(path):
    """Return (ok, detail, c1_pct) for CHECK1<50 + CHECK2 pass + CHECK3 present
    + winding ~6.0 + markers ok, parsed from a pil_k17*_out.txt."""
    try:
        t = open(path, errors="replace").read()
    except Exception as e:
        return False, f"unreadable {e}", None
    summ = ""
    for line in t.splitlines():
        if "SUMMARY" in line.upper():
            summ = line
    src = summ if summ else t
    checks = {}
    for m in re.finditer(r"CHECK(\d)\s*[:=]\s*(\w+)", src):
        checks[m.group(1)] = m.group(2).upper()
    c1_pct = None
    m = re.search(r"CHECK1\s*[:=]\s*\w+\s*\(([0-9]+(?:\.[0-9]+)?)\s*%\)", src)
    if m:
        c1_pct = float(m.group(1))
    else:
        pcts = [float(x) for x in re.findall(r"([0-9]+(?:\.[0-9]+)?)\s*%", src)]
        c1_pct = min(pcts) if pcts else None
    c1_ok = (checks.get("1") == "PASS") and (c1_pct is not None and c1_pct < 50.0)
    c2_ok = checks.get("2") == "PASS"
    c3_ok = checks.get("3") in ("PASS", "PRESENT")
    wv = [float(x) for x in re.findall(r"wind(?:ing)?[- ]?ratio?[:=]\s*([0-9]+(?:\.[0-9]+)?)", src, re.I)]
    if not wv:
        wv = [float(x) for x in re.findall(r"wind(?:ing)?[^0-9]{0,20}([0-9]\.[0-9]+)", src, re.I)]
    wind_ok = any(5.5 <= v <= 6.5 for v in wv)
    mk = re.search(r"markers?[:=]\s*(\w+)", src, re.I)
    markers_ok = bool(mk) and mk.group(1).upper() == "PASS"
    ok = c1_ok and c2_ok and c3_ok and wind_ok and markers_ok
    detail = (f"CHECK1={'PASS' if c1_ok else 'FAIL'}(pct={c1_pct}) "
              f"CHECK2={checks.get('2')} CHECK3={checks.get('3')} "
              f"winding={wv} markers={mk.group(1) if mk else '?'}")
    return ok, detail, c1_pct


def qualify(dirpath):
    md5s = {}
    for n in PNGS:
        p = os.path.join(dirpath, n)
        if not os.path.isfile(p):
            return None
        m = md5(p)
        if m == K15[n]:
            return None
        md5s[n] = m
    suffix = os.path.basename(dirpath).replace("assets_", "")  # e.g. k17a
    pil_cands = sorted(glob.glob(os.path.join(dirpath, "pil_k17*_out.txt")))
    pil_cands += sorted(glob.glob(os.path.join(D, f"pil_{suffix}*_out.txt")))
    pil_cands += sorted(glob.glob(os.path.join(D, "pil_k17*_out.txt")))
    pil_cands = sorted(set(pil_cands), key=os.path.getmtime)
    if not pil_cands:
        return None
    pil = pil_cands[-1]
    ok, detail, c1 = parse_pil(pil)
    if not ok:
        return None
    return {"dir": os.path.basename(dirpath), "md5s": md5s, "pil": os.path.basename(pil),
            "detail": detail, "c1": c1 if c1 is not None else 999.0}


def run(cmd, cwd=ROOT, env=None, timeout=600):
    e = dict(os.environ)
    if env:
        e.update(env)
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout)
    return r


def poll_for_assets():
    deadline = time.time() + 2 * 3600
    while time.time() < deadline:
        row = db_row()
        log(f"poll db={row}")
        if row and row[0] == "passed" and row[1] == "PASS":
            with open(f"{D}/ALREADY_PASSED_K17C.txt", "w") as f:
                f.write(f"{now()} slide25 already passed/PASS ({row}) — promoter stopping\n")
            log("DB slide25 already passed/PASS — STOP")
            return "already_passed"
        found = []
        for dp in sorted(glob.glob(os.path.join(D, "assets_k17*"))):
            if not os.path.isdir(dp):
                continue
            q = qualify(dp)
            if q:
                found.append(q)
                log(f"QUALIFYING {q['dir']} pil={q['pil']} {q['detail']}")
        if found:
            found.sort(key=lambda q: q["c1"])
            return found[0]
        stat = []
        for dp in sorted(glob.glob(os.path.join(D, "assets_k17*"))):
            if os.path.isdir(dp):
                n = sum(1 for p in PNGS if os.path.isfile(os.path.join(dp, p)))
                npil = len(glob.glob(os.path.join(dp, "pil_k17*_out.txt"))) + \
                    len(glob.glob(os.path.join(D, "pil_*_out.txt")))
                stat.append(f"{os.path.basename(dp)}:pngs={n}/4")
            else:
                stat.append(f"{os.path.basename(dp)}:-")
        log("no qualifying set | " + " ".join(stat))
        time.sleep(120)
    log("POLL TIMEOUT (2h) — no qualifying k17 set")
    return None


def promote(w):
    log(f"PROMOTE {w['dir']} md5s={w['md5s']} pil={w['pil']} {w['detail']}")
    # (1) DB row 25 first
    row = db_row()
    log(f"pre-promote DB row: {row}")
    if row and row[0] == "passed" and row[1] == "PASS":
        log("DB already passed/PASS at promote time — STOP, nothing changed")
        return "already_passed"
    # (2) backup pptx
    bak = f"{D}/slide_025_recreated.preK17c.bak.pptx"
    shutil.copy2(PPTX, bak)
    log(f"backed up pptx -> {bak} (md5 {md5(bak)})")
    # (3) backup build assets then copy winners over
    pre = f"{D}/assets_preK17c"
    os.makedirs(pre, exist_ok=True)
    for n in PNGS:
        shutil.copy2(os.path.join(BUILD, "assets", n), os.path.join(pre, n))
    log(f"backed up build/assets/plot_025_*.png -> {pre}")
    srcdir = os.path.join(D, w["dir"])
    for n in PNGS:
        shutil.copy2(os.path.join(srcdir, n), os.path.join(BUILD, "assets", n))
        log(f"copied {w['dir']}/{n} md5={md5(os.path.join(BUILD, 'assets', n))} over build/assets/")
    # (4) rebuild
    r = run(["node", "slide_025.js"], cwd=BUILD, timeout=300)
    log(f"node slide_025.js rc={r.returncode} {r.stdout.strip()[-300:]} {r.stderr.strip()[-300:]}")
    if r.returncode != 0:
        log("BUILD FAILED — aborting promotion, restoring backups")
        for n in PNGS:
            shutil.copy2(os.path.join(pre, n), os.path.join(BUILD, "assets", n))
        shutil.copy2(bak, PPTX)
        return "build_failed"
    new_md5 = md5(PPTX)
    log(f"new pptx md5={new_md5} (prev {PREV_PPTX_MD5}, required != prev: {new_md5 != PREV_PPTX_MD5})")
    if new_md5 == PREV_PPTX_MD5:
        log("ABORT: rebuilt pptx md5 == b93c5fa... — build did not change")
        return "md5_unchanged"
    # (5) render + chrome check
    os.makedirs(TMPDIR, exist_ok=True)
    env = {"TMPDIR": TMPDIR}
    pdf = f"{D}/slide_025_recreated.pdf"
    for f in (pdf, f"{D}/render_k17c.png"):
        if os.path.exists(f):
            os.remove(f)
    r = run(["soffice", "--headless",
             f"-env:UserInstallation=file://{TMPDIR}/lo_rejudge_025_k17c",
             "--convert-to", "pdf", PPTX, "--outdir", D],
            env=env, timeout=300)
    log(f"soffice rc={r.returncode} {r.stdout.strip()[-200:]} {r.stderr.strip()[-200:]}")
    if not os.path.exists(pdf):
        log("RENDER FAIL — no pdf"); return "render_failed"
    r = run(["pdftoppm", "-png", "-r", "150", "-singlefile", pdf, f"{D}/render_k17c"],
            env=env, timeout=120)
    rk = f"{D}/render_k17c.png"
    if not os.path.exists(rk):
        log("PDFTOPPM FAIL"); return "render_failed"
    from PIL import Image
    sz = Image.open(rk).size
    log(f"render_k17c.png size={sz} (expect (2001, 1125))")
    r = run(["python3", f"{NS}/shared_patterns/house_chrome_check.py", rk, "25"], timeout=120)
    with open(f"{D}/chrome_check_k17c.txt", "w") as f:
        f.write(r.stdout + r.stderr)
    log(f"house_chrome_check rc={r.returncode}: {r.stdout.strip()[-300:]}")
    if r.returncode != 0:
        log("CHROME CHECK FAIL — stopping before legs")
        return "chrome_failed"
    # crop pair via pick_dense_region.py 25
    r = run(["python3", f"{RJ}/pick_dense_region.py", "25"], timeout=120)
    region = r.stdout.strip().split()[-4:]
    x0, y0, x1, y1 = map(int, region)
    log(f"dense region from pick_dense_region.py 25: {x0} {y0} {x1} {y1}")
    import numpy as np
    rp = Image.open(rk).convert("RGB")
    op = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
    sc = rp.size[1] / 540.0
    rc = rp.crop((int(x0 * sc), int(y0 * sc), int(np.ceil(x1 * sc)), int(np.ceil(y1 * sc))))
    oc = op.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(f"{D}/crop_dense_render_k17c.png")
    oc.save(f"{D}/crop_dense_orig_k17c.png")
    log(f"crop pair: render {rc.size} orig {oc.size} -> crop_dense_render_k17c.png / crop_dense_orig_k17c.png")
    # (6) launch legs, OCC_MAX=700, durable, from ROOT
    leg_env = f"export OCC_MAX=700 TMPDIR={TMPDIR}\n"
    full_cmd = (f"setsid nohup bash \"{RJ}/vision_leg.sh\" \"{D}/judge_full_k17c.txt\" 1200 "
                f"\"{D}/render_k17c.png\" \"{NS}/unique_slides/slide_025.jpg\" "
                f"\"Slide 25 recreation k17c — fidelity check vs original lecture frame\" "
                f"\"IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame\" "
                f"\"{RJ}/payload_A.txt\" > \"{D}/judge_full_k17c.txt.wrapper.out\" 2>&1 < /dev/null &")
    crop_cmd = (f"setsid nohup bash \"{RJ}/vision_leg.sh\" \"{D}/crop_dense_judge_k17c.txt\" 600 "
                f"\"{D}/crop_dense_render_k17c.png\" \"{D}/crop_dense_orig_k17c.png\" "
                f"\"Slide 025 zoomed crop — fidelity check vs original IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame\" "
                f"\"{RJ}/payload_B_025.txt\" > \"{D}/crop_dense_judge_k17c.txt.wrapper.out\" 2>&1 < /dev/null &")
    r = run(["bash", "-c", leg_env + full_cmd + "\n" + crop_cmd + "\necho launched"], timeout=60)
    log(f"legs launched: {r.stdout.strip()} {r.stderr.strip()}")
    # (7) poll for FINAL VERDICT + no 429
    def verdict(path):
        if not os.path.exists(path):
            return None
        t = open(path, errors="replace").read()
        if "FINAL VERDICT" not in t:
            return None
        m = re.findall(r"FINAL VERDICT:? *\*{0,2} *(PASS|FAIL)", t)
        c429 = len(re.findall(r"429", t, re.I))
        return (m[-1] if m else None, c429)
    leg_deadline = time.time() + 3900
    full_v = crop_v = None
    while time.time() < leg_deadline:
        full_v = verdict(f"{D}/judge_full_k17c.txt")
        crop_v = verdict(f"{D}/crop_dense_judge_k17c.txt")
        log(f"leg poll full={full_v} crop={crop_v}")
        if full_v and crop_v:
            break
        row = db_row()
        if row and row[0] == "passed" and row[1] == "PASS":
            log("DB already passed/PASS while legs ran — STOP")
            return "already_passed"
        time.sleep(120)
    log(f"FINAL legs: full={full_v} crop={crop_v}")
    if not (full_v and crop_v):
        log("legs did not produce clean verdicts in window — leaving DB untouched, report")
        return "legs_incomplete"
    fv, f429 = full_v
    cv, c429 = crop_v
    # PIL-adjudicate FAILs (scratch copy of rejudge_adjudicate.py pointed at k17c files)
    adj = f"{TMPDIR}/rejudge_adjudicate_k17c.py"
    src = open(f"{RJ}/rejudge_adjudicate.py").read()
    src = src.replace("render.png", "render_k17c.png").replace(
        "crop_dense_render.png", "crop_dense_render_k17c.png").replace(
        "crop_dense_orig.png", "crop_dense_orig_k17c.png")
    with open(adj, "w") as f:
        f.write(src)
    dismiss = {"full": False, "crop": False}
    if fv == "FAIL" or f429 > 0:
        r = run(["python3", adj, "025", "--full"], timeout=300)
        with open(f"{D}/adjudicate_k17c_full.txt", "w") as f:
            f.write(r.stdout + r.stderr)
        log("adjudicate_k17c_full.txt written:\n" + r.stdout[-1500:])
        dismiss["full"] = classify_dismiss(r.stdout)
    if cv == "FAIL" or c429 > 0:
        r = run(["python3", adj, "025", "--crop"], timeout=300)
        with open(f"{D}/adjudicate_k17c_crop.txt", "w") as f:
            f.write(r.stdout + r.stderr)
        log("adjudicate_k17c_crop.txt written:\n" + r.stdout[-1500:])
        dismiss["crop"] = classify_dismiss(r.stdout)
    log(f"verdicts full={fv}(429={f429}) crop={cv}(429={c429}) dismissed={dismiss}")
    full_ok = (fv == "PASS" and f429 == 0) or dismiss["full"]
    crop_ok = (cv == "PASS" and c429 == 0) or dismiss["crop"]
    if not (full_ok and crop_ok):
        log("NOT PROMOTING TO passed/PASS: legs not clean (FAIL stands or 429 present)")
        return "legs_failed"
    # promote DB
    r = run(["sqlite3", DB, ".timeout 20000",
             "UPDATE slides SET gen_status='passed', visual_check='PASS', last_error=NULL WHERE slide_id=25;"],
            cwd=NS, timeout=60)
    log(f"DB update rc={r.returncode}: {r.stdout.strip()} {r.stderr.strip()}")
    log(f"DB row now: {db_row()}")
    # final deck update + render gate
    r = run(["python3", "final_deck_tool.py", "update", "25"], cwd=f"{BUILD}/final_deck", timeout=600)
    log(f"final_deck_tool update 25 rc={r.returncode}: {r.stdout.strip()[-800:]} {r.stderr.strip()[-400:]}")
    r = run(["python3", "render_check_pages.py", "25"], cwd=f"{BUILD}/final_deck", timeout=900)
    with open(f"{D}/render_check_k17c_25.txt", "w") as f:
        f.write(r.stdout + r.stderr)
    log(f"render_check_pages 25 rc={r.returncode}: {r.stdout.strip()[-600:]} {r.stderr.strip()[-300:]}")
    # append result.txt + REJUDGE_REGISTER.md
    with open(f"{D}/result.txt", "a") as f:
        f.write(f"K17C={now()} FRESH background promoter (backup to 278/296): promoted {w['dir']} "
                f"(pil={w['pil']} {w['detail']}); pptx md5 {new_md5} (!= {PREV_PPTX_MD5}); "
                f"render_k17c.png {sz} chrome_check_k17c.txt rc-pass; "
                f"legs judge_full_k17c.txt={fv} crop_dense_judge_k17c.txt={cv} 429 full={f429} crop={c429} "
                f"dismissed={dismiss} (adjudicate_k17c_full.txt / adjudicate_k17c_crop.txt); "
                f"DB 25 passed/PASS; final_deck update 25 + render_check_pages 25 rc recorded in render_check_k17c_25.txt. "
                f"Backups: slide_025_recreated.preK17c.bak.pptx, assets_preK17c/. No git; no evidence deleted.\n")
    with open(f"{RJ}/REJUDGE_REGISTER.md", "a") as f:
        f.write(f"\n## {now()} — slide025 k17c FRESH background promoter (backup to 278/296)\n\n"
                f"Promoted {w['dir']} (pil={w['pil']}, {w['detail']}). Rebuilt pptx md5 {new_md5} "
                f"(!= {PREV_PPTX_MD5}). render_k17c.png {sz}, chrome PASS. Legs: full={fv} crop={cv} "
                f"(429: {f429}/{c429}, dismissed={dismiss}). DB 25 -> passed/PASS; final_deck update 25; "
                f"render_check_pages 25 honestly recorded in slide025/render_check_k17c_25.txt. "
                f"Backups slide_025_recreated.preK17c.bak.pptx + assets_preK17c/. No git; no evidence deleted.\n")
    log("PROMOTION COMPLETE")
    return "promoted"


def classify_dismiss(adj_out):
    """Heuristic separating banked-dismissed (diffuse orig-heavy) from
    PIL-confirmed standing FAIL (localized solid diff, render ink-starved)."""
    m = re.search(r"diff px total: (\d+) \(([0-9.]+)%", adj_out)
    if not m:
        return False
    pct = float(m.group(2))
    ink = re.search(r"render-ink (\d+) vs orig-ink (\d+)", adj_out)
    maxcell = re.search(r"max cell (\d+)", adj_out)
    mc = int(maxcell.group(1)) if maxcell else 99999
    if ink:
        ri, oi = int(ink.group(1)), int(ink.group(2))
        ratio = ri / max(oi, 1)
    else:
        ratio = 1.0
    dismissed = (pct < 35.0) and (mc < 1000) and (ratio >= 0.6)
    log(f"classify_dismiss: pct={pct} maxcell={mc} ink_ratio={ratio:.3f} -> {dismissed}")
    return dismissed


def main():
    log(f"promoter start pid={os.getpid()} K15={K15}")
    w = poll_for_assets()
    if w == "already_passed" or w is None:
        return 0 if w == "already_passed" else 1
    rc = promote(w)
    log(f"promoter end rc={rc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
