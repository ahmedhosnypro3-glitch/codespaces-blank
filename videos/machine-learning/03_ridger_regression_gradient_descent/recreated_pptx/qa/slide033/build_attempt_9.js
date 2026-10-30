// Build: slide 033 — "Non-Convex Function"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Reference frame: unique_slides/slide_033.jpg (960x540, 1px = 1pt = 1/72 in)
//
// ATTEMPT 7 — rebuilt from a full PIL re-measurement of the ORIGINAL frame
// (attempts 1-6 drew a generic layout that did not match the frame: Arial
// title that wrapped over the subtitle, a violet param box, the equation
// inside the annotation box, only 16 table columns, empty right-hand cells,
// and a hand-traced plot fragment). Every element below now follows the
// frame's measured ink bboxes documented inline.
//
// =====================================================================
// MEASURED GEOMETRY (frame px; PIL analysis of unique_slides/slide_033.jpg)
// =====================================================================
// HOUSE CHROME: shared_patterns/house_chrome.js drawHouseChrome(numeral 33).
//
// TITLE   "Non-Convex Function": Times bold, ink x197..432 y66..83, C00000,
//         centered in the x100..530 band (center 314.5).
// SUB L1  "May reach different minimum value based on:" Times bold C00000,
//         ink x115..525 y95..109 (center 320).
// SUB L2  "initial point and learning rate": "initial point" BLUE #0000CC,
//         " and " RED #C00000, "learning rate" BLUE #0000CC; ink x192..459
//         y119..138 (center 325.5); Times bold.
//
// PARAM BOX x75..174 y246..308 (white, navy #1E1856 border). Three coloured
//         cell rows: step|0.1 green #E9FFD4, initial X|-11 pink #F9BBC1,
//         delta|0.1 yellow #FDFD00. Text 8pt Arial bold black.
// RED BLOCK ARROW from (167,299) to (202,338) pointing to the table's
//         first column (frame shows a hollow red-outlined block arrow).
//
// EQUATION BOX x449..585 y182..230 white with C00000 border; 2D stacked
//         fraction f(x) = (x^2 cos(x) - x)/10 (mathtext \dfrac 13.5pt PNG
//         at exact px/600 size; original equation ink x460..575 y188..225).
// ANNOTATION BOX x246..597 y254..299 pale green #EFFFE2, green border.
//         Line 1: "X" red bold italic + "is in between -9.7 and color red
//         bold -9.6" (the literal words "color red bold" ARE on the frame;
//         the analysis had stripped them as a style descriptor) with BOTH
//         -9.7 and -9.6 red bold (frame census: -9.7 ink 183/197 reddish
//         min RGB (210,139,136); -9.6 ink 221/232 reddish min (154,14,25)). Line 2: "f(x)" blue bold italic + "is in between -8.08
//         and -8.011" with both values blue bold.
//
// PLOT box x607..845 y60..313 white with C00000 border. The plotted ink is
//         the analytic f(x) over x in [-12.68, 13.69] (mapping fitted on the
//         frame's teal ink: x_px = 721.5 + 8.95x, y_px = 172 - 9.25 f(x),
//         median residual 0.34 px). Grid every 2 units, black double-arrow
//         axes at y=0 / x=0, x ticks -10..10, y ticks 8..-12 (0 / -2 not
//         printed on the frame). Curve teal #2FA9AC, lw 2.6.
//         Markers (frame-measured): maroon dashed drop line x617 y150..171;
//         red dot x621..626 y144..149; orange #ED7D31 arrow x632..645
//         y118..136; bright green square x629..642 y237..245; pink
//         #F7C9FA "Reach / Local Minima" callout x613..700 y258..295 with
//         purple italic text and a black pointer to the green square.
//         Axis label "x" sits OUTSIDE the plot border at ~x850 y168.
//
// TABLE outer box x86..869 y320..519 (white, navy border).
//   label column x86..143; 18 data columns with separators measured at
//   143,184,224,264,304,344,384,425,465,505,546,586,626,666,707,747,787,
//   827,867. The analysis transcribed only 16 columns; the frame shows 18
//   (after x=-9.8 the gradient-descent columns oscillate -9.7 / -9.6).
//   Bands (frame-measured):
//     band1 y331..369 fill #D9E275, navy border;  rows y341 / 359
//     band2 y374..411 fill #D6B2F5, violet border; rows y383 / 401
//     band3 y417..455 fill #F7DDC2, brown border;  rows y427 / 445
//     slope y459..479: label cell #E9FFD4, data #DEAC95, green border;
//           cols 14 & 16 (slope 0.3) are yellow #F5FB9C with green borders;
//           row y469
//     next x y483..503: pink #F7BEC4, red border; row y493
//   Cyan insert x666..787 y332..368 (#8BF8AB) with a maroon DASHED border
//   over band1 cols 13-15; its text is dark green #006400.
//   All table text 8pt Arial bold; labels right-aligned at x141, values
//   centered per column.
//
// Laws: hex without '#'; fontFace explicit; margin 0; measured geometry;
// equation/plot images embedded at exact px/600 and px/72 sizes.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_033_recreated.pptx";

