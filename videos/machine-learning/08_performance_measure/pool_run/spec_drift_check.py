#!/usr/bin/env python3
"""Spec-drift check: reanalysis (fresh read of the ORIGINAL frame) vs the
consumed spec (analysis/slide_NNN_final.json).

A MATERIAL delta is text or a data value present in the reanalysis but missing
from the consumed spec — i.e. the build was handed a spec that did not contain
something the original frame actually shows. Writes findings to spec_drift.md.

Usage:
  spec_drift_check.py <analysis_dir> <reanalysis_dir> <out.md> [slide ...]
"""

import difflib
import json
import os
import re
import sys

# Text that carries no content signal for drift purposes.
NOISE = re.compile(
    r"^(n/?a|none|null|\[?\]?|-+|—+|…+|\?+)$",
    re.I,
)

# A reanalysis string this similar to a consumed-spec string is the SAME text
# (vision OCR jitter, one-character slip), not content the build is missing.
SIMILARITY_THRESHOLD = 0.90


def norm(s):
    """Normalize for comparison: collapse whitespace, unify quotes/dashes."""
    if s is None:
        return ""
    s = str(s)
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def significant(s):
    s = norm(s)
    return bool(s) and not NOISE.match(s)


def text_items(d):
    """Collect title + bullets + labels + equations as tagged strings."""
    out = []
    t = d.get("slide_title")
    if significant(t):
        out.append(("slide_title", norm(t), str(t)))
    vt = d.get("verbatim_text") or {}
    for key in ("bullets", "labels", "equations"):
        for item in vt.get(key) or []:
            if isinstance(item, dict):
                item = item.get("text") or item.get("label") or json.dumps(item)
            if significant(item):
                out.append((f"verbatim_text.{key}", norm(item), str(item)))
    return out


NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def data_values(d):
    """Every number appearing in a table/chart element description."""
    vals = []
    for el in d.get("visual_elements") or []:
        if not isinstance(el, dict):
            continue
        etype = str(el.get("type") or "").lower()
        if etype not in ("table", "chart", "graph", "confusion-matrix", "matrix"):
            continue
        desc = str(el.get("description") or "")
        for n in NUM_RE.findall(desc):
            vals.append((f"visual_elements[{etype}].data", n, desc[:300]))
    return vals


def contains_token(hay_norm, token_norm):
    """Is token present in haystack? (exact, or as a whitespace-normalized substring)"""
    if not token_norm:
        return True
    return token_norm in hay_norm


def best_ratio(token_norm, pool):
    """Best similarity between token and any string in pool."""
    best = 0.0
    for cand in pool:
        if not cand:
            continue
        r = difflib.SequenceMatcher(None, token_norm, cand).ratio()
        if r > best:
            best = r
    return best


def present_in_spec(ntext, final_items, final_blob):
    """True when the reanalysis text is (near-)present in the consumed spec."""
    if contains_token(final_blob, ntext):
        return True
    pool = [x[1] for x in final_items]
    # Long text: substring/containment against the blob is enough.
    if len(ntext) > 40:
        return any(ntext in p or p in ntext for p in pool if p)
    # Short text: tolerate vision jitter (one-character slips in a name/label).
    if best_ratio(ntext, pool) >= SIMILARITY_THRESHOLD:
        return True
    # Multi-word short text: compare against each final item's own words too,
    # so "Zewail City" matches a spec item "ZEWAIL CITY" written as one string
    # or as "ZEWAIL" + "CITY" split across labels.
    words = ntext.split()
    if len(words) > 1:
        for w in words:
            if len(w) < 3:
                continue
            if best_ratio(w, pool) < SIMILARITY_THRESHOLD:
                return False
        return True
    return False


