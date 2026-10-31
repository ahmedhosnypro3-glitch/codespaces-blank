# SOURCES_MAP.md — machine-learning/08_performance_measure

Fleet map for web-source verification per `~/.agents/skills/slide-recreation/references/source-research.md`.
Scope this lane: slides 001-019 (reinforcement lane A, 2026-10-31). Per-slide provenance records live at `sources/slide_NNN/SOURCES.md`; earlier flat notes from a prior lane live at `sources/slide_NNN_research.md` (cross-referenced, not re-spent).

Method: `mcp__agy-cli-mcp__agy_web_search` (agy CLI, OAuth token from keyring), grounding URLs resolved live to source pages in the same session. Query budget this lane: 16 queries total across slides 01-19 (5 + 5 + 5 + 1), each listed per slide in its SOURCES.md. No 429s encountered; no retries needed.

Confidence legend: CONFIRMED = source resolved live this session and the claim verified against it / re-computed locally. origin-level = provenance from a banked prior-lane record. [?] = unresolved.

## Slide-range -> source table (slides 001-019)

| Slide | Topic | Primary sources (all CONFIRMED) | Record |
|---|---|---|---|
| 001 | Title / course identity / metrics overview | scikit-learn model_evaluation guide; zewailcity.edu.eg program/40 + member/53; Han & Kamber ch.6 (prior lane) | sources/slide_001/SOURCES.md |
| 002 | Labels [0,1], sigmoid (0,+1), threshold 0.5 | sklearn classification_threshold; FixedThresholdClassifier docs; logistic-curve reference | sources/slide_002/SOURCES.md |
| 003 | Labels [-1,+1], bipolar step, threshold zero | Analytics Vidhya activation functions; Semantic Scholar perceptron PDF; sklearn classification_threshold | sources/slide_003/SOURCES.md |
| 004 | Radar example, confusion matrix 30/70, TP18/FN12/FP10/TN60 | Wikipedia Confusion matrix; Paperspace wiki; Ultralytics glossary; sklearn confusion_matrix | sources/slide_004/SOURCES.md |
| 005 | Totals TP+FN / FP+TN; FN/FP definitions | Wikipedia Confusion matrix; sklearn confusion_matrix marginals | sources/slide_005/SOURCES.md |
| 006 | Accuracy = (TP+TN)/all = 78/100; "not sufficient" | sklearn accuracy_score; Wikipedia Confusion matrix; sklearn model_evaluation imbalance caveat | sources/slide_006/SOURCES.md |
| 007 | Precision = TP/(TP+FP), trust meaning | sklearn precision_score (verbatim quote); Wikipedia Precision and recall (FDR) | sources/slide_007/SOURCES.md |
| 008 | High precision != retrieved more positives | Wikipedia Precision and recall (independent denominators); APXML tradeoff | sources/slide_008/SOURCES.md |
| 009 | Precision 5/(5+0)=100% example | sklearn precision_score; Wikipedia Precision and recall | sources/slide_009/SOURCES.md |
| 010 | Recall = TP/(TP+FN), "does it miss positives" | sklearn recall_score (verbatim quote); Wikipedia Sensitivity and specificity; Google ML Crash Course | sources/slide_010/SOURCES.md |
| 011 | Recall 28/(28+2)=93.3%; recall-vs-precision trust | sklearn recall_score; Wikipedia P&R / Sensitivity | sources/slide_011/SOURCES.md |
| 012 | All-positive model: recall 100% is not a model | sklearn recall/precision docs; APXML degenerate-classifier analysis | sources/slide_012/SOURCES.md |
| 013 | Good model P=64.5% R=66.6%, arithmetic avg 65.55% | sklearn precision/recall/f1 docs; APXML F1 metric | sources/slide_013/SOURCES.md |
| 014 | "Not a Model" all-positive; average not good | APXML degenerate 30/70 example (F1 46%); sklearn model_evaluation caveat; Wikipedia F-score | sources/slide_014/SOURCES.md |
| 015 | Penalize small values via 1/x; 1/F1 reciprocal form; normalize 0.5 | Wikipedia F-score + Harmonic mean; APXML F1 metric | sources/slide_015/SOURCES.md |
| 016 | F1 = 2PR/(P+R) confirmed (65.55% vs 46% panels) | Wikipedia F-score; APXML F1 + degenerate example | sources/slide_016/SOURCES.md |
| 017 | F1-vs-recall curve family for precision 0.1..1.0 | sklearn f1_score + fbeta_score; MachineLearningMastery F-beta; Wikipedia F-score | sources/slide_017/SOURCES.md |
| 018 | Multiclass Dog/Cat/Fish per-class P/R (column/row sums) | sklearn precision_recall_fscore_support + recall_score; Accelerated DS Multiclass guide | sources/slide_018/SOURCES.md |
| 019 | Bipolar step (-1,+1), threshold zero, train/eval path | Analytics Vidhya activation functions; sklearn classification_threshold; Wikipedia Perceptron | sources/slide_019/SOURCES.md |

