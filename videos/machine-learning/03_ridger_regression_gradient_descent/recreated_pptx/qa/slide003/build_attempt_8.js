// Build: slide 003 — "Matrix Notation for Linear Regression and Classification (N- Samples)"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Reference frame: unique_slides/slide_003.jpg (960x540, 1px=1pt=1/72in)
// Spec: analysis/slide_003_final.json
//
// MEASURMENTS (frame px, PIL-measured on unique_slides/slide_003.jpg 2026-10-23;
// the FRAME wins over the spec wherever they disagree):
//   Chrome: house_chrome.js (deck law) — canvas FFFFFF, panel E9E9E7 x54..903
//     y45..540, C00000 1pt LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY (no top
//     stroke), badge d35 at (876,73) FDFD96 ring 6A5ACD numeral 3.
//   Title ink:      x82..832, y68..90 — ONE line; "Matrix" blue #0000FF, the
//     remaining words RED #FF0000 (spec said black; frame says red).
//   N Training Samples: x81..272, y177..199, red.
//   Top matrix box: x271..596, y107..301 — BLUE #0000FF border, white fill.
//     Three full-height column bands y141..296: yellow #FFFF99 x296..337,
//     cyan #CCFFFF x372..415, pink #FFC0CB x513..557. Column headers above the
//     bands at y120..139; red y-labels inside the bands at y277..293.
//   Remember box:   x649..874, y153..221 — blue border, pale-cyan fill;
//     red bold italic "Remember" x656..689 y160..176; blue UNDERLINED equation
//     y=W^T X = X^T W, blue ink x699..867 y185..214.
//   In General box: x659..850, y268..294 — border #6C5B3D, cream fill.
//   Bottom-left box:  x79..533, y323..517 — RED #C00000 border, cyan #CCFFFF fill
//   Bottom-right box: x572..752, y323..517 — RED #C00000 border, white fill
//   Arrow:          x532..573, y330..409 (tall chevron)
//
// The previous build carried an unverified "LO badge correction" (badge cy
// 83.56 instead of 73) and a Remember box at x700..900 y70..180 whose white
// fill was drawn OVER the badge — house_chrome_check.py failed on renders 1-4.
//
// FRAME-VS-SPEC DEVIATIONS: deck house chrome overrides spec's background/border/badge.

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_003_recreated.pptx";

const px = (v) => v / 72;
const A = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

// ---- HOUSE CHROME (shared deck module — badge numeral = file number 3) -----
drawHouseChrome(pptx, slide, { numeral: 3 });

// ---- TITLE: ONE line, measured ink x82..832 y68..90 -----------------------
slide.addText([
  { text: "Matrix", options: { fontFace: A, fontSize: 26, bold: true, color: "0000FF" } },
  { text: " Notation for Linear Regression and Classification (N- Samples)",
    options: { fontFace: A, fontSize: 26, bold: true, color: "FF0000" } },
], {
  x: px(82), y: px(63), w: px(832 - 82), h: px(30),
  align: "center", valign: "top", margin: 0,
});

// ---- LEFT LABEL: "N Training Samples" (measured x81..272 y177..199) --------
slide.addText("N Training Samples", {
  x: px(80), y: px(173), w: px(200), h: px(30),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 18, bold: true, color: "FF0000",
});

// ---- TOP MATRIX BOX (measured x271..596 y107..301, blue border) -----------
const tm_x = 271, tm_y = 107, tm_w = 325, tm_h = 194;
slide.addShape(pptx.ShapeType.rect, {
  x: px(tm_x), y: px(tm_y), w: px(tm_w), h: px(tm_h),
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 },
});

