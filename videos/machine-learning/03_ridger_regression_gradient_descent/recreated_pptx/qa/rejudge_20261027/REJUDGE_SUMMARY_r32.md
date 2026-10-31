# REJUDGE_SUMMARY_r32 — consolidated state snapshot 2026-10-31T07:57:39Z

Fresh background consolidation worker. Read-only w.r.t. DB/deck/builds/pptx; no git; no vision
launches; no evidence deleted. Register `REJUDGE_REGISTER.md` touched only by one appended
pointer line. Scan method (same as r31): per `rejudge_20261027/slide001..slide051`, newest-mtime
`judge_full*.txt` / `crop_dense_judge*.txt` containing `FINAL VERDICT` (markdown-bold tolerated)
with zero `429` lines; `*.bak`/`*.bank`/`*.log`/`*.out`/`_bak*`/`.clean*` excluded. A slide is
**OPEN** when either leg is missing or its newest clean verdict is FAIL. All leg times UTC 2026-10-31.

## 1. DB state — `videos/machine-learning/03_ridger_regression_gradient_descent/slides_progress.db` (read-only)

- `SELECT slide_id,gen_status,visual_check FROM slides WHERE gen_status!='passed' OR visual_check!='PASS';`
  → exactly one row: **slide 25** | gen_status=`building` | visual_check=`''`
- Count `gen_status='passed' AND visual_check='PASS'` → **50** of 51 total rows
  (census: `passed|PASS`=50, `building|''`=1).

## 2. Per-slide newest clean FULL/CROP — all 51 slides

FULL census: PASS=30 / FAIL=21 / missing=0. CROP census: PASS=40 / FAIL=11 / missing=0.
**OPEN count: 27** (list at end of table).

