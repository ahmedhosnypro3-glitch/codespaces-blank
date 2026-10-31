# CLOSEOUT DRAFT — machine-learning lecture 03: Ridge Regression & Gradient Descent

Status: DRAFT (docs worker, 2026-10-31 ~08:47Z). Written to
`recreated_pptx/qa/rejudge_20261027/CLOSEOUT_DRAFT.md` because a (skeleton)
`CLOSEOUT_REPORT.md` already exists at the namespace root and was NOT touched.
Structure follows the closed decks' reports (`videos/machine-learning/01_ml-intro/CLOSEOUT_REPORT.md`,
`videos/deep-learning/*/CLOSEOUT_REPORT.md`). All counts measured live on 2026-10-31
from the named sources; the deck is still under active rejudge, so rejudge-census
numbers are point-in-time.

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`
RJ = `recreated_pptx/qa/rejudge_20261027/`

## 1. Overview

- 51 founder-curated unique slides (`unique_slides/slide_001.jpg` … `slide_051.jpg`;
  51 jpgs verified on disk, plus `new2old_mapping.json` + `slides_index.json`).
  Founder approved the frame set 2026-10-19 (HARD STOP lifted for this set).
  Frames 960×540, 1px = 1pt.
- House chrome per namespace `AGENTS.md` (measured 2026-10-19 from slide_003.jpg;
  DIFFERENT from ml-intro and lecture 02): white canvas `FFFFFF`, gray panel
  `E9E9E7` (x54, y45, w850, to bottom, no border), three red `C00000` 1pt strokes
  (left x58.5, right x901, bottom y538.5 — NO top stroke), yellow badge `FDFD96`
  with purple ring `6A5ACD` at (876, 73)px, numeral = file number N.
  Zoomed visual judge (FULL + CROP legs) mandatory on every slide.
- Deliverables: one single-version `slide_NNN_recreated.pptx` per slide (51 files
  verified, NNN = 001..051) + continuous final deck
  `recreated_pptx/03_ridger_regression_gradient_descent_final.pptx`
  (md5 `872284b7f41336fddf39b84ef5ddc63e`, matches ledger `deck_md5`).
  `recreated_pptx/*.pptx` glob count = 54: the 51 plain per-slide files + the final
  deck + 2 superseded variants still on disk (`slide_015_recreated_v2.pptx`,
  `slide_015_recreated_v3.pptx` — not deliverables, not deleted per evidence law).
- Analysis: 51 `slide_NNN_raw.json` + 52 `slide_NNN_final.json` (slide_050 rename
  recorded in `analysis/RECONCILE_NOTE.md`) + `summary.md`; 105 files total in
  `analysis/`.
- Certification: 50/51 slides `passed`/`PASS` in `slides_progress.db`; **slide 25 OPEN**.

## 2. Per-slide certification table (51 rows, measured 2026-10-31)

DB source: `sqlite3 slides_progress.db "SELECT gen_status,visual_check,COUNT(*) ..."`
→ `passed|PASS = 50`, `building|(blank) = 1`.
Rejudge columns = newest clean (zero error-429) FULL / CROP verdict per
`$RJ/slideNNN/`, computed 2026-10-31 08:46:53Z (VERDICT_CENSUS_r1.md did not exist;
this table is the computed census).

| # | DB gen_status | DB visual_check | Rejudge FULL (newest clean) | Rejudge CROP (newest clean) | Status |
|---|---|---|---|---|---|
| 001 | passed | PASS | FAIL | FAIL | certified (rejudge leg FAIL under adjudication) |
| 002 | passed | PASS | FAIL | FAIL | certified (leg FAIL under adjudication) |
| 003 | passed | PASS | FAIL | FAIL | certified (leg FAIL under adjudication) |
| 004 | passed | PASS | PASS | PASS | certified, both legs clean |
| 005 | passed | PASS | PASS | PASS | certified, both legs clean |
| 006 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 007 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 008 | passed | PASS | PASS | PASS | certified, both legs clean |
| 009 | passed | PASS | PASS | PASS | certified, both legs clean |
| 010 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 011 | passed | PASS | PASS | PASS | certified, both legs clean |
| 012 | passed | PASS | PASS | PASS | certified, both legs clean |
| 013 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 014 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 015 | passed | PASS | FAIL | FAIL | certified (legs FAIL under adjudication) |
| 016 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 017 | passed | PASS | FAIL | FAIL | certified (legs FAIL under adjudication) |
| 018 | passed | PASS | FAIL | FAIL | certified (legs FAIL under adjudication) |
| 019 | passed | PASS | PASS | PASS | certified, both legs clean |
| 020 | passed | PASS | PASS | PASS | certified, both legs clean |
| 021 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 022 | passed | PASS | FAIL | FAIL | certified (legs FAIL under adjudication) |
| 023 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 024 | passed | PASS | PASS | PASS | certified, both legs clean |
| 025 | **building** | **(blank)** | **FAIL** (k17z3 08:31Z) | **FAIL** (k17z3 08:32Z) | **OPEN** |
| 026 | passed | PASS | PASS | PASS | certified, both legs clean |
| 027 | passed | PASS | PASS | PASS | certified, both legs clean |
| 028 | passed | PASS | PASS | PASS | certified, both legs clean |
| 029 | passed | PASS | PASS | PASS | certified, both legs clean |
| 030 | passed | PASS | PASS | PASS | certified, both legs clean |
| 031 | passed | PASS | FAIL | FAIL | certified (legs FAIL under adjudication) |
| 032 | passed | PASS | PASS | PASS | certified, both legs clean |
| 033 | passed | PASS | PASS | PASS | certified, both legs clean |
| 034 | passed | PASS | PASS | PASS | certified, both legs clean |
| 035 | passed | PASS | PASS | PASS | certified, both legs clean |
| 036 | passed | PASS | FAIL | FAIL | certified (legs FAIL under adjudication) |
| 037 | passed | PASS | FAIL | FAIL | certified (legs FAIL under adjudication) |
| 038 | passed | PASS | PASS | PASS | certified, both legs clean |
| 039 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 040 | passed | PASS | PASS | PASS | certified, both legs clean |
| 041 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 042 | passed | PASS | FAIL | (no clean leg) | certified (FULL leg FAIL under adjudication) |
| 043 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 044 | passed | PASS | PASS | PASS | certified, both legs clean |
| 045 | passed | PASS | PASS | PASS | certified, both legs clean |
| 046 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 047 | passed | PASS | FAIL | FAIL | certified (legs FAIL under adjudication) |
| 048 | passed | PASS | FAIL | FAIL | certified (legs FAIL under adjudication) |
| 049 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 050 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |
| 051 | passed | PASS | FAIL | PASS | certified (FULL leg FAIL under adjudication) |

Census totals (newest clean, 08:46:53Z): FULL PASS 30 / FAIL 21;
CROP PASS 37 / FAIL 13 / missing 1 (slide 042); **both legs clean = 22 slides**;
29 slides not both-clean (many carry banked PIL dismissals per REJUDGE_REGISTER —
census-only, not a re-open order; r34 08:20Z snapshot: FULL 28/23, CROP 39/12,
both-clean 22, open list 29).

## 3. Rejudge wave summary (2026-10-27 wave, state 2026-10-31)

- Register: `$RJ/REJUDGE_REGISTER.md` (append-only, 577 KB + many `.bak*` kept);
  consolidated snapshots `REJUDGE_SUMMARY_r31..r34.md` (r34 @ 08:20:37Z).
- Mandate: fresh vision reads over all certified slides; each slide needs BOTH a
  clean FULL (full-slide vs original frame) and a clean CROP (zoomed densest-region
  crop-pair) leg; FAILs PIL-adjudicated before reopening. Payloads byte-for-byte
  from `shared_patterns/judge_protocol_03.md`; drivers `rejudge_driver.sh` /
  `rejudge_slide.sh`; adjudicator `rejudge_adjudicate.py`.
- `VERDICT_CENSUS_r1.md` absent → FULL/CROP clean counts computed in §2 above
  (method: newest-mtime verdict transcript per slide dir, excluding
  `.bak/.bank/.log/.out/_bak/.clean/.stale` files and any transcript containing
  error-style 429 lines).
- Fleet census r1 (08:35:11Z, `fleet_census_r1.md`): 57 slide dirs under RJ,
  4073 files, 1796 with FINAL VERDICT; verdict lines all-time PASS 3770 / FAIL 1627;
  6 dirs (slide03, slide05, slide10, slide12, slide13, slide17 — alternate naming)
  had no verdict transcript yet. Gateway pressure LOW at the frontier: 0 HTTP-429 /
  rate-limit lines in the newest 30 files (all-time: HTTP 429 = 20,
  upstream_rate_limited = 18). Processes at census: ~404 `vision_leg.sh`,
  ~705 `analyze_image`, 10 `soffice`. Disk: 88% full, 3.8G avail on /home/codespace.
- Sweep r35 (08:32–08:36Z, read-only, `sweep_r35.md`): confirms DB 50/51, slide 25
  the only non-passed row; no clean PASS transcript for slide 25 exists
  (newest completed k17z3 FULL 08:31 + CROP 08:32 both FAIL, zero 429s; k17z2
  FULL/CROP and bl_labels_leg still in flight at sweep time).

## 4. OMML / equation summary

- Equations rendered professional-2D per the math rule: matplotlib mathtext →
  600 dpi transparent PNG → `addImage` at exact px/600 in; OMML wrap post-
  certification via `scripts/18_omml_wrapper.py` (v2 PowerPoint-authored pattern),
  rel ids re-derived from the CURRENT pptx. 180 `eq_*.json` sidecars in
  `recreated_pptx/build/assets/`; 15 slides carry equation images
  (004, 005, 009, 015, 021, 023, 030, 031, 032, 036, 037, 044, 048, 050, 051).
- Wrap run 2026-10-31 (`$RJ/OMML_WRAP_LOG.md`): wrapped+replaced 004 (1 block),
  005 (8), 015 (1), 021 (5), 030 (2) — subset manifests where the full manifest
  fail-louds on unsupported mathtext (`\underline`, `\mathbf{\hat{Y}}`); remaining
  pics stay as plain PNG embeds (idempotent). Already-wrapped 009/036/039 untouched;
  slide 25 untouched. Pre-OMML backups at `$RJ/slideNNN/*.preOMML.bak.pptx`;
  wrap proven pixel-identical (0 px vs preOMML backup / banked pdf).
- Verified directly from the 51 current pptx files (zip scan of
  `ppt/slides/slide1.xml`): **8 slides wrapped — 004, 005, 009, 015, 021, 030, 036,
  039 — 42 `mc:AlternateContent` blocks, 63 `m:oMath` occurrences total**.

## 5. Graph summary (advanced-graph rule)

Generated-image graphs embedded in the single-version pptx (matplotlib via
build-chain scripts in `recreated_pptx/build/`):

- **025** — 4 surface plots `plot_025_{tl,tr,bl,br}.png` (300 dpi, exact measured
  geometry), generators `generate_plots_025*.py` (k4…k17m series). This is the OPEN
  slide — see §7.
- **033** — `slide_033_plot_v7.png` embedded in `slide_033.js`.
- **034** — `slide_034_plot.png` via `gen_plot_034.py`, embedded in `slide_034.js`.
- **046** — scatter `plot_046_scatter.png` via `generate_plot_046.py` +
  `m046_*` matrix/vector JSON assets, embedded in `slide_046.js`.

## 6. Final deck + merge gate — **PENDING**

Ledger `recreated_pptx/final_deck_state.json` (measured 2026-10-31 ~08:46Z):

- Deck: `03_ridger_regression_gradient_descent_final.pptx`; `total_pages` = 51;
  all 51 page entries `status=certified`; 197 events (last: `update-page` 51 @
  2026-10-31T08:26:31); scope `S21_continuous_final_deck (run 299640)`; doctrine
  continuous final deck (founder directive 2026-10-25).
- `deck_md5` = `872284b7f41336fddf39b84ef5ddc63e` — **matches the on-disk md5**.
- `render_check` census: **PASS 4 (pages 14, 19, 33, 50), FAIL 46, PENDING 1
  (page 51)**. Ledger `source_md5` stale vs disk on 4 pages (4, 10, 13, 25) per
  sweep_r35 §5 (page 25 disk file IS the canonical `c50e78bf…`).
- Latest full-gate attempts (`deck_gate_r25.txt`, 08:09–08:41Z): attempts 1–3 died
  on `soffice` exit 1 (shared LO profile `s21_lo_profile_299640` contended by the
  ~400-wrapper rejudge fleet), attempt 4 on a missing module, attempt 5 in flight
  at last read. Individual page gates passing piecemeal (p14/p19/p33/p50 PASS).
- **Merge-gate verdict: PENDING until 51/51 pages show render_check PASS in a
  single full-deck gate, followed by a restage** (re-run the full 51-page gate on
  an uncontended/private LO profile, refresh the ledger `source_md5` entries for
  pages 4/10/13/25, and re-record `deck_md5`).

## 7. Open items

- **Slide 25 — OPEN.** Title "Types of Loss function shapes".
  DB: `gen_status=building`, `visual_check=''`, `visual_attempts=4`,
  `last_error`: "rejudge 2026-10-27 wave: FULL=FAIL CROP=FAIL, PIL-confirmed
  TR/BR surface fidelity gap; deck page gate FAIL — fix in progress (agent-180)".
  Transcript state (sweep_r35 §4): newest completed k17z3 FULL (08:31Z) and CROP
  (08:32Z) both **FAIL**, zero 429s; k17z2 FULL/CROP and `bl_labels_leg` legs were
  still in flight at 08:36Z; **no clean PASS exists for slide 25**. FAIL reasons:
  bottom-left "Non-Convex" panel "Local Maxima" clipped, leader-line collision,
  "Global Maxima" mislabeled, foreign base strip at foot of bottom-right plot;
  crop leg additionally wrong render type, missing z-axis/labels/contour
  projection, probable value inversion. On-disk `slide_025_recreated.pptx` =
  canonical md5 `c50e78bf39531523dcf69d652254b647` but under active CLOBBER
  (CLOBBER_WATCH logging repeated clobber events with swapped plot md5s); ledger
  `source_md5` for page 25 is stale. Fix path: complete the in-flight legs, PIL-
  adjudicate, rebuild the TR/BR surfaces, re-judge FULL+CROP clean, then write
  `passed`/`PASS` and restage the deck.

## 8. Evidence locations

- This draft + rejudge wave: `$RJ/` — `REJUDGE_REGISTER.md` (+ `.bak*`),
  `REJUDGE_SUMMARY_r31..r34.md`, `OMML_WRAP_LOG.md`, `OMML_INVENTORY_r1/r2.md`,
  `OMML_WRAP_PLAN_r3.md`, `sweep_r35.md`, `fleet_census_r1.md`, `deck_gate_r21..r25.txt`,
  `deck_updates_r22/r25.txt`, per-slide dirs `slide001..slide051` (+ alternate-named
  `slide03/05/10/12/13/17/...`), driver scripts and payloads.
- Per-slide QA: `recreated_pptx/qa/slideNNN/` and `qa/slide_0NN/`.
- Final-deck gates: `recreated_pptx/qa/final_deck_updates/gate_*/gate_report.txt`;
  ledger `recreated_pptx/final_deck_state.json`; build chain `recreated_pptx/build/`
  (per-slide scripts, `components/` for dependency edges 10>9, 13>12, 17>13, 18>17,
  `assets/` eq + plot PNGs/JSONs, `final_deck/` tooling).
- Namespace root: `CLOSEOUT_REPORT.md` (existing skeleton — NOT modified by this
  draft), `AGENTS.md`, `HANDOFF.md`, `CONTINUATION_PROMPT.md`, `SOURCES_MAP.md`,
  `slides_progress.db`; `sources/slide_NNN_source/SOURCES.md` (51/51 web-research
  records per the 2026-10-19 mandate); `analysis/` (raw+final JSONs).
- Laws: never git, never delete banked evidence; qa/ + scratch/ untracked by
  convention.
