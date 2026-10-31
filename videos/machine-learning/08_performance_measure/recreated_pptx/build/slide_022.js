const pptxgen = require("pptxgenjs");

// Slide 22 — Effect of Selecting Threshold Value on Model Performance
// Geometry measured from unique_slides/slide_022.jpg (960x540; inches = px/72).
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const W = 13.33, H = 7.5;
const BG = "E8E8E8";
const RED = "C00000";        // house frame / red annotation layer
const DARKRED = "9D0000";    // model box fill (measured 157,0,0)
const YELLOW = "FFF9C4";     // house badge
const DARK = "333333";
const FONT = "Arial";
const BLUE_T = "0000FF";     // correct-value blue in matrix
const RED_T = "C00000";      // error-value red in matrix
const GREEN = "CDE9CD";      // TP/TN cell tint (measured pale green)
const PANEL = "FAFEE3";      // flowchart panel fill (measured 250,254,227)
const BEIGE = "F5E9C8";      // threshold=0.3 box fill
const PEACH = "FFD9C0";      // class ovals (measured ~255,220,200)
const NAVY = "222E68";       // blue range box (measured ~34,46,104)
const GRAY = "404040";       // airplane line art
const BLUELINE = "1E88E5";   // dashed threshold line
const PURPLE = "B883C7";     // pie icon in Model box

let s = pptx.addSlide();
s.background = { color: BG };

// ================= HOUSE CHROME (root AGENTS.md 2026-10-09) =================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("22", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  align: "center", valign: "middle",
  fontSize: 26, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ================= LEFT BLOCK =================
// Small annotation matrix (TP/FN/FP/TN): grid x106..168 y110..138 px
const smCellW = 31 / 72, smCellH = 14 / 72;
const smGridX = 106 / 72, smGridY = 110 / 72;

s.addText("Predicted as", {
  x: smGridX, y: 96 / 72, w: smCellW * 2, h: 8 / 72,
  fontSize: 8, bold: true, color: RED_T, fontFace: FONT, align: "center", margin: 0,
});
s.addText("P", { x: smGridX, y: 104 / 72, w: smCellW, h: 6 / 72, fontSize: 8, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: smGridX + smCellW, y: 104 / 72, w: smCellW, h: 6 / 72, fontSize: 8, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
const cells = [
  { c: 0, r: 0, t: "TP", fill: GREEN, tc: DARK },
  { c: 1, r: 0, t: "FN", fill: "F6D5D5", tc: DARK },
  { c: 0, r: 1, t: "FP", fill: "F6D5D5", tc: DARK },
  { c: 1, r: 1, t: "TN", fill: GREEN, tc: DARK },
];
for (const cell of cells) {
  const cx = smGridX + cell.c * smCellW, cy = smGridY + cell.r * smCellH;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: cx, y: cy, w: smCellW, h: smCellH,
    fill: { color: cell.fill }, line: { color: RED_T, width: 0.75 },
  });
  s.addText(cell.t, {
    x: cx, y: cy, w: smCellW, h: smCellH,
    fontSize: 8, bold: true, color: cell.tc, fontFace: FONT,
    align: "center", valign: "middle", margin: 0,
  });
}
s.addText("P", { x: 92 / 72, y: smGridY, w: 12 / 72, h: smCellH, fontSize: 8, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: 92 / 72, y: smGridY + smCellH, w: 12 / 72, h: smCellH, fontSize: 8, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", {
  x: 68 / 72, y: 119 / 72, w: 30 / 72, h: 10 / 72,
  fontSize: 8, bold: true, color: RED_T, fontFace: FONT,
  align: "center", valign: "middle", margin: 0, rotate: 270,
});

