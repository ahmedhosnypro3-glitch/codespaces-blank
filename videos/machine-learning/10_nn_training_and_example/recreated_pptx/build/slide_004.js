// Build: recreated_pptx/build/slide_004.js
// Slide 4 — Remember: Derivative of Sigmoid Function
// Source: unique_slides/slide_004.jpg (+ analysis/slide_004_raw.json + parse)
// House chrome: machine-learning family

const pptxgen = require("pptxgenjs");
const fs = require("fs");

const ROOT = "/home/codespace/ai_llm_slides";
const VID = ROOT + "/videos/machine-learning/10_nn_training_and_example";
const ASSETS = VID + "/recreated_pptx/build/assets/slide_004";
const NUM = 4;
const S = 13.33 / 960;
function px(v) { return +(v * S).toFixed(4); }

const FONT = "Arial";
const TITLE = "Derivative of Sigmoid Function";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// --- House chrome ------------------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3, fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText(String(NUM), { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0 });
s.addText("Remember:", { x: 0.6, y: 0.28, w: 2.0, h: 0.55, align: "left", valign: "top", fontSize: 24, bold: true, color: "0000FF", fontFace: FONT, margin: 0 });
s.addText(TITLE, { x: 2.6, y: 0.28, w: 10.13, h: 0.55, align: "left", valign: "top", fontSize: 24, bold: true, color: "CC0000", fontFace: FONT, margin: 0 });

// --- Layout per analysis regions ---------------------------------------------
// Left: O_j: annotation + definition box (cream)
// Center: Sigma diagram + green f(x) box
// Right: Sigmoid graph in blue-bordered box
// Middle: derivation boxes (3 stacked, white)
// Bottom-left: factored form (white)
// Bottom-right: orange result box with blue arrow

// O_j: annotation (blue, left of definition box)
s.addText("O_j:", { x: px(80), y: px(120), w: px(60), h: px(25), align: "right", valign: "middle", fontSize: 16, bold: false, color: "0000FF", fontFace: FONT, margin: 0 });

// Definition box (upper-left): f(Net_j) = 1 / (1 + e^(-Net_j))
// Box fill is drawn BEFORE its equation image: a transparent PNG must sit on
// top of the shape, otherwise the solid fill hides the equation.
const eq1 = JSON.parse(fs.readFileSync(ASSETS + "/eq1.png.meta.json", "utf8"));
s.addShape(pres.shapes.RECTANGLE, { x: px(135), y: px(105), w: eq1.w_in + px(10), h: eq1.h_in + px(10), fill: { color: "FFF8DC" }, line: { color: "000000", width: 1 } });
s.addImage({ path: ASSETS + "/eq1.png", x: px(140), y: px(110), w: eq1.w_in, h: eq1.h_in });

// Sigma diagram (center): blue circle Σ -> red dot Net_j -> arrow -> blue box f
const cx = px(380), cy = px(140);
s.addShape(pres.shapes.OVAL, { x: cx - px(25), y: cy - px(25), w: px(50), h: px(50), fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 2 } });
s.addText("\u03a3", { x: cx - px(25), y: cy - px(25), w: px(50), h: px(50), align: "center", valign: "middle", fontSize: 28, bold: true, color: "0000FF", fontFace: FONT, margin: 0 });

// Red dot with Net_j label
s.addShape(pres.shapes.OVAL, { x: cx + px(80), y: cy - px(12), w: px(24), h: px(24), fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 } });
s.addText("Net_j", { x: cx + px(110), y: cy - px(15), w: px(50), h: px(20), align: "left", valign: "middle", fontSize: 14, bold: true, color: "FF0000", fontFace: FONT, margin: 0 });

// Arrow to f box
s.addShape(pres.shapes.LINE, { x: cx + px(50), y: cy, w: px(60), h: 0, line: { color: "000000", width: 1.5, headEndType: "triangle" } });

// Blue f box
const fx = cx + px(115);
s.addShape(pres.shapes.RECTANGLE, { x: fx, y: cy - px(20), w: px(40), h: px(40), fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 2 } });
s.addText("f", { x: fx, y: cy - px(20), w: px(40), h: px(40), align: "center", valign: "middle", fontSize: 18, bold: true, color: "0000FF", fontFace: FONT, margin: 0 });

