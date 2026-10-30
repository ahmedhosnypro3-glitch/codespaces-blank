
from PIL import Image, ImageDraw, ImageFont
S=4
COLS=[99,122,144,165,189,212]
COLS_V=[["1","1","1"],["1","2","1"],["1","1","2"],["1","5","4"],["1","6","5"],["1","6","6"]]
CLS=["C1","C1","C1","C2","C2","C2"]
COLORS=["#C00000","#C00000","#C00000","#0000FF","#0000FF","#0000FF"]
FONT=r'''/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'''
BOLD=r'''/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'''
W=(232-86+1)*S; H=(242-182+1)*S
img=Image.new("RGBA",(W,H),(0,0,0,0))
d=ImageDraw.Draw(img)
f=lambda pt: ImageFont.truetype(FONT, int(round(pt*S)))
fb=lambda pt: ImageFont.truetype(BOLD, int(round(pt*S)))
VT,VB=183,223
CY=(VT+VB)//2
def cell(txt,pt,cx,cy,col,bold=False):
    ft=fb(pt) if bold else f(pt)
    bb=d.textbbox((0,0),txt,font=ft)
    tw,th=bb[2]-bb[0],bb[3]-bb[1]
    d.text(((cx-86)*S-(tw/2)-bb[0], (cy-182)*S-(th/2)-bb[1]), txt, font=ft, fill=col)
# 6 stacked column vectors: ( a ; b ; c ) with tall parens flanking the digits
for i,c in enumerate(COLS):
    cx=COLS[i]
    top,bot=VT,VB
    vals=COLS_V[i]
    n=len(vals)
    step=(bot-top-10)//(n-1) if n>1 else 0
    ys=[top+5+k*step for k in range(n)] if n>1 else [CY]
    for v,yy in zip(vals,ys):
        cell(v,11,cx,yy,"#000000")
    OFF=7          # frame px from column centre to each paren stroke
    for ch,poff in (("(",-OFF),(")",OFF)):
        ft=f(bot-top)                       # render the glyph as tall as the span
        bb=d.textbbox((0,0),ch,font=ft)
        big=Image.new("RGBA",(max(4,bb[2]-bb[0]+4), max(4,bb[3]-bb[1]+4)),(0,0,0,0))
        ImageDraw.Draw(big).text((-bb[0]+2,-bb[1]+2),ch,font=ft,fill="#000000")
        th=int(round((bot-top)*S))
        tw=max(2,int(round(0.10*S)))        # ~3 frame px wide, height spans the vector
        big=big.resize((tw,th),Image.LANCZOS)
        img.paste(big,(int(round((cx+poff-86)*S)),int(round((top-182)*S))),big)
# class row
for i,c in enumerate(CLS):
    cell(c,12,COLS[i],233+5,COLORS[i],bold=True)
img.save(r'''/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/aug_043.png''')
print("WROTE",r'''/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/aug_043.png''', img.size)
