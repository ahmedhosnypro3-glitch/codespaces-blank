const pptxgen = require("pptxgenjs");
const path = require("path");
const { newPres, addHouseChrome, W, H } = require("./shared.js");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const NUM = 43;
// Spec qa/reanalysis2/slide_043_analysis.txt (from line "1. SLIDE_TITLE"):
// SLIDE_TITLE: none. Scatter plot only. Plot area [0.23,0.14,0.76,0.82],
// y labels [0.20,0.12,0.23,0.82], x labels [0.23,0.82,0.76,0.87] — all rendered
// into the pre-generated plot PNG covering [0.20,0.12,0.76,0.87] (matches spec).
const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, NUM, null);

// Generated plot (gen_graph_043.py): 1492x1125 px @200dpi = 7.46 x 5.625 in,
// placed at the spec region [0.20,0.12,0.76,0.87] -> exact size, no rescale.
const GX = 0.20 * W, GY = 0.12 * H, GW = (0.76 - 0.20) * W, GH = (0.87 - 0.12) * H;
s.addImage({
  path: path.join(NS, "recreated_pptx/build/slide_043_graph.png"),
  x: GX, y: GY, w: GW, h: GH,
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_043_recreated.pptx") })
  .then(() => console.log("wrote slide_043_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
