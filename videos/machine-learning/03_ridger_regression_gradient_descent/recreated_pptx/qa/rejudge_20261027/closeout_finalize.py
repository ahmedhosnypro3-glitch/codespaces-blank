#!/usr/bin/env python3
"""Fill $NS/CLOSEOUT_REPORT.md from live closeout data.

Read-only over DB / ledger / register / gate files; the only possible write is
$NS/CLOSEOUT_REPORT.md, and only when both guards pass:
  1. DB census: COUNT(*) FROM slides WHERE gen_status='passed' AND visual_check='PASS' == 51
  2. $RJ/merge_gate_FINAL.md exists and carries a PASS verdict line
The merge gate itself is never run here; its result file is only read.

Usage:
  python3 closeout_finalize.py            # write CLOSEOUT_REPORT.md if guards pass
  python3 closeout_finalize.py --dry-run  # print the report to stdout, write nothing
"""

import hashlib
import json
import os
import re
import sqlite3
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone

RJ = os.path.dirname(os.path.abspath(__file__))
NS = os.path.abspath(os.path.join(RJ, "..", "..", ".."))
DB = os.path.join(NS, "slides_progress.db")
LEDGER = os.path.join(NS, "recreated_pptx", "final_deck_state.json")
DECK = os.path.join(NS, "recreated_pptx",
                    "03_ridger_regression_gradient_descent_final.pptx")
REPORT = os.path.join(NS, "CLOSEOUT_REPORT.md")
REGISTER = os.path.join(RJ, "REJUDGE_REGISTER.md")
WRAP_LOG = os.path.join(RJ, "OMML_WRAP_LOG.md")
GATE_FINAL = os.path.join(RJ, "merge_gate_FINAL.md")
TEMPLATE = os.path.join(RJ, "CLOSEOUT_DRAFT.md")

EXPECTED = 51


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def db_census():
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    cur = con.cursor()
    total = cur.execute("SELECT COUNT(*) FROM slides").fetchone()[0]
    passed = cur.execute(
        "SELECT COUNT(*) FROM slides WHERE gen_status='passed' AND visual_check='PASS'"
    ).fetchone()[0]
    census = cur.execute(
        "SELECT gen_status, COALESCE(visual_check,''), COUNT(*) FROM slides "
        "GROUP BY 1,2 ORDER BY 3 DESC"
    ).fetchall()
    rows = cur.execute(
        "SELECT slide_id, gen_status, COALESCE(visual_check,''), COALESCE(last_error,'') "
        "FROM slides ORDER BY slide_id"
    ).fetchall()
    open_rows = cur.execute(
        "SELECT slide_id, gen_status, COALESCE(visual_check,''), COALESCE(last_error,'') "
        "FROM slides WHERE NOT (gen_status='passed' AND visual_check='PASS') ORDER BY slide_id"
    ).fetchall()
    con.close()
    return {"total": total, "passed": passed, "census": census, "rows": rows,
            "open": open_rows}


def ledger_summary():
    with open(LEDGER) as f:
        led = json.load(f)
    pages = led.get("pages", {})
    status_c = Counter(str(v.get("status")) for v in pages.values())
    rc_c = Counter(str(v.get("render_check")) for v in pages.values())
    events = led.get("events", [])
    deck_exists = os.path.exists(DECK)
    disk_md5 = md5_of(DECK) if deck_exists else None
    page_count = None
    if deck_exists:
        with zipfile.ZipFile(DECK) as z:
            page_count = len([n for n in z.namelist()
                              if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)])
    return {
        "deck_path": DECK, "deck_exists": deck_exists, "disk_md5": disk_md5,
        "page_count": page_count, "ledger_md5": led.get("deck_md5"),
        "md5_match": bool(disk_md5 and disk_md5 == led.get("deck_md5")),
        "total_pages": led.get("total_pages"), "scope": led.get("scope"),
        "doctrine": led.get("doctrine"),
        "status_census": dict(status_c), "render_census": dict(rc_c),
        "n_events": len(events), "last_event": events[-1] if events else None,
        "pages": {int(k): v for k, v in pages.items()},
    }


