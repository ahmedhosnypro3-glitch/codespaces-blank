# Parse adjudication — slide 008 (10_nn_training_and_example)

SOURCE IMAGE: `unique_slides/slide_008.jpg` (960x540 px, md5 3717cbdf59bd4e75280ccbc6fddc331d)
PARSE TRANSCRIPT: `analysis/parse/slide_008.parse.md` + `analysis/parse/slide_008.parse.json`
ENVELOPE: finish_reason=`stop`, usage.output_tokens=**6**, content_len=55 -> **valid call on transport grounds; the defect is content-level, not truncation**
SECOND READ TYPE: **corroborated** — (a) script-12 vision analysis `analysis/slide_008_final.json` (verdict PASS_WITH_FIXES, independent vision model, full-frame read; question asked: full layout/regions/labels extraction); (b) image-analysis cross-check `analysis/parse/adjudication/vision/slide_008.vision.txt` (independent vision read; question asked: transcribe every visible text item, state whether a title exists, list every label inside the beige diagram box, transcribe the math notation and symbol at far right, and the badge numeral).
MEASUREMENT: `analysis/parse/adjudication/measurements/slide_008.pil.txt`, glyph census `glyphs.py`.

## What the parse returned

The **entire** transcript is one line: `<x_0.3633><y_0.1156><x_0.9346><y_0.4031><class_Picture>`.
Resolved against 960x540 this is the pixel box **(349,62)-(897,218)**, carrying one class token and **zero text tokens**.

## Severity-ranked findings

### BLOCKER — `dropped-region` — a text-bearing slide parsed as a picture shell with no text (confidence: high, corroborated)
The frame is not empty: full-frame ink is 43,380 px = **8.37%** of the canvas (dominant bg `#E7E9E6`), and the top-10
colour list includes 12,007 px of `#000000` and 10,775 px of diagram-grey `#DACEC2` — a populated diagram slide.
Inside the parse's own `<class_Picture>` box the dark-ink census finds **184 components**, of which **9 are glyph-scale**
(h 6-14 px, w 3-15 px) plus two large marks: a vertical bar at x=764, w=14, h=124 and a 40x27 element at x=856, y=62.
A full-frame dark census reproduces the same 9 glyph-scale components — the glyph-scale marks are concentrated exactly
inside the box the parse declared textless.
-> The parse emitted a `<class_Picture>` shell over a region that carries glyph-scale ink, and returned **no text at all**.
Both independent vision reads list ~14 text labels on the slide. Per process-notes, a text-bearing image parsed with
zero text tokens is a FAIL, not a "no result". REAL.

### MAJOR — `glyph-floor-blindness` (mechanism for the BLOCKER) (confidence: medium, corroborated)
The glyph-scale marks inside the box measure **6-14 px tall** (measured heights 9, 7, 14, 14, 14, 9, 14, 14 px), i.e.
below the documented 15-22 px legibility floor, while the script-12 vision read resolves the same pixels to readable
labels (`Multi Bias`, `Net`, `O`, `w`, `Output 1/2/m`, `Error`, `Class 1/2/m`, `∂E/∂w_ij`).
-> The slide is a floor case, not a budget case: `finish_reason=stop` with **6 output tokens** and the ceiling unused.
REAL as the causal class; the specific label inventory is DEBATABLE (see list).

### MAJOR — `hallucinated-content` — a class token asserted over a region the parse never read (confidence: high, corroborated)
`<class_Picture>` with a two-corner box and no content is the parse's structural shell. The box itself is *geometrically*
plausible (it covers the beige diagram), but asserting a class for a region whose contents were never emitted is a
defect: the parse cannot report the class of content it did not read. REAL as a defect.

### MINOR — `coordinate-misalignment` (low severity) (confidence: medium, single-read)
The box's two corner tokens resolve to (349,62) and (897,218). Measured diagram ink occupies x=349..897, y=62..218
(block census: x=30..930 frame-line, content band y=45..225), so the box corners land on real content, not empty canvas.
-> Corners are consistent with the beige diagram extent; no misalignment banked.

### MINOR — `dropped-region` — badge numeral `8` absent (confidence: high, corroborated)
Every other slide in this range has its badge numeral in the parse (007 -> `7`, 009 -> `9`, 011 -> `11`, 012 -> `12`).
Slide 008's parse has none. Both vision reads place a yellow circle with `8` at top-right. REAL.

## Explicit classification list

- REAL (high, corroborated): zero text tokens returned on a text-bearing slide — `dropped-region`, BLOCKER.
- REAL (high, corroborated): badge numeral `8` dropped — `dropped-region`, MINOR.
- REAL (medium-high, corroborated): glyph-floor-blindness as the mechanism (glyph heights 6-14 px, output ceiling unused).
- REAL (high, corroborated): a `<class_Picture>` class asserted over a region whose contents were never read.
- DEBATABLE (advisory only): the exact label inventory — the script-12 read lists `Multi Bias`, `Net`, `O`, `w`,
  `Output 1/2/m`, `Error`, `Class 1/2/m`, `∂E/∂w_ij`, `?`; my local census proves glyph-scale ink but cannot resolve
  the letterforms, so no individual label string is banked as ground truth from my own read.
- HALLUCINATED: none — the parse invented no strings; the defect is omission.

## Uncertainty markers

- `[?]` Whether every label the vision read reports is genuinely on the frame — the vision lane is itself a model read;
  my own evidence is limited to "glyph-scale ink exists inside the declared-textless box".
- `[?]` Whether the far-right element is `∂E/∂w_ij` plus a question mark, or a single `?` — the two vision reads agree
  on both, but no local glyph resolution confirms it.

PARSE ADJUDICATION: FAIL — a text-bearing slide returned as a single empty `<class_Picture>` with 6 output tokens and no text; the parse is untrustworthy for this slide. FIX: do not re-run the same full-frame read (output ceiling unused, so a bigger budget will not help); use the crop cascade on the diagram box at >=3x and/or take the vision-analysis lane's label inventory as the text authority.
