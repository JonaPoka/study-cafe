import sys
from PIL import Image, ImageDraw
p,x,y,w,h,s,out=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
im=Image.open(p).convert('RGBA').crop((x,y,x+w,y+h))
pad=28
bg=Image.new('RGBA',(w*s+pad,h*s+pad),(60,60,70,255))
d=ImageDraw.Draw(bg)
# checker
for cy in range(0,h,8):
  for cx in range(0,w,8):
    if (cx//8+cy//8)%2: d.rectangle([pad+cx*s,pad+cy*s,pad+(cx+8)*s-1,pad+(cy+8)*s-1],fill=(75,75,85,255))
bg.alpha_composite(im.resize((w*s,h*s),Image.NEAREST),(pad,pad))
for gx in range(0,w+1,16):
  c=(255,80,80,255) if (x+gx)%32==0 else (255,200,80,140)
  d.line([(pad+gx*s,pad),(pad+gx*s,pad+h*s)],fill=c,width=1)
  if (x+gx)%32==0: d.text((pad+gx*s+2,2),str(x+gx),fill=(255,255,255))
for gy in range(0,h+1,16):
  c=(255,80,80,255) if (y+gy)%32==0 else (255,200,80,140)
  d.line([(pad,pad+gy*s),(pad+w*s,pad+gy*s)],fill=c,width=1)
  if (y+gy)%32==0: d.text((1,pad+gy*s+2),str(y+gy),fill=(255,255,255))
bg.save(out)
