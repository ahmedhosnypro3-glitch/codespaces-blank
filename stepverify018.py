from PIL import Image
V="/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
B=f"{V}/recreated_pptx/build"
S=300/72.0
def probe(name,box,pts,label):
    im=Image.open(f"{B}/{name}").convert("RGB")
    print("==",name,label)
    for item in pts:
        fx,fy,tag=item
        x0,y0=box[0],box[1]
        q,p=int(round((fx-x0)*S)),int(round((fy-y0)*S))
        print(f"  {tag}: frame({fx},{fy}) png({q},{p}) -> {im.getpixel((q,p))}")
probe("slide_018_unipolar_step.png",(70,168,340,274),
  [(230,194,"hi-plateau gold"),(150,225,"lo-plateau gold"),(194,210,"jump pink"),
   (292,194,"crimson head"),(195,240,"shaft grey"),(180,205,"ellipse yellow"),
   (240,224,"gold below axis")],"uni")
probe("slide_018_bipolar_step.png",(509,168,780,274),
  [(680,194,"hi-plateau gold"),(600,252,"lo-plateau gold"),(645,225,"jump"),
   (645,258,"shaft below low"),(600,258,"ellipse yellow"),(680,195,"hi plateau lower edge")],"bip")
