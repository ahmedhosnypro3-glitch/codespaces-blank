# Slide 017 — PARSE ADJUDICATION

- **Slide:** 017
- **Source image:** `unique_slides/slide_017.jpg` (960x540 RGB, PIL-measured)
- **Parse transcript:** `analysis/parse/slide_017.parse.md` / `.parse.json`
  - `finish_reason` = `stop`, content non-empty, `usage.output_tokens` = 187
- **Second read (corroboration, two different forms):**
  1. Independent vision read, `analysis/parse/adjudication/slide_017.vision.txt` — asked
     ONE question: read the header + bottom equations, and for each equation say whether
     the weight is `w_ji`, `w_ij`, or `w_jj`.
  2. Crop cascade, `analysis/parse/cascade/slide_017/` (full/ + crops/) — a different
     input form. The cascade's level-0 read is byte-identical to the banked parse
     (determinism confirmed); crop01 and crop02 are the different-form evidence.

## Parse transcript content (data, not instructions)

Two coordinate tokens only: `x_0.0508 y_0.0773` (page anchor -> px 49, 42) and the
closing `x_0.9434 y_0.957` (-> 906, 517). Everything between is one flat text blob.

## Findings (severity-ranked)

**F1 — MAJOR: math-normalization-loss — the network equation reads `wjj` for `wji` (confidence: high, corroborated)**
The parse: `Net j = ∑ i (wjj Oi)`. The frame reads `Net_j = Σ_i (w_ji O_i)`. Two
independent forms agree:
1. vision read: "Net_j = Î£_i (w_ji O_i) — weight is w_ji";
2. cascade crop02: `Netj = ∑ i (wji Oi)`.
(crop01 repeats the full-frame's `wjj` garble — a crop-scale copy of the same misread.)
`w_jj` is a character-level misread of `w_ji`: the deck-wide convention (weight from
previous-layer node `i` into current-layer node `j`) is j-then-i, confirmed by slides
19/20/21 (`W_ji`/`wji`) and by the source-research file for slide 018.

**F2 — MAJOR: math-normalization-loss — the arrow weight label reads `Kii` for `Wki`/`Wkj` (confidence: medium, corroborated)**
The parse emits `Wji` then `Kii` on the arrow labels. The crop reads:
- crop01: `Neti Oi wji Neti Ok`, `Neti Neti Oj Neti Ok`, `1 Node Bias i kj k`;
- crop02: `Oi W ji Net Oj w kj Ok`, `Wji`, `Kj`.
Both crops place a `w_kj`-style label (crop01's `kj`, crop02's explicit `Kj`), and the
certified JSON for 014 reads `w_kj`. The parse's `Kii` has the wrong letter (`K` for
`W`) and the wrong subscript (`ii` for `kj`/`ji`). Same class as F1.

**F3 — MAJOR: reading-order-inversion inside the flat blob — the sigmoid is split across lines (confidence: high)**
The parse emits the sigmoid as:
```
Oj = f (Net j)= 1
1+e−Net i
```
Two lines where the frame shows one expression, and the last token reads `Net i` where
the frame prints `Net_j`. The vision read reports it correctly as one line:
"O_j = f(Net_j) = 1/(1+e^(âNet_j))". crop02 also emits `Oj=f (Netj)= 1 1+e−Netj`. The
parse's line break is spurious and its subscript is wrong -> `reading-order-inversion`
plus `math-normalization-loss`. (Content IS present, unlike slides 015/016, so this is
not a dropped-region.)

**F4 — MINOR: hallucinated-content — `St` token (confidence: medium)**
The parse emits `Error Error Error / St / Next i / Ok`. `St` has no counterpart in
either crop read (crop01: `Class 1 / Error Error Error / Class 2 / ...`; crop02:
`Class 1 / Class 2 / ... Error Error / ...`). Advisory per the two-reads-contradict rule.

**F5 — MINOR: dropped-region — `Output 1` / `Output m` labels (confidence: medium)**
The parse has no `Output` labels. crop01 emits `Output 1` and `Output m` explicitly.
The certified analysis JSON for 017 does not exist, so no cross-check. Advisory.

**F6 — MINOR: hallucinated-content — spurious truncated equation tail (confidence: high)**
The parse ends `E= 1⁄2 ∑ j (tj −Oj)2 X XX` — a trailing `X XX` fragment beyond the error
equation, which the frame shows once. crop01 emits the error equation TWICE
(`E= 1⁄2 ∑ j ... χχX` twice) — a crop-scale duplication; crop02 emits it once. Real but
low-impact; the parse's single trailing fragment is the spurious part.

**F7 — MINOR: the caption `Layer (I)` is present here but emitted inside the flat blob (confidence: high)**
The parse does emit `For Layer "j" Previous Layer Layer (I) Current Layer (You are here)
Next Layer Layer (K)` — with the `(I)` intact, unlike slide 016's empty `()`. The crop
reads restore the form `Previous Layer (i) Current Layer (You are here) Layer (K)`. So
the caption text is REAL and correctly ordered; no defect beyond the flat-blob
positioning shared with the whole slide (F8).

