#!/bin/bash
# Leg 1 driver for slide 033 — full-slide Template A judge.
#
# Metric: `pgrep -c -f analyze_image.py` ALSO matches the gate wrapper, the
# `timeout 1700` shell and any bash -c that merely names the script — three
# processes per real call. Measured 2026-10-24 15:05 with only TWO real
# in-flight calls (lanes 015, 051): pgrep -f = 8, real python3 clients = 2.
# Slide 030's proven driver (`dispatch_legs_6_v3.sh`, which landed today's only
# heavy verdict) therefore gates on the REAL client count:
#   ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/'
# The gate's own flock (16 slots) remains the authoritative throttle.
#
# 504 handling: `upstream_timeout` from Nvidia is an upstream failure, not a
# judge FAIL and not an attempt. It fast-fails in ~60s, so a retry is cheap and
# is not the forbidden "retry loop around the gate" — the orchestrator's wall
# (--timeout 1200 inside `timeout 1700`) is preserved on every call and the
# payload bytes are unchanged (md5 re-verified each attempt).
set -u
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033
V=videos/machine-learning/03_ridger_regression_gradient_descent
LOG=$Q/leg1_driver_k9.log

real_clients() { ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }

MAXTRY=14
for t in $(seq 1 $MAXTRY); do
  if [ -s "$Q/judge_attempt_9.txt" ]; then
    echo "[$(date '+%T')] transcript exists ($(wc -c < "$Q/judge_attempt_9.txt") bytes) — stop"
    break
  fi
  rc=$(real_clients)
  pg=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0)
  echo "[$(date '+%T')] try#$t real_clients=$rc pgrep_f=$pg"
  if [ "$rc" -ge 8 ]; then
    echo "[$(date '+%T')]   gate saturated on real clients ($rc) — sleep 120"
    sleep 120
    continue
  fi
  echo "[$(date '+%T')]   firing (real clients=$rc, gate flock arbitrates)"
  bash scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/render_9.png $V/unique_slides/slide_033.jpg \
    --view "Slide 33 recreation — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript $Q/judge_attempt_9.txt \
    -p "$(cat $Q/judge_payload_A_k9.txt)" >> "$LOG" 2>&1
  echo "[$(date '+%T')]   exit=$?"
  if [ -s "$Q/judge_attempt_9.txt" ]; then
    echo "[$(date '+%T')]   TRANSCRIPT LANDED ($(wc -c < "$Q/judge_attempt_9.txt") bytes)"
    break
  fi
  echo "[$(date '+%T')]   no transcript (upstream error) — backoff 90s"
  sleep 90
done
echo "[$(date '+%T')] driver done"