def parse_verdict_census():
    files = sorted((f for f in os.listdir(RJ) if f.startswith("VERDICT_CENSUS")),
                   key=lambda f: os.path.getmtime(os.path.join(RJ, f)))
    result = {"files": files, "used": None, "generated": None, "rows": {},
              "stats": []}
    if not files:
        return result
    used = files[-1]
    path = os.path.join(RJ, used)
    result["used"] = used
    with open(path) as f:
        text = f.read()
    m = re.search(r"Generated:\s*(.+)", text)
    result["generated"] = m.group(1).strip() if m else None
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 10 and re.fullmatch(r"\d{3}", cells[0]):
            n = int(cells[0])
            result["rows"][n] = {
                "full": cells[1], "full_file": cells[2], "full_mtime": cells[3],
                "crop": cells[4], "crop_file": cells[5], "crop_mtime": cells[6],
                "db_gen": cells[7], "db_vis": cells[8],
                "flags": cells[9] if len(cells) > 9 else "",
            }
    in_stats = False
    for line in text.splitlines():
        if line.startswith("## Stats"):
            in_stats = True
            continue
        if in_stats:
            if line.startswith("## "):
                break
            if line.strip().startswith("-"):
                result["stats"].append(line.strip().lstrip("- ").strip())
    return result


def register_census():
    baks = [f for f in os.listdir(RJ)
            if f.startswith("REJUDGE_REGISTER.md") and f != "REJUDGE_REGISTER.md"]
    summaries = sorted(f for f in os.listdir(RJ) if f.startswith("REJUDGE_SUMMARY"))
    size = os.path.getsize(REGISTER) if os.path.exists(REGISTER) else 0
    return {"path": REGISTER, "size_kb": round(size / 1024, 1), "backups": len(baks),
            "summaries": summaries}


def parse_wrap_log():
    wrapped, skipped = {}, []
    if not os.path.exists(WRAP_LOG):
        return {"wrapped": wrapped, "skipped": skipped, "exists": False}
    with open(WRAP_LOG) as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and re.fullmatch(r"\d{3}", cells[0]):
                outcome = cells[1]
                if "WRAPPED" in outcome:
                    m = re.search(r"(\d+)\s*mc:AlternateContent", outcome) or \
                        re.search(r"AltContent=(\d+)/", outcome)
                    wrapped[int(cells[0])] = {"outcome": outcome,
                                              "blocks": int(m.group(1)) if m else None}
                elif "SKIP" in outcome:
                    skipped.append((int(cells[0]), outcome))
    return {"wrapped": wrapped, "skipped": skipped, "exists": True}


def zip_scan_omml():
    wrapped, ac_total, omath_total = {}, 0, 0
    rp = os.path.join(NS, "recreated_pptx")
    for n in range(1, EXPECTED + 1):
        p = os.path.join(rp, "slide_%03d_recreated.pptx" % n)
        if not os.path.exists(p):
            continue
        ac = omath = 0
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name):
                    data = z.read(name).decode("utf-8", "replace")
                    ac += data.count("mc:AlternateContent")
                    omath += data.count("m:oMath")
        if ac:
            wrapped[n] = ac
            ac_total += ac
            omath_total += omath
    return {"wrapped": wrapped, "ac_blocks": ac_total, "omath": omath_total}


def parse_gate_final():
    if not os.path.exists(GATE_FINAL):
        return {"exists": False, "pass": False}
    with open(GATE_FINAL) as f:
        text = f.read()
    lines = text.splitlines()
    pass_line = next((l.strip() for l in lines
                      if re.search(r"(?i)\bPASS\b", l) and
                      re.search(r"(?i)(verdict|result|gate|overall)", l)), None)
    fail_line = next((l.strip() for l in lines
                      if re.search(r"(?i)\bFAIL\b", l) and
                      re.search(r"(?i)(verdict|result|gate|overall)", l)), None)
    exit_m = re.search(r"(?i)(?:exit(?:\s*code)?|rc)\s*[:=]?\s*(\d+)", text)
    mm = re.search(r"(?i)mismatched pages\s*\[([^\]]*)\]", text)
    mm_frac = re.search(r"(?i)(\d+)\s*/\s*(\d+)\s*mismatched", text)
    mismatched = None
    if mm:
        items = [x.strip() for x in mm.group(1).split(",") if x.strip()]
        mismatched = [int(x) for x in items if x.isdigit()]
    elif mm_frac:
        mismatched = int(mm_frac.group(1))
    return {"exists": True, "pass": bool(pass_line and not fail_line),
            "pass_line": pass_line, "fail_line": fail_line,
            "exit": int(exit_m.group(1)) if exit_m else None,
            "mismatched": mismatched}