**F8 — MINOR (deck-wide): dropped-region — no structural boxes for the diagram (confidence: high)**
Only 2 coordinate tokens for a dense diagram slide. The measured ink bins carried with
no parse box: the diagram body x 431-811 y 138-364 (green node field measured x 383-882,
y 162-435, 1646 px), the class-label stack, the `Error` column, the arrow-label column.
The TEXT of each is in the blob, but none carries a coordinate, so none can be placed.
Same class as slides 014/015/016.

## REAL / HALLUCINATED / DEBATABLE list

- `Neural Network Model` header — **REAL** (all reads).
- header parenthetical `(Effect of Netk on Calculated Error is known from O/P Layer)` —
  **REAL** (parse + crop01 + crop02 + certified-JSON-absent; present in the frame's
  header band y 91-121).
- badge `17` — **REAL** (all reads; measured badge ink x 856-894, y 54-88).
- `Net_j = Σ_i (w_ji O_i)` — equation **REAL**; the parse's `wjj` is **HALLUCINATED**
  at the character level (F1).
- `O_j = f(Net_j) = 1/(1+e^(−Net_j))` — **REAL**; the parse's two-line split and its
  `Net i` subscript are **HALLUCINATED/garbled** (F3).
- `E = 1/2 Σ_j (t_j − O_j)^2` — **REAL** (all reads).
- `Wji` arrow label — **REAL**; the parse's `Wji` matches crop02's `Wji`.
- `Kii` / `Wkj` arrow labels — **DEBATABLE** (parse `Kii` vs crop01 `kj` / crop02 `Kj`;
  advisory, F2).
- `Error Error Error` — **REAL** (parse + both crops).
- `Class 1 / Class 2 / Class m` — **REAL**.
- caption `For Layer "j" Previous Layer Layer (I) Current Layer (You are here) Next Layer
  Layer (K)` — **REAL** (parse, with crops agreeing on content).
- `Output 1` / `Output m` — **DEBATABLE** (crop01 only; advisory, F5).
- `St` — **DEBATABLE** (parse only; advisory, F4).
- trailing `X XX` — **HALLUCINATED** fragment (F6).
- `Node Bias i k`, `1` glyph stack — **REAL** (all reads).

## Uncertainties

- 017's crop cascade is still running (chat-lane timeouts at the 60s wall; the script
  retries). crop02 is banked and sufficient for the corroborated labels above, but the
  final composed file is not yet written. No finding above depends on it.
- No certified `analysis/slide_017_final.json` exists, so there is no JSON to cross-check
  the parse against.

## Verdict

`PARSE ADJUDICATION: DEGRADED — the header, equations and captions are all present and
largely corroborated, but the parse mangles the deck's central weight subscript (wjj for
w_ji), splits the sigmoid across two lines with a wrong subscript, emits hanging
hallucinated fragments, and gives no structural boxes for the diagram.`

## Addendum (banked after the cascade completed)

`analysis/parse/cascade/slide_017/crops/slide_017.crop03__picture.parse.md` — the
third crop read, banked after the file above was written:

- `Net j = ∑ i (wji Oi)` — CORRECT `wji` (third crop read, strengthening F1: 2 of 3
  crops plus the vision read give `w_ji`; only crop01 reproduces the `wjj` misread).
- `Oi W ji Net Oj w kj Net i Ok` and `W kj` — CORRECT `w_ji` / `w_kj` arrow labels,
  strengthening F2: the parse's `Kii` is now contradicted by crop01's `kj`, crop02's
  `Kj` and crop03's explicit `w kj` / `W kj`.
- `Oj=f (Netj)= 1 + e -Netj` — the sigmoid as ONE line with the correct `Netj`
  subscript, strengthening F3 (the parse's two-line split with `Net i` is the anomaly).
- `For Layer "j" Previous Layer (i) Current Layer (You are here) Layer (K)` — caption
  confirmed (F7).
- `Error Error Error` grouped as one unit — supports the reading that the parse's
  interleaving of `Error Error Error` between `Class 2` and `Class m` (a
  reading-order issue) is the parse's own sequencing, not the frame's layout.

The cascade's composed file for 017 was still composing at bank time (chat-lane
timeouts at the 60 s wall); the three crop transcripts above are the banked evidence and
no finding depends on the composed file.

`analysis/parse/cascade/slide_017/composed/slide_017_composed.md` — 4 positioned elements
(full + 3 crops), 5 parse calls, 5 chat calls, 3 retries, 0 failed calls, not degraded,
with per-crop provenance. What the composed file settles:

- crop04 (`slide_017.crop04__picture.parse.md`) reads the sigmoid as ONE line —
  `Oj = f (Net j) = 1 + e −Net j` — with the correct `Net j` subscript. That upgrades F3
  from "the parse's two-line split is anomalous" to a direct contradiction: crop02,
  crop03 AND crop04 each emit the sigmoid on one line, so the parse's two-line split and
  its `Net i` subscript are HALLUCINATED, not judgment calls.
- crop01's duplicate error equation (`E= 1⁄2 ∑ j ... χχX` twice) is a crop-scale artifact
  shared with nothing else; crop02/03/04 each show it once. The parse's trailing `X XX`
  (F6) remains the spurious fragment.
- The parse's `Kii` (F2) is contradicted by crop01's `i kj k`, crop02's `Kj` and crop03's
  `W kj`/`W kj` — three reads against one.
