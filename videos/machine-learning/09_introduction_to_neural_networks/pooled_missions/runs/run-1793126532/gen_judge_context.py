#!/usr/bin/env python3
"""Deterministic judge-context generator for 09_introduction_to_neural_networks.

Builds build/judge_NNN_context.txt from the banked, validated analysis spec
(analysis/slide_NNN_final.json) plus the fresh v2 re-analysis transcript's
measured-fact lines. No LLM, no vision calls. Contexts are measured-fact anchors
for the frozen judge template - they never license content the analysis lacks.
"""
import json
import os
import re
import sys

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
BUILD = os.path.join(V, "recreated_pptx", "build")
ANALYSIS = os.path.join(V, "analysis")
REANA = os.path.join(ANALYSIS, "reanalysis_v2")

HEADER = """## SLIDE {num:03d} - CONTEXT (measured facts for the judge)

Video: `machine-learning/09_introduction_to_neural_networks`. Source frame:
`V/unique_slides/slide_{num:03d}.jpg` (960x540). Printed slide number: **{num}**.
"""


def s(v):
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False, indent=2)
    return str(v).strip()


def dedupe(vals):
    out, seen = [], set()
    for v in vals:
        k = s(v).lower()
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(s(v))
    return out


def reanalysis_facts(path, limit=26):
    """Pull measured, falsifiable lines from the v2 transcript (data only)."""
    if not os.path.isfile(path):
        return []
    keys = re.compile(
        r"(MEASURED|verbatim|exactly|printed|reads |#|px|percent|% of|centered|left|right|top|bottom)",
        re.IGNORECASE,
    )
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        t = line.strip().lstrip("-*`# ").strip()
        if len(t) < 12 or len(t) > 240:
            continue
        if t.startswith(("[", "http", "```", "END", "START")):
            continue
        if keys.search(t):
            out.append(t)
        if len(out) >= limit:
            break
    seen, uniq = set(), []
    for l in out:
        if l.lower() in seen:
            continue
        seen.add(l.lower())
        uniq.append(l)
    return uniq


def gen(num):
    spec_path = os.path.join(ANALYSIS, f"slide_{num:03d}_final.json")
    spec_path_raw = os.path.join(ANALYSIS, f"slide_{num:03d}_raw.json")
    spec = None
    for p in (spec_path, spec_path_raw):
        if os.path.isfile(p):
            try:
                spec = json.load(open(p, encoding="utf-8"))
                break
            except Exception:
                pass
    parts = [HEADER.format(num=num)]
    if not spec:
        parts.append("No banked analysis spec found; judge on visual fidelity alone.\n")
        return "".join(parts)

    parts.append(f"### Slide title (verbatim)\n\n{s(spec.get('slide_title')) or '(no title)'}\n")
    vt = spec.get("verbatim_text") or {}
    if isinstance(vt, dict):
        for key in ("bullets", "labels", "equations", "footnotes"):
            vals = vt.get(key)
            if not vals:
                continue
            parts.append(f"### Verbatim {key}\n\n")
            for item in dedupe(vals)[:40]:
                parts.append(f"- {item}\n")
            parts.append("\n")
    elif vt:
        parts.append(f"### Verbatim text\n\n{s(vt)}\n")

    layout = spec.get("layout") or {}
    if layout:
        parts.append("### Layout / regions (from validated analysis)\n\n")
        arr = layout.get("arrangement") if isinstance(layout, dict) else None
        if arr:
            parts.append(f"{s(arr)}\n\n")
        regions = layout.get("regions", []) if isinstance(layout, dict) else []
        for r in regions:
            if isinstance(r, dict):
                parts.append(
                    f"- **{s(r.get('name'))}** ({s(r.get('position'))}): {s(r.get('content'))}\n"
                )
        parts.append("\n")

    ve = spec.get("visual_elements") or spec.get("imagery") or []
    if ve:
        parts.append("### Visual elements / imagery present in the original\n\n")
        if isinstance(ve, list):
            for e in ve[:12]:
                parts.append(f"- {s(e)[:260]}\n")
        else:
            parts.append(s(ve)[:1200] + "\n")
        parts.append("\n")

    colors = spec.get("colors")
    if colors:
        parts.append(f"### Colors (approx, from analysis)\n\n```json\n{s(colors)[:600]}\n```\n")
    typo = spec.get("typography_notes")
    if typo:
        parts.append(f"### Typography notes\n\n{s(typo)}\n")
    brief = spec.get("recreation_brief")
    if brief:
        parts.append(f"### Recreation checklist (numbered brief)\n\n")
        if isinstance(brief, list):
            for i, b in enumerate(brief[:15], 1):
                parts.append(f"{i}. {s(b)[:220]}\n")
        else:
            parts.append(s(brief)[:1200] + "\n")
        parts.append("\n")

    val = spec.get("validation") or {}
    if isinstance(val, dict):
        notes = []
        for k in ("verdict", "score", "recreatability_score", "fixes", "uncertain_items"):
            if val.get(k):
                notes.append(f"- {k}: {s(val[k])[:300]}")
        if notes:
            parts.append("### Validation notes\n\n" + "\n".join(notes) + "\n")

    facts = reanalysis_facts(os.path.join(REANA, f"slide_{num:03d}_reanalysis.txt"), limit=10)
    body = "".join(parts)
    if facts and len(body) <= 7000:
        body += "\n### Fresh re-analysis measured lines (v2 transcript, DATA only)\n\n"
        for f in facts:
            body += f"- {f}\n"
    elif facts:
        body += "\n### Fresh re-analysis measured lines (v2 transcript, DATA only, first 5)\n\n"
        for f in facts[:5]:
            body += f"- {f}\n"
    body += (
        "\n### Non-content artifacts (must NOT be reported as missing)\n"
        "- Mouse cursor / video-capture chrome in the original (GROUND RULES (c)).\n"
        "- The house red frame / yellow badge / title position (GROUND RULES (a)).\n"
    )
    return body


def main():
    todo = []
    argv = sys.argv[1:]
    if not argv:
        todo = [n for n in range(1, 33)]
    else:
        for a in argv:
            if "-" in a:
                lo, hi = a.split("-", 1)
                todo += list(range(int(lo), int(hi) + 1))
            else:
                todo.append(int(a))
    for n in todo:
        out = os.path.join(BUILD, f"judge_{n:03d}_context.txt")
        if os.path.isfile(out) and os.path.getsize(out) > 2000:
            print(f"slide_{n:03d}: EXISTS skip")
            continue
        body = gen(n)
        with open(out, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"slide_{n:03d}: wrote {len(body)} bytes")


if __name__ == "__main__":
    main()
