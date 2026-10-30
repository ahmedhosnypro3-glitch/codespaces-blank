#!/usr/bin/env python3
"""scope_a18 local analyzer: identical prompt/route to scripts/12_analyze_slides.py
but with robust JSON extraction, because script 12's extract_json() fails with
"Extra data" when the images route returns a valid JSON object followed by
trailing text. Writes the same analysis/slide_XXX_raw.json shape.

Usage: python3 _pool/a18_analyze_robust.py <NN> [more NNs...]
"""
import base64
import importlib.util
import json
import os
import sys
import time

import openai

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDES = os.path.join(VID, "unique_slides")
OUT = os.path.join(VID, "analysis")

spec = importlib.util.spec_from_file_location(
    "p12", "/home/codespace/ai_llm_slides/scripts/12_analyze_slides.py")
p12 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p12)
ANALYSIS_PROMPT = p12.ANALYSIS_PROMPT

key_file = "/home/codespace/ai_llm_slides/.analyze-image-key"
api_key = os.environ.get("IR_API_KEY") or open(key_file).read().strip()
base_url = os.environ.get("IR_BASE_URL", "http://localhost:17844/v1")
client = openai.OpenAI(base_url=base_url, api_key=api_key)


def extract_robust(text):
    """Return (obj, how). Handles prose, fences, and trailing junk after JSON."""
    dec = json.JSONDecoder()
    t = text.strip()
    cands = []
    for m_start in [m.start() for m in __import__("re").finditer(r"\{", t)]:
        try:
            obj, _ = dec.raw_decode(t[m_start:])
            cands.append((obj, f"raw_decode at {m_start}"))
        except ValueError:
            continue
    if not cands:
        raise ValueError("no JSON object found")
    # prefer the largest (most complete) object
    best = max(cands, key=lambda c: len(json.dumps(c[0])))
    return best


def run(n):
    fname = f"slide_{n:03d}.jpg"
    out_file = os.path.join(OUT, fname.replace(".jpg", "_raw.json"))
    if os.path.exists(out_file):
        print(f"{fname}: already analyzed, skipping")
        return True
    with open(os.path.join(SLIDES, fname), "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    print(f"{fname}: analyzing with images ...", flush=True)
    t0 = time.time()
    try:
        resp = client.chat.completions.create(
            model=os.environ.get("IR_VISION_MODEL", "images"),
            messages=[{"role": "user", "content": [
                {"type": "text", "text": ANALYSIS_PROMPT},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ]}],
            max_tokens=os.environ.get("IR_MAX_TOKENS", 16000),
            temperature=0.1,
            stream=True,
        )
        parts, finish = [], None
        for chunk in resp:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                parts.append(chunk.choices[0].delta.content)
            if chunk.choices and chunk.choices[0].finish_reason:
                finish = chunk.choices[0].finish_reason
        raw_text = "".join(parts)
        parsed, how = extract_robust(raw_text)
        parsed["_meta"] = {"frame": fname, "model": "images",
                           "elapsed_s": round(time.time() - t0, 1)}
        with open(out_file, "w") as f:
            json.dump(parsed, f, indent=2)
        print(f"  -> {out_file} ({time.time()-t0:.0f}s, finish={finish}, parse={how}, "
              f"raw_len={len(raw_text)})")
        return True
    except Exception as e:
        print(f"  FAILED: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    ok = True
    for a in sys.argv[1:]:
        ok = run(int(a)) and ok
    sys.exit(0 if ok else 1)
