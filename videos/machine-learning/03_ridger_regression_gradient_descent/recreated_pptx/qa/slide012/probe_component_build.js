// Probe: build slide 012 from the BANKED component and prove it matches the
// certified deliverable slide_012_recreated.pptx (render-pixel identity + shape
// geometry equality). Companion to components/slide_012.js.
const path = require("path");
const pptxgen = require("pptxgenjs");
const { renderBase } = require(path.resolve(__dirname, "../../build/components/slide_012.js"));

const OUT = path.resolve(__dirname, "component_build_probe.pptx");
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
renderBase(pptx, slide, { numeral: 12 });
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
