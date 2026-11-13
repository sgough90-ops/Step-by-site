import cv2, numpy as np, json, os, sys
FR='/home/claude/work/frames'
BX0,BY0=150,500
med=np.nan_to_num(np.load('B_med.npy')).clip(0,255).astype(np.float32)
mask=np.load('C_mask.npy').astype(np.uint8)
H,W=mask.shape
medu=med.astype(np.uint8)
refg=cv2.cvtColor(medu,cv2.COLOR_BGR2GRAY).astype(np.float32)
mask_er=(cv2.erode(mask,np.ones((5,5),np.uint8))*255).astype(np.uint8)
mask_d=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
ONES=np.full((1280,720),255,np.uint8)
sift=cv2.SIFT_create(nfeatures=5000)
kt,dt=sift.detectAndCompute(cv2.cvtColor(medu,cv2.COLOR_BGR2GRAY),mask_er)
print('template kp',len(kt))
bf=cv2.BFMatcher(cv2.NORM_L2)
ys,xs=np.nonzero(mask_er)
idx=np.random.RandomState(0).choice(len(xs),300,replace=False)
SP=np.float32(np.stack([xs[idx],ys[idx]],1))[None]
EM=mask_er>0
def warp_in(im,A):
    return cv2.warpAffine(im,A,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR)
def valid_in(A):
    return cv2.warpAffine(ONES,A,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_NEAREST)>0
def score(im,A):
    w=warp_in(im,A).astype(np.float32);v=valid_in(A)
    m=EM&v
    if m.sum()<500: return 99,None,None,None
    g=np.array([np.median(w[...,c][m]/np.maximum(med[...,c][m],1)) for c in range(3)])
    d=np.abs(cv2.GaussianBlur(w,(3,3),0)-cv2.GaussianBlur(med*g,(3,3),0)).mean(axis=2)
    return float(np.median(d[m])),w,v,g
def ecc(g,A,gs=5,msk=None):
    try:
        cc,A2=cv2.findTransformECCWithMask(refg,g,mask_er if msk is None else msk,ONES,A.astype(np.float32).copy(),cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,80,1e-6),gs)
        return A2
    except cv2.error: return None
def disp(A,B):
    return float(np.abs(cv2.transform(SP,A)-cv2.transform(SP,B)).max())
film=sys.argv[1];F0=int(sys.argv[2]);F1=int(sys.argv[3])
for film in [film]:
    res=[];prevA=None
    for f in range(F0,F1+1):
        im=cv2.imread(f'{FR}/{film}/{f:04d}.jpg');g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
        cands=[]
        kf,df=sift.detectAndCompute(g.astype(np.uint8),None)
        if df is not None and len(kf)>10:
            m=bf.knnMatch(dt,df,k=2)
            good=[a for a,b in m if a.distance<0.75*b.distance]
            if len(good)>=10:
                src=np.float32([kt[a.queryIdx].pt for a in good]);dst=np.float32([kf[a.trainIdx].pt for a in good])
                A0,inl=cv2.estimateAffine2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=3,maxIters=8000,confidence=0.998)
                if A0 is not None and inl.sum()>=10:
                    cands.append(('sift',A0,int(inl.sum())))
                Ap,inl2=cv2.estimateAffinePartial2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=3,maxIters=8000,confidence=0.998)
                if Ap is not None and inl2.sum()>=10: cands.append(('siftp',Ap,int(inl2.sum())))
        if prevA is not None: cands.append(('prev',prevA,0))
        best=None
        for name,A0,ni in cands:
            for gs in (5,9):
                A=ecc(g,A0,gs)
                if A is None: continue
                if name!='prev' and disp(A,A0)>20: continue
                e,w,v,gn=score(im,A)
                if best is None or e<best[0]: best=(e,A,name+'+ecc'+str(gs),ni)
                break
            e,w,v,gn=score(im,A0)
            if name!='prev' and (best is None or e<best[0]): best=(e,A0,name,ni)
        if best is None or best[0]>30:
            res.append(None);prevA=None;continue
        e,A,how,ni=best
        # visibility
        vis=float((valid_in(A)&(mask>0)).sum()/mask.sum())
        if vis<0.03: res.append(None);prevA=None;continue
        res.append({'A':A.tolist(),'err':e,'how':how,'n':ni,'vis':vis})
        prevA=A
    json.dump(res,open(f'trackD_{film}_{F0}.json','w'))
    ok=[r for r in res if r]
    print(film,len(ok),'err>9',sum(r['err']>9 for r in ok),'how',{h:sum(1 for r in ok if r['how']==h) for h in set(r['how'] for r in ok)})
