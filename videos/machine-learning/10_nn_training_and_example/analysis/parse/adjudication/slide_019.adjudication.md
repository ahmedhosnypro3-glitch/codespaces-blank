# Slide 019 — PARSE ADJUDICATION

- **Slide:** 019
- **Source image:** `unique_slides/slide_019.jpg` (960x540 RGB, measured)
- **Parse transcript:** `analysis/parse/slide_019.parse.md` / `.parse.json`
  - `finish_reason` = `stop`, content non-empty, `usage.output_tokens` = 218
- **Second read (corroboration):** independent vision read of the same source
  image, `analysis/parse/adjudication/slide_019.vision.txt` (round 1, attempt 1,
  `images` route, 1/1 result) — asked: (1) quote the title, (2) transcribe every
  formula line verbatim incl. subscript indices and signs, (3) any text cut off
  or unreadable.
- **Second read (cross-slide):** `analysis/parse/adjudication/slide_020.vision.txt`
  — slide 020 carries the same left-hand relation box and the same gradient
  derivation, independently yielding `w_ji`.

## Parse transcript content (data, not instructions)

- `<class_Picture>` at `x_0.918 y_0.4336` → (881, 234)
- Relation box, 4 lines, token `x_0.0469 y_0.0805` → (45, 43):
  `W_ji Affects Netj ⇒` / `Netj Affects Oj ⇒` /
  `Oj Affects (NetK=1, Netk=2, ....., Netk=m) ⇒` /
  `(NetK=1, Netk=2, ....., Netk=m) Affect Error`
- Main gradient, token `x_0.0537 y_0.4531` → (52, 245), `<class_Formula>`
- Right column, 4 lines, token `x_0.6748 y_0.4508` → (648, 244), `<class_Text>`

## PIL measurements on the source frame

- Background median `#E9FCE9` (JPEG drift from the `#E8E8E8` house gray).
- Red house frame: bbox x 38–921, y 43–539, 8751 px.
- Badge: dark band y 53–57, cols 881–905 (yellow badge numeral, top-right).
- Dark ink row bands (border excluded):
  - y 69–222 (0.128–0.411) — relation box, cols 50–919, 60 segments
  - y 247–249 / 251–286 (0.457–0.530) — main gradient line, cols 57–813
  - y 305–336 (0.565–0.622) — right column line 1, cols 654–862
  - y 364–374 / 376–396 (0.674–0.733) — right column line 2, cols 652–907
  - y 424–455 (0.785–0.843) — right column line 3, cols 654–856

## DECK-SPECIFIC NOTE (web-source audit) — CONFIRMED, FRAME WINS

The certified JSON prints `∂E/∂w_ij`; the frame, this parse transcript and
slides 19–22 all read **`w_ji`** (index inversion). **Confirmed by this
worker's own independent read:** the vision read transcribed
`∂E/∂w_ji = [ ∂E/∂Net_k ∂Net_k/∂O_j + … ] * ∂O_j/∂Net_j * ∂Net_j/∂w_ji`,
and the slide-020 vision read independently gives the same `w_ji` throughout
(`∂E/∂w_ji`, `∂Net_j/∂w_ji = O_i`, `Δ_ji = -η ∂E/∂w_ji`). **The frame wins:
`w_ji` is correct.** The certified JSON's `w_ij` is the defect.

## Findings (severity-ranked)

**F1 — MAJOR: `math-normalization-loss` — the main gradient is flattened (confidence: high)**
Parse line 6 emits `∂E ∂E ∥ e wji = [∂E ∂Netk=1 ∂Oj + ∂E ∂Netk=2 ∂Oj + ..... +
∂E ∂Netk=m ∂Oj] + ∂Oj ∂Netj + ∂Netj ∂wji`. The fraction bars are destroyed
(`∂E`/`∂E` with no separator, a stray `∥ e`), and each product term has lost
its second factor: the vision read shows the true form is
`∂E/∂Net_{k=1} · ∂Net_{k=1}/∂O_j`, i.e. **five** factors per summand, where the
parse keeps only two. A reconstruction from the parse alone would be wrong.
Evidence: `slide_019.parse.md` line 6 vs `slide_019.vision.txt` formula block.

