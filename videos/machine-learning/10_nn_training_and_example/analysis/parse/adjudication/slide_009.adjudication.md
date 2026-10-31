# Parse adjudication — slide 009 (10_nn_training_and_example)

SOURCE IMAGE: `unique_slides/slide_009.jpg` (960x540 px, md5 cc1fc954c33f8a5aaa7dfa608fd65e5c)
PARSE TRANSCRIPT: `analysis/parse/slide_009.parse.md` + `analysis/parse/slide_009.parse.json`
ENVELOPE: finish_reason=`stop`, usage.output_tokens=189, content_len=392 -> **valid call**
SECOND READ TYPE: **corroborated** — (a) script-12 vision analysis `analysis/slide_009_final.json` (verdict PASS_WITH_FIXES, independent vision model; question asked: full layout/regions/labels/equations extraction); (b) image-analysis cross-check `analysis/parse/adjudication/vision/slide_009.vision.txt` (independent vision read; question asked: transcribe every text item region by region, reproduce fractions/sums/superscripts as seen).
MEASUREMENT: `analysis/parse/adjudication/measurements/slide_009.pil.txt`, glyph census `glyphs.py`.

## Severity-ranked findings

### MAJOR — `hallucinated-content` — the sigmoid equation is mangled (confidence: high, corroborated)
Parse line: `For **Sigmoid** Activation Oj=f (Netj)= 1 −Netj 1+e Netj = ∑ i (wji Oi)`.
Two things are wrong. (1) `1 −Netj 1+e` is not a denominator form: both vision reads give `O_j = f(Net_j) = 1/(1+e^{-Net_j})`,
i.e. a fraction whose denominator is `1 + e^{-Net_j}` — the parse emits the minus sign and the `e` on the same linear run
with no grouping. (2) `Netj = ∑ i (wji Oi)` is a **separate equation** that has been fused onto the Sigmoid line.
-> The parse fuses three distinct equations (error function, sigmoid, net input) into one line and garbles the
sigmoid denominator. REAL.

### MAJOR — `hallucinated-content` — `∂Νii = Oi` (confidence: high, corroborated)
Parse line: `∂E ∂E = −(tj−Oj) ∂Nij ∂Νii = Oi`. `Ν` is a Greek capital Nu with no counterpart in any read; both vision
reads give `∂Net_j/∂W_ji = O_i`. The glyph is invented at the symbol position.
-> REAL (a symbol substituted for the `N`/`W_ji` base).

### MAJOR — `dropped-region` — output labels `Output 2`, `Output m` and the three `Error Class n` labels are missing (confidence: high, corroborated)
Parse contains `Class 1` only, and no `Output 2` / `Output m`. Script-12 read lists `Output 1`, `Output 2`, `Output m`,
`Error`, `Error Class 1`, `Error Class 2`, `Error Class m`, `Net1/Net2/Net m`, `O1/O2/Om`.
Local corroboration (measured, not read): the far-right column x=790..935 y=60..350 holds **9 glyph-scale marks in
4 distinct lines** (y=68, 227-230, 275, 336-340) and the strip x=700..790 y=60..350 holds **13 glyph-scale marks in 5
lines** — i.e. more label ink than a single `Class 1` line can account for.
-> REAL.

### MAJOR — `reading-order-inversion` (confidence: high, corroborated)
The parse emits the far-right `Error Error Error 9` / `Class 1` line *before* the equations that sit to the left of them,
and then fuses the error function, sigmoid and net-input equations onto a single line. The measured layout is:
title + update equations at top-left (x=78..313, y=73..153), the boxed block y=220..255, three boxed derivatives at
y=312..365, and the chain-rule box at y=372..397 — a left-to-right, top-to-bottom reading order the parse does not follow.
REAL.

### MINOR — `math-normalization-loss` — `E = 1 2 ∑ j (tj −Oj)2` inline (confidence: high, corroborated)
The `1/2` is inline and the sum index is dropped to a flat run; `W ji Updated = W ji old - η ∂E ∂W ji` likewise flattens a
stacked fraction. Both vision reads keep the numerator/denominator structure. REAL (format only; nothing invented).

### MINOR — `dropped-region` — bottom-right yellow derivative-summary box (confidence: medium, corroborated)
The script-12 read reports a light-yellow box at bottom-right (70-95% width, 55-85% height) repeating the three
partial derivatives. The parse's content has no boxed summary line; measured ink in the lower-right quadrant
(rows y=319..397, cols x=240..480) exists but the parse covers it only through the unsegmented equation run.
-> DEBATABLE (the box may be inside the parse's fused line); advisory.

### MINOR — `hallucinated-content` — subscript swap `Δjj` vs `Δ_ji` (confidence: medium, corroborated)
Parse: `Where Δjj = −η∂E ∂W ji`. Both vision reads give `Δ_ji`. The `j` subscript is a misread of `i`.
-> REAL as a defect, MINOR: slide 010's parse of the same formula reads `Where Δ ji = −η ∂ E`.

## Explicit classification list

- REAL (high, corroborated): sigmoid denominator garbled + net-input equation fused onto the sigmoid line — `hallucinated-content`.
- REAL (high, corroborated): `∂Νii` Greek-Nu symbol invented — `hallucinated-content`.
- REAL (high, corroborated): `Output 2`, `Output m`, `Error Class 1/2/m` dropped — `dropped-region`.
- REAL (high, corroborated): right-hand error/class labels sequenced before the left-hand equations — `reading-order-inversion`.
- REAL (high, corroborated): stacked fractions flattened to inline — `math-normalization-loss`.
- REAL (medium, corroborated): `Δjj` subscript misread for `Δ_ji`.
- DEBATABLE (advisory): coverage of the bottom-right yellow summary box.
- DEBATABLE (advisory): whether `Error Error Error` is one vertical bar read three times or three bars — local census shows 3 distinct error-bar glyph lines, consistent with 3.
- HALLUCINATED: none beyond the `Ν` symbol and the fused sigmoid line.

## Uncertainty markers

- `[?]` The exact count of net/output nodes (`Net1/Net2/Net m` vs `Net_i/O_i` per column) — the parse drops the index to `Neti`, so index letters are unresolved.
- `[?]` Whether the bottom-right yellow box duplicates the three derivatives or holds a fourth variant.

PARSE ADJUDICATION: DEGRADED — the parse is `finish=stop` and carries the slide's core equations, but it garbles the sigmoid denominator, invents a `Ν` symbol, drops the output/error-class label column, and inverts the reading order.
