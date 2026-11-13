import cv2, numpy as np, json
from scipy import ndimage as ndi
FR='/home/claude/work/frames'
D=json.load(open('trackD.json'))
med=np.nan_to_num(np.load('B_med.npy')).clip(0,255).astype(np.float32)
mask=np.load('C_mask.npy').astype(np.uint8);H,W=mask.shape
mask_d=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))>0
mask_er=cv2.erode(mask,np.ones((5,5),np.uint8))>0
rx0,ry0=80,930
rimg=cv2.imread(f'{FR}/star/0431.jpg')[930:1120,80:620]
rmask=np.load('rock_mask.npy').astype(np.uint8)
RH,RW=rmask.shape
sift=cv2.SIFT_create(nfeatures=3000)
kr,dr=sift.detectAndCompute(cv2.cvtColor(rimg,cv2.COLOR_BGR2GRAY),cv2.erode(rmask,np.ones((5,5),np.uint8))*255)
print('rock kp',len(kr))
bf=cv2.BFMatcher(cv2.NORM_L2)
rg=cv2.cvtColor(rimg,cv2.COLOR_BGR2GRAY).astype(np.float32)
ONES=np.full((1280,720),255,np.uint8)
rockT={}
prev=None
for f in range(1,451):
    im=cv2.imread(f'{FR}/star/{f:04d}.jpg');g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    kf,df=sift.detectAndCompute(g,None)
    A=None
    if df is not None:
        m=bf.knnMatch(dr,df,k=2);good=[a for a,b in m if a.distance<0.75*b.distance]
        if len(good)>=12:
            src=np.float32([kr[a.queryIdx].pt for a in good]);dst=np.float32([kf[a.trainIdx].pt for a in good])
            A,inl=cv2.estimateAffinePartial2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=3,maxIters=5000)
            if A is not None and inl.sum()<12: A=None
    if A is None and prev is not None: A=prev
    if A is None: continue
    try:
        cc,A2=cv2.findTransformECCWithMask(rg,g.astype(np.float32),cv2.erode(rmask,np.ones((5,5),np.uint8))*255,ONES,A.astype(np.float32),cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,60,1e-6),5)
        A=A2
    except cv2.error: pass
    rockT[f]=A;prev=A
print('rock tracked',len(rockT))
added={}
for f in range(1,451):
    o=D['star'][f-1]
    if not o or f not in rockT: continue
    Af=np.array(o['A'],np.float32)  # face ref -> frame
    Ar=rockT[f]                     # rock tpl -> frame
    # rock mask & pred in face ref coords: face_ref -> frame -> rock_tpl : inv(Ar) o Af
    Af3=np.vstack([Af,[0,0,1]]);Ar3=np.vstack([Ar,[0,0,1]])
    M=(np.linalg.inv(Ar3)@Af3)[:2]   # face ref -> rock tpl
    rm=cv2.warpAffine(rmask*255,M.astype(np.float32),(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_NEAREST)>0
    ov=rm&mask_d
    if ov.sum()<50: continue
    im=cv2.imread(f'{FR}/star/{f:04d}.jpg').astype(np.float32)
    w=cv2.warpAffine(im,Af,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR)
    rp=cv2.warpAffine(rimg.astype(np.float32),M.astype(np.float32),(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR)
    # gains: face from non-overlap eroded mask; rock from rock pixels outside the face
    fm=mask_er&~rm
    gf=np.array([np.median(w[...,c][fm]/np.maximum(med[...,c][fm],1)) for c in range(3)]) if fm.sum()>300 else np.ones(3)
    # rock gain: use rock pixels in frame outside face region
    rfull=cv2.warpAffine(rmask*255,Ar.astype(np.float32),(720,1280),flags=cv2.INTER_NEAREST)>0
    facefull=cv2.warpAffine(mask_d.astype(np.uint8)*255,Af,(720,1280),flags=cv2.INTER_NEAREST)>0
    rpf=cv2.warpAffine(rimg.astype(np.float32),Ar.astype(np.float32),(720,1280),flags=cv2.INTER_LINEAR)
    sel=rfull&~facefull
    gr=np.array([np.median(im[...,c][sel]/np.maximum(rpf[...,c][sel],1)) for c in range(3)]) if sel.sum()>300 else np.ones(3)
    wb=cv2.GaussianBlur(w,(5,5),0)
    dfc=np.abs(wb-cv2.GaussianBlur(med*gf,(5,5),0)).mean(axis=2)
    drk=np.abs(wb-cv2.GaussianBlur(rp*gr,(5,5),0)).mean(axis=2)
    rockpix=(drk<dfc)&ov
    rockpix=cv2.medianBlur(rockpix.astype(np.uint8)*255,7)>0
    frac=rockpix.sum()/max(1,ov.sum())
    if frac<0.5:   # face in front of the rock here
        continue
    # rock in front: the whole overlap (rock shape) is occluder
    added[f]=float(frac)
    occ=np.unpackbits(np.load(f'occE/star_{f:04d}.npy'))[:H*W].reshape(H,W).astype(bool)
    occ=occ|ov
    np.save(f'occE/star_{f:04d}.npy',np.packbits(occ))
print('frames with rock in front',len(added),sorted(added)[:5],sorted(added)[-5:])
json.dump({str(k):v for k,v in added.items()},open('rock_added.json','w'))
