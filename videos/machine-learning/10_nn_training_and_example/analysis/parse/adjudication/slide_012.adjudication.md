# Parse adjudication — slide 012 (10_nn_training_and_example)

SOURCE IMAGE: `unique_slides/slide_012.jpg` (960x540 px, md5 d91d41d2951c9aac940416c2e3cd8682)
PARSE TRANSCRIPT: `analysis/parse/slide_012.parse.md` + `analysis/parse/slide_012.parse.json`
ENVELOPE: finish_reason=`stop`, usage.output_tokens=134, content_len=425 -> **valid call**
SECOND READ TYPE: **corroborated** — (a) re-analysis vision read `analysis/reanalysis/slide_012_final.json` (verdict PASS_WITH_FIXES); (b) image-analysis cross-check `analysis/parse/adjudication/vision/slide_012.vision.txt` (question asked: transcribe every text item region by region and note repeated identical labels). The two reads **disagree on subscript forms** (`O_i` vs `O_1/O_2/O_3`), so nothing resting on that token is banked as fact.
MEASUREMENT: `analysis/parse/adjudication/measurements/slide_012.pil.txt`, glyph census `glyphs.py`.

## Geometry verification — the parse's boxes are the most accurate in this scope

Parse token boxes vs measured ink (960x540; x*W, y*H):
| Parse token | resolved px | measured ink | delta |
|---|---|---|---|
| heading `<x_0.082><y_0.1195>`..`<x_0.29><y_0.1688>` | (79,65)-(278,91) | x=84..275, y=69..87 | <=6 px |
| `<class_Picture>` box `<x_0.1641><y_0.1922>`..`<x_0.8486><y_0.7305>` | (158,104)-(815,394) | x=150..828, y=100..399 | <=8 px |
| badge `12` `<x_0.9023><y_0.1164>`..`<x_0.9229><y_0.1516>` | (866,63)-(886,82) | top-right badge ring | on target |
-> No `coordinate-misalignment` for any box the parse emitted.

## Severity-ranked findings

### MAJOR — `hallucinated-content` — `Eror` for `Error` (confidence: high, corroborated by both reads)
The picture block lists `Eror` as the error-bar label; the cross-check reads the same vertical text as `Error` inside the
tall rectangle at ~(520,165), and the reanalysis read lists `Error`. A dropped letter in a verbatim-text lane. REAL.

### MINOR — `dropped-region` — label multiplicities under-counted (confidence: high, corroborated)
Cross-check inventory: `w_i j` x3, `delta_j` x3, `O_j` x3, `t_1/t_2/t_3` x3, `Error` x1. Parse inventory: `w ji` x1 +
`Wji` x2 = 3 (ok), `delta_j`: `δj` x1 + `Dj` x1 = 2 (short 1), `O_j`: `Oj` x1 only (short 2), `Error`: `Eror` x1 (ok).
Local census of the picture-box interior: **56 glyph-scale components across 12 glyph lines** (y=121..348).
-> `O_j` and `delta_j` are under-read. REAL, MINOR.

### MINOR — `math-normalization-loss` — subscripts flattened inline (confidence: high, corroborated)
`Δji = η Oi δj`, `Where: δj = Oj(1-Oj) (tj-Oj)` keep the content right but flatten every subscript to adjacency.
The cross-check confirms the original is itself INLINE with no stacked fractions, so no fraction loss applies — only
subscript positioning is flattened. REAL, MINOR.

### ADVISORY (not banked as a defect) — the parse's `11` token (confidence: low)
Neither vision read lists any `11` on this slide: the cross-check enumerates the full label set (`O_1/O_2/O_3`,
`w_i j` x3, `delta_j` x3, `O_j` x3, `Error`, `t_1/t_2/t_3`, the panel band, the two bottom lines, badge `12`) and contains
no `11`. But my local census finds **exactly two glyph-scale marks** at (x=450..500, y=288) and (x=450..500, y=299) —
i.e. *inside the panel equation band* the cross-check places at y 285-320 — so ink exists there and is consistent with a
mis-read digit of the band's `O_j(1-O_j)` characters rather than a bare hallucination. Advisory only.

### ADVISORY — `Bj` (confidence: low)
No counterpart in either read. May be a genuine bias-labelled node or a mis-read of `O_j`/`delta_j`.

## RETRACTED finding (recorded for the evidence trail)

An earlier draft of this file classified a MAJOR `class-token-mismatch`: that the picture block's final lines
(`Δji = η Oi`, `Oj (1-Oj) (tj-Oj)`) were equation text mis-assigned into `<class_Picture>`, on the inference that the
last lines of a y-ordered block must map to the bottom-of-slide formula lines at y=421..449. **The cross-check refutes
that inference**: the panel (x 148..763, y 90..350) itself contains an equation band at y 285-320 reading
`Delta_ji = eta O_i O_j(1-O_j) (t_j - O_j)`, which is *inside* the parse's picture box (y 104..394) — so those lines are
correctly placed. The separate `<class_Formula>` / `<class_Text>` lines correctly correspond to the bottom annotation
box's `Delta_ji = eta O_i delta_j` / `Where: delta_j = O_j(1-O_j) (t_j - O_j)`. No defect.

## Explicit classification list

- REAL (high, corroborated): `Eror` for `Error` — `hallucinated-content`, MAJOR.
- REAL (high, corroborated): `O_j` (1 of 3) and `delta_j` (2 of 3) under-read — `dropped-region`, MINOR.
- REAL (high, corroborated): subscripts flattened inline — `math-normalization-loss`, MINOR.
- POSITIVE (high, corroborated): all emitted coordinate/class boxes resolve onto their named content.
- DEBATABLE: the parse's `Oi` x3 — reanalysis reads `O_i`, cross-check reads `O_1`/`O_2`/`O_3`; two reads contradict, so nothing is banked either way.
- DEBATABLE: `Dj` — a `delta_j` with delta mis-read as `D`, or a distinct `D`-labelled node.
- DEBATABLE (advisory): `11`, `Bj`.
- HALLUCINATED: `Eror` (dropped letter).

## Uncertainty markers

- `[?]` The subscript identity of the three input-node labels (`O_i` vs `O_1/O_2/O_3`) — irreconcilable between the two reads.
- `[?]` Whether `Dj` is a fourth `delta_j` or a distinct label.

PARSE ADJUDICATION: DEGRADED — geometry and reading order are sound (this is the best-formed parse in the scope), but the parse drops the `r` from `Error`, under-reads two label families, and emits two unverified tokens (`11`, `Bj`).
