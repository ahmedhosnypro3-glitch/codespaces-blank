# waveW7_summary — full-rejudge wave W7 (deck 03, rejudge_20261027)

Launched: 2026-10-31 ~08:50 UTC by leg-launcher subagent. Scope: slides 001..051 except 025.
No git operations; no DB writes; no pptx modifications; no evidence deleted. Writes confined to
`$RJ` (this summary, `waveW7_launch_013.log`, `REJUDGE_REGISTER.md` append, `slide013/render_w7.png`,
`slide013/w7/`, `slide013/judge_full_w7.txt*`) and project scratch (`scratch/tmp/w7_gapscan*.py`).

## 1. Gap determination

- `$RJ/VERDICT_CENSUS_r1.md` (generated 2026-10-31 08:42:39 UTC) was present and checked first.
  Its gap list reads "none" (51/51 clean FULL) — but its clean rule tolerates non-error `429`
  lines ("a line containing `429` that is not a `no 429` annotation").
- Operative rule used here = the leg's own rule (`vision_leg.sh:25`): clean = `FINAL VERDICT`
  present AND `grep -qi '429'` finds NOTHING in the file (task parenthetical "(no 429)").
- Scan: newest (max mtime) `judge_full*.txt` per `slideNNN` dir (recursive) + root-level
  `judge_full*NNN*.txt`, for NNN in 001..051 except 025. Script: `scratch/tmp/w7_gapscan2.py`.
  Ran twice: 08:47:56Z and 08:49:33Z — identical result.

| result | count | slides |
|---|---|---|
| clean newest FULL transcript | 49 | 001 002 003 004 005 006 007 008 009 010 011 012 014 015 016 017 018 019 020 021 022 023 024 026 027 028 029 030 031 032 033 034 035 036 037 038 039 040 041 042 043 044 045 046 047 048 049 050 051 |
| GAP (newest FULL lacks clean verdict) | 1 | **013** |

- Slide 013 gap cause: newest transcript `slide013/judge_full_fresh.txt` (mtime 08:47:31Z, being
  rewritten by a live fleet leg at scan time) ends `FINAL VERDICT: PASS` but line 38 contains the
  coordinate text `x404–429` — a `429` substring, so NOT clean under the leg rule. (Census counted
  it clean under its annotation-tolerant rule; noted here for transparency.)
- Newest-clean verdict census at scan time: PASS 30, FAIL 19, gap 1 (of 50).

## 2. Legs launched (max 2 concurrent per bash call; each call ends with `wait`)

| slide | render | leg (one bash call, from repo root, ending `& wait`) | transcript | verdict |
|---|---|---|---|---|
| 013 | `$RJ/slide013/render_w7.png` rendered 08:52:16Z (unique LO profile `lo_w7_013`, TMPDIR=`scratch/tmp`, `pdftoppm -png -r 150 -singlefile`), size **2001x1125** as expected; pptx md5 `244dde61917015d674f650242fa92ae3` | `OCC_MAX=700 ATTEMPTS=10 setsid nohup bash $RJ/vision_leg.sh $RJ/slide013/judge_full_w7.txt 600 $RJ/slide013/render_w7.png $NS/unique_slides/slide_013.jpg "Slide 013 full rejudge W7" "2001x1125 app render vs 960x540 orig" $RJ/payload_A.txt & wait` — launched 08:52:16Z, log `waveW7_launch_013.log`, wrapper out `slide013/judge_full_w7.wrapper.out` | `slide013/judge_full_w7.txt` | **PENDING** |

## 3. Counts

- Slides scanned (001..051 except 025): **50**
- Gap slides found: **1** (013)
- Legs launched: **1** (013) — 0 skipped-already-clean, 49 already clean
- Renders produced: **1** (`slide013/render_w7.png`, 2001x1125)
- Verdicts harvested this wave: **pending** (filled in below after `wait` returns)

## 4. Verdict register (appended after leg completion)

- slide 013 `judge_full_w7.txt`: PENDING
