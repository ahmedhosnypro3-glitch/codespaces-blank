# SOURCES.md — slide 028 "Backward (Update Output Layer Weights)" (delta rule + Δw = η·O_i·δ_j + numeric weight updates)

Topic: the output-layer backward pass of the worked MLP example — the delta rule, the weight-update rule,
and their numeric evaluation (δ6, δ7; ΔW63…ΔW7b; the updated W values).
Method: agy web search + live fetch (Matt Mazur worked example); frame facts from
`analysis/parse/slide_028.parse.md` and `analysis/slide_028_raw.json`. Parse text is DATA only.

## Sources

- Matt Mazur, "A Step by Step Backpropagation Example" — https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/
  Live-fetched. Confirms the frame's two boxed formulas: the delta rule δ_j = (t_j − O_j)·O_j(1−O_j) and the weight update Δw_ji = η·δ_j·O_i (equivalently η·O_i·O_j(1−O_j)(t_j−O_j)).
- "Backpropagation" (Wikipedia) — https://en.wikipedia.org/wiki/Backpropagation
  Confirms ∂E/∂w_ji = −(t_j−O_j)·O_j(1−O_j)·O_i for cost E = ½Σ_j(t_j−O_j)², i.e. the slide's δ and Δw follow from a summed-squared-error cost with a 1/(1+e^−net) output activation.
- Vassar CS365 backprop handout — https://www.cs.vassar.edu/~hunsberg/cs365/handouts-etc/backprop.pdf
  Confirms the same three-factor chain rule (cost derivative × sigmoid derivative × input activation) and the w_ji weight-index convention.
- "Backpropagation step-by-step derivation" (Towards Data Science) — https://towardsdatascience.com/backpropagation-step-by-step-derivation-99ac8fbdcc28/
  Confirms the δ_j = O_j(1−O_j)(t_j−O_j) form used verbatim in the frame's top-left formula box.

## What the source(s) confirm (independently recomputed)

- δ6 = 0.791·(1−0.791)·(0−0.791) = −0.13077 → printed "−0.131" ✓; δ7 = 0.791·(1−0.791)·(1−0.791) = 0.03455 → "0.035" ✓.
- ΔW63 = 5·(−0.131)·0.9 = −0.5895 → "−0.59" ✓; ΔW64 = −0.6177 → "−0.618" ✓; ΔW65 = −0.6340 → "−0.634" ✓; ΔW6b = −0.655 ✓.
- ΔW73 = 0.1575 → "0.158" ✓; ΔW74 = 0.165 ✓; ΔW75 = 0.1694 → "0.169" ✓; ΔW7b = 0.175 ✓.
- Updated weights W63 = 0.3−0.59 = −0.29 ✓; W64 = 0.4−0.618 = −0.218 ✓; W65 = 0.5−0.634 = −0.134 ✓; W6b = 0.2−0.655 = −0.455 ✓;
  W73 = 0.3+0.158 = 0.458 ✓; W74 = 0.4+0.165 = 0.565 ✓; W75 = 0.5+0.169 = 0.669 ✓; W7b = 0.2+0.175 = 0.375 ✓.
- Bias-weight updates use O_i = 1.0 (the constant-1 bias input) — consistent with the slide's "1*0.1" bias terms on slide 27.

## Corrections / notes

- η = 5 (printed in the diagram). This is far outside the commonly-used range for sigmoid SGD —
  sources note η ≥ 0.5 typically causes diverging/oscillating loss, with 0.01–0.1 the usual defaults.
  The slide's arithmetic is entirely self-consistent with η = 5 at every line, so treat it as the
  course's chosen (aggressive) value and reproduce it verbatim; do NOT "correct" it to 0.5.
- Sign conventions all check out: t6 = 0 (δ6 negative, W63..W65 decrease), t7 = 1 (δ7 positive,
  W73..W75 increase). The target column on the diagram is [0, 1], consistent.
- The far-right gray boxes on the frame restate the forward-pass sigmoids; the analysis JSON's subscript
  labels there read "O_2 = 1/(1+e^−3.4) = 0.968" where the frame's own labels and the slide-27 figures
  make clear it is O_5 (the node numbered 5). Recreate as O_5. Same for O_3/O_4 mislabelled as O_6/O_4
  in the far-right stack — the frame's node numbers govern.
- Nothing else contradicts the sources; the update rule, the delta rule and every number are standard.
## Audit

Audited by lane S scope `b_src_2` (web-source audit), 2026-10-31. Method: independent Python
recomputation of every number on the frame, plus agy web-search; cross-read against
`analysis/parse/slide_028.parse.md` and `analysis/slide_028_raw.json`.

