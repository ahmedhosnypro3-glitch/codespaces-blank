# Compliance audit r1 — 03_ridger_regression_gradient_descent (2026-10-31)

Read-only auditor. Scope per tasking: (1) house-chrome check on sampled slides,
(2) SOURCES.md existence, (3) analysis finals existence, (4) rule-violation sweep.
Governing docs: namespace `AGENTS.md` (deck chrome + web-source mandate + zoomed-judge
mandate) and project-root `AGENTS.md`. No git commands were run.

## 1. House chrome (sample: 001, 014, 019, 025, 033, 051)

All six PASS via `shared_patterns/house_chrome_check.py` on the newest full-slide render
per slide (each render mtime verified newer than the current `slide_NNN_recreated.pptx`).
Panel E9E9E7 x54..903 y45..bottom, red C00000 strokes L/R/bottom present, TOP BARE
(no-top-stroke law holds), badge FDFD96/6A5ACD at (876,73) d~35 with numeral ink.
Detail log: `recreated_pptx/chrome_audit_r1.md`. **6/6 PASS, 0 FAIL.**

## 2. Web-source research (SOURCES.md per slide)

- `sources/` contains exactly 51 `slide_NNN_source/` dirs; **51/51 have a non-empty
  `SOURCES.md` — 0 missing.**
- Fleet map `SOURCES_MAP.md` present at namespace root; **51/51 slide rows present**.
- Mandate satisfied on existence/completeness of records.

## 3. Analysis finals

- `analysis/slide_001_final.json` … `slide_051_final.json`: **51/51 present — 0 missing**
  (plus aggregate `slides_final.json`, 51 raws, `RECONCILE_NOTE.md`, `summary.md`).
- `unique_slides/` holds exactly 51 `slide_NNN.jpg` frames (founder-curated set).

## 4. Other rule checks / observations

- Deliverables: 51 plain-named `slide_NNN_recreated.pptx` + final deck
  `03_ridger_regression_gradient_descent_final.pptx` present.
- **Finding (naming/single-version rule):** the deliverable root also carries
  `slide_014_recreated.pptx.bak_prefix3`, `slide_015_recreated_v2.pptx`,
  `slide_015_recreated_v3.pptx` (+ `slide_015_recreated.pdf`, `slide_015_recreated_v2.pdf`,
  `slide_015_recreated_v3.pdf`, `slide_025_recreated.pdf`). The single-version rule
  (one plain-named pptx per slide; superseded builds only under qa/ evidence dirs) is
  arguably violated by the `_v2`/`_v3` pptx variants sitting at the deliverable root.
  The `.bak_prefix3` file reads as a banked-evidence archive (never-delete law) rather
  than a parallel deliverable.
- `unique_slides/new2old_mapping.json` is present although the deck AGENTS.md says the
  founder removed the pre-curation index/mapping and the state is intentionally
  unrecoverable; `slides_index.json` is present but the AGENTS.md itself acknowledges it
  was rebuilt from raws' `_meta` (35/51 provenance). The mapping file's presence is an
  inconsistency with the "never hunt for old artifacts" note — flagged for the owner, not
  treated as a build defect.
- Zoomed-crop judging mandate (AGENTS.md §ZOOMED VISUAL JUDGE): crop-pair judge
  transcripts exist for many slides under `recreated_pptx/qa/` (e.g. slide014, slide019,
  slide025 crop_*_judge.txt); the sampled slides 001/033/051 show full-slide renders and
  dispatch briefs but no crop-pair certificates in the dirs inspected. This audit did
  not exhaustively verify crop coverage for all 51 slides — noted as not-fully-verified,
  not as a violation.
- Numeral identity: chrome checker verifies ink presence only; digit=N per AGENTS.md is
  asserted from the raws (48/48 verified per AGENTS.md) — accepted as documented.

## Verdict

| Check | Result |
|---|---|
| Chrome on sampled 6 slides | 6 PASS / 0 FAIL |
| SOURCES.md 51/51 | PASS (0 missing, all non-empty; map rows 51/51) |
| analysis finals 51/51 | PASS (0 missing) |
| unique_slides set = 51 | PASS |
| Rule violations in current state | 1 flagged: superseded `_v2`/`_v3`/`.bak`/stray pdf variants at deliverable root (single-version naming); zoomed-crop coverage not exhaustively audited |
