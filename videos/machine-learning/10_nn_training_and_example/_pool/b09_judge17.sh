#!/usr/bin/env bash
# b09 slide-17 fresh judge: probe (short wall) then the real comparison call with
# a wide outer wall (gate slots are held by the fleet; the inner wall stays 540).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/.agents/skills/image-analysis
cd "$NS" || exit 1
PROMPT="$(cat "$NS/judge_template.txt")"

# 1) probe on an already-banked PNG (short wall)
timeout 400 ./_pool/vision_gate.sh timeout 300 \
  python3 "$SKILL/scripts/analyze_image.py" analysis \
  qa/slide017/render-1.png -p "Reply with the single word READY" \
  --timeout 240 --rounds 1 --tries 1 > _pool/b09_probe_17.txt 2>&1
echo "probe rc=$? bytes=$(wc -c < _pool/b09_probe_17.txt) $(date +%T)"

# 2) the comparison judge (IMG1 = recreation render, IMG2 = original frame)
timeout 1800 ./_pool/vision_gate.sh timeout 540 \
  python3 "$SKILL/scripts/analyze_image.py" comparison \
  qa/slide017/rejudge/attempt2/render-1.png unique_slides/slide_017.jpg \
  --view "Slide 017 recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > qa/slide017/rejudge/judge_attempt_4.txt 2>&1
echo "judge17 rc=$? bytes=$(wc -c < qa/slide017/rejudge/judge_attempt_4.txt) $(date +%T)"
grep -a 'FINAL VERDICT' qa/slide017/rejudge/judge_attempt_4.txt || echo "NO VERDICT"
