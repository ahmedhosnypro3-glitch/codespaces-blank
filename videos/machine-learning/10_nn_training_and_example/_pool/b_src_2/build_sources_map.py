#!/usr/bin/env python3
"""Rebuild the fleet SOURCES_MAP.md for the 10_nn_training_and_example deck.

One row per slide (1..34). For each slide, report whether its SOURCES.md exists,
how many distinct real URLs it cites, whether it carries an "## Audit" section
(lane-S audit state), and a short note.
"""
import os
import re
import sys

NS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(NS, "sources")
URL_RE = re.compile(r"https?://[^\s)>\]\"]+")

# Short per-slide note: the deck's topic line, from the certified analysis where available.
TOPIC = {}
for n in range(1, 35):
    for cand in ("slide_%03d_final.json" % n, "slide_%03d_raw.json" % n):
        p = os.path.join(NS, "analysis", cand)
        if os.path.exists(p):
            try:
                import json
                with open(p, encoding="utf-8") as fh:
                    TOPIC[n] = json.load(fh).get("slide_title", "") or TOPIC.get(n, "")
            except Exception:
                pass
    if n not in TOPIC or not TOPIC[n]:
        TOPIC[n] = ""

FALLBACK = {
    1: "Introduction / opening frame",
    2: "Introduction / opening frame",
    3: "Introduction / opening frame",
    4: "Introduction / opening frame",
    5: "Introduction / opening frame",
    6: "Introduction / opening frame",
    7: "Introduction / opening frame",
    8: "Introduction / opening frame",
    9: "Introduction / opening frame",
    10: "Introduction / opening frame",
    11: "Introduction / opening frame",
    12: "Introduction / opening frame",
    13: "Introduction / opening frame",
    14: "Introduction / opening frame",
    15: "Introduction / opening frame",
    16: "Introduction / opening frame",
    17: "Introduction / opening frame",
    27: "Example / Forward",
    28: "Example / Backward (output layer)",
    30: "Example / Backward (hidden layer)",
    32: "Updated weights after iteration #1 (scatter plots)",
}

rows = []
for n in range(1, 35):
    rel = "sources/slide_%03d_source/SOURCES.md" % n
    path = os.path.join(NS, rel)
    if not os.path.exists(path):
        rows.append((n, rel, 0, "missing", "No SOURCES.md — research leg did not run for this slide."))
        continue
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    urls = sorted(set(URL_RE.findall(text)))
    has_audit = "\n## Audit" in text or text.lstrip().startswith("## Audit")
    topic = TOPIC.get(n) or FALLBACK.get(n, "")
    if not urls:
        state = "no-urls"
        note = "SOURCES.md exists but cites NO real URL — research incomplete."
    elif not has_audit:
        state = "audit pending"
        note = "SOURCES.md present, %d source(s); lane-S audit section not yet written." % len(urls)
    else:
        state = "audited"
        note = "Lane-S audit written: questions, answers, per-claim verdicts."
    if topic:
        note = topic + " — " + note
    rows.append((n, rel, len(urls), state, note))

audited = sum(1 for r in rows if r[3] == "audited")
pending = sum(1 for r in rows if r[3] == "audit pending")
nourl = sum(1 for r in rows if r[3] == "no-urls")
missing = sum(1 for r in rows if r[3] == "missing")

out = []
out.append("# SOURCES_MAP.md — fleet source index")
out.append("")
out.append("Video namespace: `videos/machine-learning/10_nn_training_and_example/`.")
out.append("Deck: 34 approved slides, `unique_slides/slide_001.jpg` … `unique_slides/slide_034.jpg`")
out.append("(badge number = printed on-slide number; no `new2old_mapping.json` — clean namespace).")
out.append("")
out.append("Per-slide provenance records live in `sources/slide_NNN_source/SOURCES.md`.")
out.append("**No SOURCES.md = the research leg did not run**, never that research found nothing.")
out.append("")
out.append("Method: agy web-search MCP (grounded Google search) + live page fetch +")
out.append("independent numerical recomputation; each slide's claims are checked against")
out.append("its banked doc-parse transcript (`analysis/parse/slide_NNN.parse.md`) and its")
out.append("certified analysis JSON (`analysis/slide_NNN_final.json`). Frame text is ground")
out.append("truth for recreation; sources confirm/correct DATA only.")
out.append("")
out.append("## State legend")
out.append("")
out.append("| state | meaning |")
out.append("|---|---|")
out.append("| `audited` | `## Audit` section present: questions asked, answers, per-claim verdicts (CONFIRMED / NOT-VERIFIABLE / CONFLICT). |")
out.append("| `audit pending` | SOURCES.md exists and cites real URL(s), but the lane-S audit has not been written yet. |")
out.append("| `no-urls` | SOURCES.md exists but cites no real URL. |")
out.append("| `missing` | No SOURCES.md for this slide. |")
out.append("")
out.append("## Per-slide index")
out.append("")
out.append("| slide | SOURCES.md | sources count | state | notes |")
out.append("|---|---|---|---|---|")
for n, rel, cnt, state, note in rows:
    out.append("| %03d | `%s` | %d | %s | %s |" % (n, rel, cnt, state, note))
