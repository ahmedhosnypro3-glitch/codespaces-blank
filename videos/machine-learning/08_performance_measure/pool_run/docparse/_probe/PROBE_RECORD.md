# Parse-route probe gate record

Probe law (references/reliability-notes.md): before any heavy call, fire a tiny
cheap probe on the same route. A probe pass = exit 0, non-degenerate transcript,
zero degenerate events. A green probe does NOT guarantee the heavy call — it only
proves the route is alive.

## Probe: probe_001.jpg (320x180 JPEG q90 crop of slide_001.jpg, 3045 bytes)

- command: python3 <skill>/scripts/parse_document.py probe_001.jpg -o <probe dir> --timeout 90
- wall timeout wrapper: `timeout 120` (wrapper), HTTP read timeout 90 s
- start: 2026-10-27 ~22:19
- exit code: 0
- wall: 1 s (probe call itself 0.8 s)
- stderr: none
- transcript: 54 chars, 7 output tokens
- finish_reason: stop
- transcript head: `<x_0.0><y_0.0>4<x_0.0.9971><y_0.9938><class_Page-footer>` (page-number badge region read as a bare digit; expected — the probe is a small corner crop, not a verdict)
- degenerate events: 0

Probe verdict: PASS (route alive). The sliding scale from this probe is tens of
seconds to minutes per heavy call on a contended window.

## Lane parameters adopted for this run

- All 13 target frames are 960x540 px — inside the 1664x2048 recommendation, so NO
  downscale was applied lane-side and the ORIGINAL frames are parsed at native res.
- Parse timeout: 150 s (heavy-lane explicit). Chat timeout: 60 s.
- Fan: cascade_runner's internal bounded pool (--max-parallel 4), plus the
  sanctioned per-worker bounded fan of <=4 in-flight parse calls in one shell
  invocation ending `wait` where a worker drives separate calls itself.
- Budgets: --max-crops 16 --max-parse-calls 24 --max-depth 6 --max-retries 3.
- Retry recipe: one paced (~60 s) single retry into a FRESH call directory; two
  identical hangs in one window => stop the lane and bank the blocker.