ROC/AUC note: no slide in 01-19 shows a ROC curve; ROC/AUC sources (sklearn roc_curve / roc_auc_score) were verified this session anyway for deck-level readiness if later slides need them.

## Failed findings / do-not-reuse
- None this lane. No hallucinated or dead URLs recorded.

## Append-only note
Later decks/lane runs APPEND rows below this line; never edit or delete earlier rows. A [?] is removed only by the owning slide's worker after confirmation recorded in that slide's SOURCES.md.

---

## Lane C append — second-opinion pass, slides 020-037 (2026-10-31)

Scope: second-opinion verification of the lane B records `sources/slide_020_research.md` … `sources/slide_037_research.md` (sigmoid threshold, threshold effects, ROC sweep 27-36, AUC 37). Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries = 20 queries, 75-110s sleeps between batches. No 429s, no retries needed.

Result: every lane B CONFIRMED claim re-confirmed against sklearn (roc_curve / auc / classification_threshold / recall_score docs), Wikipedia ROC, Google ML Crash Course (roc-and-auc, accuracy-precision-recall), Evidently AI, MathWorks, UVA Library, TrainInData. The one CORRECTED claim (threshold=0.6 panel TPR=3/(3+1) is 0.75, not 0.6; course-authored slip, frame wins for recreation) independently re-confirmed via OmniCalculator/StatisticsFundamentals — recorded on slide 033 and cross-referenced by 034-036.

`## Second-opinion` sections appended ONLY where new confirming sources were added or a correction was re-verified: `sources/slide_020_research.md` (Ultralytics + MachineLearningMastery sigmoid range, sklearn FixedThresholdClassifier/TunedThresholdClassifierCV), `sources/slide_028_research.md` (roc_curve thresholds[0]=inf detail, MathWorks FPR=1-specificity), `sources/slide_033_research.md` (0.75 correction confirmation), `sources/slide_036_research.md` ((0,0) endpoint via inf first threshold, UVA Library locus source), `sources/slide_037_research.md` (sklearn metrics.auc trapezoidal rule — NEW; Wikipedia AUC probabilistic/Mann-Whitney meaning). Slides 021-027, 029-032, 034-035: no new sources beyond the banked records, no corrections — no sections appended, per the append-only-if-new rule. analysis/, recreated_pptx/, mission.db and other namespaces untouched.

## Lane D append — second-opinion pass, slides 001-019 (2026-10-31)

Scope: second-opinion verification of `sources/slide_001_research.md` … `sources/slide_019_research.md`. Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries = 20 queries, 85-100s sleeps between batches, all grounding URLs resolved live this session; every worked example additionally re-computed locally in Python. No 429s, no retries needed.

Result: 15 slides CONFIRMED (001, 004, 006-013, 016-019); 4 slides CORRECTED, each re-confirmed this lane — 002 (sigmoid model cannot emit (-1,+1); range is the open interval (0,1) — Google MLCC / MachineLearningMastery / APXML), 003 (spelling: "bipolar step" — GeeksforGeeks / Cornell CS4780 / Wikipedia Perceptron), 005 (spelling: "misclassified" — Ultralytics), 014 (spec operand misread "68.7%/60%"; frame's 64.5%+66.6%→65.55% arithmetically confirmed; not-a-model panel mean ~65% vs harmonic F1 0.46), and 015 (spec bullet "F1 range 0..0.5" upgraded UNVERIFIED→CORRECTED: F1 ∈ [0,1], 0.5 only when P=R=0.5 — sklearn f1_score / Wikipedia F-score / DataCamp / Datature). Slide 016's printed 46% re-confirmed as the harmonic mean (2·0.303·1/1.303 = 0.465) vs arithmetic 0.651. Slide 018's per-class values (Dog 5/16 & 5/8, Cat 6/8 & 6/11, Fish 0/2 & 0/7) match a live Stats.SE 3x3 worked example and local re-computation. One search snippet mislabeled sklearn's precision docstring sentence as "specificity" — recorded here as a do-not-reuse interpretation; the docstring line is sklearn's own precision wording.

`## Second-opinion` sections appended to all 19 research files (each had new confirming sources resolved live this session). analysis/, recreated_pptx/, mission.db and other namespaces untouched.
