import cv2, numpy as np, json, os
exec(open('exportE.py').read().split("out={}")[0])
D=json.load(open('trackD.json'))
E=json.load(open('exportE.json'))
out={'v':1,'fps':30,'W':W,'H':H}
# silhouette for the under-fill (2 px bigger than the drawn face, so its outline is covered too)
md=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
cnts,_=cv2.findContours(md,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
c=max(cnts,key=cv2.contourArea)
ap=cv2.approxPolyDP(c,1.0,True)[:,0,:]
out['sil']=[int(v) for v in ap.ravel()]
ys,xs=np.nonzero(mask)
out['c']=[round(float(xs.mean()),1),round(float(ys.mean()),1)];out['area']=int(len(xs))
out['bb']=[int(xs.min()),int(ys.min()),int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)]
hsv=cv2.cvtColor(med.astype(np.uint8),cv2.COLOR_BGR2HSV)
paper=(mask>0)&(hsv[...,2]>200)&(hsv[...,1]<40)
pc=[float(np.median(med[...,ch][paper])) for ch in (2,1,0)]
out['paper']=[round(v) for v in pc]
print('paper',out['paper'],'sil pts',len(ap))
for film in ['silly','wonky','star']:
    fr=E[film]['f'];occs=[]
    nf=[]
    for i,x in enumerate(fr):
        f=i+1
        if not x: nf.append(0);continue
        occ=np.unpackbits(np.load(f'occE/{film}_{f:04d}.npy'))[:H*W].reshape(H,W).astype(bool)
        p=pack_occ(occ)
        oi=-1
        if p: occs.append(p);oi=len(occs)-1
        nf.append(x[:9]+[oi])
    # trailing zeros trimmed
    while nf and nf[-1]==0: nf.pop()
    out[film]={'f':nf,'o':occs}
    print(film,len(nf),'occ',len(occs))
out['poster']=json.load(open('poster_track.json'))
s=json.dumps(out,separators=(',',':'))
open('face.json','w').write(s)
import gzip;print('size',len(s),'gz',len(gzip.compress(s.encode())))
