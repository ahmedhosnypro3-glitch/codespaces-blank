#!/usr/bin/env bash
# scope_r4 rejudge step-1 runner: fresh vision analysis + fresh text validation
# for slides 11, 12, 13 into analysis/reanalysis/ (certified analysis untouched).
#
# STORM-RESILIENCE CLAUSE: on any provider/upstream error sleep 120s and retry
# up to 3x per step. Never abort the run. Every step is banked atomically
# (script 12/13 write their own output files) and logged to _pool/storm_log.

set -u
VID="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
PROJ="/home/codespace/ai_llm_slides"
OUT="$VID/analysis/reanalysis"
LOG="$VID/_pool/r4_analysis.log"
STORM="$VID/_pool/storm_log/storm_r4.log"
TMPDIR="$VID/_pool"

export TMPDIR
mkdir -p "$OUT" "$VID/_pool/storm_log"

say() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
storm() {
  echo "[$(date '+%F %T')] STORM-RESILIENCE: $1 | step=$2 | retry=$3/3 | action=sleep 120 then retry" | tee -a "$STORM" >> "$LOG"
  sleep 120
}

say "=== scope_r4 fresh analysis start (slides 11,12,13) ==="

for N in 011 012 013; do
  # ---------- Step 1a: vision analysis (script 12) ----------
  done=0
  for TOKENS in 16000 16000 32000; do
    for try in 1 2 3; do
      RAW="$OUT/slide_${N}_raw.json"
      if [[ -s "$RAW" ]]; then
        say "slide_$N: raw analysis already banked ($RAW) -> skip"
        done=1; break
      fi
      say "slide_$N: script12 analysis attempt try=$try max_tokens=$TOKENS"
      python3 "$PROJ/scripts/12_analyze_slides.py" \
        "$VID/unique_slides" "$OUT" --from "$((10#$N))" --to "$((10#$N))" \
        --slides 10 --max-tokens "$TOKENS" >> "$LOG" 2>&1
      rc=$?
      if [[ $rc -eq 0 && -s "$RAW" ]]; then
        say "slide_$N: analysis OK (raw banked)"
        done=1; break
      fi
      storm "script12 exit=$rc (provider/upstream error or stall)" "12-analyze slide_$N" "$try"
    done
    [[ $done -eq 1 ]] && break
  done
  if [[ $done -eq 0 ]]; then
    storm "script12 exhausted 3 retries for slide_$N" "12-analyze slide_$N" 3
    say "slide_$N: analysis NOT produced after retries (recorded for report; continue)"
    continue
  fi

  # ---------- Step 1b: text validation (script 13) ----------
  vdone=0
  for try in 1 2 3; do
    FIN="$OUT/slide_${N}_final.json"
    if [[ -s "$FIN" ]]; then
      say "slide_$N: final validation already banked -> skip"
      vdone=1; break
    fi
    say "slide_$N: script13 validation attempt try=$try"
    python3 "$PROJ/scripts/13_validate_slides.py" \
      "$OUT" --from "$((10#$N))" --to "$((10#$N))" --slides 10 >> "$LOG" 2>&1
    rc=$?
    if [[ $rc -eq 0 && -s "$FIN" ]]; then
      say "slide_$N: validation OK (final banked)"
      vdone=1; break
    fi
    storm "script13 exit=$rc (validation endpoint error / empty content)" "13-validate slide_$N" "$try"
  done
  if [[ $vdone -eq 0 ]]; then
    storm "script13 exhausted 3 retries for slide_$N" "13-validate slide_$N" 3
    say "slide_$N: validation NOT produced after retries (recorded for report; continue)"
  fi
done

say "=== scope_r4 fresh analysis complete ==="
for N in 011 012 013; do
  [[ -s "$OUT/slide_${N}_raw.json" ]] && say "  slide_$N raw: present" || say "  slide_$N raw: MISSING"
  [[ -s "$OUT/slide_${N}_final.json" ]] && say "  slide_$N final: present" || say "  slide_$N final: MISSING"
done
