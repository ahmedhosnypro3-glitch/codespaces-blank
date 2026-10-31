#!/usr/bin/env bash
# Judge attempt 3 for slides 21 and 22 (b11) — frozen template verbatim,
# mandatory vision gate, default route (no --models), banked to files.
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example || exit 1
AI=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$(cat judge_template.txt)"

./_pool/vision_gate.sh timeout 540 python3 "$AI" \
  comparison qa/slide021/rejudge/v3/render-1.png unique_slides/slide_021.jpg \
  --view "Slide 021 recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
  > qa/slide021/rejudge/judge_attempt_3.txt 2>&1 &
P1=$!
sleep 15
./_pool/vision_gate.sh timeout 540 python3 "$AI" \
  comparison qa/slide022/rejudge/v3/render-1.png unique_slides/slide_022.jpg \
  --view "Slide 022 recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
  > qa/slide022/rejudge/judge_attempt_3.txt 2>&1 &
P2=$!
wait $P1 $P2
echo "judge attempts done $(date +%F\ %T)"
grep -h "FINAL VERDICT" qa/slide02{1,2}/rejudge/judge_attempt_3.txt