// Three full-height column bands, measured y141..296
const band_defs = [
  { cx: 316.5, w: 42, fill: "FFFF99", label: "X_1" },
  { cx: 393.5, w: 44, fill: "CCFFFF", label: "X_2" },
  { cx: 535,   w: 45, fill: "FFC0CB", label: "X_n" },
];
for (const b of band_defs) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(b.cx - b.w / 2), y: px(141), w: px(b.w), h: px(155),
    fill: { color: b.fill },
  });
}
// Column headers above the bands, measured y120..139
const hdr_x = [316.5, 393.5, 535];
const col_labels = ["X_1", "X_2", "X_n"];
for (let i = 0; i < 3; i++) {
  slide.addText(col_labels[i], {
    x: px(hdr_x[i] - 20), y: px(117), w: px(40), h: px(22),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 13, bold: true, color: "000000", italic: true,
  });
}
// Red y-labels inside the bands, measured y277..293
const y_labels = ["y_1", "y_2", "y_n"];
for (let c = 0; c < 3; c++) {
  slide.addText(y_labels[c], {
    x: px(hdr_x[c] - 20), y: px(274), w: px(40), h: px(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, color: "FF0000", italic: true,
  });
}

// ---- REMEMBER BOX (measured x649..874 y153..221, blue border, pale-cyan fill).
// The old seat (x700..900 y70..180) overlapped and OCCLUDED the house badge. ----
const rb_x = 649, rb_y = 153, rb_w = 225, rb_h = 68;
slide.addShape(pptx.ShapeType.rect, {
  x: px(rb_x), y: px(rb_y), w: px(rb_w), h: px(rb_h),
  fill: { color: "CCFFFF", transparency: 40 }, line: { color: "0000FF", width: 1.5 },
});
// red bold italic "Remember" — measured ink x656..689 y160..176
slide.addText("Remember", {
  x: px(rb_x + 7), y: px(rb_y + 4), w: px(120), h: px(22),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 18, bold: true, color: "FF0000", italic: true,
});
// "y = W^T X = X^T W" — blue glyphs measured x699..867 y185..214 with underline
// runs (y198..199 x677..693 and y214 x843..867). Native text with real
// underline runs in professional 2D-ish layout; blue + underlined per the frame.
const eq_size = 20;
slide.addText([
  { text: "y", options: { fontFace: A, fontSize: eq_size, italic: true, color: "000000" } },
  { text: " = ", options: { fontFace: A, fontSize: eq_size, color: "000000" } },
  { text: "W", options: { fontFace: A, fontSize: eq_size, bold: true, color: "0000FF", underline: true } },
  { text: "T", options: { fontFace: A, fontSize: eq_size, italic: true, color: "000000" } },
  { text: "X", options: { fontFace: A, fontSize: eq_size, bold: true, color: "0000FF", underline: true } },
  { text: " = ", options: { fontFace: A, fontSize: eq_size, color: "000000" } },
  { text: "X", options: { fontFace: A, fontSize: eq_size, bold: true, color: "0000FF", underline: true } },
  { text: "T", options: { fontFace: A, fontSize: eq_size, italic: true, color: "000000" } },
  { text: "W", options: { fontFace: A, fontSize: eq_size, bold: true, color: "0000FF", underline: true } },
], {
  x: px(697), y: px(183), w: px(170), h: px(30),
  align: "left", valign: "middle", margin: 0,
});
// Sidecar banked alongside the superseded PNG asset (eq_*.json law).
fs.writeFileSync(__dirname + "/assets/eq_003_remember.json", JSON.stringify({
  rel_id: null, image: "assets/eq_003_remember.png",
  mathtext: "y = W^{T}X = X^{T}W", font_size_pt: 20, color: "000000",
  blue_runs: ["W", "X", "X", "W"], underline: true,
  note: "native text runs with underline; PNG superseded by the measured build",
}, null, 2));

// ---- IN GENERAL BOX (measured x659..850 y268..294, border #6C5B3D) ---------
const ig_x = 659, ig_y = 268, ig_w = 191, ig_h = 26;
slide.addShape(pptx.ShapeType.rect, {
  x: px(ig_x), y: px(ig_y), w: px(ig_w), h: px(ig_h),
  fill: { color: "FFFFFF" }, line: { color: "6C5B3D", width: 1 },
});
slide.addText([
  { text: "In General: ", options: { fontFace: A, fontSize: 15, color: "000000" } },
  { text: "N", options: { fontFace: A, fontSize: 15, bold: true, color: "FF0000" } },
  { text: " >>> ", options: { fontFace: A, fontSize: 15, bold: true, color: "FF0000" } },
  { text: "d", options: { fontFace: A, fontSize: 15, bold: true, color: "FF0000" } },
], {
  x: px(ig_x + 6), y: px(ig_y + 2), w: px(ig_w - 12), h: px(ig_h - 4),
  align: "left", valign: "middle", margin: 0,
});

// ---- BOTTOM-LEFT BOX (measured x79..533 y323..517, RED border, cyan fill) --
const bl_x = 79, bl_y = 323, bl_w = 454, bl_h = 194;
slide.addShape(pptx.ShapeType.rect, {
  x: px(bl_x), y: px(bl_y), w: px(bl_w), h: px(bl_h),
  fill: { color: "CCFFFF" }, line: { color: "C00000", width: 1 },
});

slide.addText("[", {
  x: px(70), y: px(bl_y + 10), w: px(20), h: px(120),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 30, color: "000000",
});
slide.addText("]", {
  x: px(120), y: px(bl_y + 10), w: px(20), h: px(120),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 30, color: "000000",
});
const y_entries = ["y_1", "y_2", "...", "y_n"];
for (let i = 0; i < y_entries.length; i++) {
  slide.addText(y_entries[i], {
    x: px(75), y: px(bl_y + 15 + i * 28), w: px(45), h: px(22),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, color: "000000", italic: true,
  });
}
slide.addText("N × 1", {
  x: px(70), y: px(bl_y + 135), w: px(70), h: px(16),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 11, color: "FF0000",
});

slide.addText("=", {
  x: px(135), y: px(bl_y + 60), w: px(20), h: px(30),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 24, color: "000000", bold: true,
});

const mx_x = 150;
const mx_rows = [
  ["1", "x_{11}", "x_{12}", "...", "x_{1d}"],
  ["1", "x_{21}", "x_{22}", "...", "x_{2d}"],
  ["1", "...", "...", "...", "..."],
  ["1", "x_{n1}", "x_{n2}", "...", "x_{nd}"],
];
const mx_col_x = [0, 40, 80, 120, 160];
const mx_y_start = bl_y + 15;
const mx_dy = 28;

for (let r = 0; r < mx_rows.length; r++) {
  for (let c = 0; c < mx_rows[r].length; c++) {
    slide.addText(mx_rows[r][c], {
      x: px(mx_x + mx_col_x[c]), y: px(mx_y_start + r * mx_dy), w: px(35), h: px(22),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 11, color: "000000", italic: (c > 0),
    });
  }
}

const wv_x = 350;
slide.addText("[", {
  x: px(wv_x), y: px(bl_y + 10), w: px(20), h: px(120),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 30, color: "000000",
});
slide.addText("]", {
  x: px(wv_x + 45), y: px(bl_y + 10), w: px(20), h: px(120),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 30, color: "000000",
});
slide.addText("b", {
  x: px(wv_x + 5), y: px(bl_y + 15), w: px(40), h: px(22),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 13, color: "0000FF", bold: true,
});
const w_entries = ["w_1", "w_2", "...", "w_d"];
for (let i = 0; i < w_entries.length; i++) {
  slide.addText(w_entries[i], {
    x: px(wv_x + 5), y: px(bl_y + 43 + i * 28), w: px(40), h: px(22),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, color: "000000", italic: true,
  });
}
slide.addText("d+1 × 1", {
  x: px(wv_x), y: px(bl_y + 135), w: px(65), h: px(16),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 11, color: "FF0000",
});

// ---- ARROW (measured ink x532..573 y330..409 — a tall chevron) ------------
slide.addShape(pptx.ShapeType.rightArrow, {
  x: px(532), y: px(330), w: px(573 - 532), h: px(409 - 330),
  fill: { color: "808080" }, line: { color: "808080", width: 0 },
});

// ---- BOTTOM-RIGHT BOX (measured x572..752 y323..517, RED border, white) ----
const br_x = 572, br_y = 323, br_w = 180, br_h = 194;
slide.addShape(pptx.ShapeType.rect, {
  x: px(br_x), y: px(br_y), w: px(br_w), h: px(br_h),
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
});

slide.addText([
  { text: "Y", options: { fontFace: A, fontSize: 16, bold: true, color: "000000", underline: true } },
  { text: " = ", options: { fontFace: A, fontSize: 16, bold: true, color: "000000" } },
  { text: "X", options: { fontFace: A, fontSize: 16, bold: true, color: "000000", underline: true } },
  { text: " ", options: { fontFace: A, fontSize: 16, bold: true, color: "000000" } },
  { text: "W", options: { fontFace: A, fontSize: 16, bold: true, color: "000000", underline: true } },
], {
  x: px(br_x + 15), y: px(br_y + 15), w: px(br_w - 30), h: px(30),
  align: "left", valign: "top", margin: 0,
});

slide.addText([
  { text: "Where: ", options: { fontFace: A, fontSize: 14, color: "000000" } },
  { text: "X", options: { fontFace: A, fontSize: 14, color: "000000", underline: true, italic: true } },
  { text: "_{N×d+1} is a matrix", options: { fontFace: A, fontSize: 14, color: "000000", italic: true } },
], {
  x: px(br_x + 15), y: px(br_y + 55), w: px(br_w - 30), h: px(30),
  align: "left", valign: "top", margin: 0,
  lineSpacing: 1.2,
});

slide.addText([
  { text: "Y", options: { fontFace: A, fontSize: 14, color: "000000", underline: true, italic: true } },
  { text: "_{N×1} is labels vector", options: { fontFace: A, fontSize: 14, color: "000000", italic: true } },
], {
  x: px(br_x + 15), y: px(br_y + 90), w: px(br_w - 30), h: px(30),
  align: "left", valign: "top", margin: 0,
  lineSpacing: 1.2,
});

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch(err => {
  console.error("ERROR:", err);
});