// Build: slide 003 — "Matrix Notation for Linear Regression and Classification (N- Samples)"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Reference frame: unique_slides/slide_003.jpg (960x540, 1px=1pt=1/72in)
// Spec: analysis/slide_003_final.json
//
// MEASURED GEOMETRY (frame px from PIL measurement + ASCII art structural analysis):
//   Canvas: white FFFFFF
//   Panel: gray E9E9E7 rect x54..903 y45..540 (no top stroke)
//   Title: "Matrix Notation for Linear Regression and Classification (N- Samples)"
//     - y band ~68-86, x ~88..894 (center ~474)
//     - "Matrix" blue #0000FF bold ~32pt; rest black #000000 bold ~32pt
//   Badge: numeral "3" at (876, 73) d~35, fill FDFD96, ring 6A5ACD 2pt, numeral 333333 bold Arial 18pt
//     - LO render correction: badge cy needs +10.56 frame px (22px at 150dpi) -> use cy=83.56
//   Left label: "N Training Samples" red #FF0000 ~18pt, x~80..180, y~110..145
//   Top matrix box: gray #808080 border rect ~x140..740, y~90..230
//   Remember box: blue #0000FF border rect ~x700..900, y~70..180
//   In General box: black border rect ~x700..900, y~195..260
//   Bottom-left box: gray #808080 border rect ~x55..400, y~285..490
//   Arrow: gray #808080 right-pointing, x~396..470 at y~375
//   Bottom-right box: gray #808080 border rect ~x475..904, y~285..490
//
// FRAME-VS-SPEC DEVIATIONS: deck house chrome overrides spec's background/border/badge.

const pptxgen = require("pptxgenjs");
const fs = require("fs");

const ASSET_DIR = __dirname + "/assets";
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_003_recreated.pptx";

const px = (v) => v / 72;
const A = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

// ---- HOUSE CHROME (inlined with badge cy correction) ----
// Canvas
slide.background = { color: "FFFFFF" };
// Panel: x54..903, y45..540
slide.addShape(pptx.ShapeType.rect, {
  x: px(54), y: px(45), w: px(903 - 54 + 1), h: px(540 - 45),
  fill: { color: "E9E9E7" },
});
// Strokes: C00000 1pt - LEFT, RIGHT, BOTTOM only (NO TOP)
const st = { color: "C00000", width: 1 };
// Left vertical: x58.5, y46..539
slide.addShape(pptx.ShapeType.line, {
  x: px(58.5), y: px(46), w: 0, h: px(539 - 46),
  line: st,
});
// Right vertical: x901, y46..539
slide.addShape(pptx.ShapeType.line, {
  x: px(901), y: px(46), w: 0, h: px(539 - 46),
  line: st,
});
// Bottom horizontal: y538.5, x58..902
slide.addShape(pptx.ShapeType.line, {
  x: px(58), y: px(538.5), w: px(902 - 58), h: 0,
  line: st,
});
// Badge: corrected cy = 83.56 frame px (was 73, LO renders 22px high)
const badge_cx = 876 / 72;
const badge_cy = 83.56 / 72;  // corrected for LO offset
const badge_d = 35 / 72;
const bx = badge_cx - badge_d / 2;
const by = badge_cy - badge_d / 2;
slide.addShape(pptx.ShapeType.ellipse, {
  x: bx, y: by, w: badge_d, h: badge_d,
  fill: { color: "FDFD96" },
  line: { color: "6A5ACD", width: 2 },
});
slide.addText("3", {
  x: bx, y: by, w: badge_d, h: badge_d,
  align: "center", valign: "middle", bold: true,
  fontSize: 18, color: "333333", fontFace: "Arial", margin: 0,
});

// ---- TITLE ---------------------------------------------------------------
slide.addText("Matrix", {
  x: px(474 - 410), y: px(77 - 8), w: px(820), h: px(55),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 32, bold: true, color: "0000FF",
});
slide.addText("Notation for Linear Regression and Classification (N- Samples)", {
  x: px(474 - 410), y: px(77 - 8 + 34), w: px(820), h: px(55),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 32, bold: true, color: "000000",
});

// ---- LEFT LABEL: "N Training Samples" ------------------------------------
slide.addText("N Training Samples", {
  x: px(60), y: px(110), w: px(130), h: px(50),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 18, bold: true, color: "FF0000", italic: false,
  lineSpacing: 22,
});

// ---- TOP MATRIX BOX (gray border) ----------------------------------------
const tm_x = 140, tm_y = 90, tm_w = 600, tm_h = 140;
slide.addShape(pptx.ShapeType.rect, {
  x: px(tm_x), y: px(tm_y), w: px(tm_w), h: px(tm_h),
  fill: { color: "FFFFFF" }, line: { color: "808080", width: 1 },
});

