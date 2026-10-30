// slide_009.js — "Precision" rebuild from fresh image-analysis of slide_009.jpg (960x540, 1px=1pt)
const pptxgenpkg = require("pptxgenjs");
const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const BLUE = "2E75B6", DBLUE = "1F4E79", LBLUE = "0070C0", GREEN = "00B050", LGREEN = "92D050";
const FONT = "Arial";
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE CHROME (root AGENTS.md 2026-10-09 — overrides everything)
s.addShape(pptx.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { color: BG }, line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 } });
s.addText("9", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0 });
s.addText("Precision", { x: 0.6, y: 0.28, w: 12.13, h: 0.8, align: "center", valign: "middle", fontSize: 40, bold: true, color: RED, fontFace: FONT, margin: 0 });

// ===== LEFT COLUMN =====
// 1. Gray definition band (px x71-655 y112-175) with red rule (y139-142, x81-645)
s.addShape(pptx.shapes.RECTANGLE, { x: 71/72, y: 112/72, w: (655-71)/72, h: (175-112)/72, fill: { color: "CFCFCF" }, line: { color: "A6A6A6", width: 0.75 } });
s.addText("Correctly Classified (as Positive)", { x: 71/72, y: 116/72, w: (655-71)/72, h: 22/72, align: "center", valign: "middle", fontSize: 14, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: 81/72, y: 139/72, w: (645-81)/72, h: 3/72, fill: { color: RED }, line: { type: "none" } });
s.addText("Total Classified as Positive (either Correct and Erroneous)", { x: 71/72, y: 144/72, w: (655-71)/72, h: 28/72, align: "center", valign: "middle", fontSize: 14, bold: true, color: TEXT, fontFace: FONT, margin: 0 });

// 2. Meaning box (pale yellow, px x71-624 y200-257)
s.addShape(pptx.shapes.RECTANGLE, { x: 71/72, y: 200/72, w: (624-71)/72, h: (257-200)/72, fill: { color: "FFFBD7" }, line: { color: "BFBF8F", width: 0.75 } });
s.addText("Meaning", { x: 80/72, y: 204/72, w: 90/72, h: 22/72, fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0, valign: "middle" });
s.addText([
  { text: "% of what you " },
  { text: "Predicted", options: { bold: true, color: RED, underline: true } },
  { text: " as " },
  { text: "POSITIVE", options: { bold: true, color: LBLUE } },
  { text: " is Actually Positive" },
], { x: 74/72, y: 228/72, w: (620-74)/72, h: 26/72, fontSize: 15, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });

// 3. Formula box (white, red border, px x68-317 y262-321)
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 68/72, y: 262/72, w: (317-68)/72, h: (321-262)/72, fill: { color: "FFFFFF" }, line: { color: RED, width: 2 } });
s.addText("Precision =", { x: 76/72, y: 280/72, w: 130/72, h: 32/72, fontSize: 20, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });
// stacked fraction TP/(TP+FP) as 600dpi mathtext PNG at exact size
s.addImage({ path: NS + "/recreated_pptx/build/assets/eq_009_precision.png", x: 2.55, y: 3.66, w: 0.8, h: 0.395 });

// 4. Worked-example box (light blue, px x335-527 y291-336)
s.addShape(pptx.shapes.RECTANGLE, { x: 335/72, y: 291/72, w: (527-335)/72, h: (336-291)/72, fill: { color: "DEEAF6" }, line: { color: BLUE, width: 1 } });
s.addText("Precision= 5/(5+0)", { x: 335/72, y: 293/72, w: (527-335)/72, h: 20/72, align: "center", valign: "middle", fontSize: 13, bold: true, color: LBLUE, fontFace: FONT, margin: 0 });
s.addText("= 100%", { x: 335/72, y: 314/72, w: (527-335)/72, h: 20/72, align: "center", valign: "middle", fontSize: 13, bold: true, color: LBLUE, fontFace: FONT, margin: 0 });

