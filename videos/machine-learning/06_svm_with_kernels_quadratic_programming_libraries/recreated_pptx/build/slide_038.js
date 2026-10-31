// slide_038.js — REBUILD WAVE 3. Built ONLY from qa/reanalysis2/slide_038_analysis.txt
// (spec starts at "1. SLIDE_TITLE"). House chrome per video AGENTS.md (overrides spec).
// Run from project root: node <NS>/recreated_pptx/build/slide_038.js
const pptxgen = require("pptxgenjs");
const path = require("path");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx", "build", "eq_038");
const MAN = require(path.join(EQ, "rb3_manifest.json"));
const OUT = path.join(NS, "recreated_pptx", "slide_038_recreated.pptx");

const X = v => v * 13.33, Y = v => v * 7.5;
const BW = (a, b) => (b - a) * 13.33, BH = (a, b) => (b - a) * 7.5;
const ARIAL = "Arial", MATHF = "Times New Roman";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();

// house chrome (mandatory)
s.background = { color: "E8E8E8" };
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText("38", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: ARIAL, margin: 0 });
// spec SLIDE_TITLE: none -> no title text

function rbox(b, color, rounded, fill) {
  s.addShape(rounded === false ? pres.shapes.RECTANGLE : pres.shapes.ROUNDED_RECTANGLE, {
    x: X(b[0]), y: Y(b[1]), w: BW(b[0], b[2]), h: BH(b[1], b[3]),
    fill: fill ? { color: fill } : { type: "none" }, line: { color, width: 1.25 } });
}
function img(name, x, y, centerW) {
  const m = MAN[name];
  s.addImage({ path: path.join(EQ, name + ".png"),
    x: centerW ? x + (centerW - m.w_in) / 2 : x, y, w: m.w_in, h: m.h_in });
}
const txt = (t, x, y, w, h, o) =>
  s.addText(t, Object.assign({ x, y, w, h, margin: 0, fontFace: ARIAL }, o));
const sub = (base, n, color) => [
  { text: base, options: { italic: true, color, fontFace: MATHF } },
  { text: String(n), options: { italic: true, color, subscript: true, fontFace: MATHF } },
];

// top red box (cream fill per original): training/test vectors + constraints
rbox([0.07, 0.03, 0.93, 0.30], "C00000", true, "FFF6DC");
const tOpt = { align: "center", valign: "middle", fontSize: 14, bold: true, color: "C00000" };
txt("Training Vectors", X(0.08), Y(0.042), BW(0.08, 0.45), 0.24, tOpt);
txt("Test Vectors", X(0.45), Y(0.042), BW(0.45, 0.63), 0.24, tOpt);

function vecBlock(x0, x1, base, vecs, ys) {
  const cw = BW(x0, x1) / vecs.length;
  vecs.forEach((v, i) => {
    txt(sub(base, i + 1, "C00000"), X(x0) + i * cw, Y(0.088), cw, 0.24,
      { align: "center", valign: "middle", fontSize: 14 });
    const m = MAN[v];
    s.addImage({ path: path.join(EQ, v + ".png"),
      x: X(x0) + i * cw + (cw - m.w_in) / 2, y: Y(0.122), w: m.w_in, h: m.h_in });
    if (ys) {
      const ym = MAN[ys[i]];
      s.addImage({ path: path.join(EQ, ys[i] + ".png"),
        x: X(x0) + i * cw + (cw - ym.w_in) / 2, y: Y(0.245), w: ym.w_in, h: ym.h_in });
    }
  });
}
vecBlock(0.08, 0.45, "x", ["rb3f2_vec_x1", "rb3f2_vec_x2", "rb3f2_vec_x3", "rb3f2_vec_x4"],
  ["rb3f2_y1", "rb3f2_y2", "rb3f2_y3", "rb3f2_y4"]);
vecBlock(0.45, 0.63, "T", ["rb3f2_vec_T1", "rb3f2_vec_T2", "rb3f2_vec_T3"], null);

// "Use C=1" box + blue-framed top-right constraint equations
rbox([0.65, 0.05, 0.76, 0.12], "C00000", false);
txt("Use C=1", X(0.65), Y(0.05), BW(0.65, 0.76), BH(0.05, 0.12),
  { align: "center", valign: "middle", fontSize: 13, color: "000000" });
rbox([0.63, 0.125, 0.92, 0.29], "0070C0");
img("rb3f2_topcons", X(0.63), Y(0.135), BW(0.63, 0.92));

// middle blue box: dual formulation equation (2D stacked sums, MAJOR fix)
rbox([0.08, 0.32, 0.92, 0.40], "0070C0");
img("rb3f_eq_dual", X(0.08), Y(0.318), BW(0.08, 0.92));

// lower-middle red box: kernel matrix expansion (blocks + arrow + line per spec)
rbox([0.08, 0.44, 0.92, 0.68], "C00000");
const my = Y(0.452);
img("rb3_blockA", X(0.095), my);
img("rb3_blockB", X(0.295), my);
s.addShape(pres.shapes.RIGHT_ARROW, { x: X(0.50), y: Y(0.55), w: BW(0.50, 0.53),
  h: BH(0.55, 0.60), fill: { color: "C00000" }, line: { color: "C00000" }, rotate: 43 });
s.addShape(pres.shapes.LINE, { x: X(0.53), y: Y(0.58), w: BW(0.53, 0.58),
  h: BH(0.58, 0.62), line: { color: "C00000", width: 1.5 } });
img("rb3_blockC", X(0.555), my);
img("rb3_blockD", X(0.715), my);

// bottom red box (pink fill per original): QP expansion + constraints + caption
rbox([0.07, 0.69, 0.93, 0.94], "C00000", true, "FADBD8");
img("rb3_eq_qp", X(0.09), Y(0.705), BW(0.09, 0.91));
txt("Subject to:", X(0.10), Y(0.815), 2.0, 0.22,
  { align: "left", valign: "middle", fontSize: 13, bold: true, color: "000000" });
img("rb3f2_cons_l", X(0.10), Y(0.845));
img("rb3f2_cons_r", X(0.10) + MAN.rb3f2_cons_l.w_in + 0.25, Y(0.845));
txt("Quadratic Equation in \u03b1 with constraints", X(0.52), Y(0.82), BW(0.52, 0.90), 0.34,
  { align: "center", valign: "middle", fontSize: 16, bold: true, color: "C00000", fontFace: MATHF });

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
