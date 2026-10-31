#!/bin/bash
# Doc-parse full-frame lane: slides 020-028 -> pool_run/docparse_j/slideNNN
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
OUT=$NS/pool_run/docparse_j
SCRIPT=/home/codespace/.agents/skills/doc-parse/scripts/parse_document.py
mkdir -p "$OUT"
: > "$OUT/parse_attempts.log"

parse_one() {
  local num=$1 img=$2
  local dir=$OUT/slide$num
  mkdir -p "$dir"
  local attempt ok rc
  for attempt in 1 2 3 4 5; do
    rm -f "$dir"/*.parse.json "$dir"/*.parse.md
    python3 "$SCRIPT" "$img" -o "$dir" --timeout 300 > "$dir/run_attempt${attempt}.log" 2>&1
    rc=$?
    ok=$(python3 - "$dir" <<'EOF'
import json, sys, glob
fs = glob.glob(sys.argv[1] + '/*.parse.json')
if not fs:
    print('nojson')
else:
    d = json.load(open(fs[0]))
    c = d.get('content') or ''
    fr = d.get('finish_reason')
    print('ok' if fr == 'stop' and len(c.strip()) > 0 else 'bad finish=%s len=%d' % (fr, len(c)))
EOF
)
    echo "slide$num attempt=$attempt rc=$rc check=$ok" >> "$OUT/parse_attempts.log"
    if [ "$ok" = "ok" ]; then
      echo "slide$num OK attempt=$attempt"
      return 0
    fi
    if [ "$attempt" -lt 5 ]; then sleep 60; fi
  done
  echo "slide$num FAILED after 5 attempts"
  return 1
}

run_pair() {
  parse_one "$1" "$NS/unique_slides/slide_$1.jpg" &
  parse_one "$2" "$NS/unique_slides/slide_$2.jpg" &
  parse_one "$3" "$NS/unique_slides/slide_$3.jpg" &
  parse_one "$4" "$NS/unique_slides/slide_$4.jpg" &
  wait
}

# slide 028 file is slide_028-.jpg; cap 4 parse calls in flight
parse_one 028 "$NS/unique_slides/slide_028-.jpg" &
run_pair 021 022 023 024
wait
run_pair 025 026 027 020
wait
echo "ALL_FULLFRAME_DONE" >> "$OUT/parse_attempts.log"
