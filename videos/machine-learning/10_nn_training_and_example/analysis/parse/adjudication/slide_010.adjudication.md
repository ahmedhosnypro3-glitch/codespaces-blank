# Parse adjudication — slide 010 (10_nn_training_and_example)

SOURCE IMAGE: `unique_slides/slide_010.jpg` (960x540 px, md5 12aad673bb8ca120db96904549c6c286)
PARSE TRANSCRIPT: `analysis/parse/slide_010.parse.md` + `analysis/parse/slide_010.parse.json`
ENVELOPE: finish_reason=`stop`, usage.output_tokens=289, content_len=594 -> **valid call** (289 of an unused ceiling: no truncation)
SECOND READ TYPE: **corroborated** — (a) script-12 vision analysis `analysis/slide_010_final.json` (verdict PASS_WITH_FIXES, independent vision model; question asked: full layout/regions/labels extraction); (b) image-analysis cross-check `analysis/parse/adjudication/vision/slide_010.vision.txt` (independent vision read; question asked: transcribe every text item region by region, reproduce fractions/sums/superscripts as seen).
MEASUREMENT: `analysis/parse/adjudication/measurements/slide_010.pil.txt`, glyph census `glyphs.py`.

## Severity-ranked findings

### MAJOR — `dropped-region` — the entire top-right network diagram and its label column are unparsed (confidence: high, corroborated)
The parse's content is **title + equations only**: no `Input Bias`, no `Output 1/2/m`, no `Error Class 1/2/m`,
no node/weight labels. Its only two coordinate tokens are the title anchor (0.0371,0.0781) and one `<class_Picture>`
at (0.9463,0.957); no box is asserted over the diagram.
Measured ink proves the region is populated: the cream diagram box occupies x=320..790, y=45..205 (grid rows 2-9,
cols 8-19 at 48-100% density) and the far-right label column carries glyph-scale ink.
Script-12 read lists `Input Bias`, `Output 1/2/m`, `Error Class 1/2/m` as on-slide labels.
-> A whole visible region with labels, dropped entirely. REAL.

### MAJOR — `hallucinated-content` — the sigmoid equation is truncated mid-denominator (confidence: high, corroborated)
Parse line: `For **Sigmoid** Activation Oj=f ( Netj)= 1 −Netj i Netj = ∑i ( wji Oi)`.
The denominator ends in a stray `1 −Netj i` — the `e` and the closing group are gone and a bare `i` is left behind.
Both vision reads give `O_j = f(Net_j) = 1/(1+e^{-Net_j})`. Slide 009's parse of the same formula reads `1+e`, so the
`i` here is not a consistent glyph reading of the frame. -> REAL.

### MAJOR — `hallucinated-content` — `Oj(i−Oj)` (confidence: high, corroborated)
Parse: `∂ Oj ∂ Netj = Oj(i−Oj)`. The `1` in `O_j(1-O_j)` is read as a letter `i`. Both vision reads give `O_j(1-O_j)`.
The `i`/`1` confusion is a *glyph* read, not a formatting loss: it changes the expression's content. REAL.

### MAJOR — `hallucinated-content` — `∂ Wii = Oi` (confidence: high, corroborated)
Parse: `∂ Wii = Oi`. Should be `∂Net_j / ∂W_ji = O_i`. The parse emits `∂ Wii`, a symbol run with no counterpart in
either second read. REAL.

### MINOR — `reading-order-inversion` (confidence: high, corroborated)
The parse's line `E = 1 2 ∑ j ( tj −Oj)2 For **Sigmoid** Activation ...` fuses the error-function, sigmoid and
net-input equations onto one line, and the chain-rule lines are interleaved with the δ rules
(`∂ E ∂ E ∂ Oj = −(tj−Oj)` appears twice, `= = δj * Oi`). Measured layout: update equations y=124..153, error block
y=220..255, three boxed derivatives y=312..365, chain box y=366..402, bottom rule y=479..495 — a clean stack the
parse's ordering does not follow. REAL.

### MINOR — `math-normalization-loss` (confidence: high, corroborated)
`E = 1 2 ∑ j ( tj −Oj)2` and `W ji old - η ∂ EW ji` flatten stacked fractions; `**Sigmoid**` keeps literal markdown
bold markers in the output stream. REAL (format only).

### MINOR — `dropped-region` — badge numeral `10` absent (confidence: high, corroborated)
Parse has no `10`; both second reads place a yellow badge with `10` at top-right, and every sibling slide in this
range carries its badge numeral (007->`7`, 009->`9`, 011->`11`, 012->`12`). REAL.

## Explicit classification list

- REAL (high, corroborated): whole top-right diagram label column dropped — `dropped-region`, MAJOR.
- REAL (high, corroborated): `Input Bias`, `Output 1/2/m`, `Error Class 1/2/m` dropped — `dropped-region`, MAJOR.
- REAL (high, corroborated): badge `10` dropped — `dropped-region`, MINOR.
- REAL (high, corroborated): sigmoid denominator truncated to `1 −Netj i` — `hallucinated-content`, MAJOR.
- REAL (high, corroborated): `Oj(i−Oj)` letter-for-digit substitution — `hallucinated-content`, MAJOR.
- REAL (high, corroborated): `∂ Wii = Oi` garbled symbol run — `hallucinated-content`, MAJOR.
- REAL (high, corroborated): equation lines fused and the chain rule duplicated — `reading-order-inversion`, MINOR.
- REAL (high, corroborated): stacked fractions flattened inline; markdown `**` markers leaked — `math-normalization-loss`, MINOR.
- HALLUCINATED: none beyond the `i`/`∂ Wii` substitutions above.

## Uncertainty markers

- `[?]` Whether the far-right column holds `Error Class 1/2/m` as a stack or a single `Error` bar plus separate class labels — not resolved locally.
- `[?]` Whether the bottom-right yellow box duplicates the three derivatives or holds a fourth variant.

PARSE ADJUDICATION: DEGRADED — the parse recovered the equation chain correctly at the content level (289 tokens, `finish=stop`), but it drops the whole diagram label column and the badge, and corrupts the sigmoid denominator, `O_j(1-O_j)` and `∂Net_j/∂W_ji`.