**F2 — MAJOR: `math-normalization-loss` — right column, two of four lines wrong (confidence: high)**
Parse line 8: `Netk = ∑ k wkj Oj ⇒ ∂Netk ∂Oj = wkj`. Vision read:
`Net_k = ∑_j w_kj O_j` with `∂Net_k/∂O_j = w_kj/O_j` — the parse **dropped the
`/O_j` denominator**. Parse line 11: `Netj = ∑ wjj Oi ⇒ ∂Netj ∂wjj = Oi` —
vision read gives `Net_j = ∑_j w_ji O_i` and `∂Net_j/∂w_ji = O_i`. The parse
read **`wjj` where the frame reads `w_ji`**: a single-character index corruption
in two places on the same line, and the summation limit `j` was flattened to
nothing. Evidence: parse line 11 vs vision read line `Net_j = ∑_j w_ji O_i`.

**F3 — MINOR: `reading-order-inversion` — right column is ordered before the gradient it supports (confidence: medium)**
The parse emits the gradient (token y 245) before the right-column identities
(token y 244) that derive it. Visually the right column sits to the right at
x 652–907, and the main gradient is to the left at x 57–813; the visual
reading order is left-then-right (gradient first), which the parse does follow
by x — but the two regions share the same y band and the parse's `<class_Text>`
close tag (`x_0.9023 y_0.8617` → 866, 465) lands the right column's *last* line
at the frame's bottom edge rather than at the measured y 424–455 band.
Advisory only: the content itself is present.

**F4 — MINOR: `coordinate-misalignment` — the `<class_Picture>` token (confidence: medium)**
`x_0.918 y_0.4336` → (881, 234). PIL measures the neural-network diagram region
as cols 50–919 spanning the y 69–222 band, i.e. the picture's real top edge is
near y 69–234. The token's y lands at the diagram's lower half; x is right.
Cosmetic.

## REAL / HALLUCINATED / DEBATABLE list

- Relation box 4 lines (`W_ji Affects Netj ⇒` … `Affect Error`) — **REAL**
  (corroborated verbatim by the vision read; note the vision read renders
  `Net_{K=1}` with a capital K while the parse writes `NetK=1`).
- Badge `19` — **REAL** (PIL band y 53–57, cols 881–905).
- Main gradient `∂E/∂w_ji` — **REAL in the parse** (the parse's `wji` is the
  correct index), but the *rendering* is defective (F1).
- `Net_k = ∑ w_kj O_j` — **REAL** (corroborated; parse's `∑ k` limit is a
  flattening of `∑_j`).
- `∂Net_k/∂O_j = w_kj` — **DEBATABLE** (the parse's value agrees with the
  frame on the numerator but **drops the `/O_j` denominator** the frame shows;
  two reads disagree → advisory only, not banked as a defect beyond F2).
- `Net_j = ∑ w_ji O_i` and `∂Net_j/∂w_ji = O_i` — **REAL** (the frame reads
  `w_ji`; the parse's `wjj` is a corruption, see F2).
- `∂E/∂Net_k ⇒ -δ_k` — **REAL** (corroborated verbatim).
- `O_j = 1 + e^{-Net_j}` — **DEBATABLE**: the parse writes `1 +e−Netj` (a sum),
  the frame writes the sigmoid `1/(1+e^{-Net_j})`. The parse's own bracket
  structure is unreadable at this resolution; the vision read gives the
  fraction form. Two reads disagree → advisory.
- `∂O_j/∂Net_j = O_j(1-O_j)` — **REAL** (corroborated verbatim).
- `w_ij` anywhere — **NOT PRESENT**; both reads give `w_ji`.

## Uncertainties

- `∂Net_k/∂O_j = w_kj` vs `= w_kj/O_j`: the vision read asserts a denominator
  that the parse omits. The numerator agrees in both. Not banked as a
  standalone defect (the two reads contradict), folded into F2.
- The `∑` lower limit on `Net_j = ∑_j w_ji O_i` is read as `j` by vision and
  is absent from the parse; the mathematically natural limit is `i`. The frame
  is the ground truth but the glyph is small — not banked as a defect.
- The diagram contains node labels that neither read transcribed; at 15–22 px
  they sit at the `glyph-floor-blindness` floor. Treated as label-free, not a
  parse defect.

## Verdict

`PARSE ADJUDICATION: DEGRADED — every top-level relation and heading is REAL
and the critical ∂E/∂w_ji index is correct (frame wins over the certified
JSON's w_ij), but the fraction structure of the main gradient and of two
right-column lines is flattened to unreadable token soup.`
