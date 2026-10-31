# VERDICT_CENSUS_r1 — per-slide newest clean transcript verdicts

Generated: 2026-10-31 08:51:51 UTC (read-only harvest; no vision calls, no git, no DB/pptx writes)

Source: every file under `recreated_pptx/qa/rejudge_20261027/` (slideNNN dirs + flat files) containing a line-anchored `FINAL VERDICT: PASS|FAIL`.
Clean = no 429 line (a line containing `429` that is not a `no 429` annotation). Newest = max file mtime among clean transcripts for that slide+mode.
DB: `SELECT gen_status, visual_check FROM slides WHERE slide_id=N` from `slides_progress.db` (opened read-only).

| slide | FULL verdict | FULL file | FULL mtime | CROP verdict | CROP file | CROP mtime | DB gen_status | DB visual_check | flags |
|---|---|---|---|---|---|---|---|---|---|
| 001 | FAIL | `slide001/judge_full_w4.wrapper.out` | 2026-10-31 08:43:00 UTC | PASS | `slide001/judge_crop_w4.wrapper.out` | 2026-10-31 08:41:55 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 002 | FAIL | `slide002/judge_full_r19.wrapper.out` | 2026-10-31 06:08:47 UTC | PASS | `slide002/judge_crop_w4.wrapper.out` | 2026-10-31 08:43:12 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 003 | PASS | `fresh_003.out` | 2026-10-31 08:12:45 UTC | PASS | `slide003/crop_dense_judge_r17.wrapper.out` | 2026-10-31 08:34:03 UTC | passed | PASS | ok |
| 004 | PASS | `slide004/judge_full_r20.wrapper.out` | 2026-10-31 08:49:38 UTC | PASS | `slide004/crop_dense_judge_r20.wrapper.out` | 2026-10-31 08:21:43 UTC | passed | PASS | ok |
| 005 | PASS | `slide005/judge_full_r18.wrapper.out` | 2026-10-31 08:28:01 UTC | FAIL | `slide005/crop_dense_judge_r19_r22.txt.wrapper.out` | 2026-10-31 08:48:05 UTC | passed | PASS | newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 006 | FAIL | `slide006/judge_full_r15_r22.txt.wrapper.out` | 2026-10-31 07:33:18 UTC | PASS | `slide006/crop_dense_judge_r17.wrapper.out` | 2026-10-31 05:30:49 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 007 | PASS | `slide007/judge_full_r19.wrapper.out` | 2026-10-31 08:06:28 UTC | FAIL | `slide007/crop_dense_judge_r20.wrapper.out` | 2026-10-31 08:41:31 UTC | passed | PASS | newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 008 | PASS | `fresh_008.out` | 2026-10-31 08:34:23 UTC | PASS | `fresh_008.out` | 2026-10-31 08:34:23 UTC | passed | PASS | ok |
| 009 | PASS | `slide009/judge_full_r20.wrapper.out` | 2026-10-31 06:11:35 UTC | PASS | `slide009/crop_dense_judge_r20.wrapper.out` | 2026-10-31 08:04:43 UTC | passed | PASS | ok |
| 010 | FAIL | `fresh_010.out` | 2026-10-31 08:35:51 UTC | PASS | `slide010/crop_dense_judge_r20.wrapper.out` | 2026-10-31 08:39:51 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 011 | PASS | `slide011/judge_full_r16_r22.txt.wrapper.out` | 2026-10-31 08:22:14 UTC | PASS | `slide011/crop_dense_judge_r15.wrapper.out` | 2026-10-31 06:21:21 UTC | passed | PASS | ok |
| 012 | PASS | `slide012/judge_full_r17.wrapper.out` | 2026-10-31 08:40:38 UTC | PASS | `fresh_012.out` | 2026-10-31 08:12:45 UTC | passed | PASS | ok |
| 013 | PASS | `fresh_013.out` | 2026-10-31 08:31:54 UTC | PASS | `fresh_013.out` | 2026-10-31 08:31:54 UTC | passed | PASS | ok |
| 014 | FAIL | `slide014/judge_full_fix2.txt.wrapper.out` | 2026-10-31 07:08:43 UTC | PASS | `slide014/crop_dense_judge_fix2.txt.wrapper.out` | 2026-10-31 08:35:00 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 015 | FAIL | `slide015/judge_full_r17.wrapper.out` | 2026-10-31 08:23:43 UTC | FAIL | `fresh_015.out` | 2026-10-31 08:10:34 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS; newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 016 | FAIL | `fresh_016.out` | 2026-10-31 08:15:12 UTC | PASS | `slide016/crop_dense_judge_r17.wrapper.out` | 2026-10-31 06:36:00 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 017 | PASS | `slide017/judge_full_r18.wrapper.out` | 2026-10-31 08:34:47 UTC | FAIL | `slide017/crop_dense_judge_r15.wrapper.out` | 2026-10-31 07:51:54 UTC | passed | PASS | newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 018 | PASS | `slide018/judge_full_r19.wrapper.out` | 2026-10-31 07:22:12 UTC | FAIL | `slide018/crop_dense_judge_r18.wrapper.out` | 2026-10-31 08:36:44 UTC | passed | PASS | newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 019 | PASS | `slide019/judge_full_wfix.wrapper.out` | 2026-10-31 06:51:16 UTC | FAIL | `slide019/crop_dense_judge_w5.wrapper.out` | 2026-10-31 08:47:16 UTC | passed | PASS | newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 020 | PASS | `slide020/judge_full_r21.wrapper.out` | 2026-10-31 07:27:31 UTC | PASS | `slide020/crop_dense_judge_r20.wrapper.out` | 2026-10-31 07:35:21 UTC | passed | PASS | ok |
| 021 | FAIL | `slide021/judge_full_r17.wrapper.out` | 2026-10-31 08:36:06 UTC | PASS | `slide021/crop_dense_judge_r21.wrapper.out` | 2026-10-31 08:13:41 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 022 | FAIL | `slide022/judge_full_r20.wrapper.out` | 2026-10-31 06:17:13 UTC | PASS | `slide022/crop_dense_judge_r19.wrapper.out` | 2026-10-31 08:47:44 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 023 | FAIL | `slide023/judge_full_r21.wrapper.out` | 2026-10-31 08:45:29 UTC | PASS | `slide023/crop_dense_judge_r19.wrapper.out` | 2026-10-31 08:18:19 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 024 | PASS | `slide024/judge_full_r19_r22.txt.wrapper.out` | 2026-10-31 08:04:44 UTC | PASS | `slide024/crop_dense_judge_r16.wrapper.out` | 2026-10-31 05:33:14 UTC | passed | PASS | ok |
| 025 | FAIL | `slide025/judge_full_k17z3.wrapper.out` | 2026-10-31 08:43:48 UTC | FAIL | `slide025/crop_dense_judge_k17q.wrapper.out` | 2026-10-31 08:51:22 UTC | building |  | newest clean FULL = FAIL; newest clean CROP = FAIL |
| 026 | PASS | `slide026/judge_full_r18.wrapper.out` | 2026-10-31 08:38:15 UTC | PASS | `slide026/crop_dense_judge_r21.wrapper.out` | 2026-10-31 06:53:58 UTC | passed | PASS | ok |
| 027 | PASS | `fresh_027.out` | 2026-10-31 08:42:50 UTC | PASS | `fresh_027.out` | 2026-10-31 08:42:50 UTC | passed | PASS | ok |
| 028 | PASS | `slide028/judge_full_r16.wrapper.out` | 2026-10-31 06:05:38 UTC | PASS | `slide028/crop_dense_judge_r20.wrapper.out` | 2026-10-31 07:03:32 UTC | passed | PASS | ok |
| 029 | PASS | `slide029/judge_full_r21.wrapper.out` | 2026-10-31 08:38:54 UTC | PASS | `slide029/crop_dense_judge_r21.wrapper.out` | 2026-10-31 08:41:38 UTC | passed | PASS | ok |
| 030 | PASS | `slide030/judge_full_r17.wrapper.out` | 2026-10-31 06:57:16 UTC | PASS | `slide030/crop_dense_judge_w03.wrapper.out` | 2026-10-31 06:30:32 UTC | passed | PASS | ok |
| 031 | PASS | `slide031/judge_full_r18.wrapper.out` | 2026-10-31 08:45:50 UTC | FAIL | `slide031/crop_dense_judge_r17.wrapper.out` | 2026-10-31 07:02:04 UTC | passed | PASS | newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 032 | PASS | `slide032/judge_full_r21.wrapper.out` | 2026-10-31 08:14:16 UTC | PASS | `slide032/crop_dense_judge_w03.wrapper.out` | 2026-10-31 05:35:15 UTC | passed | PASS | ok |
| 033 | PASS | `fresh_033.out` | 2026-10-31 08:51:08 UTC | PASS | `slide033/crop_dense_judge.txt.W02bank` | 2026-10-31 08:51:19 UTC | passed | PASS | ok |
| 034 | PASS | `slide034/judge_full_r19.wrapper.out` | 2026-10-31 07:17:47 UTC | PASS | `slide034/crop_dense_judge_r19.wrapper.out` | 2026-10-31 08:42:37 UTC | passed | PASS | ok |
| 035 | PASS | `slide035/judge_full_r20.wrapper.out` | 2026-10-31 08:40:25 UTC | PASS | `slide035/crop_dense_judge_r20.wrapper.out` | 2026-10-31 08:51:17 UTC | passed | PASS | ok |
| 036 | PASS | `fresh_036.out` | 2026-10-31 08:19:46 UTC | FAIL | `fresh_036.out` | 2026-10-31 08:19:46 UTC | passed | PASS | newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 037 | FAIL | `slide037/judge_full_r20.wrapper.out` | 2026-10-31 06:01:09 UTC | FAIL | `slide037/crop_dense_judge_fresh3_r22.txt.wrapper.out` | 2026-10-31 08:10:47 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS; newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 038 | PASS | `fresh_038.out` | 2026-10-31 08:40:55 UTC | PASS | `fresh_038.out` | 2026-10-31 08:40:55 UTC | passed | PASS | ok |
| 039 | FAIL | `fresh_039.out` | 2026-10-31 08:49:21 UTC | PASS | `fresh_039.out` | 2026-10-31 08:49:21 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 040 | PASS | `slide040/judge_full_r19.wrapper.out` | 2026-10-31 08:42:22 UTC | PASS | `slide040/crop_dense_judge_fresh3.txt.wrapper.out` | 2026-10-31 06:40:36 UTC | passed | PASS | ok |
| 041 | FAIL | `slide041/judge_full_r17.wrapper.out` | 2026-10-31 08:03:44 UTC | PASS | `slide041/crop_dense_judge_r21.wrapper.out` | 2026-10-31 08:40:39 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 042 | PASS | `fresh_042.out` | 2026-10-31 08:43:06 UTC | — | — | — | passed | PASS | GAP: no clean CROP |
| 043 | PASS | `fresh_043.out` | 2026-10-31 08:35:34 UTC | FAIL | `slide043/crop_dense_judge_r21.wrapper.out` | 2026-10-31 08:20:16 UTC | passed | PASS | newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 044 | PASS | `fresh_044.out` | 2026-10-31 08:50:25 UTC | PASS | `fresh_044.out` | 2026-10-31 08:50:25 UTC | passed | PASS | ok |
| 045 | PASS | `slide045/judge_full_r17.wrapper.out` | 2026-10-31 08:42:55 UTC | PASS | `fresh_045.out` | 2026-10-31 08:39:03 UTC | passed | PASS | ok |
| 046 | FAIL | `slide046/judge_full_fresh2.txt.wrapper.out` | 2026-10-31 05:02:02 UTC | PASS | `slide046/crop_dense_judge_r22.txt.wrapper.out` | 2026-10-31 07:21:20 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 047 | PASS | `slide047/judge_full_r18.wrapper.out` | 2026-10-31 06:46:45 UTC | FAIL | `slide047/crop_dense_judge_r18.wrapper.out` | 2026-10-31 08:30:45 UTC | passed | PASS | newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 048 | FAIL | `slide048/judge_full_r18.wrapper.out` | 2026-10-31 08:30:03 UTC | FAIL | `slide048/crop_dense_judge_r18.wrapper.out` | 2026-10-31 07:46:48 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS; newest clean CROP = FAIL; CROP verdict FAIL != DB visual_check PASS |
| 049 | FAIL | `fresh_049.out` | 2026-10-31 08:49:16 UTC | PASS | `slide049/crop_dense_judge_r22.txt.wrapper.out` | 2026-10-31 06:38:33 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 050 | FAIL | `slide050/judge_full_r18.wrapper.out` | 2026-10-31 08:39:41 UTC | PASS | `slide050/crop_dense_judge_fresh3.txt.wrapper.out` | 2026-10-31 07:31:34 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |
| 051 | FAIL | `slide051/judge_full_w2.wrapper.out` | 2026-10-31 05:45:02 UTC | PASS | `slide051/crop_dense_judge_r18.wrapper.out` | 2026-10-31 08:28:50 UTC | passed | PASS | newest clean FULL = FAIL; FULL verdict FAIL != DB visual_check PASS |

