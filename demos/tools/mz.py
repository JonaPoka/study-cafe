import sys,subprocess,os
ZOOM=os.path.join(os.path.dirname(os.path.abspath(__file__)),'zoom.py')
from PIL import Image
# args: out scale then groups of path x y w h
out=sys.argv[1]; s=sys.argv[2]; a=sys.argv[3:]
ims=[]
for i in range(0,len(a),5):
    p,x,y,w,h=a[i:i+5]
    subprocess.run([sys.executable,'-I',ZOOM,p,x,y,w,h,s,f'_t{i}.png'],check=True)
    ims.append(Image.open(f'_t{i}.png'))
W=max(i.size[0] for i in ims); H=sum(i.size[1]+6 for i in ims)
c=Image.new('RGBA',(W,H),(30,30,36,255)); y=0
for i in ims: c.paste(i,(0,y)); y+=i.size[1]+6
c.save(out)
