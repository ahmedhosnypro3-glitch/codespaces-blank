# REJUDGE_SUMMARY_r33 — consolidated state snapshot 2026-10-31T08:05:56Z

Fresh background consolidation worker. Read-only w.r.t. DB/deck/builds/pptx; no git; no vision
launches; no evidence deleted. Register `REJUDGE_REGISTER.md` untouched except one appended
pointer line. Scan method: per `slide001..slide051` under this dir, newest-mtime
`judge_full*.txt` / `crop_dense_judge*.txt` containing `FINAL VERDICT` (markdown-bold tolerated)
with zero `429` lines; `*.bak`/`*.bank`/`*.log`/`*.out`/`_bak*`/`.clean*`/`.stale*`/`.preW02*`/
`.W02bank*` excluded. All leg times UTC 2026-10-31. NOTE: live rejudge/fix workers were still
rewriting transcripts during the scan (e.g. 007/016/041 full legs landed 07:56–08:03), so
"newest clean" below is as-of the scan timestamp.

## 1. DB state — `videos/machine-learning/03_ridger_regression_gradient_descent/slides_progress.db` (read-only)

- `SELECT COUNT(*) FROM slides WHERE gen_status='passed' AND visual_check='PASS';` → **50** (of 51 rows)
- Open (non-passed) rows: exactly one —
  - **slide 25** | title `Types of Loss function shapes` | gen_status=`building` |
    visual_check='' | visual_attempts=4 | worker_id=`S27_019_025` | updated_at=2026-10-26T16:44:42 |
    last_error: `rejudge 2026-10-27 wave: FULL=FAIL CROP=FAIL, PIL-confirmed TR/BR surface
    fidelity gap; deck page gate FAIL — fix in progress (agent-180)`

## 2. Per-slide newest clean FULL + CROP verdicts, slides 001–051 (as of 2026-10-31 ~08:03Z)

Census: FULL PASS=29 / FAIL=22 / missing=0; CROP PASS=41 / FAIL=10 / missing=0.

