const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_009");
const NUM = 9, TITLE = "Example", FONT = "Arial";
const X = v => v * 13.33, Y = v => v * 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (overrides spec): red frame, badge, centered title
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
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
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

function img(name, x, y) {
  const meta = require(path.join(EQ, name + ".png.json"));
  s.addImage({ path: path.join(EQ, name + ".png"), x, y, w: meta.w_in, h: meta.h_in });
}
function txt(t, x, y, w, h, o) {
  s.addText(t, Object.assign(
    { x, y, w, h, fontFace: FONT, margin: 0, fontSize: 14, color: "000000" }, o));
}

// Upper equation stack (spec sec. 3/8)
img("m1", X(0.070), Y(0.128));
img("m2", X(0.286), Y(0.181));
img("m3", X(0.299), Y(0.246));
// Pale-yellow boxed quadratic form
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.692), y: Y(0.222), w: X(0.935 - 0.692), h: Y(0.286 - 0.222),
  fill: { color: "FFFFE0" }, line: { color: "000000", width: 0.75 },
});
img("boxed_fix", X(0.692) + 0.12, Y(0.222) + 0.03);
// P and q matrices
img("P", X(0.381), Y(0.419));
img("q", X(0.449), Y(0.419));
// Red horizontal divider under the top block
s.addShape(pres.shapes.LINE, {
  x: X(0.043), y: Y(0.553), w: X(0.964 - 0.043), h: 0,
  line: { color: "FF0000", width: 1.5 },
});
// Subject-to header with red border
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.060), y: Y(0.589), w: X(0.161 - 0.060), h: Y(0.635 - 0.589),
  fill: { type: "none" }, line: { color: "FF0000", width: 1 },
});
txt("Subject to", X(0.060), Y(0.589), X(0.161 - 0.060), Y(0.635 - 0.589),
  { bold: true, color: "FF0000", fontSize: 16, valign: "middle" });
// Original constraints, arrow, transformed constraints
img("consL", X(0.060), Y(0.638));
img("arrow", X(0.171), Y(0.704));
img("consR", X(0.218), Y(0.630));
// Standard form Gx<=h with G/h matrices
img("gh", X(0.392), Y(0.589));
img("G_full", X(0.360), Y(0.700));
img("h_full", X(0.470), Y(0.700));
// Vertical divider + right evaluation box
s.addShape(pres.shapes.LINE, {
  x: X(0.557), y: Y(0.571), w: 0, h: Y(0.920 - 0.571),
  line: { color: "FF0000", width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.567), y: Y(0.571), w: X(0.981 - 0.567), h: Y(0.920 - 0.571),
  fill: { type: "none" }, line: { color: "FF0000", width: 1.5 },
});
txt("x=0, y=5", X(0.578), Y(0.601), X(0.700 - 0.578), Y(0.642 - 0.601),
  { bold: true, color: "FF0000", fontSize: 16 });
img("checks", X(0.578), Y(0.664));
txt("Minimum value:", X(0.578), Y(0.838), X(0.700 - 0.578), Y(0.872 - 0.838),
  { italic: true, color: "0000FF", fontSize: 13 });
img("finalv", X(0.578), Y(0.876));

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_009_recreated.pptx") })
  .then(() => console.log("wrote slide_009_recreated.pptx"))
  .catch(e => console.error(e));
