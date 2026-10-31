import glob, json, os, random, subprocess, sys, threading, time

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
OUT = os.path.join(NS, "pool_run/docparse_g")
SCRIPT = os.path.expanduser("~/.agents/skills/doc-parse/scripts/parse_document.py")
LOG = open(os.path.join(OUT, "run.log"), "a", buffering=1)

def log(msg):
    LOG.write(f"{time.strftime('%H:%M:%S')} {msg}\n")

def check_ok(outdir):
    for j in glob.glob(os.path.join(outdir, "*.parse.json")):
        try:
            d = json.load(open(j))
        except Exception:
            return False
        if d.get("finish_reason") == "stop" and (d.get("content") or "").strip():
            return True
    return False

def run_slide(nn):
    inp = glob.glob(os.path.join(NS, "unique_slides", f"slide_0{nn:02d}*.jpg"))
    assert inp, f"no input for slide {nn}"
    inp = sorted(inp)[0]
    outdir = os.path.join(OUT, f"slide{nn}")
    os.makedirs(outdir, exist_ok=True)
    for attempt in range(1, 7):
        log(f"slide{nn} attempt {attempt} start input={os.path.basename(inp)} outdir={outdir}")
        t0 = time.time()
        p = subprocess.run([sys.executable, SCRIPT, inp, "-o", outdir, "--timeout", "300"],
                           capture_output=True, text=True)
        dt = time.time() - t0
        tail = (p.stderr or "").strip().splitlines()[-3:]
        log(f"slide{nn} attempt {attempt} rc={p.returncode} {dt:.1f}s stderr_tail={tail}")
        if check_ok(outdir):
            log(f"slide{nn} OK after {attempt} attempt(s)")
            return True
        if attempt < 6:
            s = 120 + random.randint(0, 180)
            log(f"slide{nn} attempt {attempt} incomplete, sleeping {s}s before retry")
            time.sleep(s)
    log(f"slide{nn} FAILED after 6 attempts")
    return False

sem = threading.Semaphore(2)
threads = []
for nn in range(20, 29):
    # dispatch spacing: 60-90s between launches
    if nn > 20:
        time.sleep(random.randint(60, 90))
    def work(nn=nn):
        with sem:
            run_slide(nn)
    t = threading.Thread(target=work)
    t.start()
    threads.append(t)
    log(f"dispatched slide{nn}")

for t in threads:
    t.join()
log("lane G complete")
