# rendercheck_r2 — read-only render gate sample, deck 03 (2026-10-31)

- NS = `/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent`
- Deck = `recreated_pptx/03_ridger_regression_gradient_descent_final.pptx` (md5 `872284b7f41336fddf39b84ef5ddc63e`, == ledger `deck_md5`, MATCH)
- Outputs (all under this dir): `rendercheck_r2.py`, `deck PDF`, `pages/`, `src/`, `src_png/`, `metrics.json`, `gate_report.txt`
- **Read-only honored**: no git, no DB writes, deck/ledger untouched. `build/final_deck/render_check_pages.py` was NOT executed because its `main()` ends in `T.mark_render(...)` (`final_deck_tool.py:297-309`), which rewrites `final_deck_state.json`. Instead `rendercheck_r2.py` replicates its method exactly (one LO profile session, deck→PDF, per-slide pptx→PDF, `pdftoppm -r 150`, PIL `ImageChops.difference`, 0-px PASS rule) but writes only here and uses a private LO profile (`lo_profile/`) so the shared `scratch/tmp/s21_lo_profile_299640` and concurrent workers are unaffected. No `final_deck_tool.py update` was run.

## 1. Per-page verdicts (pages 1,2,3,7,25,30,40,51; 150 dpi, 2001×1125 px)

| page | gate verdict | diff% (any channel) | diff% (>16) | diff bbox | mean abs/channel | ledger render_check at read time |
|---|---|---|---|---|---|---|
| 1 | FAIL | 0.2917 | 0.2224 | [177,652,1305,912] | 0.120 | FAIL |
| 2 | PASS | 0.0 | 0.0 | — | 0.0 | FAIL |
| 3 | FAIL | 0.3261 | 0.2524 | [187,142,1756,850] | 0.128 | FAIL |
| 7 | FAIL | 1.0087 | 0.7874 | [222,513,1803,866] | 0.452 | FAIL |
| 25 | FAIL | 20.6666 | 16.1749 | [172,138,1834,1107] | 17.667 | FAIL |
| 30 | PASS | 0.0 | 0.0 | — | 0.0 | FAIL |
| 40 | PASS | 0.0 | 0.0 | — | 0.0 | FAIL |
| 51 | PASS | 0.0 | 0.0 | — | 0.0 | PENDING (see §4) |

## 2. Package-context control (banked per-slide renders, scaled to 150-dpi size)

For each page the fresh single-slide render (`src_png/sNNN-*.png`) was also diffed against the banked rejudge per-slide render `$RJ/slideNNN/render.png` (LANCZOS-resized), and the deck page against the same banked render:

| page | src vs banked diff% | deck vs banked diff% | interpretation |
|---|---|---|---|
| 1 | 0.0 | 0.2917 | single-slide renders identical; only the 51-page-package render differs |
| 2 | 0.0 | 0.0 | fully identical |
| 3 | 0.0 | 0.3261 | package-context only |
| 7 | 0.0 | 1.0087 | package-context only |
| 25 | **6.9264** | 20.747 | on-disk pptx renders differently from the banked render too → real content change |
| 30 | 0.0 | 0.0 | fully identical |
| 40 | 0.0 | 0.0 | fully identical |
| 51 | 0.0 | 0.0 | fully identical |

OPC byte check (deck vs on-disk `slide_NNN_recreated.pptx`): for pages 1,2,3,7,25,40,51 the deck's `ppt/slides/slideN.xml` and `notesSlideN.xml` are **md5-identical** to the source's `slide1.xml`/`notesSlide1.xml`, and rels are correctly retargeted (`imgNNN_*` media rename per the merge law). Media bytes are identical for all sampled pages **except page 25**, where all 4 deck media parts (`img025_image-1-{1..4}.png`, md5 0a81fe69/dd9e8fb9/bc226b60/bf74603b) differ from the current on-disk source media (cd62022f/b45c723a/7a8e7210/f6af102e — the latter match the canonical `plot_025_*.png` asset md5s banked in sweep_r35.md §3). Page 30's deck `slide30.xml` DIFFERS from the current on-disk slide_030 pptx, yet both render 0 px apart (non-visual XML delta in the newer rebuild).

Diff localization (150-dpi pixel histograms, >16 channel diff): page 3's diffs sit almost entirely in the top band (rows 0–112, the title line); page 1 in the lower-middle band (rows 652–912); page 7 in the middle content band (rows 513–866) — small localized text/edge anti-aliasing shifts, not wholesale content change. Page 25 differs across the entire slide (all row/col bins populated, max diff 255, mean-over-16 ≈ 168) — a different plot set, i.e. genuinely different content.

