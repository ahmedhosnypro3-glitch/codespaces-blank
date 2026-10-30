# doc-parse cross-check findings — actionable spec gaps

Cross-checked with `pool_run/docparse/spec_coverage_check.py` (doc-parse composed
transcripts, a DIFFERENT model family from the vision analysis lane, vs the consumed
specs). Register: `pool_run/docparse/spec_coverage.md`.

Filtered out before reporting:
- Words emitted from `<class_Picture>` regions — the parser garbles logo/photo OCR.
- Cascade bookkeeping words (parse/crop/degraded/manifest vocabulary).

## CONFIRMED — Slide 1: "CSAI 253 - Spring 2024" missing from the spec

The composed parse has a positioned text element `CSAI 253 - Spring 2024` at
(x=329, y=282, w=293, h=26). The vision spec's `verbatim_text.labels` lists the
instructor lines, the slide number and the university logos, but NOT this line.

- Action for slide 1's build worker: verify the line against
  `unique_slides/slide_001.jpg` and place it at the measured position if present.
- The vision lane's `analysis/reanalysis/slide_001_raw.json` also omitted it, so this
  is a two-read gap, not a single-read fluke.

## LOW-SIGNAL — remaining parse-only words

`other` (slides 5, 20, 21, 24), `note` (5), `category` (13), `axis`/`color`/
`items`/`multi` (17), `docg` (18), `normal` (21). These are generic tokens and
likely garbled OCR — each needs a vision read of the original region before any
build change. Do NOT add them to a build on this evidence alone.
