const pptxgen = require("pptxgenjs");

// Slide 015 — FRESH build from qa/reanalysis2/slide_015_analysis.txt ONLY.
// Spec: "Non-Linearly Separable Data". Inner white panel with red border,
// italic red instruction line, two annotation label boxes with lavender leader
// lines, matplotlib plot (orange parabola + blue line + red x-axis + 12 markers
// + red "x"), small black cursor triangle, bottom black overlay bar.
// House chrome overrides spec geometry for frame/badge/title.
const NUM = 15;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_015_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (mandatory) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Title: "Non-Linearly Separable Data" — "Separable" blue + underlined per spec
s.addText([
  { text: "Non-Linearly ", options: { fontSize: 24, bold: true, color: "C00000", fontFace: FONT } },
  { text: "Separable", options: { fontSize: 24, bold: true, color: "0000FF", fontFace: FONT, underline: true } },
  { text: " Data", options: { fontSize: 24, bold: true, color: "C00000", fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top", margin: 0,
});

// ---- spec content ----
// Inner red content rectangle (white fill), spec [0.090,0.175,0.912,0.935]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.090 * W, y: 0.175 * H, w: (0.912 - 0.090) * W, h: (0.935 - 0.175) * H,
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1 },
});

// Plot PNG (spec sections 4/9/10 items 11-16) covering [0.10,0.48,0.87,0.87]
s.addImage({
  path: __dirname + "/slide_015_graph.png",
  x: 0.10 * W, y: 0.48 * H, w: (0.87 - 0.10) * W, h: (0.87 - 0.48) * H,
});

// Leader line 1 (lavender): (0.265,0.404) -> (0.288,0.528)
s.addShape(pres.shapes.LINE, {
  x: 0.265 * W, y: 0.404 * H, w: (0.288 - 0.265) * W, h: (0.528 - 0.404) * H,
  line: { color: "B19CD9", width: 1.5 },
});
// Leader line 2 (lavender): (0.397,0.428) -> (0.436,0.520)
s.addShape(pres.shapes.LINE, {
  x: 0.397 * W, y: 0.428 * H, w: (0.436 - 0.397) * W, h: (0.520 - 0.428) * H,
  line: { color: "B19CD9", width: 1.5 },
});
// Annotation box 1: "Non-Linear / Decision / Boundary", spec [0.296,0.387,0.394,0.478]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.296 * W, y: 0.387 * H, w: (0.394 - 0.296) * W, h: (0.478 - 0.387) * H,
  fill: { color: "FFFFFF" }, line: { color: "9999CC", width: 1.25 },
});
s.addText("Non-Linear\nDecision\nBoundary", {
  x: 0.296 * W, y: 0.387 * H, w: (0.394 - 0.296) * W, h: (0.478 - 0.387) * H,
  align: "center", valign: "middle", margin: 0,
  fontSize: 12, bold: true, italic: true, color: "3333CC",
  fontFace: "Times New Roman", lineSpacing: 14,
});

// Annotation box 2: "Linear / Decision / Boundary", spec [0.438,0.417,0.534,0.513]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.438 * W, y: 0.417 * H, w: (0.534 - 0.438) * W, h: (0.513 - 0.417) * H,
  fill: { color: "FFFFFF" }, line: { color: "B07FD0", width: 1.25 },
});
s.addText("Linear\nDecision\nBoundary", {
  x: 0.438 * W, y: 0.417 * H, w: (0.534 - 0.438) * W, h: (0.513 - 0.417) * H,
  align: "center", valign: "middle", margin: 0,
  fontSize: 12, bold: true, italic: true, color: "6633CC",
  fontFace: "Times New Roman", lineSpacing: 14,
});

// Italic red instruction line, spec [0.135,0.246,0.548,0.276]; wide left box per lesson
s.addText('Each Sample is represented by one features "x"', {
  x: 1.33, y: 0.246 * H, w: 9.5, h: 0.35,
  align: "left", valign: "top", margin: 0,
  fontSize: 16, italic: true, color: "CC0000", fontFace: FONT,
});

// Small black cursor-like arrow (isosceles triangle pointing NW), spec [0.405,0.659,0.423,0.696]
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: 0.405 * W, y: 0.659 * H, w: (0.423 - 0.405) * W, h: (0.696 - 0.659) * H,
  fill: { color: "000000" }, line: { color: "808080", width: 0.75 },
  rotate: 315,
});

// Bottom black overlay bar, spec [0.042,0.950,0.978,1.000]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.042 * W, y: 0.950 * H, w: (0.978 - 0.042) * W, h: (1.000 - 0.950) * H,
  fill: { color: "000000" }, line: { type: "none" },
});

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote slide_015_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
