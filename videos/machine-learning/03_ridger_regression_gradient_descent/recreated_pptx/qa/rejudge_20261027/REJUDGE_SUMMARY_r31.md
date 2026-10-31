# REJUDGE_SUMMARY_r31 — consolidated state snapshot 2026-10-31T07:35:54Z

Fresh background consolidation worker. Read-only w.r.t. DB/deck/builds/pptx; no git; no vision
launches; no evidence deleted. Register `REJUDGE_REGISTER.md` untouched except one appended
pointer line. Scan method: per `slide001..slide051`, newest-mtime `judge_full*.txt` /
`crop_dense_judge*.txt` containing `FINAL VERDICT` (markdown-bold tolerated) with zero `429`
lines; `*.bak`/`*.bank`/`*.log`/`*.out`/`_bak*`/`.clean*` excluded. All leg times UTC 2026-10-31.

## 1. DB state — `videos/machine-learning/03_ridger_regression_gradient_descent/slides_progress.db` (read-only)

- `SELECT COUNT(*) FROM slides WHERE gen_status='passed' AND visual_check='PASS';` → **50**
- Total rows: 51. Group census: `passed|PASS` = 50, `building|''` = 1.
- Open (non-passed) rows: exactly one —
  - **slide 25** | title `Types of Loss function shapes` | gen_status=`building` |
    visual_check='' | visual_attempts=4 | worker_id=`S27_019_025` |
    worker_heartbeat_at=2026-10-26T18:08:31 | updated_at=2026-10-26T16:44:42 |
    last_error: `rejudge 2026-10-27 wave: FULL=FAIL CROP=FAIL, PIL-confirmed TR/BR surface
    fidelity gap; deck page gate FAIL — fix in progress (agent-180)`

## 2. Per-slide newest clean FULL/CROP verdicts — passed-in-DB slides whose legs are FAIL-only or missing (potential re-open debt)

26 of the 50 passed rows have a newest-clean leg that is FAIL (no leg is missing a clean
transcript at scan time):

| slide | newest clean FULL | newest clean CROP |
|---|---|---|
| 001 | FAIL `judge_full_r18.txt` 07:21:08 | PASS `crop_dense_judge_r16.txt` 07:28:11 |
| 002 | FAIL `judge_full_r19.txt` 06:08:41 | PASS `crop_dense_judge_r16.txt` 05:04:45 |
| 003 | FAIL `judge_full_r17.txt` 05:26:21 | FAIL `crop_dense_judge.txt` 06:18:02 |
| 006 | FAIL `judge_full_r15_r22.txt` 07:33:17 | PASS `crop_dense_judge_r17.txt` 05:30:47 |
| 008 | PASS `judge_full_r20.txt` 06:57:54 | FAIL `crop_dense_judge_r19.txt` 07:20:46 |
| 010 | FAIL `judge_full_r17.txt` 07:17:34 | PASS `crop_dense_judge_r21.txt` 07:03:21 |
| 013 | FAIL `judge_full_r18.txt` 06:34:39 | PASS `crop_dense_judge_r20.txt` 07:32:07 |
| 014 | FAIL `judge_full_fix2.txt` 07:08:42 | PASS `crop_dense_judge_fix3.txt` 06:38:51 |
| 015 | FAIL `judge_full_fresh3.txt` 05:25:35 | FAIL `crop_dense_judge_r20.txt` 06:11:35 |
| 016 | FAIL `judge_full.txt` 2026-10-29 23:45:23 | PASS `crop_dense_judge_r17.txt` 06:35:59 |
| 017 | PASS `judge_full_r19.txt` 06:47:16 | FAIL `crop_dense_judge_r17.txt` 06:25:23 |
| 018 | PASS `judge_full_r19.txt` 07:22:11 | FAIL `crop_dense_judge_r20.txt` 07:06:58 |
| 022 | FAIL `judge_full_r20.txt` 06:17:11 | FAIL `crop_dense_judge_r17.txt` 05:19:17 |
| 026 | FAIL `judge_full_r16.txt` 06:18:04 | PASS `crop_dense_judge_r21.txt` 06:53:57 |
| 031 | PASS `judge_full_r19.txt` 07:08:41 | FAIL `crop_dense_judge_r17.txt` 07:02:04 |
| 036 | PASS `judge_full_r21.txt` 07:29:56 | FAIL `crop_dense_judge_r17.txt` 06:29:52 |
| 037 | FAIL `judge_full_r20.txt` 06:01:08 | PASS `crop_dense_judge_fresh3.txt` 06:41:36 |
| 041 | PASS `judge_full_r21.txt` 07:32:27 | FAIL `crop_dense_judge_r19.txt` 06:58:10 |
| 043 | FAIL `judge_full_r20.txt` 07:11:26 | PASS `crop_dense_judge_r16.txt` 06:44:14 |
| 044 | FAIL `judge_full_r18.txt` 06:45:47 | PASS `crop_dense_judge_r16.txt` 06:05:19 |
| 045 | FAIL `judge_full_r19.txt` 07:16:21 | PASS `crop_dense_judge_fresh3.txt` 07:31:15 |
| 046 | FAIL `judge_full_fresh2.txt` 05:02:02 | PASS `crop_dense_judge_r22.txt` 07:21:19 |
| 048 | FAIL `judge_full_r20.txt` 07:25:30 | PASS `crop_dense_judge_r20.txt` 07:04:48 |
| 049 | FAIL `judge_full_r16.txt` 06:26:22 | PASS `crop_dense_judge_r22.txt` 06:38:32 |
| 050 | FAIL `judge_full_r20.txt` 07:24:38 | PASS `crop_dense_judge_fresh3.txt` 07:31:33 |
| 051 | FAIL `judge_full_w2.txt` 05:45:01 | PASS `crop_dense_judge_w2.txt` 06:40:12 |

