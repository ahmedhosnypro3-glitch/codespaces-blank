# Source verification — slide 052

## Claims checked

- No textual claim of any kind appears on this frame. The slide is a bare figure on a white
  stage: no title, no legend, no axis titles, no caption, no equations, no library names,
  no dataset names, no hyperparameter names, no theorem attributions, no sign
  conventions — claims checked: 0 — NEEDS_NO_SOURCE — no source required
  (doc-parse `analysis/parse_out_052/slide_052.parse.md` returns only a scatter-chart
  table; pixel scan of the frame finds no glyphs anywhere outside the purple badge).
- The only numerals on the frame are the plot's own axis tick labels (x 0–14, y 7.5–27,
  read by doc-parse from the raster, so ±1 unit of rounding is expected). These are the
  figure's internal coordinate ranges, not an external factual assertion, and no
  authoritative source exists that could confirm or correct them — NEEDS_NO_SOURCE — no
  source required.
- What the figure depicts is disputed between two banked transcripts — UNVERIFIABLE —
  `analysis/slide_052_raw.json` reads red dots above / blue dots below with a decision
  boundary line, while pixel bands measured off `unique_slides/slide_052.jpg` put the
  dense red mass in y 180–260 and the dense blue mass in y 180–330 — the two overlap, so
  the classes are not cleanly separated into an upper/lower split in this frame. This is
  an image-reading question about the original frame, not a DATA claim; web sources
  cannot settle it. Resolve visually against `unique_slides/slide_052.jpg`.

## Overall

- VERDICT: NEEDS_NO_SOURCE
- 0 web searches spent; there is no named external fact on this slide (no dataset,
  library, formula, hyperparameter, or theorem) for a source to confirm or correct.
- Tolerance notes for the rebuild: `verbatim_text` must stay EMPTY — the slide shows no
  text at all, so a recreation that adds a title, legend, axis titles, or a caption
  invents content. Reproduce the axis tick ranges only (x 0–14, y 7.5–27) and the red/blue
  dot positions as measured from the frame, keeping the measured band overlap rather than
  an idealized clean separation. The bottom black bar clipped by the frame's bottom edge
  (rows 516–539, ~452 px wide of a ~840 px bar) is capture chrome, not slide content.
  Badge numeral stays exactly `52` per the house rule (badge = printed number on the
  original).
