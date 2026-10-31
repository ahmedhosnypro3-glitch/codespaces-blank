import sys
p = 'build/slide_008.js'
src = open(p).read()
def rep(old, new, cnt=1):
    global src
    assert old in src, old[:70]
    src = src.replace(old, new, cnt)

rep('fontSize: 42, bold: true, color: RED', 'fontSize: 46, bold: true, color: RED')
rep('x: P(67), y: P(118), w: P(573), h: P(22), align: "center", valign: "middle",\n  fontSize: 17, bold: true',
    'x: P(67), y: P(118), w: P(573), h: P(22), align: "center", valign: "middle",\n  fontSize: 19, bold: true')
rep('x: P(67), y: P(151), w: P(573), h: P(21), align: "center", valign: "middle",\n  fontSize: 17, bold: true',
    'x: P(67), y: P(151), w: P(573), h: P(21), align: "center", valign: "middle",\n  fontSize: 19, bold: true')
rep('x: P(79), y: P(139), w: P(552), h: P(3)', 'x: P(81), y: P(139), w: P(558), h: P(3)')
rep('x: P(80), y: P(205), w: P(92), h: P(25), align: "left", valign: "middle",\n  fontSize: 20, bold: true',
    'x: P(80), y: P(205), w: P(92), h: P(25), align: "left", valign: "middle",\n  fontSize: 22, bold: true')
rep('fontSize: 17, color: INK, fontFace: FONT, breakLine: false } },\n  { text: "Predicted"',
    'fontSize: 17, bold: true, color: INK, fontFace: FONT, breakLine: false } },\n  { text: "Predicted"')
rep('fontSize: 17, color: INK, fontFace: FONT, breakLine: false } },\n  { text: "POSITIVE"',
    'fontSize: 17, bold: true, color: INK, fontFace: FONT, breakLine: false } },\n  { text: "POSITIVE"')
rep('{ text: " is Actually Positive", options: { fontSize: 17, color: INK',
    '{ text: " is Actually Positive", options: { fontSize: 17, bold: true, color: INK')
rep('x: P(67), y: P(262), w: P(263), h: P(60),', 'x: P(67), y: P(262), w: P(249), h: P(60),')
rep('x: P(86), y: P(284), w: P(140), h: P(28), align: "left", valign: "middle",\n  fontSize: 20, bold: true',
    'x: P(86), y: P(284), w: P(140), h: P(28), align: "left", valign: "middle",\n  fontSize: 24, bold: true')
rep('x: P(228), y: P(278), w: 0.76333, h: 0.37833', 'x: P(226), y: P(276), w: 0.76333, h: 0.37833')
rep('x: P(341), y: P(293), w: 2.31667, h: 0.25', 'x: P(341), y: P(298), w: 2.31667, h: 0.25')
rep('x: P(67), y: P(430), w: P(477), h: P(82),', 'x: P(72), y: P(431), w: P(427), h: P(83),')
src = src.replace('fontSize: 12, italic: true, color: BLUE', 'fontSize: 15, italic: true, color: BLUE')
src = src.replace('fontSize: 12, italic: true, bold: true, color: BLUE', 'fontSize: 15, italic: true, bold: true, color: BLUE')
src = src.replace('fontSize: 12, italic: true, bold: true, underline: true, color: BLUE', 'fontSize: 15, italic: true, bold: true, underline: true, color: BLUE')
src = src.replace('fontSize: 12, italic: true, bold: true, color: RED', 'fontSize: 15, italic: true, bold: true, color: RED')
rep('x: P(79), y: P(434), w: P(420), h: P(74), align: "left", valign: "top",\n  margin: 0, lineSpacing: 20',
    'x: P(79), y: P(435), w: P(412), h: P(76), align: "left", valign: "top",\n  margin: 0, lineSpacing: 20')
rep('x: P(737), y: P(100), w: P(53), h: P(24), fill: { color: GREEN }', 'x: P(749), y: P(101), w: P(39), h: P(23), fill: { color: GREEN }')
rep('x: P(790), y: P(127), w: P(54), h: P(23), fill: { color: GREEN }', 'x: P(799), y: P(127), w: P(39), h: P(23), fill: { color: GREEN }')
rep('x: P(790), y: P(252), w: P(54), h: P(30), fill: { color: GREEN }', 'x: P(808), y: P(254), w: P(40), h: P(27), fill: { color: GREEN }')
rep('x: P(536), y: P(298), w: P(344), h: P(205),', 'x: P(536), y: P(291), w: P(346), h: P(212),')
open(p, 'w').write(src)
print('patched OK')
