# PARSE ADJUDICATION — slide 034

- Source image: `unique_slides/slide_034.jpg` (960×540 px, video frame, md5 25fcf51d3019f71822b27a62b4dcf116)
- Parse transcript: `analysis/parse/slide_034.parse.md` + `.parse.json` — `finish_reason: stop`, 199 output tokens
- Second-read type: **corroborated** (different input form: 4 region crops +
  automated cascade `analysis/parse/cascade/slide_034/`, all `finish_reason: stop`)
- Second-read files: `_pool/bparse6/crops/p034a` (top panel), `p034b` (table),
  `p_c034c` (title), `p_c034d` (badge), `p_c034e` (table bottom)

## Severity-ranked findings

1. **MAJOR / high — `dropped-region` (title + badge).** The full-frame parse emits
   no title and no badge token. Two independent crops return them: `p_c034c`
   (box 46,45–301,203, 3.0×) reads `Forward Calculations` alone; `p_c034d`
   (box 856,45–920,203, 7.5×) reads `34`. So the frame's title is
   **"Forward Calculations"** and the badge numeral is 34 — both absent from
   `slide_034.parse.md`. Every other slide of this deck (029–033) does return its
   title + badge token.
2. **MAJOR / high — `coordinate-misalignment` (block extent vs content).** The
   transcript's only block is `<x_0.0><y_0.0>` … `<x_0.999><y_0.9984>`, i.e. the
   whole 960×540 frame, for content that is one table. Measured grid: outer border
   y=202–531, verticals x≈45/216/337/476/647 (PIL `_pool/bparse6/measure2.py` and
   `lines.py 34`). The block claims x 0–959 / y 0–538 while the table occupies
   x 45–647 / y 202–531 — the box swallows the whole network schematic the parse
   never transcribed, so no downstream consumer can tell the table's real box
   from this block.
3. **MAJOR / high — network schematic lost (`dropped-region`).** `p034a`
   (top crop) returns `title: Forward Calculations` plus a node table
   (3→0.1, 4→0.2, 5→0.5, 6→0.4, 7→0.7, 8→0.5) with `note: η=5`; the frame's
   top half is the 3-hidden/2-output network (input x₁=1, x₂=5, Bias; hidden 3/4/5
   with O₃/O₄/O₅; output 6/7 with O₆/O₇; Target column x≈872–914). None of it
   appears in the full-frame read except `note: η=5`.
4. **MINOR / high — `class-token-mismatch` / `chart-token-pollution`.** A plain
   markdown grid is emitted inside `<chart type="other">` … `</chart>`
   `<class_Chart>`. The frame has a printed table with a red outer border
   (measured) — no chart, no axes, no plotted points. The chart wrapper plus
   `column_1` for the unread row-label header is the authority-loss defect.
5. **MINOR / high — header row misread.** Header printed as
   `column_1 | O6 | O7 | Squared Error`; `p034b` (table crop, box 5,177–955,540)
   agrees on `O6`, `O7`, `Squared Error` and confirms `column_1` is a placeholder:
   the first column header is not read by either read. Frame pixel geometry puts
   that header cell at x≈45–216, y≈215–245 (text x 227–294 is `O6`'s cell).
6. **MINOR / medium — `Target` row's Squared Error cell.** `p034b` and `p_c034e`
   both show `| Target | 0 | 1 |` with the Squared Error cell **empty** on the
   frame; the full-frame read simply omits the Target row (dropped-region).
   An "ellipsis" row asserted by `analysis/slide_034_final.json`
   (`layout/regions[3]`, "rows Initial Weights, Iteration 1–5, ellipsis row,
   Target") was **not** observed in any read or in the measured 9-band grid —
   treat that JSON claim as unconfirmed.

## REAL / HALLUCINATED / DEBATABLE list

- **REAL (corroborated, 2 reads)** — Squared Error column: 0.669362, 0.151129,
  0.038729, 0.025186, 0.018868, 0.01517 for Initial/It1–It5, with O6/O7 values
  0.791/0.791, 0.352/0.835, 0.152/0.875, 0.119/0.895, 0.102/0.908, 0.091/0.917.
- **REAL (arithmetic, decisive)** — every Squared Error equals Σ(t−O)² with
  t=(0,1) to <7e-18: e.g. (0−0.791)²+(1−0.791)²=0.669362 and
  (0−0.091)²+(1−0.917)²=0.015170. The printed column therefore carries **no ½
  factor** (½·Σ would print 0.334681 / 0.007585). This is a property of the
  *source slide*, not a parse defect: the parse transcribed the printed values
  faithfully. Any recreation must render the frame's numbers, not a "corrected"
  ½ version — worth an explicit note to the builder.
- **REAL (single-read)** — the Target row `0 | 1` and the empty Squared Error
  cell on that row.
- **REAL (single-read)** — `Forward Calculations` title (not in parse; corroborate
  via `p034a`'s `title: Forward Calculations` + `p_c034c`).
- **DEBATABLE** — first-column header text: unread by both reads. Measured cell
  x≈45–216 / y≈215–245; `column_1` in the parse is a placeholder, not a claim.
- **HALLUCINATED (w.r.t. frame coverage)** — the parse's single whole-frame
  `<class_Chart>` box implies the frame is one chart.

## Uncertainties

- Vision cross-check lane down: `analyze_image.py` returned a context header only
  (0 body bytes, 140 s wall) — HTTP endpoint HardDown for this reader. All
  verdicts rest on parse reads + PIL geometry (no contradictions between them).
- The network schematic's exact node labels/weight values in slide 034's top half
  were only read once (`p034a`, garbled chart-shaped output); not banked as content.

PARSE ADJUDICATION: DEGRADED — table content itself is faithful (Squared Error verified exact), but the full-frame read dropped title, badge, target row and the whole network schematic and wrapped a printed table as `<class_Chart>`.
