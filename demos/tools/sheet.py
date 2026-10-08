import sys
from PIL import Image, ImageDraw
def contact(paths, out, scale=2, maxw=1800, bg=(70,70,80)):
    ims=[]
    for p in paths:
        im=Image.open(p).convert('RGBA'); ims.append((p.split('/')[-1], im))
    # layout rows
    x=y=0; rowh=0; pos=[]
    for name,im in ims:
        w,h=im.size[0]*scale, im.size[1]*scale+14
        if x+w>maxw and x>0: x=0; y+=rowh+8; rowh=0
        pos.append((x,y)); x+=w+8; rowh=max(rowh,h)
    H=y+rowh; W=maxw
    canvas=Image.new('RGBA',(W,H),bg+(255,))
    d=ImageDraw.Draw(canvas)
    for (name,im),(px,py) in zip(ims,pos):
        big=im.resize((im.size[0]*scale,im.size[1]*scale),Image.NEAREST)
        # grid every 32px
        for gx in range(0,big.size[0],32*scale): d.line([(px+gx,py+14),(px+gx,py+14+big.size[1])],fill=(90,90,100))
        for gy in range(0,big.size[1],32*scale): d.line([(px,py+14+gy),(px+big.size[0],py+14+gy)],fill=(90,90,100))
        canvas.alpha_composite(big,(px,py+14))
        d.text((px,py),f"{name} {im.size}",fill=(255,255,200))
    canvas.save(out)
if __name__=='__main__':
    out=sys.argv[1]; sc=int(sys.argv[2]); contact(sys.argv[3:],out,sc)
