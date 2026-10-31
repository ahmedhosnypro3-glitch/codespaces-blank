const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const FONT = "Arial";
const A = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE CHROME
s.addShape(pptx.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { color: BG }, line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 } });
s.addText("11", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0 });
s.addText("Recall", { x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "middle", fontSize: 44, bold: true, color: RED, fontFace: FONT, margin: 0 });

// ---------- LEFT COLUMN ----------
// 1. Definition strip: gray panel, red rule divider, two bold centered lines (px/72 from frame)
s.addShape(pptx.shapes.RECTANGLE, { x: 0.96, y: 2.01, w: 8.95, h: 1.11, fill: { color: "D9D9D9" }, line: { type: "none" } });
s.addShape(pptx.shapes.LINE, { x: 1.30, y: 2.39, w: 4.30, h: 0, line: { color: RED, width: 2 } });
s.addText("Correctly Classified (as Positive)", { x: 1.06, y: 2.08, w: 8.75, h: 0.32, fontSize: 17, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center", valign: "middle" });
s.addText("Total objects that should be retrieved (Actually Positive)", { x: 1.06, y: 2.46, w: 8.75, h: 0.36, fontSize: 17, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center", valign: "middle" });

// 2. Meaning panel (pale yellow)
s.addShape(pptx.shapes.RECTANGLE, { x: 0.55, y: 3.24, w: 9.1, h: 0.72, fill: { color: "FFFFCC" }, line: { color: "CCCC00", width: 0.75 } });
s.addText("Meaning", { x: 0.70, y: 3.28, w: 2.0, h: 0.34, fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0, valign: "middle" });
s.addText([
  { text: "Does the classifier " },
  { text: "miss", options: { color: "FF0000", italic: true, underline: true } },
  { text: " any of " },
  { text: "Positive", options: { color: "0000CC", bold: true } },
  { text: " Objects ?" },
], { x: 0.70, y: 3.62, w: 8.8, h: 0.32, fontSize: 19, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });

// 3. Recall formula: one red rounded box containing "Recall =" + stacked-fraction PNG
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.82, y: 4.04, w: 4.75, h: 1.25, fill: { color: "FFFFFF" }, line: { color: RED, width: 2 } });
s.addText("Recall =", { x: 0.95, y: 4.35, w: 1.6, h: 0.6, fontSize: 22, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });
s.addImage({ path: A + "/eq_011_frac_tpfn.png", x: 3.55, y: 4.28, w: 1.465, h: 0.6717 });

// 4. Calculation box (white, blue outline): line1 "Recall= 28/(28+2)", line2 "=93.3%" red
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 5.83, y: 4.04, w: 3.33, h: 1.25, fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 } });
s.addText("Recall=", { x: 5.95, y: 4.20, w: 1.0, h: 0.35, fontSize: 15, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });
s.addImage({ path: A + "/eq_011_frac_28.png", x: 6.95, y: 4.18, w: 0.7317, h: 0.4183 });
s.addText("=93.3%", { x: 5.95, y: 4.72, w: 1.4, h: 0.35, fontSize: 15, bold: true, color: "FF0000", fontFace: FONT, margin: 0, valign: "middle" });