// ---- Threshold=0.3 box: right of small matrix, same band (x182..309 y109..135 px) ----
const tbX = 182 / 72, tbY = 109 / 72, tbW = 127 / 72, tbH = 26 / 72;
s.addShape(pptx.shapes.RECTANGLE, {
  x: tbX, y: tbY, w: tbW, h: tbH,
  fill: { color: BEIGE }, line: { color: RED_T, width: 1.25 },
});
s.addText("Threshold=0.3", {
  x: tbX, y: tbY, w: tbW, h: tbH,
  fontSize: 12, bold: true, color: RED_T, fontFace: FONT,
  align: "center", valign: "middle", margin: 0,
});

// ---- Big numeric matrix below (left edge aligned with small matrix, x106..242 y158..222 px) ----
const bmX = 106 / 72, bmW = 136 / 72;
const bmGridY = 158 / 72, bmGridH = 64 / 72;
const bmCellW = bmW / 2, bmCellH = bmGridH / 2;
s.addText("Predicted as", {
  x: bmX + 12 / 72, y: 138 / 72, w: bmW - 12 / 72, h: 9 / 72,
  fontSize: 8, bold: true, color: RED_T, fontFace: FONT, align: "center", margin: 0,
});
s.addText("P", { x: bmX, y: 147 / 72, w: bmCellW, h: 10 / 72, fontSize: 10, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: bmX + bmCellW, y: 147 / 72, w: bmCellW, h: 10 / 72, fontSize: 10, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", {
  x: 61 / 72, y: 185 / 72, w: 40 / 72, h: 10 / 72,
  fontSize: 8, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270,
});
s.addText("P", { x: bmX - 14 / 72, y: bmGridY, w: 12 / 72, h: bmCellH, fontSize: 10, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: bmX - 14 / 72, y: bmGridY + bmCellH, w: 12 / 72, h: bmCellH, fontSize: 10, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
const vals = [
  { c: 0, r: 0, t: "5", tc: BLUE_T },
  { c: 1, r: 0, t: "0", tc: RED_T },
  { c: 0, r: 1, t: "2", tc: RED_T },
  { c: 1, r: 1, t: "4", tc: BLUE_T },
];
for (const v of vals) {
  const cx = bmX + v.c * bmCellW, cy = bmGridY + v.r * bmCellH;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: cx, y: cy, w: bmCellW, h: bmCellH,
    fill: { color: "FFFFFF" }, line: { color: RED_T, width: 0.75 },
  });
  s.addText(v.t, {
    x: cx, y: cy, w: bmCellW, h: bmCellH,
    fontSize: 14, bold: true, color: v.tc, fontFace: FONT,
    align: "center", valign: "middle", margin: 0,
  });
}

// ================= FLOWCHART PANEL (x327..841 y100..196 px) =================
const pnX = 327 / 72, pnY = 100 / 72, pnW = (841 - 327) / 72, pnH = (196 - 100) / 72;
s.addShape(pptx.shapes.RECTANGLE, {
  x: pnX, y: pnY, w: pnW, h: pnH,
  fill: { color: PANEL }, line: { color: "5A4A2A", width: 1 },
});

const fy = 150 / 72; // main pipeline vertical center (px 150)

// --- Test Sample: label + small airplane sketch (x340..400 y110..180 px) ---
s.addText("Test\nSample", {
  x: 340 / 72, y: 100 / 72, w: 66 / 72, h: 24 / 72,
  fontSize: 10, bold: true, color: "000000", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
// enclosing image box around the test sample + the original's own thumbnail pixels
s.addShape(pptx.shapes.RECTANGLE, {
  x: 340 / 72, y: 124 / 72, w: 64 / 72, h: 56 / 72,
  fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1 },
});
s.addImage({
  path: "recreated_pptx/build/assets/s22/test_sample.png",
  x: 342 / 72, y: 126 / 72, w: 60 / 72, h: 52 / 72,
});

// arrow helper: hollow white shaft + red outline + red triangle head
function arrow(x0, y0, x1, y1) {
  const horizontal = Math.abs(y1 - y0) < 0.01;
  if (horizontal) {
    const w = x1 - x0;
    s.addShape(pptx.shapes.RECTANGLE, {
      x: x0, y: y0 - 0.025, w: w - 0.10, h: 0.05,
      fill: { color: "FFFFFF" }, line: { color: RED_T, width: 1 },
    });
    s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
      x: x1 - 0.10, y: y0 - 0.07, w: 0.10, h: 0.14,
      fill: { color: "FFFFFF" }, line: { color: RED_T, width: 1 }, rotate: 90,
    });
  } else {
    const h = y1 - y0;
    s.addShape(pptx.shapes.LINE, {
      x: x0, y: Math.min(y0, y1), w: x1 - x0, h: Math.abs(h),
      line: { color: RED_T, width: 1.5, endArrowType: "triangle" },
    });
  }
}

