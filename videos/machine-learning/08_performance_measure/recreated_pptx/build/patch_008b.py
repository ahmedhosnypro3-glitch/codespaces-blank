import sys
p = 'build/slide_008.js'
src = open(p).read()
def rep(old, new):
    global src
    assert old in src, old[:70]
    src = src.replace(old, new, 1)

rep('{ text: "% of what you ", options: { fontSize: 17, bold: true, color: INK, fontFace: FONT, breakLine: false } }',
    '{ text: "% of what you ", options: { fontSize: 17, bold: true, charSpacing: 1.4, color: INK, fontFace: FONT, breakLine: false } }')
rep('{ text: "Predicted", options: { fontSize: 17, bold: true, underline: true, color: RED, fontFace: FONT, breakLine: false } }',
    '{ text: "Predicted", options: { fontSize: 17, bold: true, underline: true, charSpacing: 1.5, color: RED, fontFace: FONT, breakLine: false } }')
rep('{ text: " as ", options: { fontSize: 17, bold: true, color: INK, fontFace: FONT, breakLine: false } }',
    '{ text: " as ", options: { fontSize: 17, bold: true, charSpacing: 1.4, color: INK, fontFace: FONT, breakLine: false } }')
rep('{ text: "POSITIVE", options: { fontSize: 17, bold: true, color: BLUE, fontFace: FONT, breakLine: false } }',
    '{ text: "POSITIVE", options: { fontSize: 17, bold: true, charSpacing: 3, color: BLUE, fontFace: FONT, breakLine: false } }')
rep('{ text: " is Actually Positive", options: { fontSize: 17, bold: true, color: INK, fontFace: FONT, breakLine: false } }',
    '{ text: " is Actually Positive", options: { fontSize: 17, bold: true, charSpacing: 1.4, color: INK, fontFace: FONT, breakLine: false } }')
rep('x: P(86), y: P(284), w: P(140), h: P(28), align: "left", valign: "middle",\n  fontSize: 24, bold: true',
    'x: P(86), y: P(283), w: P(140), h: P(30), align: "left", valign: "middle",\n  fontSize: 26, bold: true')
open(p, 'w').write(src)
print('patched2 OK')
