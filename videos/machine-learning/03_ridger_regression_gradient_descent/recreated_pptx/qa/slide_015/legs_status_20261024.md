# Legs status — slide 015, attempt 4 (judge legs; live run)

Worker `w015-buildfirst-20261024`. This file is the LIVE congestion record for
the verdict legs. It is updated as the run proceeds; the final adjudication and
certification outcome is appended to `worker_report.md`.

## Root cause of the previous run's failure (diagnosed 2026-10-24)

The first gate-policed run **did dispatch legs** — the count reached 7 at
14:45 UTC and 4 at 14:51. Every dispatch then failed within ~1 s with

```
HTTP 504 {"error":{"code":"upstream_timeout","ironrouter":
{"provider":"Nvidia","message":"the upstream provider timed out"}}}
[info] 0/1 result(s) analyzed successfully
```

So the earlier "congestion" diagnosis was wrong in kind: this was an **upstream
NIM timeout**, not gateway saturation. The one wall-extension retry
(`--timeout 1200` on the banked judgeA payload, byte-identity verified by
`scratch/tmp/wallext_check.sh`) aborted at the script's own hard wall-clock
(1230 s, `HangError ... abort+retry 1/3`) and the tool itself warns that
`--timeout > 600s` saturates the shared gateway for everyone. **No transcript
file was ever written by any attempt** (`probe_4.txt`, `judge_attempt_4.txt`
and `crop_4_*_judge.txt` all absent), so nothing garbage was banked.

Final runner `scratch/tmp/lorch15_final.sh` therefore uses the **banked
unmodified dispatches at `--timeout 600`** — the payloads are the frozen,
byte-checked ones. Its log is `qa/slide_015/final_legs_status.txt`; per-leg
logs are `qa/slide_015/judgeA_final.log` and `qa/slide_015/crop_<slug>_final.log`.

### Client-retry resilience (payload still untouched)

A 504 is a transient upstream fault, not a verdict, so the runner raises the
**client** retry count only: `--tries 1` → `--tries 3`. The judgment payload
is provably unaffected — `scratch/tmp/tries_check.sh` asserts, before every
call, that the `-p` string is byte-identical to the banked dispatch and that
`--tries` is the ONLY difference anywhere in the file. Verified for all six
dispatches:

```
TRIES-OK: --tries 1 -> 3, -p payload byte-identical   (judgeA + all 5 crops)
```

The `--timeout` stays at the banked 600 s (the script itself warns that
`--timeout > 600s` saturates the shared gateway for everyone).

## Observed gateway load (fleet-global, `pgrep -c -f analyze_image.py`)

All observations are from the same run; times are UTC.

| time | gate | note |
|---|---|---|
| 11:09 | 9 | first probe this session |
| 11:11 | 8 | |
| 11:13 | 12 | |
| 11:22 | 17 | |
| 11:28 | 25 | |
| 11:30 | 22 | legs run #1 start |
| 11:46 | 20 | |
| 11:50 | 17 | |
| 11:54 | 15 | |
| 11:58 | 13 | lowest observed; still > 8 |
| 12:02 | 14 | |
| 12:10 | 22 | |
| 12:18 | 22 | legs run #1 tool-wall killed (no vision call ever dispatched) |
| 12:25 | 51 | peak |
| 12:2x | 44-48 | legs run #2 start (4h patient wait) |

**No vision call has been dispatched from this worker at any point**: the gate
never read `< 8`. Per gate law no leg was forced through, so **no
`FINAL VERDICT:` line exists for slide 015** and the slide is NOT certified.

The 14-25 concurrent `analyze_image.py` are **sibling lanes of deck 03 itself**
(measured via `ps`), not load from other decks — i.e. the congestion is local
to this deck's remaining slides, and it is not caused by this worker.

## What was verified independently (non-vision, banked, this session)

Re-measured on `render_4.png` vs `unique_slides/slide_015.jpg` with a fresh
script (`scratch/tmp/adjud_015_generic.py`, frame-px boxes, render scaled by
2001/960, both images sampled at equal effective scale):

| region | width ratio r/orig | height ratio | verdict |
|---|---|---|---|
| eq1_l1 | 0.88 | ~1.16 | forced narrow — see below |
| eq1_l2 | 0.87 | ~1.21 | forced narrow — see below |
| eq1_l3 | 0.90 | ~1.14 | forced narrow — see below |
| redbox_eq | 0.98 | — | matches the banked ratio 1.00 |
| normal | 0.93 | 1.00 | |
| solution | 0.76 | ~0.9 | forced narrow — see below |
| redbox_sent | 0.99 | 0.70 | line height only |
| deriv_l1 | 0.99 | 0.91 | |
| deriv_l2 | 0.97 | 1.00 | |
| peach_eq | 0.97 | 0.82 | |
| Remember | 1.02 | 0.65 | |

These reproduce the banked numbers exactly (eq1 0.87-0.90, solution 0.76),
which is the pre-condition for refuting any repeat finding.