const px = (v) => v / 72;
const A = "Arial";
const T = "Times New Roman";

const C_RED = "C00000";
const C_BLUE = "0000CC";
const C_NAVY = "1E1856";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: "33" });

// ================= TITLE / SUBTITLE =================
slide.addText("Non-Convex Function", {
  x: px(100), y: px(60), w: px(430), h: px(26),
  align: "center", valign: "top", margin: 0,
  fontFace: T, fontSize: 25, bold: true, color: C_RED,
});
slide.addText("May reach different minimum value based on:", {
  x: px(100), y: px(91), w: px(440), h: px(20),
  align: "center", valign: "top", margin: 0,
  fontFace: T, fontSize: 17, bold: true, color: C_RED, charSpacing: 1.8,
});
slide.addText([
  { text: "initial point", options: { fontFace: T, fontSize: 21, bold: true, color: C_BLUE } },
  { text: " and ", options: { fontFace: T, fontSize: 21, bold: true, color: C_RED } },
  { text: "learning rate", options: { fontFace: T, fontSize: 21, bold: true, color: C_BLUE } },
], {
  x: px(175), y: px(114), w: px(300), h: px(27),
  align: "center", valign: "top", margin: 0,
});

// ================= PARAMETER BOX =================
// white box with navy border, three coloured cell rows
slide.addShape(pptx.ShapeType.rect, {
  x: px(75), y: px(246), w: px(99), h: px(62),
  fill: { color: "FFFFFF" }, line: { color: C_NAVY, width: 1.25 },
});
const PCELLS = [
  { y0: 255, y1: 270, fill: "E9FFD4", label: "step", value: "0.1" },
  { y0: 270, y1: 285, fill: "F9BBC1", label: "initial X", value: "-11" },
  { y0: 285, y1: 300, fill: "FDFD00", label: "delta", value: "0.1" },
];
for (const c of PCELLS) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(80), y: px(c.y0), w: px(47), h: px(c.y1 - c.y0),
    fill: { color: c.fill }, line: { color: C_NAVY, width: 0.5 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(127), y: px(c.y0), w: px(43), h: px(c.y1 - c.y0),
    fill: { color: c.fill }, line: { color: C_NAVY, width: 0.5 },
  });
  slide.addText(c.label, {
    x: px(81), y: px(c.y0), w: px(45), h: px(c.y1 - c.y0),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 8, bold: true, color: "000000",
  });
  slide.addText(c.value, {
    x: px(128), y: px(c.y0), w: px(41), h: px(c.y1 - c.y0),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 8, bold: true, color: "000000",
  });
}
// hollow red block arrow pointing from the param box to the table
slide.addShape(pptx.ShapeType.rightArrow, {
  x: px(156), y: px(297), w: px(58), h: px(26), rotate: 45,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 },
});

// ================= EQUATION BOX =================
slide.addShape(pptx.ShapeType.rect, {
  x: px(449), y: px(182), w: px(136), h: px(48),
  fill: { color: "FFFFFF" }, line: { color: C_RED, width: 1.25 },
});
// eq_033_main_v7b.png: 998 x 216 px at 600 dpi -> 119.8 x 25.9 pt exactly
slide.addImage({
  path: ASSET_DIR + "/eq_033_main_v7b.png",
  x: px(517 - 119.8 / 2), y: px(206.5 - 25.9 / 2),
  w: 119.8 / 72, h: 25.9 / 72,
});

// ================= ANNOTATION BOX =================
slide.addShape(pptx.ShapeType.rect, {
  x: px(246), y: px(254), w: px(351), h: px(45),
  fill: { color: "EFFFE2" }, line: { color: "008000", width: 1.25 },
});
slide.addText("X", {
  x: px(248), y: px(257), w: px(42), h: px(16),
  align: "left", valign: "middle", margin: 0,
  fontFace: T, fontSize: 17, bold: true, italic: true, color: C_RED,
});
slide.addText([
  { text: "is in between ", options: { fontFace: T, fontSize: 17, bold: true, color: "000000" } },
  { text: "-9.7", options: { fontFace: T, fontSize: 17, bold: true, color: C_RED } },
  { text: " and color red bold ", options: { fontFace: T, fontSize: 17, bold: true, color: "000000" } },
  { text: "-9.6", options: { fontFace: T, fontSize: 17, bold: true, color: C_RED } },
], {
  x: px(293), y: px(257), w: px(301), h: px(16),
  align: "left", valign: "middle", margin: 0,
});
slide.addText("f(x)", {
  x: px(248), y: px(276), w: px(44), h: px(20),
  align: "left", valign: "middle", margin: 0,
  fontFace: T, fontSize: 17, bold: true, italic: true, color: C_BLUE,
});
slide.addText([
  { text: "is in between ", options: { fontFace: T, fontSize: 17, bold: true, color: "000000" } },
  { text: "-8.08", options: { fontFace: T, fontSize: 17, bold: true, color: C_BLUE } },
  { text: " and ", options: { fontFace: T, fontSize: 17, bold: true, color: "000000" } },
  { text: "-8.011", options: { fontFace: T, fontSize: 17, bold: true, color: C_BLUE } },
], {
  x: px(293), y: px(276), w: px(301), h: px(20),
  align: "left", valign: "middle", margin: 0,
});

