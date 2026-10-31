# REJUDGE_SUMMARY_r34 — consolidated state snapshot 2026-10-31T08:20:37Z

Fresh background consolidation worker. Read-only w.r.t. DB/deck/builds/pptx; no git; no vision
launches; no evidence deleted. Register `REJUDGE_REGISTER.md` untouched except one appended
pointer line. Scan method: same as r33 — per `slide001..slide051` under this dir, newest-mtime
`judge_full*.txt` / `crop_dense_judge*.txt` containing `FINAL VERDICT` (markdown-bold tolerated)
with zero `429` lines; `*.bak`/`*.bank`/`*.log`/`*.out`/`_bak*`/`.clean*`/`.stale*`/`.preW02*`/
`.W02bank*` excluded (script `scratch/tmp/r34_scan.py`, output `r34_scan.json`). All leg times
UTC 2026-10-31. Live rejudge/fix workers are still rewriting transcripts (e.g. 015/021/032/041
legs landed 08:11–08:14Z, 025 k17z3 full landed 08:16:11Z), so "newest clean" is as-of the scan
~08:17Z.

## 1. DB state — `videos/machine-learning/03_ridger_regression_gradient_descent/slides_progress.db` (read-only)

- `SELECT COUNT(*) FROM slides;` → **51**; `SELECT COUNT(*) FROM slides WHERE gen_status='passed' AND visual_check='PASS';` → **50**
- Open (non-passing) rows: exactly one —
  - **slide_id 25** | title `Types of Loss function shapes` | gen_status=`building` |
    visual_check='' | visual_attempts=4 | worker_id=`S27_019_025` | updated_at=2026-10-26T16:44:42 |
    last_error: `rejudge 2026-10-27 wave: FULL=FAIL CROP=FAIL, PIL-confirmed TR/BR surface
    fidelity gap; deck page gate FAIL — fix in progress (agent-180)`

## 2. Per-slide newest clean FULL + CROP verdicts, slides 001–051 (as of 2026-10-31 ~08:17Z)

Census: FULL PASS=28 / FAIL=23 / missing=0; CROP PASS=39 / FAIL=12 / missing=0.

