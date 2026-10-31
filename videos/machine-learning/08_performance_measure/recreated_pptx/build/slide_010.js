const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", REDLINE = "FF0000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const GREEN = "00B050", LGREEN = "92D050", BLUE = "0070C0", PALE = "EAF3FA", BLUEBORDER = "4472C4";
const DARKBLUE = "1F3864", ORANGE = "F4B183", MATRIXBLUE = "0000FF", ARROW = "0000FF";
const FONT = "Arial";
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE CHROME
s.addShape(pptx.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { color: BG }, line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 } });
s.addText("10", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0 });
s.addText("Recall", { x: 0.6, y: 0.28, w: 12.13, h: 0.5, align: "center", valign: "middle", fontSize: 40, bold: true, color: RED, fontFace: FONT, margin: 0 });

// 1. GRAY DEFINITION BAND (orig x70-657, y46-166 px; top dropped to clear house title box)
s.addShape(pptx.shapes.RECTANGLE, { x: 0.97, y: 0.80, w: 8.15, h: 1.51, fill: { color: "D9D9D9" }, line: { color: "BFBFBF", width: 0.75 } });
s.addText("Correctly Classified (as Positive)", { x: 1.1, y: 1.55, w: 7.9, h: 0.35, fontSize: 15, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center" });
s.addShape(pptx.shapes.LINE, { x: 1.125, y: 1.95, w: 7.83, h: 0, line: { color: RED, width: 2 } });
s.addText("Total objects that should be retrieved (Actually Positive)", { x: 1.1, y: 2.02, w: 7.9, h: 0.28, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center" });

// 2. MEANING PANEL (orig x72-614, y202-255 px)
s.addShape(pptx.shapes.RECTANGLE, { x: 1.0, y: 2.81, w: 7.53, h: 0.74, fill: { color: "FFFFCC" }, line: { color: "D0C000", width: 0.75 } });
s.addText("Meaning", { x: 1.15, y: 2.86, w: 2.0, h: 0.4, fontSize: 20, bold: true, color: RED, fontFace: FONT, margin: 0 });
s.addText([
  { text: "Does the classifier " },
  { text: "miss", options: { color: RED, bold: true, underline: true } },
  { text: " any of " },
  { text: "Positive", options: { color: BLUE, bold: true, underline: true } },
  { text: " Objects ?" }
], { x: 1.15, y: 3.24, w: 7.2, h: 0.3, fontSize: 14, bold: true, color: TEXT, fontFace: FONT, margin: 0 });

// 3. RECALL FORMULA BOX (orig x69-316, y264-321 px) — red border, white fill
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.96, y: 3.67, w: 3.43, h: 0.79, fill: { color: "FFFFFF" }, line: { color: REDLINE, width: 2 } });
s.addText("Recall =", { x: 1.08, y: 3.92, w: 1.05, h: 0.35, fontSize: 18, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });
s.addImage({ path: NS + "/recreated_pptx/build/assets/eq_010_recall_v2.png", x: 2.2, y: 3.90, w: 0.68333, h: 0.33 });

// 4. PRECISION BOX (right of formula box)
s.addShape(pptx.shapes.RECTANGLE, { x: 4.58, y: 3.54, w: 2.78, h: 0.97, fill: { color: PALE }, line: { color: BLUEBORDER, width: 1 } });
s.addText("Precision= 18/(18+12)", { x: 4.72, y: 3.75, w: 2.5, h: 0.3, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "left" });
s.addText("=60%", { x: 4.72, y: 4.12, w: 2.5, h: 0.3, fontSize: 13, bold: true, color: BLUE, fontFace: FONT, margin: 0, align: "left" });

// 5. CALLOUT NOTES with upward tails (orig x115-320, y343-376 px)
function callout(x, fill, line2, tailX) {
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: tailX, y: 4.60, w: 0.16, h: 0.16, fill: { color: fill }, line: { color: "E0C000", width: 0.5 }, rotate: 180 });
  s.addShape(pptx.shapes.RECTANGLE, { x: x, y: 4.76, w: 1.36, h: 0.46, fill: { color: fill }, line: { color: "E0C000", width: 0.75 } });
  s.addText([{ text: "Positive", options: { breakLine: true } }, { text: line2 }], { x: x + 0.03, y: 4.78, w: 1.3, h: 0.42, fontSize: 10, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center", valign: "middle", lineSpacing: 11 });
}
callout(1.6, "FFFFCC", "Classified as +ive", 2.30);
callout(3.11, "FCE4D6", "Classified as -ive", 2.95);

// 6. GREEN UNDERBRACE + caption (orig brace x111-332, y391-396 px)
s.addImage({ path: NS + "/recreated_pptx/build/assets/brace_010.png", x: 1.54, y: 5.34, w: 2.6, h: 0.2167 });
s.addText("All Positive Samples in the Dataset", { x: 1.54, y: 5.58, w: 3.07, h: 0.3, fontSize: 13, italic: true, color: RED, fontFace: FONT, margin: 0, align: "center" });

// 7. BOTTOM QUESTION BOX (orig x75-499, y463-509 px)
s.addShape(pptx.shapes.RECTANGLE, { x: 1.04, y: 6.43, w: 5.89, h: 0.64, fill: { color: PALE }, line: { color: BLUEBORDER, width: 1.5 } });
s.addText([
  { text: "If you said: I picked " },
  { text: "ALL", options: { bold: true } },
  { text: " Positive objects,", options: { breakLine: true } },
  { text: "can I trust you? At what %?" }
], { x: 1.14, y: 6.47, w: 5.69, h: 0.56, fontSize: 13, italic: true, color: BLUE, fontFace: FONT, margin: 0, align: "left", valign: "middle", lineSpacing: 17 });

// 8. MATRIX PANELS (blue border; orig x672-867, panel1 y52-159, panel2 y167-288 px)
function matrix(px, py, pw, ph, cells) {
  s.addShape(pptx.shapes.RECTANGLE, { x: px, y: py, w: pw, h: ph, fill: { color: "FFFFFF" }, line: { color: MATRIXBLUE, width: 1.5 } });
  s.addText("Predicted as", { x: px + 0.12, y: py + 0.06, w: pw - 0.24, h: 0.25, fontSize: 12, bold: true, color: REDLINE, fontFace: FONT, align: "center", margin: 0 });
  const gx = px + 0.62, gy = py + 0.56, cw = 1.0, ch = ph > 1.6 ? 0.45 : 0.39;
  s.addText("P", { x: gx, y: py + 0.34, w: cw, h: 0.22, fontSize: 12, bold: true, color: REDLINE, fontFace: FONT, align: "center", margin: 0 });
  s.addText("N", { x: gx + cw, y: py + 0.34, w: cw, h: 0.22, fontSize: 12, bold: true, color: REDLINE, fontFace: FONT, align: "center", margin: 0 });
  s.addText("Actual", { x: px + 0.06, y: gy - 0.05, w: 0.42, h: ch * 2 + 0.1, fontSize: 10, bold: true, color: REDLINE, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
  s.addText("P", { x: px + 0.29, y: gy, w: 0.3, h: ch, fontSize: 12, bold: true, color: REDLINE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addText("N", { x: px + 0.29, y: gy + ch, w: 0.3, h: ch, fontSize: 12, bold: true, color: REDLINE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  // cells
  cells.forEach((c, i) => {
    const cx = gx + (i % 2) * cw, cy = gy + Math.floor(i / 2) * ch;
    s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: cw, h: ch, fill: { color: c.fill || "FFFFFF" }, line: { color: REDLINE, width: 1 } });
    if (c.ring) {
      s.addShape(pptx.shapes.OVAL, { x: cx + cw / 2 - 0.26, y: cy + ch / 2 - 0.26, w: 0.52, h: 0.52, fill: { color: "FFFFFF" }, line: { color: c.ring, width: 1.75 } });
      s.addText(c.label, { x: cx, y: cy, w: cw, h: ch, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
    } else if (c.circle) {
      s.addShape(pptx.shapes.OVAL, { x: cx + cw / 2 - 0.21, y: cy + ch / 2 - 0.21, w: 0.42, h: 0.42, fill: { color: c.circle }, line: { color: c.circle, width: 1 } });
      s.addText(c.label, { x: cx + cw / 2 - 0.21, y: cy + ch / 2 - 0.21, w: 0.42, h: 0.42, fontSize: 12, bold: true, color: c.textColor || "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
    } else {
      s.addText(c.label, { x: cx, y: cy, w: cw, h: ch, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
    }
  });
}
matrix(9.33, 0.72, 2.71, 1.49, [
  { label: "TP", fill: LGREEN },
  { label: "FN", fill: "FFFFFF" },
  { label: "FP", fill: "FFFFFF" },
  { label: "TN", fill: LGREEN }
]);
matrix(9.33, 2.32, 2.71, 1.68, [
  { label: "18", fill: "FFFFFF", ring: "7030A0" },
  { label: "12", circle: ORANGE, textColor: TEXT },
  { label: "10", fill: "FFFFFF" },
  { label: "60", fill: LGREEN }
]);

// 9. TREE PANEL (red border; orig x536-881, y300-502 px)
const tpX = 7.44, tpY = 4.17, tpW = 4.79, tpH = 2.81;
s.addShape(pptx.shapes.RECTANGLE, { x: tpX, y: tpY, w: tpW, h: tpH, fill: { color: "FFFFFF" }, line: { color: REDLINE, width: 1.5 } });
s.addText("Positive", { x: 7.75, y: tpY + 0.07, w: 1.5, h: 0.3, fontSize: 16, bold: true, color: RED, fontFace: FONT, align: "center", margin: 0 });
s.addText("Negative", { x: 10.0, y: tpY + 0.07, w: 1.5, h: 0.3, fontSize: 16, bold: true, color: GREEN, fontFace: FONT, align: "center", margin: 0 });
s.addImage({ path: NS + "/recreated_pptx/build/assets/plane_010_pos.png", x: 7.85, y: 4.62, w: 1.3333, h: 0.4167 });
s.addImage({ path: NS + "/recreated_pptx/build/assets/plane_010_neg.png", x: 9.95, y: 4.62, w: 1.3333, h: 0.4167 });

function node(cx, cy, color, label) {
  s.addShape(pptx.shapes.OVAL, { x: cx - 0.21, y: cy - 0.21, w: 0.42, h: 0.42, fill: { color: color }, line: { color: color, width: 1 } });
  s.addText(label, { x: cx - 0.21, y: cy - 0.21, w: 0.42, h: 0.42, fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
}
function arrow(x1, y1, x2, y2) {
  s.addShape(pptx.shapes.LINE, { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color: ARROW, width: 1.5 } });
  const ang = Math.atan2(x2 - x1, -(y2 - y1)) * 180 / Math.PI;
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x2 - 0.08, y: y2 - 0.08, w: 0.16, h: 0.16, fill: { color: ARROW }, line: { color: ARROW, width: 0.5 }, rotate: ang });
}
node(8.58, 5.46, RED, "30");
node(11.15, 5.46, GREEN, "70");
arrow(8.58, 5.67, 7.94, 6.11);
arrow(8.58, 5.67, 9.18, 6.14);
arrow(11.15, 5.67, 10.49, 6.14);
arrow(11.15, 5.67, 11.74, 6.12);
node(7.94, 6.32, RED, "18");
node(9.18, 6.35, GREEN, "12");
node(10.49, 6.35, GREEN, "60");
node(11.74, 6.33, RED, "10");
const leafLabels = [[7.94, "TP", RED], [9.18, "FN", GREEN], [10.49, "TN", GREEN], [11.74, "FP", RED]];
leafLabels.forEach(([cx, t, c]) => {
  s.addText(t, { x: cx - 0.4, y: 6.58, w: 0.8, h: 0.25, fontSize: 11, bold: true, color: c, fontFace: FONT, align: "center", margin: 0 });
});

const outFile = NS + "/recreated_pptx/slide_010_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done", outFile));
