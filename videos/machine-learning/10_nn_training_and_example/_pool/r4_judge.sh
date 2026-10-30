#!/usr/bin/env bash
# scope_r4 step-4 dispatcher: frozen-template comparison judge for one slide.
# usage: r4_judge.sh <NNN> <attempt> [per_req_timeout=240] [wall=300] [render_png=.../render-1.png]
set -u
N="$1"; A="$2"; TO="${3:-240}"; WALL="${4:-300}"
RENDER="${5:-}"
VID="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SKILL="/home/codespace/.agents/skills/image-analysis"
PROMPT="$(cat "$VID/judge_template.txt")"
mkdir -p "$VID/qa/slide$N/rejudge"
if [ -z "$RENDER" ]; then RENDER="$VID/qa/slide$N/rejudge/render-1.png"; fi
cd "$SKILL" || exit 9
timeout "$WALL" python3 analyze_image/analyze_image.py comparison \
  "$RENDER" \
  "$VID/unique_slides/slide_$N.jpg" \
  --view "Slide $((10#$N)) recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout "$TO" --rounds 1 --tries 1 \
  > "$VID/qa/slide$N/rejudge/judge_attempt_$A.txt" 2>&1
echo "r4_judge slide=$N attempt=$A exit=$? render=$RENDER file=qa/slide$N/rejudge/judge_attempt_$A.txt"
