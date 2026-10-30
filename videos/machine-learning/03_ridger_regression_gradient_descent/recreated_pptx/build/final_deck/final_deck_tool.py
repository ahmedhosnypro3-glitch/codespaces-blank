#!/usr/bin/env python3
"""Continuous final deck tool — deck 03 (final-deck-merge doctrine).

Subcommands:
  verify-structure   fail-loud OPC structural check of the current final deck
  init-ledger        write final_deck_state.json (all pages placeholder)
  update             MODE=update N [N ...]: replace pages with certified slide
                     content at the OPC package level (slide XML verbatim, rels
                     retargeted, media renamed per slide), atomically, with a
                     post-write self-check; append ledger rows.

Laws (skill references/patterns/final-deck-merge/README.md + MERGE_RUNBOOK):
- page count and order are CONSTANT from init (51 pages, slide order 1..51);
- certified page content is byte-identical to the per-slide deck's content —
  slide/notes XML and media bytes are copied VERBATIM, never re-encoded; only
  the per-slide .rels targets are retargeted;
- the deck file is written atomically (temp + rename) so a crashed update
  never leaves a torn package; the deck md5 is banked after every update;
- skeleton parts (layout/master/theme/notesMaster) are md5-checked against the
  source; a difference is a WARN (the render gate arbitrates).
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sqlite3
import sys
import zipfile
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent")
PPTX_DIR = NS / "recreated_pptx"
DECK = PPTX_DIR / "03_ridger_regression_gradient_descent_final.pptx"
LEDGER = PPTX_DIR / "final_deck_state.json"
DB = NS / "slides_progress.db"
TOTAL = 51

SKELETON_PARTS = (
    "ppt/slideLayouts/slideLayout1.xml",
    "ppt/slideMasters/slideMaster1.xml",
    "ppt/theme/theme1.xml",
    "ppt/notesMasters/notesMaster1.xml",
)
RELS_RE = re.compile(r'<Relationship Id="([^"]+)" Type="([^"]+)" Target="([^"]+)"/>')


def md5(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()


def now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


def fail(msg: str) -> None:
    sys.exit(f"FATAL: {msg}")


def load_ledger() -> dict:
    if not LEDGER.is_file():
        fail(f"ledger missing: {LEDGER}")
    return json.loads(LEDGER.read_text())


def save_ledger(state: dict) -> None:
    tmp = LEDGER.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2) + "\n")
    os.replace(tmp, LEDGER)


def verify_structure(deck: Path = DECK) -> None:
    if not deck.is_file() or deck.stat().st_size == 0:
        fail(f"final deck missing or empty: {deck}")
    z = zipfile.ZipFile(deck)
    names = set(z.namelist())
    for n in range(1, TOTAL + 1):
        if f"ppt/slides/slide{n}.xml" not in names:
            fail(f"deck lacks ppt/slides/slide{n}.xml (page-count law)")
    pres = z.read("ppt/presentation.xml").decode()
    sld_ids = re.findall(r'<p:sldId id="\d+" r:id="(rId\d+)"/>', pres)
    if len(sld_ids) != TOTAL:
        fail(f"presentation.xml has {len(sld_ids)} sldIds, expected {TOTAL}")
    prels = z.read("ppt/_rels/presentation.xml.rels").decode()
    rid2t = {rid: target for rid, _, target in RELS_RE.findall(prels)}
    for n in range(1, TOTAL + 1):
        target = rid2t.get(f"rId{n + 1}", "")
        if target != f"slides/slide{n}.xml":
            fail(f"presentation rels: rId{n + 1} -> {target!r}, expected slides/slide{n}.xml")
    ct = z.read("[Content_Types].xml").decode()
    for n in range(1, TOTAL + 1):
        if f'PartName="/ppt/slides/slide{n}.xml"' not in ct:
            fail(f"[Content_Types].xml lacks override for slide{n}.xml")
    print(f"structure OK: {TOTAL} pages, rels map rId(n+1)->slides/slideN.xml, "
          f"content-type overrides present")


def db_certified() -> dict:
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT slide_id, gen_status, visual_check, pptx_path FROM slides").fetchall()
    finally:
        con.close()
    cert = {}
    for sid, gs, vc, pptx in rows:
        if gs == "passed" and vc == "PASS":
            cert[int(sid)] = pptx or ""
    return cert


def init_ledger() -> None:
    verify_structure()
    state = {
        "deck": str(DECK),
        "doctrine": "continuous final deck (founder directive 2026-10-25); "
                    "skill references/patterns/final-deck-merge",
        "scope": "S21_continuous_final_deck (run 299640)",
        "total_pages": TOTAL,
        "deck_md5": md5(DECK.read_bytes()),
        "pages": {str(n): {"page": n, "status": "placeholder", "updated_at": now()}
                  for n in range(1, TOTAL + 1)},
        "events": [{"at": now(), "action": "placeholder-init",
                    "detail": f"{TOTAL} placeholder pages, blank-count gate pending"}],
    }
    save_ledger(state)
    print(f"ledger initialized: {LEDGER} (deck md5 {state['deck_md5']})")


def ensure_content_types(ct: str, n: int, new_media_exts: list[str]) -> str:
    for part, kind in ((f"/ppt/slides/slide{n}.xml", "slide"),
                       (f"/ppt/notesSlides/notesSlide{n}.xml", "notesSlide")):
        if f'PartName="{part}"' not in ct:
            add = (f'<Override PartName="{part}" ContentType="application/'
                   f'vnd.openxmlformats-officedocument.presentationml.{kind}+xml"/>')
            ct = ct.replace("</Types>", add + "</Types>")
    for ext in new_media_exts:
        if f'Default Extension="{ext}"' not in ct:
            mime = {"png": "image/png", "jpeg": "image/jpeg", "jpg": "image/jpeg",
                    "gif": "image/gif", "svg": "image/svg+xml"}.get(ext)
            if not mime:
                fail(f"unhandled media extension .{ext} for page {n}")
            ct = ct.replace("</Types>",
                            f'<Default Extension="{ext}" ContentType="{mime}"/>' + "</Types>")
    return ct


def update_pages(pages: list[int]) -> None:
    verify_structure()
    state = load_ledger()
    if state.get("total_pages") != TOTAL:
        fail("ledger total_pages mismatch")
    cert = db_certified()

    deck_md5_before = md5(DECK.read_bytes())

    warnings = []
    with zipfile.ZipFile(DECK) as zin:
        order = zin.namelist()
        data = {name: zin.read(name) for name in order}

    replaced = {}   # part -> expected md5
    removed = set()

    for n in sorted(pages):
        if not (1 <= n <= TOTAL):
            fail(f"page {n} out of range 1..{TOTAL}")
        if n not in cert:
            fail(f"page {n} is not certified (gen_status='passed' AND visual_check='PASS') — "
                 f"the update law refuses uncertified content")
        src = PPTX_DIR / f"slide_{n:03d}_recreated.pptx"
        db_name = Path(cert[n]).name
        if db_name and db_name != src.name:
            fail(f"DB pptx_path for slide {n} is {db_name!r} but convention gives {src.name!r}")
        if not src.is_file() or src.stat().st_size == 0:
            fail(f"certified slide {n} has no pptx on disk: {src}")
        src_md5 = md5(src.read_bytes())
        z = zipfile.ZipFile(src)
        snames = set(z.namelist())
        for part in ("ppt/slides/slide1.xml", "ppt/slides/_rels/slide1.xml.rels",
                     "ppt/notesSlides/notesSlide1.xml", "ppt/notesSlides/_rels/notesSlide1.xml.rels"):
            if part not in snames:
                fail(f"source slide {n} lacks {part}")

        # skeleton parity vs the CURRENT deck parts (WARN, render gate arbitrates)
        for part in SKELETON_PARTS:
            if part in snames and data.get(part) is not None and z.read(part) != data[part]:
                warnings.append(f"page {n}: skeleton part {part} differs from deck "
                                f"(relying on render gate)")

        # 1. slide XML verbatim
        data[f"ppt/slides/slide{n}.xml"] = z.read("ppt/slides/slide1.xml")
        replaced[f"ppt/slides/slide{n}.xml"] = md5(data[f"ppt/slides/slide{n}.xml"])

        # 2. slide rels: retarget layout/notesSlide/media
        rels = z.read("ppt/slides/_rels/slide1.xml.rels").decode("utf-8")
        media_bases = []
        for m in z.namelist():
            if m.startswith("ppt/media/") and not m.endswith("/"):
                media_bases.append(Path(m).name)

        def retarget(mo):
            rid, rtype, target = mo.groups()
            t = rtype.rsplit("/", 1)[-1]
            if t == "slideLayout":
                new = "../slideLayouts/slideLayout1.xml"
            elif t == "notesSlide":
                new = f"../notesSlides/notesSlide{n}.xml"
            elif t == "image":
                new = f"../media/img{n:03d}_{Path(target).name}"
            else:
                fail(f"page {n}: unhandled rel type {rtype}")
            return f'<Relationship Id="{rid}" Type="{rtype}" Target="{new}"/>'

        rels = RELS_RE.sub(retarget, rels)
        data[f"ppt/slides/_rels/slide{n}.xml.rels"] = rels.encode("utf-8")
        replaced[f"ppt/slides/_rels/slide{n}.xml.rels"] = md5(rels.encode("utf-8"))

        # 3. notes slide verbatim + retargeted notes rels
        data[f"ppt/notesSlides/notesSlide{n}.xml"] = z.read("ppt/notesSlides/notesSlide1.xml")
        replaced[f"ppt/notesSlides/notesSlide{n}.xml"] = md5(data[f"ppt/notesSlides/notesSlide{n}.xml"])
        nrels = z.read("ppt/notesSlides/_rels/notesSlide1.xml.rels").decode("utf-8")
        nrels = nrels.replace("../slides/slide1.xml", f"../slides/slide{n}.xml")
        data[f"ppt/notesSlides/_rels/notesSlide{n}.xml.rels"] = nrels.encode("utf-8")
        replaced[f"ppt/notesSlides/_rels/notesSlide{n}.xml.rels"] = md5(nrels.encode("utf-8"))

        # 4. media renamed per page (drop this page's old media first)
        for name in list(data):
            if re.fullmatch(rf"ppt/media/img{n:03d}_.+", name):
                removed.add(name)
                del data[name]
        new_exts = []
        for base in sorted(media_bases):
            part = f"ppt/media/img{n:03d}_{base}"
            data[part] = z.read(f"ppt/media/{base}")
            replaced[part] = md5(data[part])
            new_exts.append(Path(base).suffix.lstrip(".").lower())
        new_exts = [e for e in dict.fromkeys(new_exts) if e]

        # 5. content types for the replaced page
        ct = data["[Content_Types].xml"].decode("utf-8")
        ct = ensure_content_types(ct, n, new_exts)
        data["[Content_Types].xml"] = ct.encode("utf-8")
        replaced["[Content_Types].xml"] = md5(data["[Content_Types].xml"])

        # ledger row (render check pending until the render gate runs)
        state["pages"][str(n)] = {
            "page": n, "status": "certified",
            "source_pptx": str(src), "source_md5": src_md5,
            "render_check": "PENDING",
            "updated_at": now(),
        }
        state["events"].append({"at": now(), "action": "update-page", "page": n,
                                "source_md5": src_md5, "deck_md5_before": deck_md5_before})
        print(f"page {n:03d}: staged from {src.name} (md5 {src_md5})")

    # atomic write: temp + rename (crash never leaves a torn package)
    tmp = DECK.with_name(DECK.name + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in order:
            if name not in data:
                # data carries re-added parts under their removed names, so a
                # name pruned from data here is gone for good — skip it only
                # then, never when it was re-staged this run.
                continue
            zout.writestr(name, data[name])
        for name in data:
            if name not in order:
                zout.writestr(name, data[name])
    os.replace(tmp, DECK)

    # self-check: re-read, verify every replaced part and the part set
    with zipfile.ZipFile(DECK) as zchk:
        have = set(zchk.namelist())
        want = (set(order) - removed) | set(data)
        if have != want:
            bad_extra = sorted(have - want)
            bad_missing = sorted(want - have)
            fail(f"part set mismatch after write: extra={bad_extra} missing={bad_missing}")
        for part, want_md5 in replaced.items():
            if md5(zchk.read(part)) != want_md5:
                fail(f"part bytes changed unexpectedly: {part}")

    state["deck_md5"] = md5(DECK.read_bytes())
    if warnings:
        state.setdefault("skeleton_warnings", []).extend(warnings)
    save_ledger(state)
    print(f"deck updated atomically: pages {sorted(pages)}; md5 {deck_md5_before} -> {state['deck_md5']}")
    if warnings:
        print("WARNINGS (render gate arbitrates):")
        for w in warnings:
            print("  " + w)


def mark_render(pages: list[int], result: str, detail: str) -> None:
    state = load_ledger()
    for n in pages:
        row = state["pages"].get(str(n))
        if not row or row["status"] != "certified":
            fail(f"cannot mark render for page {n}: not a certified page in the ledger")
        row["render_check"] = result
        row["render_check_detail"] = detail
        row["render_checked_at"] = now()
    state["events"].append({"at": now(), "action": "render-check", "pages": pages,
                            "result": result, "detail": detail})
    save_ledger(state)
    print(f"ledger: render_check={result} for pages {pages}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("verify-structure")
    sub.add_parser("init-ledger")
    u = sub.add_parser("update")
    u.add_argument("pages", type=int, nargs="+", help="page numbers (slide numbers), ascending")
    m = sub.add_parser("mark-render")
    m.add_argument("pages", type=int, nargs="+")
    m.add_argument("result", choices=("PASS", "FAIL"))
    m.add_argument("detail")
    args = ap.parse_args()

    if args.cmd == "verify-structure":
        verify_structure()
    elif args.cmd == "init-ledger":
        init_ledger()
    elif args.cmd == "update":
        update_pages(sorted(set(args.pages)))
    elif args.cmd == "mark-render":
        mark_render(args.pages, args.result, args.detail)


if __name__ == "__main__":
    main()