| slide | newest clean FULL | newest clean CROP |
|---|---|---|
| 001 | FAIL `judge_full_r18.txt` 07:21:08 | PASS `crop_dense_judge_r16.txt` 07:28:11 |
| 002 | FAIL `judge_full_r19.txt` 06:08:41 | PASS `crop_dense_judge_r15_r22.txt` 08:12:43 |
| 003 | FAIL `judge_full_r17.txt` 05:26:21 | FAIL `crop_dense_judge.txt` 06:18:02 |
| 004 | PASS `judge_full_r15.txt` 05:42:50 | PASS `crop_dense_judge_r15.txt` 06:36:00 |
| 005 | PASS `judge_full_r16.txt` 07:02:40 | PASS `crop_dense_judge_r19.txt` 06:59:58 |
| 006 | FAIL `judge_full_r15_r22.txt` 07:33:17 | PASS `crop_dense_judge_r17.txt` 05:30:47 |
| 007 | PASS `judge_full_r19.txt` 08:06:28 | PASS `crop_dense_judge_r18.txt` 06:20:43 |
| 008 | PASS `judge_full_r20.txt` 06:57:54 | FAIL `crop_dense_judge_r19.txt` 07:20:46 |
| 009 | PASS `judge_full_r20.txt` 06:11:33 | PASS `crop_dense_judge_r20.txt` 08:04:42 |
| 010 | FAIL `judge_full_r17.txt` 07:17:34 | PASS `crop_dense_judge_r21.txt` 07:03:21 |
| 011 | PASS `judge_full_r16.txt` 06:53:45 | PASS `crop_dense_judge_r15.txt` 06:21:21 |
| 012 | FAIL `judge_full.txt` 01:10:48 | PASS `crop_dense_judge.txt` 04:32:11 |
| 013 | FAIL `judge_full_r18.txt` 06:34:39 | PASS `crop_dense_judge_r20.txt` 07:32:07 |
| 014 | FAIL `judge_full_fix2.txt` 07:08:42 | PASS `crop_dense_judge_fix3.txt` 06:38:51 |
| 015 | FAIL `judge_full_r19.txt` 08:13:22 | FAIL `crop_dense_judge_r20.txt` 06:11:35 |
| 016 | FAIL `judge_full_r21.txt` 07:38:20 | PASS `crop_dense_judge_r17.txt` 06:35:59 |
| 017 | PASS `judge_full_r19.txt` 06:47:16 | FAIL `crop_dense_judge_r15.txt` 07:51:53 |
| 018 | PASS `judge_full_r19.txt` 07:22:11 | FAIL `crop_dense_judge_r20.txt` 07:06:58 |
| 019 | PASS `judge_full_wfix.txt` 06:51:15 | PASS `crop_dense_judge_wfix.txt` 06:47:33 |
| 020 | PASS `judge_full_r21.txt` 07:27:31 | PASS `crop_dense_judge_r20.txt` 07:35:21 |
| 021 | PASS `judge_full_r18.txt` 06:31:55 | PASS `crop_dense_judge_r21.txt` 08:13:40 |
| 022 | FAIL `judge_full_r20.txt` 06:17:11 | FAIL `crop_dense_judge_r17.txt` 05:19:17 |
| 023 | PASS `judge_full_r20.txt` 06:21:12 | PASS `crop_dense_judge_r16.txt` 05:27:02 |
| 024 | PASS `judge_full_r19_r22.txt` 08:04:44 | PASS `crop_dense_judge_r16.txt` 05:33:13 |
| 025 | FAIL `judge_full_k17z3.txt` 08:16:11 | PASS `crop_dense_judge_k17n.txt` 08:03:16 |
| 026 | FAIL `judge_full_r16.txt` 06:18:04 | PASS `crop_dense_judge_r21.txt` 06:53:57 |
| 027 | PASS `judge_full_r16.txt` 06:16:05 | PASS `crop_dense_judge_r16.txt` 05:22:54 |
| 028 | PASS `judge_full_r16.txt` 06:05:37 | PASS `crop_dense_judge_r20.txt` 07:03:32 |
| 029 | PASS `judge_full_r20.txt` 07:47:20 | PASS `crop_dense_judge_r17.txt` 06:11:19 |
| 030 | PASS `judge_full_r17.txt` 06:57:15 | PASS `crop_dense_judge_w03.txt` 06:30:31 |
| 031 | PASS `judge_full_r19.txt` 07:08:41 | FAIL `crop_dense_judge_r17.txt` 07:02:04 |
| 032 | PASS `judge_full_r21.txt` 08:14:16 | PASS `crop_dense_judge_w03.txt` 05:35:15 |
| 033 | PASS `judge_full_w03.txt` 07:29:53 | PASS `crop_dense_judge_fresh.txt` 04:03:52 |
| 034 | PASS `judge_full_r19.txt` 07:17:47 | PASS `crop_dense_judge_w03.txt` 06:36:16 |
| 035 | PASS `judge_full_r16.txt` 07:41:39 | PASS `crop_dense_judge_r19.txt` 06:05:16 |
| 036 | PASS `judge_full_fresh.txt` 08:11:24 | FAIL `crop_dense_judge_r17.txt` 06:29:52 |
| 037 | FAIL `judge_full_r20.txt` 06:01:08 | FAIL `crop_dense_judge_fresh3_r22.txt` 08:10:47 |
| 038 | PASS `judge_full_r20.txt` 06:10:57 | PASS `crop_dense_judge_r21.txt` 07:26:55 |
| 039 | PASS `judge_full.txt` 02:45:27 | PASS `crop_dense_judge_r17.txt` 07:09:36 |
| 040 | PASS `judge_full_r17.txt` 06:24:29 | PASS `crop_dense_judge_fresh3.txt` 06:40:34 |
| 041 | FAIL `judge_full_r17.txt` 08:03:44 | PASS `crop_dense_judge_r20.txt` 08:11:24 |
| 042 | PASS `judge_full_r20.txt` 06:48:21 | PASS `crop_dense_judge.txt` 02:07:56 |
| 043 | FAIL `judge_full_r20.txt` 07:11:26 | PASS `crop_dense_judge_r16.txt` 06:44:14 |
| 044 | FAIL `judge_full_r18.txt` 06:45:47 | PASS `crop_dense_judge_r16.txt` 06:05:19 |
| 045 | FAIL `judge_full_r19.txt` 07:16:21 | FAIL `crop_dense_judge.txt` 08:11:49 |
| 046 | FAIL `judge_full_fresh2.txt` 05:02:02 | PASS `crop_dense_judge_r22.txt` 07:21:19 |
| 047 | PASS `judge_full_r18.txt` 06:46:43 | FAIL `crop_dense_judge_r21.txt` 08:09:29 |
| 048 | FAIL `judge_full_r20.txt` 07:25:30 | FAIL `crop_dense_judge_r18.txt` 07:46:48 |
| 049 | FAIL `judge_full_r16.txt` 06:26:22 | PASS `crop_dense_judge_r22.txt` 06:38:32 |
| 050 | FAIL `judge_full_r20.txt` 07:24:38 | PASS `crop_dense_judge_fresh3.txt` 07:31:33 |
| 051 | FAIL `judge_full_w2.txt` 05:45:01 | PASS `crop_dense_judge_w2.txt` 06:40:12 |