## Gap list (no clean FULL or CROP verdict)
- (42, 'CROP')

## Disagreements (newest clean verdict != DB visual_check)
- slide 001 FULL: transcript FAIL vs DB visual_check=PASS
- slide 002 FULL: transcript FAIL vs DB visual_check=PASS
- slide 005 CROP: transcript FAIL vs DB visual_check=PASS
- slide 006 FULL: transcript FAIL vs DB visual_check=PASS
- slide 007 CROP: transcript FAIL vs DB visual_check=PASS
- slide 010 FULL: transcript FAIL vs DB visual_check=PASS
- slide 014 FULL: transcript FAIL vs DB visual_check=PASS
- slide 015 FULL: transcript FAIL vs DB visual_check=PASS
- slide 015 CROP: transcript FAIL vs DB visual_check=PASS
- slide 016 FULL: transcript FAIL vs DB visual_check=PASS
- slide 017 CROP: transcript FAIL vs DB visual_check=PASS
- slide 018 CROP: transcript FAIL vs DB visual_check=PASS
- slide 019 CROP: transcript FAIL vs DB visual_check=PASS
- slide 021 FULL: transcript FAIL vs DB visual_check=PASS
- slide 022 FULL: transcript FAIL vs DB visual_check=PASS
- slide 023 FULL: transcript FAIL vs DB visual_check=PASS
- slide 031 CROP: transcript FAIL vs DB visual_check=PASS
- slide 036 CROP: transcript FAIL vs DB visual_check=PASS
- slide 037 FULL: transcript FAIL vs DB visual_check=PASS
- slide 037 CROP: transcript FAIL vs DB visual_check=PASS
- slide 039 FULL: transcript FAIL vs DB visual_check=PASS
- slide 041 FULL: transcript FAIL vs DB visual_check=PASS
- slide 043 CROP: transcript FAIL vs DB visual_check=PASS
- slide 046 FULL: transcript FAIL vs DB visual_check=PASS
- slide 047 CROP: transcript FAIL vs DB visual_check=PASS
- slide 048 FULL: transcript FAIL vs DB visual_check=PASS
- slide 048 CROP: transcript FAIL vs DB visual_check=PASS
- slide 049 FULL: transcript FAIL vs DB visual_check=PASS
- slide 050 FULL: transcript FAIL vs DB visual_check=PASS
- slide 051 FULL: transcript FAIL vs DB visual_check=PASS

## Newest clean verdict is FAIL
- slide 001 FULL
- slide 002 FULL
- slide 005 CROP
- slide 006 FULL
- slide 007 CROP
- slide 010 FULL
- slide 014 FULL
- slide 015 FULL
- slide 015 CROP
- slide 016 FULL
- slide 017 CROP
- slide 018 CROP
- slide 019 CROP
- slide 021 FULL
- slide 022 FULL
- slide 023 FULL
- slide 025 FULL
- slide 025 CROP
- slide 031 CROP
- slide 036 CROP
- slide 037 FULL
- slide 037 CROP
- slide 039 FULL
- slide 041 FULL
- slide 043 CROP
- slide 046 FULL
- slide 047 CROP
- slide 048 FULL
- slide 048 CROP
- slide 049 FULL
- slide 050 FULL
- slide 051 FULL

## Stats
- transcript verdict-lines harvested: 1373 (clean 1370, dirty-429 3)
- slides with clean FULL: 51/51
- slides with clean CROP: 50/51
- files with verdict lines but unattributed (skipped): 2
  - `fresh_legs_018034.log` — no slide num
  - `fresh_worker_853213.log` — no slide num
