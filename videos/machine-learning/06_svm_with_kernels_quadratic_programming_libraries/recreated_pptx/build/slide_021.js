// slide_021.js — fix cycle 2: native sub/superscript text for inline math, big 2-row panel images
const path = require("path");
const pptxgen = require("pptxgenjs");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const W = 13.33, H = 7.5;
const SERIF = "Times New Roman";
const RED = "CC0000", BLUE = "0000CC", INK = "1A1A1A", DARK = "333333";

const R = b => ({ x: b[0] * W, y: b[1] * H, w: (b[2] - b[0]) * W, h: (b[3] - b[1]) * H });
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const SH = pres.shapes;

const EQ = n => path.join(__dirname, "eq_021", n + ".png");
const emeta = n => require(path.join(__dirname, "eq_021", n + ".json"));
function addEq(slide, name, b) {
  const m = emeta(name), r = R(b);
  slide.addImage({
    path: EQ(name),
    x: r.x + (r.w - m.w_in) / 2, y: r.y + (r.h - m.h_in) / 2,
    w: m.w_in, h: m.h_in,
  });
}
function box(slide, b, fill, line, lw, dash, rounded) {
  const shape = rounded === false ? SH.RECTANGLE : SH.ROUNDED_RECTANGLE;
  slide.addShape(shape, Object.assign(R(b), {
    fill: { color: fill },
    line: Object.assign({ color: line, width: lw || 1 }, dash ? { dashType: dash } : {}),
  }));
}
function txt(slide, s, b, size, color, opts) {
  slide.addText(s, Object.assign(R(b), {
    align: "center", valign: "middle", fontSize: size, color,
    fontFace: SERIF, margin: 0,
  }, opts || {}));
}
// rich-text run line: parts = [{t:"a", o:{color, superscript}}], o defaults italic serif
function runs(slide, parts, b, size) {
  const rr = parts.map(p => ({ text: p.t, options: Object.assign(
    { fontFace: SERIF, fontSize: size, italic: true, color: INK }, p.o || {}) }));
  slide.addText(rr, Object.assign(R(b), { align: "center", valign: "middle", margin: 0 }));
}
function arrow(slide, b, color) {
  slide.addShape(SH.RIGHT_ARROW, Object.assign(R(b), {
    fill: { color: "FFFFFF" }, line: { color, width: 1.5 },
  }));
}
// shared run fragments
const BR = [{ t: "[", o: { color: DARK, italic: false } }];
function ab2(slide, b, size) { // [a^T b]^2
  runs(slide, [
    { t: "[", o: { color: DARK, italic: false } },
    { t: "a", o: { color: RED } },
    { t: "T", o: { color: RED, superscript: true } },
    { t: " ", o: {} },
    { t: "b", o: { color: BLUE } },
    { t: "]", o: { color: DARK, italic: false } },
    { t: "2", o: { color: DARK, superscript: true, italic: false } },
  ], b, size);
}
function vecAB(slide, b, i, j, size) { // a_i | b_j  (single row)
  runs(slide, [
    { t: "a", o: { color: RED } },
    { t: String(i), o: { color: RED, subscript: true } },
    { t: "  |  ", o: { color: DARK, italic: false } },
    { t: "b", o: { color: BLUE } },
    { t: String(j), o: { color: BLUE, subscript: true } },
  ], b, size);
}

const slide = pres.addSlide();

