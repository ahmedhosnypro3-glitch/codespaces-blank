#!/usr/bin/env bash
# scope_r2 fresh-judge runner: storm-resilient, atomic banking, never aborts.
# Recipe aligned with the active fleet lanes (project skill copy + --thinking high +
# --timeout 460, gated through 16_vision_gate.sh): the protocol's bare --timeout 240
# burned the tool's 270s hard wall 2x on gateway-heavy comparison calls with no
# transcript; DEFAULT route kept, no --models, frozen template untouched.
set -u
V=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
R=/home/codespace/ai_llm_slides
TOOL="$R/.agents/skills/image-analysis/scripts/analyze_image.py"
LOG="$V/_pool/storm_log/storm_r2_judge.log"
mkdir -p "$V/_pool/storm_log"
log(){ printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"; }
PROMPT="$(cat "$V/judge_template.txt")"

verdict_ok(){ [ -f "$1" ] && grep -qaE "FINAL VERDICT: ?\*{0,2}(PASS|FAIL)" "$1"; }

for N in "$@"; do
  PNN=$(printf "%03d" "$N")
  OUT="$V/qa/slide${PNN}/rejudge"
  mkdir -p "$OUT"
  attempt=1
  while [ "$attempt" -le 3 ]; do
    T="$OUT/judge_attempt_${attempt}.txt"
    S="$OUT/judge_attempt_${attempt}.stdout.txt"
    log "JUDGE slide=$N attempt=$attempt start"
    ( cd "$R/.agents/skills/image-analysis" && TMPDIR="$V/_pool" timeout 1560 \
      "$R/scripts/16_vision_gate.sh" python3 "$TOOL" comparison \
        "$OUT/render-1.png" "$V/unique_slides/slide_${PNN}.jpg" \
        --view "Slide ${PNN} recreation render vs original lecture frame" \
        --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
        -p "$PROMPT" --thinking high --timeout 460 --max-tokens 65536 \
        --rounds 1 --tries 1 --transcript "$T" > "$S" 2>&1 )
    rc=$?
    if verdict_ok "$T"; then
      log "JUDGE slide=$N attempt=$attempt OK rc=$rc verdict=$(grep -aoE 'FINAL VERDICT:.*' "$T" | tail -1)"
      break
    fi
    log "JUDGE slide=$N attempt=$attempt FAIL rc=$rc transcript=$([ -f "$T" ] && echo yes || echo no) $(grep -aoE 'ABORT [A-Za-z]+:.*|attempt ?[0-9]+:.*' "$S" | tail -1)"
    if [ "$attempt" -lt 3 ]; then
      log "STORM sleep 120s before judge retry slide=$N"
      sleep 120
    fi
    attempt=$((attempt+1))
  done
done
log "JUDGE RUN COMPLETE"
