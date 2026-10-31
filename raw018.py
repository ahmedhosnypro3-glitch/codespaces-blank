from PIL import Image
V="/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
orig=Image.open(f"{V}/unique_slides/slide_018.jpg").convert("RGB")
def row(y,x0,x1):
    print(f"--- orig y={y}")
    for x in range(x0,x1):
        p=orig.getpixel((x,y))
        tag=""
        if p==(255,255,255): tag=""
        elif p[0]>245 and p[1]>245 and p[2]>125: tag="Y"
        elif abs(p[0]-206)<40 and abs(p[1]-160)<45 and p[2]<95: tag="G"
        elif p[0]<120 and p[1]<60 and p[2]<70: tag="K"
        elif abs(p[0]-196)<50 and abs(p[1]-94)<50 and abs(p[2]-108)<40: tag="P"
        elif max(p)<130: tag="S"
        else: tag="?"
        print(f"  x{x} {p} {tag}")
# UNIPOLAR high plateau
for y in (193,194,195,196):
    row(y,190,300)
