# TRANSPLANT_LOG.md — deck-agnostic QA tool files copied from sibling decks

Date: 2026-10-31. Read-only checker task: no git used; sources read from sibling
namespaces on disk. Rule honored: copied ONLY into new paths (`cp -n`, target dir
did not exist); no existing deck-03 file was overwritten.

Destination root: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/qa_templates/`

CAVEAT: every copied judge template carries the ml-intro house-chrome values
(E8E8E8 / 0.15in red frame / FFF9C4 badge) inside its GROUND RULES. Deck 03's
chrome DIFFERS (white canvas, E9E9E7 panel, three red strokes, FDFD96 badge with
purple ring — see namespace AGENTS.md). These files are reference templates only;
the AUTHORITATIVE frozen judge template for deck 03 is
`shared_patterns/judge_protocol_03.md`. Do not dispatch judges from the copied
files without swapping the chrome clause.

## Copies

| # | Source | Destination |
|---|--------|-------------|
| 1 | videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/qa/judge_template.txt | recreated_pptx/qa/qa_templates/judge_template_deck09.txt |
| 2 | videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/qa/judge_template_011.txt | recreated_pptx/qa/qa_templates/judge_template_011_deck09.txt |
| 3 | videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/qa/judge_template_frozen.txt | recreated_pptx/qa/qa_templates/judge_template_frozen_deck09.txt |
| 4 | videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/judge_template_v2.txt | recreated_pptx/qa/qa_templates/judge_template_v2_deck09.txt |
| 5 | videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/qa/slides_001_011/judge_header_template.txt | recreated_pptx/qa/qa_templates/judge_header_template_deck06.txt |
| 6 | videos/machine-learning/08_performance_measure/pool_run/judge_prompt_template.txt | recreated_pptx/qa/qa_templates/judge_prompt_template_deck08.txt |
| 7 | videos/machine-learning/10_nn_training_and_example/judge_template.txt | recreated_pptx/qa/qa_templates/judge_template_deck10.txt |

## Verified already present in deck 03 (NOT copied)

- `shared_patterns/house_chrome_check.py` (plus house_chrome.js, judge_protocol_03.md)
- `recreated_pptx/build/final_deck/final_deck_tool.py`
- `CLOSEOUT_REPORT.md` skeleton at namespace root (measured live 2026-10-31)
- rejudge payload templates: `qa/rejudge_20261027/payload_A.txt`, `payload_B.tmpl`,
  `payload_B_001..051.txt`, `payload_BL_labels.txt`
- render_eq tooling is shared, not per-deck: `scripts/render_eq.py`,
  `scripts/render_eq_stix.py`, `scripts/render_eq_wide.py` (project root) and
  `~/.agents/skills/slide-recreation/scripts/render_eq*.py`

## Considered but NOT copied (deck-specific, not deck-agnostic)

- `08_performance_measure/recreated_pptx/qa/region_read.sh` — hardcodes the 08 namespace
- `08/pool_run/merge_final_deck.py`, `10/merge_final_deck.py`,
  `09/recreated_pptx/build/init_final_deck.py` — deck-specific final-deck tooling;
  deck 03 already has its own `build/final_deck/final_deck_tool.py`
- `deep-learning/shared_patterns/README.md` + `index.json` — describe the
  deep-learning playlist chrome (founder directive 2026-10-11), not deck-agnostic
- sibling `CLOSEOUT_REPORT.md` files — deck-specific content, not a skeleton
- `01_ml-intro` qa/ tree — removed per founder directive 2026-10-10; nothing on disk
