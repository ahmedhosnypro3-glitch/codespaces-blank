# Sources — Slide 3 — Training Samples with Labels [-1,+1] (Two Classes)

Spec: analysis/slide_003_final.json.

- Bipolar step activation outputs the range (-1, +1): CONFIRMED — "Perceptrons: The First Neural Network Model", https://towardsdatascience.com/perceptrons-the-first-neural-network-model-8b3ee4513757/ — the bipolar step (sign) function outputs {-1, +1} versus the Heaviside step's {0, 1}; matches the Activation Function box's "Bi-polor step (-1, +1)".
- Threshold at "zero" for the bipolar step: CONFIRMED — Raschka STAT 453 lecture notes, https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L03_perceptron_slides.pdf — f(z) = +1 if z ≥ 0, -1 if z < 0, i.e. the decision cutoff sits at zero, exactly the step plot drawn on the slide.
- Positive-class labels [+1], negative-class labels [-1]: CONFIRMED — "Perceptrons: The First Neural Network Model", https://towardsdatascience.com/perceptrons-the-first-neural-network-model-8b3ee4513757/ — with bipolar outputs the target labels must be mapped to the same {-1, +1} format, so Class 1 = +1 and Class 2 = -1 as the two label columns show.
- {-1,+1} vs {0,1} label coding is estimator-dependent: CONFIRMED — sklearn accuracy_score docs, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html — e.g. SVC is trained on and predicts {-1, +1} labels while LogisticRegression uses {0, 1}; both codings coexist in practice, so slides 2 and 3 are two valid textbook codings, not an error.
- Model box caption "(Any value) -> (-1,+1)": CONFIRMED — "Perceptrons: The First Neural Network Model", https://towardsdatascience.com/perceptrons-the-first-neural-network-model-8b3ee4513757/ — unlike slide 2, this slide's activation is genuinely bipolar, so a model emitting (-1,+1) is correct here; the step plot's y-levels -1 and +1 agree.
- "Bi-polor step" spelling: CORRECTED (spelling) — the standard term is "bipolar step" (or sign function) — Raschka STAT 453 lecture notes, https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L03_perceptron_slides.pdf — "Bi-polor" is a course typo; keep it verbatim for recreation, but do not propagate the misspelling into any spec annotation.

## Second-opinion (lane D, 2026-10-31)

Method: `mcp__agy-cli-mcp__agy_web_search`, 5 batches x 4 queries, URLs resolved live. Verdict: content CONFIRMED; spelling CORRECTED stands. New confirming sources: GeeksforGeeks perceptron rule (https://www.geeksforgeeks.org/deep-learning/what-is-the-perceptron-rule/), Cornell CS4780 lecturenote03 (https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html), thomascountz.com perceptron post, Wikipedia Perceptron — the sign/bipolar step is f(z)=+1 if z>=0 else -1, decision cutoff at zero, paired with {-1,+1} targets; "bipolar step" is the standard term, "Bi-polor" stays verbatim on the frame only.

## Cross-check (lane F, 2026-10-31, agy web search)

- "Bi-polar step (-1, +1)" with "Threshold at zero" and labels (+1, -1): CONFIRMED — Analytics Vidhya activation-functions guide (https://www.analyticsvidhya.com/blog/2022/01/activation-functions-for-neural-networks-and-their-implementation-in-python/) and NYU CS6673 SimpleNN notes (https://cse.engineering.nyu.edu/~mleung/CS6673/s08/SimpleNN.pdf): the bipolar step (= sign function) maps net >= 0 to +1 and net < 0 to -1, i.e. output range {-1, +1} with decision threshold 0, and perceptrons using it are labeled with bipolar targets +1/-1. Matches the frame exactly. No corrections.