| slide | newest clean FULL | newest clean CROP |
|---|---|---|
| 001 | FAIL `judge_full_r18.txt` 07:21:08 | PASS `crop_dense_judge_r16.txt` 07:28:11 |
| 002 | FAIL `judge_full_r19.txt` 06:08:41 | PASS `crop_dense_judge_r16.txt` 05:04:45 |
| 003 | FAIL `judge_full_r17.txt` 05:26:21 | FAIL `crop_dense_judge.txt` 06:18:02 |
| 004 | PASS `judge_full_r15.txt` 05:42:50 | PASS `crop_dense_judge_r15.txt` 06:36:00 |
| 005 | PASS `judge_full_r16.txt` 07:02:40 | PASS `crop_dense_judge_r19.txt` 06:59:58 |
| 006 | FAIL `judge_full_r15_r22.txt` 07:33:17 | PASS `crop_dense_judge_r17.txt` 05:30:47 |
| 007 | PASS `judge_full_r20.txt` 08:03:14 | PASS `crop_dense_judge_r18.txt` 06:20:43 |
| 008 | PASS `judge_full_r20.txt` 06:57:54 | FAIL `crop_dense_judge_r19.txt` 07:20:46 |
| 009 | PASS `judge_full_r20.txt` 06:11:33 | PASS `crop_dense_judge_r21.txt` 07:01:22 |
| 010 | FAIL `judge_full_r17.txt` 07:17:34 | PASS `crop_dense_judge_r21.txt` 07:03:21 |
| 011 | PASS `judge_full_r16.txt` 06:53:45 | PASS `crop_dense_judge_r15.txt` 06:21:21 |
| 012 | PASS `judge_full_fresh.txt` 04:11:08 | PASS `crop_dense_judge.txt` 04:32:11 |
| 013 | FAIL `judge_full_r18.txt` 06:34:39 | PASS `crop_dense_judge_r20.txt` 07:32:07 |
| 014 | FAIL `judge_full_fix2.txt` 07:08:42 | PASS `crop_dense_judge_fix3.txt` 06:38:51 |
| 015 | FAIL `judge_full_fresh3.txt` 05:25:35 | FAIL `crop_dense_judge_r20.txt` 06:11:35 |
| 016 | FAIL `judge_full_fresh.txt` 07:56:03 | PASS `crop_dense_judge_r17.txt` 06:35:59 |
| 017 | PASS `judge_full_r19.txt` 06:47:16 | FAIL `crop_dense_judge_r15.txt` 07:51:53 |
| 018 | PASS `judge_full_r19.txt` 07:22:11 | FAIL `crop_dense_judge_r20.txt` 07:06:58 |
| 019 | PASS `judge_full_wfix.txt` 06:51:15 | PASS `crop_dense_judge_wfix.txt` 06:47:33 |
| 020 | PASS `judge_full_r21.txt` 07:27:31 | PASS `crop_dense_judge_r20.txt` 07:35:21 |
| 021 | PASS `judge_full_r18.txt` 06:31:55 | PASS `crop_dense_judge_r16.txt` 05:35:48 |
| 022 | FAIL `judge_full_r20.txt` 06:17:11 | FAIL `crop_dense_judge_r17.txt` 05:19:17 |
| 023 | PASS `judge_full_r20.txt` 06:21:12 | PASS `crop_dense_judge_r16.txt` 05:27:02 |
| 024 | PASS `judge_full_r19.txt` 06:45:41 | PASS `crop_dense_judge_r16.txt` 05:33:13 |
| 025 | FAIL `judge_full_k17d.txt` 07:39:06 | PASS `crop_dense_judge_k17n.txt` 08:03:16 |
| 026 | FAIL `judge_full_r16.txt` 06:18:04 | PASS `crop_dense_judge_r21.txt` 06:53:57 |
| 027 | PASS `judge_full_r16.txt` 06:16:05 | PASS `crop_dense_judge_r16.txt` 05:22:54 |
| 028 | PASS `judge_full_r16.txt` 06:05:37 | PASS `crop_dense_judge_r20.txt` 07:03:32 |
| 029 | PASS `judge_full_r20.txt` 07:47:20 | PASS `crop_dense_judge_r17.txt` 06:11:19 |
| 030 | PASS `judge_full_r17.txt` 06:57:15 | PASS `crop_dense_judge_w03.txt` 06:30:31 |
| 031 | PASS `judge_full_r19.txt` 07:08:41 | FAIL `crop_dense_judge_r17.txt` 07:02:04 |
| 032 | PASS `judge_full_r17.txt` 06:59:26 | PASS `crop_dense_judge_w03.txt` 05:35:15 |
| 033 | PASS `judge_full_w03.txt` 07:29:53 | PASS `crop_dense_judge_fresh.txt` 04:03:52 |
| 034 | PASS `judge_full_r19.txt` 07:17:47 | PASS `crop_dense_judge_w03.txt` 06:36:16 |
| 035 | PASS `judge_full_r16.txt` 07:41:39 | PASS `crop_dense_judge_r19.txt` 06:05:16 |
| 036 | PASS `judge_full_r21.txt` 07:29:56 | FAIL `crop_dense_judge_r17.txt` 06:29:52 |
| 037 | FAIL `judge_full_r20.txt` 06:01:08 | PASS `crop_dense_judge_r16.txt` 07:47:22 |
| 038 | PASS `judge_full_r20.txt` 06:10:57 | PASS `crop_dense_judge_r21.txt` 07:26:55 |
| 039 | PASS `judge_full.txt` 02:45:27 | PASS `crop_dense_judge_r17.txt` 07:09:36 |
| 040 | PASS `judge_full_r17.txt` 06:24:29 | PASS `crop_dense_judge_fresh3.txt` 06:40:34 |
| 041 | FAIL `judge_full_r17.txt` 08:03:44 | FAIL `crop_dense_judge_r19.txt` 06:58:10 |
| 042 | PASS `judge_full_r20.txt` 06:48:21 | PASS `crop_dense_judge.txt` 02:07:56 |
| 043 | FAIL `judge_full_r20.txt` 07:11:26 | PASS `crop_dense_judge_r16.txt` 06:44:14 |
| 044 | FAIL `judge_full_r18.txt` 06:45:47 | PASS `crop_dense_judge_r16.txt` 06:05:19 |
| 045 | FAIL `judge_full_r19.txt` 07:16:21 | PASS `crop_dense_judge_fresh3.txt` 07:31:15 |
| 046 | FAIL `judge_full_fresh2.txt` 05:02:02 | PASS `crop_dense_judge_r22.txt` 07:21:19 |
| 047 | PASS `judge_full_r18.txt` 06:46:43 | PASS `crop_dense_judge_fresh2.txt` 03:25:22 |
| 048 | FAIL `judge_full_r20.txt` 07:25:30 | FAIL `crop_dense_judge_r18.txt` 07:46:48 |
| 049 | FAIL `judge_full_r16.txt` 06:26:22 | PASS `crop_dense_judge_r22.txt` 06:38:32 |
| 050 | FAIL `judge_full_r20.txt` 07:24:38 | PASS `crop_dense_judge_fresh3.txt` 07:31:33 |
| 051 | FAIL `judge_full_w2.txt` 05:45:01 | PASS `crop_dense_judge_w2.txt` 06:40:12 |