**OPEN list (newest clean leg FAIL on FULL and/or CROP, or DB-open) — 29 slides:**
001, 002, 003, 006, 008, 010, 012, 013, 014, 015, 016, 017, 018, 022, **025** (also the only
DB-open row), 026, 031, 036, 037, 041, 043, 044, 045, 046, 047, 048, 049, 050, 051.
FULL-FAIL-only (17): 001, 002, 006, 010, 012, 013, 014, 016, 025, 026, 041, 043, 044, 046, 049,
050, 051.
CROP-FAIL-only (6): 008, 017, 018, 031, 036, 047.
Both legs FAIL (6): 003, 015, 022, 037, 045, 048.
Fully clean (PASS/PASS): 22 slides — 004, 005, 007, 009, 011, 019, 020, 021, 023, 024, 027,
028, 029, 030, 032, 033, 034, 035, 038, 039, 040, 042.
Changes vs r33 (08:05Z): 007 full r20→r19 PASS; 008 full r20→PASS; 012 full fresh→`judge_full.txt`
FAIL; 015 full fresh3→r19 FAIL; 016 full fresh→r21 FAIL; 024 full→r19_r22 PASS; 032 full→r21 PASS;
036 full→fresh PASS; 037 crop→fresh3_r22 FAIL; 041 crop r19→r20 PASS; 045 crop→`crop_dense_judge.txt`
FAIL; 047 crop→r21 FAIL; 025 full k17d→k17z3 FAIL. Per register rulings many FAIL legs carry banked
PIL dismissals (see r31 §2 and the register); this table is census-only, not a re-open order.

## 3. Slide 025 special section

- Current `recreated_pptx/slide_025_recreated.pptx` md5 at 2026-10-31T08:20:37Z:
  **`c50e78bf39531523dcf69d652254b647`**, mtime 2026-10-31 07:37:06Z, size 1169724 — this is
  the monitor's expected "canonical" deck md5, but the file is under ACTIVE CLOBBER: the
  CLOBBER_WATCH log shows repeated CLOBBER EVENTs (08:18:51Z observed `e85d834b…` with swapped
  tl/tr/bl/br asset md5s vs canonical), and direct reads churned 07:58→08:20Z
  (`5479c739…` → `1809b318…` → `cd4582ba…` → `e2bf0bd4…` → `6dda603c…` → `96238948…` →
  `c9b56a09…` → `6f70c13c…` → `d1cf0b09…` → `c50e78bf…` → `e85d834b…` → back to `c50e78bf…`).
- Build assets `recreated_pptx/build/assets/plot_025_{tl,tr,bl,br}.png` md5s at 08:11Z —
  tl `cd62022fbf0cfe30a351309c0230adb3`, tr `b45c723af19e2cf11659109d63134cad`,
  bl `7a8e7210f118b728245d268552a7d32d`, br `f6af102ec110ff5113482659ff4f9d73`
  (identical to the pre-k17z bank copies in `slide025/assets_bank_pre_k17z_build_assets/` except
  tl: bank has `a98e8eaf…` — tl was rebuilt during the k17 series).
