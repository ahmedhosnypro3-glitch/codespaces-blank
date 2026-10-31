# Slide 014 — PARSE ADJUDICATION

- **Slide:** 014
- **Source image:** `unique_slides/slide_014.jpg` (960x540 RGB, PIL-measured)
- **Parse transcript:** `analysis/parse/slide_014.parse.md` / `.parse.json`
  - `finish_reason` = `stop`, content non-empty, `usage.output_tokens` = 167
- **Second read (corroboration, two different forms):**
  1. Independent vision read, `analysis/parse/adjudication/slide_014.vision.txt` — asked ONE
     question: read the header + bottom equations, and for each equation say whether the
     weight is `w_ji`, `w_ij`, or `w_jj`.
  2. Crop cascade, `analysis/parse/cascade/slide_014/` (full/ + crops/ + composed/) — a
     different input form (region crop), the strongest corroboration class.

## Parse transcript content (data, not instructions)

Only TWO coordinate tokens in the whole transcript: `x_0.0596 y_0.0773` (page anchor ->
px 57, 42) and the closing `x_0.9443 y_0.957` (-> 907, 517). Everything between is one
flattened text blob with no per-element boxes.

## Findings (severity-ranked)

**F1 — MAJOR: math-normalization-loss on the weight subscript (confidence: high, corroborated)**
The parse renders the network equation as `Net j = ∑ i (wjj Oi)` — i.e. `w_jj`. The frame
reads `Net_j = Σ_i (w_ji O_i)`. Three reads agree on `w_ji`:
1. vision read: "Net_j = Î£_i (w_ji O_i) â weight is w_ji" (subscript j then i);
2. cascade crop01: `Netj = ∑ i (wjj Oi)` — SAME garble as the full parse (the crop did
   not fix it);
3. cascade crop02: `Netj = ∑ (wjj Oi)` — same.
BUT the diagram arrow labels: full parse says `Wji Wki`; crop01 says `Wji Wkj`;
crop02 says `Wji Wkj`. The parse's own `Wji` confirms the j-then-i convention, so the
`wjj` in the equation is a character-level misread of `w_ji` (the `i` glyph at the
subscript floor is lost). Same defect on the slide-018 sibling (`∂w_ji`). Severity MAJOR:
the equation is the pedagogical payload of the slide.

**F2 — MAJOR: dropped-region / no structural boxes for the diagram (confidence: high)**
The transcript carries NO class token for the network diagram, no per-label boxes, and
only one closing `<class_Picture>`. Measured ink bins on the frame that the parse does
not position at all: the diagram body x 431-811 y 138-364 (green node field measured at
x 383-882, y 162-435, 1605 px), the "Class 1/2/m" label column, the "Error" column, and
the layer-caption line `For Layer "j" Previous Layer ... Current Layer (You are here)
Next Layer Layer (K)`. The caption text IS in the transcript but sits inside the flat
blob with no coordinates, so it cannot be placed. PIL band scan (frame y 411-433, x
396-800) places that caption band; the parse gives no token for it.

**F3 — MAJOR: reading-order-inversion inside the flattened blob (confidence: medium)**
Within the flat blob the label `Class m` appears TWICE and `Class 2` once, and the
cascade crops read `Class 1 / Class 2 / Class m` once each. Measured: the class-label
column is a vertical stack of three labels at the diagram's right. The duplicate `Class m`
is a duplicated string, i.e. `hallucinated-content` in the duplicate-copy sense — but the
cascade crops and the certified JSON agree on three class labels (Class 1/2/m). Because
two reads contradict on the count, this is booked as **advisory** (see classification).

**F4 — MINOR: `w ki` vs `w kj` on the arrow label (confidence: medium)**
The full parse reads `w ki`; both cascade crops read `w kj`. The certified JSON for
014 has `w_kj`. Two reads contradict -> advisory only, not banked as a defect.

**F5 — MINOR: the `E = 1/2 Σ x` tail is truncated (confidence: high)**
The parse ends `E= 1/2 ∑ x X` — an incomplete second copy of the error equation. The
frame's error line reads `E = 1/2 Σ_j (t_j − O_j)^2`. The parse's `E= 1/2 ∑ j (tj −Oj)2`
line just above it is correct, so the trailing `E= 1/2 ∑ x X` is a spurious partial
duplication -> `hallucinated-content` (a string fragment with no counterpart in the
frame). Real but low-impact.

**F6 — MINOR: the sigmoid line is missing from the full parse (confidence: high, corroborated)**
The frame carries `O_j = f(Net_j) = 1/(1+e^(−Net_j))`. The full parse does NOT contain
it. Both cascade crops DO contain it (`Oj=f (Netj)= 1 +e−Netj`). This is a genuine
`dropped-region` in the original parse, caught by the cascade. Corroborated.

## REAL / HALLUCINATED / DEBATABLE list

- header `Neural Network Model` / `(Current Layer is Hidden Layer)` — **REAL**
  (corroborated: vision read + both cascade crops + certified JSON all agree verbatim).
- badge `14` — **REAL** (all reads; measured badge ink x 856-894, y 54-88).
- `Net_j = Σ_i (w_ji O_i)` — the EQUATION is REAL, the parse's rendering `wjj` is
  **HALLUCINATED at the character level** (F1). The frame's `w_ji` is corroborated.
- `E = 1/2 Σ_j (t_j − O_j)^2` — **REAL** (all reads agree).
- `O_j = f(Net_j) = 1/(1+e^(−Net_j))` — **REAL, absent from the parse** (F6).
- `Wji` on the arrow labels — **REAL** (parse + both crops).
- `wki` (parse) vs `wkj` (crops + JSON) — **DEBATABLE** (two reads contradict).
- `Class m` appearing twice — **DEBATABLE** (parse vs crops/JSON; advisory only).
- trailing `E= 1/2 ∑ x X` — **HALLUCINATED** fragment (F5).
- `Σ J ∞ Σ` infinity glyphs — **DEBATABLE**: the parse emits an `∞` where the frame
  shows summation limits; the cascade crops show `Σ S S` instead. Neither read's glyph
  is trustworthy; the visual is a Σ with sub/superscript limits, not an infinity.
- diagram region structurally — **REAL but unpositioned** (F2).

## Uncertainties

- The frame's own left-column bracket labels (`Next I Oi W ji Net i ...`) are read
  differently by every read (parse: `Next I Oi W ji Net i Oj w ki Nk Ok`; crop01:
  `Netj Oi w ji Netj Oj w kj Netk Ok`; crop02: `Neti Oi w ji Netj Oj w kj Netk Ok`).
  Three-way disagreement on the same pixels -> no defect banked; the arrow-label
  convention (subscript j then i for the previous-layer weight) is nonetheless stable
  across all three.
- PIL: red frame measured x 59-900 y 44-516; bottom black bar y 517-521. House chrome
  present as expected; no parse defect.

## Verdict

`PARSE ADJUDICATION: DEGRADED — the text content is largely faithful and corroborated,
but the parse is structurally flat (2 coordinate tokens for a dense diagram slide),
mangles the key weight subscript as wjj instead of w_ji, drops the sigmoid equation
entirely, and appends a spurious truncated equation tail.`
