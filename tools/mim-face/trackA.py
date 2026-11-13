import cv2, numpy as np, json, sys, os
FR='/home/claude/work/frames'
ref=cv2.imread(f'{FR}/silly/0240.jpg')
x0,y0,x1,y1=200,548,526,900
mask=np.zeros(ref.shape[:2],np.uint8)
cv2.ellipse(mask,((x0+x1)//2,(y0+y1)//2),((x1-x0)//2,(y1-y0)//2),0,0,360,255,-1)
sift=cv2.SIFT_create(nfeatures=4000)
g=cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)
kr,dr=sift.detectAndCompute(g,mask)
print('ref kp',len(kr))
bf=cv2.BFMatcher(cv2.NORM_L2)
res={}
for film in ['silly','wonky','star']:
    out=[]
    n=len(os.listdir(f'{FR}/{film}'))
    for i in range(1,n+1):
        im=cv2.imread(f'{FR}/{film}/{i:04d}.jpg',0)
        kf,df=sift.detectAndCompute(im,None)
        if df is None or len(kf)<10: out.append(None);continue
        m=bf.knnMatch(dr,df,k=2)
        good=[a for a,b in m if a.distance<0.75*b.distance]
        if len(good)<8: out.append(None);continue
        src=np.float32([kr[a.queryIdx].pt for a in good]);dst=np.float32([kf[a.trainIdx].pt for a in good])
        M,inl=cv2.estimateAffinePartial2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=4,maxIters=5000,confidence=0.995)
        ni=int(inl.sum()) if inl is not None else 0
        out.append({'M':M.tolist() if M is not None else None,'n':ni,'g':len(good)})
    res[film]=out
    ok=sum(1 for o in out if o and o['n']>=12)
    print(film,n,'ok',ok)
json.dump(res,open('trackA.json','w'))