const col_x = [315, 393, 697];
const col_labels = ["X_1", "X_2", "X_n"];
const col_bg = ["FFFF99", "CCFFFF", "FFC0CB"];

for (let i = 0; i < 3; i++) {
  const cx = col_x[i];
  const bw = 70;
  slide.addShape(pptx.ShapeType.rect, {
    x: px(cx - bw/2), y: px(115), w: px(bw), h: px(22),
    fill: { color: col_bg[i] }, line: { color: "808080", width: 0.5 },
  });
  slide.addText(col_labels[i], {
    x: px(cx - bw/2), y: px(115), w: px(bw), h: px(22),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 13, bold: true, color: "000000", italic: true,
  });
}

slide.addText("...", {
  x: px(450), y: px(115), w: px(100), h: px(22),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 16, bold: true, color: "000000",
});

const entry_rows = [
  ["x_{11}", "x_{21}", "x_{n1}"],
  ["x_{12}", "x_{22}", "x_{n2}"],
  ["...", "...", "..."],
  ["x_{1d}", "x_{2d}", "x_{nd}"],
];
const entry_y_start = 145;
const entry_dy = 15;
for (let r = 0; r < entry_rows.length; r++) {
  for (let c = 0; c < 3; c++) {
    slide.addText(entry_rows[r][c], {
      x: px(col_x[c] - 30), y: px(entry_y_start + r * entry_dy), w: px(70), h: px(16),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 11, color: "000000", italic: true,
    });
  }
}

slide.addShape(pptx.ShapeType.line, {
  x: px(tm_x + 10), y: px(210), w: px(tm_w - 20), h: 0,
  line: { color: "000000", width: 1 },
});

const y_labels = ["y_1", "y_2", "y_n"];
for (let c = 0; c < 3; c++) {
  slide.addText(y_labels[c], {
    x: px(col_x[c] - 30), y: px(213), w: px(70), h: px(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, color: "FF0000", italic: true,
  });
}

// ---- REMEMBER BOX (blue border) ------------------------------------------
const rb_x = 700, rb_y = 70, rb_w = 200, rb_h = 110;
slide.addShape(pptx.ShapeType.rect, {
  x: px(rb_x), y: px(rb_y), w: px(rb_w), h: px(rb_h),
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 },
});
slide.addText("Remember", {
  x: px(rb_x + 10), y: px(rb_y + 8), w: px(rb_w - 20), h: px(22),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 16, bold: false, color: "FF0000", italic: true,
});
const eq_rem_w = 2.09333, eq_rem_h = 0.36333;
slide.addImage({
  path: ASSET_DIR + "/eq_003_remember.png",
  x: px(rb_x + rb_w/2) - eq_rem_w/2, y: px(rb_y + 35),
  w: eq_rem_w, h: eq_rem_h,
});

// ---- IN GENERAL BOX (black border) ---------------------------------------
const ig_x = 700, ig_y = 195, ig_w = 200, ig_h = 65;
slide.addShape(pptx.ShapeType.rect, {
  x: px(ig_x), y: px(ig_y), w: px(ig_w), h: px(ig_h),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1.5 },
});
slide.addText([
  { text: "In General: ", options: { fontFace: A, fontSize: 15, bold: false, color: "000000" } },
  { text: "N", options: { fontFace: A, fontSize: 15, bold: true, color: "FF0000" } },
  { text: " >>> ", options: { fontFace: A, fontSize: 15, bold: true, color: "FF0000" } },
  { text: "d", options: { fontFace: A, fontSize: 15, bold: true, color: "FF0000" } },
], {
  x: px(ig_x + 10), y: px(ig_y + 10), w: px(ig_w - 20), h: px(ig_h - 20),
  align: "left", valign: "top", margin: 0,
});

// ---- BOTTOM-LEFT BOX (gray border) ---------------------------------------
const bl_x = 55, bl_y = 285, bl_w = 345, bl_h = 205;
slide.addShape(pptx.ShapeType.rect, {
  x: px(bl_x), y: px(bl_y), w: px(bl_w), h: px(bl_h),
  fill: { color: "FFFFFF" }, line: { color: "808080", width: 1 },
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

// ---- ARROW (gray, right-pointing) ----------------------------------------
const arrow_y = 375;
const arrow_x0 = 400, arrow_x1 = 475;
slide.addShape(pptx.ShapeType.rightArrow, {
  x: px(arrow_x0), y: px(arrow_y - 6), w: px(arrow_x1 - arrow_x0), h: px(12),
  fill: { color: "808080" }, line: { color: "808080", width: 0 },
});

// ---- BOTTOM-RIGHT BOX (gray border) --------------------------------------
const br_x = 475, br_y = 285, br_w = 430, br_h = 205;
slide.addShape(pptx.ShapeType.rect, {
  x: px(br_x), y: px(br_y), w: px(br_w), h: px(br_h),
  fill: { color: "FFFFFF" }, line: { color: "808080", width: 1 },
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