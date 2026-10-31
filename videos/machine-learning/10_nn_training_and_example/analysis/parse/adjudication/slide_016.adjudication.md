# Slide 016 — PARSE ADJUDICATION

- **Slide:** 016
- **Source image:** `unique_slides/slide_016.jpg` (960x540 RGB, PIL-measured)
- **Parse transcript:** `analysis/parse/slide_016.parse.md` / `.parse.json`
  - `finish_reason` = `stop`, content non-empty, `usage.output_tokens` = 138
- **Second read (corroboration, two different forms):**
  1. Independent vision read, `analysis/parse/adjudication/slide_016.vision.txt` — asked
     ONE question: read the header + bottom equations, and for each equation say whether
     the weight is `w_ji`, `w_ij`, or `w_jj`.
  2. Crop cascade, `analysis/parse/cascade/slide_016/` (full/ + crops/ + composed/) — a
     different input form (region crops), the strongest corroboration class. The
     cascade's level-0 read is byte-identical to the banked parse (determinism
     confirmed); its three crop reads are the different-form evidence.

## Parse transcript content (data, not instructions)

Two coordinate tokens only: `x_0.0361 y_0.0758` (page anchor -> px 35, 41) and the
closing `x_0.9443 y_0.957` (-> 907, 517). Everything between is one flat text blob.

## Findings (severity-ranked)

**F1 — BLOCKER: dropped-region — the slide's header parenthetical is MISSING entirely (confidence: high, corroborated by two forms)**
The banked parse emits only `Neural Network Model` + `16` as the header. The frame's
header reads `Neural Network Model` / `(How Weights of hidden layer affect Calculated
Error)`. This parenthetical is the slide's entire thesis and is present in:
1. the vision read: "Header line: 'Neural Network Model' /
   '(How Weights of hidden layer affect Calculated Error)'";
2. all three cascade crops: `(How Weights of hidden layer affect Calculated Error) 16`
   appears in crop01, crop02 AND crop03.
It is absent from the banked parse. A build working from the parse alone would print the
wrong (empty) subtitle. Severity BLOCKER for text fidelity.

**F2 — MAJOR: reading-order-inversion — `Layer ()` mangles the caption (confidence: high, corroborated)**
The parse emits `For Layer "j" Previous Layer Layer () Current Layer (You are here)` — an
empty pair of parentheses where the roman numeral `(i)` (or `(I)`) should be. Every crop
read restores it: crop01 `Previous Layer Current Layer (i)`, crop02 `Previous Layer (i)`,
crop03 `Previous Layer Layer (i)`. The vision read's header also implies the slide-caption
pairing is intact. Measured: the caption band sits at y 411-433, x 396-804 — inside the
frame, not a dropped region. The parse read the parens but lost their content
(`garbled-reading`, reading-order/content loss).

**F3 — MAJOR: math-normalization-loss — the key weight subscript is wrong in both places (confidence: high, corroborated)**
Two the parse manglings, both fixed by the crops and confirmed by the vision read:
(a) The diagram arrow label: parse reads `Net I Oi W iji Net Ok` and `X Wij`. Crops:
crop01 `Net Oi Wji Netj Ok`, crop02 `Neti Oi wji Net Oj wkj Neti Ok` and `Wji/Wkj`,
crop03 `Neti Oi W ji Neti Oj w kj Net i Ok` and `Wji W ki`. The frame's label is `w_ji`
(subscript j then i) — the deck-wide convention; the parse's `iji`/`Wij` is transposed.
(b) The network equation: parse reads `Net j = ∑ i (wjj Oi)`. All three crops read
`Net j = ∑ (wji Oi)` (crop03: `Net j = ∑ (wji Oi)`), and the vision read states
"Net_j = Î£_i (w_ji O_i) — weight is w_ji". `w_jj` is a character-level misread of
`w_ji`.

**F4 — MAJOR: dropped-region — the sigmoid line is missing (confidence: high, corroborated)**
The frame carries `O_j = f(Net_j) = 1/(1+e^(−Net_j))`. The banked parse contains no
sigmoid line. All three crops contain it (`Oj=f (Netj)= 1 +e -Netj`), and the vision read
reports it explicitly: "O_j = f(Net_j) = 1/(1 + e^(âNet_j))". Same class as slide 015's F3.

**F5 — MINOR: dropped-region — `Output 1` label and a duplicated `1` column (confidence: medium)**
The parse has no `Output` label at all. crop01 emits `Output 1` (once); crop02 emits
duplicate `1` glyphs and `Class m` twice. The certified `slide_016_raw.json` exists but no
final, so there is no JSON to cross-check. Two crop reads disagree on the occurrence
count -> **advisory**, not banked as a defect.