| slide | newest clean FULL (file, verdict, HH:MM:SS) | newest clean CROP (file, verdict, HH:MM:SS) | |
|---|---|---|---|
| 001 | `judge_full_r18.txt` FAIL 07:21:08 | `crop_dense_judge_r16.txt` PASS 07:28:11 | **OPEN**
| 002 | `judge_full_r19.txt` FAIL 06:08:41 | `crop_dense_judge_r16.txt` PASS 05:04:45 | **OPEN**
| 003 | `judge_full_r17.txt` FAIL 05:26:21 | `crop_dense_judge.txt` FAIL 06:18:02 | **OPEN**
| 004 | `judge_full_r15.txt` PASS 05:42:50 | `crop_dense_judge_r15.txt` PASS 06:36:00 |
| 005 | `judge_full_r16.txt` PASS 07:02:40 | `crop_dense_judge_r19.txt` PASS 06:59:58 |
| 006 | `judge_full_r15_r22.txt` FAIL 07:33:17 | `crop_dense_judge_r17.txt` PASS 05:30:47 | **OPEN**
| 007 | `judge_full_r17.txt` PASS 06:23:51 | `crop_dense_judge_r18.txt` PASS 06:20:43 |
| 008 | `judge_full_r20.txt` PASS 06:57:54 | `crop_dense_judge_r19.txt` FAIL 07:20:46 | **OPEN**
| 009 | `judge_full_r20.txt` PASS 06:11:33 | `crop_dense_judge_r21.txt` PASS 07:01:22 |
| 010 | `judge_full_r17.txt` FAIL 07:17:34 | `crop_dense_judge_r21.txt` PASS 07:03:21 | **OPEN**
| 011 | `judge_full_r16.txt` PASS 06:53:45 | `crop_dense_judge_r15.txt` PASS 06:21:21 |
| 012 | `judge_full_fresh.txt` PASS 04:11:08 | `crop_dense_judge.txt` PASS 04:32:11 |
| 013 | `judge_full_r18.txt` FAIL 06:34:39 | `crop_dense_judge_r20.txt` PASS 07:32:07 | **OPEN**
| 014 | `judge_full_fix2.txt` FAIL 07:08:42 | `crop_dense_judge_fix3.txt` PASS 06:38:51 | **OPEN**
| 015 | `judge_full_fresh3.txt` FAIL 05:25:35 | `crop_dense_judge_r20.txt` FAIL 06:11:35 | **OPEN**
| 016 | `judge_full_fresh.txt` FAIL 07:56:03 | `crop_dense_judge_r17.txt` PASS 06:35:59 | **OPEN**
| 017 | `judge_full_r19.txt` PASS 06:47:16 | `crop_dense_judge_r15.txt` FAIL 07:51:53 | **OPEN**
| 018 | `judge_full_r19.txt` PASS 07:22:11 | `crop_dense_judge_r20.txt` FAIL 07:06:58 | **OPEN**
| 019 | `judge_full_wfix.txt` PASS 06:51:15 | `crop_dense_judge_wfix.txt` PASS 06:47:33 |
| 020 | `judge_full_r21.txt` PASS 07:27:31 | `crop_dense_judge_r20.txt` PASS 07:35:21 |
| 021 | `judge_full_r18.txt` PASS 06:31:55 | `crop_dense_judge_r16.txt` PASS 05:35:48 |
| 022 | `judge_full_r20.txt` FAIL 06:17:11 | `crop_dense_judge_r17.txt` FAIL 05:19:17 | **OPEN**
| 023 | `judge_full_r20.txt` PASS 06:21:12 | `crop_dense_judge_r16.txt` PASS 05:27:02 |
| 024 | `judge_full_r19.txt` PASS 06:45:41 | `crop_dense_judge_r16.txt` PASS 05:33:13 |
| 025 | `judge_full_k17d.txt` FAIL 07:39:06 | `crop_dense_judge_k17d.txt` FAIL 07:38:42 | **OPEN**
| 026 | `judge_full_r16.txt` FAIL 06:18:04 | `crop_dense_judge_r21.txt` PASS 06:53:57 | **OPEN**
| 027 | `judge_full_r16.txt` PASS 06:16:05 | `crop_dense_judge_r16.txt` PASS 05:22:54 |
| 028 | `judge_full_r16.txt` PASS 06:05:37 | `crop_dense_judge_r20.txt` PASS 07:03:32 |
| 029 | `judge_full_r20.txt` PASS 07:47:20 | `crop_dense_judge_r17.txt` PASS 06:11:19 |
| 030 | `judge_full_r17.txt` PASS 06:57:15 | `crop_dense_judge_w03.txt` PASS 06:30:31 |
| 031 | `judge_full_r19.txt` PASS 07:08:41 | `crop_dense_judge_r17.txt` FAIL 07:02:04 | **OPEN**
| 032 | `judge_full_r17.txt` PASS 06:59:26 | `crop_dense_judge_w03.txt` PASS 05:35:15 |
| 033 | `judge_full_w03.txt` PASS 07:29:53 | `crop_dense_judge_fresh.txt` PASS 04:03:52 |
| 034 | `judge_full_r19.txt` PASS 07:17:47 | `crop_dense_judge_w03.txt` PASS 06:36:16 |
| 035 | `judge_full_r16.txt` PASS 07:41:39 | `crop_dense_judge_r19.txt` PASS 06:05:16 |
| 036 | `judge_full_r21.txt` PASS 07:29:56 | `crop_dense_judge_r17.txt` FAIL 06:29:52 | **OPEN**
| 037 | `judge_full_r20.txt` FAIL 06:01:08 | `crop_dense_judge_r16.txt` PASS 07:47:22 | **OPEN**
| 038 | `judge_full_r20.txt` PASS 06:10:57 | `crop_dense_judge_r21.txt` PASS 07:26:55 |
| 039 | `judge_full.txt` PASS 02:45:27 | `crop_dense_judge_r17.txt` PASS 07:09:36 |
| 040 | `judge_full_r17.txt` PASS 06:24:29 | `crop_dense_judge_fresh3.txt` PASS 06:40:34 |
| 041 | `judge_full_r21.txt` PASS 07:32:27 | `crop_dense_judge_r19.txt` FAIL 06:58:10 | **OPEN**
| 042 | `judge_full_r20.txt` PASS 06:48:21 | `crop_dense_judge.txt` PASS 02:07:56 |
| 043 | `judge_full_r20.txt` FAIL 07:11:26 | `crop_dense_judge_r16.txt` PASS 06:44:14 | **OPEN**
| 044 | `judge_full_r18.txt` FAIL 06:45:47 | `crop_dense_judge_r16.txt` PASS 06:05:19 | **OPEN**
| 045 | `judge_full_r19.txt` FAIL 07:16:21 | `crop_dense_judge_fresh3.txt` PASS 07:31:15 | **OPEN**
| 046 | `judge_full_fresh2.txt` FAIL 05:02:02 | `crop_dense_judge_r22.txt` PASS 07:21:19 | **OPEN**
| 047 | `judge_full_r18.txt` PASS 06:46:43 | `crop_dense_judge_fresh2.txt` PASS 03:25:22 |
| 048 | `judge_full_r20.txt` FAIL 07:25:30 | `crop_dense_judge_r18.txt` FAIL 07:46:48 | **OPEN**
| 049 | `judge_full_r16.txt` FAIL 06:26:22 | `crop_dense_judge_r22.txt` PASS 06:38:32 | **OPEN**
| 050 | `judge_full_r20.txt` FAIL 07:24:38 | `crop_dense_judge_fresh3.txt` PASS 07:31:33 | **OPEN**
| 051 | `judge_full_w2.txt` FAIL 05:45:01 | `crop_dense_judge_w2.txt` PASS 06:40:12 | **OPEN**