- k17z2 leg states at scan time:
  - Transcripts `judge_full_k17z2.txt` / `crop_dense_judge_k17z2.txt` still DO NOT EXIST at
    08:18Z (only 0-byte `*.txt.log` + 0-byte `.wrapper.out` from 07:45–07:52Z); therefore
    FINAL VERDICT: none, 429 count: 0 (nothing written). The original k17z2 wrapper pids
    (2349588/2349594) are dead, but their `16_vision_gate.sh` children (2380449/2380450 full,
    2384938/2384939 crop, started 07:45–07:46Z) were STILL RUNNING at 08:11Z against
    `render_k17z2.png` / `crop_dense_{render,orig}_k17z2.png`.
  - `leg_full_k17z2.pid` / `leg_crop_k17z2.pid` files now hold NEW pids (2540836 / 2540837),
    both alive at 08:17Z — re-pointed at a fresh wrapper generation; `MONITOR_k17z2.log` still
    shows both legs `pending size=missing` through 08:18:47Z.
- k17z3 leg states: `judge_full_k17z3.txt` EXISTS (5120 bytes, mtime 08:16:11Z) — clean
  (0 `429` lines), **FINAL VERDICT: FAIL**. `crop_dense_judge_k17z3.txt` still MISSING at 08:18Z.
  Wrapper pids per pid files: `leg_full_k17z3.pid`=2544510, `leg_crop_k17z3.pid`=2544511, both
  alive at 08:17Z (multiple `vision_leg.sh` k17z3 processes for both legs visible in ps).
  - Newest clean 025 legs in the census above: FULL FAIL `judge_full_k17z3.txt` 08:16:11,
    CROP PASS `crop_dense_judge_k17n.txt` 08:03:16.
- CLOBBER_WATCH (pid 2488910, alive) actively logging; suspect-process list empty at last event.

## 4. Deck ledger — `recreated_pptx/final_deck_state.json` (read-only) + on-disk md5 comparison

- `total_pages`: 51; page entries: 51; page `status` census: **certified 51/51**.
- `render_check` census: **FAIL 47, PASS 4 (pages 14, 19, 33, 51), PENDING 0**. Latest events:
  render-check [33,50,51] PASS @ 08:11:58Z (0 px differ); [41..50] FAIL @ 08:14:21Z (mismatched
  [46, 49]); [31..40] FAIL @ 08:05:19Z (mismatched [36, 37]); [14,19,33,51] PASS @ 08:02:56Z.
- `deck_md5` ledger `e55b0ba6153d34006e679739ac4fadb6` == on-disk md5 of
  `03_ridger_regression_gradient_descent_final.pptx` — **MATCH** (deck bytes match the ledger).
- `source_md5` mismatches vs on-disk per-slide pptx: **3** —
  - page 4: ledger `761bcac7…` vs disk `4d21712f…` (`slide_004_recreated.pptx`)
  - page 10: ledger `9b4ee43a…` vs disk `67b341ef…` (`slide_010_recreated.pptx`)
  - page 25: ledger `8a355c24…` vs disk churning (at 08:16Z `d1cf0b09…`; at 08:20:37Z `c50e78bf…`)

## 5. Live wrappers

- `pgrep -fc vision_leg.sh` at 2026-10-31T08:20:37Z → **479** live wrapper processes
  (fleet-wide; was 487 at r33 08:05:56Z, 477 at 08:17:17Z — the slide-25 k17z2/k17z3 fix storm
  is still running).

## 6. Cron note

- `crontab -l` (2026-10-31 ~08:17Z) holds only two `*/15` monitor/watchdog entries for OTHER
  namespaces (`videos/machine-learning/08_performance_measure/pool_run/monitor.sh`,
  `videos/machine-learning/10_nn_training_and_example/_pool/watchdog.sh`) — **no cron entries
  for this 03 namespace**; the rejudge_20261027 drivers run as live background processes, not cron.
  (Session CronList unavailable to background workers; system crontab read directly.)

## Files changed this spawn

- Created this file `REJUDGE_SUMMARY_r34.md`; appended one dated pointer line to
  `REJUDGE_REGISTER.md` (append-only).
- Scratch only: `scratch/tmp/r34_scan.py`, `scratch/tmp/r34_scan.json` (project scratch, untracked).
- No git operations; no vision legs launched; no evidence deleted; no build/pptx/DB/deck files modified.