def build_report(db, led, census, register, wrap, omml_scan, gate, dry_run):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    guards = []
    guards.append("DB passed&PASS = %d/%d %s" % (
        db["passed"], EXPECTED,
        "(OK)" if db["passed"] >= EXPECTED else "(BELOW 51 — write refused in real mode)"))
    if not gate["exists"]:
        guards.append("merge_gate_FINAL.md MISSING — write refused in real mode")
    else:
        guards.append("merge_gate_FINAL.md present, PASS marker %s" %
                      ("FOUND" if gate["pass"] else "ABSENT — write refused in real mode"))

    L = []
    a = L.append
    a("# CLOSEOUT_REPORT.md — machine-learning lecture 03: Ridge Regression & Gradient Descent")
    a("")
    if dry_run:
        a("Status: DRY RUN (printed by `closeout_finalize.py --dry-run` at %s; "
          "nothing was written). Section template: `%s`." % (now, os.path.basename(TEMPLATE)))
    else:
        a("Status: FINALIZED by `closeout_finalize.py` at %s from live data "
          "(DB + ledger + rejudge register/census + OMML log + merge gate file). "
          "Section template: `%s`." % (now, os.path.basename(TEMPLATE)))
    a("")
    a("Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`")
    a("RJ = `recreated_pptx/qa/rejudge_20261027/`")
    a("")
    a("Write guards at run time:")
    for g in guards:
        a("- %s" % g)
    a("")

    a("## 1. DB census (`slides_progress.db`, opened read-only)")
    a("")
    a("- Total rows: **%d**; `gen_status='passed' AND visual_check='PASS'`: **%d**" %
      (db["total"], db["passed"]))
    a("- Census by (gen_status, visual_check): " +
      ", ".join("`%s|%s` = %d" % r for r in db["census"]))
    if db["open"]:
        a("- Non-passed rows:")
        for sid, gen, vis, err in db["open"]:
            a("  - slide %03d: gen_status=`%s`, visual_check=`%s`, last_error: %s" %
              (sid, gen, vis, err))
    else:
        a("- Non-passed rows: none.")
    a("")

    a("## 2. Final deck + ledger (`recreated_pptx/final_deck_state.json`)")
    a("")
    a("- Deck: `%s`" % os.path.basename(DECK))
    a("- Page count (zip `ppt/slides/slideN.xml`): **%s**; ledger `total_pages`: **%s**" %
      (led["page_count"], led["total_pages"]))
    a("- md5 on disk: `%s`" % led["disk_md5"])
    a("- ledger `deck_md5`: `%s` → %s" %
      (led["ledger_md5"], "MATCH" if led["md5_match"] else "MISMATCH"))
    a("- scope: `%s`; doctrine: %s" % (led["scope"], led["doctrine"]))
    a("- Ledger page `status` census: " +
      ", ".join("%s = %d" % kv for kv in sorted(led["status_census"].items())))
    a("- Ledger `render_check` census: " +
      ", ".join("%s = %d" % kv for kv in sorted(led["render_census"].items())))
    a("- Events: %d (last: `%s` at %s)" %
      (led["n_events"], led["last_event"].get("action"), led["last_event"].get("at"))
      if led["last_event"] else "- Events: 0")
    a("")

    a("## 3. Rejudge census (2026-10-27 wave)")
    a("")
    a("- Register: `%s` (%.1f KB, append-only; %d backup/snapshot files kept); "
      "consolidated snapshots: %s" %
      (os.path.basename(REGISTER), register["size_kb"], register["backups"],
       ", ".join(register["summaries"]) or "none"))
    if census["used"]:
        a("- Verdict census source: `%s` (generated %s); files present: %s" %
          (census["used"], census["generated"], ", ".join(census["files"])))
        rows = census["rows"]
        fulls = Counter(r["full"] for r in rows.values())
        crops = Counter(r["crop"] for r in rows.values())
        both = sum(1 for r in rows.values() if r["full"] == "PASS" and r["crop"] == "PASS")
        a("- Newest-clean FULL verdicts: " +
          ", ".join("%s = %d" % kv for kv in sorted(fulls.items())))
        a("- Newest-clean CROP verdicts: " +
          ", ".join("%s = %d" % kv for kv in sorted(crops.items())))
        a("- Both legs clean: **%d** of %d slides with census rows" % (both, len(rows)))
        gaps = [n for n, r in sorted(rows.items())
                if r["full"] not in ("PASS", "FAIL") or r["crop"] not in ("PASS", "FAIL")]
        if gaps:
            a("- Gap list (no clean verdict on a leg): %s" %
              ", ".join("%03d (%s/%s)" % (n, rows[n]["full"], rows[n]["crop"]) for n in gaps))
        for s in census["stats"]:
            a("- census stat: %s" % s)
    else:
        a("- No VERDICT_CENSUS files found under RJ.")
    a("")

    a("## 4. OMML wrapped slides (`OMML_WRAP_LOG.md` + live zip scan)")
    a("")
    if wrap["exists"]:
        if wrap["wrapped"]:
            a("- Wrapped per wrap log: " + ", ".join(
                "%03d (%s%s)" % (n, w["outcome"].split("(")[0].strip(),
                                 ", %d blocks" % w["blocks"] if w["blocks"] else "")
                for n, w in sorted(wrap["wrapped"].items())))
        else:
            a("- Wrapped per wrap log: none recorded.")
        if wrap["skipped"]:
            a("- Skipped per wrap log: " +
              ", ".join("%03d (%s)" % (n, o) for n, o in wrap["skipped"]))
    else:
        a("- OMML_WRAP_LOG.md missing.")
    a("- Live zip scan of the 51 `slide_NNN_recreated.pptx`: **%d slides wrapped — %s**; "
      "%d `mc:AlternateContent` blocks, %d `m:oMath` occurrences total" %
      (len(omml_scan["wrapped"]),
       ", ".join("%03d" % n for n in sorted(omml_scan["wrapped"])) or "none",
       omml_scan["ac_blocks"], omml_scan["omath"]))
    a("")

    a("## 5. Merge gate (`merge_gate_FINAL.md`, agent-441 — read only, never run here)")
    a("")
    if not gate["exists"]:
        a("- **FILE MISSING** — closeout cannot be written in real mode until it exists "
          "with a PASS verdict.")
    else:
        a("- Gate EXIT: %s" % (gate["exit"] if gate["exit"] is not None else "not recorded"))
        a("- Verdict line: `%s`" % (gate["pass_line"] or gate["fail_line"] or "(none found)"))
        a("- Gate result: **%s**" % ("PASS" if gate["pass"] else "NO PASS MARKER / FAIL"))
        mm = gate["mismatched"]
        if isinstance(mm, list):
            a("- Mismatched pages: %d %s" % (len(mm), mm if mm else "(none — 0/51)"))
        elif mm is not None:
            a("- Mismatched pages: %s" % mm)
        else:
            a("- Mismatched pages: not recorded")
    a("")

    a("## 6. Per-slide table (51 rows, live)")
    a("")
    a("| slide | DB gen_status | DB visual_check | Rejudge FULL (newest clean) | "
      "Rejudge CROP (newest clean) | Deck page status | Deck render_check |")
    a("|---|---|---|---|---|---|---|")
    for sid, gen, vis, _err in db["rows"]:
        c = census["rows"].get(sid, {})
        pg = led["pages"].get(sid, {})
        a("| %03d | %s | %s | %s | %s | %s | %s |" % (
            sid, gen, vis or "(blank)",
            c.get("full", "—"), c.get("crop", "—"),
            pg.get("status", "—"), pg.get("render_check", "—")))
    a("")

    a("## 7. Evidence locations")
    a("")
    ev = [
        ("Rejudge wave dir (this RJ)", "recreated_pptx/qa/rejudge_20261027/",
         ["REJUDGE_REGISTER.md (+ .bak*/snapshot files)", "VERDICT_CENSUS_*.md",
          "REJUDGE_SUMMARY_r*.md", "OMML_WRAP_LOG.md / OMML_INVENTORY_r*.md / OMML_WRAP_PLAN_r3.md",
          "merge_gate_plan.md / merge_gate_FINAL.md (agent-441)",
          "CLOSEOUT_DRAFT.md / CLOSEOUT_GAPLIST.md / CLOSEOUT_EVIDENCE_INDEX.md / closeout_pack/",
          "deck_gate_r*.txt / deck_updates_r*.txt / sweep_r*.md / fleet_census_r1.md",
          "per-slide dirs slide001..slide051 (+ alternates) with leg transcripts",
          "drivers: rejudge_driver.sh, rejudge_slide.sh, rejudge_adjudicate.py, payload_B_*.txt"]),
        ("Per-slide QA", "recreated_pptx/qa/",
         ["slideNNN/ and slide_0NN/ dirs", "final_deck_updates/gate_*/gate_report.txt"]),
        ("Build chain + ledger", "recreated_pptx/",
         ["build/ (per-slide scripts, components/, assets/ eq+plots, final_deck/ tooling)",
          "final_deck_state.json (ledger)", "03_ridger_regression_gradient_descent_final.pptx",
          "slide_NNN_recreated.pptx x51 (single-version deliverables)"]),
        ("Namespace root", "",
         ["CLOSEOUT_REPORT.md (this file)", "AGENTS.md", "slides_progress.db",
          "SOURCES_MAP.md", "sources/slide_NNN_source/SOURCES.md (51/51)",
          "analysis/ (slide_NNN_raw.json + slide_NNN_final.json + summary.md)",
          "unique_slides/slide_001..051.jpg"]),
        ("This script + dry run", "recreated_pptx/qa/rejudge_20261027/",
         ["closeout_finalize.py", "closeout_dryrun.md"]),
    ]
    for title, base, items in ev:
        a("- **%s** — `%s`" % (title, base or "namespace root"))
        for it in items:
            a("  - `%s`" % (base + it if base else it))
    a("")
    a("Laws: never git, never delete banked evidence; qa/ + scratch/ untracked by convention.")
    a("")
    return "\n".join(L)


