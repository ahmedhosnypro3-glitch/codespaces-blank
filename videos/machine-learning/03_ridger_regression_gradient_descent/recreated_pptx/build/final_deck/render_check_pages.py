#!/usr/bin/env python3
"""Per-update render gate for the continuous final deck — deck 03.

Renders the final deck AND the updated pages' source pptx in ONE LibreOffice
session (deterministic LO renders; the S14 merge gate's methodology), rasterizes
the affected pages at 150dpi, and PIL-diffs page N vs source N. 0 differing
pixels required. Marks PASS/FAIL per page in final_deck_state.json.

usage: render_check_pages.py <page> [<page> ...]   (ascending)
exit 0 = all checked pages identical; exit 1 = any mismatch (stop-and-fix law).
"""

import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import final_deck_tool as T  # noqa: E402

TOTAL = T.TOTAL
GATE_ROOT = T.PPTX_DIR / "qa" / "final_deck_updates"
TMPDIR = Path("/home/codespace/ai_llm_slides/scratch/tmp")
LO_PROFILE = TMPDIR / "s21_lo_profile_299640"


def sh(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def lo_convert(profile: Path, outdir: Path, src: Path) -> Path:
    out = outdir / (src.stem + ".pdf")
    if out.exists():
        out.unlink()
    sh(["soffice", "--headless", f"-env:UserInstallation=file://{profile}",
        "--convert-to", "pdf", "--outdir", str(outdir), str(src)])
    if not out.is_file():
        T.fail(f"LibreOffice produced no PDF for {src}")
    return out


def main() -> None:
    pages = sorted(set(int(a) for a in sys.argv[1:]))
    if not pages:
        T.fail("usage: render_check_pages.py <page> [<page> ...]")
    for n in pages:
        row = T.load_ledger()["pages"].get(str(n))
        if not row or row["status"] != "certified":
            T.fail(f"page {n} is not a certified page in the ledger")

    if LO_PROFILE.exists():
        lock = LO_PROFILE / ".lock"
        if lock.exists():
            shutil.rmtree(LO_PROFILE)

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    gate = GATE_ROOT / f"gate_{stamp}_p{'-'.join(str(n) for n in pages)}"
    (gate / "pages").mkdir(parents=True)
    (gate / "src_png").mkdir()
    (gate / "src").mkdir()

    old = os.environ.get("TMPDIR")
    os.environ["TMPDIR"] = str(TMPDIR)
    TMPDIR.mkdir(parents=True, exist_ok=True)
    try:
        deck_pdf = lo_convert(LO_PROFILE, gate, T.DECK)
        pdfinfo = subprocess.run(["pdfinfo", str(deck_pdf)], capture_output=True, text=True, check=True).stdout
        npages = int([l for l in pdfinfo.splitlines() if l.startswith("Pages:")][0].split()[1])
        if npages != TOTAL:
            T.fail(f"deck PDF has {npages} pages, expected {TOTAL} (page-count law)")

        for n in pages:
            src = T.PPTX_DIR / f"slide_{n:03d}_recreated.pptx"
            src_pdf = lo_convert(LO_PROFILE, gate / "src", src)
            sh(["pdftoppm", "-png", "-r", "150", "-f", str(n), "-l", str(n),
                str(deck_pdf), str(gate / "pages" / f"pg{n:03d}")])
            sh(["pdftoppm", "-png", "-r", "150", "-f", "1", "-l", "1",
                str(src_pdf), str(gate / "src_png" / f"s{n:03d}")])

        from PIL import Image, ImageChops
        report = []
        bad = []
        for n in pages:
            a = sorted((gate / "pages").glob(f"pg{n:03d}-*.png"))
            b = sorted((gate / "src_png").glob(f"s{n:03d}-*.png"))
            if not a or not b:
                T.fail(f"rasterization missing for page {n}")
            ia = Image.open(a[0]).convert("RGB")
            ib = Image.open(b[0]).convert("RGB")
            if ia.size != ib.size:
                bad.append(n)
                report.append(f"page {n:03d}: FAIL (size {ia.size} vs {ib.size})")
                continue
            diff = ImageChops.difference(ia, ib).getbbox()
            if diff:
                bad.append(n)
                report.append(f"page {n:03d}: FAIL (diff bbox {diff})")
            else:
                report.append(f"page {n:03d}: PASS (0 px differ vs fresh 150dpi source render, same LO session)")
    finally:
        if old is not None:
            os.environ["TMPDIR"] = old

    (gate / "gate_report.txt").write_text(
        "render gate — continuous final deck update\n"
        f"deck: {T.DECK}\npages: {pages}\n" + "\n".join(report) + "\n")
    print("\n".join(report))

    if bad:
        T.mark_render(pages, "FAIL", f"mismatched pages {bad}; report {gate / 'gate_report.txt'}")
        sys.exit(f"RENDER GATE FAILED for pages {bad} — stop, fix the update path, redo the page(s)")

    T.mark_render(pages, "PASS",
                  f"0 px differ vs fresh 150dpi source renders (one LO session); report {gate / 'gate_report.txt'}")
    print(f"render gate PASSED for pages {pages}; artifacts {gate}")


if __name__ == "__main__":
    main()
