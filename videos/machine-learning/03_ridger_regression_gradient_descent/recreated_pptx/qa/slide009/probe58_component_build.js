// probes: build a pptx ENTIRELY from the banked component (no local geometry
// duplicates) into a scratch QA path, so qa/slide009/component_fidelity.py can
// pixel-diff its render against the certified slide_009_recreated.pptx render.
// This proves components/slide_009.js is a faithful banked composition — the
// deliverable stays the single plain-named slide_009_recreated.pptx (single-version
// law); this file is evidence, never a deliverable.
const pptxgen = require("pptxgenjs");
const comp = require("../../build/components/slide_009.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/component_build_probe.pptx";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
comp.renderBase(pptx, slide, {});   // full slide, default numeral 9

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