// ================= FUNCTION PLOT =================
// white plot box with the frame's dark-red border
slide.addShape(pptx.ShapeType.rect, {
  x: px(607), y: px(60), w: px(238), h: px(253),
  fill: { color: "FFFFFF" }, line: { color: C_RED, width: 1.25 },
});
// generated analytic plot: 1966 x 2083 px at 600 dpi -> 235.92 x 249.96 pt
slide.addImage({
  path: ASSET_DIR + "/slide_033_plot_v7.png",
  x: px(608), y: px(62), w: 1966 / 600, h: 2083 / 600,
});
// axis label "x" — the frame prints it OUTSIDE the plot border (x~850 y168)
slide.addText("x", {
  x: px(847), y: px(164), w: px(16), h: px(16),
  align: "center", valign: "middle", margin: 0,
  fontFace: T, fontSize: 10, bold: true, color: "333333",
});
// maroon dashed drop line under the initial point
slide.addShape(pptx.ShapeType.line, {
  x: px(617), y: px(150), w: 0, h: px(21),
  line: { color: "8B0000", width: 1, dashType: "dash" },
});
// red initial-point dot (frame x621..626 y144..149)
slide.addShape(pptx.ShapeType.ellipse, {
  x: px(620), y: px(143), w: px(7), h: px(7),
  fill: { color: "D00000" }, line: { color: "D00000", width: 0 },
});
// orange arrow from the initial point up-right (frame x632..645 y118..136);
// flipH makes the line run (646,117)->(633,136) with the head at the lower left
slide.addShape(pptx.ShapeType.line, {
  x: px(633), y: px(117), w: px(13), h: px(19), flipH: true,
  line: { color: "ED7D31", width: 3, endArrowType: "triangle" },
});
// bright green square at the reached local minimum (x629..642 y237..245)
slide.addShape(pptx.ShapeType.rect, {
  x: px(629), y: px(236), w: px(13), h: px(9),
  fill: { color: "7CFC00" }, line: { color: "7CFC00", width: 0 },
});
// "Reach Local Minima" callout (x613..700 y258..295) + pointer
slide.addShape(pptx.ShapeType.line, {
  x: px(692), y: px(258), w: px(-51), h: px(-12),
  line: { color: "000000", width: 1.2 },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(613), y: px(257), w: px(87), h: px(38),
  fill: { color: "F7C9FA" }, line: { color: "8E2A92", width: 0.75 },
});
slide.addText([
  { text: "Reach", options: { fontFace: T, fontSize: 10, bold: true, italic: true, color: "8E2A92", breakLine: true } },
  { text: "Local Minima", options: { fontFace: T, fontSize: 10, bold: true, italic: true, color: "8E2A92" } },
], {
  x: px(613), y: px(257), w: px(87), h: px(38),
  align: "center", valign: "middle", margin: 0, lineSpacing: 12,
});

// ================= TABLE =================
const TBL = { x0: 86, x1: 869, y0: 320, y1: 519 };
// outer white table box with navy border
slide.addShape(pptx.ShapeType.rect, {
  x: px(TBL.x0), y: px(TBL.y0), w: px(TBL.x1 - TBL.x0), h: px(TBL.y1 - TBL.y0),
  fill: { color: "FFFFFF" }, line: { color: C_NAVY, width: 1.25 },
});
const XSEP = [143, 184, 224, 264, 304, 344, 384, 425, 465, 505, 546, 586, 626, 666, 707, 747, 787, 827, 867];

