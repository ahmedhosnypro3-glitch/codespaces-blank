const pptxgen = require("pptxgenjs");

// Slide 024 — built FRESH from qa/reanalysis2/slide_024_analysis.txt only.
// Title-divider slide: 3-line title (red/red/blue), no equations, no plots.
// House chrome (frame/badge/title box) overrides spec geometry per house rule.
const NUM = 24;
const FONT = "Arial";
const W = 13.33, H = 7.5;

// Normalized spec coords [x0,y0,x1,y1] -> inches
const ix = v => v * W, iy = v => v * H;
const iw = (x0, x1) => (x1 - x0) * W, ih = (y0, y1) => (y1 - y0) * H;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. House outer red frame (house rule overrides spec frame box)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. House badge: yellow circle + numeral (house rule overrides spec badge style)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title block in the house title box (spec VERBATIM_TEXT [TITLE] lines,
//    per-line colors/sizes from spec sections 6/7: 28pt red, 24pt red, 26pt blue)
s.addText([
  { text: "KERNEL Functions", options: { fontSize: 28, bold: true, color: "C00000", fontFace: FONT, breakLine: true } },
  { text: "and", options: { fontSize: 24, bold: true, color: "C00000", fontFace: FONT, breakLine: true } },
  { text: "Kernel Trick", options: { fontSize: 26, bold: true, color: "0000CC", fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 1.9,
  align: "center", valign: "top", lineSpacingMultiple: 1.6, margin: 0,
});

// 4. Faint thin horizontal rule, top right (spec [0.890, 0.066, 1.000, 0.072], #9FB3B3)
s.addShape(pres.shapes.RECTANGLE, {
  x: ix(0.890), y: iy(0.066), w: iw(0.890, 1.000), h: ih(0.066, 0.072),
  fill: { color: "9FB3B3" }, line: { type: "none" },
});

// 5. Solid black letterbox bar along the bottom edge (spec [0.042, 0.957, 0.969, 1.000])
s.addShape(pres.shapes.RECTANGLE, {
  x: ix(0.042), y: iy(0.957), w: iw(0.042, 0.969), h: ih(0.957, 1.000),
  fill: { color: "000000" }, line: { type: "none" },
});

// 6. Mouse-pointer arrow, lower-left-of-centre (spec [0.335, 0.843, 0.362, 0.898]),
//    black with white edge, pointing up-left
s.addShape(pres.shapes.LEFT_UP_ARROW, {
  x: ix(0.335), y: iy(0.843), w: iw(0.335, 0.362), h: ih(0.843, 0.898),
  fill: { color: "000000" }, line: { color: "FFFFFF", width: 0.75 },
});

// 7. Remaining framed area intentionally empty (spec RECREATION_BRIEF item 10)

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_024_recreated.pptx" })
  .then(() => console.log("wrote slide_024_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