### Geometric forcing, re-proved

Matching the original's width at the render's own ink aspect ratio would
require more ink height than the enclosing band allows, so the narrow widths
are forced rather than fixable:

| region | render wxh | aspect | orig width | height needed | band available |
|---|---|---|---|---|---|
| eq1_l1 | 610x50 | 12.20 | 694 | 56.9 | 44 |
| eq1_l2 | 575x51 | 11.27 | 663 | 58.8 | 47 |
| eq1_l3 | 500x51 | 9.80 | 555 | 56.6 | 45 |
| solution | 248x36 | 6.89 | 325 | 47.2 | 40 (green box interior) |

Each needed height exceeds its band, so widening to the original's width makes
the stacked lines collide / overflows its box. Recorded, not "fixed".

### Arrow adjudication re-confirmed

`adjud_015_generic.py arrow_gap` on the *strictly interior* gap
`x511..546, y466..521` at `luma<200`: **0 ink px in the original** (and 0 in the
render). The claimed right-pointing arrow after the normal-equation line does
not exist. Never add it.

Note for future measurements: measuring a gap that *includes* the boundary
columns (x510 or x547) picks up the equation's closing paren and the green
box's left edge and yields a false ~45 px signal. Interior-only measurement is
the correct one, and the correct one says zero.

### Crop pairs (fairness precondition)

All five pairs are exactly co-dimensioned, so no drift can be fabricated by
scale mismatch: eq_stack 1481x358, pinkbox 1329x121, peachbox 242x140,
deriv_stack 933x277, solution 727x121 (render and orig identical in each).

## Resume commands (nothing to redo; the bank is intact)

```bash
cd <repo root>
pgrep -c -f analyze_image.py            # must read < 8 before ANY call

# whole leg sequence, gate-policed, 4h patience per leg:
bash scratch/tmp/lorch15_main.sh        # probe -> judgeA (this file's live run)
bash scratch/tmp/lorch15_crops.sh       # the five Procedure B crop legs

# or leg by leg, exactly as banked:
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/dispatch_driver_4.sh probe
bash .../dispatch_driver_4.sh judgeA
bash .../dispatch_driver_4.sh crop eq_stack   # then pinkbox peachbox deriv_stack solution
```

Legs land at `qa/slide_015/probe_4.txt`, `judge_attempt_4.txt` and
`crop_4_<slug>_judge.txt`. A leg counts only when its transcript carries a real
`FINAL VERDICT:` line.

## Certification sequence (unchanged, for whoever lands the verdicts)

`claim()` resets `gen_status` to `building` (`scripts/15_progress.py:337`), so
`set gen_status passed` must be the LAST content write before `release`, and
`get 15` must be re-read after it. Final row must read
`gen_status=passed`, `visual_check=PASS`, `worker_id=""`.

### Full congestion log from the first run (12:42-15:22 UTC)

