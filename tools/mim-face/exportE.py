import cv2, numpy as np, json
from scipy import ndimage as ndi
FR='/home/claude/work/frames'
D=json.load(open('trackD.json'))
med=np.nan_to_num(np.load('B_med.npy')).clip(0,255).astype(np.float32)
mask=np.load('C_mask.npy').astype(np.uint8)
H,W=mask.shape
mask_er=cv2.erode(mask,np.ones((5,5),np.uint8))>0
mask_d=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))>0
ONES=np.full((1280,720),255,np.uint8)
predb=cv2.GaussianBlur(med,(3,3),0)
R=2
def tolerant_diff(wb,pred):
    best=None
    P=np.pad(pred,((R,R),(R,R),(0,0)),mode='edge')
    for dy in range(-R,R+1):
        for dx in range(-R,R+1):
            s=P[R+dy:R+dy+H,R+dx:R+dx+W]
            d=np.abs(wb-s).mean(axis=2)
            best=d if best is None else np.minimum(best,d)
    return best
def rle(b):
    # b: 2D bool; row-major runs starting with zeros
    f=b.ravel().astype(np.uint8)
    runs=[];cur=0;n=0
    for v in f:
        if v==cur: n+=1
        else: runs.append(n);cur=v;n=1
    runs.append(n)
    return runs
def frame_data(im,A,keep_occ=True):
    w=cv2.warpAffine(im,A,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR).astype(np.float32)
    v=cv2.warpAffine(ONES[:im.shape[0],:im.shape[1]],A,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_NEAREST)>0
    wb=cv2.GaussianBlur(w,(3,3),0)
    m=mask_er&v
    occ=np.zeros((H,W),bool)
    for it in range(2):
        mm=m&~occ
        if mm.sum()<200: mm=m
        g=np.array([np.median(w[...,c][mm]/np.maximum(med[...,c][mm],1)) for c in range(3)])
        d=tolerant_diff(wb,predb*g)
        occ=(d>45)&mask_d&v
    lab,n=ndi.label(occ)
    if n:
        sz=ndi.sum(occ,lab,range(1,n+1))
        keep=np.isin(lab,1+np.nonzero(sz>=60)[0])
        occ=keep
    if occ.any():
        occ=cv2.morphologyEx(occ.astype(np.uint8),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
        occ=cv2.dilate(occ,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))>0
        occ=occ&mask_d&v
    return g,occ
def pack_occ(occ):
    if not occ.any(): return None
    h2=cv2.resize(occ.astype(np.float32),(W//2,H//2),interpolation=cv2.INTER_AREA)>0.25
    ys,xs=np.nonzero(h2)
    if len(xs)==0: return None
    x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
    sub=h2[y0:y1,x0:x1]
    return {'b':[int(x0),int(y0),int(x1-x0),int(y1-y0)],'r':rle(sub)}
out={}
for film in ['silly','wonky','star']:
    fr=[];occs=[];nocc=0
    for i,o in enumerate(D[film]):
        f=i+1
        if not o: fr.append(0);continue
        A=np.array(o['A'],np.float32)
        im=cv2.imread(f'{FR}/{film}/{f:04d}.jpg')
        g,occ=frame_data(im,A)
        np.save(f'occE/{film}_{f:04d}.npy',np.packbits(occ))
        p=pack_occ(occ)
        oi=-1
        if p: occs.append(p);oi=len(occs)-1;nocc+=1
        a=A.ravel().tolist()
        fr.append([round(a[0],5),round(a[1],5),round(a[2],2),round(a[3],5),round(a[4],5),round(a[5],2),round(float(g[2]),3),round(float(g[1]),3),round(float(g[0]),3),oi])
    out[film]={'f':fr,'o':occs}
    print(film,'frames',sum(1 for x in fr if x),'with occ',nocc)
json.dump(out,open('exportE.json','w'),separators=(',',':'))
import os;print('size',os.path.getsize('exportE.json'))
