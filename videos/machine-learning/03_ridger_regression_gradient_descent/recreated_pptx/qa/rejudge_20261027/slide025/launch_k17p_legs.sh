#!/usr/bin/env bash
# launch_k17p_legs.sh — launch the k17p crop judge leg (full already running).
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide025
N=025
mkdir -p "$RJ/legs_20261031.pids"

OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$D/crop_dense_judge_k17p.txt" 600 \
  "$D/crop_dense_render_k17p.png" "$D/crop_dense_orig_k17p.png" \
  "Slide 25 zoomed crop — fidelity check vs original (k17p)" \
  "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
  "$RJ/payload_B_$N.txt" > "$D/crop_dense_judge_k17p.wrapper.out" 2>&1 < /dev/null &
PID=$!
echo "$PID" > "$RJ/legs_20261031.pids/${N}_crop_k17p.pid"
echo "launched crop_k17p pid $PID"
date -u +%Y-%m-%dT%H:%M:%SZ