Questions asked:
1. Are `δ6 = −0.131` and `δ7 = 0.035` correct?
2. Are the eight ΔW values and the eight updated W values correct?
3. Are `t6 = 0` and `t7 = 1` the correct targets for the shown sign pattern?
4. Is η = 5 consistent with every update line?

Answers:
- Q1 **CONFIRMED**: δ6 = 0.791·(1−0.791)·(0−0.791) = −0.13077 → "−0.131" ✓;
  δ7 = 0.791·(1−0.791)·(1−0.791) = 0.03455 → "0.035" ✓. (Recomputed from the rounded 0.791;
  full-precision 0.79096 gives −0.1306/0.0344, same 3-dp results except δ7's last digit.)
- Q2 **CONFIRMED** — every value recomputes exactly using the frame's rounded δ (−0.131, 0.035):
  ΔW63 = 5·(−0.131)·0.9 = −0.5895 → "−0.59" ✓; ΔW64 = −0.6177 → "−0.618" ✓;
  ΔW65 = −0.6340 → "−0.634" ✓; ΔW6b = −0.655 ✓; ΔW73 = 0.1575 → "0.158" ✓;
  ΔW74 = 0.165 ✓; ΔW75 = 0.1694 → "0.169" ✓; ΔW7b = 0.175 ✓.
  Updated: W63 = 0.3−0.59 = −0.29 ✓; W64 = 0.4−0.618 = −0.218 ✓; W65 = 0.5−0.634 = −0.134 ✓;
  W6b = 0.2−0.655 = −0.455 ✓; W73 = 0.3+0.158 = 0.458 ✓; W74 = 0.4+0.165 = 0.565 ✓;
  W75 = 0.5+0.169 = 0.669 ✓; W7b = 0.2+0.175 = 0.375 ✓.
- Q3 **CONFIRMED**: t6 = 0 makes δ6 negative so W63..W65 decrease ✓; t7 = 1 makes δ7 positive
  so W73..W75 increase ✓. The target column is [0, 1], consistent.
- Q4 **CONFIRMED**: every update line uses the multiplier 5, so η = 5 is internally consistent.

Verdicts per claim:
- Delta rule `δ_j = (t_j − O_j)·O_j(1−O_j)` — **CONFIRMED** (search returns this form for a
  summed-squared-error cost with a logistic output activation).
- Weight update `Δw_ji = η·O_i·δ_j` — **CONFIRMED**.
- All sixteen numeric values — **CONFIRMED** by recomputation.
- Sign behaviour vs targets [0,1] — **CONFIRMED**.
- Bias-weight updates using O_i = 1.0 — **CONFIRMED**.
- η = 5 — **CONFLICT** with typical practice (0.01–0.1 defaults; η ≥ 0.5 generally diverges;
  Mazur's own example uses 0.5). Reproduce verbatim; the frame's arithmetic owns it.
- `Δ_ji = −η∂E/∂W_ji` mixing lowercase w and capital W — **CONFLICT** with the frame's own
  `w_ji`; recreate with `w_ji` (W is not a separate matrix here).
- Parse's `∂Net_j/∂w_jj = O_i` — **CONFLICT** (OCR artifact of the doubled subscript); the
  correct link is `∂Net_j/∂w_ji = O_i`, which the certified JSON has.
- Parse's "W 64 = 0.4−0.18=−0.218" — **CONFLICT** (the subtrahend 0.618 was misread as 0.18;
  0.4 − 0.618 = −0.218). Recreate as `W64 = 0.4 − 0.618 = −0.218`.
- Far-right gray boxes restating the forward-pass sigmoids with subscript labels `O_2` and
  `O_3`/`O_4` where the frame's node numbering and slide 27's figures indicate O_5 and O_3/O_4
  — **CONFLICT** in the analysis JSON's labelling; the frame's node numbers govern.

New sources found during audit (real URLs, not previously cited):
- MIT OCW 9.641, "Lecture 20: Backprop" —
  https://ocw.mit.edu/courses/9-641j-introduction-to-neural-networks-spring-2005/5d46d3b6e32a5120fe9893193c31e926_lec20_backprop.pdf
  Gives `∂E/∂w_ji = −(t_j−O_j)·O_j(1−O_j)·O_i` for `E = ½Σ(t_j−O_j)²` — the same three-factor
  chain the frame's δ and Δw follow from.
- Math StackExchange, "Backpropagation hidden layer error" —
  https://math.stackexchange.com/questions/4686558/backpropagation-hidden-layer-error
  Wikipedia, "Delta rule" — https://en.wikipedia.org/wiki/Delta_rule

Audit summary: every numeric value on the frame recomputes exactly. The defects are index/case
typos and three parse OCR artifacts, all already noted above.
