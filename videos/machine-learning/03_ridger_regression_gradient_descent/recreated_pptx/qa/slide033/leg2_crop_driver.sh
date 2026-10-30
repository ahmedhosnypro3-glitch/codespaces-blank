#!/bin/bash
# Leg 2 driver — Procedure B zoomed crop-pair judges, slide 033, attempt 9.
# Usage: leg2_crop_driver.sh [region ...]   (default: plot table center — the
# three DENSE regions of this slide: curve+markers, table numbers, equation.
# "title" is plain 3-line text, not a dense region; include it only on request.)
#
# Gating (same refined metric as the banked leg1_driver_k9.sh, which landed
# fleet-wide precedent today): pgrep -f analyze_image.py ALWAYS counts 3
# processes per real call (gate wrapper + timeout shell + bash -c that names
# the script), so the fleet "pgrep 40-42" is ~14 real clients. The gate's own
# flock (16 slots) is the authoritative throttle. This driver waits until
#   ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/'  < 8
# before each call and heartbeats the progress DB while waiting.
#
# Failure handling: upstream 504/HangError is not a judge FAIL. Each region
# gets up to 3 spaced attempts (240s apart); payload bytes never change
# (md5 0b5a221e...), the orchestrator wall is preserved on every call
# (--timeout 1200 inside `timeout 1700`, --rounds 1 --tries 1). This is a
# bounded re-probe policy, NOT a retry loop around the gate.
set -u
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp   # deck AGENTS.md scratch/QA law
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
V=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$V/recreated_pptx/qa/slide033
PAY=$Q/judge_payload_B_k9.txt
LOG=$Q/leg2_driver_k9.log
REGIONS="${*:-plot table center}"

real_clients() { ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }
hb() { VIDEO=$V python3 scripts/15_progress.py heartbeat 33 w033-fresh-20261024 >/dev/null 2>&1; }

wait_for_slot() {
  for i in $(seq 1 12); do
    rc=$(real_clients)
    if [ "$rc" -lt 8 ]; then echo "[$(date '+%T')] slot free (real_clients=$rc)"; return 0; fi
    echo "[$(date '+%T')] saturated real_clients=$rc — wait 120 (iter $i)"; hb; sleep 120
  done
  echo "[$(date '+%T')] no slot after 24 min — PARK region $1"; return 1
}

fire() { # $1 region
  bash scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/crop_9_${1}_render.png $Q/crop_9_${1}_orig.png \
    --view "Slide 33 zoomed crop ${1} — render vs original at matched scale (attempt 9)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript $Q/crop_9_${1}_judge.txt \
    -p "$(cat $PAY)"
}

for R in $REGIONS; do
  if [ -s "$Q/crop_9_${R}_judge.txt" ]; then
    echo "[$(date '+%T')] $R: transcript already present ($(wc -c < "$Q/crop_9_${R}_judge.txt") bytes) — skip"; continue
  fi
  for t in 1 2 3; do
    echo "[$(date '+%T')] $R attempt $t: real_clients=$(real_clients)"
    if ! wait_for_slot "$R"; then echo "[$(date '+%T')] $R PARKED (no slot)"; break; fi
    hb
    echo "[$(date '+%T')] $R firing"
    fire "$R" >> "$LOG" 2>&1
    echo "[$(date '+%T')] $R exit=$?"
    if [ -s "$Q/crop_9_${R}_judge.txt" ]; then
      echo "[$(date '+%T')] $R TRANSCRIPT LANDED ($(wc -c < "$Q/crop_9_${R}_judge.txt") bytes)"; break
    fi
    echo "[$(date '+%T')] $R no transcript (upstream error) — 240s backoff"; sleep 240
  done
done
echo "[$(date '+%T')] leg2 driver done"
echo "FINAL LEG2 STATE:"
for R in $REGIONS; do
  if [ -s "$Q/crop_9_${R}_judge.txt" ]; then echo "  $R: LANDED $(wc -c < "$Q/crop_9_${R}_judge.txt") bytes"; else echo "  $R: NO TRANSCRIPT"; fi
done
