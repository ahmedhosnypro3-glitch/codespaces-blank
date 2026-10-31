# PARSE ADJUDICATION — slide 033

- Source image: `unique_slides/slide_033.jpg` (960×540 px, video frame)
- Parse transcript: `analysis/parse/slide_033.parse.md` + `.parse.json` — `finish_reason: stop`, 291 output tokens
- Second-read type: **corroborated** (different input form: 4 panel crops at two
  scales — 2.0× and 3.0× — all `finish_reason: stop`)
- Second-read files: `_pool/bparse6/crops/p_c033a` (top 2×), `p_c033b` (bottom 2×),
  `p_c033c` (top 3×)
- JSON context: `analysis/slides_final.json` is `[]`; `analysis/slide_033_final.json`
  exists and independently describes the same two panels
  ("Header 'Initialized weights'" top; "after iteration # 10" bottom).

## Severity-ranked findings

1. **MAJOR / high — `dropped-region` (top panel title).** The top block carries no
   title. Both crop reads return `title: Initialized weights`
   (`p_c033a` box 66,51–859,301 at 2×; `p_c033c` box 100,60–830,260 at 3×),
   corroborated by `analysis/slide_033_final.json`'s own region description.
2. **MAJOR / high — panel content cross-contamination (`reading-order-inversion`).**
   The boxes are right — top block `<x_0.1016><y_0.1656>`→`<x_0.8574><y_0.5242>`
   (x 98–823, y 89–283) and bottom block `<x_0.1025><y_0.6109>`→`<x_0.8564><y_0.9734>`
   (x 98–822, y 330–526) match the measured rulers y≈89/260–285 and
   y≈330/502–525 (`_pool/bparse6/lines.py 33`) — but the rows are cross-panel:
   - Parse top block: `Input 0.155 | O3 0.215 | Output 0.675 | Target 0.835 |
     O4 0.93 | O5 0.575 | O4 -0.93 | O5 0.943 | O5 1.05 | Bias 0.105`.
   - Frame top panel (2 corroborating reads): `Input 0.1 | O3 0.3 | O4 0.4 |
     O5 0.5 | O5 0.5 | Output 0.791 | Target t₆`.
   - Parse bottom block: `X1 0.155 | X2 0.305 | O3 0.675 | O4 0.835 | O5 0.93 |
     O7 0.943 | O7 0.155 | Bias 0.115 | Bias 0.625 | O5 1.05 | O5 -1.2 | T 0.77`.
   - Frame bottom panel (`p_c033b`, 2×): `Input 0.155 | O3 0.215 | O4 0.675 |
     O5 0.575 | O5 -0.856 0.943 | O5 -1.2 0.93 | O6 0.943 | O7 1.05 | O7 0.77`.
   The two blocks agree on none of the top panel's actual values, and each borrows
   the other's numbers. 0.155/0.215/0.675/0.575/0.943/0.93/1.05/0.77 are bottom-panel
   values (all confirmed by `p_c033b`); 0.1/0.3/0.4/0.5/0.791 are top-panel values
   absent from both parse blocks.
3. **MAJOR / high — `class-token-mismatch` + `chart-token-pollution`.** Both panels
   are printed network diagrams with the same measured geometry as slide 032
   (x 101–823, y 138–254 / y 343–496). The parse wraps them in
   `<chart type="scatter">` (top) and `<chart type="lollipop">` (bottom) with
   invented metadata `axis[x]: Bias`, `bind: value ; ; y` / `bind: value ; ; x`.
   No axes exist on either panel.
4. **MINOR / medium — unconfirmed / contradictory values.** `0.835` and `O4 -0.93`
   appear only in the parse's top block and in **no** crop read; `-0.856`
   (`p_c033b`) appears only in the crop read. Three reads disagree, so per the
   "never bank a claim as a defect when two reads contradict" law these stay
   **advisory**: 0.835, -0.93 (parse-only) and -0.856 (crop-only) are individually
   DEBATABLE.
5. **MINOR / low — `O7 0.155` vs `Input 0.155`.** Parse bottom block labels 0.155
   as `O7`; `p_c033b` labels it `Input`. `X_2 0.305` likewise appears only in the
   parse.

## REAL / HALLUCINATED / DEBATABLE list

- **REAL (corroborated, 2 reads)** — badge `33` (parse `<x_0.9199><y_0.1227>33`);
  `note: η=5`; bottom panel title `Updated weights (after iteration # 10)`
  (parse + `p_c033b` + `analysis/slide_033_final.json`).
- **REAL (corroborated, 2 reads)** — FRAME TOP PANEL label set: header
  `Initialized weights`; `Input 0.1`; `O3 0.3`; `O4 0.4`; `O5 0.5` printed twice;
  `Output 0.791` (node 6's output value); `Target t₆`.
- **REAL (single-read)** — FRAME BOTTOM PANEL: `Input 0.155`, `O3 0.215`,
  `O4 0.675`, `O5 0.575`, `O6 0.943`, `O7 1.05`, `O7 0.77` and the weights
  `-1.2`, `0.93` (`p_c033b`).
- **DEBATABLE** — `0.835`, `-0.93`, `-0.856` (see 4); `X_2 0.305` label.
- **HALLUCINATED (w.r.t. this frame)** — `-0.344` and `-0.455`: no read of slide 033
  contains them (they live only in `analysis/slide_028_raw.json` /
  `analysis/slide_029_raw.json`).

## Uncertainties

- Vision cross-check lane down (`analyze_image.py` header-only, 0 body bytes).
- Bottom-panel row labels (`O6` vs `O7` for 0.943/1.05/0.77) were read once; the
  two crop scales of the *top* panel agree with each other, and the bottom panel
  was read at one scale only (`p_c033b`, 2×) — its values are banked as single-read.

PARSE ADJUDICATION: DEGRADED — stop-finish and crop-recoverable, but both panels' contents are cross-assigned between the top and bottom blocks, the top panel title is dropped, and diagrams are wrapped as `scatter`/`lollipop` charts.