// bands: [y0, y1, fill, border]
const BANDS = [
  { y0: 331, y1: 369, fill: "D9E275", border: C_NAVY, bw: 1.25 },
  { y0: 374, y1: 411, fill: "D6B2F5", border: "5B2C6F", bw: 1.25 },
  { y0: 417, y1: 455, fill: "F7DDC2", border: "6B4226", bw: 1.25 },
];
for (const bd of BANDS) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(87), y: px(bd.y0), w: px(781), h: px(bd.y1 - bd.y0),
    fill: { color: bd.fill }, line: { color: bd.border, width: bd.bw },
  });
}
// slope band: pale-green label cell + salmon data area + green border
slide.addShape(pptx.ShapeType.rect, {
  x: px(87), y: px(459), w: px(56), h: px(20),
  fill: { color: "E9FFD4" }, line: { color: "2E7D32", width: 1.5 },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(143), y: px(459), w: px(724), h: px(20),
  fill: { color: "DEAC95" }, line: { color: "2E7D32", width: 1.5 },
});
// yellow slope cells (0.3) at cols 14 and 16
for (const ci of [14, 16]) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(XSEP[ci]), y: px(460), w: px(XSEP[ci + 1] - XSEP[ci]), h: px(18),
    fill: { color: "F5FB9C" }, line: { color: "2E7D32", width: 0.75 },
  });
}
// next x band: pink with red border
slide.addShape(pptx.ShapeType.rect, {
  x: px(87), y: px(483), w: px(781), h: px(20),
  fill: { color: "F7BEC4" }, line: { color: "C00000", width: 1.5 },
});
// cyan insert over band1 cols 13-15 with the maroon dashed border
slide.addShape(pptx.ShapeType.rect, {
  x: px(666), y: px(332), w: px(121), h: px(36),
  fill: { color: "8BF8AB" }, line: { color: "8B0000", width: 1.25, dashType: "dash" },
});

// thin white separators between cells
for (const bd of [[331, 369], [374, 411], [417, 455], [459, 479], [483, 503]]) {
  for (const sx of XSEP) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(sx), y: px(bd[0] + 1), w: 0, h: px(bd[1] - bd[0] - 2),
      line: { color: "FFFFFF", width: 0.5 },
    });
  }
}
// thin white separators between the two text rows of each 2-row band
for (const hy of [350, 392.5, 436]) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(88), y: px(hy), w: px(780), h: 0,
    line: { color: "FFFFFF", width: 0.5 },
  });
}

// ---- table content: 8 rows x 18 columns (frame-verified values) ----
const rows = [
  { label: "x", vals: ["-11", "-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6", "-9.7", "-9.6", "-9.7"] },
  { label: "f(x)", vals: ["1.15", "-0.04", "-1.19", "-2.26", "-3.27", "-4.19", "-5.03", "-5.77", "-6.41", "-6.95", "-7.39", "-7.72", "-7.96", "-8.08", "-8.11", "-8.08", "-8.11", "-8.08"] },
  { label: "x-delta", vals: ["-11.1", "-11", "-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.8", "-9.7", "-9.8"] },
  { label: "f(x-delta)", vals: ["2.39", "1.15", "-0.04", "-1.19", "-2.26", "-3.27", "-4.19", "-5.03", "-5.77", "-6.41", "-6.95", "-7.39", "-7.72", "-7.96", "-8.08", "-7.96", "-8.08", "-7.96"] },
  { label: "x+delta", vals: ["-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6", "-9.5", "-9.6", "-9.5", "-9.6"] },
  { label: "f(x+delta)", vals: ["-0.04", "-1.19", "-2.26", "-3.27", "-4.19", "-5.03", "-5.77", "-6.41", "-6.95", "-7.39", "-7.72", "-7.96", "-8.08", "-8.11", "-8.05", "-8.11", "-8.05", "-8.11"] },
  { label: "slope", vals: ["-24.3", "-23.4", "-22.2", "-20.8", "-19.3", "-17.6", "-15.8", "-13.8", "-11.8", "-9.8", "-7.7", "-5.7", "-3.6", "-1.5", "0.3", "-1.5", "0.3", "-1.5"] },
  { label: "next x", vals: ["-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6", "-9.7", "-9.6", "-9.7", "-9.6"] },
];
const row_ys = [341, 359, 383, 401, 427, 445, 469, 493];
for (let ri = 0; ri < rows.length; ri++) {
  const ymid = row_ys[ri];
  slide.addText(rows[ri].label, {
    x: px(88), y: px(ymid - 7), w: px(53), h: px(14),
    align: "right", valign: "middle", margin: 0,
    fontFace: A, fontSize: 8, bold: true, color: "000000",
  });
  for (let ci = 0; ci < 18; ci++) {
    const inCyan = (ri < 2 && ci >= 13 && ci <= 15);
    slide.addText(rows[ri].vals[ci], {
      x: px(XSEP[ci]), y: px(ymid - 7), w: px(XSEP[ci + 1] - XSEP[ci]), h: px(14),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 8, bold: true,
      color: inCyan ? "006400" : "000000",
    });
  }
}

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch(err => {
  console.error("ERROR:", err);
});
