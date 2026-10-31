from PIL import Image
B="/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
S=300/72.0
for name,box,xs,ys in (("slide_018_unipolar_step.png",(70,168,340,274),195,225),
                       ("slide_018_bipolar_step.png",(509,168,780,274),645,225)):
    im=Image.open(f"{B}/{name}").convert("RGB")
    px,py=im.size
    x0,y0,x1,y1=box
    def P(fx,fy): return (int(round((fx-x0)*S)), int(round((fy-y0)*S)))
    print(name, im.size)
    for fy in range(180,270,2):
        q,p=P(xs,fy)
        row=[]
        for fx in range(xs-3,xs+4):
            r,rr=P(fx,fy)
            row.append(im.getpixel((r,rr)) if 0<=r<px and 0<=rr<py else None)
        print(f"  fy={fy} (px {p}) {im.getpixel((q,p)) if 0<=q<px else None}  row+-3={row}")
