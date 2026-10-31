#!/usr/bin/env bash
# b12 judge dispatcher: slide 23 (current build) + slide 24 attempt4, via namespace gate.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
SK=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$(cat judge_template.txt)"
CAP="13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame"

judge() { # $1 slide num, $2 render png, $3 out file, $4 view
  ./_pool/vision_gate.sh timeout 540 python3 "$SK" comparison "$2" "unique_slides/slide_$1.jpg" \
    --view "$4" --capture "$CAP" -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$3" 2>&1
  echo "$(date +%T) rc=$? bytes=$(wc -c < "$3") -> $3" >> _pool/b12_judge.status
}

echo "=== b12 judge dispatch $(date +%T) ===" >> _pool/b12_judge.status
judge 024 qa/slide024/attempt4/render-1.png qa/slide024/attempt4/judge_attempt_1.txt \
  "Slide 024 recreation render vs original lecture frame" &
sleep 15
judge 023 qa/slide023/attempt_r2/render-1.png qa/slide023/attempt_r2/judge_attempt_1.txt \
  "Slide 023 recreation render vs original lecture frame" &
wait
echo "=== b12 judge done $(date +%T) ===" >> _pool/b12_judge.status
for f in qa/slide024/attempt4/judge_attempt_1.txt qa/slide023/attempt_r2/judge_attempt_1.txt; do
  echo "--- $f"; grep -i "FINAL VERDICT" "$f" || echo "(no verdict line)"
done >> _pool/b12_judge.status 2>&1
