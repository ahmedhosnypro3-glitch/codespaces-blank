# Read-only sweep r35 — 03_ridger_regression_gradient_descent

- NS = `/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent`
- RJ = `$NS/recreated_pptx/qa/rejudge_20261027`
- Sweep executed 2026-10-31 08:32:58 – 08:36 UTC (read-only except this report file; no git, no DB writes, no deletions)

## 1. Time
`date -u` → **Sat Oct 31 08:32:58 UTC 2026**

## 2. slides_progress.db — non-passed rows and status counts
Query: `SELECT slide_id,gen_status,visual_check FROM slides WHERE gen_status!='passed' OR visual_check!='PASS';`

| slide_id | gen_status | visual_check |
|---|---|---|
| 25 | building | (empty) |

Counts (51 rows total):
- gen_status: `passed` = 50, `building` = 1
- visual_check: `PASS` = 50, empty = 1 (slide 25)

**Slide 25 row does NOT show passed/PASS** → the "verify certifying transcripts before believing it" clause does not trigger from the DB side; transcript check done anyway in §4: there is no clean PASS.

## 3. md5 checks
- `recreated_pptx/slide_025_recreated.pptx` → `c50e78bf39531523dcf69d652254b647` = **canonical MATCH**
- `recreated_pptx/build/assets/plot_025_*.png` (4 files):
  - `plot_025_bl.png` 7a8e7210f118b728245d268552a7d32d
  - `plot_025_br.png` f6af102ec110ff5113482659ff4f9d73
  - `plot_025_tl.png` cd62022fbf0cfe30a351309c0230adb3
  - `plot_025_tr.png` b45c723af19e2cf11659109d63134cad

## 4. Newest FINAL VERDICT + 429 count — `$RJ/slide025/*k17z2*.txt`, `*k17z3*.txt`, `bl_labels_leg.txt`
Method: `grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' <f> | tail -1`; 429 = count of `429` (and strict `429 Too Many|HTTP 429|Too Many Requests|rate.?limit` — both zero everywhere).

| file | mtime (UTC) | newest FINAL VERDICT | 429 |
|---|---|---|---|
| crop_region_k17z2.txt | 07:38:29 | none (30 B region spec) | 0 |
| pil_k17z2_render_census.txt | 07:52:58 | none (pixel census) | 0 |
| judge_full_k17z2.txt | **absent — in flight** (only .log, 495 B, no verdict yet) | — | 0 |
| crop_dense_judge_k17z2.txt | **absent — in flight** (.log 0 B) | — | 0 |
| adjudicate_crop_monitor_k17z3_20261031_0816.txt | 08:16:19 | none (pixel-diff dump) | 0 |
| adjudicate_full_monitor_k17z3_20261031_0817.txt | 08:17:40 | none (pixel-diff dump) | 0 |
| chrome_check_k17z3.txt | 08:19:18 | none | 0 |
| crop_region_k17z3.txt | 08:19:25 | none | 0 |
| monitor_bank_judge_full_k17z3_082908.txt | 08:29:08 | **FAIL** | 0 |
| judge_full_k17z3.txt | 08:31:28 | **FAIL** | 0 |
| crop_dense_judge_k17z3.txt | 08:32:20 | **FAIL** | 0 |
| bl_labels_leg.txt | **absent — wrapper running since 08:30** (.log/.wrapper.out 0 B) | — | 0 |

FAIL reasons (k17z3): FULL — bottom-left "Non-Convex" panel "Local Maxima" clipped to "cal Maxima", leader-line collision, "Global Maxima" mislabeled, foreign base strip at foot of bottom-right plot. CROP — wrong render type, missing z-axis + labels, missing contour projection, probable value inversion.

**No PASS verdict exists in any k17z2/k17z3 .txt.** Latest completed legs (k17z3 FULL 08:31 and CROP 08:32) are both FAIL with zero 429s; k17z2 FULL/CROP and bl_labels_leg are still running. Note: `CLOBBER_WATCH.log` contains a `FINAL VERDICT: PASS` string and 3 `429` token hits, but both are artifacts of that watch log (a PASS line echoed from an older k17n run; the `429` hits are PID `2429197` inside logged command lines) — it is not a k17z2/k17z3/bl judge transcript. **Certifying clean-PASS transcripts (FULL + CROP, no 429) for slide 25 do NOT currently exist.**

## 5. Deck ledger — `recreated_pptx/final_deck_state.json`
- deck: `.../03_ridger_regression_gradient_descent_final.pptx` (path recorded as `/home/ahmed/Projects/...` — founder-machine path), `deck_md5` = `872284b7f41336fddf39b84ef5ddc63e`, `total_pages` = 51, scope `S21_continuous_final_deck (run 299640)`, 197 events (last: update-page 51 @ 2026-10-31T08:26:31).
- pages: **51 entries, all `status=certified`**.
- render_check counts: PASS = 4 (pages 14, 19, 33, 50), FAIL = 46, PENDING = 1 (page 51).
- source_md5 vs disk md5 of `slide_NNN_recreated.pptx` — **4 mismatches**:

| page | ledger source_md5 | disk md5 |
|---|---|---|
| 4 | 761bcac779b717283a562386447856c9 | 4d21712f117e541d74acd852067c44c7 |
| 10 | 9b4ee43ad50f90f09df108c1645c4d26 | 67b341efaf3ac298c9b5cba604e97881 |
| 13 | 468d84817c02b4ffe703b2f87cc5ea40 | 244dde61917015d674f650242fa92ae3 |
| 25 | 8a355c242807bcdac9574b941dcf85f5 | c50e78bf39531523dcf69d652254b647 (= canonical) |

Page 25's ledger entry is stale (ledger 8a355c…, updated 2026-10-31T02:54:14); the file on disk IS the canonical c50e78bf… — the ledger has not been refreshed after the current build.

## 6. Running vision processes (sampled ~08:35 UTC; counts fluctuate)
- `ps -eo args | grep -c '[v]ision_leg.sh'` → **410** at first sample, **405** on re-sample
- `ps -eo args | grep -c '[a]nalyze_image'` → **708**
- slide025 currently has 11 unique vision_leg targets in flight: bl_labels_leg.txt, crop_dense_judge_{fresh2,k15,k17o,k17p,k17z2,k17z3}.txt, judge_full_{k15,k17o,k17p,k17z2,k17z3}.txt
- Legs span many slides (slide045: 35, slide040: 31, slide035: 27, …) — the rejudge fan-out is fleet-wide, not just slide 25.

## 7. CronList — skipped per instruction.

## Bottom line
Slide 25 is the only non-passed row (`building` / blank visual_check), consistent with the transcript evidence: newest completed k17z3 FULL and CROP verdicts are FAIL (no 429s), k17z2 and bl_labels_leg legs are still in flight, and no clean PASS exists for the requested files. The on-disk `slide_025_recreated.pptx` is byte-identical to the canonical md5, but the deck ledger's source_md5 for pages 4, 10, 13, 25 is stale relative to disk (25's disk file matches canonical). ~405 vision_leg.sh wrappers / ~708 analyze_image processes are running fleet-wide at sweep time.
