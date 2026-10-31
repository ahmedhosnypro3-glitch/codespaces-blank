#!/usr/bin/env bash
# Fresh vision RE-ANALYSIS of every unique frame via the image-analysis skill script.
# Background task (NOT a subagent), per founder directive. Banks one transcript per
# slide into analysis/reanalysis_skill/ — banked evidence is never overwritten.
# Uses the namespace vision gate; the shared gateway is stormed fleet-wide.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
OUTDIR=analysis/reanalysis_skill
PROMPT=$NS/_pool/audit_prompt.txt
LOG=$NS/_pool/reanalysis_skill.log
mkdir -p "$OUTDIR"
: > "$LOG"
log(){ echo "$(date +%F\ %T) $*" >> "$LOG"; }
# Each parallel worker holds ONE gate slot: xargs -P3 == 3 concurrent vision calls.
export VISION_SLOTS=1

run_one(){
  local n="$1"
  local out="$OUTDIR/slide_${n}.analysis.txt"
  if [ -s "$out" ] && grep -q '## 9\.' "$out"; then log "SKIP $n already banked"; return 0; fi
  local i=1
  while [ $i -le 4 ]; do
    log "START $n attempt $i"
    bash _pool/vision_gate.sh python3 -u "$SKILL/scripts/analyze_image.py" analysis \
      unique_slides/slide_${n}.jpg \
      --view "Slide $n — forensic slide analysis for a high-fidelity recreation" \
      --capture "960x540 lecture frame (machine learning, NN training and example)" \
      --max-tokens 24000 --timeout 780 --rounds 1 --tries 1 \
      -p "$(cat "$PROMPT")" > "${out}.a${i}" 2>&1
    local rc=$? sz w
    sz=$(wc -c < "${out}.a${i}" 2>/dev/null || echo 0)
    w=$(grep -c '\[winner\]' "${out}.a${i}" 2>/dev/null || echo 0)
    log "END $n attempt $i rc=$rc bytes=$sz winner=$w"
    if grep -q '## 9\.' "${out}.a${i}" 2>/dev/null && [ "$sz" -gt 4000 ]; then
      mv "${out}.a${i}" "$out"; log "BANKED $n"; return 0
    fi
    if grep -q 'FINAL VERDICT' "${out}.a${i}" 2>/dev/null; then
      mv "${out}.a${i}" "$out"; log "BANKED $n (verdict body)"; return 0
    fi
    i=$((i+1))
    if [ $i -le 4 ]; then sleep 90; else mv "${out}.a${i-1}" "${out}.debt" 2>/dev/null; fi
  done
  log "FAIL $n no coherent body after 4 attempts"
  return 0
}
export -f run_one
export NS SKILL OUTDIR PROMPT
log "=== reanalysis driver start (all 34 slides) ==="
for i in $(seq 1 34); do printf "%03d\n" "$i"; done | \
  xargs -P "${VISION_SLOTS:-3}" -I{} bash -c 'run_one "$@"' _ {}
log "=== reanalysis driver end ==="
