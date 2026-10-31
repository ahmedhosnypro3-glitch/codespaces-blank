#!/usr/bin/env bash
# b13 redo: regenerate audit2/slide_026.txt (429 stub) and bank a complete
# FINAL VERDICT transcript for slide 025 on the attempt2 build (the build that
# adds the w/node labels the blocked-out a3 verdict flagged as a fidelity gap).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
LOG="$NS/_pool/b13_redo.log"
PROMPT="$(cat "$NS/_pool/audit_prompt.txt")"
JPROMPT="$(cat "$NS/judge_template.txt")"
ERRS='HTTP 429|HTTP 502|HTTP 504|Connection error|HangError|Garbage|EmptyStream|every model failed|Traceback|No such file'

audit_ok() { grep -q '\[winner\]' "$1" 2>/dev/null && [ "$(wc -c < "$1" 2>/dev/null || echo 0)" -ge 4000 ]; }
judge_pass() { grep -q '\[winner\]' "$1" 2>/dev/null && grep -qi 'FINAL VERDICT: PASS' "$1" && [ "$(wc -c < "$1")" -ge 4000 ]; }
judge_final() { grep -qi 'FINAL VERDICT' "$1" 2>/dev/null; }

audit26() {
  local out="$NS/_pool/audit2/slide_026.txt" i
  for i in 1 2 3 4; do
    timeout 1800 env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
      python3 "$SKILL/scripts/analyze_image.py" analysis "$NS/unique_slides/slide_026.jpg" \
      --timeout 1500 --rounds 1 --tries 1 \
      --view "Slide 026 — 'Neural Network Training and Example' lecture slide, printed badge 026" \
      --capture "960x540 CSS px, 1x scale, lecture video frame" \
      -p "$PROMPT" > "$out.tmp" 2>&1
    mv "$out.tmp" "$out"
    if audit_ok "$out"; then echo "audit26 OK $(wc -c < "$out")B try=$i $(date +%T)" >> "$LOG"; return 0; fi
    echo "audit26 invalid $(wc -c < "$out")B try=$i $(date +%T) — storm sleep 120" >> "$LOG"
    [ "$i" -lt 4 ] && sleep 120
  done
  echo "audit26 FAILED after 4 tries $(date +%T)" >> "$LOG"; return 1
}

judge_one() { # $1 render path, $2 out path
  timeout 2400 env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" comparison "$1" "$NS/unique_slides/slide_025.jpg" \
    --view "Slide 025 recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    --max-tokens 20000 --timeout 1500 --rounds 1 --tries 1 \
    -p "$JPROMPT" > "$2.tmp" 2>&1
  mv "$2.tmp" "$2"
}

judge25() {
  local renders=("$NS/qa/slide025/attempt2/render-1.png" "$NS/qa/slide025/render/render-1.png")
  local outs=("$NS/qa/slide025/judge_attempt_4.txt" "$NS/qa/slide025/judge_attempt_5.txt")
  local r o i j
  for j in 0 1; do
    r="${renders[$j]}"; o="${outs[$j]}"
    for i in 1 2 3 4; do
      judge_one "$r" "$o"
      echo "judge25 try=$i render=$(basename "$(dirname "$r")") bytes=$(wc -c < "$o") $(date +%T)" >> "$LOG"
      if judge_pass "$o"; then echo "judge25 PASS $(basename "$o")" >> "$LOG"; return 0; fi
      # genuine FAIL verdict from the model = no storm retry; provider errors = retry
      if judge_final "$o" && ! grep -Eq "$ERRS" "$o"; then echo "judge25 FAIL $(basename "$o")" >> "$LOG"; break; fi
      [ "$i" -lt 4 ] && sleep 120
    done
  done
  return 1
}

echo "=== b13 redo start $(date +%F' '%T) ===" >> "$LOG"
audit26 & A=$!
sleep 15
judge25 & J=$!
wait $A; ra=$?
wait $J; rj=$?
echo "=== b13 redo done audit=$ra judge=$rj $(date +%F' '%T) ===" >> "$LOG"
