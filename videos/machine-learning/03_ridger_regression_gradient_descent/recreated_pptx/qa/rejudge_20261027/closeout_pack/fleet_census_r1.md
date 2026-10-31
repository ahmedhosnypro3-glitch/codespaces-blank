# Fleet census r1 — read-only, subagent

Timestamp (UTC): 2026-10-31 08:35:11 UTC (`date -u`)
NS = videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027

## 1. Running processes (ps -eo args, self-excluding grep)

- vision_leg.sh wrapper procs: **404**
- analyze_image.py procs: **705**
- soffice procs: **10**

## 2. Rejudge transcript status (per slideNNN dir under NS)

- slide dirs: **57**
- total files inside slide dirs: **4073**
- files containing 'FINAL VERDICT': **1796**
- ...of which also contain the string '429': 574 (mostly "no 429" harvest-log lines, not errors)
- dirs with >=1 FINAL VERDICT transcript (done): **51**
- dirs with NO verdict transcript (pending): **6** — slide03, slide05, slide10, slide12, slide13, slide17
- FINAL VERDICT lines across slide dirs: 5397 total — PASS 3770, FAIL 1627 (multiple rounds per file; line count > file count)

## 3. Gateway pressure (429 / rate-limit lines)

- lines containing '429' anywhere in NS: 8454 (includes "no 429" log text)
- true error-style lines: HTTP 429 = **20**, upstream_rate_limited = **18**
- in the **newest 30 files** by mtime: **0** HTTP-429/rate-limit lines (125 lines mention 429 but all are "no 429" harvest-log text) — pressure currently LOW at the frontier

## 4. Disk

- `df -h /home/codespace`: overlay 32G total, 26G used, **3.8G avail, 88% full**

## 5. Watchdog / monitor last-fire evidence (file mtimes, newest first)

- 2026-10-31 08:35:54 slide025/MONITOR_k17z2.log
- 2026-10-31 08:35:21 fix_watch_033_051.log
- 2026-10-31 08:34:28 slide025/watch_r22.log
- 2026-10-31 08:33:17 slide025/promoter_k17b_watch.log
- 2026-10-31 08:33:12 slide025/watch_k17_poll.out (+ .watch_k17_poll_sigs)
- (older) 07:53:09 slide025/.watch_k17_poll_probed, watch_k17.log; 07:52:58 pil_k17z2_render_census.txt
- Newest file in NS overall: 2026-10-31 08:36:05 slide021/judge_full_r17.txt(.log) — fleet actively writing ~seconds before census

Cron registration cannot be checked from a subagent; mtime evidence shows watchdog/monitor activity within the last ~3 minutes.
