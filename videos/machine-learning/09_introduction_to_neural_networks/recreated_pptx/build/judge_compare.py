#!/usr/bin/env python3
"""Compare original slide frame vs recreated render via the local vision gateway."""
import base64
import json
import os
import sys
import time

from openai import OpenAI

BASE_URL = os.environ.get("IR_BASE_URL", "http://localhost:17844/v1")
KEY_FILE = "/home/codespace/ai_llm_slides/.analyze-image-key"


def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def main():
    slide = sys.argv[1]
    orig = sys.argv[2]
    rec = sys.argv[3]
    out = sys.argv[4]
    client = OpenAI(base_url=BASE_URL, api_key=open(KEY_FILE).read().strip())

    prompt = open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/judge_template.txt").read() + "\n\n" + open(out.replace(".txt", "_prompt.txt")).read()

    t0 = time.time()
    resp = client.chat.completions.create(
        model="images",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + img_b64(orig)}},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + img_b64(rec)}},
        ]}],
        max_tokens=8000,
        stream=True,
    )
    parts = []
    for chunk in resp:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            parts.append(chunk.choices[0].delta.content)
    text = "".join(parts)
    with open(out, "w") as f:
        f.write(text)
    print(f"wrote {out} ({len(text)} chars, {time.time()-t0:.0f}s)")
    print(text[-1500:])


if __name__ == "__main__":
    main()
