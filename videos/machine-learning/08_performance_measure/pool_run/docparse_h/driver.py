#!/usr/bin/env python3
"""Doc-parse lane H driver: slides 29-37 of 08_performance_measure.

Max 2 concurrent parse calls, 60-90s dispatch spacing, up to 6 attempts
per slide with 120-300s sleeps between attempts. A call counts as failed
when finish_reason != stop or content is empty. Logs to run.log.
"""
import json
import random
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
OUT = NS / "pool_run/docparse_h"
LOG = OUT / "run.log"
SCRIPT = str(Path.home() / ".agents/skills/doc-parse/scripts/parse_document.py")
SLIDES = list(range(29, 38))
MAX_CONCURRENT = 2
MAX_ATTEMPTS = 6

log_lock = threading.Lock()


def log(msg):
    line = f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] {msg}"
    with log_lock:
        with LOG.open("a") as f:
            f.write(line + "\n")
    print(line, flush=True)


def attempt(slide, attempt_no):
    img = NS / "unique_slides" / f"slide_{slide:03d}.jpg"
    outdir = OUT / f"slide{slide}"
    outdir.mkdir(parents=True, exist_ok=True)
    log(f"slide {slide} attempt {attempt_no}/{MAX_ATTEMPTS} dispatch")
    t0 = time.time()
    proc = subprocess.run(
        [sys.executable, SCRIPT, str(img), "-o", str(outdir), "--timeout", "300"],
        capture_output=True, text=True,
    )
    dt = time.time() - t0
    pj = outdir / f"{img.stem}.parse.json"
    ok = False
    reason = ""
    clen = 0
    if pj.exists():
        try:
            data = json.loads(pj.read_text())
            fr = data.get("finish_reason")
            content = data.get("content") or ""
            clen = len(content)
            reason = fr
            ok = (fr == "stop" and clen > 0)
        except Exception as e:
            reason = f"json-error: {e}"
    else:
        reason = f"no-json exit={proc.returncode} stderr={proc.stderr.strip()[:200]}"
    log(f"slide {slide} attempt {attempt_no} done in {dt:.0f}s finish_reason={reason} content_len={clen} ok={ok}")
    return ok, clen


def run_slide(slide):
    for a in range(1, MAX_ATTEMPTS + 1):
        ok, clen = attempt(slide, a)
        if ok:
            log(f"slide {slide} SUCCESS on attempt {a} (content_len={clen})")
            return True
        if a < MAX_ATTEMPTS:
            sleep_s = random.uniform(120, 300)
            log(f"slide {slide} attempt {a} FAILED, sleeping {sleep_s:.0f}s before retry")
            time.sleep(sleep_s)
    log(f"slide {slide} EXHAUSTED {MAX_ATTEMPTS} attempts")
    return False


def main():
    log("== lane H driver start: slides 29-37, max 2 concurrent, 60-90s dispatch spacing ==")
    results = {}
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as pool:
        futures = {}
        for slide in SLIDES:
            # dispatch spacing: wait before submitting next task
            if futures:
                spacing = random.uniform(60, 90)
                log(f"dispatch spacing {spacing:.0f}s before slide {slide}")
                time.sleep(spacing)
            fut = pool.submit(run_slide, slide)
            futures[fut] = slide
        for fut in futures:
            results[futures[fut]] = fut.result()
    log("== driver summary ==")
    for slide in SLIDES:
        pj = OUT / f"slide{slide}" / f"slide_{slide:03d}.parse.json"
        status = "OK" if results.get(slide) else "FAILED"
        fr, clen = "-", 0
        if pj.exists():
            try:
                d = json.loads(pj.read_text())
                fr = d.get("finish_reason")
                clen = len(d.get("content") or "")
            except Exception:
                fr = "json-error"
        log(f"RESULT slide={slide} finish_reason={fr} content_len={clen} status={status}")
    log("== lane H driver end ==")


if __name__ == "__main__":
    main()
