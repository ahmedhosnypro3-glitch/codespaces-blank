# Cert-evidence audit — rejudge_20261027 (read-only verification, 2026-10-31)

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent`
Scope: all slides with `gen_status='passed' AND visual_check='PASS'` in `slides_progress.db` — **50 slides** (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51).

Evidence required per slide (all three):
1. a **FULL** transcript under `$RJ` (slideNNN dir or flat, filename contains `full`) containing a clean `FINAL VERDICT` PASS (>=1 PASS verdict, 0 FAIL verdicts, **0 lines containing '429**)')
2. a **CROP** transcript (filename contains `crop`) with the same clean-PASS property
3. ledger page `pages['<n>'].status == 'certified'` in `recreated_pptx/final_deck_state.json`

Verdict-line matcher: `FINAL VERDICT` followed by PASS/FAIL (colon, no-colon, and `**bold**` forms all accepted). Payload/prompt files, registers, summaries, result logs, and non-text artifacts are excluded. Where several clean transcripts exist, the newest by mtime is listed.

## Summary

- In scope: **50**
- **OK** (clean full PASS + clean crop PASS + certified ledger page): **47**
- **MISSING** (at least one of the three absent): **3**

MISSING slides: **16, 42, 50**

## Per-slide rows

| slide | DB gen/visual | full PASS transcript (mtime) | crop PASS transcript (mtime) | ledger page | verdict |
|---|---|---|---|---|---|
| 1 | passed / PASS | `slide001/judge_full_r15_r22.txt.wrapper.out` (2026-10-31 06:37:14) | `slide001/judge_crop_w4.wrapper.out` (2026-10-31 08:41:55) | certified | OK |
| 2 | passed / PASS | `leg_005_full_fresh2.log` (2026-10-31 03:22:26) | `slide002/judge_crop_w4.wrapper.out` (2026-10-31 08:43:12) | certified | OK |
| 3 | passed / PASS | `slide003/judge_full.txt.log` (2026-10-31 05:01:41) | `slide003/crop_dense_judge_r17.wrapper.out` (2026-10-31 08:34:03) | certified | OK |
| 4 | passed / PASS | `slide004/judge_full_r15.wrapper.out` (2026-10-31 05:42:50) | `slide004/crop_dense_judge_r20.wrapper.out` (2026-10-31 08:21:43) | certified | OK |
| 5 | passed / PASS | `slide005/judge_full_r18.wrapper.out` (2026-10-31 08:28:01) | `slide005/crop_dense_judge_r19.wrapper.out` (2026-10-31 06:59:59) | certified | OK |
| 6 | passed / PASS | `slide006/judge_full_r19.wrapper.out` (2026-10-31 07:19:52) | `slide006/crop_dense_judge_r17.wrapper.out` (2026-10-31 05:30:49) | certified | OK |
| 7 | passed / PASS | `slide007/judge_full_r19.wrapper.out` (2026-10-31 08:06:28) | `slide007/crop_dense_judge_r18.wrapper.out` (2026-10-31 06:20:43) | certified | OK |
| 8 | passed / PASS | `slide008/judge_full_fresh.txt.log` (2026-10-31 08:19:50) | `slide008/crop_dense_judge.txt.log` (2026-10-31 08:34:23) | certified | OK |
| 9 | passed / PASS | `slide009/judge_full_r20.wrapper.out` (2026-10-31 06:11:35) | `slide009/crop_dense_judge_r20.wrapper.out` (2026-10-31 08:04:43) | certified | OK |
| 10 | passed / PASS | `slide010/judge_full_retry.txt` (2026-10-30 00:27:19) | `slide010/crop_dense_judge_r20.wrapper.out` (2026-10-31 08:39:51) | certified | OK |
| 11 | passed / PASS | `slide011/judge_full_r16_r22.txt.wrapper.out` (2026-10-31 08:22:14) | `slide011/crop_dense_judge_r15.wrapper.out` (2026-10-31 06:21:21) | certified | OK |
| 12 | passed / PASS | `slide012/judge_full_r17.wrapper.out` (2026-10-31 08:40:38) | `slide012/crop_dense_judge.txt.log` (2026-10-31 04:32:11) | certified | OK |
| 13 | passed / PASS | `slide013/judge_full_r20.wrapper.out` (2026-10-31 06:02:38) | `slide013/crop_dense_judge_fleet_20261031.txt` (2026-10-31 08:25:57) | certified | OK |
| 14 | passed / PASS | `slide014/leg_full_fix.wrapper.out` (2026-10-31 05:44:02) | `slide014/crop_dense_judge_fix2.txt.wrapper.out` (2026-10-31 08:35:00) | certified | OK |
| 15 | passed / PASS | `slide015/judge_full_fresh.txt.log` (2026-10-31 08:10:33) | `slide015/crop_dense_judge.txt.pre_fresh20261031` (2026-10-31 02:45:55) | certified | OK |
| 16 | passed / PASS | MISSING — 22 full-named files scanned, 0 clean PASS | `slide016/crop_dense_judge_r17.wrapper.out` (2026-10-31 06:36:00) | certified | MISSING |
| 17 | passed / PASS | `slide017/judge_full_r18.wrapper.out` (2026-10-31 08:34:47) | `slide017/crop_dense_judge.log` (2026-10-31 04:13:49) | certified | OK |
| 18 | passed / PASS | `slide018/judge_full_r19.wrapper.out` (2026-10-31 07:22:12) | `slide018/crop_dense_judge_r19.wrapper.out` (2026-10-31 05:59:53) | certified | OK |
| 19 | passed / PASS | `slide019/judge_full_wfix.wrapper.out` (2026-10-31 06:51:16) | `slide019/crop_dense_judge_wfix.wrapper.out` (2026-10-31 06:47:34) | certified | OK |
| 20 | passed / PASS | `slide020/judge_full_r21.wrapper.out` (2026-10-31 07:27:31) | `slide020/crop_dense_judge_r20.wrapper.out` (2026-10-31 07:35:21) | certified | OK |
| 21 | passed / PASS | `slide021/judge_full_r18.wrapper.out` (2026-10-31 06:31:56) | `slide021/crop_dense_judge_r21.wrapper.out` (2026-10-31 08:13:41) | certified | OK |
| 22 | passed / PASS | `slide022/judge_full_r16.wrapper.out` (2026-10-31 05:33:03) | `slide022/crop_dense_judge_r19.wrapper.out` (2026-10-31 08:47:44) | certified | OK |
| 23 | passed / PASS | `slide023/judge_full_r18.wrapper.out` (2026-10-31 08:38:12) | `slide023/crop_dense_judge_r19.wrapper.out` (2026-10-31 08:18:19) | certified | OK |
| 24 | passed / PASS | `slide024/judge_full_r19_r22.txt.wrapper.out` (2026-10-31 08:04:44) | `slide024/crop_dense_judge_r16.wrapper.out` (2026-10-31 05:33:14) | certified | OK |
| 26 | passed / PASS | `slide026/judge_full_r18.wrapper.out` (2026-10-31 08:38:15) | `slide026/crop_dense_judge_r21.wrapper.out` (2026-10-31 06:53:58) | certified | OK |
| 27 | passed / PASS | `slide027/judge_full_fresh.txt.log` (2026-10-31 08:38:37) | `slide027/crop_dense_judge.txt.log` (2026-10-31 08:42:49) | certified | OK |
| 28 | passed / PASS | `slide028/judge_full_r16.wrapper.out` (2026-10-31 06:05:38) | `slide028/crop_dense_judge_r20.wrapper.out` (2026-10-31 07:03:32) | certified | OK |
| 29 | passed / PASS | `slide029/judge_full_r21.wrapper.out` (2026-10-31 08:38:54) | `slide029/crop_dense_judge_r21.wrapper.out` (2026-10-31 08:41:38) | certified | OK |
| 30 | passed / PASS | `slide030/judge_full_r17.wrapper.out` (2026-10-31 06:57:16) | `slide030/crop_dense_judge_w03.wrapper.out` (2026-10-31 06:30:32) | certified | OK |
| 31 | passed / PASS | `slide031/judge_full_r18.wrapper.out` (2026-10-31 08:45:50) | `slide031/crop_dense_judge_r19.wrapper.out` (2026-10-31 06:39:45) | certified | OK |
| 32 | passed / PASS | `slide032/judge_full_r21.wrapper.out` (2026-10-31 08:14:16) | `slide032/crop_dense_judge_w03.wrapper.out` (2026-10-31 05:35:15) | certified | OK |
| 33 | passed / PASS | `slide033/judge_full_fresh.txt.log` (2026-10-31 08:39:51) | `slide033/crop_dense_judge_fresh.txt.log` (2026-10-31 04:03:52) | certified | OK |
| 34 | passed / PASS | `slide034/judge_full_r19.wrapper.out` (2026-10-31 07:17:47) | `slide034/crop_dense_judge_r19.wrapper.out` (2026-10-31 08:42:37) | certified | OK |
| 35 | passed / PASS | `slide035/judge_full_r20.wrapper.out` (2026-10-31 08:40:25) | `slide035/crop_dense_judge_r19.wrapper.out` (2026-10-31 06:05:17) | certified | OK |
| 36 | passed / PASS | `slide036/judge_full_fresh.txt.log` (2026-10-31 08:11:24) | `slide036/crop_dense_judge_r20.wrapper.out` (2026-10-31 06:19:44) | certified | OK |
| 37 | passed / PASS | `slide037/judge_full_r17.wrapper.out` (2026-10-31 05:31:19) | `slide037/crop_dense_judge_r16.txt.wrapper.out` (2026-10-31 07:47:22) | certified | OK |
| 38 | passed / PASS | `slide038/judge_full_fresh.txt.log` (2026-10-31 08:37:16) | `slide038/crop_dense_judge.txt.log` (2026-10-31 08:40:55) | certified | OK |
| 39 | passed / PASS | `slide039/judge_full_r17.wrapper.out` (2026-10-31 08:23:44) | `slide039/crop_dense_judge_r20.wrapper.out` (2026-10-31 08:38:49) | certified | OK |
| 40 | passed / PASS | `slide040/judge_full_r19.wrapper.out` (2026-10-31 08:42:22) | `slide040/crop_dense_judge_fresh3.txt.wrapper.out` (2026-10-31 06:40:36) | certified | OK |
| 41 | passed / PASS | `slide041/judge_full_r21.wrapper.out` (2026-10-31 07:32:28) | `slide041/crop_dense_judge_r21.wrapper.out` (2026-10-31 08:40:39) | certified | OK |
| 42 | passed / PASS | `slide042/judge_full_fresh.txt.log` (2026-10-31 08:43:06) | MISSING — 13 crop-named files scanned, 0 clean PASS | certified | MISSING |
| 43 | passed / PASS | `slide043/judge_full_fresh.txt.log` (2026-10-31 08:35:34) | `slide043/crop_dense_judge_r16.txt.wrapper.out` (2026-10-31 06:44:15) | certified | OK |
| 44 | passed / PASS | `slide044/judge_full_fresh.txt.log` (2026-10-31 08:43:40) | `slide044/crop_dense_judge_r20.wrapper.out` (2026-10-31 08:17:17) | certified | OK |
| 45 | passed / PASS | `slide045/judge_full_r17.wrapper.out` (2026-10-31 08:42:55) | `slide045/crop_dense_judge.txt.log` (2026-10-31 08:39:02) | certified | OK |
| 46 | passed / PASS | `slide046/judge_full.txt.wrapper.out` (2026-10-31 03:34:08) | `slide046/crop_dense_judge_r22.txt.wrapper.out` (2026-10-31 07:21:20) | certified | OK |
| 47 | passed / PASS | `slide047/judge_full_r18.wrapper.out` (2026-10-31 06:46:45) | `slide047/crop_dense_judge_r20.wrapper.out` (2026-10-31 08:09:04) | certified | OK |
| 48 | passed / PASS | `slide048/judge_full_r17.wrapper.out` (2026-10-31 06:32:26) | `slide048/crop_dense_judge_r17.wrapper.out` (2026-10-31 07:38:48) | certified | OK |
| 49 | passed / PASS | `slide049/judge_full_fresh2.txt.wrapper.out` (2026-10-31 03:30:25) | `slide049/crop_dense_judge_r22.txt.wrapper.out` (2026-10-31 06:38:33) | certified | OK |
| 50 | passed / PASS | MISSING — 34 full-named files scanned, 0 clean PASS | `slide050/crop_dense_judge_fresh3.txt.wrapper.out` (2026-10-31 07:31:34) | certified | MISSING |
| 51 | passed / PASS | `slide051/judge_full_fresh3.txt.wrapper.out` (2026-10-31 04:52:23) | `slide051/crop_dense_judge_r18.wrapper.out` (2026-10-31 08:28:50) | certified | OK |

## MISSING-slide detail

### slide 16 — ledger=certified
- full leg: 22 file(s) with 'full' in name scanned, 0 clean PASS; certifying file: none
- crop leg: 17 file(s) with 'crop' in name scanned, 5 clean PASS; certifying file: slide016/crop_dense_judge_r17.wrapper.out

### slide 42 — ledger=certified
- full leg: 21 file(s) with 'full' in name scanned, 13 clean PASS; certifying file: slide042/judge_full_fresh.txt.log
- crop leg: 13 file(s) with 'crop' in name scanned, 0 clean PASS; certifying file: none

### slide 50 — ledger=certified
- full leg: 34 file(s) with 'full' in name scanned, 0 clean PASS; certifying file: none
- crop leg: 21 file(s) with 'crop' in name scanned, 6 clean PASS; certifying file: slide050/crop_dense_judge_fresh3.txt.wrapper.out

## Method notes

- DB opened read-only (`file:...?mode=ro`); exact query: `SELECT slide_id FROM slides WHERE gen_status='passed' AND visual_check='PASS';` — no writes, no git.
- Candidate files: everything in `$RJ/slide%03d/` and `$RJ/slide%d/` plus flat `$RJ` files whose names reference the slide (padded `NNN` or digit-bounded plain `N`); filename must contain `full` (FULL leg) or `crop` (CROP leg); excluded: `payload*`, `probe*`, `result.txt*`, `REJUDGE_*`, summaries, `.md/.py/.sh/.png/.pdf/.pptx/.db/.json`, `chrome_check`, drivers.
- Clean PASS = >=1 `FINAL VERDICT...PASS` line, 0 `FINAL VERDICT...FAIL` lines, 0 lines containing `429` (literal substring, as specified).
- Ledger check: `final_deck_state.json` -> `pages['<slide_id>'].status`.
- Backup/banked transcript copies (`.bank`, `.W02bank`, `.pre_*`) are counted as transcripts since they are byte-copies of the leg transcript; driver `.out` logs are counted only when the leg word appears in the filename.
