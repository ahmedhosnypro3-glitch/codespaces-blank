#!/usr/bin/env bash
# b06 finish for slide 011: run only after a banked FINAL VERDICT: PASS.
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
TRANS="qa/slide011/rejudge/judge_attempt_11.txt"

if ! grep -q 'FINAL VERDICT: PASS' "$TRANS"; then
  echo "ABORT: no banked PASS verdict in $TRANS" >&2
  exit 1
fi

# 1. single-version deliverable (byte copy of the certified build)
cp -p recreated_pptx/build/slide_011_recreated_attempt2.pptx recreated_pptx/slide_011_recreated.pptx
md5sum recreated_pptx/slide_011_recreated.pptx

# 2. park the naming stray (move, never delete)
mkdir -p qa/slide011/rejudge/_attempt2
mv recreated_pptx/build/slide_011_recreated_attempt2.pptx \
   qa/slide011/rejudge/_attempt2/slide_011_recreated_attempt2.pptx

# 3. merge page 11 into the final deck (fleet-locked inside the tool)
python3 merge_final_deck.py update 11 \
  "$NS/recreated_pptx/slide_011_recreated.pptx" \
  "$NS/10_nn_training_and_example_final.pptx"

# 4. verify the ledger page
python3 - <<'PY'
import json
d = json.load(open('final_deck_ledger.json'))
p = [x for x in d['pages'] if x['slide_num'] == 11][0]
print('ledger page 11:', p)
assert p['status'] == 'certified', 'page 11 not certified'
PY

# 5. progress DB row
sqlite3 slides_progress.db "update slides set gen_status='certified',
  pptx_path='recreated_pptx/slide_011_recreated.pptx',
  build_script='recreated_pptx/build/slide_011_attempt2.js',
  visual_check='PASS', visual_attempts=8,
  visual_transcript='qa/slide011/rejudge/judge_attempt_11.txt',
  updated_at=datetime('now') where slide_id=11;"
sqlite3 -header slides_progress.db \
  "select slide_id,gen_status,pptx_path,visual_check from slides where slide_id=11;"
echo "=== b06 slide_011 certify complete $(date +%T)"
