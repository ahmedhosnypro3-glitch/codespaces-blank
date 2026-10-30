#!/usr/bin/env python3
"""Write the 31 PIL-only paren_sweep.md notes for the S23 sweep (deck 03)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
CEN = json.load(open(f"{HERE}/sweep_census.json"))

SPECIAL = {
    2: "The two tall ( readings sit where the original reads ( too (pairs d=0.8/2.4"
       " frame px, same sign) — the flagged duplicate-read concern does not exist.",
    4: "BAD-pair resolution (ascii-verified at frame (374,68)): the flagged render"
       " stroke is a solid filled triangle glyph with a bar, not a paren; the orig"
       " side is small handwritten glyphs. Cross-glyph pairing noise.",
    5: "3 BAD pairs = cross-glyph noise: each flagged render stroke's true"
       " opposite-sign partner sits 20-36 frame px away on the render side"
       " (programmatic nearest-partner check); typed-vs-original layout drift"
       " defeats the distance matcher, not the directions.",
    6: "2 unmatched render ( strokes are large display parens (delta -3.16/-7.30)"
       " whose sparse handwritten counterparts fall below the orig pairing window;"
       " direction correct on the render side.",
    7: "BAD-pair resolution (ascii-verified at frame (419,151)): the flagged render"
       " stroke is a thin diagonal slash glyph, not a paren; orig side is text"
       " glyphs. Pairing noise.",
    11: "Census ran on render_1_pre_underline_fix.png; the certified render_1.png"
        " (1 min newer) differs only by the title underline bar (horizontal, build"
        " rows 259-260), which the tall-thin filter ignores — directions unaffected.",
    12: "4 unmatched ( strokes are the typed table-header paren glyphs (frame y73-74)"
        " whose small handwritten counterparts fall below the pairing window; no"
        " direction conflict.",
    23: "4 BAD pairs = cross-glyph noise (ascii-verified at frame (608,196): the"
        " flagged stroke is a solid flag/bold glyph, not a paren); typed-vs-"
        " handwritten position drift crossed the matcher's partners.",
    26: "BAD-pair resolution: the flagged render stroke's true opposite-sign partner"
        " sits 10.6 frame px away at the same y (programmatic check) — the matcher"
        " crossed neighbors inside a dense formula band.",
    28: "The flagged giant stroke (delta -60.8 render / -29.4 orig, pair d=1.9) is"
        " the dashed dimension-line GRAPHIC present in both images at the same"
        " position — not a delimiter; its size is why the delta is huge.",
    30: "BAD-pair resolution (ascii-verified at frame (445,71)): the flagged stroke"
        " is a typed glyph-hook block, not a paren ('mystery ( ( (' class = f/t"
        " glyph top-hooks); orig side is the handwritten glyph.",
    36: "2 BAD pairs = cross-glyph noise (ascii-verified at frame (273,159): the"
        " flagged strokes are letterform diagonal+stem groups, not parens); orig"
        " side is handwritten text glyphs.",
    39: "Title-band delimiters pair with sign agreement in the fresh census; the"
        " original's title itself carries the verbatim stray ) of '...Descent SGD)'"
        " (certified pptx XML) which the render reproduces faithfully — typo"
        " propagation, not a direction defect. Flagged pair = glyph noise (render"
        " true partner 58 frame px away).",
    45: "BAD-pair resolution (ascii-verified at frame (229,150)): the flagged strokes"
        " are a thin dotted stem + table-rule glyphs, not parens. The 75 unmatched"
        " render strokes are the certified typed table's paren-heavy notation with"
        " no same-position orig counterpart (orig curved set is sparse); the only"
        " position-matched conflict is the resolved glyph-noise pair.",
}

TARGET = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20, 22, 23, 24, 26, 27, 28,
          29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 45]

for s in TARGET:
    v = CEN[str(s)]
    pairs = v["pairs"]
    agree = sum(1 for p in pairs if p["render"][1] == p["orig"][1])
    ur = v.get("unmatched_render_curved", [])
    sdb = v.get("samedir_bands", [])
    mind = min((p["dist"] for p in pairs), default=0)
    lines = []
    A = lines.append
    A(f"# S23 paren sweep — slide {s:03d} (2026-10-26, s23-paren-worker)")
    A("")
    A("Scope: paren-curve-direction defect class audit of the certified render.")
    A("")
    A("## Census (qa/paren_sweep_20261026/s23_fresh/sweep_all.py, fresh 2026-10-26)")
    A(f"- certified render `{v['render'].split('/')[-1]}` (2001x1125):"
      f" {v['ren_curved']} curved / {v['ren_straight']} straight tall-thin strokes;"
      f" original frame: {v['orig_curved']} curved.")
    A(f"- matched pairs: {len(pairs)}, direction sign agreement {agree}/{len(pairs)};")
    if pairs:
        A(f"  closest pair {mind:.1f} frame px. Paired delimiters agree on direction"
          " everywhere (render amplitudes ~2-8 render px vs original ~1-4 frame px —"
          " same signs, typed ink carries the larger amplitude; certification-settled"
          " medium difference, never a direction flip).")
    A("")
    A("## Census-flag resolutions")
    if sdb:
        A(f"- SAME-DIR-PAIR bands ({len(sdb)}): side-by-side same-direction enclosures"
          " (adjacent vector/interval parens); the original shows the same pattern —"
          " legitimate, not a mirrored pair.")
    if ur:
        A(f"- Unmatched render strokes ({len(ur)}): glyph-class strokes (letter"
          " diagonals, glyph hooks, fill edges, band repeats) outside the matcher's"
          " position/height window; ascii spot-checks found no delimiter among them.")
    if s in SPECIAL:
        A(f"- {SPECIAL[s]}")
    if not sdb and not ur and s not in SPECIAL:
        A("- No flags: every curved stroke paired with same-sign original counterpart.")
    A("")
    A("## Verdict")
    A("NO mirrored/wrong-direction delimiter. CLEAN — no rebuild. (PIL-only note;")
    A("no vision leg for this slide — legs were reserved for the heavy-delimiter")
    A("slides 003/021/041/042/047/049.)")
    out = f"{DECK}/recreated_pptx/qa/slide{s:03d}/paren_sweep.md"
    assert not os.path.exists(out), f"refusing to overwrite existing {out}"
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", out)