def compare(slide, final_path, reana_path):
    final = json.load(open(final_path, encoding="utf-8"))
    reana = json.load(open(reana_path, encoding="utf-8"))

    findings = []

    # 1) Text fields: reanalysis item missing from the consumed spec.
    final_items = text_items(final)
    final_blob = norm(" | ".join(x[2] for x in final_items))
    final_title = norm(final.get("slide_title") or "")

    for field, ntext, raw in text_items(reana):
        if present_in_spec(ntext, final_items, final_blob):
            continue
        # Title comparison: allow a superset title (spec may carry extra words),
        # but flag when the reanalysis title shares no significant token with it.
        if field == "slide_title":
            fr = set(re.findall(r"[a-z0-9]+", final_title))
            rr = set(re.findall(r"[a-z0-9]+", ntext))
            if rr and rr <= fr:
                continue
            if fr and rr and (rr & fr):
                # Titles overlap but differ — report as a delta for review.
                findings.append((field, raw, str(final.get("slide_title") or "")))
                continue
        findings.append((field, raw, ""))

    # 2) Data values in table/chart elements missing from the consumed spec.
    # Compare each number against the final spec's table/chart descriptions AND
    # its text blob, so a value that appears anywhere in the spec is not drift.
    final_data_blob = norm(" ".join(
        str(el.get("description") or "")
        for el in (final.get("visual_elements") or [])
        if isinstance(el, dict)
    )) + " " + final_blob
    for field, token, ctx in data_values(reana):
        if token in final_data_blob:
            continue
        findings.append((field, token, ctx))

    return findings


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    analysis_dir, reana_dir, out_md = sys.argv[1], sys.argv[2], sys.argv[3]
    slides = sys.argv[4:]

    rows = []
    if slides:
        names = slides
    else:
        names = sorted(
            f for f in os.listdir(reana_dir)
            if f.startswith("slide_") and f.endswith("_raw.json")
        )

    for fname in names:
        slide = fname.replace("_raw.json", "").replace("slide_", "")
        final_path = os.path.join(analysis_dir, f"slide_{slide}_final.json")
        reana_path = os.path.join(reana_dir, fname)
        if not os.path.isfile(final_path):
            rows.append((slide, "SKIP", "verbatim_text.*", "", "no consumed final spec"))
            continue
        if not os.path.isfile(reana_path):
            rows.append((slide, "SKIP", "*", "", "no reanalysis file"))
            continue
        try:
            findings = compare(slide, final_path, reana_path)
        except Exception as e:  # noqa: BLE001 - report, never crash the lane
            rows.append((slide, "ERROR", "*", "", str(e)))
            continue
        for field, reana_text, final_text in findings:
            rows.append((slide, "DRIFT", field, reana_text, final_text))

    material = [r for r in rows if r[1] == "DRIFT"]

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Spec drift — reanalysis vs consumed spec\n\n")
        f.write("Reanalysis = fresh vision re-read of the ORIGINAL frame "
                "(`analysis/reanalysis/`). Consumed spec = `analysis/slide_NNN_final.json`, "
                "the spec the build worker actually used.\n\n")
        f.write("A MATERIAL delta is text or a table/chart data value present in the "
                "reanalysis but absent from the consumed spec — the build could not "
                "have rendered it. Per-slide build re-dispatch is the parent "
                "orchestrator's call; this lane only banks the finding.\n\n")
        if material:
            f.write("## Material deltas\n\n")
            for slide, _, field, reana_text, final_text in material:
                f.write(f"### Slide {slide} — `{field}`\n\n")
                f.write(f"- **Reanalysis (original frame)**: {reana_text}\n")
                if final_text:
                    f.write(f"- **Consumed spec**: {final_text}\n")
                f.write("- **Action**: re-dispatch this slide's build worker to add the "
                        "missing content, then re-run both judge reads.\n\n")
        else:
            f.write("## Material deltas\n\n")
            f.write("None — no text or table/chart data value present in the "
                    "reanalysis is missing from the consumed spec.\n\n")
        others = [r for r in rows if r[1] in ("SKIP", "ERROR")]
        if others:
            f.write("## Not compared\n\n")
            for slide, status, field, a, b in others:
                f.write(f"- Slide {slide}: {status} — {field} {b}\n")
            f.write("\n")

    print(f"compared={len(names)} material_deltas={len(material)} -> {out_md}")
    for r in material:
        print(f"  DRIFT slide {r[0]} [{r[2]}] reana={r[3][:70]!r} final={r[4][:70]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