// 5. Callout tags under the formula (px tag1 x117-209 y325-373, tag2 x225-317 y323-372)
function callout(x, y, w, h, fill, line, l1, l2) {
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: x, y: y, w: w, h: h, fill: { color: fill }, line: { color: line, width: 1 } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x + w/2 - 0.07, y: y - 0.11, w: 0.14, h: 0.11, fill: { color: fill }, line: { color: line, width: 1 }, rotate: 180 });
  s.addText(l1, { x: x, y: y + 0.06, w: w, h: 0.24, align: "center", fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
  s.addText(l2, { x: x, y: y + 0.30, w: w, h: 0.24, align: "center", fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
}
callout(117/72, 325/72, (209-117)/72, (373-325)/72, "FFF2CC", "FFD966", "Positive", "Classified as +ve");
callout(225/72, 323/72, (317-225)/72, (372-323)/72, "FCE4D6", "F4B183", "Negative", "Classified as +ve");

// 6. Green brace line (px y391-395 x107-333) + end ticks
s.addShape(pptx.shapes.LINE, { x: 107/72, y: 392/72, w: (333-107)/72, h: 0, line: { color: GREEN, width: 2.5 } });
s.addShape(pptx.shapes.LINE, { x: 107/72, y: 385/72, w: 0, h: 10/72, line: { color: GREEN, width: 2.5 } });
s.addShape(pptx.shapes.LINE, { x: 333/72, y: 385/72, w: 0, h: 10/72, line: { color: GREEN, width: 2.5 } });

// 7. Red italic caption (px y413-427 x80-308)
s.addText("All Samples classified as Positive", { x: 80/72, y: 412/72, w: (308-80)/72, h: 16/72, fontSize: 13, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0, valign: "middle" });

// 8. Blue takeaway box (px x64-524 y439-500)
s.addShape(pptx.shapes.RECTANGLE, { x: 64/72, y: 439/72, w: (524-64)/72, h: (500-439)/72, fill: { color: "E4EDFD" }, line: { color: BLUE, width: 1.5 } });
s.addText("Whatever objects you retrieved as positive, I can trust you", { x: 72/72, y: 452/72, w: (493-72)/72, h: 16/72, fontSize: 13, bold: true, italic: true, color: DBLUE, fontFace: FONT, margin: 0, valign: "middle" });
s.addText("(Irrespective of how many MISSED Positive samples)", { x: 78/72, y: 479/72, w: (447-78)/72, h: 13/72, fontSize: 11, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0, valign: "middle" });

// ===== RIGHT: confusion matrices =====
function matrix(x, y, w, h) {
  // outer blue frame; header band; 2x2 grid with label col
  const lx = x, lw = 65/72;          // row-label col
  const gx = x + lw, gw = w - lw;     // grid width
  const hh = 0.30;                    // "Predicted as" header height
  const chh = 0.30;                   // P/N col-header height
  const rh = (h - hh - chh) / 2;
  s.addShape(pptx.shapes.RECTANGLE, { x: x, y: y, w: w, h: h, fill: { color: "FFFFFF" }, line: { color: "2E5C8A", width: 1.5 } });
  s.addText("Predicted as", { x: gx, y: y + 0.02, w: gw, h: hh, align: "center", valign: "middle", fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0 });
  s.addText("P", { x: gx, y: y + hh, w: gw/2, h: chh, align: "center", valign: "middle", fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
  s.addText("N", { x: gx + gw/2, y: y + hh, w: gw/2, h: chh, align: "center", valign: "middle", fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
  s.addText("Actual", { x: x + 0.02, y: y + hh + 0.05, w: 0.22, h: rh*2, align: "center", valign: "middle", fontSize: 9, bold: true, color: RED, fontFace: FONT, margin: 0, rotate: 270 });
  s.addText("P", { x: x, y: y + hh + chh, w: lw, h: rh, align: "center", valign: "middle", fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0 });
  s.addText("N", { x: x, y: y + hh + chh + rh, w: lw, h: rh, align: "center", valign: "middle", fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0 });
  // grid lines
  s.addShape(pptx.shapes.LINE, { x: lx, y: y + hh, w: w - lw, h: 0, line: { color: "E0A0A0", width: 0.75 } });
  s.addShape(pptx.shapes.LINE, { x: lx, y: y + hh + chh, w: w - lw, h: 0, line: { color: "E0A0A0", width: 0.75 } });
  s.addShape(pptx.shapes.LINE, { x: gx + gw/2, y: y + hh, w: 0, h: h - hh, line: { color: "E0A0A0", width: 0.75 } });
  s.addShape(pptx.shapes.LINE, { x: lx, y: y + hh + chh + rh, w: w - lw, h: 0, line: { color: "E0A0A0", width: 0.75 } });
  return { gx, gw, gy: y + hh + chh, rh, cw: gw/2 };
}
function cell(g, cx, cy, fill, label, txtColor) {
  s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: g.cw, h: g.rh, fill: { color: fill }, line: { color: "E0A0A0", width: 0.75 } });
  s.addText(label, { x: cx, y: cy, w: g.cw, h: g.rh, align: "center", valign: "middle", fontSize: 14, bold: true, color: txtColor, fontFace: FONT, margin: 0 });
}
// Matrix 1 — symbolic (px x672-867 y43-158)
const m1 = matrix(672/72, 43/72, (867-672)/72, (158-43)/72);
cell(m1, m1.gx, m1.gy, LGREEN, "TP", "FFFFFF");
cell(m1, m1.gx + m1.cw, m1.gy, "FFFFFF", "FN", TEXT);
cell(m1, m1.gx, m1.gy + m1.rh, "FFFFFF", "FP", TEXT);
cell(m1, m1.gx + m1.cw, m1.gy + m1.rh, LGREEN, "TN", "FFFFFF");

// Matrix 2 — numeric (px x673-867 y168-288); 5 has dark-blue circle badge, 0 pale orange, 70 green
const m2 = matrix(673/72, 168/72, (867-673)/72, (288-168)/72);
cell(m2, m2.gx, m2.gy, "FFFFFF", "", TEXT);
s.addShape(pptx.shapes.OVAL, { x: m2.gx + m2.cw/2 - 0.16, y: m2.gy + m2.rh/2 - 0.16, w: 0.32, h: 0.32, fill: { color: "1A1499" }, line: { color: "1A1499", width: 1 } });
s.addText("5", { x: m2.gx, y: m2.gy, w: m2.cw, h: m2.rh, align: "center", valign: "middle", fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });
cell(m2, m2.gx + m2.cw, m2.gy, "FFFFFF", "25", TEXT);
cell(m2, m2.gx, m2.gy + m2.rh, "FCE4D6", "0", TEXT);
cell(m2, m2.gx + m2.cw, m2.gy + m2.rh, LGREEN, "70", "FFFFFF");

// ===== TREE PANEL (red frame, px x535-882 y291-503) =====
const pX = 535/72, pY = 291/72, pW = (882-535)/72, pH = (503-291)/72;
s.addShape(pptx.shapes.RECTANGLE, { x: pX, y: pY, w: pW, h: pH, fill: { color: BG }, line: { color: RED, width: 1.5 } });
s.addText("Positive", { x: 596/72, y: 298/72, w: (668-596)/72, h: 16/72, align: "center", fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0 });
s.addText("Negative", { x: 774/72, y: 298/72, w: (852-774)/72, h: 16/72, align: "center", fontSize: 15, bold: true, color: GREEN, fontFace: FONT, margin: 0 });

// light-gray fish sketches (px left (589,323)-(672,376), right (765,325)-(852,366))
function fish(cx, cy, w, h) {
  s.addShape(pptx.shapes.OVAL, { x: cx, y: cy, w: w, h: h, line: { color: "BFBFBF", width: 1.25 } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: cx - w*0.22, y: cy + h*0.15, w: w*0.24, h: h*0.7, line: { color: "BFBFBF", width: 1.25 }, rotate: 270 });
  s.addShape(pptx.shapes.OVAL, { x: cx + w*0.72, y: cy + h*0.32, w: 0.05, h: 0.05, fill: { color: "BFBFBF" }, line: { type: "none" } });
}
fish(589/72, 323/72, (672-589)/72, (376-323)/72);
fish(765/72, 325/72, (852-765)/72, (366-325)/72);

function node(cx, cy, r, fill, label) {
  s.addShape(pptx.shapes.OVAL, { x: cx - r, y: cy - r, w: 2*r, h: 2*r, fill: { color: fill }, line: { color: fill, width: 1 } });
  s.addText(label, { x: cx - r, y: cy - r, w: 2*r, h: 2*r, align: "center", valign: "middle", fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });
}
function branch(x0, y0, x1, y1) {
  s.addShape(pptx.shapes.LINE, { x: x0, y: y0, w: x1 - x0, h: y1 - y0, line: { color: "5B53A1", width: 1.75 } });
  // small triangle head at (x1,y1) pointing along direction
  const ang = Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI;
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x1 - 0.07, y: y1 - 0.07, w: 0.14, h: 0.14, fill: { color: "5B53A1" }, line: { type: "none" }, rotate: ang + 90 });
}
// left tree: 30 -> 5 (TP), 25 (FN)
const r1x = 618/72, r1y = 393/72, r = 0.22;
node(r1x, r1y, r, "C00000", "30");
const l1x = 573/72, l1y = 457/72, l2x = 661/72, l2y = 457/72;
branch(r1x - 0.12, r1y + 0.18, l1x, l1y - r);
branch(r1x + 0.12, r1y + 0.18, l2x, l2y - r);
node(l1x, l1y, r, "C00000", "5");
node(l2x, l2y, r, "009245", "25");
s.addText("TP", { x: l1x - 0.2, y: 482/72, w: 0.4, h: 10/72, align: "center", fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0 });
s.addText("FN", { x: l2x - 0.2, y: 482/72, w: 0.4, h: 10/72, align: "center", fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0 });
// right tree: 70 -> 70 (TN), 0 (FP)
const r2x = 800/72, r2y = 393/72;
node(r2x, r2y, r, "009245", "70");
const l3x = 754/72, l3y = 457/72, l4x = 845/72, l4y = 457/72;
branch(r2x - 0.12, r2y + 0.18, l3x, l3y - r);
branch(r2x + 0.12, r2y + 0.18, l4x, l4y - r);
node(l3x, l3y, r, "009245", "70");
node(l4x, l4y, r, "C00000", "0");
s.addText("TN", { x: l3x - 0.2, y: 482/72, w: 0.4, h: 10/72, align: "center", fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0 });
s.addText("FP", { x: l4x - 0.2, y: 482/72, w: 0.4, h: 10/72, align: "center", fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0 });

// red curved emphasis arrows at panel edges (px (545,397)-(565,428) and (855,398)-(875,429))
s.addShape(pptx.shapes.LINE, { x: 548/72, y: 400/72, w: 12/72, h: 24/72, line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: 548/72 + 3/72, y: 424/72, w: 0.12, h: 0.12, fill: { color: RED }, line: { type: "none" }, rotate: 180 - 20 });
s.addShape(pptx.shapes.LINE, { x: 858/72, y: 400/72, w: 12/72, h: 24/72, line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: 862/72, y: 424/72, w: 0.12, h: 0.12, fill: { color: RED }, line: { type: "none" }, rotate: 180 + 20 });

const outFile = NS + "/recreated_pptx/slide_009_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done", outFile));
