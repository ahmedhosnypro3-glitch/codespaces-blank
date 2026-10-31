// slide_018.js — FRESH rebuild wave 3 from qa/reanalysis2/slide_018_analysis.txt
// Build from project root: cd /home/codespace/ai_llm_slides && node <NS>/recreated_pptx/build/slide_018.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const NUM = 18;
const TITLE = "Non-Linearly Separable Data";
const W = 13.33, H = 7.5;
const ARIAL = "Arial";
const SERIF = "Times New Roman";
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const BUILD = NS + "/recreated_pptx/build";
const eqMap = require(BUILD + "/eq_018/eq18_map_rb3.json");
const eqCol = require(BUILD + "/eq_018/eq18_colvec_rb4.json");
const graph = require(BUILD + "/slide_018_graph_rb4.png.json");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (overrides spec): outer red frame, badge, title box
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
  fontSize: 18, bold: true, color: "333333", fontFace: ARIAL, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 14, bold: true, color: "C00000", fontFace: ARIAL, margin: 0,
});

// Inner red content frame [0.088,0.168,0.896,0.917]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.088 * W, y: 0.168 * H, w: (0.896 - 0.088) * W, h: (0.917 - 0.168) * H,
  fill: { type: "none" }, line: { color: "CC0000", width: 1.5 },
});

// Mapping panel [0.105,0.228,0.313,0.463], white fill, #CC3300 border
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.105 * W, y: 0.228 * H, w: (0.313 - 0.105) * W, h: (0.463 - 0.228) * H,
  fill: { color: "FFFFFF" }, line: { color: "CC3300", width: 1.5 },
});
// "Mapping" heading, blue bold italic serif [0.117,0.248,0.190,0.278]
s.addText("Mapping", {
  x: 0.117 * W, y: 0.248 * H, w: 0.073 * W, h: 0.030 * H,
  align: "left", valign: "middle",
  fontSize: 13, bold: true, italic: true, color: "0000CC", fontFace: SERIF, margin: 0,
});
// "Z => phi(Z)" mathtext PNG on the same row, right-aligned to [..,0.288,0.282]
{
  const rowY = 0.248 * H, rowH = (0.282 - 0.248) * H;
  s.addImage({
    path: path.join(BUILD, eqMap.path),
    x: 0.288 * W - eqMap.w_in, y: rowY + (rowH - eqMap.h_in) / 2,
    w: eqMap.w_in, h: eqMap.h_in,
  });
}
// Column-vector mapping equation PNG, centred in [0.117,0.325,0.300,0.443]
{
  const bx = 0.117 * W, by = 0.325 * H, bw = (0.300 - 0.117) * W, bh = (0.443 - 0.325) * H;
  s.addImage({
    path: path.join(BUILD, eqCol.path),
    x: bx + (bw - eqCol.w_in) / 2, y: by + (bh - eqCol.h_in) / 2,
    w: eqCol.w_in, h: eqCol.h_in,
  });
}

// Note box [0.682,0.268,0.888,0.367], red border, two red italic serif lines
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.682 * W, y: 0.268 * H, w: (0.888 - 0.682) * W, h: (0.367 - 0.268) * H,
  fill: { color: "FFFFFF" }, line: { color: "CC0000", width: 1.25 },
});
s.addText("Data is linearly separable\nIn the new representation", {
  x: 0.690 * W, y: 0.288 * H, w: (0.868 - 0.690) * W, h: (0.352 - 0.288) * H,
  align: "left", valign: "middle", lineSpacing: 15,
  fontSize: 11, italic: true, color: "CC0000", fontFace: SERIF, margin: 0,
});
// 3-D diagram PNG spanning [0.300,0.265,0.788,0.902]
s.addImage({
  path: path.join(BUILD, graph.path),
  x: 0.300 * W, y: 0.265 * H, w: graph.w_in, h: graph.h_in,
});

// Callout box [0.748,0.549,0.846,0.654], blue border, three centred lines
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.748 * W, y: 0.549 * H, w: (0.846 - 0.748) * W, h: (0.654 - 0.549) * H,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.25 },
});
s.addText("Linear\nDecision\nBoundary", {
  x: 0.748 * W, y: 0.549 * H, w: (0.846 - 0.748) * W, h: (0.654 - 0.549) * H,
  align: "center", valign: "middle", lineSpacing: 12,
  fontSize: 10, bold: true, italic: true, color: "0000FF", fontFace: SERIF, margin: 0,
});

// Blue leader line [0.700,0.532 -> 0.783,0.589] from boundary to callout
s.addShape(pres.shapes.LINE, {
  x: 0.700 * W, y: 0.532 * H, w: (0.783 - 0.700) * W, h: (0.589 - 0.532) * H,
  line: { color: "0000FF", width: 1.5 },
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_018_recreated.pptx") })
  .then(() => console.log("wrote slide_018_recreated.pptx"))
  .catch(e => console.error(e));