// 5. Two beige callouts with UPWARD tails, two-line text
function callout(x, line2) {
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x + 0.61, y: 5.30, w: 0.24, h: 0.14, fill: { color: "F2E6D9" }, line: { color: "C8A878", width: 1 } });
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: x, y: 5.44, w: 1.67, h: 0.49, fill: { color: "F2E6D9" }, line: { color: "C8A878", width: 1 } });
  s.addText("Positive", { x: x + 0.05, y: 5.46, w: 1.57, h: 0.22, fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center", valign: "middle" });
  s.addText(line2, { x: x + 0.05, y: 5.68, w: 1.57, h: 0.22, fontSize: 10, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center", valign: "middle" });
}
callout(1.25, "Classified as +ive");
callout(3.03, "Classified as -ive");

// 6. Green underbrace + blue italic caption
s.addImage({ path: A + "/brace_011_under.png", x: 1.22, y: 5.98, w: 3.6, h: 0.1267 });
s.addText("All Positive Samples in the Dataset", { x: 1.32, y: 6.10, w: 3.40, h: 0.20, fontSize: 11, italic: true, color: RED, fontFace: FONT, margin: 0, align: "center", valign: "middle" });

// 7. Bottom blue note (rounded, light blue) — 3 lines as in original, "NOT" preserved
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.53, y: 6.24, w: 7.79, h: 1.08, fill: { color: "ADD8E6" }, line: { type: "none" } });
s.addText([
  { text: "Higher Recall means ", options: { color: "0000EE" } },
  { text: "I HIGHLY trust you if you said I picked", options: { bold: true, color: TEXT } },
], { x: 0.68, y: 6.32, w: 7.5, h: 0.3, fontSize: 12, fontFace: FONT, margin: 0, valign: "top" });
s.addText("ALL Positive Objects.", { x: 0.68, y: 6.62, w: 7.5, h: 0.3, fontSize: 12, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "top" });
s.addText([
  { text: "It Does ", options: { color: "0000EE" } },
  { text: "NOT", options: { bold: true, color: "FF0000" } },
  { text: " mean ", options: { color: "0000EE" } },
  { text: "All you said Positive are Actually Positive", options: { bold: true, color: TEXT } },
], { x: 0.68, y: 6.92, w: 7.5, h: 0.3, fontSize: 12, fontFace: FONT, margin: 0, valign: "top" });

// ---------- RIGHT COLUMN ----------
// Confusion matrices: 4 cols x 4 rows, blue border, yellow-green header cells
function matrix(y, cells) {
  const hdr = { fontSize: 11, bold: true, color: TEXT, fontFace: FONT, fill: { color: "FFFFFF" }, align: "center", valign: "middle" };
  const redHdr = { fontSize: 11, bold: true, color: RED, fontFace: FONT, fill: { color: "FFFFFF" }, align: "center", valign: "middle" };
  const empty = { text: " ", options: { fontSize: 11, fill: { color: "FFFFFF" } } };
  const cell = (t, fill, color) => ({ text: t, options: { fontSize: 12, bold: true, color: color || TEXT, fontFace: FONT, fill: { color: fill }, align: "center", valign: "middle" } });
  const data = [
    [empty, empty, { text: "Predicted as", options: { ...redHdr, colspan: 2 } }],
    [empty, empty, { text: "P", options: hdr }, { text: "N", options: hdr }],
    [empty, { text: "P", options: hdr }, cell(cells[0][0], cells[0][1], cells[0][4]), cell(cells[0][2], cells[0][3], cells[0][5])],
    [empty, { text: "N", options: hdr }, cell(cells[1][0], cells[1][1], cells[1][4]), cell(cells[1][2], cells[1][3], cells[1][5])],
  ];
  s.addTable(data, {
    x: 10.28, y: y, w: 2.44,
    colW: [0.55, 0.49, 0.70, 0.70],
    rowH: [0.25, 0.40, 0.56, 0.56],
    border: [{ type: "solid", color: "0000FF", width: 1.25 }],
  });
  // vertical red "Actual" label in the corner column
  s.addText("Actual", {
    x: 10.055, y: y + 0.25 + 0.40 + 0.28 - 0.15, w: 1.0, h: 0.3,
    rotate: 90, fontSize: 11, bold: true, color: RED, fontFace: FONT,
    align: "center", valign: "middle", margin: 0,
  });
}
matrix(0.69, [["TP", "90EE90", "FN", "FFFFFF"], ["FP", "FFFFFF", "TN", "90EE90"]]);
matrix(3.08, [["28", "FFFFFF", "2", "FFFFFF"], ["30", "FFFFFF", "40", "90EE90"]]);
// tight purple highlight ring on the 28 cell only (no red capture-artifact oval)
s.addShape(pptx.shapes.OVAL, { x: 11.36, y: 3.76, w: 0.62, h: 0.50, fill: { type: "none" }, line: { color: "800080", width: 1.5 } });

// Tree panel: red frame
s.addShape(pptx.shapes.RECTANGLE, { x: 8.20, y: 5.15, w: 4.85, h: 2.10, fill: { color: "FFFFFF" }, line: { color: RED, width: 2 } });
s.addText("Positive", { x: 9.03, y: 5.20, w: 1.11, h: 0.28, fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0, align: "center", valign: "middle" });
s.addText("Negative", { x: 11.80, y: 5.20, w: 1.11, h: 0.28, fontSize: 15, bold: true, color: "00B050", fontFace: FONT, margin: 0, align: "center", valign: "middle" });
// airplane icons above each root
s.addImage({ path: A + "/airplane_011_v2.png", x: 8.70, y: 5.48, w: 0.5283, h: 0.2783 });
s.addImage({ path: A + "/airplane_011_neg.png", x: 11.90, y: 5.48, w: 0.5283, h: 0.2783 });

function node(cx, cy, num, fill) {
  s.addShape(pptx.shapes.OVAL, { x: cx - 0.195, y: cy - 0.195, w: 0.39, h: 0.39, fill: { color: fill }, line: { color: fill, width: 1 } });
  s.addText(num, { x: cx - 0.195, y: cy - 0.195, w: 0.39, h: 0.39, fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
}
function branch(x0, y0, x1, y1) {
  const x = Math.min(x0, x1), y = Math.min(y0, y1);
  s.addShape(pptx.shapes.LINE, { x: x, y: y, w: Math.abs(x1 - x0), h: Math.abs(y1 - y0), line: { color: "0000FF", width: 1 } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x1 - 0.06, y: y1 - 0.11, w: 0.12, h: 0.11, fill: { color: "0000FF" }, line: { color: "0000FF", width: 0.5 }, rotate: 180 });
}
function leaf(cx, cy, label) {
  s.addText(label, { x: cx - 0.195, y: cy, w: 0.39, h: 0.24, fontSize: 11, bold: true, color: TEXT, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
}
// left (Positive) tree: solid red nodes, green for the FN child
node(8.835, 6.075, "30", "FF0000");
node(8.475, 6.775, "28", "FF0000");
node(9.525, 6.775, "2", "00B050");
branch(8.835, 6.27, 8.475, 6.58);
branch(8.835, 6.27, 9.525, 6.58);
leaf(8.475, 6.99, "TP");
leaf(9.525, 6.99, "FN");
// right (Negative) tree: solid green nodes, red for the FP child
node(12.075, 6.075, "70", "00B050");
node(11.665, 6.775, "40", "00B050");
node(12.725, 6.775, "30", "FF0000");
branch(12.075, 6.27, 11.665, 6.58);
branch(12.075, 6.27, 12.725, 6.58);
leaf(11.665, 6.99, "TN");
leaf(12.725, 6.99, "FP");

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_011_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done"));
