# Slide 022 — PARSE ADJUDICATION

- **Slide:** 022
- **Source image:** `unique_slides/slide_022.jpg` (960x540 RGB, measured)
- **Parse transcript:** `analysis/parse/slide_022.parse.md` / `.parse.json`
  - `finish_reason` = `stop`, content non-empty, `usage.output_tokens` = **15**
- **Second read (corroboration):** cascade re-parse, `analysis/parse/cascade/slide_022/`
  (full + 2 crops, `composed/slide_022_composed.md`, `manifest.json`) — a
  different input form (upscaled regional crop), so it is a genuine corroborating read.
- **Cascade resolution:** recovered the complete algorithm body `[1]`-`[6]`.

## The OPEN ITEM (DB task 91) — RESOLVED

The original full-frame parse emitted exactly one element: the title plus a
single closing `<class_Picture>`. It returned **15 output tokens** — the
sparsest read in this deck's 34-slide parse bank. The cascade crop01 (frame
box `[38.4, 42.6, 881.3, 492.8]` px, scale 1.7479) returned **459 tokens** of
algorithm text. The originally-missed region is the whole algorithm body box.

- **UNCOVERED by the original parse** (frame px):
  - Algorithm box x 38–881, y 253–493: steps `[1]`–`[6]` + `Remember:` line
  - Neural-network diagram: inside the same box, ~y 200–250, x 40–880
- **Covered by the original parse:** only the title band y 43–60, x 38–881
  (token `x_0.04 y_0.0789` resolves to `(38, 43)` — correct) and the badge `22`.

## Findings (severity-ranked)

**F1 — BLOCKER: `dropped-region` — the entire algorithm body (confidence: high)**
The full-frame read emitted one `<class_Picture>` covering 97.8% of the slide
(`x_0.04 y_0.0789` → `x_0.958 y_0.9914`) and no content. Cascade crop01 on the
same frame box returned steps `[1]`–`[6]` verbatim plus the `Remember:` line.
This is the known OPEN ITEM (task 91) — now with the recoverable evidence banked.
Evidence: `analysis/parse/slide_022.parse.md` vs `analysis/parse/cascade/slide_022/
crops/slide_022.crop01__picture.parse.md`, `manifest.json` stats (3 parse calls,
9 elements).

**F2 — MAJOR: `math-normalization-loss` inside the recovered steps [4]/[5] (confidence: high)**
`Δji = η Oi Oj(1−Oj) (tj−Oj)` — the subscripts flatten to `ji` only when the
parse chooses to render them at all; the step text `Calculate Δji, Wji` loses
the subscript relationship. Both cascade and vision read render `Δ_ji` with an
explicit subscript, so the flattening is a parse artifact, not the slide's.
Evidence: `crops/slide_022.crop01__picture.parse.md` lines for steps `[4]`,`[5]`.

**F3 — MINOR: `class-token-mismatch` on the badge (confidence: medium)**
The title token closes with `<class_Picture>` — the frame-covering wrapper.
The badge `22` sits at `x_0.958 y_0.9914` (bottom-right by token position) but
PIL band scan puts the badge at y 53–59, x 878–908 (top-right). The parse's
`class_Picture` is the structural convention, not a content assertion, so this
is a note. Evidence: band-scan band `y53-59 cols 878-908`.

## REAL / HALLUCINATED / DEBATABLE

- Title `Back Propagation Training Algorithm` — **REAL** (corroborated; vision
  read Q1 and cascade full read agree verbatim).
- Badge `22` — **REAL** (PIL: yellow ring x 861–891, y 58–84; token top-right).
- Steps `[1]`–`[6]` + `Remember:` — **REAL, MISSING** from the original parse
  (recovered by cascade crop01, corroborated by vision read Q2/Q4).
- `class_Picture` covering the frame — **DEBATABLE** (real structural region,
  but it swallowed all algorithm content).
- Any `w_ij` subscript — **none present**; all reads give `w_ji`.

## Uncertainties

- The badge's exact ink position differs between the PIL ring measurement
  (x 861–891) and the parse's normalized token (x 878–908). Both reads agree it
  is top-right; the parse's token is inside the ring, so this is not a defect.
- Whether the diagram contains node labels below the 15–22 px legibility floor
  (`glyph-floor-blindness`) — neither read transcribed any node label, so the
  region is treated as label-free.

## Verdict

`PARSE ADJUDICATION: DEGRADED — original full-frame read captured 15 tokens
(title only); full [1]-[6] algorithm body recovered by the banked crop cascade;
verbatim text is REAL and correct but the base transcript is unusable standalone.`
