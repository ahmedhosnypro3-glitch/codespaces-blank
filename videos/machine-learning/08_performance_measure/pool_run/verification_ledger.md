# Verification ledger — dual-read certification + re-analysis

| slide | first PASS transcript | corroboration transcript | verify verdict | reanalysis | certified |
|---|---|---|---|---|---|
| 020 | `recreated_pptx/qa/slide020/judge_attempt_13.txt` (render_8.png) | `recreated_pptx/qa/slide020/judge_verify_13.txt` (render_8.png) | PASS / PASS (original-first, drift item "Any value → (0, +1)" present on both Model nodes) | `analysis/reanalysis/slide_020_raw.json` | yes |
| 1 | recreated_pptx/qa/slide001/judge_attempt_5.txt | recreated_pptx/qa/slide001/judge_verify_5.txt | PASS | analysis/reanalysis/slide_001_raw.json (gap fixed: Arabic label جامعة العلوم والتكنولوجيا, rtlMode) | yes |
| 28 | recreated_pptx/qa/slide28/judge_attempt_4.txt | recreated_pptx/qa/slide28/judge_verify_4c.txt | PASS (dual-read, original-first) | analysis/reanalysis/slide_028_raw.json | yes |
| 009 | recreated_pptx/qa/slide009/judge_attempt_1.txt | recreated_pptx/qa/slide009/judge_verify_1.txt | PASS/PASS | reanalysis/slide_009_raw.json | certified=yes |
| 23 | recreated_pptx/qa/slide023/judge_attempt_2.txt | recreated_pptx/qa/slide023//judge_verify_2.txt | FAIL | analysis/reanalysis/slide_023_raw.json | no |
| 27 | recreated_pptx/qa/slide027/judge_attempt_1.txt | recreated_pptx/qa/slide027/judge_verify_1.txt | PASS (dual-read, original-first) | fresh pool_run/image_analysis/slide_027_analysis.txt (no drift vs spec; cursor/letterbox artifacts omitted) | yes |
| 3 | recreated_pptx/qa/slide003/judge_attempt_1.txt (+ judge_attempt_3.txt on render_2) | recreated_pptx/qa/slide003/judge_verify_1c.txt (fresh original-first corroboration vs render_2, FINAL VERDICT: PASS; + judge_verify_3.txt) | PASS (dual-read, original-first, render_2) | analysis/reanalysis/slide_003_raw.json + pool_run/image_analysis/slide_003_analysis.txt (no drift; see qa/slide003/adjudication_verify1.txt for refuted FAIL bodies) | yes |
| 29 | recreated_pptx/qa/slide029/judge_attempt_2.txt (render_2) | recreated_pptx/qa/slide029/judge_verify_4.txt (fresh original-first corroboration vs current render_5/render_5.png, FINAL VERDICT: PASS) | PASS (dual-read, original-first) | analysis/reanalysis/slide_029_raw.json | certified=yes |
| 29 | recreated_pptx/qa/slide029/judge_attempt_4.txt | recreated_pptx/qa/slide029/judge_verify_4.txt | PASS / PASS (original-first dual-read) | analysis/reanalysis/slide_029_raw.json | yes |