// --- Model box (x449..568 y121..178 px, fill #9D0000) ---
const mdX = 449 / 72, mdY = 121 / 72, mdW = 119 / 72, mdH = 57 / 72;
s.addShape(pptx.shapes.RECTANGLE, {
  x: mdX, y: mdY, w: mdW, h: mdH,
  fill: { color: DARKRED }, line: { color: DARKRED, width: 1 },
});
s.addText("Model", {
  x: mdX, y: mdY + 4 / 72, w: mdW - 45 / 72, h: 20 / 72,
  fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addText("[Any value] \u2192 (0, +1)", {
  x: mdX, y: mdY + mdH - 20 / 72, w: mdW, h: 18 / 72,
  fontSize: 8, bold: true, color: "FFE14D", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
// white dial with pink wedge and radial line, fully inside Model box right side
const pieX = 534 / 72, pieY = 132 / 72, pieD = 24 / 72;
s.addShape(pptx.shapes.OVAL, { x: pieX, y: pieY, w: pieD, h: pieD, fill: { color: "FFFFFF" }, line: { color: PURPLE, width: 1 } });
s.addShape(pptx.shapes.PIE, { x: pieX, y: pieY, w: pieD, h: pieD, fill: { color: "F4A6D0" }, line: { type: "none" }, angleRange: [180, 270] });
s.addShape(pptx.shapes.LINE, { x: pieX + pieD / 2, y: pieY, w: 0, h: pieD / 2, line: { color: PURPLE, width: 1 } });

// arrow TestSample -> Model ; Model -> blue box
arrow(400 / 72, fy, 449 / 72, fy);
arrow(568 / 72, fy, 610 / 72, fy);

// --- "Predicted Value" label above blue box (x570..621 y106..113) ---
s.addText("Predicted\nValue", {
  x: 558 / 72, y: 100 / 72, w: 74 / 72, h: 26 / 72,
  fontSize: 9, bold: true, color: "000000", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
// --- predicted-value range box: white fill, blue outline, dark text (x610..668 y130..168 px) ---
const bbX = 610 / 72, bbY = 130 / 72, bbW = 58 / 72, bbH = 38 / 72;
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: bbX, y: bbY, w: bbW, h: bbH, adjustValue: 0.25,
  fill: { color: "FFFFFF" }, line: { color: "1565C0", width: 1.5 },
});
s.addText("(0 --- 1)", {
  x: bbX, y: bbY, w: bbW, h: bbH,
  fontSize: 9, bold: true, color: "1565C0", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});

// arrow blue box -> threshold box
arrow(668 / 72, fy, 680 / 72, fy);

// --- Threshold box (x680..734 y110..184 px, red border, beige fill, vertical text) ---
const thX = 680 / 72, thY = 110 / 72, thW = 54 / 72, thH = 74 / 72;
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: thX, y: thY, w: thW, h: thH, adjustValue: 0.2,
  fill: { color: BEIGE }, line: { color: RED_T, width: 1.25 },
});
s.addText("Threshold\n(e.g. 0.5)", {
  x: thX, y: thY + 12 / 72, w: thW, h: 50 / 72,
  fontSize: 9, bold: true, color: RED_T, fontFace: FONT,
  align: "center", valign: "middle", margin: 0,
});

// --- fork arrows to Class I / Class II (red diagonals) ---
arrow(734 / 72, 132 / 72, 748 / 72, 124 / 72);
arrow(734 / 72, 168 / 72, 748 / 72, 176 / 72);

// --- Class I (light green) / Class II (pink) ovals ---
s.addShape(pptx.shapes.OVAL, {
  x: 750 / 72, y: 110 / 72, w: 66 / 72, h: 30 / 72,
  fill: { color: "C8E6C9" }, line: { color: "2E7D32", width: 1 },
});
s.addText("Class I", {
  x: 750 / 72, y: 110 / 72, w: 66 / 72, h: 30 / 72,
  fontSize: 11, bold: true, color: "000000", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 750 / 72, y: 156 / 72, w: 66 / 72, h: 30 / 72,
  fill: { color: "F4A6D0" }, line: { color: "C2185B", width: 1 },
});
s.addText("Class II", {
  x: 750 / 72, y: 156 / 72, w: 66 / 72, h: 30 / 72,
  fontSize: 11, bold: true, color: "000000", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});

// ================= PLOT: airplanes (original-frame crops), legend strip, dashed line, axis =================
// legend strip above the plot (x80..890 y194..224 px) — cropped from the original frame
s.addImage({
  path: "recreated_pptx/build/assets/s22/legend_strip.png",
  x: 80 / 72, y: 194 / 72, w: 810 / 72, h: 30 / 72,
});
// 11 hand-drawn airplanes, cropped verbatim from the original frame (transparent PNGs)
const planeMeta = require("./assets/s22/planes_meta.json");
for (const p of planeMeta) {
  s.addImage({
    path: "recreated_pptx/build/assets/s22/" + p.file,
    x: p.x / 72, y: p.y / 72, w: p.w / 72, h: p.h / 72,
  });
}

// dashed vertical threshold line at x=320px, y204..490px (original runs past the axis to y~492)
const dashX = 320 / 72;
for (let y = 204; y <= 488; y += 10) {
  s.addShape(pptx.shapes.LINE, {
    x: dashX, y: y / 72, w: 0, h: 5 / 72,
    line: { color: "8A93A8", width: 1, dashType: "dash" },
  });
}

// ---- x-axis: y=435px, x 87..868, single right arrowhead ----
const axY = 435.5 / 72;
const axL = 87 / 72, axR = 868 / 72;
s.addShape(pptx.shapes.LINE, { x: axL, y: axY, w: axR - axL - 0.11, h: 0, line: { color: RED, width: 2 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: axR - 0.11, y: axY - 0.055, w: 0.11, h: 0.11, fill: { color: RED }, line: { type: "none" }, rotate: 90 });
// 11 ticks at every 0.1
for (let i = 0; i <= 10; i++) {
  const tx = axL + (axR - axL) * (i / 10);
  s.addShape(pptx.shapes.LINE, { x: tx, y: axY + 0.02, w: 0, h: 8 / 72, line: { color: RED, width: 1.5 } });
}
// small red marker where dashed line meets axis (x316..328 y437..450)
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: 316 / 72, y: 437 / 72, w: 12 / 72, h: 13 / 72, fill: { color: RED }, line: { type: "none" }, rotate: 180 });
// tick labels 0.0 / 0.5 / 1.0 at y451..461
const tickLabels = [
  { t: "0.0", x: 87 / 72 },
  { t: "0.5", x: 478 / 72 },
  { t: "1.0", x: 868 / 72 },
];
for (const tl of tickLabels) {
  s.addText(tl.t, {
    x: tl.x - 12 / 72, y: 451 / 72, w: 24 / 72, h: 10 / 72,
    fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", margin: 0,
  });
}

// ---- OUTPUT ----
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_022_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done", outFile));