**OPEN list (newest clean leg FAIL on FULL and/or CROP, or DB-open) — 27 slides:**
001, 002, 003, 006, 008, 010, 013, 014, 015, 016, 017, 018, 022, **025** (also the only DB-open row),
026, 031, 036, 037, 041, 043, 044, 045, 046, 048, 049, 050, 051.
FULL-FAIL-only: 001, 002, 006, 010, 013, 014, 015, 016, 026, 037, 043, 044, 045, 046, 049, 050, 051.
CROP-FAIL-only: 008, 017, 018, 031, 036. Both legs FAIL: 003, 022, 025 (DB-open), 041, 048.
Fully clean (PASS/PASS): 24 slides — 004, 005, 007, 009, 011, 012, 019, 020, 021, 023, 024, 027,
028, 029, 030, 032, 033, 034, 035, 038, 039, 040, 042, 047.
Per register rulings many FAIL legs carry banked PIL dismissals (see r31 §2 and the register);
this table is census-only, not a re-open order.

## 3. Slide 025 special section

- Current `recreated_pptx/slide_025_recreated.pptx` md5 at 2026-10-31T08:05:56Z:
  **`6dda603c7f4760a2d86e866b548501be`** — the file is under ACTIVE rebuild by live workers:
  md5 observed churning 07:58→08:05Z (`5479c739…` → `1809b318…` → `cd4582ba…` → `e2bf0bd4…` →
  `6dda603c…`, per `slide025/MONITOR_k17z2.log` CLOBBER-WATCH sigs and direct md5sum reads).
- k17z2 leg states at scan time:
  - `leg_full_k17z2.pid` / `leg_crop_k17z2.pid` wrapper pids (2349588 / 2349594) are dead, but
    their `16_vision_gate.sh` children are STILL RUNNING (pids 2380449/2380450 full,
    2384938/2384939 crop, ~18 min elapsed at 08:04Z) against `render_k17z2.png` /
    `crop_dense_{render,orig}_k17z2.png`.
  - Transcripts `judge_full_k17z2.txt` / `crop_dense_judge_k17z2.txt` do NOT exist yet
    (0-byte `.log` + 0-byte `.wrapper.out`); `MONITOR_k17z2.log` (pid 2445103, alive) shows both
    legs `pending size=missing` through 08:01:41Z. Expected deck md5 per the monitor:
    `c50e78bf39531523dcf69d652254b647` (not yet seen on disk).
  - A successor `k17z3` crop leg (`vision_leg.sh … crop_dense_judge_k17z3.txt`, pid 2463551) was
    launched 08:01Z; its transcript also not yet written at 08:04Z.
  - Newest clean 025 legs in the rejudge table above: FULL FAIL `judge_full_k17d.txt` 07:39:06,
    CROP PASS `crop_dense_judge_k17n.txt` 08:03:16 (supersede r31's k16-PASS / fresh-FAIL pair).

## 4. Deck ledger — `recreated_pptx/final_deck_state.json` (read-only) + on-disk md5 comparison

- `total_pages`: 51; page entries: 51; page `status` census: **certified 51/51**.
- `render_check` census: **FAIL 47, PASS 4 (pages 14, 19, 33, 51), PENDING 0** — pages 33 and 51
  flipped PENDING→PASS at 07:59:22Z / 08:02:56Z render-checks since r31. Latest event:
  render-check pages [14,19,33,51] PASS @ 2026-10-31T08:02:56Z; before that pages
  [21..30] FAIL @08:02:07Z (mismatched [23, 25, 27]).
- `deck_md5` ledger `e55b0ba6153d34006e679739ac4fadb6` == on-disk md5 of
  `03_ridger_regression_gradient_descent_final.pptx` — **MATCH** (deck bytes match the ledger).
- `source_md5` mismatches vs on-disk per-slide pptx: **3** —
  - page 4: ledger `761bcac7…` vs disk `4d21712f…` (`slide_004_recreated.pptx`)
  - page 10: ledger `9b4ee43a…` vs disk `67b341ef…` (`slide_010_recreated.pptx`)
  - page 25: ledger `8a355c24…` vs disk `6dda603c…` (at 08:05:56Z; still churning — slide 25 is
    the open DB row and active fix target)

## 5. Live wrappers

- `pgrep -fc vision_leg.sh` at 2026-10-31T08:05:56Z → **487** live wrapper processes
  (fleet-wide; up from 464 at r31 07:35:54Z — the slide-25 k17z2/k17z3 fix storm is still running).

## 6. OMML wrapped count (grep -c mc:AlternateContent on each slide pptx slide1.xml)

- **3 of 51 slides wrapped, 1 AlternateContent each: `slide_009`, `slide_036`, `slide_039`**
  (total 3 `mc:AlternateContent` occurrences across the deck's slide1.xml files).

## Files changed this spawn

- Created this file `REJUDGE_SUMMARY_r33.md`; appended one dated pointer line to
  `REJUDGE_REGISTER.md` (append-only).
- Scratch only: `scratch/tmp/r33_scan.py`, `scratch/tmp/r33_scan.json` (project scratch, untracked).
- No git operations; no vision legs launched; no evidence deleted; no build/pptx/DB/deck files modified.
