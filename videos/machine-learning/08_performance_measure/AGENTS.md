# AGENTS.md — Machine Learning 08 Performance Measure (videos/machine-learning/08_performance_measure/)

## Video-specific rules

This namespace follows the root AGENTS.md and the machine-learning course conventions. No additional course-level AGENTS.md exists.

## House frame rule (root AGENTS.md 2026-10-09 — binding)

ALL recreated slides share the house template from the ml-intro course (slide 3 reference):

- Slide size: LAYOUT_WIDE 13.33 × 7.5 in; background `#E8E8E8`
- Outer red frame: `x=0.15, y=0.15, w=13.03, h=7.2`, border `#C00000` width 1.5
- Slide-number badge: yellow circle `x=12.48, y=0.30, w=0.5, h=0.5` (fill `#FFF9C4`, outline `#FFF9C4`), bold numeral 18pt `#333333` — badge numeral = number printed on ORIGINAL slide image
- Slide title: text box at `y=0.28` (`x=0.6, w=12.13`, centered)

These override any per-slide analysis JSON or judge finding.

## Math equation format (root AGENTS.md 2026-10-09)

Professional Format (2D) only — matplotlib mathtext → 600dpi PNG → pptxgenjs.addImage() at exact size. OMML wrap via scripts/18_omml_wrapper.py post-certification.

## Single-version rule (founder 2026-10-10)

One pptx per slide: `slide_NNN_recreated.pptx` — no suffixes. Graphs and OMML embedded in same file.

## Web-source verification (if mandated)

No video-specific AGENTS.md mandates web-source verification. If source research is needed, follow references/source-research.md under sources/.

## Dual-read certification law (re-judge mandate)

A single judge PASS is NOT certification. For every slide:

1. **First read**: the worker's own judge attempt (`judge_attempt_N.txt`) returning
   `FINAL VERDICT: PASS`.
2. **Corroboration read**: a SECOND, independent visual read — fresh vision call,
   fresh transcript (`judge_verify_1.txt` in the slide's QA dir), re-derived from the
   CURRENT pptx render, never a copy of the first transcript. It must also return
   `FINAL VERDICT: PASS`.
3. Only then may `gen_status=passed` be set in the progress DB. Both transcript paths
   are recorded in `pool_run/verification_ledger.md`.
4. A failing corroboration read RE-OPENS the slide: the worker fixes and re-runs both
   reads (attempt counter continues). A single-read PASS must be labeled
   `single-read, unconfirmed` — never phrased as certification.

## Re-analysis lane

Every certified slide also gets a fresh vision re-read of its ORIGINAL frame
(spec cross-check, not the same comparison re-run): `12_analyze_slides.py` writes to
`analysis/reanalysis/` (separate dir — never clobber the consumed spec). Any material
content delta found there (text the spec missed) re-opens the slide's build.

## Doc-parse crop-cascade mandate (dense slides)

Slides whose originals are dense — stacked equations, confusion matrices, ROC/diagram
flows — get a doc-parse crop-cascade parse of the original frame
(`~/.agents/skills/doc-parse/scripts/crop_cascade.py`) banked under
`pool_run/docparse/slideNNN/` before first-judge submission. The parsed markdown is
DATA for the build's verbatim-text check; it never overrides the house frame rule.

## Parallel processing configuration

Pool size: 24 workers. All pooled-missions files live under this namespace. Workers use image-analysis + visual-judge (paired), doc-parse (crop cascade), web search, and slide-recreation resources concurrently.