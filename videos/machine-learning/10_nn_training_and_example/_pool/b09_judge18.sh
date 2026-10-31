#!/usr/bin/env bash
# b09 slide-18 attempt1 fresh judge (wide outer wall; inner wall 540 per protocol).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/.agents/skills/image-analysis
cd "$NS" || exit 1
PROMPT="$(cat "$NS/judge_template.txt")"
timeout 1800 ./_pool/vision_gate.sh timeout 540 \
  python3 "$SKILL/scripts/analyze_image.py" comparison \
  qa/slide018/rejudge/attempt1/render-1.png unique_slides/slide_018.jpg \
  --view "Slide 018 recreation render (attempt1) vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > qa/slide018/rejudge/attempt1/judge_attempt_1.txt 2>&1
echo "judge18 rc=$? bytes=$(wc -c < qa/slide018/rejudge/attempt1/judge_attempt_1.txt) $(date +%T)"
grep -a 'FINAL VERDICT' qa/slide018/rejudge/attempt1/judge_attempt_1.txt || echo "NO VERDICT"
