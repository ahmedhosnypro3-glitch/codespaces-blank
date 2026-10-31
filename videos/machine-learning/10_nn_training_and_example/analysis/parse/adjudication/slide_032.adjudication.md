# PARSE ADJUDICATION — slide 032

- Source image: `unique_slides/slide_032.jpg` (960×540 px, video frame)
- Parse transcript: `analysis/parse/slide_032.parse.md` + `.parse.json` — `finish_reason: stop`, 260 output tokens
- Second-read type: **corroborated** (different input form: 4 panel crops at two
  scales — 2.0× and 3.0× — all `finish_reason: stop`)
- Second-read files: `_pool/bparse6/crops/p_c032a` (top 2×), `p_c032b` (bottom 2×),
  `p_c032c` (top 3×), `p_c032d` (bottom 3×)
- JSON context: `analysis/slides_final.json` is `[]` (no per-slide entries at all)
  and `analysis/slide_032_final.json` does not exist — only `slide_032_raw.json`,
  so **no analysis-JSON truth exists for this slide**; everything below is
  frame-derived.

## Severity-ranked findings

1. **MAJOR / high — `dropped-region` (top panel title).** The parse's top block
   carries no title, but the frame's top panel is titled. Both crop reads return
   `title: Initialized weights` (`p_c032a` box 66,51–859,301 at 2×;
   `p_c032c` box 100,60–830,260 at 3×) — corroborated, and consistent with
   `analysis/slide_032_raw.json`'s own "TOP PANEL ('Initialized weights')"
   description. The full-frame read simply drops it.
2. **MAJOR / high — panel content cross-contamination (`reading-order-inversion`).**
   The coordinate *boxes* are correct (top block `<x_0.1016><y_0.1656>`→
   `<x_0.8555><y_0.5258>` = x 98–821, y 89–285; bottom block `<x_0.1025><y_0.6102>`→
   `<x_0.8545><y_0.9734>` = x 98–820, y 330–526 — matching the measured panel
   rulers at y≈89/260–285 and y≈330/502–525 in `_pool/bparse6/lines.py 32`).
   The *rows inside them* are not:
   - Parse top block: `Input 0.125 | O3 0.215 | Output 0.527 | Target 0.458 |
     Bias 0.575 | Bias 0.134 | Bias 0.625 | Output 0.105`.
   - Frame top panel (2 corroborating reads): `Input 0.1 | O3 0.3 | O4 0.4 |
     O5 0.5 | O5 0.5 | Output 6 | O6 0.791 | Target t₆`.
   - The parse's 0.125/0.215/0.575/0.625/0.669/0.375 are the **bottom** panel's
     weights (`p_c032b`, `p_c032d` both return them). The top block therefore sells
     bottom-panel values as top-panel values, and none of the frame's actual top
     values (0.1/0.3/0.4/0.5/0.791) appear in it.
3. **MAJOR / high — `class-token-mismatch` + `chart-token-pollution`.** Both panels
   are printed network diagrams (input vector, yellow hidden nodes 3/4/5, orange
   output nodes 6/7, coloured weight labels between them; measured panel boxes
   x 101–823, y 138–254 and y 343–496). The parse wraps each in
   `<chart type="scatter">` and emits markdown data tables with invented
   chart metadata `axis[x]: Bias`, `bind: value ; ; y` / `bind: x1 ; ; x`,
   `bind: y2 ; ; y`. No axes exist on either panel; the parse is trying to force a
   diagram into chart syntax.
4. **MINOR / medium — unconfirmed values.** `0.527`, `0.458`, `0.105` in the top
   block: none appear in any crop read of either panel. Sibling frames carry
   `0.525` (`W32=0.4+0.125=0.525`, from `slide_030.parse.md` and slide 031's
   cascade) and `0.458` (`W73`, `slide_030.parse.md`), so 0.527/0.458 are probably
   frame values of a *different* region, not of slide 032's top panel. Banked as
   suspicious, not as hallucination, because a third read was not obtainable.
5. **MINOR / low — `glyph-floor-blindness` on the Bias label.** `p_c032d` (3×)
   renders the Bias row as `Bigs` twice while 2× and the full-frame read read
   `Bias` correctly — the classic two-scale signature. Full-frame `Bias` tokens
   are accepted as correct.

## REAL / HALLUCINATED / DEBATABLE list

- **REAL (corroborated, 2 reads)** — badge `32` (parse `<x_0.9199><y_0.1227>32`);
  `note: η=5` in both panels; bottom panel title
  `Updated weights (after iteration # 1)` (parse + `p_c032b` + `p_c032d`).
- **REAL (corroborated, 2 reads)** — FRAME TOP PANEL label set (this is the e)
  deliverable for slide 032, since no `slides_final.json` entry exists):
  header `Initialized weights`; `Input 0.1`; `O3 0.3`; `O4 0.4`;
  `O5 0.5` printed twice (two `O₅` labels); `Output 6` (node number);
  `O6 0.791`; `Target t₆`.
- **REAL (corroborated, 2 reads)** — FRAME BOTTOM PANEL contains the weight values
  0.125, 0.305, 0.215, 0.575, 0.105, 0.125, 0.115, 0.625, 0.669 and 0.375.
- **REAL (single-read)** — bottom panel carries the magenta hidden→output weights
  `-0.134` paired with `0.669` and `-0.445` paired with `0.375`
  (`p_c032b` only).
- **HALLUCINATED (w.r.t. this frame)** — `-0.344` and `-0.455` do not appear in any
  read of slide 032 (they occur only in `analysis/slide_028_raw.json` /
  `analysis/slide_029_raw.json`). The disputed pair is therefore
  **`-0.134`+`-0.445` REAL, `-0.344`+`-0.455` not frame-supported on this slide**.
- **DEBATABLE** — `0.527` / `0.458` / `0.105` in the parse's top block (see 4).

## Uncertainties

- Vision cross-check lane down (`analyze_image.py` header-only, 0 body bytes,
  140 s wall). No parse read and no PIL measurement contradicted each other.
- Whether the top panel prints one or two `O₅ 0.5` labels was read identically by
  both crop scales, so it is banked as two labels, but it is a diagram-label
  question a vision leg should settle.

PARSE ADJUDICATION: DEGRADED — stop-finish and recoverable by crops, but the full-frame block sells bottom-panel values as top-panel values, drops the top panel title, and wraps diagrams as `<chart type="scatter">`.
