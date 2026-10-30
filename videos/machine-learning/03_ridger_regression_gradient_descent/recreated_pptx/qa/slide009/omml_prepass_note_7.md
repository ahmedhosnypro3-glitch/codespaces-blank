# OMML wrap prepass — slide 009, attempt 7 (post annotation-fix rebuild)

Date: 2026-10-26 01:41. Single-version law: the plain-named deliverable now carries the
OMML wrap (PowerPoint shows editable native equations; LibreOffice renders the exact
certified pixels).

## Inputs (verified before wrapping)

- Plain pptx pre-wrap: `slide_009_recreated.pptx` md5 `d58d5bd33624a4d920322ac31559cdd6`
  (124814 B) — banked as `qa/slide009/pre_omml_wrap2_d58d5bd3.pptx`.
- Manifest `qa/slide009/omml_manifest_7.json`: rId1 → `eq_009_left_attempt4.png`
  (`50.85^{2} = 2585`, 12.1 pt), rId2 → `eq_009_right_attempt4.png`
  (`63.64^{2} = 4050`, 12.1 pt); both asset md5s re-verified
  (`98ebbe2649ec777d87637650af05c096`, `a287d6661cdb10162267ab8f56fcc4ca`).
- Pptx rels re-derived from the CURRENT package: rId1 → `media/image-1-1.png`,
  rId2 → `media/image-1-2.png` (rel ids do survive this rebuild; verified, not assumed).

## Wrap result

`scripts/18_omml_wrapper.py` (PowerPoint-author v2 pattern) wrapped 2/2, skipped 0:
- rId1: 1584 B OMML-para
- rId2: 1584 B OMML-para

Zip-level check: identical 41-entry set; media bytes untouched (11254 / 11211 B);
`mc:AlternateContent` present in slide1.xml. File size 124814 → 41241 B is
deflate-vs-stored recompression only (uncompressed totals 119940 → 124539 B).

## LO render proof (pixel gate)

Headless LO with the scratch profile
(`-env:UserInstallation=file:///home/ahmed/Projects/ai_llm_slides/scratch/tmp/lo_009`;
founder's GUI untouched): wrapped pptx → PDF → pdftoppm 150 dpi →
`omml_prepass_7_page-1.png`.

- `render_7.png` md5 `84fc8bfc4d403edf248fb442ede3313a`
- wrapped render md5 `84fc8bfc4d403edf248fb442ede3313a` — **byte-identical files**
- PIL ImageChops: 0 of 2,251,125 pixels differ (bbox None).

## Deliverable

`slide_009_recreated.pptx` replaced atomically with the wrapped build;
new md5 `0003d2cbb6f3717154a5eef9df3de8c2` (this hash feeds the final-deck ledger
update — the old ledger row `af0598c8…` was stale). The wrap is idempotent and
fail-loud per the v2 contract; no LO resave of the wrapped file was performed.
