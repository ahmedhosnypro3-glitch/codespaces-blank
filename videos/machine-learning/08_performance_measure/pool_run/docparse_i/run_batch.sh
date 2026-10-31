#!/bin/bash
# docparse_i lane runner: slides 011-019, batches of <=4 in flight, one attempt each.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
SK=/home/codespace/.agents/skills/doc-parse/scripts/parse_document.py
OUT=$NS/pool_run/docparse_i

run_one() {
  local n=$1 att=$2
  local img=$NS/unique_slides/slide_${n}.jpg
  local dir=$OUT/slide${n}
  if [ "$att" -gt 1 ]; then dir=$OUT/slide${n}_retry${att}; fi
  local log=$OUT/slide${n}.attempt${att}.log
  echo "start $(date -u +%FT%TZ) slide_${n} attempt${att} -> $dir" > "$log"
  python3 "$SK" "$img" -o "$dir" --timeout 300 >> "$log" 2>&1
  echo "exit=$? end $(date -u +%FT%TZ)" >> "$log"
}

run_one 011 1 & run_one 012 1 & run_one 013 1 & run_one 014 1 & wait
echo "batch1 done $(date -u +%FT%TZ)"
run_one 015 1 & run_one 016 1 & run_one 017 1 & run_one 018 1 & wait
echo "batch2 done $(date -u +%FT%TZ)"
run_one 019 1 & wait
echo "ALL_BATCHES_DONE $(date -u +%FT%TZ)"
