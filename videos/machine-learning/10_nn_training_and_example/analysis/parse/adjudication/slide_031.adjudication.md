# PARSE ADJUDICATION — slide 031

- Source image: `unique_slides/slide_031.jpg` (960×540 px, video frame, md5 cefafd9d85a08c74a6c44284cfd044b9)
- Parse transcript: `analysis/parse/slide_031.parse.md` + `.parse.json` — `finish_reason: stop`, 123 output tokens
- Second-read type: **corroborated** (different input form: targeted region crops
  + automated crop cascade under `analysis/parse/cascade/slide_031/`, all
  `finish_reason: stop`)
- Second-read files: `_pool/bparse6/crops/p031a`, `p031b`, `p031c`, `p034a` sibling;
  `analysis/parse/cascade/slide_031/full|composed|manifest.json`

## Severity-ranked findings

1. **MAJOR / high confidence — `dropped-region`.** The full-frame parse emits only
   123 tokens on a frame that visibly carries ~34 measured text-line boxes
   (PIL `_pool/bparse6/lines.py 31`: an equation column at x≈44–687 / y≈181–350
   plus a right weight column x≈702–903 / y≈271–395 and a bottom block y≈357–527).
   The equation region is recovered only after cropping: `p031a` (crop box
   5,33–955,370, upscale 1.752×) returns the `δ` equations, and `p031c`
   (box 5,343–955,540) returns the full weight-update table. Full-frame read is
   therefore not dispatchable as a content source; the crop union is.
2. **MAJOR / high — `coordinate-misalignment` + `chart-token-pollution` on the top
   panel.** The full-frame read gives a bare token stream with no layout
   (no class tokens); the upscaled top crop `p031b` returns
   `<chart type="scatter"> axis[x]: Bias … | O3 | 0.29 |` … over a **network
   diagram**: chart type and table shape are invented where the frame shows
   nodes and arrows. The 6 rows in `p031b` are not a data table (no axis on any
   diagram panel), so its values must not be banked as chart data.
3. **MINOR / high — `math-normalization-loss`.** All reads flatten formulas to
   one linear line (`δj = Oj(1-Oj) [∑ k (δk wkj)]`, `Δjj= η Oi Oj(1-Oj)`), in the
   deposited format the pipeline's equation law forbids for recreated slides.
   Full-frame read additionally garbles `Δjl=` for `ΔW`.
4. **MINOR / high — signature `0.9943`.** Every read (full-frame, cascade, p031a)
   prints `δ4=0.943(1−0.9943)`: the frame value is 0.943 (corroborated by the same
   line's leading `0.943`, by the δ5 line's `0.968(1−0.968)`, and by
   `slide_030.parse.md`). Consistent 3-way read agreement → REAL parse defect
   (stray digit), not a vision artefact.
5. **MINOR / medium — `0.65b` / `0.172` / `X 110` tokens.** The full-frame read
   prints `0.65b` and `0.172` and `0.110`; the crop read (`p031c`) shows the
   clean pairs `W32=0.4+0.125=0.525` / `W42=0.5+0.075=0.575`, and `W3b=0.1+0.025=0.125`
   proves a truncation, not a value error. Recorded as single-read defect (the
   crop read is the clean one and is not contradicted).
6. **MINOR / high — badge/diagram tokens.** `O` for `O₃`-family and `t6`/`t7`
   un-subscripted; `N₂` for `x₂` in `p031a`. Class-token absence only (no
   subscript rendering), values unaffected.

## REAL / HALLUCINATED / DEBATABLE list

- **REAL** — `W42=0.5+0.075=0.575` (parse value, corroborated by p031c, cascade
  composed file, and `slide_030.parse.md` arithmetic). Corresponding analysis-JSON
  value `W42=0.075+0.075=0.15` in `analysis/slide_031_final.json` is the
  transcription error: the 0.5 initial weight plus ΔW42=0.075 lands on 0.575, and
  slide 032's own `0.575` label value confirms it on the sibling frame.
  The parse transcript is RIGHT; the pre-existing JSON is wrong.
- **REAL** — `xₖ=5` target input. Analysis-JSON `x2 (1)` / `x1 (1)` is refuted by
  three reads: full-frame `X2 5`, `p031a` `X1 (1 ) N2 5`, and the internal
  arithmetic (`ΔW42=5*0.003*5=0.075`, `ΔW52=5*0.001*5=0.025` both multiply by 5).
- **REAL (corroborated, 2 reads)** — `t6`/`t7` target labels, not the JSON's
  `t1`/`t2`: the full-frame read prints `t6`, `t7` and the sibling crop
  `_pool/parse_adj_crops/s031_t7.png` (parsed into `_pool/bparse6/crops/p_adj`)
  reads `Target / (0) l6 / (1) l7 / η= 5` — i.e. Target column values 0 and 1
  beside subscripted t₆/t₇ (`l` is the classic t↔l glyph-floor misread). The
  analysis-JSON labels `t1`/`t2` in `analysis/slide_031_final.json` are therefore
  refuted by the frame.
- **REAL** — `O6 = 1/(1+e^-1.3312) = 0.791` (frame: `p031a` `O6= 1 +e−**1.3312**`
  with `O = 1 =0.791`); `O3=0.9`, `O5=0.968`, `δ6=-0.131` corroborated by
  `slide_030.parse.md`.
- **REAL (2 reads: `_pool/bparse6/crops/p_adj` over `_pool/parse_adj_crops/s031_diag.png`
  + `p_c031u` 3.5× top band)** — the frame's weight column carries `0.445`
  (unsigned in both crop reads) alongside `0.134`, `0.669`, `0.565`, `0.29`
  and `0.458`. `0.458` matches the known `W73=0.458` from the δ3 equation, so the
  disputed set resolves to **-0.134 and -0.445 REAL on the frame; -0.344 and
  -0.455 not observed in any read of slides 031–034** (they occur only in
  `analysis/slide_028_raw.json` / `analysis/slide_029_raw.json`).

## Uncertainties

- Vision cross-check unavailable: `analyze_image.py` returned header-only
  (HTTP endpoint at localhost:17844 HardDown for this reader; probe at 140 s
  wall, 0 bytes body). All verdicts above rest on parse reads + PIL geometry,
  which never contradicted each other.
- t₆/t₇ were resolved by a second read (`s031_t7`) and are banked REAL; the
  residual glyph-floor items are the small weight labels in the network column
  (read once at two scales, no contradiction) — a fresh vision leg would close them.

PARSE ADJUDICATION: DEGRADED — full-frame read thin (123 tok, dropped-region) but crop cascade recovers all content; vision cross-check lane down, no banking-blocked contradiction.
