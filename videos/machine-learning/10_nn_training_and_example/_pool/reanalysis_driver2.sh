#!/usr/bin/env bash
# Parallel fresh RE-ANALYSIS of all 34 unique frames (background task, not a subagent).
# Per-slide flock: two drivers can never process the same frame twice.
# Skips slides already banked with a coherent body; never overwrites banked evidence.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
OUTDIR=analysis/reanalysis_skill
PROMPT=$NS/_pool/audit_prompt.txt
LOG=$NS/_pool/reanalysis2.log
LOCKDIR=$OUTDIR/.locks
mkdir -p "$LOCKDIR" "$OUTDIR"
log(){ echo "$(date +%F\ %T) $*" >> "$LOG"; }
export -f log
export NS SKILL OUTDIR PROMPT LOG LOCKDIR

banked(){ [ -s "$OUTDIR/slide_${1}.analysis.txt" ] && grep -q '## 9\.' "$OUTDIR/slide_${1}.analysis.txt" 2>/dev/null; }

run_one(){
  n="$1"
  if banked "$n"; then log "SKIP $n already banked"; return 0; fi
  exec 8>>"$LOCKDIR/slide_${n}.lock"
  flock -n 8 || { log "SKIP-LOCK $n another driver holds it"; return 0; }
  if banked "$n"; then log "SKIP $n banked while locking"; return 0; fi
  i=1
  while [ "$i" -le 4 ]; do
    VISION_SLOTS="${RA_SLOTS:-2}" bash _pool/vision_gate.sh python3 -u "$SKILL/scripts/analyze_image.py" analysis \
      "unique_slides/slide_${n}.jpg" \
      --view "Slide $n — forensic slide analysis for a high-fidelity recreation" \
      --capture "960x540 lecture frame (machine learning, NN training and example)" \
      --max-tokens 24000 --timeout 780 --rounds 1 --tries 1 \
      -p "$(cat "$PROMPT")" > "$OUTDIR/slide_${n}.analysis.txt.b${i}" 2>&1
    rc=$?; sz=$(wc -c < "$OUTDIR/slide_${n}.analysis.txt.b${i}" 2>/dev/null || echo 0)
    w=$(grep -c '\[winner\]' "$OUTDIR/slide_${n}.analysis.txt.b${i}" 2>/dev/null || echo 0)
    log "END $n attempt $i rc=$rc bytes=$sz winner=$w"
    if grep -q '## 9\.' "$OUTDIR/slide_${n}.analysis.txt.b${i}" 2>/dev/null && [ "$sz" -gt 4000 ]; then
      mv -n "$OUTDIR/slide_${n}.analysis.txt.b${i}" "$OUTDIR/slide_${n}.analysis.txt"; log "BANKED $n"; return 0
    fi
    if grep -q 'FINAL VERDICT' "$OUTDIR/slide_${n}.analysis.txt.b${i}" 2>/dev/null && [ "$sz" -gt 4000 ]; then
      mv -n "$OUTDIR/slide_${n}.analysis.txt.b${i}" "$OUTDIR/slide_${n}.analysis.txt"; log "BANKED $n verdict body"; return 0
    fi
    rm -f "$OUTDIR/slide_${n}.analysis.txt.b${i}"
    i=$((i+1)); [ "$i" -le 4 ] && sleep 90
  done
  log "FAIL $n no coherent body after 4 attempts"
  return 0
}
export -f log banked run_one
log "=== reanalysis2 driver start (34 slides, parallel) ==="
for i in $(seq 1 34); do printf "%03d\n" "$i"; done | xargs -P "${RA_PAR:-3}" -I{} bash -c 'run_one "$@"' _ {}
log "=== reanalysis2 driver end ==="
