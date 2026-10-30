const path = require("path");
const pptxgen = require("/workspaces/codespaces-blank/ai_llm_slides/node_modules/pptxgenjs");
const C = require("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/components/slide_012.js");
const out = process.argv[2];
const opts = process.argv[3] ? eval("(" + process.argv[3] + ")") : {};
const p = new pptxgen(); p.layout = "LAYOUT_WIDE";
const s = p.addSlide();
C.renderBase(p, s, opts);
p.writeFile({ fileName: out }).then(() => console.log(out));