// Green f(x) box (right of diagram)
const eq2 = JSON.parse(fs.readFileSync(ASSETS + "/eq2.png.meta.json", "utf8"));
s.addShape(pres.shapes.RECTANGLE, { x: fx + px(50), y: cy - px(20), w: eq2.w_in + px(10), h: eq2.h_in + px(10), fill: { color: "90EE90" }, line: { color: "000000", width: 1 } });
s.addImage({ path: ASSETS + "/eq2.png", x: fx + px(55), y: cy - px(15), w: eq2.w_in, h: eq2.h_in });

// Sigmoid graph (upper-right) — 220x220px @72dpi = 3.05in square
s.addImage({ path: ASSETS + "/sigmoid_graph.png", x: px(700), y: px(80), w: 3.05, h: 3.05 });

// Derivation boxes - ensure they have content (not empty white boxes)
const boxLeftX = px(140);
const boxWidth = px(500); // wide enough for equations

// Derivation 1 box (middle-upper): f'(Net_j) = e^(-Net_j) / (1+e^(-Net_j))^2
const eq3 = JSON.parse(fs.readFileSync(ASSETS + "/eq3.png.meta.json", "utf8"));
const box1Y = px(250);
s.addShape(pres.shapes.RECTANGLE, { x: px(135), y: px(245), w: boxWidth, h: eq3.h_in + px(10), fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } });
s.addImage({ path: ASSETS + "/eq3.png", x: boxLeftX, y: box1Y, w: eq3.w_in, h: eq3.h_in });

// Derivation 2 box (middle-lower): f'(Net_j) = 1/(1+e^(-Net_j)) * ((1+e^(-Net_j))-1)/(1+e^(-Net_j))
const eq4 = JSON.parse(fs.readFileSync(ASSETS + "/eq4.png.meta.json", "utf8"));
const box2Y = px(330);
s.addShape(pres.shapes.RECTANGLE, { x: px(135), y: px(325), w: boxWidth, h: eq4.h_in + px(10), fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } });
s.addImage({ path: ASSETS + "/eq4.png", x: boxLeftX, y: box2Y, w: eq4.w_in, h: eq4.h_in });

// Derivation 3 box (bottom-left): f'(Net_j) = 1/(1+e^(-Net_j)) * (1 - 1/(1+e^(-Net_j)))
const eq5 = JSON.parse(fs.readFileSync(ASSETS + "/eq5.png.meta.json", "utf8"));
const box3Y = px(410);
s.addShape(pres.shapes.RECTANGLE, { x: px(135), y: px(405), w: boxWidth, h: eq5.h_in + px(10), fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } });
s.addImage({ path: ASSETS + "/eq5.png", x: boxLeftX, y: box3Y, w: eq5.w_in, h: eq5.h_in });

// Final result box (bottom-right, orange/peach): f'(Net_j) = O_j (1 - O_j)
const eq6 = JSON.parse(fs.readFileSync(ASSETS + "/eq6.png.meta.json", "utf8"));
const resX = px(700), resY = px(380);
s.addShape(pres.shapes.RECTANGLE, { x: resX, y: resY, w: eq6.w_in + px(20), h: eq6.h_in + px(20), fill: { color: "FFE4B5" }, line: { color: "FFA500", width: 2 } });
s.addImage({ path: ASSETS + "/eq6.png", x: resX + px(10), y: resY + px(10), w: eq6.w_in, h: eq6.h_in });

// Blue handwritten curved arrow pointing to orange box
s.addShape(pres.shapes.LINE, {
  x: resX - px(80), y: resY + eq6.h_in/2 + px(10),
  w: px(70), h: 0,
  line: { color: "0000FF", width: 2, headEndType: "triangle", dashType: "dash" }
});

// Net_j label on arrow from sigma to f box
s.addText("Net_j", { x: cx + px(55), y: cy - px(30), w: px(40), h: px(20), align: "center", valign: "middle", fontSize: 12, bold: true, color: "FF0000", fontFace: FONT, margin: 0 });

pres.writeFile({ fileName: VID + "/recreated_pptx/build/slide_004_recreated.pptx" })
  .then(() => console.log("wrote slide_004_recreated.pptx"))
  .catch((e) => { console.error(e); process.exit(1); });