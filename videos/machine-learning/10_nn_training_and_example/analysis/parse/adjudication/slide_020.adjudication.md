# Slide 020 — PARSE ADJUDICATION

- **Slide:** 020
- **Source image:** `unique_slides/slide_020.jpg` (960x540 RGB, measured)
- **Parse transcript:** `analysis/parse/slide_020.parse.md` / `.parse.json`
  - `finish_reason` = `stop`, content non-empty, `usage.output_tokens` = 282
- **Second read (corroboration):** independent vision read of the same source
  image, `analysis/parse/adjudication/slide_020.vision.txt` (round 1, attempt 1,
  `images` route, 1/1 result) — asked: (1) quote the title or say none,
  (2) transcribe every formula line verbatim incl. subscript indices, summation
  limits and signs, (3) any text cut off or unreadable.
- **Cross-slide corroboration:** slide 019 carries the same left-hand relation
  box and the same gradient derivation; `slide_019.vision.txt` independently
  yields the same `w_ji` indices.

## Parse transcript content (data, not instructions)

- Relation box, 4 lines, token `x_0.04 y_0.0742` → (38, 40)
- 5 formula lines, all inside one `<class_Picture>` closing at
  `x_0.9658 y_0.9914` → (927, 535)
- Line 5 closes with `Where δj = ∑ mk=1 δkwwkj ∗ Oj(1−Oj) _( for each Node j at hidden layer )_`

## PIL measurements on the source frame

- Background median `#F1F9E8` (JPEG drift from the `#E8E8E8` house gray).
- Red house frame: bbox x 38–921, y 43–539, 12231 px.
- Badge: dark band y 53–57, cols 881–905 (top-right numeral).
- Dark ink row bands (border excluded):
  - y 68–222 (0.126–0.411) — relation box, cols 50–913, 58 segments
  - y 247–286 (0.457–0.530) — formula line 1, cols 57–814
  - y 305–349 (0.565–0.646) — formula lines 2–3, cols 58–862
  - y 361–398 (0.669–0.737) — formula line 4, cols 148–907
  - y 424–482 (0.785–0.893) — formula line 5, cols 50–859
  - y 501–509 (0.928–0.943) — the `Where …` tail, cols 59–631

## DECK-SPECIFIC NOTE (index inversion) — CONFIRMED AGAIN

Slide 020's parse writes `wjj` in places and `w_ji` in others. The vision
read gives `∂E/∂w_ji`, `∂Net_j/∂w_ji = O_i`, `Δ_ji = -η ∂E/∂w_ji` and
`∂Net_k/∂O_j = w_kj/O_j` — **the frame reads `w_ji` (j-th weight, i-th
input), matching slides 019 and 022.** The certified JSON's `w_ij` remains
wrong; the frame wins.

## Findings (severity-ranked)

**F1 — MAJOR: `math-normalization-loss` — every formula line is flattened (confidence: high)**
All five formula lines lose their fraction structure. Parse line 5:
`∂E ∂E ∂E k=1 ∂Netk=1 ∂Oj + ∂E ∂Netk=2 + .....+ ∂E ∂Netk=m ∂Oj + ∂Oj ∂Netj
+ ∂Netj ∂wjj` — the vision read gives the true structure as
`∂E/∂w_ji = ∂E/∂Net_{k1} · ∂Net_{k1}/∂O_j · ∂O_j/∂Net_j · ∂Net_j/∂w_ji
+ … + ∂E/∂Net_{km} · ∂Net_{km}/∂O_j · ∂O_j/∂Net_j · ∂Net_j/∂w_ji`.
The parse keeps **one** factor per summand where the frame has **four**, and
the `∑_{k=1}^{m}` limit is destroyed into a bare `k=1`. A reader could not
reconstruct the derivation from this transcript. Evidence: `slide_020.parse.md`
lines 5–8 vs `slide_020.vision.txt` LaTeX blocks.

**F2 — MAJOR: `math-normalization-loss` — the `Δ_ji` line is corrupted (confidence: high)**
Parse line 8: `Δjj = -η ∂EW j = ∑ m δkwkj ⇒ Oj(1−Oj) ∗ Oi = η δj ∗ Oi`.
Vision read: `Δ_ji = -η ∂E/∂w_ji = η ∑_{k=1}^{m} δ_k w_kj O_j(1-O_j) * O_i
= η δ_j * O_i`. The parse has **`Δjj` where the frame reads `Δ_ji`** (the same
j/i inversion as the certified JSON), and it flattens `∂E/∂w_ji` to `∂EW j`
and `∑_{k=1}^{m}` to `∑ m`. Evidence: parse line 8 vs vision read
`Δ_ji = -η ∂E/∂w_ji`.