## 3. Conclusion — are the FAILs a package-context artifact?

**Mostly yes, with one real exception.** For pages 1, 3, 7 the deck-page bytes are identical to the certified per-slide bytes (XML + notes + media md5-verified), the fresh single-slide render is pixel-identical (0.0%) to the banked per-slide render, and only the render of the same slide inside the 51-page package differs, by ≤1.01% of pixels in localized bands. That is exactly a LibreOffice package-context rendering artifact, not a content defect — doctrine CONFIRMED on this sample. Pages 2, 30, 40, 51 render 0 px differ (gate-PASS) even in package context.

**Page 25 is NOT an artifact**: the deck still carries the pre-rebuild media bytes while the on-disk `slide_025_recreated.pptx` (md5 `c50e78bf…`, the canonical rebuild) contains different plot images; deck page 25 vs fresh source render differs by **20.67%** of pixels across the whole slide, and source-vs-banked differs by 6.93%. This matches the ledger (`source_md5` stale for 25) and the DB (slide 25 = `building`/blank visual_check, k17z3 FULL+CROP verdicts FAIL per sweep_r35 §4). Page 25 needs a content restage (`final_deck_tool.py update 25`) once slide 25 is certified — not just a re-mark.

## 4. Ledger reconciliation (PASS 14,19,33,50 vs earlier "51")

At read time (before the 08:44/08:49 fleet-wide re-gates) the ledger showed render_check PASS = {14, 19, 33, 50}, FAIL = 46, PENDING = 1 (page 51). The "14,19,33,51" figures came from gates `gate_20261031-080637_p33-50-51`, `gate_20261031-081426_p51` and the 08:19:31 watcherA re-mark — all on the pre-08:26 deck bytes. Event `update-page 51` at **2026-10-31T08:26:31** re-staged page 51 and reset its `render_check` to PENDING (`final_deck_tool.py:252`), which is the state the r35 sweep (08:32–08:36) recorded. So both statements are consistent: 51 passed the gate on the old bytes, then was restaged and went PENDING. **This r2 run shows page 51 gate-clean (0 px) on the current bytes** — it needs only a render-gate mark, not a restage. (Note: at final write time, 08:44:56 and 08:49:15 fleet-wide 51-page gates re-marked ALL pages FAIL with mismatched set [1,3,4,7,12,13,23,25,27,36,37,46,49] — concurrent with this read-only run; deck md5 still matches ledger.)

## 5. Pages needing restage (ledger `source_md5` != md5 of on-disk per-slide pptx, basename-resolved)

Current as of this run (**8 pages**: 4, 5, 10, 13, 15, 21, 25, 30):

| page | ledger source_md5 | disk md5 | ledger updated_at | file mtime | note |
|---|---|---|---|---|---|
| 4 | 761bcac7… | f65fd300… | 2026-10-26T00:41 | 2026-10-31 08:37 | rebuilt after staging |
| 5 | 03b77ff5… | c72f0be1… | 2026-10-26T03:22 | 2026-10-31 08:37 | rebuilt after staging |
| 10 | 9b4ee43a… | 67b341ef… | 2026-10-25T15:00 | 2026-10-27 16:24 | rebuilt after staging |
| 13 | 468d8481… | 244dde61… | 2026-10-25T15:00 | 2026-10-31 08:19 | rebuilt after staging |
| 15 | 39dc053a… | b6b3a99d… | 2026-10-30T22:12 | 2026-10-31 08:37 | rebuilt after staging |
| 21 | c094b309… | 9099303f… | 2026-10-31T00:18 | 2026-10-31 08:37 | rebuilt after staging |
| 25 | 8a355c24… | c50e78bf… (= canonical) | 2026-10-31T02:54 | 2026-10-31 07:37 | **content differs** (see §3); DB row still building |
| 30 | bbb6a634… | c48f8fa3… | 2026-10-25T15:01 | 2026-10-31 08:37 | xml differs but renders 0 px (non-visual delta) |

Sweep r35 (08:32–08:36) reported only **4, 10, 13, 25**; the mismatch set has since grown to 8 because per-slide pptx files 4/5/15/21/30 were rebuilt at 08:19–08:37, after the ledger staged them. Most ledger `source_pptx` paths are stale `/home/ahmed/Projects/...` founder-machine paths; comparison above is by basename under `recreated_pptx/`.

## 6. Artifacts

- `rendercheck_r2.py` (read-only replica), `metrics.json`, `gate_report.txt`
- `pages/pgNNN-*.png` (deck page renders), `src/sNNN.pdf` + `src_png/sNNN-*.png` (fresh single-slide renders), deck PDF in this dir
- No ledger, deck, DB, or evidence files were modified or deleted.
