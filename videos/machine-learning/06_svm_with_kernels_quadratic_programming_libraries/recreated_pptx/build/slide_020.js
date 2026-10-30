const pptxgen = require("pptxgenjs");
const { addEq } = require("./eqimg.js");

const NUM = 20;
const TITLE = "Model Kernelization";
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

// House frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// Badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Title
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", fontSize: 26, bold: true, color: "E74C3C", fontFace: FONT, margin: 0,
});

// --- TOP FLOW: Normal Model ---
// Input vectors as bracketed matrices
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 1.35, w: 1.5, h: 1.0,
  fill: { type: "none" }, line: { color: "2C3E50", width: 1 },
});
addEq(s, "eq20_mtx_t", { x: 0.42, y: 1.42, w: 1.42, h: 0.9 });
// Arrow to Normal Model
s.addShape(pres.shapes.LINE, {
  x: 2.0, y: 1.85, w: 1.3, h: 0,
  line: { color: "E74C3C", width: 3, endArrowType: "triangle" },
});
// Normal Model pane (white with blue border, per original)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 3.4, y: 1.1, w: 4.9, h: 1.6,
  fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 2 },
});
s.addText("Normal Model", {
  x: 3.5, y: 1.15, w: 4.7, h: 0.4,
  fontSize: 16, bold: true, italic: true, color: "E74C3C", fontFace: FONT, margin: 0, align: "center",
});
addEq(s, "eq20_calc_a", { x: 3.5, y: 1.48, w: 4.7, h: 0.4 });
// 2x2 matrix inside
s.addShape(pres.shapes.RECTANGLE, {
  x: 4.2, y: 1.9, w: 2.2, h: 0.7,
  fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 1 },
});
addEq(s, "eq20_mtx2", { x: 4.25, y: 1.92, w: 2.1, h: 0.66 });
// O/P with hollow red arrow
s.addShape(pres.shapes.LINE, {
  x: 8.4, y: 1.8, w: 0.5, h: 0,
  line: { color: "E74C3C", width: 2.5, endArrowType: "triangle" },
});
s.addText("O/P", {
  x: 8.9, y: 1.65, w: 0.8, h: 0.35,
  fontSize: 13, bold: true, color: "3498DB", fontFace: FONT, margin: 0,
});

// --- MIDDLE GUIDANCE BAND (bold italic blue per original) ---
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 3.4, y: 2.95, w: 4.9, h: 0.6,
  fill: { color: "D6EAF8" }, line: { color: "3498DB", width: 1 },
});
s.addText("Map Input data to higher dimensions Before Apply to the model", {
  x: 3.5, y: 2.98, w: 4.7, h: 0.55,
  align: "center", fontSize: 12, bold: true, italic: true, color: "1F618D", fontFace: FONT, margin: 0, lineSpacing: 14,
});

// --- BOTTOM FLOW: Kernelized Model ---
// Left input vectors (same as top)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 4.6, w: 1.5, h: 1.0,
  fill: { type: "none" }, line: { color: "2C3E50", width: 1 },
});
addEq(s, "eq20_mtx_b", { x: 0.42, y: 4.67, w: 1.42, h: 0.9 });
// Arrow to Vectors Mapping
s.addShape(pres.shapes.LINE, {
  x: 2.0, y: 5.1, w: 0.9, h: 0,
  line: { color: "E74C3C", width: 3, endArrowType: "triangle" },
});
// Vectors Mapping box (purple)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 3.0, y: 4.5, w: 1.6, h: 1.2,
  fill: { color: "F5EEF8" }, line: { color: "8E44AD", width: 2 },
});
s.addText("Vectors Mapping", {
  x: 3.05, y: 4.55, w: 1.5, h: 0.35,
  fontSize: 12, bold: true, color: "8E44AD", fontFace: FONT, margin: 0, align: "center",
});
addEq(s, "eq20_map", { x: 3.05, y: 4.88, w: 1.5, h: 0.3 });
addEq(s, "eq20_uv_map", { x: 3.05, y: 5.16, w: 1.5, h: 0.52 });
// Arrow to purple u/v columns
s.addShape(pres.shapes.LINE, {
  x: 4.65, y: 5.1, w: 0.65, h: 0,
  line: { color: "E74C3C", width: 3, endArrowType: "triangle" },
});
// Purple u/v columns with ellipses (u_1...u_m, v_1...v_m)
s.addShape(pres.shapes.RECTANGLE, {
  x: 5.4, y: 4.35, w: 1.7, h: 1.5,
  fill: { color: "F5EEF8" }, line: { color: "8E44AD", width: 1.5 },
});
addEq(s, "eq20_uv_mtx", { x: 5.45, y: 4.4, w: 1.6, h: 1.4 });

// Purple complexity chip under Vectors Mapping (was MISSING)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 3.0, y: 5.85, w: 2.6, h: 0.45,
  fill: { color: "8E44AD" }, line: { color: "8E44AD" },
});
s.addText("Higher Computational Complexity !!!", {
  x: 3.05, y: 5.86, w: 2.5, h: 0.42,
  fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0, align: "center",
});

// Arrow to Kernelized Model
s.addShape(pres.shapes.LINE, {
  x: 6.95, y: 5.1, w: 0.75, h: 0,
  line: { color: "E74C3C", width: 3, endArrowType: "triangle" },
});
// Kernelized Model pane (pale green per original, green border)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 7.75, y: 4.35, w: 5.2, h: 2.0,
  fill: { color: "D5F5E3" }, line: { color: "27AE60", width: 2 },
});
s.addText("Kernelized Model", {
  x: 7.85, y: 4.4, w: 5.0, h: 0.35,
  fontSize: 16, bold: true, italic: true, color: "27AE60", fontFace: FONT, margin: 0, align: "center",
});
addEq(s, "eq20_calc_u", { x: 7.85, y: 4.7, w: 5.0, h: 0.35 });
// u/v columns inside the kernelized pane (with ellipses, full column)
addEq(s, "eq20_u_row", { x: 7.95, y: 5.1, w: 4.8, h: 0.3 });
addEq(s, "eq20_v_row", { x: 7.95, y: 5.4, w: 4.8, h: 0.3 });
// Complexity chip INSIDE the kernelized pane
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 7.85, y: 5.8, w: 2.9, h: 0.42,
  fill: { color: "27AE60" }, line: { color: "27AE60" },
});
s.addText("Higher Computational Complexity !!!", {
  x: 7.9, y: 5.81, w: 2.8, h: 0.4,
  fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0, align: "center",
});
// O/R with hollow red arrow
s.addShape(pres.shapes.LINE, {
  x: 11.0, y: 5.1, w: 0.5, h: 0,
  line: { color: "E74C3C", width: 2.5, endArrowType: "triangle" },
});
s.addText("O/R", {
  x: 11.5, y: 4.95, w: 0.8, h: 0.35,
  fontSize: 13, bold: true, color: "3498DB", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_020_recreated.pptx" })
  .then(() => console.log("wrote slide_020_recreated.pptx"))
  .catch(e => console.error(e));
