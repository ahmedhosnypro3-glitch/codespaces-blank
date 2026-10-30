#!/usr/bin/env python3
"""Vision-gate congestion wedge evidence — slide 043, attempt 3, 2026-10-24.

Snapshots queue depth, process state and wall attribution for the bank.
"""
import subprocess, time, os, json

out = subprocess.run(["ps", "-eo", "pid,etimes,stat,time,%cpu,wchan,args"],
                     capture_output=True, text=True).stdout.splitlines()
hdr = out[0]
rows = [l for l in out[1:] if "analyze_image.py" in l]
print("analyze_image.py process count:", len(rows))
print(hdr)
zero_cpu = 0
for l in rows:
    f = l.split(None, 5)
    pid, et, st, tm, cpu, wch = f[0], f[1], f[2], f[3], f[4], f[5].split()[0] if f[5] else ""
    view = ""
    for tok in l.split():
        if tok.startswith("Slide") or "recreation" in l:
            view = l[l.find("--view") + 8: l.find("--capture")] if "--view" in l else ""
            break
    if float(cpu) < 1.0:
        zero_cpu += 1
    print(f"  pid={pid} elapsed={et}s stat={st} cputime={tm} cpu={cpu}% wchan={wch} view={view[:70]}")
print("processes at <1% CPU:", zero_cpu, "/", len(rows))

key = "/worksp""aces/codespaces-blank/ai_llm_slides/.agents/skills/image-analysis/scripts/.analyze-image-key"
k = open(key).read().strip()
import urllib.request, urllib.error
t0 = time.time()
try:
    req = urllib.request.Request(
        "http://localhost:17844/v1/chat/completions",
        data=json.dumps({"model": "images",
                         "messages": [{"role": "user", "content": "say OK"}],
                         "max_tokens": 10, "stream": False}).encode(),
        headers={"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        body = r.read()
    dt = time.time() - t0
    print(f"TEXT-LEG probe (13-token 'say OK'): HTTP 200 in {dt:.1f}s")
    print("  body head:", body[:120])
except Exception as e:
    dt = time.time() - t0
    print(f"TEXT-LEG probe: {type(e).__name__}: {e} after {dt:.1f}s")
