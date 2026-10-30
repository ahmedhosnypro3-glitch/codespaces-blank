# COMPONENT VERIFICATION — slide 013

Date: 2026-10-24 · worker w013 · deck 03_ridger_regression_gradient_descent

The deliverable build (`recreated_pptx/build/slide_013.js`) is a thin writer that
requires `recreated_pptx/build/components/slide_013.js` and calls
`renderBase(pres, slide, { numeral: 13 })`. The component is therefore the single
source of truth for the certified composition.

Closed-loop proof that the exported component reproduces the certified slide
byte-for-byte at the render level:

```
NODE_PATH=$(npm root -g) node qa/slide013/component_probe_013.js
soffice --headless -env:UserInstallation=file://<scratch>/lo/probe13 \
  --convert-to pdf --outdir <scratch> qa/slide013/component_probe_013.pptx
pdftoppm -png -r 150 ... -> qa/slide013/component_probe_013.png
```

| file | md5 |
|---|---|
| qa/slide013/component_probe_013.png | 0321e28c3abb6afd3f35b099d5cb5547 |
| qa/slide013/render_6.png (certified) | 0321e28c3abb6afd3f35b099d5cb5547 |

Result: **pixel-identical** (same md5, 2001x1125) — the component export is the
certified composition, no drift.

Component contract for children (slide 017 imports this):

- `renderBase(pptx, slide, opts)` — full slide: house chrome (numeral 13) +
  title + Train/Test labels + 3 train tables + 3 test tables + 6 arrows + 3 W
  boxes (red border + 600-dpi math image). `opts.numeral`, `opts.skip{block}`,
  `opts.only{block}`.
- Per-block exports: `drawChrome, drawTitle, drawLabels, drawTrainTables,
  drawTestTables, drawArrows, drawWBoxes`.
- Data/geometry exports: `TITLE_TEXT, TITLE_BOX, LABELS, TRAIN_X/W/COLS/BANDS,
  TEST_X/W/COLS/BANDS, WBOX_RECT/IMG/W/H, ARROWS, ARROW, TRAIN_HEADER,
  TEST_HEADER, TRAIN_ROWS, TEST_ROWS, TABLE_FONT_SIZE, TEST_HEAD_FONT_SIZE,
  SUBSCRIPT_SIZE, RED, BLUE, BLACK, WHITE, YELLOW, TRAIN_BORDER, TEST_BORDER,
  TEST_SHADE, SERIF, SANS, runsFor`.
- Shared table-pattern re-exports (from the certified parent 012):
  `makeTrainTable, makeTestTable`.
