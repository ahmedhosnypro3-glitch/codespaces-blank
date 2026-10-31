#!/usr/bin/env bash
# judge_s16.sh <K> <transcript_name> <render_png_name>
# Original-first judge for slide 16 of 08_performance_measure, via fleet vision gate.
set -u
export PYTHONUNBUFFERED=1
REPO=/home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
PYBIN=/home/codespace/.pyenv/versions/3.15.2/bin/python3
K=$1; TNAME=$2; RNAME=$3
QA=$NS/recreated_pptx/qa/slide016
cd "$REPO"
bash scripts/16_vision_gate.sh timeout 540 "$PYBIN" \
  .agents/skills/image-analysis/scripts/analyze_image.py \
  comparison "$NS/unique_slides/slide_016.jpg" "$NS/recreated_pptx/qa/slide016/$RNAME" \
  --view "Slide 16 recreation — judge read vs original lecture frame (08_performance_measure, attempt $K)" \
  --capture "IMG1=original lecture video frame 960x540 (ground truth, read FIRST); IMG2=150dpi PNG render of 13.33x7.5in PPTX recreation (read SECOND)" \
  --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
  --transcript "$QA/$TNAME" \
  -p "$(cat "$NS/pool_run/judge_prompt_template.txt")" \
  > "$QA/${TNAME%.txt}.log" 2>&1
echo "rc=$?"
