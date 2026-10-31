#!/usr/bin/env python3
"""READ-ONLY replica of build/final_deck/render_check_pages.py for deck 03.

Differences from the original (read-only mandate):
- never imports final_deck_tool, never calls mark_render, never touches
  final_deck_state.json / the deck / the DB;
- writes only under this script's directory ($RJ/rendercheck_r2/);
- uses a PRIVATE LibreOffice profile (lo_profile/) instead of the shared
  scratch/tmp/s21_lo_profile_299640, so concurrent workers are unaffected.

Method identical to the gate: one LO profile session, deck -> PDF, source
slide -> PDF, pdftoppm 150dpi, PIL diff (0 px required for PASS).
Additionally quantifies diff% and compares against the banked per-slide
renders in $RJ/slideNNN/render.png (scaled) as a package-context control.
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops

RJ = Path(__file__).resolve().parent
NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent")
PPTX_DIR = NS / "recreated_pptx"
DECK = PPTX_DIR / "03_ridger_regression_gradient_descent_final.pptx"
REJUDGE = PPTX_DIR / "qa" / "rejudge_20261027"
PROFILE = RJ / "lo_profile"
PAGES = [1, 2, 3, 7, 25, 30, 40, 51]
TOTAL = 51
DPI = 150


def sh(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def lo_convert(outdir: Path, src: Path) -> Path:
    out = outdir / (src.stem + ".pdf")
    if out.exists():
        out.unlink()
    sh(["soffice", "--headless", f"-env:UserInstallation=file://{PROFILE}",
        "--convert-to", "pdf", "--outdir", str(outdir), str(src)])
    if not out.is_file():
        sys.exit(f"FATAL: no PDF for {src}")
    return out


def metrics(ia: Image.Image, ib: Image.Image) -> dict:
    a, b = ia.convert("RGB"), ib.convert("RGB")
    if a.size != b.size:
        return {"size_a": list(a.size), "size_b": list(b.size), "size_match": False}
    d = ImageChops.difference(a, b)
    bbox = d.getbbox()
    hist_total = a.size[0] * a.size[1]
    px = d.tobytes()
    n_diff = 0
    n_gt16 = 0
    sum_abs = 0
    for i in range(0, len(px), 3):
        m = max(px[i], px[i + 1], px[i + 2])
        if m:
            n_diff += 1
            sum_abs += px[i] + px[i + 1] + px[i + 2]
            if m > 16:
                n_gt16 += 1
    return {
        "size_a": list(a.size), "size_b": list(b.size), "size_match": True,
        "bbox": list(bbox) if bbox else None,
        "n_diff_px": n_diff, "n_diff_gt16": n_gt16,
        "diff_pct": round(100.0 * n_diff / hist_total, 4),
        "diff_gt16_pct": round(100.0 * n_gt16 / hist_total, 4),
        "mean_abs_per_channel": round(sum_abs / (3.0 * hist_total), 4),
    }


def main():
    (RJ / "pages").mkdir(exist_ok=True)
    (RJ / "src").mkdir(exist_ok=True)
    (RJ / "src_png").mkdir(exist_ok=True)

    deck_pdf = lo_convert(RJ, DECK)
    info = subprocess.run(["pdfinfo", str(deck_pdf)], capture_output=True, text=True, check=True).stdout
    npages = int([l for l in info.splitlines() if l.startswith("Pages:")][0].split()[1])
    if npages != TOTAL:
        sys.exit(f"FATAL: deck PDF has {npages} pages, expected {TOTAL}")

    results = {}
    for n in PAGES:
        src = PPTX_DIR / f"slide_{n:03d}_recreated.pptx"
        src_pdf = lo_convert(RJ / "src", src)
        sh(["pdftoppm", "-png", "-r", str(DPI), "-f", str(n), "-l", str(n),
            str(deck_pdf), str(RJ / "pages" / f"pg{n:03d}")])
        sh(["pdftoppm", "-png", "-r", str(DPI), "-f", "1", "-l", "1",
            str(src_pdf), str(RJ / "src_png" / f"s{n:03d}")])

        pa = sorted((RJ / "pages").glob(f"pg{n:03d}-*.png"))[0]
        sb = sorted((RJ / "src_png").glob(f"s{n:03d}-*.png"))[0]
        ia, ib = Image.open(pa), Image.open(sb)
        gate = metrics(ia, ib)
        gate["verdict"] = "PASS" if gate.get("size_match") and gate["n_diff_px"] == 0 else "FAIL"

        # control: banked per-slide render from the rejudge wave, scaled to the fresh render
        banked = REJUDGE / f"slide{n:03d}" / "render.png"
        banked_m = None
        if banked.is_file():
            bb = Image.open(banked).convert("RGB").resize(ib.size, Image.LANCZOS)
            banked_m = {"deck_vs_banked": metrics(ia, bb), "src_vs_banked": metrics(ib, bb)}

        results[n] = {"page_png": str(pa), "src_png": str(sb), "gate": gate, "banked": banked_m}
        print(f"page {n:03d}: gate={gate['verdict']} diff%={gate.get('diff_pct')} "
              f"gt16%={gate.get('diff_gt16_pct')} bbox={gate.get('bbox')}")

    (RJ / "metrics.json").write_text(json.dumps({"deck_pdf_pages": npages, "dpi": DPI,
                                                 "pages": {str(k): v for k, v in results.items()}}, indent=2) + "\n")
    lines = [f"read-only render check r2 — deck {DECK.name} (deck PDF pages={npages}, {DPI}dpi, one private LO profile)"]
    for n, r in results.items():
        g = r["gate"]
        lines.append(f"page {n:03d}: {g['verdict']} diff%={g.get('diff_pct')} gt16%={g.get('diff_gt16_pct')} "
                     f"bbox={g.get('bbox')} meanabs={g.get('mean_abs_per_channel')}")
    (RJ / "gate_report.txt").write_text("\n".join(lines) + "\n")
    print("wrote", RJ / "gate_report.txt")


if __name__ == "__main__":
    main()