```
[12:42:32] === leg run start (attempt 4) ===
[12:42:32] gate=32
[12:42:32]   heartbeat
[12:43:32] gate=33
[12:44:32] gate=41
[12:45:32] gate=39
[12:46:32] gate=38
[12:46:32]   heartbeat
[12:47:32] gate=37
[12:48:32] gate=36
[12:49:32] gate=38
[12:50:32] gate=38
[12:50:32]   heartbeat
[12:51:33] gate=43
[12:52:33] gate=49
[12:53:33] gate=52
[12:54:33] gate=47
[12:54:33]   heartbeat
[12:55:33] gate=50
[12:56:33] gate=62
[12:57:33] gate=52
[12:58:33] gate=49
[12:58:33]   heartbeat
[12:59:33] gate=49
[13:00:33] gate=43
[13:01:33] gate=46
[13:02:33] gate=43
[13:02:33]   heartbeat
[13:03:33] gate=49
[13:04:33] gate=48
[13:05:33] gate=49
[13:06:33] gate=44
[13:06:34]   heartbeat
[13:07:34] gate=46
[13:08:34] gate=44
[13:09:34] gate=41
[13:10:34] gate=31
[13:10:34]   heartbeat
[13:11:34] gate=32
[13:12:34] gate=28
[13:13:34] gate=24
[13:14:34] gate=27
[13:14:34]   heartbeat
[13:15:34] gate=26
[13:16:34] gate=24
[13:17:34] gate=23
[13:18:34] gate=23
[13:18:34]   heartbeat
[13:19:34] gate=24
[13:20:34] gate=24
[13:21:34] gate=24
[13:22:34] gate=22
[13:22:34]   heartbeat
[13:23:34] gate=19
[13:24:34] gate=19
[13:25:34] gate=22
[13:26:35] gate=14
[13:26:35]   heartbeat
[13:27:35] gate=16
[13:28:35] gate=18
[13:29:35] gate=16
[13:30:35] gate=16
[13:30:35]   heartbeat
[13:31:35] gate=16
[13:32:35] gate=13
[13:33:35] gate=17
[13:34:35] gate=16
[13:34:35]   heartbeat
[13:35:35] gate=16
[13:36:35] gate=19
[13:37:35] gate=16
[13:38:35] gate=21
[13:38:35]   heartbeat
[13:39:36] gate=20
[13:40:36] gate=21
[13:41:36] gate=22
[13:42:36] gate=23
[13:42:36]   heartbeat
[13:43:36] gate=23
[13:44:36] gate=20
[13:45:36] gate=22
[13:46:36] gate=19
[13:46:36]   heartbeat
[13:47:36] gate=17
[13:48:36] gate=17
[13:49:36] gate=13
[13:50:36] gate=13
[13:50:36]   heartbeat
[13:51:36] gate=14
[13:52:36] gate=13
[13:53:36] gate=13
[13:54:36] gate=13
[13:54:36]   heartbeat
[13:55:36] gate=13
[13:56:36] gate=13
[13:57:36] gate=13
[13:58:36] gate=12
[13:58:37]   heartbeat
[13:59:37] gate=9
[14:00:37] gate=11
[14:01:37] gate=10
[14:02:37] gate=11
[14:02:37]   heartbeat
[14:03:37] gate=11
[14:04:37] gate=11
[14:05:37] gate=9
[14:06:37] gate=9
[14:06:37]   heartbeat
[14:07:37] gate=10
[14:08:37] gate=14
[14:09:37] gate=11
[14:10:37] gate=10
[14:10:37]   heartbeat
[14:11:37] gate=9
[14:12:37] gate=15
[14:13:37] gate=15
[14:14:38] gate=12
[14:14:38]   heartbeat
[14:15:38] gate=12
[14:16:38] gate=11
[14:17:38] gate=17
[14:18:38] gate=9
[14:18:38]   heartbeat
[14:19:38] gate=12
[14:20:38] gate=9
[14:21:38] gate=9
[14:22:38] gate=10
[14:22:38]   heartbeat
[14:23:38] gate=12
[14:24:38] gate=12
[14:25:38] gate=12
[14:26:38] gate=12
[14:26:38]   heartbeat
[14:27:38] gate=12
[14:28:38] gate=10
[14:29:38] gate=10
[14:30:38] gate=11
[14:30:38]   heartbeat
[14:31:38] gate=11
[14:32:38] gate=12
[14:33:38] gate=11
[14:34:38] gate=11
[14:34:39]   heartbeat
[14:35:39] gate=11
[14:36:39] gate=10
[14:37:39] gate=10
[14:38:39] gate=10
[14:38:39]   heartbeat
[14:39:39] gate=10
[14:40:39] gate=8
[14:41:39] gate=11
[14:42:39] gate=12
[14:42:39]   heartbeat
[14:43:39] gate=9
[14:44:39] gate=9
[14:45:39] gate=7
[14:45:39] gate drained (7)
[14:45:39] dispatching probe (gate 7)
[14:46:40]   probe exit=1
[14:46:40]   probe NO VERDICT (rc=1) - one wall-extension retry permitted
[14:46:40] probe produced no transcript - one re-probe after sleep 300 (driver law)
[14:51:40] gate=4
[14:51:40] gate drained (4)
[14:51:40] dispatching probe2 (gate 4)
[14:52:42]   probe2 exit=1
[14:52:42]   probe2 NO VERDICT (rc=1) - one wall-extension retry permitted
[14:52:42] gate=6
[14:52:42] gate drained (6)
[14:52:42] dispatching judgeA (gate 6)
[14:53:43]   judgeA exit=1
[14:53:43]   judgeA NO VERDICT (rc=1) - one wall-extension retry permitted
[14:53:43] gate=6
[14:53:43] gate drained (6)
[14:53:43] WALLEXT-OK: only timeout 600->1200 - payload byte-identical
[14:53:43] retry judgeA with --timeout 1200 (gate 6)
[15:22:03]   judgeA retry still no verdict (rc=124)
[15:22:03] === judgeA outcome rc=2 ===
[15:22:03] DONE
```

### Final runner log (15:39-16:39 UTC, gate never < 8)

```
[16:18:24] gate=18
[16:19:24] gate=14
[16:20:24] gate=14
[16:21:24] gate=16
[16:22:24] gate=15
[16:23:24] gate=16
[16:24:24] gate=12
[16:24:24]   heartbeat
[16:25:24] gate=14
[16:26:24] gate=15
[16:27:24] gate=14
[16:28:24] gate=18
[16:29:24] gate=14
[16:30:24] gate=18
[16:31:24] gate=16
[16:32:24] gate=12
[16:33:24] gate=13
[16:34:24] gate=12
[16:35:24] gate=24
[16:36:24] gate=15
[16:37:24] gate=15
[16:38:24] gate=11
[16:39:24] gate=17
[16:39:25]   heartbeat
```
