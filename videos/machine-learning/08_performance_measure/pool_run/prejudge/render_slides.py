#!/usr/bin/env python3
"""Render slide pptx files to 150dpi PNGs into pool_run/prejudge/slideNNN/.

Uses a project-scratch LibreOffice profile (never /tmp).
"""
import hashlib
import json
import os
import subprocess
import sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
PPTX_DIR = os.path.join(NS, "recreated_pptx")
PRE = os.path.join(NS, "pool_run", "prejudge")
PROFILE = os.path.join(NS, "scratch", "lo_prejudge")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render(slide):
    pptx = os.path.join(PPTX_DIR, f"slide_{slide:03d}_recreated.pptx")
    if not os.path.exists(pptx):
        return None
    outdir = os.path.join(PRE, f"slide_{slide:03d}")
    os.makedirs(outdir, exist_ok=True)
    subprocess.run(
        ["soffice", "--headless",
         f"-env:UserInstallation=file://{PROFILE}",
         "--convert-to", "pdf", "--outdir", outdir, pptx],
        check=True, capture_output=True, timeout=420)
    pdf = os.path.join(outdir, f"slide_{slide:03d}_recreated.pdf")
    stem = os.path.join(outdir, "render")
    subprocess.run(["pdftoppm", "-png", "-r", "150", pdf, stem],
                   check=True, timeout=300)
    png = os.path.join(outdir, "render-1.png")
    size = os.path.getsize(png)
    return {
        "pptx": pptx,
        "pptx_md5": md5(pptx),
        "pptx_mtime": os.path.getmtime(pptx),
        "build_mtime": build_mtime(slide),
        "pdf": pdf,
        "png": png,
        "png_bytes": size,
    }


def build_mtime(slide):
    p = os.path.join(PPTX_DIR, "build", f"slide_{slide:03d}.js")
    return os.path.getmtime(p) if os.path.exists(p) else None


def main():
    slides = [int(a) for a in sys.argv[1:]] or [1, 5, 10, 11, 15, 17]
    for slide in slides:
        info = render(slide)
        if info is None:
            print(f"slide {slide:03d}: NO PPTX (build pending)")
            continue
        meta = os.path.join(PRE, f"slide_{slide:03d}", "render_meta.json")
        with open(meta, "w") as f:
            json.dump(info, f, indent=2)
        print(f"slide {slide:03d}: {info['png']} {info['png_bytes']}B md5={info['pptx_md5'][:8]}")


if __name__ == "__main__":
    main()
