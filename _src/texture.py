# -*- coding: utf-8 -*-
"""Procedural 'graffiti wall' texture built from the site's own tag lettering (no third-party imagery).

    python3 _src/texture.py      (requires: pip install numpy pillow cairosvg)

Writes docs/assets/img/bg/wall.webp and wall-1100.webp. Deterministic (fixed seed)."""
import io, os, numpy as np, cairosvg
from PIL import Image, ImageFilter, ImageDraw, ImageChops
SRC=os.path.dirname(os.path.abspath(__file__)); IMG=os.path.join(os.path.dirname(SRC),"docs","assets","img")+os.sep; SVG=os.path.join(SRC,"svg")+os.sep
W,H=1920,1280; rng=np.random.default_rng(852)
def noise(scale,blur=0):
    a=rng.random((max(2,H//scale+2),max(2,W//scale+2))).astype(np.float32)
    im=Image.fromarray((a*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)
    if blur: im=im.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(im,dtype=np.float32)/255-0.5
# 1) concrete base
base=11+ noise(420)*9 + noise(140)*7 + noise(46)*5 + noise(14)*4 + noise(4)*3.2 + noise(1)*4.2
# 2) faint block / mortar grid with hand jitter
mort=Image.new("L",(W,H),0); d=ImageDraw.Draw(mort); bh=86; y=0; r=0
while y<H+bh:
    yy=y+int(rng.integers(-3,4)); d.line([(0,yy),(W,yy+int(rng.integers(-4,5)))],fill=255,width=2)
    x=-int(rng.integers(0,200)) + (r%2)*112
    while x<W: d.line([(x,yy),(x+int(rng.integers(-3,4)),yy+bh)],fill=255,width=2); x+=int(rng.integers(190,250))
    y+=bh; r+=1
mort=np.asarray(mort.filter(ImageFilter.GaussianBlur(1.6)),dtype=np.float32)/255
base-= mort*(3.2+noise(60)*3)
# 3) tags (site's own lettering) sprayed on the wall
def tag(path,width,rot,alpha,blur=0.8):
    svg=open(SVG+path,encoding="utf-8").read().replace('#000','#fff').replace('preserveAspectRatio="none"','')
    im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=width))).convert("RGBA")
    a=im.split()[3].rotate(rot,expand=True,resample=Image.BICUBIC)
    if blur: a=a.filter(ImageFilter.GaussianBlur(blur))
    return a,alpha
layer=np.zeros((H,W),dtype=np.float32)
def put(path,width,rot,alpha,cx,cy,blur=0.8):
    a,al=tag(path,width,rot,alpha,blur); aw,ah=a.size; x0=int(cx*W-aw/2); y0=int(cy*H-ah/2)
    arr=np.asarray(a,dtype=np.float32)/255*al
    xs,ys=max(0,x0),max(0,y0); xe,ye=min(W,x0+aw),min(H,y0+ah)
    if xe<=xs or ye<=ys: return
    sub=arr[ys-y0:ye-y0,xs-x0:xe-x0]; layer[ys:ye,xs:xe]=np.maximum(layer[ys:ye,xs:xe],sub)
    # drips under the tag
    dr=Image.new("L",(W,H),0); dd=ImageDraw.Draw(dr)
    for _ in range(int(rng.integers(2,6))):
        px=int(rng.integers(xs,xe)) if xe>xs else xs; col=layer[ys:ye,px]; nz=np.nonzero(col>al*0.5)[0]
        if len(nz)==0: continue
        py=ys+int(nz.max()); ln=int(rng.integers(40,230)); wd=int(rng.integers(2,6))
        dd.line([(px,py-4),(px,py+ln)],fill=255,width=wd); dd.ellipse([px-wd,py+ln-wd,px+wd,py+ln+wd],fill=255)
    layer[:]=np.maximum(layer,np.asarray(dr.filter(ImageFilter.GaussianBlur(0.9)),dtype=np.float32)/255*al*0.8)
put("signature.svg",1150,-9,0.105,0.30,0.30,1.2)
put("works.svg",760,7,0.075,0.80,0.20)
put("profile.svg",620,-5,0.060,0.14,0.80)
put("contact.svg",700,4,0.070,0.66,0.74)
put("hobby.svg",420,-12,0.050,0.50,0.52)
put("skill-set.svg",520,10,0.045,0.90,0.52)
put("arrow.svg",900,-3,0.060,0.62,0.40,1.0)
put("arrow.svg",760,176,0.045,0.24,0.60,1.0)
put("frame.svg",430,14,0.055,0.93,0.86)
put("frame.svg",300,-20,0.040,0.06,0.16)
put("more.svg",300,-8,0.050,0.40,0.92)
put("signature.svg",520,12,0.055,0.86,0.94,1.0)
# worn paint: break the tags up with noise
wear=np.clip(0.62+noise(18)*1.5+noise(3)*0.9,0.12,1)
layer*=wear
# 4) spray speckle clusters
sp=Image.new("L",(W,H),0); ds=ImageDraw.Draw(sp)
for _ in range(26):
    cx,cy=rng.integers(0,W),rng.integers(0,H); rad=rng.integers(40,170)
    for _ in range(int(rng.integers(60,260))):
        ang=rng.random()*6.283; rr=abs(rng.normal(0,rad/2.4)); x=cx+np.cos(ang)*rr; y=cy+np.sin(ang)*rr; s=rng.random()*1.6+0.4
        ds.ellipse([x-s,y-s,x+s,y+s],fill=int(rng.integers(90,255)))
layer=np.maximum(layer,np.asarray(sp.filter(ImageFilter.GaussianBlur(0.5)),dtype=np.float32)/255*0.06)
g=base+layer*255
# 5) vignette + tone
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); vx=(xx/W-0.5)*1.15; vy=(yy/H-0.5)*1.05
vig=np.clip(1-(vx*vx+vy*vy)*1.35,0.25,1)
g=np.clip(g*vig,0,255)
tint_c=noise(520); tint_w=noise(380)
rgb=np.stack([g*(1.0+tint_w*0.10-tint_c*0.04), g*(1.0+tint_c*0.04), g*(1.03+tint_c*0.12-tint_w*0.05)],axis=-1)
out=Image.fromarray(np.clip(rgb,0,255).astype(np.uint8),"RGB")
os.makedirs(IMG+"bg",exist_ok=True)
out.save(IMG+"bg/wall.webp","WEBP",quality=84,method=6); out.resize((1100,733),Image.LANCZOS).save(IMG+"bg/wall-1100.webp","WEBP",quality=80,method=6)
print("wall",os.path.getsize(IMG+"bg/wall.webp")//1024,"KB | sm",os.path.getsize(IMG+"bg/wall-1100.webp")//1024,"KB | mean",round(float(g.mean()),1),"max",round(float(g.max()),1))
