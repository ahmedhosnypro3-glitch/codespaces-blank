const pptxgen = require("pptxgenjs");
const path = require("path");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_013");
const M = require(path.join(EQ, "manifest.json"));
const X = v => v * 13.33, Y = v => v * 7.5;
const W = 13.33, H = 7.5;
const SERIF = "Times New Roman";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

function rect(x0, y0, x1, y1, line, lw, fill) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: line, width: lw },
  });
}
function rrect(x0, y0, x1, y1, line, fill) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    fill: { color: fill }, line: { color: line, width: 1.25 },
  });
}
function imgC(name, x0, y0, x1, y1) {
  const m = M[name];
  s.addImage({ path: m.path, x: X(x0) + (X(x1 - x0) - m.w_in) / 2,
    y: Y(y0) + (Y(y1 - y0) - m.h_in) / 2, w: m.w_in, h: m.h_in });
}
function txt(text, x0, y0, x1, y1, o) {
  s.addText(text, Object.assign(
    { x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0), margin: 0 }, o));
}

// ---- house chrome ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("13", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
txt("", 0.6 / 13.33, 0.28 / 7.5, 12.73 / 13.33, 0.9 / 7.5,
  { align: "center", fontSize: 20, bold: true, color: "C00000" });

// ---- upper red panel (QP formulation) ----
rect(0.071, 0.120, 0.815, 0.372, "FF0000", 1.5);
txt("Minimize:", 0.075, 0.133, 0.142, 0.165,
  { fontSize: 11, bold: true, italic: true, color: "FF0000", fontFace: SERIF });
imgC("obj", 0.154, 0.128, 0.592, 0.170);
txt("Subject to:", 0.075, 0.194, 0.135, 0.226,
  { fontSize: 11, bold: true, italic: true, color: "FF0000", fontFace: SERIF });
imgC("constr", 0.170, 0.176, 0.808, 0.219);
// constraint list rows (small boxes + expanded strings)
rect(0.074, 0.235, 0.121, 0.276, "0000FF", 1);
imgC("sumbox", 0.074, 0.235, 0.121, 0.276);
imgC("exp1", 0.166, 0.241, 0.283, 0.272);
rect(0.074, 0.281, 0.117, 0.320, "FF0000", 1);
imgC("alphaleC", 0.074, 0.281, 0.117, 0.320);
imgC("listle", 0.166, 0.281, 0.381, 0.311);
rect(0.074, 0.322, 0.117, 0.359, "FF0000", 1);
imgC("alphage0", 0.074, 0.322, 0.117, 0.359);
imgC("listge", 0.166, 0.322, 0.381, 0.352);
txt([
  { text: "Quadratic Equation in ", options: { fontSize: 14, bold: true, color: "FF0000", fontFace: SERIF } },
  { text: "\u03b1", options: { fontSize: 14, bold: true, italic: true, color: "0000A0", fontFace: SERIF } },
  { text: " with constraints", options: { fontSize: 14, bold: true, color: "FF0000", fontFace: SERIF } },
], 0.422, 0.281, 0.721, 0.330, { margin: 0 });

// ---- middle red band ----
rect(0.071, 0.389, 0.627, 0.522, "FF0000", 1.5);
imgC("listge", 0.075, 0.413, 0.283, 0.444);
rect(0.071, 0.450, 0.300, 0.496, "FF0000", 1);
imgC("listle", 0.075, 0.452, 0.295, 0.494);
imgC("arrow", 0.321, 0.411, 0.342, 0.444);
rrect(0.352, 0.415, 0.622, 0.465, "FFA500", "FFFDE7");
imgC("negalpha", 0.352, 0.415, 0.622, 0.465);
rrect(0.644, 0.376, 0.729, 0.422, "FFA500", "FFFDE7");
imgC("gxleh", 0.644, 0.376, 0.729, 0.422);
rrect(0.733, 0.376, 0.814, 0.422, "FFA500", "FFFDE7");
imgC("axeb", 0.733, 0.376, 0.814, 0.422);
// ---- bottom row: G, h, A, b panels (blue border, cyan back) ----
rect(0.097, 0.528, 0.339, 0.844, "0000FF", 1.5, "E0FFFF");
txt("G =", 0.106, 0.663, 0.133, 0.707,
  { fontSize: 13, bold: true, color: "FF0000", fontFace: SERIF });
for (let i = 0; i < 8; i++) {
  const m = M["g_row" + (i + 1)];
  s.addImage({ path: m.path, x: X(0.136), y: Y(0.544) + i * Y(0.0395), w: m.w_in, h: m.h_in });
}
imgC("alphavec", 0.302, 0.548, 0.328, 0.715);
rect(0.351, 0.528, 0.429, 0.844, "0000FF", 1.5, "E0FFFF");
txt("h =", 0.360, 0.652, 0.390, 0.700,
  { fontSize: 13, bold: true, color: "FF0000", fontFace: SERIF });
imgC("hvec", 0.392, 0.544, 0.424, 0.826);
rect(0.447, 0.528, 0.682, 0.678, "0000FF", 1.5, "E0FFFF");
imgC("arow", 0.457, 0.541, 0.646, 0.593);
imgC("alphavec", 0.644, 0.539, 0.672, 0.659);
rect(0.705, 0.533, 0.795, 0.594, "0000FF", 1.5, "E0FFFF");
imgC("brow", 0.715, 0.541, 0.783, 0.587);

// ---- green Solution arrow (external callout) + solution box ----
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: X(0.503), y: Y(0.707), w: X(0.195), h: Y(0.110),
  fill: { color: "E9F9E9" }, line: { color: "00A000", width: 1.5 },
});
txt("Solution", 0.503, 0.707, 0.698, 0.817,
  { align: "center", valign: "middle", fontSize: 12, bold: true, italic: true,
    color: "00A000", fontFace: "Arial" });
rect(0.708, 0.676, 0.842, 0.844, "00B050", 1.5);
imgC("sol", 0.717, 0.694, 0.831, 0.830);

// ---- bottom player bar ----
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.036), y: Y(0.856), w: X(0.855), h: Y(0.144),
  fill: { color: "000000" }, line: { color: "000000" },
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_013_recreated.pptx") })
  .then(() => console.log("wrote slide_013_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
