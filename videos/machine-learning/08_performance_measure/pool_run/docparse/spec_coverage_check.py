#!/usr/bin/env python3
"""spec_coverage_check.py — doc-parse <-> vision-spec cross-check for the
08_performance_measure deck.

The doc-parse lane reads the ORIGINAL frames with a different model family
(different prompt surface, different output form) than the vision analysis
lane. That makes it a genuine DIFFERENT-FORM read — the corroboration the
visual-judge law asks for. This script compares each slide's composed parse
transcript against the consumed vision spec and reports text the spec does
not account for (a potential missing-content defect for the build worker).

Read-only over specs and transcripts; writes one register.
"""
import json
import pathlib
import re
import sys

NS = pathlib.Path("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
DP = NS / "pool_run/docparse"
OUT = NS / "pool_run/docparse/spec_coverage.md"

CLASS_TOKEN = re.compile(r"<class_[^>]+>")
COORD = re.compile(r"\(x=[\d.]+, ?y=[\d.]+, ?w=[\d.]+, ?h=[\d.]+\)")
PROVENANCE = re.compile(r"—\s*from\s+\S+\.parse\.md.*$", re.M)
MARKUP = re.compile(r"[*_`#>|\[\]()=+~^]")
WORD = re.compile(r"[A-Za-z][A-Za-z0-9\-']{2,}")

# Only the content sections carry parsed slide content; the rest is cascade bookkeeping.
CONTENT_SECTIONS = ("## Positioned elements", "## Unpositioned text")


def content_only(text: str) -> str:
    kept, keep, in_picture = [], False, False
    for ln in text.splitlines():
        if ln.startswith("## "):
            keep = ln.strip().startswith(CONTENT_SECTIONS)
            in_picture = False
            continue
        if not keep or ln.startswith("#"):
            continue
        # Text OCR'd out of a <class_Picture> region is unreliable (the parser
        # garbles logos); it must not be reported as missing slide content.
        if "<class_Picture>" in ln:
            in_picture = True
            continue
        if in_picture:
            if ln.startswith("- ") or ln.startswith("  "):
                continue
            in_picture = False
        kept.append(ln)
    return "\n".join(kept)


def parse_tokens(text: str) -> set[str]:
    text = content_only(text)
    text = PROVENANCE.sub(" ", text)
    text = CLASS_TOKEN.sub(" ", text)
    text = COORD.sub(" ", text)
    text = MARKUP.sub(" ", text)
    return {w.lower() for w in WORD.findall(text)}


def spec_text(spec: dict) -> str:
    parts: list[str] = []
    vt = spec.get("verbatim_text") or {}
    for key in ("bullets", "labels", "equations"):
        parts.extend(str(x) for x in (vt.get(key) or []))
    parts.append(str(spec.get("slide_title") or ""))
    parts.append(str((spec.get("layout") or {}).get("arrangement") or ""))
    for el in spec.get("visual_elements") or []:
        parts.append(str(el.get("description") or ""))
        parts.append(str(el.get("type") or ""))
    parts.extend(str(x) for x in (spec.get("imagery") or []))
    parts.extend(str(x) for x in (spec.get("recreation_brief") or []))
    return "\n".join(parts)


def norm_words(s: str) -> set[str]:
    return {w.lower() for w in WORD.findall(MARKUP.sub(" ", s))}


# Words the parser emits as structural/formatting metadata, not slide content.
NOISE_WORDS = {
    "none", "chart", "type", "begin", "end", "multicolumn", "multirow", "tabular",
    "thead", "mbox", "ranked", "lollipop", "bind", "column", "cccc", "figure",
    "table", "header", "caption", "level", "initial", "text", "class", "slide",
    "source", "frame", "crops", "crop", "full", "parse", "chat", "degraded",
    "composed", "elements", "calls", "failed", "fallback", "retries", "dedup",
    "collapsed", "notes", "reading", "order", "positioned", "unpositioned",
    "backstop", "kept", "spent", "stops", "deterministic", "conservative",
    "picture", "then", "from", "with", "true", "false",
}


def main() -> None:
    rows, findings = [], []
    for n in range(1, 38):
        padded = f"{n:03d}"
        comp = sorted((DP / f"slide{padded}").glob("composed/*_composed.md"))
        spec_path = NS / f"analysis/slide_{padded}_final.json"
        spec_path_r = NS / f"analysis/slide_{padded}_raw.json"
        if not comp:
            rows.append((padded, "NO-COMPOSED", "-", "-")); continue
        parse_words = parse_tokens(comp[0].read_text(encoding="utf-8", errors="replace"))
        if not parse_words:
            rows.append((padded, "EMPTY-PARSE", "-", "-")); continue
        if not spec_path.exists() and not spec_path_r.exists():
            rows.append((padded, "NO-SPEC", "-", str(len(parse_words)))); continue
        spec = json.load(open(spec_path if spec_path.exists() else spec_path_r))
        spec_words = norm_words(spec_text(spec))
        missing = sorted(w for w in parse_words - spec_words
                         if len(w) >= 4 and not w.isdigit() and w not in NOISE_WORDS)
        rows.append((padded, "checked", str(len(spec_words)), str(len(missing))))
        if missing:
            findings.append((n, comp[0].name, missing))
    with OUT.open("w") as f:
        f.write("# doc-parse spec coverage cross-check\n\n")
        f.write("Parse transcript (different model family) vs consumed vision spec. ")
        f.write("Words present in the parse but absent from the spec are candidate ")
        f.write("MISSING-CONTENT items for the build worker to verify against the original.\n\n")
        f.write("| slide | state | spec_words | parse_only_words |\n|---|---|---|---|\n")
        for r in rows:
            f.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |\n")
        f.write("\n## Candidate missing content (parse-only words, len>=4)\n\n")
        if not findings:
            f.write("None — every parse word is represented in the specs.\n")
        for n, cname, missing in findings:
            f.write(f"### Slide {n} ({cname})\n\n")
            f.write("- " + ", ".join(f"`{w}`" for w in missing) + "\n\n")
    print(f"wrote {OUT} — {len(findings)} slides with parse-only words")


if __name__ == "__main__":
    main()
