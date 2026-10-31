#!/usr/bin/env python3
"""Check docparse_i slide dirs: finish_reason=stop and non-empty content."""
import json, os, sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
OUT = os.path.join(NS, "pool_run/docparse_i")

for n in range(10, 20):
    stem = f"slide_{n:03d}"
    # find newest attempt dir containing a parse.json for this slide
    candidates = [f"slide{n:03d}", f"slide{n}"]
    candidates += sorted(
        (d for d in os.listdir(OUT) if d.startswith(f"slide{n:03d}_retry") or d.startswith(f"slide{n}_retry")),
        key=lambda d: int(d.rsplit("retry", 1)[1]),
    )
    status = "MISSING"
    detail = ""
    for d in candidates:
        p = os.path.join(OUT, d, f"{stem}.parse.json")
        if os.path.exists(p):
            try:
                data = json.load(open(p))
            except Exception as e:
                status = "UNREADABLE_JSON"
                detail = f"{d}: {e}"
                continue
            fr = data.get("finish_reason")
            content = data.get("content") or ""
            toks = (data.get("usage") or {}).get("output_tokens")
            if fr == "stop" and content.strip():
                status = "OK"
                detail = f"{d}: finish={fr} chars={len(content)} out_tokens={toks}"
            else:
                status = "FAILED"
                detail = f"{d}: finish={fr} chars={len(content)} out_tokens={toks}"
            break
    print(f"{stem}: {status} | {detail}")
