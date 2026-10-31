from PIL import Image
V="/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
B=f"{V}/recreated_pptx/build"
orig=Image.open(f"{V}/unique_slides/slide_018.jpg").convert("RGB")
rend=Image.open(f"{B}/slide_018_rejudge_rendered-1.png").convert("RGB")
print("orig",orig.size,"rend",rend.size)
def ox(o): return (0.15+(o-57)/846*13.03)*150.13
def oy(o): return (0.15+(o-43)/474*7.2)*150
def at(im,o):
    return im.getpixel((int(round(ox(o))),int(round(oy(o)))))
print("ORIG bipolar shaft column x=645, y 250..268:")
for y in range(250,269):
    print("  y",y, [orig.getpixel((x,y)) for x in range(643,648)])
print("REND bipolar shaft: render px for orig x=645:")
rx=ox(645); ry0=oy(250); ry1=oy(268)
print("  rx",rx,"ry",ry0,ry1)
for y in range(int(ry0),int(ry1)+1):
    print("  ry",y,[rend.getpixel((int(rx)+d,y)) for d in (-1,0,1)])
