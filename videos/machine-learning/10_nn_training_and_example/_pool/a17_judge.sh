#!/usr/bin/env bash
# scope_a17 comparison-judge dispatcher (MISSION_PROTOCOL 3.8)
# usage: a17_judge.sh <NNN> <attempt> [render_png]
# Judge route: DEFAULT no-params (images alias). glm leg DEFERRED/BLOCKED.
set -u
N="$1"; A="$2"; RENDER="${3:-}"
VD=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SK=/home/codespace/.agents/skills/image-analysis
GATE=/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh
[ -z "$RENDER" ] && RENDER="$VD/qa/slide${N}/render-1.png"
OUT="$VD/qa/slide${N}/judge_attempt_${A}.txt"
mkdir -p "$VD/qa/slide${N}"
cd "$SK" || exit 9
PROMPT="$(cat "$VD/judge_template.txt")"
TMPDIR="$VD/_pool" timeout 300 "$GATE" python3 analyze_image/analyze_image.py comparison \
  "$RENDER" \
  "$VD/unique_slides/slide_${N}.jpg" \
  --view "Slide ${N} recreation render vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in slide (2000x1125px); IMG2=original lecture frame (960x540px)" \
  -p "$PROMPT" --timeout 240 --rounds 1 --tries 1 \
  > "$OUT" 2>&1
rc=$?
echo "slide${N} judge attempt ${A} exit=$rc -> $OUT"
exit 0