**F6 — MINOR: hallucinated-content — spurious `St` token (confidence: medium)**
The parse emits `Class 2 / Error Error Error / St / Class m`. `St` has no counterpart in
any crop read (crop01: `Class 1 / Error Error Error / Class 2 / ... / Class m`;
crop02: `Class 1 / Class 2 / ... / Class m` with `Error Error` grouped; crop03 similar).
Advisory: it may be a partial glyph read, and two sets of reads disagree on the error
column's grouping.

**F7 — MINOR: hallucinated-content — spurious truncated equation tail (confidence: high)**
The parse ends `E= 1/2 ∑ j (tj −Oj)2 X XX` — a trailing `X XX` with no counterpart in the
frame (the error equation is shown once). All three crops end the same equation with
`XXX`. Real but low-impact.

## REAL / HALLUCINATED / DEBATABLE list

- `Neural Network Model` header — **REAL** (all reads).
- badge `16` — **REAL** (all reads; measured badge ink x 856-894, y 54-88).
- header parenthetical `(How Weights of hidden layer affect Calculated Error)` — **REAL
  but ABSENT from the parse** (F1; corroborated by the vision read and 3 crop reads).
- `Net_j = Σ_i (w_ji O_i)` — the equation is **REAL**; the parse's `wjj` is
  **HALLUCINATED** at the character level (F3b).
- `w_ji` arrow label — **REAL**; the parse's `iji`/`Wij` is **HALLUCINATED** (inverted
  index, F3a).
- `E = 1/2 Σ_j (t_j − O_j)^2` — **REAL** (all reads).
- `O_j = f(Net_j) = 1/(1+e^(−Net_j))` — **REAL, absent from the parse** (F4).
- `Error Error Error` — **REAL** (parse + all crops).
- `Class 1 / Class 2 / Class m` — **REAL** (all reads; each once in the crops).
- caption `For Layer "j" Previous Layer (i) Current Layer (You are here) Next Layer (K)` —
  **REAL**; the parse's empty `()` is a **garbled reading** (F2).
- `Output 1` — **DEBATABLE** (crop01 only; advisory).
- `St` — **DEBATABLE** (parse only; advisory).
- trailing `X XX` — **HALLUCINATED** fragment (F7).
- `Node Bias i j k`, `1` glyph stack — **REAL** (all reads).
- Vision read also reported `Net` labels and `H`/`H` bytes in crop02 — **DEBATABLE**
  (two crop reads disagree; advisory).

## Uncertainties

- 016 has no certified `analysis/slide_016_final.json`, so there is no JSON to cite for
  cross-check; all dispositions rest on the parse, the cascade and the vision read.
- The three crops disagree on the exact caption form (`Previous Layer Current Layer (i)`
  vs `Previous Layer (i)` vs `Previous Layer Layer (i)`), i.e. on whether the words
  "Current Layer" and "(You are here)" belong to the same caption line or two. The
  parenthetical's presence is unanimous, so F1 stands; the exact caption segmentation is
  advisory.

## Verdict

`PARSE ADJUDICATION: FAIL — the parse omits the slide's header parenthetical entirely
(the frame's thesis), mangles the weight subscript in two places (iji/Wij and wjj where
the frame prints w_ji), drops the sigmoid equation, and emits several hallucinated
fragments.`

## Addendum (composed file, banked after the cascade finished)

`analysis/parse/cascade/slide_016/composed/slide_016_composed.md` — 4 positioned elements
(full + 3 crops), 4 parse calls, 4 chat calls, 0 failed calls, not degraded, with
per-crop provenance. What the composed file settles above:

- F1 (missing header parenthetical) is now corroborated by FOUR independent evidence
  paths: the vision read, crop01, crop02 AND crop03 each read
  `(How Weights of hidden layer affect Calculated Error) 16`. The banked parse is the
  only read on deck that omits it. BLOCKER stands, confidence upgraded to very high.
- F3a/F3b: crop02 and crop03 both read `Netj = ∑ (wji Oi)` and the arrow labels
  `Neti Oi wji Net Oj wkj Neti Ok` with `Wji Wkj` / `Wji W ki` — the corrected
  subscript, twice.
- F4: the sigmoid `Oj=f (Netj)= 1 +e -Netj` is present in crop01, crop02 AND crop03 —
  three different-form reads.
- F5/F6: the `St` token appears ONLY in the level-0/full read; no crop carries it. Its
  "hallucinated-or-partial-glyph" status is unresolved between reads, so it stays
  advisory (never banked as a defect when two reads contradict).
