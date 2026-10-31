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
  { c: 1, r: 0, t: "FN", fill: "FFFFFF", tc: DARK },
  { c: 0, r: 1, t: "FP", fill: "FFFFFF", tc: DARK },
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
  x: 78 / 72, y: smGridY, w: 10 / 72, h: smCellH * 2,
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

// ---- Big numeric matrix below (grid x93..229 y158..222 px) ----
const bmX = 93 / 72, bmW = 136 / 72;
const bmGridY = 158 / 72, bmGridH = 64 / 72;
const bmCellW = bmW / 2, bmCellH = bmGridH / 2;
s.addText("Predicted as", {
  x: bmX + 12 / 72, y: 138 / 72, w: bmW - 12 / 72, h: 9 / 72,
  fontSize: 8, bold: true, color: RED_T, fontFace: FONT, align: "center", margin: 0,
});
s.addText("P", { x: bmX, y: 147 / 72, w: bmCellW, h: 10 / 72, fontSize: 10, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: bmX + bmCellW, y: 147 / 72, w: bmCellW, h: 10 / 72, fontSize: 10, bold: true, color: RED_T, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", {
  x: bmX - 26 / 72, y: bmGridY, w: 10 / 72, h: bmGridH,
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
s.addText("Test Sample", {
  x: 340 / 72, y: 106 / 72, w: 66 / 72, h: 12 / 72,
  fontSize: 9, bold: true, color: "000000", fontFace: FONT, align: "center", margin: 0,
});
function drawSketch(cx, cy, w) {
  const h = w * 0.40;
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: cx - w / 2, y: cy - h * 0.10, w: w, h: h * 0.20,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 }, adjustValue: 0.5,
  });
  s.addShape(pptx.shapes.OVAL, {
    x: cx + w / 2 - h * 0.24, y: cy - h * 0.11, w: h * 0.24, h: h * 0.22,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 },
  });
  s.addShape(pptx.shapes.LINE, { x: cx + w / 2 + 0.02, y: cy - h * 0.32, w: 0, h: h * 0.64, line: { color: GRAY, width: 1.5 } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w * 0.08, y: cy + h * 0.05, w: w * 0.22, h: h * 0.45,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 }, rotate: 205,
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w * 0.08, y: cy - h * 0.50, w: w * 0.22, h: h * 0.45,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 }, rotate: 155,
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w / 2, y: cy - h * 0.30, w: w * 0.12, h: h * 0.30,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 }, rotate: 270,
  });
}
// enclosing image box around the test-sample sketch (x340..404 y124..180 px)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 340 / 72, y: 124 / 72, w: 64 / 72, h: 56 / 72,
  fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1 },
});
drawSketch(372 / 72, 152 / 72, 52 / 72);

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
  x: mdX, y: mdY + 4 / 72, w: mdW - 30 / 72, h: 20 / 72,
  fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addText("[Any value] \u2192 (0, +1)", {
  x: mdX, y: mdY + mdH - 18 / 72, w: mdW, h: 16 / 72,
  fontSize: 7, bold: true, color: "FFE14D", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
// lavender circle with purple wedge (pie-chart icon) inside Model box right side
const pieX = 552 / 72, pieY = 146 / 72, pieD = 28 / 72;
s.addShape(pptx.shapes.OVAL, { x: pieX, y: pieY, w: pieD, h: pieD, fill: { color: "D9B8E6" }, line: { color: PURPLE, width: 1 } });
s.addShape(pptx.shapes.PIE, { x: pieX, y: pieY, w: pieD, h: pieD, fill: { color: PURPLE }, line: { type: "none" }, angleRange: [180, 270] });

// arrow TestSample -> Model ; Model -> blue box
arrow(400 / 72, fy, 449 / 72, fy);
arrow(568 / 72, fy, 610 / 72, fy);

// --- "Predicted Value" label above blue box (x570..621 y106..113) ---
s.addText("Predicted Value", {
  x: 566 / 72, y: 104 / 72, w: 60 / 72, h: 10 / 72,
  fontSize: 8, bold: true, color: "000000", fontFace: FONT, align: "center", margin: 0,
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
arrow(668 / 72, fy, 682 / 72, fy);

// --- Threshold box (x682..730 y110..184 px, red border, beige fill, vertical text) ---
const thX = 682 / 72, thY = 110 / 72, thW = 48 / 72, thH = 74 / 72;
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: thX, y: thY, w: thW, h: thH, adjustValue: 0.2,
  fill: { color: BEIGE }, line: { color: RED_T, width: 1.25 },
});
s.addText("Threshold (e.g. 0.5)", {
  x: thX + thW / 2 - 8 / 72, y: thY + 2 / 72, w: 16 / 72, h: thH - 4 / 72,
  fontSize: 7, bold: true, color: RED_T, fontFace: FONT,
  align: "center", valign: "middle", margin: 0, rotate: 270,
});

// --- fork arrows to Class I / Class II (red diagonals) ---
arrow(730 / 72, 132 / 72, 746 / 72, 124 / 72);
arrow(730 / 72, 168 / 72, 746 / 72, 176 / 72);

// --- Class I (light green) / Class II (pink) ovals ---
s.addShape(pptx.shapes.OVAL, {
  x: 748 / 72, y: 110 / 72, w: 66 / 72, h: 30 / 72,
  fill: { color: "C8E6C9" }, line: { color: "2E7D32", width: 1 },
});
s.addText("Class I", {
  x: 748 / 72, y: 110 / 72, w: 66 / 72, h: 30 / 72,
  fontSize: 10, bold: true, color: "000000", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 748 / 72, y: 156 / 72, w: 66 / 72, h: 30 / 72,
  fill: { color: "F4A6D0" }, line: { color: "C2185B", width: 1 },
});
s.addText("Class II", {
  x: 748 / 72, y: 156 / 72, w: 66 / 72, h: 30 / 72,
  fontSize: 10, bold: true, color: "000000", fontFace: FONT, align: "center", valign: "middle", margin: 0,
});

// ================= PLOT: airplanes, dashed line, axis =================
// 11 hand-drawn airplanes, each ~100px wide, with nose dot (red/blue)
const planes = [
  { x: 108, y: 229, w: 110, h: 63, dot: "R", dx: 129, dy: 248 },
  { x: 192, y: 281, w: 110, h: 54, dot: "R", dx: 282, dy: 296 },
  { x: 88, y: 319, w: 112, h: 56, dot: "R", dx: 110, dy: 341 },
  { x: 206, y: 346, w: 89, h: 64, dot: "R", dx: 222, dy: 372 },
  { x: 330, y: 217, w: 101, h: 63, dot: "B", dx: 347, dy: 229 },
  { x: 347, y: 286, w: 108, h: 86, dot: "R", dx: 376, dy: 302 },
  { x: 480, y: 283, w: 111, h: 63, dot: "R", dx: 572, dy: 299 },
  { x: 628, y: 299, w: 142, h: 52, dot: "B", dx: 652, dy: 311 },
  { x: 765, y: 227, w: 92, h: 67, dot: "B", dx: 775, dy: 265 },
  { x: 775, y: 347, w: 95, h: 50, dot: "B", dx: 854, dy: 356 },
  { x: 498, y: 363, w: 111, h: 48, dot: "B", dx: 517, dy: 376 },
];
function drawPlane(px, py, pw, ph, dotColor, dotX, dotY) {
  const cx = (px + pw / 2) / 72, cy = (py + ph / 2) / 72, w = pw / 72;
  const h = ph / 72;
  // fuselage
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: cx - w / 2, y: cy - h * 0.10, w: w, h: h * 0.20,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, adjustValue: 0.5,
  });
  // nose
  s.addShape(pptx.shapes.OVAL, {
    x: cx + w / 2 - h * 0.24, y: cy - h * 0.11, w: h * 0.24, h: h * 0.22,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 },
  });
  // propeller
  s.addShape(pptx.shapes.LINE, { x: cx + w / 2 + 0.02, y: cy - h * 0.32, w: 0, h: h * 0.64, line: { color: GRAY, width: 1.75 } });
  // main wings
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w * 0.08, y: cy + h * 0.05, w: w * 0.22, h: h * 0.45,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, rotate: 205,
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w * 0.08, y: cy - h * 0.50, w: w * 0.22, h: h * 0.45,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, rotate: 155,
  });
  // tail
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w / 2, y: cy - h * 0.30, w: w * 0.12, h: h * 0.30,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, rotate: 270,
  });
  // class dot
  s.addShape(pptx.shapes.OVAL, {
    x: dotX / 72 - 3.5 / 72, y: dotY / 72 - 3.5 / 72, w: 7 / 72, h: 7 / 72,
    fill: { color: dotColor === "R" ? "C00000" : "0000CD" }, line: { type: "none" },
  });
}
for (const p of planes) drawPlane(p.x, p.y, p.w, p.h, p.dot, p.dx, p.dy);

// dashed vertical threshold line at x=320px, y204..432px (stops at the axis)
const dashX = 320 / 72;
for (let y = 204; y <= 430; y += 10) {
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
// small marker where dashed line meets axis (x317..327 y438..449)
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: 317 / 72, y: 438 / 72, w: 9 / 72, h: 10 / 72, fill: { color: "8A93A8" }, line: { type: "none" }, rotate: 180 });
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