Census over all 51 slides at scan time: FULL PASS=31 / FAIL=20 / missing=0; CROP PASS=40 /
FAIL=11 / missing=0. Per register rulings many of the FAIL legs above carry banked
dismissals (diffuse/PIL-refuted `adjudicate_*`) — 003, 014, 015, 016, 017, 018, 022, 037,
041, 044, 045, 046, 050, 051 — while 001, 002, 006, 008, 010, 013, 026, 031, 036, 043, 048,
049 are standing-pending (census-only or no banked dismissal). Slide 025 is NOT in this list:
its DB row is not passed (open, see §1); its newest clean legs are FULL PASS
`judge_full_k16.txt` 07:23:46 / CROP FAIL `crop_dense_judge_fresh.txt` 07:22:45.

## 3. Deck ledger — `recreated_pptx/final_deck_state.json` (read-only)

- `total_pages`: 51; page entries: 51; every page `status: certified`.
- `render_check` census: **FAIL 45, PENDING 2 (pages 33, 51), PASS 4 (pages 14, 19, 34, 50)**
  → **47 of 51 pages are ledger-mismatch vs a PASS render gate** (certified status with
  non-PASS render_check).
- `deck_md5` (ledger) `f88417e2eeb3f359bd0455d7e1769397` == on-disk md5 of
  `03_ridger_regression_gradient_descent_final.pptx` — deck bytes match the ledger.
- `source_md5` mismatches vs on-disk per-slide pptx: **3** — page 4
  (ledger `761bcac7…` vs disk `4d21712f…`), page 10 (`9b4ee43a…` vs `67b341ef…`),
  page 25 (`8a355c24…` vs `e171bd65…`; unmerged k16/k17 rebuild — slide 25 is the open row).
- Last ledger events: update-page 51 @07:26:12; render-check p19 PASS @07:27:41;
  render-check p14 PASS @07:28:13.

## 4. Live wrappers

- `pgrep -fc vision_leg.sh` at 2026-10-31T07:35:54Z → **464** live wrapper processes
  (fleet-wide, mostly this rejudge storm; includes parked occ-wait loops).

## Files changed this spawn

- Created this file `REJUDGE_SUMMARY_r31.md`; appended one dated pointer line to
  `REJUDGE_REGISTER.md` (append-only).
- Scratch only: `scratch/tmp/r31_scan.py`, `scratch/tmp/r31_scan.json` (project scratch, untracked).
- No git operations; no vision legs launched; no evidence deleted; no build/pptx/DB/deck files modified.
