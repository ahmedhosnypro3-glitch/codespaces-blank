// slide_006.js — rb5_ dejavusans mathtext assets + house chrome.
// Round-2 fixes: panel-2 Gx<=h chip moved fully inside panel 2; chips salmon-filled.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx", "build", "eq_006") + "/";
const W = 13.33, H = 7.5;
const SANS = "Arial";
const RED = "C00000", LABEL_RED = "FF0000", GREEN = "008000", ORANGE = "FF8C00", BLACK = "000000";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("6", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: SANS, margin: 0,
});
s.addText("Less Than Equal Constraints", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: RED, fontFace: SANS, margin: 0,
});

function meta(name) { return JSON.parse(fs.readFileSync(EQ + "rb5_" + name + ".json")); }
function imgC(name, cx, cy) {
  const j = meta(name);
  s.addImage({ path: EQ + "rb5_" + name + ".png", x: cx - j.w_in / 2, y: cy - j.h_in / 2, w: j.w_in });
}
function imgL(name, x, bandY, bandH) {
  const j = meta(name);
  s.addImage({ path: EQ + "rb5_" + name + ".png", x, y: bandY + (bandH - j.h_in) / 2, w: j.w_in });
}
function txt(x, y, w, h, runs, extra) {
  s.addText(runs, Object.assign({ x, y, w, h, margin: 0, valign: "middle", fontFace: SANS }, extra));
}
const run = (text, o) => ({ text, options: Object.assign({ fontSize: 11, color: BLACK }, o) });

function container(y0n, y1n) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.03 * W, y: y0n * H, w: (0.97 - 0.03) * W, h: (y1n - y0n) * H,
    fill: { color: "FFFFFF" }, line: { color: RED, width: 0.75 },
  });
}
container(0.160, 0.345);
container(0.350, 0.580);
container(0.585, 0.900);

function gxChip(x0n, y0n, x1n, y1n) {
  const x = x0n * W, y = y0n * H, w = (x1n - x0n) * W, h = (y1n - y0n) * H;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, fill: { color: "F4CCCC" }, line: { color: LABEL_RED, width: 1.25 },
  });
  imgC("gxleh", x + w / 2, y + h / 2);
}
gxChip(0.672, 0.246, 0.790, 0.285);
gxChip(0.675, 0.700, 0.790, 0.740);

s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.674 * W, y: 0.375 * H, w: (0.902 - 0.674) * W, h: (0.535 - 0.375) * H,
  fill: { color: "FFF8DC" }, line: { color: "808080", width: 0.75 },
});
const convCx = (0.674 + 0.902) / 2 * W;
txt(0.063 * W, 0.19 * H, (0.19 - 0.063) * W, 0.375,
  [run("3 constraints", { bold: true, italic: true, color: LABEL_RED, fontSize: 14 })],
  { align: "left" });
txt(0.063 * W, 0.615 * H, (0.22 - 0.063) * W, 0.3375,
  [run("6 constraints , 3 variables", { bold: true, italic: true, color: LABEL_RED, fontSize: 14 })],
  { align: "left" });

txt(0.674 * W, 0.385 * H, (0.902 - 0.674) * W, 0.3,
  [run("Convert", { bold: true, italic: true, color: ORANGE, fontSize: 11 })],
  { align: "center" });
{
  const j1 = meta("conv1");
  s.addImage({ path: EQ + "rb5_conv1.png", x: convCx - j1.w_in / 2, y: 0.435 * H + (0.225 - j1.h_in) / 2, w: j1.w_in });
  const j2 = meta("conv2");
  s.addImage({ path: EQ + "rb5_conv2.png", x: convCx - j2.w_in / 2, y: 0.485 * H + (0.225 - j2.h_in) / 2, w: j2.w_in });
}
txt(0.674 * W, 0.468 * H, (0.902 - 0.674) * W, 0.22,
  [run("to", { color: GREEN, fontSize: 11 })], { align: "center" });

imgL("le_str", 0.065 * W, 0.237 * H, (0.275 - 0.237) * H);
imgC("arrow", 0.35 * W, 2.04375);
imgC("m3id", (0.365 + 0.475) / 2 * W, 2.04375);
imgC("vx3", (0.53 + 0.56) / 2 * W, 2.04375);
imgC("leq", 0.58 * W, 2.04375);
imgC("vz3", (0.635 + 0.67) / 2 * W, 2.04375);

imgL("ge_str", 0.065 * W, 0.385 * H, (0.425 - 0.385) * H);
imgC("arrow", 0.35 * W, 3.20625);
imgC("m3neg", (0.365 + 0.475) / 2 * W, 3.20625);
imgC("vx3", (0.53 + 0.56) / 2 * W, 3.20625);
imgC("leq", 0.58 * W, 3.20625);
imgC("vnegz3", (0.635 + 0.67) / 2 * W, 3.20625);

imgL("chain_str", 0.065 * W, 0.665 * H, (0.705 - 0.665) * H);
imgC("arrow", 0.35 * W, 5.45625);
imgC("m6", (0.365 + 0.48) / 2 * W, 5.45625);
imgC("vx3", (0.53 + 0.56) / 2 * W, 5.45625);
imgC("leq", 0.58 * W, 5.45625);
imgC("vyz6", (0.635 + 0.675) / 2 * W, 5.45625);
txt(0.445 * W, 0.795 * H, (0.505 - 0.445) * W, 0.225,
  [run("6 x 3", { color: LABEL_RED, fontSize: 10 })], { align: "center" });

pres.writeFile({ fileName: path.join(NS, "recreated_pptx", "slide_006_recreated.pptx") });
console.log("wrote slide_006_recreated.pptx");