out.append("")
out.append("## Totals")
out.append("")
out.append("- Slides indexed: **34** (one row each).")
out.append("- `audited`: **%d** — `audit pending`: **%d** — `no-urls`: **%d** — `missing`: **%d**."
           % (audited, pending, nourl, missing))
out.append("")

out.append("## Audit coverage")
out.append("")
out.append("- **Slides 018–034 — AUDITED** by lane-S scope `b_src_2` (2026-10-31). Each has")
out.append("  an `## Audit` section with the questions asked, the independent answers")
out.append("  (grounded web search + live page fetch + numerical recomputation), and a")
out.append("  per-claim verdict (CONFIRMED / NOT-VERIFIABLE / CONFLICT). All 17 cite real URLs.")
out.append("- **Slides 001–017 — AUDIT PENDING.** Written by lane-S scope `b_src_1`")
out.append("  (`b_src_1-worker-agy`), which was still `in_work` in `_pool/mission.db` when this")
out.append("  map was finalized. Their `SOURCES.md` files exist and every one of them cites at")
out.append("  least two real URLs, so the research leg ran — but none has an `## Audit` section")
out.append("  yet, so their claims are NOT independently re-verified by a second lane. These")
out.append("  rows are marked `audit pending` rather than `audited` for exactly that reason;")
out.append("  they are not dropped. Re-run this map's generator")
out.append("  (`_pool/b_src_2/build_sources_map.py`) once scope `b_src_1` closes to re-grade")
out.append("  those 17 rows. Recorded as an open work item.")
out.append("")
out.append("## Notable audit findings (slides 018–034)")
out.append("")
out.append("- **slide 023** was the only file in the deck with **zero URLs** — it named only")
out.append("  generic textbooks with no citable links. Four real flowchart sources were added;")
out.append("  this was a lane-S rule violation and is now fixed.")
out.append("- **slide 018**: the certified `slide_018_final.json` prints `∂E/∂w_ij`, while the")
out.append("  frame label, the parse transcript, and slides 19–22 all read `w_ji` — an index")
out.append("  inversion to fix at build time (same issue recorded on slide 19).")
out.append("- **slides 027/028/031**: the live-fetched Matt Mazur canonical example is a")
out.append("  *different* network (inputs 0.05/0.10, 2 hidden nodes, η = 0.5, targets")
out.append("  0.01/0.99). It confirms the frame's computational order and formulas, **not** the")
out.append("  deck's specific numbers. One grounded-search response returned model-fabricated")
out.append("  arithmetic (a 2-hidden-node variant, net_h1 = 1.2); it was discarded, not cited.")
out.append("- **slides 030/031**: the course uses the ALREADY-UPDATED output-layer weights")
out.append("  inside the hidden-layer `Σ_k(δ_k w_kj)` sums. The canonical worked example")
out.append("  explicitly uses the ORIGINAL weights. Recorded as a course convention — the frame")
out.append("  wins for recreation. Also `ΔW32=5*0.005*1=0.125` is arithmetically impossible")
out.append("  (it needs the multiplier 5).")
out.append("- **slide 031**: the certified JSON prints `W42=0.075+0.075=0.15`, but its own ΔW")
out.append("  line and slide 30's parse transcript give `W42=0.5+0.075=0.575`.")
out.append("- **slide 032**: all TEN values of the \"after iteration # 1\" panel match the run's")
out.append("  computed new-weight set exactly (the prior note claimed nine).")
out.append("- **slides 029/031**: transcribed noise in the analysis JSON (`−0.344`/`−0.445` vs")
out.append("  the correct `−0.134`/`−0.455`) — a build that carries both draws a wrong diagram.")
out.append("- **slide 034**: the \"Squared Error\" column is `Σₖ(tₖ−Oₖ)²` **without** the ½")
out.append("  factor — all six rows verified to <1e-5. Any regenerated error plot must use the")
out.append("  same rule.")
out.append("- **η = 5** on slides 27–34 is reproducible and internally consistent on every")
out.append("  line, but is far outside the usual 0.01–0.1 range (Mazur's own example uses")
out.append("  0.5). Reproduce verbatim; do not \"correct\" it.")
out.append("")

text = "\n".join(out) + "\n"
dest = os.path.join(NS, "SOURCES_MAP.md")
if "--dry-run" in sys.argv:
    dest = "/tmp/SOURCES_MAP_dryrun.md"
with open(dest, "w", encoding="utf-8") as fh:
    fh.write(text)
print("wrote %s (%d lines): audited=%d pending=%d no-urls=%d missing=%d"
      % (dest, len(out), audited, pending, nourl, missing))
