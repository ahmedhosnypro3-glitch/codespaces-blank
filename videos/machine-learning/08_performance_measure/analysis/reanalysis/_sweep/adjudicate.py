#!/usr/bin/env python3
"""adjudicate.py — focused vision read of one cropped region of a slide frame.

Used by the re-analysis sweep to settle numeric/text disputes between two
independent vision reads: crop -> 3x upscale -> one focused transcription call
through the shared vision gateway.

Usage:
  adjudicate.py <frame.jpg> <x0> <y0> <x1> <y1> <question> <out.json> [scale]
"""
import base64
import json
import os
import sys

import openai
from PIL import Image

BASE_URL = os.environ.get("IR_BASE_URL", "http://localhost:17844/v1")
API_KEY = os.environ.get("IR_API_KEY")
if not API_KEY:
    key_file = "/home/codespace/ai_llm_slides/.analyze-image-key"
    if os.path.exists(key_file):
        API_KEY = open(key_file).read().strip()
if not API_KEY:
    sys.exit("IR_API_KEY env var required (or .analyze-image-key in the project root)")


def main():
    frame, x0, y0, x1, y1, question, out_path = sys.argv[1:8]
    scale = float(sys.argv[8]) if len(sys.argv) > 8 else 3.0
    x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    im = Image.open(frame).convert("RGB").crop((x0, y0, x1, y1))
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    tmp = out_path + ".crop.png"
    im.save(tmp)
    b64 = base64.b64encode(open(tmp, "rb").read()).decode()

    prompt = (
        "You are reading a CROP of a lecture slide, upscaled for legibility. "
        "Transcribe EXACTLY what is written, character for character, including every digit, "
        "percent sign, plus sign, parenthesis and equals sign. Do not paraphrase, do not correct, "
        "do not guess. If a character is genuinely unreadable, mark it [?]. "
        "Answer with JSON: {\"lines\": [{\"text\": \"<line as written>\"}], \"notes\": \"<what is "
        "unreadable, if anything>\"}. " + question
    )

    client = openai.OpenAI(base_url=BASE_URL, api_key=API_KEY)
    resp = client.chat.completions.create(
        model=os.environ.get("IR_VISION_MODEL", "images"),
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
        ]}],
        max_tokens=4000,
        temperature=0.1,
        stream=True,
    )
    parts, finish = [], None
    for chunk in resp:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            parts.append(chunk.choices[0].delta.content)
        if chunk.choices and chunk.choices[0].finish_reason:
            finish = chunk.choices[0].finish_reason
    raw = "".join(parts).strip()
    start, end = raw.find("{"), raw.rfind("}")
    parsed = json.loads(raw[start:end + 1]) if start != -1 and end > start else {"lines": [], "notes": "PARSE FAIL: " + raw[:500]}
    parsed["_meta"] = {"frame": frame, "crop": [x0, y0, x1, y1], "scale": scale,
                       "finish": finish, "question": question}
    with open(out_path, "w") as f:
        json.dump(parsed, f, indent=2)
    print(f"finish={finish} -> {out_path}")
    print(json.dumps(parsed, indent=2)[:2000])


if __name__ == "__main__":
    main()