// ---- house chrome (mandatory) ----
slide.background = { color: "E8E8E8" };
slide.addShape(SH.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
slide.addShape(SH.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
slide.addText("21", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
slide.addText("Quadratic Kernel", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: SERIF, margin: 0,
});

// ---- top band ----
box(slide, [0.067, 0.098, 0.178, 0.165], "FFFFFF", BLUE, 1.5, "dash");
txt(slide, "Example-1", [0.067, 0.098, 0.178, 0.165], 16, BLUE, { bold: true, italic: true });
ab2(slide, [0.594, 0.102, 0.673, 0.157], 20);

// ---- upper-middle row ----
box(slide, [0.078, 0.230, 0.164, 0.337], "F8F8E8", "B8B88A", 1);
vecAB(slide, [0.080, 0.248, 0.162, 0.288], 1, 1, 19);
vecAB(slide, [0.080, 0.288, 0.162, 0.328], 2, 2, 19);
arrow(slide, [0.169, 0.263, 0.502, 0.306], RED);
box(slide, [0.504, 0.180, 0.823, 0.409], "FFFFFF", BLUE, 2, null, false);
txt(slide, "Normal Model", [0.617, 0.215, 0.709, 0.246], 13, RED, { bold: true, italic: true });
runs(slide, [
  { t: "Calculate ", o: { color: INK, italic: false } },
  { t: "a", o: { color: RED } },
  { t: "T", o: { color: RED, superscript: true } },
  { t: " ", o: {} },
  { t: "b", o: { color: BLUE } },
], [0.619, 0.256, 0.709, 0.287], 13);
box(slide, [0.611, 0.280, 0.700, 0.394], "E6F0FB", "A8C8E8", 1);
runs(slide, [
  { t: "a", o: { color: RED } }, { t: "1", o: { color: RED, subscript: true } },
  { t: " ", o: {} },
  { t: "a", o: { color: RED } }, { t: "2", o: { color: RED, subscript: true } },
  { t: "  |  ", o: { color: DARK, italic: false } },
  { t: "b", o: { color: BLUE } }, { t: "1", o: { color: BLUE, subscript: true } },
], [0.613, 0.300, 0.698, 0.340], 18);
runs(slide, [
  { t: "      |  ", o: { color: DARK, italic: false } },
  { t: "b", o: { color: BLUE } }, { t: "2", o: { color: BLUE, subscript: true } },
], [0.613, 0.340, 0.698, 0.380], 18);
arrow(slide, [0.819, 0.291, 0.854, 0.326], RED);

// ---- mid band ----
box(slide, [0.103, 0.387, 0.455, 0.446], "FFFFFF", "B8B88A", 1);
txt(slide, "Map Input data from 2-D to 3-D", [0.103, 0.387, 0.455, 0.446], 14, BLUE, { bold: true, italic: true });

// ---- lower half, left flow ----
box(slide, [0.077, 0.617, 0.164, 0.719], "F8F8E8", "B8B88A", 1);
vecAB(slide, [0.079, 0.632, 0.162, 0.672], 1, 1, 19);
vecAB(slide, [0.079, 0.672, 0.162, 0.712], 2, 2, 19);
arrow(slide, [0.170, 0.650, 0.202, 0.681], RED);
box(slide, [0.233, 0.544, 0.310, 0.617], "F8F8E8", "B8B88A", 1);
ab2(slide, [0.233, 0.544, 0.310, 0.617], 17);
box(slide, [0.203, 0.617, 0.345, 0.696], "FFFFFF", RED, 2, null, false);
txt(slide, "Vectors Mapping", [0.209, 0.620, 0.339, 0.652], 13, RED, { bold: true });
txt(slide, "a , b ⇒ u , v", [0.221, 0.652, 0.328, 0.692], 14, RED, { bold: true, italic: false });
box(slide, [0.212, 0.696, 0.338, 0.844], "EADCF8", "B090D8", 1, null, false);
txt(slide, "Higher\nComputational\nComplexity !!!", [0.212, 0.696, 0.338, 0.844], 11, BLUE, { bold: true, italic: true });

// ---- lower half, center -> Kernelized Model panel ----
box(slide, [0.383, 0.533, 0.518, 0.806], "F9E9F9", "CC88CC", 1, null, false);
addEq(slide, "fix2_pink", [0.383, 0.533, 0.518, 0.806]);
arrow(slide, [0.347, 0.650, 0.381, 0.681], RED);
arrow(slide, [0.520, 0.650, 0.552, 0.681], RED);
box(slide, [0.537, 0.483, 0.819, 0.861], "FFFFFF", "008000", 2, null, false);
txt(slide, "Kernelized Model", [0.607, 0.502, 0.722, 0.533], 13, RED, { bold: true, italic: true });
runs(slide, [
  { t: "Calculate ", o: { color: INK, italic: false } },
  { t: "u", o: { color: RED } },
  { t: "T", o: { color: RED, superscript: true } },
  { t: " ", o: {} },
  { t: "v", o: { color: BLUE } },
], [0.617, 0.541, 0.698, 0.572], 13);
box(slide, [0.552, 0.589, 0.761, 0.856], "E9F7E3", "90C090", 1);
addEq(slide, "fix2_kernel", [0.552, 0.589, 0.761, 0.856]);
// lavender complexity box: below the green panel, clear of panel and frame border
box(slide, [0.610, 0.866, 0.750, 0.972], "EADCF8", "B090D8", 1, null, false);
txt(slide, "Higher\nComputational\nComplexity !!!", [0.610, 0.866, 0.750, 0.972], 11, BLUE, { bold: true, italic: true });
arrow(slide, [0.821, 0.657, 0.855, 0.691], RED);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_021_recreated.pptx") });
console.log("wrote slide_021_recreated.pptx");
