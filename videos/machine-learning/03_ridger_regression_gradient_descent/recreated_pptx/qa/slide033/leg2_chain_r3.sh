#!/bin/bash
# Remaining Leg-2 crop legs for slide 033, fired sequentially behind the
# in-flight plot call. Same mandated wall as dispatch_crop_k9.sh
# (analyzer --timeout 1200 inside `timeout 1700`, --rounds 1 --tries 1,
# --thinking high --max-tokens 65536) and the same byte-verified payload.
# Stops early on a transcript landing; a landed transcript is the only success.
set -u
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033

s033_clients() {
  ps -eo args= | grep '[a]nalyze_image\.py comparison videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033/' | wc -l
}

for r in table center title; do
  # wait until no slide-033 analyzer client is in flight
  while [ "$(s033_clients)" -gt 0 ]; do sleep 30; done
  echo "[$(date '+%T')] firing crop region: $r"
  bash "$Q/dispatch_crop_k9.sh" "$r" >> "$Q/leg2_chain_r3.log" 2>&1
  echo "[$(date '+%T')] region $r done (transcript bytes: $(wc -c < "$Q/crop_9_${r}_judge.txt" 2>/dev/null || echo 0))"
  sleep 30
done
echo "[$(date '+%T')] chain done"
