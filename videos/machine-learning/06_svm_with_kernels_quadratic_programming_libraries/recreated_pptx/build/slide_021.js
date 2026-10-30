const pptxgen = require("pptxgenjs");
const { addEq } = require("./eqimg.js");

const NUM = 21;
const TITLE = "Quadratic Kernel";
const FORMULA = "[a\u1d40b]\u00b2";
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "2C3E50" }; // Dark gray canvas

// House frame (red border on dark)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// Badge (yellow on dark)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Example-1 pill (blue)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.3, y: 0.3, w: 1.2, h: 0.4,
  fill: { color: "3498DB" }, line: { color: "3498DB" },
});
s.addText("Example-1", { x: 0.35, y: 0.32, w: 1.1, h: 0.35, align: "center", fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });

// Title + formula (red)
s.addText(TITLE, { x: 3.0, y: 0.28, w: 7.0, h: 0.55, align: "center", fontSize: 26, bold: true, color: "E74C3C", fontFace: FONT, margin: 0 });
addEq(s, "eq21_title", { x: 3.0, y: 0.8, w: 7.0, h: 0.5 });

// Left column: yellow-outlined vector pairs with red double-arrows
// Top row
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.3, y: 1.5, w: 1.5, h: 0.5,
  fill: { type: "none" }, line: { color: "F1C40F", width: 1.5 },
});
addEq(s, "eq21_lab1", { x: 0.4, y: 1.5, w: 1.3, h: 0.5 });
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.3, y: 2.1, w: 1.5, h: 0.5,
  fill: { type: "none" }, line: { color: "F1C40F", width: 1.5 },
});
addEq(s, "eq21_lab2", { x: 0.4, y: 2.1, w: 1.3, h: 0.5 });

// Red double-arrows (top flow)
s.addShape(pres.shapes.LINE, { x: 2.0, y: 1.6, w: 1.5, h: 0, line: { color: "E74C3C", width: 3 } });
s.addShape(pres.shapes.LINE, { x: 2.0, y: 2.2, w: 1.5, h: 0, line: { color: "E74C3C", width: 3 } });

// Middle rail: blue mapping pill
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 3.5, y: 1.8, w: 3.0, h: 0.6,
  fill: { color: "3498DB" }, line: { color: "3498DB" },
});
s.addText("Map Input data from 2-D to 3-D", { x: 3.6, y: 1.85, w: 2.8, h: 0.5, align: "center", fontSize: 11, color: "FFFFFF", fontFace: FONT, margin: 0 });

// Upper-right: Normal Model (blue border)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 7.0, y: 1.5, w: 5.8, h: 2.0,
  fill: { color: "D6EAF8" }, line: { color: "E74C3C", width: 2 },
});
addEq(s, "eq21_norm_a", { x: 7.1, y: 1.55, w: 5.6, h: 0.45 });
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.5, y: 2.2, w: 3.0, h: 1.0,
  fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 1 },
});
addEq(s, "eq21_mtx", { x: 8.5, y: 2.25, w: 3.0, h: 0.9 });

// Lower rail: red box [a^T b]^2
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 3.0, w: 3.0, h: 0.5,
  fill: { color: "FFFFFF" }, line: { color: "E74C3C", width: 2 },
});
addEq(s, "eq21_sq", { x: 3.6, y: 3.0, w: 2.8, h: 0.5 });

// Purple Vectors Mapping pill
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 3.5, y: 3.7, w: 3.0, h: 0.5,
  fill: { color: "8E44AD" }, line: { color: "8E44AD" },
});
addEq(s, "eq21_map", { x: 3.6, y: 3.7, w: 2.8, h: 0.5 });

// Purple complexity pill
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 3.5, y: 4.3, w: 3.0, h: 0.5,
  fill: { color: "8E44AD" }, line: { color: "8E44AD" },
});
s.addText("Higher Computational Complexity!!!", { x: 3.6, y: 4.32, w: 2.8, h: 0.45, align: "center", fontSize: 10, color: "FFFFFF", fontFace: FONT, margin: 0 });

// Large purple vector box
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 5.0, w: 3.0, h: 1.5,
  fill: { color: "F5EEF8" }, line: { color: "8E44AD", width: 1.5 },
});
addEq(s, "eq21_uv", { x: 3.6, y: 5.1, w: 2.8, h: 1.3 });

// Lower-right: Kernelized Model (green border)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 7.0, y: 4.0, w: 5.8, h: 2.8,
  fill: { color: "D5F5E3" }, line: { color: "E74C3C", width: 2 },
});
addEq(s, "eq21_kern_u", { x: 7.1, y: 4.05, w: 5.6, h: 0.45 });
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.5, y: 4.7, w: 4.8, h: 1.8,
  fill: { color: "FFFFFF" }, line: { color: "27AE60", width: 1 },
});
addEq(s, "eq21_6d", { x: 7.6, y: 4.9, w: 4.6, h: 1.4 });
// Green complexity pill
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 7.0, y: 6.6, w: 2.5, h: 0.5,
  fill: { color: "27AE60" }, line: { color: "27AE60" },
});
s.addText("Higher Computational Complexity!!!", { x: 7.1, y: 6.62, w: 2.3, h: 0.45, align: "center", fontSize: 9, color: "FFFFFF", fontFace: FONT, margin: 0 });

// Black strip bottom (on dark bg)
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 7.0, w: 13.03, h: 0.5, fill: { color: "000000" }, line: { color: "000000" } });

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_021_recreated.pptx" })
  .then(() => console.log("wrote slide_021_recreated.pptx"))
  .catch(e => console.error(e));