**F3 — MAJOR: `math-normalization-loss` — the `∂E/∂O_j` derivation row is mangled (confidence: high)**
Parse line 7: `∂E E∂Oj ∂E/∂Netj ∂E/∂Netj=-δj ∂E/∂wjj` — a single
unpunctuated token run in which the `∂E/∂O_j` subject, the `∂E/∂Net_j = -δ_j`
underbrace label and the `∂E/∂w_ji` label have been concatenated with no
separators, and the underbrace/underbrace decoration is entirely absent.
The vision read shows the frame has red brace annotations carrying those
labels. Evidence: parse line 7 vs vision read's underbrace analysis.

**F4 — MINOR: `math-normalization-loss` — `δkwwkj` doubles the `w` (confidence: high)**
Parse line 9: `Where δj = ∑ mk=1 δkwwkj ∗ Oj(1−Oj)`. Vision read:
`δ_j = ∑_{k=1}^{m} δ_k w_kj · O_j(1-O_j)`. The parse emits `δkwwkj` — a
duplicated `w` — and folds the `O_j(1-O_j)` factor into the same product where
the frame shows it outside. Evidence: parse line 9 vs vision read.

**F5 — MINOR: `coordinate-misalignment` — the single `<class_Picture>` close (confidence: medium)**
`x_0.9658 y_0.9914` → (927, 535) is the frame's bottom-right corner. The
formula region actually measured spans y 247–509 and x 50–914. The token marks
the outer wrapper, not the formula block. Cosmetic.

## REAL / HALLUCINATED / DEBATABLE list

- Relation box 4 lines (`W_ji Affects Netj ⇒` … `Affect Error`) — **REAL**
  (corroborated verbatim by the vision read; the vision read renders the
  output-node indices as `Net_{K,1}`/`Net_{K,2}`/`Net_{K,m}` with a capital K
  and a comma, while the parse writes `NetK=1`/`Netk=2` — same content,
  different punctuation).
- `∂E/∂w_ji` — **REAL** (corroborated; the parse's `∂EW j` is the flattening
  of this, and the `wjj` variants are corruptions — see F2/F3).
- `∂E/∂Net_k ⇒ -δ_k` — **REAL** (corroborated verbatim).
- `Net_k = ∑_j w_kj O_j` — **REAL** (corroborated; parse's `∑ k` limit is a
  flattening of `∑_j`).
- `∂Net_k/∂O_j = w_kj/O_j` — **DEBATABLE**: the vision read asserts a `/O_j`
  denominator the parse omits; the numerator agrees in both. Two reads
  contradict → advisory only, not banked as a standalone defect.
- `O_j = 1/(1+e^{-Net_j})`, `∂O_j/∂Net_j = O_j(1-O_j)` — **DEBATABLE**: the
  parse writes `Oj= 1 +e−Netj` (a sum, not a sigmoid fraction). The frame
  reads the sigmoid `1/(1+e^{-Net_j})`. Reads contradict → advisory.
- `∂O_j/∂Net_j = -δ_j` vs `∂E/∂Net_j = -δ_j` — **DEBATABLE** (the parse's
  underbrace label and the vision read's differ on which quantity carries the
  `= -δ_j` label).
- `Δ_ji = -η ∂E/∂w_ji = η δ_j * O_i` — **REAL** (corroborated, modulo the
  flattening in F2).
- `δ_j = ∑_{k=1}^{m} δ_k w_kj · O_j(1-O_j)` — **REAL** (corroborated; the
  parse's `δkwwkj` is the corruption in F4).
- `(for each Node j at hidden layer)` — **REAL** (corroborated; the vision
  read gives the same parenthetical).
- Badge `20` — **REAL** (PIL band y 53–57, cols 881–905).
- `w_ij` anywhere on the frame — **NOT PRESENT**; both reads give `w_ji`.

## Uncertainties

- Whether `∂Net_k/∂O_j` carries a `/O_j` denominator, and whether the `= -δ_j`
  underbrace labels `∂E/∂Net_j` or `∂O_j/∂Net_j`: the vision read and the
  parse disagree and neither is a pixel-level authority at this resolution.
  Both left DEBATABLE and unbanked as defects.
- The red underbrace/underbrace decorations in the lower-left derivation block
  are present on the frame but appear in neither transcript as structure. If
  the braces carry the `= -δ_j` labels, that is part of F3's flattened region.
- Small subscripts (`O_i`, `w_kj`) sit near the `glyph-floor-blindness` band;
  both reads agree on their values, so they are treated as corroborated.

## Verdict

`PARSE ADJUDICATION: DEGRADED — all top-level content is REAL and the w_ji
index is confirmed correct, but all five formula lines are flattened to
unreadable token soup with the Δ_ji line and the ∂E/∂O_j row corrupted;
structural (brace/underbrace) annotations are lost entirely.`
