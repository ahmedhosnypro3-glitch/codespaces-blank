// Slide 24 "Stopping Criteria" — attempt 3: rich-text runs (no absolute-positioned
// highlight boxes) to fix the judge-FAIL text overlap. Patterns: house-chrome,
// explicit-line-spacing, highlight via run highlight (pptxgenjs 4.x).
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const FONT = "Arial";
const BG = "E8E8E8", RED = "C00000", BLACK = "000000", BLUE = "0000FF", YEL = "FFFF00";

const s = pres.addSlide();
s.background = { color: BG };

// House chrome (binding: FFF9C4 badge, 333333 numeral)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("24", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Stopping Criteria", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Panels measured from original frame (960x540, 1px = 1pt): x 54..888, top 99..252, bottom 271..521
const PX = 54 / 72, PW = (888 - 54) / 72;
const TOP_Y = 99 / 72, TOP_H = (252 - 99) / 72;
const BOT_Y = 271 / 72, BOT_H = (521 - 271) / 72;
const TX = 64 / 72, TW = PW - 2 * (64 - 54) / 72;
const PITCH = 34; // pt, measured line pitch in original

s.addShape(pres.shapes.RECTANGLE, {
  x: PX, y: TOP_Y, w: PW, h: TOP_H,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: PX, y: BOT_Y, w: PW, h: BOT_H,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 },
});

// Top panel: 4 criteria lines as ONE text box with rich runs
const topLines = [
  [ { text: "[1] Total Error = zero ", options: { fontSize: 20, color: BLACK, fontFace: FONT } },
    { text: "(Theoretical)", options: { fontSize: 20, color: BLACK, fontFace: FONT, highlight: YEL } } ],
  [ { text: "[2] Total Error < certain value (Threshold)", options: { fontSize: 20, color: BLACK, fontFace: FONT } } ],
  [ { text: "[3] Percentage Change of Weights is less than certain value (Threshold)", options: { fontSize: 20, color: BLACK, fontFace: FONT } } ],
  [ { text: "[4] Reach Maximum number of iterations ", options: { fontSize: 20, color: BLACK, fontFace: FONT } },
    { text: "(Epochs)", options: { fontSize: 20, color: BLUE, fontFace: FONT } },
    { text: " without satisfying [2] or [3]", options: { fontSize: 20, color: BLACK, fontFace: FONT } } ],
];
const topRuns = [];
topLines.forEach((ln, i) => {
  ln.forEach(r => topRuns.push(r));
  if (i < topLines.length - 1) topRuns.push({ text: "", options: { breakLine: true } });
});
s.addText(topRuns, {
  x: TX, y: TOP_Y + 0.10, w: TW, h: TOP_H - 0.15,
  lineSpacing: PITCH, margin: 0, valign: "top",
});

// Bottom panel: status line (red bold), subheading (red, underlined), 4 reasons
const botLines = [
  [ { text: "Stopping is due to reaching Maximum number of iterations = Training is FAILED",
      options: { fontSize: 20, bold: true, color: RED, fontFace: FONT } } ],
  [ { text: "Expected Reasons:",
      options: { fontSize: 20, color: RED, fontFace: FONT, underline: { style: "sng" } } } ],
  [ { text: "[1] The defined Maximum Number of ", options: { fontSize: 20, color: BLACK, fontFace: FONT } },
    { text: "Epochs", options: { fontSize: 20, color: BLUE, fontFace: FONT } },
    { text: " is small. Try to increase the limit", options: { fontSize: 20, color: BLACK, fontFace: FONT } } ],
  [ { text: "[2] Under-fitting (Training samples are not adequate). Try to provide more training samples",
      options: { fontSize: 20, color: BLACK, fontFace: FONT } } ],
  [ { text: "[3] Model Design is not suitable to training data. Try to add more nodes in ", options: { fontSize: 20, color: BLACK, fontFace: FONT } },
    { text: "hidden layer", options: { fontSize: 20, color: BLUE, fontFace: FONT } },
    { text: " or add more hidden Layers", options: { fontSize: 20, color: BLACK, fontFace: FONT } } ],
  [ { text: "[4] Data is ", options: { fontSize: 20, color: BLACK, fontFace: FONT } },
    { text: "NOT", options: { fontSize: 20, color: BLUE, fontFace: FONT } },
    { text: " separable by ", options: { fontSize: 20, color: BLACK, fontFace: FONT } },
    { text: "Neural Network", options: { fontSize: 20, color: BLUE, fontFace: FONT } },
    { text: ". Try Another Models ", options: { fontSize: 20, color: BLACK, fontFace: FONT } },
    { text: "(e.g. SVM with Kernels)", options: { fontSize: 20, color: BLACK, fontFace: FONT, highlight: YEL } } ],
];
const botRuns = [];
botLines.forEach((ln, i) => {
  ln.forEach(r => botRuns.push(r));
  if (i < botLines.length - 1) botRuns.push({ text: "", options: { breakLine: true } });
});
s.addText(botRuns, {
  x: TX, y: BOT_Y + 0.06, w: TW, h: BOT_H - 0.10,
  lineSpacing: PITCH, margin: 0, valign: "top",
});

pres.writeFile({ fileName: __dirname + "/slide_024_attempt4.pptx" })
  .then(() => console.log("wrote slide_024_attempt4.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