## 3. OPEN list (missing leg or newest clean FAIL) — 27 slides

001, 002, 003, 006, 008, 010, 013, 014, 015, 016, 017, 018, 022, 025, 026, 031, 036, 037, 041,
043, 044, 045, 046, 048, 049, 050, 051

Breakdown: FULL-FAIL-open = 001, 002, 003, 006, 010, 013, 014, 015, 016, 022, 025, 026, 043,
044, 045, 046, 048, 049, 050, 051 (21); CROP-FAIL-open = 003, 008, 015, 017, 018, 022, 025, 031,
036, 041, 048 (11). 26 of the 27 OPEN slides are passed-in-DB (re-open debt vs the register's
banked dismissals); slide 025 is the one DB-open row (building/''). Changes vs r31: slide 016's
newest clean FULL moved to `judge_full_fresh.txt` FAIL 07:56:03; slide 017 CROP moved to
`crop_dense_judge_r15.txt` FAIL 07:51:53; slide 037 CROP moved to `crop_dense_judge_r16.txt`
PASS 07:47:22; slide 048 CROP moved to `crop_dense_judge_r18.txt` FAIL 07:46:48; slide 025 FULL/CROP
moved to the k17d legs (`judge_full_k17d.txt` FAIL 07:39:06 / `crop_dense_judge_k17d.txt` FAIL
07:38:42, both 0x429-free, PIL-adjudicated FAIL stands per PROMOTER_R3).

## 4. Deck ledger — `recreated_pptx/final_deck_state.json` (read-only)

- `total_pages`: 51; `pages` dict: 51 entries; every page `status: certified`.
- `render_check` census: **FAIL 47, PENDING 2 (pages 14, 33), PASS 2 (pages 19, 51)**
  → 49 of 51 pages are ledger-mismatch vs a PASS render gate.
- `deck_md5` (ledger) `e55b0ba6153d34006e679739ac4fadb6` == on-disk md5 of
  `03_ridger_regression_gradient_descent_final.pptx` — deck bytes match the ledger.
- `source_md5` mismatches vs on-disk per-slide pptx: **3** — page 4 (ledger `761bcac7…` vs disk
  `4d21712f…`), page 10 (`9b4ee43a…` vs `67b341ef…`), page 25 (`8a355c24…` vs `5479c739…`;
  slide 25 is the DB-open row; disk pptx changed since r31's `e171bd65…`).
- Last ledger events: update-page 19 @07:55:31; update-page 14 @07:55:23; update-page 33
  @07:54:15; render-check p11..p20 FAIL @07:54:53.

## 5. Live wrappers

- `pgrep -fc vision_leg.sh` at 2026-10-31T07:57:39Z → **482** live wrapper processes
  (fleet-wide; up from 464 at r31 07:35:54Z).

## Files changed this spawn

- Created this file `REJUDGE_SUMMARY_r32.md`; appended one dated pointer line to
  `REJUDGE_REGISTER.md` (append-only).
- Scratch only: `scratch/tmp/r32_scan.py`, `scratch/tmp/r32_scan.json`, `scratch/tmp/r32_table.md`
  (project scratch, untracked).
- No git operations; no vision legs launched; no evidence deleted; no build/pptx/DB/deck files modified.
