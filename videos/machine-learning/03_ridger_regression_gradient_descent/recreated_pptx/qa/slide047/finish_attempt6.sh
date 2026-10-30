#!/usr/bin/env bash
# Finisher for slide 047 attempt 6: waits for the topband crop (still pacing in the
# dispatcher), then re-dispatches leg A (full-slide) ONCE into a quiet gateway window
# (garbage re-invoke #2 per protocol accounting), then certifies iff all 6 transcripts PASS.
set -u
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$DECK/recreated_pptx/qa/slide047
export TMPDIR="/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp"

hb() { VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 47 w047-root-20261024 >/dev/null 2>&1; }

echo "$(date -u +%FT%TZ) finisher start" >> "$Q/finisher_log.txt"

# 1) wait for the topband crop transcript (dispatcher subshell paces it)
for i in $(seq 1 240); do
  if [ -f "$Q/crop_6_topband_judge.txt" ]; then break; fi
  hb; sleep 30
done
if [ -f "$Q/crop_6_topband_judge.txt" ]; then
  echo "$(date -u +%FT%TZ) topband landed: $(grep -h 'FINAL VERDICT' "$Q/crop_6_topband_judge.txt" | head -1)" >> "$Q/finisher_log.txt"
else
  echo "$(date -u +%FT%TZ) topband still missing after 2h" >> "$Q/finisher_log.txt"
fi

# 2) re-dispatch leg A once, into a standard gate-law window (load < 8), else after 12 probes give up
if [ ! -s "$Q/judge_attempt_6.txt" ]; then
  for probe in 1 2 3 4 5 6 7 8 9 10 11 12; do
    n=$(pgrep -c -f analyze_image.py || true)
    if [ "${n:-9}" -lt 8 ]; then
      hb
      scripts/16_vision_gate.sh timeout 1700 python3 \
        .agents/skills/image-analysis/scripts/analyze_image.py comparison \
        "$Q/render_10.png" "$DECK/unique_slides/slide_047.jpg" \
        --view "Slide 047 recreation — fidelity check vs original lecture frame (attempt 6, leaf retry, wall 1200)" \
        --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
        --thinking high --max-tokens 65536 \
        --timeout 1200 --rounds 1 --tries 1 \
        --transcript "$Q/judge_attempt_6.txt" \
        -p "$(cat $Q/judge_prompt_attempt_6.txt)" > "$Q/judge_attempt_6_leaf_dispatch.log" 2>&1
      rc=$?
      echo "$(date -u +%FT%TZ) leg A leaf dispatch exit=$rc size=$(wc -c < "$Q/judge_attempt_6.txt" 2>/dev/null || echo 0)" >> "$Q/finisher_log.txt"
      break
    fi
    echo "$(date -u +%FT%TZ) leg A probe $probe: load=$n (need <8)" >> "$Q/finisher_log.txt"
    hb; sleep 240
  done
fi

# 3) certificate decision
ok=1
grep -q "FINAL VERDICT: PASS" "$Q/judge_attempt_6.txt" 2>/dev/null || ok=0
for n in topband augmatrix calceq calcright button; do
  grep -q "FINAL VERDICT: PASS" "$Q/crop_6_${n}_judge.txt" 2>/dev/null || ok=0
done
if [ "$ok" = "1" ]; then
  bash "$Q/certify_attempt6.sh" > "$Q/certify_attempt6.log" 2>&1
  echo "$(date -u +%FT%TZ) CERTIFIED (all 6 legs PASS)" >> "$Q/finisher_log.txt"
else
  {
    echo "$(date -u +%FT%TZ) NOT certified — missing/failed:"
    [ -s "$Q/judge_attempt_6.txt" ] || echo "  judge_attempt_6.txt: none"
    for n in topband augmatrix calceq calcright button; do
      [ -s "$Q/crop_6_${n}_judge.txt" ] || echo "  crop_6_${n}_judge.txt: none"
    done
    grep -h "FINAL VERDICT" "$Q/judge_attempt_6.txt" "$Q"/crop_6_*_judge.txt 2>/dev/null | sed 's/^/  /'
  } > "$Q/autocertify_note.txt"
  echo "$(date -u +%FT%TZ) not certified; state banked" >> "$Q/finisher_log.txt"
fi
echo "FINISHER DONE $(date -u +%FT%TZ)" >> "$Q/finisher_log.txt"
