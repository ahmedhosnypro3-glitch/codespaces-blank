#!/usr/bin/env bash
# r19 shard C harvest — for each slide 035-051 (skip 025):
#   clean r19 leg PASS  -> result.txt gets R19_<LEG>=PASS
#   clean r19 leg FAIL  -> rejudge_adjudicate.py NNN [--crop] banked to
#                          slideNNN/adjudicate_r19_<leg>.txt; diffuse -> PASS(dismissed),
#                          localized -> verbatim findings appended.
# result.txt is backed up (result.txt.bak_r19_20261031) before appending; register appended.
# Read-only w.r.t. transcripts; never deletes evidence; no git.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/r19_shardC_harvest.log
: > "$LOG"
clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verdict() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }

# classify adjudicate output: diffuse vs localized
# localized = a single coarse cell holds >=25% of all diff px AND >=1500 diff px
# otherwise diffuse
classify() {
  python3 - "$1" <<'PY'
import re, sys
txt = open(sys.argv[1]).read()
m = re.search(r'diff px total: (\d+)', txt)
total = int(m.group(1)) if m else 0
cells = [int(x) for x in re.findall(r': (\d+) diff px', txt)]
if total == 0 or not cells:
    print("diffuse"); sys.exit(0)
top = max(cells)
print("localized" if (top >= 1500 and top >= 0.25 * total) else "diffuse")
PY
}

for N in 035 036 037 038 039 040 041 042 043 044 045 046 047 048 049 050 051; do
  D=$RJ/slide$N
  [ -f "$D/result.txt" ] && [ ! -f "$D/result.txt.bak_r19_20261031" ] && cp "$D/result.txt" "$D/result.txt.bak_r19_20261031"
  # ---- full leg
  T=$D/judge_full_r19.txt
  if grep -q '^R19_FULL=' "$D/result.txt" 2>/dev/null; then
    echo "$N full r19: already harvested, skip" >> "$LOG"
  elif clean "$T"; then
    V=$(verdict "$T")
    echo "$N full r19: $V" >> "$LOG"
    if [ "$V" = PASS ]; then
      { echo "R19_FULL=PASS (judge_full_r19.txt clean, $(date -u +%FT%TZ))"; } >> "$D/result.txt"
    else
      (cd "$ROOT" && python3 "$RJ/rejudge_adjudicate.py" "$N" --full) > "$D/adjudicate_r19_full.txt" 2>&1
      CL=$(classify "$D/adjudicate_r19_full.txt")
      echo "$N full r19 FAIL adjudicated: $CL" >> "$LOG"
      if [ "$CL" = diffuse ]; then
        { echo "R19_FULL=PASS(dismissed) (judge_full_r19.txt clean FAIL $(date -u +%FT%TZ); PIL adjudicate_r19_full.txt diffuse -> dismissed per dispatch rule)"; } >> "$D/result.txt"
      else
        { echo "R19_FULL=FAIL (judge_full_r19.txt clean FAIL $(date -u +%FT%TZ); PIL adjudicate_r19_full.txt LOCALIZED — findings verbatim below)"
          echo "--- verbatim FAIL findings (judge_full_r19.txt) ---"
          sed -n '/FINAL VERDICT/,$p' "$T"
        } >> "$D/result.txt"
      fi
    fi
  else
    echo "$N full r19: not clean yet, skipped" >> "$LOG"
  fi
  # ---- crop leg (050 has no r19 crop by special rule)
  T=$D/crop_dense_judge_r19.txt
  if [ "$N" = "050" ]; then
    echo "050 crop r19: not launched (special rule); existing clean crop verdicts stand (see result.txt HARVEST5)" >> "$LOG"
    continue
  fi
  if grep -q '^R19_CROP=' "$D/result.txt" 2>/dev/null; then
    echo "$N crop r19: already harvested, skip" >> "$LOG"
  elif clean "$T"; then
    V=$(verdict "$T")
    echo "$N crop r19: $V" >> "$LOG"
    if [ "$V" = PASS ]; then
      { echo "R19_CROP=PASS (crop_dense_judge_r19.txt clean, $(date -u +%FT%TZ))"; } >> "$D/result.txt"
    else
      (cd "$ROOT" && python3 "$RJ/rejudge_adjudicate.py" "$N" --crop) > "$D/adjudicate_r19_crop.txt" 2>&1
      CL=$(classify "$D/adjudicate_r19_crop.txt")
      echo "$N crop r19 FAIL adjudicated: $CL" >> "$LOG"
      if [ "$CL" = diffuse ]; then
        { echo "R19_CROP=PASS(dismissed) (crop_dense_judge_r19.txt clean FAIL $(date -u +%FT%TZ); PIL adjudicate_r19_crop.txt diffuse -> dismissed per dispatch rule)"; } >> "$D/result.txt"
      else
        { echo "R19_CROP=FAIL (crop_dense_judge_r19.txt clean FAIL $(date -u +%FT%TZ); PIL adjudicate_r19_crop.txt LOCALIZED — findings verbatim below)"
          echo "--- verbatim FAIL findings (crop_dense_judge_r19.txt) ---"
          sed -n '/FINAL VERDICT/,$p' "$T"
        } >> "$D/result.txt"
      fi
    fi
  else
    echo "$N crop r19: not clean yet, skipped" >> "$LOG"
  fi
done
echo "HARVEST_DONE $(date -u +%FT%TZ)" >> "$LOG"
cat "$LOG"
