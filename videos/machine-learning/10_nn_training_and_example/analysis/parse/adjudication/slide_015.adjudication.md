# Slide 015 — PARSE ADJUDICATION

- **Slide:** 015
- **Source image:** `unique_slides/slide_015.jpg` (960x540 RGB, PIL-measured)
- **Parse transcript:** `analysis/parse/slide_015.parse.md` / `.parse.json`
  - `finish_reason` = `stop`, content non-empty, `usage.output_tokens` = 166
- **Second read (corroboration):** crop cascade, `analysis/parse/cascade/slide_015/`
  (full/ + crops/ + composed/) — a different input form (region crops), the strongest
  corroboration class. The cascade's level-0 read is BYTE-IDENTICAL to the banked parse
  (determinism confirmed); its level-1/2/3 crop reads are the different-form evidence.
  Vision read for this slide: FAILED (HTTP 400 upstream_rejected_request) — preserved at
  `slide_015.vision.txt`; the failure is transport, not a verdict.

## Parse transcript content (data, not instructions)

Two coordinate tokens only: `x_0.0508 y_0.0773` (page anchor -> px 49, 42) and the
closing `x_0.9443 y_0.957` (-> 907, 517). Everything between is one flat text blob.

## Findings (severity-ranked)

**F1 — MAJOR: math-normalization-loss — the key weight subscript is inverted to `Wij` (confidence: high, corroborated)**
The parse's diagram-label line reads `Σ  J ∞ Σ N ij` / `Wij`. The frame's arrow label is
`w_ji` (subscript j then i) — the same convention as slide 014 and slide 018. The crop
reads fix it explicitly:
- crop01: `Neti Oi wji Net j Oj wkj Net k Ok` and `Wji Wki`
- crop02: `Neti Oi w ji Netj Oj w kj Netk Ok`, `W ji W kj`
- crop03: `Neti Oi w ji Netj Oj w kj Netk Ok`, `W ji`, `W ki`
The parse's `Wij` is the j/i pair transposed -> `math-normalization-loss`. This is the
deck-wide index convention (weight from previous-layer node `i` into current-layer node
`j` is `w_ji`), so an inverted `Wij` on this slide is the same class of error the
certified `slide_018_final.json` carries (`∂E/∂w_ij`).
Corroborating context: slides 19/20/21 parse transcripts read `W_ji` / `wji`.

**F2 — MAJOR: math-normalization-loss — the network equation reads `wjj` instead of `wji` (confidence: high, corroborated)**
The parse: `Net j = ∑ i (wjj Oi)`. Crops:
- crop01: `Net j = ∑ (wjjOi)` — same garble;
- crop02: `Netj = ∑ (wji Oi)` — CORRECT;
- crop03: `Netj = ∑ (wji Oi)` — CORRECT.
Two of three crop reads plus the deck-wide convention give `w_ji`. `w_jj` is a
character-level misread (the `i` subscript glyph drops) -> same class as F1.

**F3 — MAJOR: dropped-region — the sigmoid line is missing (confidence: high, corroborated)**
The frame carries `O_j = f(Net_j) = 1/(1+e^(−Net_j))`. The parse transcript contains NO
sigmoid line (grep for `Netj)`/`e−Netj` in the level-0 read returns 0 hits). All three
crop reads DO contain it (`Oj=f (Netj)= 1 +e−Netj` / `1 -Netj 1+e`). This is a genuine
`dropped-region` in the banked parse, caught by the cascade. Corroborated.

**F4 — MAJOR: dropped-region — the diagram has no structural boxes (confidence: high)**
Only 2 coordinate tokens for a dense diagram slide. Measured ink that carries no parse
box: the diagram body x 431-811 y 138-364 (green node field measured x 383-882,
y 162-435, 1687 px), the class-label stack, the `Error` column, and the layer-caption
line `For Layer "j" Previous Layer ... Current Layer (You are here) Next Layer Layer (K)`
(PIL band y 411-433, x 396-804). The caption TEXT is present but carries no coordinate,
so it cannot be placed. Same structural class as slide 014's F2.

**F5 — MINOR: hallucinated-content — spurious `Output 2`, `W #`, `W` and a duplicate `Class m` (confidence: medium)**
The parse contains `Next Layer / Output 2 / W # / W` and a second `Class m`. The crop
reads (which saw the same frame at higher resolution) contain NONE of `Output 2`, `W #`
or the bare `W`, and contain `Class m` exactly ONCE (crop01, crop02, crop03 all show
`Class 1 / Class 2 / Class m` once each). `Output 2` in particular is a string with no
counterpart in any crop read. The certified `slide_015_final.json` labels include
`Output 1 / Output 2 / Output m` — which matches the parse, so the JSON and the parse
agree with each other but neither is confirmed by the crop reads. Because the JSON and
the parse contradict the crops, this is booked **advisory**, not as a banked defect.

