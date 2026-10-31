#!/usr/bin/env bash
# b04 fresh rejudge dispatch: slide 7 (IMG1=fresh render of current deliverable) and
# slide 8 (IMG1=fresh render of the top-level deliverable WITH the 2D equation PNG).
# Two concurrent jobs in ONE call ending wait, ~15s spacing, gate-mandatory.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS"
PROMPT="$(cat judge_template.txt)"

run_one() { # $1=slide N, $2=IMG1 render
  local N="$1" IMG1="$2"
  local OUT="$NS/qa/slide${N}/rejudge/judge_r6_attempt_1.txt"
  build_log="$NS/_pool/b04/judge_${N}.log"
  {
    echo "=== judge dispatch slide $N $(date +%F\ %T) IMG1=$IMG1 ==="
    timeout 2400 ./_pool/vision_gate.sh timeout 2300 \
      python3 "$SKILL" comparison \
      "$IMG1" "$NS/unique_slides/slide_${N}.jpg" \
      --view "Slide ${N} recreation render vs original lecture frame (fresh audit 2026-10-30, scope b04)" \
      --capture "IMG1=150dpi PNG render (2001x1125) of the current certified deliverable; IMG2=original lecture frame 960x540" \
      -p "$PROMPT" --timeout 2100 --rounds 1 --tries 1 \
      > "$OUT" 2>&1
    echo "rc=$? $(date +%F\ %T)"
  } >> "$build_log" 2>&1
}

run_one 007 "$NS/_pool/b04/render/s007-1.png" &
sleep 15
run_one 008 "$NS/_pool/b04/render/s008top-1.png" &
wait
echo "ALL JUDGE JOBS DONE $(date +%F\ %T)"
