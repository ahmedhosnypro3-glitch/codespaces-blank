#!/usr/bin/env python3
# Judge slides: image 1 = ORIGINAL frame, image 2 = recreation render. Banked transcripts.
import hashlib, json, os, re, subprocess, sys, time

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ANALYZE = "/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE = "/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh"
OUTDIR = os.path.join(BASE, "qa", "rejudge2")
LEDGER = os.path.join(OUTDIR, "ledger.jsonl")
os.makedirs(OUTDIR, exist_ok=True)
BASE_RULES = open(os.path.join(BASE, "judge_prompt_active.txt")).read().strip()
PARALLEL = int(os.environ.get("JUDGE_PARALLEL", "1"))
ATTEMPTS = int(os.environ.get("JUDGE_ATTEMPTS", "3"))
WALL = int(os.environ.get("JUDGE_WALL", "2400"))
HTTP_TIMEOUT = int(os.environ.get("JUDGE_HTTP_TIMEOUT", "420"))

CONTEXT = """VIEW: Slide {ss} — original lecture frame vs its PowerPoint recreation (SVM/kernels/QP lecture)
FACTS: the printed slide number is {num}. House chrome is MANDATORY in [2] and never a discrepancy.
Images are attached in this order: image 1 = ORIGINAL, image 2 = RECREATION.
List every discrepancy as: SEVERITY (BLOCKER|MAJOR|MINOR) — element — defect — confidence.
End with exactly one terminal line: FINAL VERDICT: PASS   or   FINAL VERDICT: FAIL
"""

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()

def ledger_rows():
    if not os.path.exists(LEDGER):
        return {}
    rows = {}
    for line in open(LEDGER):
        line = line.strip()
        if line:
            r = json.loads(line)
            rows[r["slide"]] = r
    return rows

def bank(row):
    with open(LEDGER, "a") as f:
        f.write(json.dumps(row) + "\n")

def verdict_of(path):
    if not os.path.exists(path):
        return "NO_TRANSCRIPT"
    for line in reversed(open(path, errors="replace").read().splitlines()):
        m = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", line, re.I)
        if m:
            return m.group(1).upper()
    return "INVALID_NO_VERDICT_LINE"

def needs_retry(tail):
    return any(k in tail for k in ("HangError", "hard wall-clock", "GarbageError", "abort+retry"))

def run(num, attempts=None):
    if attempts is None:
        attempts = ATTEMPTS
    ss = f"{num:03d}"
    paths = {"pptx": os.path.join(BASE, "recreated_pptx", f"slide_{ss}_recreated.pptx"),
             "orig": os.path.join(BASE, "unique_slides", f"slide_{ss}.jpg"),
             "render": os.path.join(BASE, "recreated_pptx", "renders", f"slide_{ss}_recreated-1.png")}
    for tag, p in paths.items():
        if not os.path.exists(p):
            bank({"slide": ss, "verdict": f"MISSING_{tag}", "note": p})
            print(f"[{ss}] MISSING {tag}: {p}", flush=True)
            return
    m = md5(paths["pptx"])
    prior = ledger_rows().get(ss)
    if prior and prior.get("pptx_md5") == m and prior.get("verdict") in ("PASS", "FAIL"):
        print(f"[{ss}] already {prior['verdict']} at this md5 — skip", flush=True)
        return
    prompt = CONTEXT.format(ss=ss, num=num) + "\n" + BASE_RULES
    for attempt in range(1, attempts + 1):
        stamp = time.strftime("%F %T")
        procs = []
        for k in range(PARALLEL):
            out_k = os.path.join(OUTDIR, f"slide_{ss}_judge_a{attempt}_{k}.txt")
            cmd = ["timeout", str(WALL), GATE, "python3", ANALYZE, "comparison",
                   paths["orig"], paths["render"], "-p", prompt,
                   "--timeout", str(HTTP_TIMEOUT), "--rounds", "1", "--tries", "1",
                   "--max-tokens", "32000", "--transcript", out_k]
            procs.append((out_k, cmd,
                          subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT, text=True)))
        for pi, (out_k, _cmd, proc) in enumerate(procs):
            try:
                tail = proc.communicate(timeout=WALL + 120)[0]
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
                tail = f"DRIVER_TIMEOUT after {WALL + 120}s"
            with open(os.path.join(OUTDIR, f"slide_{ss}_attempt{attempt}_{pi}.log"), "w") as f:
                f.write(tail)
            row = {"slide": ss, "attempt": attempt, "ts": stamp, "pptx_md5": m}
            if "DRIVER_TIMEOUT" in tail or tail.strip() == "TIMEOUT":
                row.update(verdict="WALL_TIMEOUT")
                bank(row)
                print(f"[{ss}] WALL_TIMEOUT (attempt {attempt})", flush=True)
                continue
            v = verdict_of(out_k)
            row.update(verdict=v, transcript=out_k)
            bank(row)
            print(f"[{ss}] {v} (attempt {attempt})", flush=True)
            if v in ("PASS", "FAIL"):
                return
            if not needs_retry(tail) and v not in ("INVALID_NO_VERDICT_LINE", "NO_TRANSCRIPT"):
                return
        if not procs:
            return
    bank({"slide": ss, "verdict": "UNRESOLVED", "ts": time.strftime("%F %T"), "pptx_md5": m})

if __name__ == "__main__":
    for n in [int(x) for x in sys.argv[1:]]:
        try:
            run(n)
        except Exception as e:
            print(f"[{n}] EXC {e}", flush=True)