**F6 — MINOR: hallucinated-content — spurious truncated equation tail (confidence: high)**
The parse ends with `E = 1/2 ∑ x (tj −Oj)2 X X` — a partial second copy of the error
equation. The frame shows the error equation once (`E = 1/2 Σ_j (t_j − O_j)^2`). This
trailing fragment is a `hallucinated-content` string fragment. Real but low-impact.

**F7 — MINOR: reading-order-inversion — the class labels are interleaved with the error column (confidence: medium)**
The parse emits `Class 1 / Class 2 / Error Error Error / ... / Class m / Class m` — the
error column text is spliced into the middle of the class-label stack. All three crop
reads emit `Class 1 / Class 2 / Class m` contiguously with `Error Error Error` grouped
separately. The parse's ordering is against the visual order -> `reading-order-inversion`.

## REAL / HALLUCINATED / DEBATABLE list

- header `Neural Network Model` / `(Weights of hidden layer AFFECT Calculated Error)` —
  **REAL** (parse + all three crops + certified JSON agree verbatim).
- badge `15` — **REAL** (all reads; measured badge ink x 856-894, y 54-88).
- `Net_j = Σ_i (w_ji O_i)` — equation is **REAL**; the parse's `wjj` is **HALLUCINATED**
  at the character level (F2), corrected by crop02/crop03.
- `W_ji` arrow label — **REAL**; the parse's `Wij` is **HALLUCINATED** (inverted index,
  F1).
- `E = 1/2 Σ_j (t_j − O_j)^2` — **REAL** (all reads).
- `O_j = f(Net_j) = 1/(1+e^(−Net_j))` — **REAL, absent from the parse** (F3).
- `Error Error Error` — **REAL** (parse + all crops; measured error column inside the
  diagram body x 431-811 y 138-364).
- `Class 1 / Class 2 / Class m` — **REAL**, once each (crops). The parse's SECOND
  `Class m` is a duplicate -> **HALLUCINATED** copy, but the JSON's `Output 1/2/m`
  labels keep F5 in advisory territory.
- `Output 2`, `W #`, `W` — **DEBATABLE** (parse + JSON vs all three crops; advisory).
- trailing `E = 1/2 ∑ x (tj −Oj)2 X X` — **HALLUCINATED** fragment (F6).
- `Σ J ∞ Σ` infinity glyphs — **DEBATABLE**: crops read `Σ S S Σ S`; the frame's Σ has
  sub/superscript limits, not an infinity. No read's glyph is trustworthy here.
- `1 Node Bias i k` and the layer-caption line — **REAL** (parse + crops + JSON).

## Uncertainties

- The three crop reads disagree on one arrow label: crop01 reads `Wji Wki`, crop02 reads
  `W ji W kj`, crop03 reads `W ji` and `W ki`. The `w_ji` / `w_ki` vs `w_ji` / `w_kj`
  split is unresolved; the important half (`w_ji`) is unanimous.
- No vision read exists for this slide (HTTP 400 upstream rejection, preserved). The
  cascade is the only second read; per the corroboration law a crop IS a different-form
  read, so the corroborated labels stand, but the label-set disagreements above stay
  advisory for that reason.

## Verdict

`PARSE ADJUDICATION: DEGRADED — header and most labels corroborated, but the parse
inverts the deck's central weight index (Wij for w_ji), mangles the network equation as
wjj, drops the sigmoid equation entirely, adds a spurious duplicated error equation and
unverified Output/W fragments, and carries no structural boxes for the diagram.`

## Addendum (vision-route status, banked after the file above was written)

Three vision attempts against `unique_slides/slide_015.jpg` failed at transport with
`HTTP 400 upstream_rejected_request` (candidate ids nva…B2PK, nva…1OGa, nva…BJnX in
`analysis/parse/adjudication/slide_015.vision.txt`). Per the corroboration law a failed
transport is never a verdict, so slide 015's corroborated labels above rest entirely on
the crop cascade — which is a different-form read and therefore valid corroboration.

A fourth attempt is banked against a DIFFERENT input form
(`analysis/parse/adjudication/slide_015.vision_crop.txt`, the cascade's own crop03 PNG
passed to the vision route). Its answer is quoted in the file below once banked; it is
advisory only, since the crop read already corroborates the labels.

`analysis/parse/adjudication/slide_015.vision_crop.txt` — the fourth attempt, reading the
cascade's crop03 PNG (a different input form). Winner (attempt 2, after a GarbageError
prompt-echo abort on attempt 1): "So answer w_ji." — reasoning quoted the equation as
`Net_j = \sum_i ( w_{j i} O_i )`. This corroborates F1/F2: the bottom-left equation's
weight subscript is **w_ji** (destination j, source i), the frame's convention. Slide 015
therefore has BOTH corroboration classes for its central claim: a crop parse read
(crop02/crop03: `Netj = ∑ (wji Oi)`) and a vision read over a crop image (w_ji).

Final evidence bank for 015: `analysis/parse/cascade/slide_015/` — composed file with
4 positioned elements (full + 3 crops), 6 parse calls, 0 failed calls, not degraded,
with per-crop provenance (call dirs full/ / crop01 / crop02 / crop03).