def main():
    dry_run = "--dry-run" in sys.argv[1:]
    db = db_census()
    led = ledger_summary()
    census = parse_verdict_census()
    register = register_census()
    wrap = parse_wrap_log()
    omml_scan = zip_scan_omml()
    gate = parse_gate_final()

    report = build_report(db, led, census, register, wrap, omml_scan, gate, dry_run)

    if dry_run:
        print(report)
        print("\n[dry-run] guards: DB %d/%d passed; merge_gate_FINAL.md %s -> "
              "real mode would %s" % (
                  db["passed"], EXPECTED,
                  "present, PASS=%s" % gate["pass"] if gate["exists"] else "MISSING",
                  "WRITE" if (db["passed"] >= EXPECTED and gate["exists"] and gate["pass"])
                  else "REFUSE TO WRITE"),
              file=sys.stderr)
        return 0

    if db["passed"] < EXPECTED:
        print("REFUSE: DB passed&PASS = %d < %d; not writing %s"
              % (db["passed"], EXPECTED, REPORT), file=sys.stderr)
        return 2
    if not gate["exists"]:
        print("REFUSE: %s missing; not writing %s" % (GATE_FINAL, REPORT),
              file=sys.stderr)
        return 3
    if not gate["pass"]:
        print("REFUSE: %s has no PASS verdict (fail line: %s); not writing %s"
              % (GATE_FINAL, gate["fail_line"], REPORT), file=sys.stderr)
        return 4

    with open(REPORT, "w") as f:
        f.write(report)
    print("wrote %s (%d bytes); DB %d/%d, gate PASS exit=%s mismatched=%s"
          % (REPORT, len(report), db["passed"], EXPECTED, gate["exit"],
             gate["mismatched"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
