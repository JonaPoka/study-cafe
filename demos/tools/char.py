import json, os
from PIL import Image
U=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','assets','characters')
S=os.path.join(U,'spritesheets')
PAL={'body':json.load(open(f'{U}/palette_definitions/body/body_ulpc.json')),
     'hair':json.load(open(f'{U}/palette_definitions/hair/hair_ulpc.json')),
     'cloth':json.load(open(f'{U}/palette_definitions/cloth/cloth_ulpc.json'))}
BASE={'body':'light','hair':'orange','cloth':'white'}
_cache={}
def sheet(path,anim):
    k=(path,anim)
    if k not in _cache:
        _cache[k]=Image.open(f'{S}/{path}/{anim}.png').convert('RGBA')
    return _cache[k]
def recolor(im,mat,name):
    if not mat or not name or name==BASE[mat]: return im
    src=[c.upper() for c in PAL[mat][BASE[mat]]]; dst=PAL[mat][name]
    m={}
    for a,b in zip(src,dst):
        m[tuple(int(a[i:i+2],16) for i in (1,3,5))]=tuple(int(b[i:i+2],16) for i in (1,3,5))
    px=im.load(); out=im.copy(); po=out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r,g,b,a=px[x,y]
            if a and (r,g,b) in m: po[x,y]=m[(r,g,b)]+(a,)
    return out
ROW={'up':0,'left':1,'down':2,'right':3}
def layers(spec):
    bt=spec.get('body','female'); thin='thin' if bt=='female' else 'male'
    L=[('body/bodies/'+bt,10,'body',spec['skin'])]
    legs=spec.get('legs','pants')
    if legs=='pants': L.append(('legs/pants/'+thin,20,'cloth',spec['legsColor']))
    elif legs=='skirt': L.append(('legs/skirts/plain/thin',20,'cloth',spec['legsColor']))
    L.append(('feet/shoes/basic/'+thin,15,'cloth',spec.get('shoes','black')))
    top=spec.get('top','tshirt')
    tp={'cardigan':'torso/clothes/longsleeve/longsleeve2_cardigan/','longsleeve':'torso/clothes/longsleeve/longsleeve/','tshirt':'torso/clothes/shortsleeve/tshirt/'}[top]+bt
    L.append((tp,35,'cloth',spec['topColor']))
    if spec.get('scarf'): L.append(('neck/scarf',90,'cloth',spec['scarf']))
    hd='female' if bt=='female' else 'male'
    L+= [('head/heads/human/'+hd,100,'body',spec['skin']),('head/faces/'+hd+'/neutral',101,'body',spec['skin']),('head/nose/button/adult',105,'body',spec['skin']),('eyes/eyebrows/thin/adult',106,'hair',spec['hairColor'])]
    if spec.get('glasses'): L.append(('facial/glasses/round/adult',115,None,None))
    h=spec.get('hair','long')
    if h=='ponytail':
        L+=[('hair/ponytail2/adult/fg',120,'hair',spec['hairColor']),('hair/ponytail2/adult/bg',9,'hair',spec['hairColor'])]
    else:
        L.append(('hair/'+h+'/adult',120,'hair',spec['hairColor']))
    return sorted(L,key=lambda t:t[1])
_rc={}
def frame(spec,anim,direction,i):
    out=Image.new('RGBA',(64,64))
    for path,z,mat,col in layers(spec):
        if not os.path.exists(f'{S}/{path}/{anim}.png'): continue
        k=(path,anim,mat,col)
        if k not in _rc: _rc[k]=recolor(sheet(path,anim),mat,col)
        sh=_rc[k]; r=ROW[direction]
        if sh.size[1]<256: r=0
        cell=sh.crop((i*64,r*64,i*64+64,r*64+64))
        out.alpha_composite(cell)
    return out
